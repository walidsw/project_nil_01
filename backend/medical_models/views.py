from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import MedicalDomain, InputType, ResearchPaper, MedicalModel, ModelCategory
from .serializers import (
    MedicalDomainSerializer, InputTypeSerializer, ResearchPaperSerializer,
    MedicalModelSerializer, MedicalModelListSerializer, ModelComparisonSerializer
)


class MedicalDomainViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for medical domains"""
    queryset = MedicalDomain.objects.all()
    serializer_class = MedicalDomainSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def models(self, request, pk=None):
        """Get all models for a specific domain"""
        domain = self.get_object()
        models = MedicalModel.objects.filter(domain=domain, status='active')
        serializer = MedicalModelListSerializer(models, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def categories(self, request, pk=None):
        """Get all categories for a specific domain"""
        domain = self.get_object()
        categories = ModelCategory.objects.filter(domain=domain)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class InputTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for input types"""
    queryset = InputType.objects.all()
    serializer_class = InputTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ResearchPaperViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for research papers"""
    queryset = ResearchPaper.objects.all()
    serializer_class = ResearchPaperSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'authors', 'journal', 'doi', 'arxiv_id']
    filterset_fields = ['year', 'journal']


class MedicalModelViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for medical models"""
    queryset = MedicalModel.objects.filter(status='active')
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name', 'description', 'domain__name']
    filterset_fields = ['domain', 'input_type', 'framework', 'status']

    def get_serializer_class(self):
        if self.action == 'list':
            return MedicalModelListSerializer
        return MedicalModelSerializer

    @action(detail=False, methods=['get'])
    def by_domain(self, request):
        """Get models filtered by domain"""
        domain_id = request.query_params.get('domain_id')
        if not domain_id:
            return Response(
                {'error': 'domain_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            domain = MedicalDomain.objects.get(id=domain_id)
            models = self.queryset.filter(domain=domain)
            serializer = self.get_serializer(models, many=True)
            return Response(serializer.data)
        except MedicalDomain.DoesNotExist:
            return Response(
                {'error': 'Domain not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def by_input_type(self, request):
        """Get models filtered by input type"""
        input_type_id = request.query_params.get('input_type_id')
        if not input_type_id:
            return Response(
                {'error': 'input_type_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            input_type = InputType.objects.get(id=input_type_id)
            models = self.queryset.filter(input_type=input_type)
            serializer = self.get_serializer(models, many=True)
            return Response(serializer.data)
        except InputType.DoesNotExist:
            return Response(
                {'error': 'Input type not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def compare_models(self, request):
        """Get models for comparison based on criteria"""
        serializer = ModelComparisonSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        domain_id = data['domain_id']
        input_type_id = data.get('input_type_id')
        category_id = data.get('category_id')
        
        # Build query
        query = Q(domain_id=domain_id, status='active')
        
        if input_type_id:
            query &= Q(input_type_id=input_type_id)
        
        if category_id:
            query &= Q(categories__id=category_id)
        
        models = self.queryset.filter(query).distinct()
        serializer = self.get_serializer(models, many=True)
        
        return Response({
            'models': serializer.data,
            'count': models.count(),
            'criteria': data
        })

    @action(detail=True, methods=['get'])
    def performance_metrics(self, request, pk=None):
        """Get detailed performance metrics for a model"""
        model = self.get_object()
        metrics = {
            'accuracy': model.accuracy,
            'precision': model.precision,
            'recall': model.recall,
            'f1_score': model.f1_score,
            'output_classes': model.output_classes,
        }
        return Response(metrics)


class ModelCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for model categories"""
    queryset = ModelCategory.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['domain']

    @action(detail=True, methods=['get'])
    def models(self, request, pk=None):
        """Get all models in a specific category"""
        category = self.get_object()
        models = category.models.filter(status='active')
        serializer = MedicalModelListSerializer(models, many=True)
        return Response(serializer.data)
