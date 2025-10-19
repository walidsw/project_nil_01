import os
import uuid
import logging
from django.conf import settings
from django.utils import timezone
from django.db import models
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import PredictionSession, ModelPrediction, PredictionResult, ComparativeAnalysis
from .serializers import (
    PredictionSessionSerializer, PredictionSessionListSerializer,
    ModelPredictionSerializer, PredictionRequestSerializer,
    FileUploadSerializer, BatchPredictionSerializer, PredictionStatusSerializer
)
from .tasks import process_prediction_session
from medical_models.models import MedicalModel, MedicalDomain, InputType

logger = logging.getLogger(__name__)


class PredictionSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for prediction sessions"""
    queryset = PredictionSession.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Filter by user if authenticated
        if self.request.user.is_authenticated:
            return PredictionSession.objects.filter(user=self.request.user)
        return PredictionSession.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PredictionSessionListSerializer
        return PredictionSessionSerializer

    @action(detail=False, methods=['post'])
    def upload_and_predict(self, request):
        """Upload file and start prediction session"""
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Save uploaded file
            uploaded_file = serializer.validated_data['file']
            file_extension = os.path.splitext(uploaded_file.name)[1]
            filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save file
            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            
            # Create prediction session
            session_id = str(uuid.uuid4())
            session = PredictionSession.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_id=session_id,
                domain=serializer.validated_data['domain'],
                input_type=serializer.validated_data['input_type'],
                input_file_path=file_path,
                input_metadata=serializer.validated_data.get('metadata', {}),
                status='pending'
            )
            
            # Start background processing
            process_prediction_session.delay(session_id)
            
            return Response({
                'session_id': session_id,
                'status': 'pending',
                'message': 'Prediction session started successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error creating prediction session: {str(e)}")
            return Response(
                {'error': 'Failed to create prediction session'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def batch_predict(self, request):
        """Upload multiple files and start batch prediction"""
        serializer = BatchPredictionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            session_ids = []
            
            for uploaded_file in serializer.validated_data['files']:
                # Save each file
                file_extension = os.path.splitext(uploaded_file.name)[1]
                filename = f"{uuid.uuid4()}{file_extension}"
                file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
                
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'wb') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
                
                # Create prediction session for each file
                session_id = str(uuid.uuid4())
                session = PredictionSession.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_id=session_id,
                    domain=serializer.validated_data['domain'],
                    input_type=serializer.validated_data['input_type'],
                    input_file_path=file_path,
                    input_metadata=serializer.validated_data.get('metadata', {}),
                    status='pending'
                )
                
                # Start background processing
                process_prediction_session.delay(session_id)
                session_ids.append(session_id)
            
            return Response({
                'session_ids': session_ids,
                'count': len(session_ids),
                'status': 'pending',
                'message': f'Batch prediction started for {len(session_ids)} files'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Error creating batch prediction: {str(e)}")
            return Response(
                {'error': 'Failed to create batch prediction'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """Get detailed status of a prediction session"""
        session = self.get_object()
        
        # Get prediction statistics
        total_predictions = session.predictions.count()
        completed_predictions = session.predictions.filter(status='completed').count()
        failed_predictions = session.predictions.filter(status='failed').count()
        processing_predictions = session.predictions.filter(status='processing').count()
        
        progress = {
            'total': total_predictions,
            'completed': completed_predictions,
            'failed': failed_predictions,
            'processing': processing_predictions,
            'percentage': (completed_predictions / total_predictions * 100) if total_predictions > 0 else 0
        }
        
        # Estimate completion time
        estimated_completion = None
        if processing_predictions > 0:
            avg_processing_time = session.predictions.filter(
                status='completed', processing_time__isnull=False
            ).aggregate(avg_time=models.Avg('processing_time'))['avg_time']
            
            if avg_processing_time:
                estimated_completion = timezone.now() + timezone.timedelta(
                    seconds=avg_processing_time * processing_predictions
                )
        
        response_data = {
            'session_id': session.session_id,
            'status': session.status,
            'progress': progress,
            'estimated_completion': estimated_completion,
        }
        
        # Include results if completed
        if session.status == 'completed':
            response_data['results'] = {
                'aggregated_result': session.aggregated_result,
                'confidence_score': session.confidence_score,
                'comparative_analysis': session.comparative_analysis
            }
        
        return Response(response_data)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get detailed results of a completed prediction session"""
        session = self.get_object()
        
        if session.status != 'completed':
            return Response(
                {'error': 'Prediction session not completed yet'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all predictions with detailed results
        predictions = session.predictions.filter(status='completed').select_related(
            'model', 'detailed_result'
        )
        
        results = []
        for prediction in predictions:
            result_data = {
                'model': {
                    'id': prediction.model.id,
                    'name': prediction.model.name,
                    'version': prediction.model.version,
                    'accuracy': prediction.model.accuracy,
                    'framework': prediction.model.framework,
                },
                'prediction': {
                    'predicted_class': prediction.predicted_class,
                    'confidence': prediction.confidence_score,
                    'processing_time': prediction.processing_time,
                },
                'detailed_result': prediction.detailed_result.raw_output if prediction.detailed_result else None,
            }
            results.append(result_data)
        
        return Response({
            'session_id': session.session_id,
            'domain': session.domain,
            'input_type': session.input_type,
            'aggregated_result': session.aggregated_result,
            'consensus_score': session.confidence_score,
            'individual_results': results,
            'comparative_analysis': session.comparative_analysis,
            'completed_at': session.completed_at,
        })

    @action(detail=False, methods=['get'])
    def by_domain(self, request):
        """Get prediction sessions filtered by domain"""
        domain = request.query_params.get('domain')
        if not domain:
            return Response(
                {'error': 'domain parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sessions = self.get_queryset().filter(domain__iexact=domain)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent prediction sessions"""
        limit = int(request.query_params.get('limit', 10))
        sessions = self.get_queryset().order_by('-created_at')[:limit]
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)


class ModelPredictionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for individual model predictions"""
    queryset = ModelPrediction.objects.all()
    serializer_class = ModelPredictionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def detailed_result(self, request, pk=None):
        """Get detailed prediction result"""
        prediction = self.get_object()
        
        if not prediction.detailed_result:
            return Response(
                {'error': 'No detailed result available'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'prediction_id': prediction.id,
            'model_name': prediction.model.name,
            'predicted_class': prediction.detailed_result.predicted_class,
            'class_probabilities': prediction.detailed_result.class_probabilities,
            'uncertainty_score': prediction.detailed_result.uncertainty_score,
            'raw_output': prediction.detailed_result.raw_output,
            'model_version': prediction.detailed_result.model_version,
            'preprocessing_applied': prediction.detailed_result.preprocessing_applied,
        })


class PredictionStatusView(generics.RetrieveAPIView):
    """Get status of a prediction session by session_id"""
    serializer_class = PredictionStatusSerializer
    
    def get_object(self):
        session_id = self.kwargs.get('session_id')
        return get_object_or_404(PredictionSession, session_id=session_id)
    
    def retrieve(self, request, *args, **kwargs):
        session = self.get_object()
        
        # Get prediction statistics
        total_predictions = session.predictions.count()
        completed_predictions = session.predictions.filter(status='completed').count()
        failed_predictions = session.predictions.filter(status='failed').count()
        processing_predictions = session.predictions.filter(status='processing').count()
        
        progress = {
            'total': total_predictions,
            'completed': completed_predictions,
            'failed': failed_predictions,
            'processing': processing_predictions,
            'percentage': (completed_predictions / total_predictions * 100) if total_predictions > 0 else 0
        }
        
        response_data = {
            'session_id': session.session_id,
            'status': session.status,
            'progress': progress,
        }
        
        # Include results if completed
        if session.status == 'completed':
            response_data['results'] = {
                'aggregated_result': session.aggregated_result,
                'confidence_score': session.confidence_score,
            }
        
        return Response(response_data)
