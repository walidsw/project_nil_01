"""
Celery tasks for handling prediction processing
"""
import os
import uuid
import logging
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from medical_models.models import MedicalModel
from .models import PredictionSession, ModelPrediction, PredictionResult, ComparativeAnalysis
try:
    from .ml_engine import inference_engine
    ML_ENGINE_AVAILABLE = True
except ImportError:
    from .mock_ml_engine import mock_inference_engine as inference_engine
    ML_ENGINE_AVAILABLE = False
from .analysis import ComparativeAnalyzer

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def process_prediction_session(self, session_id: str):
    """Process a complete prediction session with multiple models"""
    try:
        session = PredictionSession.objects.get(session_id=session_id)
        session.status = 'processing'
        session.save()
        
        logger.info(f"Starting prediction session: {session_id}")
        
        # Get all models for the domain and input type
        models = MedicalModel.objects.filter(
            domain__name=session.domain,
            input_type__name=session.input_type,
            status='active'
        )
        
        if not models.exists():
            session.status = 'failed'
            session.save()
            return {'error': 'No active models found for the specified criteria'}
        
        # Create model predictions
        predictions = []
        for model in models:
            prediction = ModelPrediction.objects.create(
                session=session,
                model=model,
                status='pending'
            )
            predictions.append(prediction)
        
        # Process each model prediction
        results = []
        for prediction in predictions:
            try:
                result = process_single_model_prediction.delay(prediction.id)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to start prediction for model {prediction.model.name}: {str(e)}")
                prediction.status = 'failed'
                prediction.error_message = str(e)
                prediction.save()
        
        # Wait for all predictions to complete
        completed_predictions = []
        for result in results:
            try:
                prediction_result = result.get(timeout=300)  # 5 minute timeout
                if prediction_result.get('success'):
                    completed_predictions.append(prediction_result)
            except Exception as e:
                logger.error(f"Prediction task failed: {str(e)}")
        
        # Perform comparative analysis
        if completed_predictions:
            analysis_result = perform_comparative_analysis.delay(session_id)
            analysis_result.get(timeout=60)  # 1 minute timeout
        
        session.status = 'completed'
        session.completed_at = timezone.now()
        session.save()
        
        logger.info(f"Completed prediction session: {session_id}")
        return {'success': True, 'session_id': session_id}
        
    except PredictionSession.DoesNotExist:
        logger.error(f"Prediction session not found: {session_id}")
        return {'error': 'Session not found'}
    except Exception as e:
        logger.error(f"Error processing prediction session {session_id}: {str(e)}")
        if 'session' in locals():
            session.status = 'failed'
            session.save()
        return {'error': str(e)}


@shared_task(bind=True)
def process_single_model_prediction(self, prediction_id: int):
    """Process prediction for a single model"""
    try:
        prediction = ModelPrediction.objects.get(id=prediction_id)
        prediction.status = 'processing'
        prediction.save()
        
        logger.info(f"Processing prediction for model: {prediction.model.name}")
        
        # Get input file path
        input_file_path = prediction.session.input_file_path
        if not input_file_path or not os.path.exists(input_file_path):
            raise ValueError(f"Input file not found: {input_file_path}")
        
        # Run inference
        start_time = timezone.now()
        result = inference_engine.run_inference(prediction.model, input_file_path)
        end_time = timezone.now()
        
        processing_time = (end_time - start_time).total_seconds()
        
        if result['success']:
            # Create detailed prediction result
            PredictionResult.objects.create(
                prediction=prediction,
                raw_output=result['predictions'],
                predicted_class=result['predictions']['predicted_class'],
                class_probabilities=result['predictions']['class_probabilities'],
                uncertainty_score=1.0 - result['predictions']['confidence'],
                model_version=result.get('model_version', '1.0'),
                preprocessing_applied=prediction.model.preprocessing_config
            )
            
            prediction.prediction_result = result['predictions']
            prediction.confidence_score = result['predictions']['confidence']
            prediction.processing_time = processing_time
            prediction.status = 'completed'
            prediction.completed_at = timezone.now()
            prediction.save()
            
            logger.info(f"Successfully processed prediction for model: {prediction.model.name}")
            return {'success': True, 'prediction_id': prediction_id}
        else:
            prediction.status = 'failed'
            prediction.error_message = result['error']
            prediction.save()
            
            logger.error(f"Prediction failed for model {prediction.model.name}: {result['error']}")
            return {'success': False, 'error': result['error']}
            
    except ModelPrediction.DoesNotExist:
        logger.error(f"Model prediction not found: {prediction_id}")
        return {'error': 'Prediction not found'}
    except Exception as e:
        logger.error(f"Error processing model prediction {prediction_id}: {str(e)}")
        if 'prediction' in locals():
            prediction.status = 'failed'
            prediction.error_message = str(e)
            prediction.save()
        return {'error': str(e)}


@shared_task(bind=True)
def perform_comparative_analysis(self, session_id: str):
    """Perform comparative analysis on completed predictions"""
    try:
        session = PredictionSession.objects.get(session_id=session_id)
        
        # Get all completed predictions
        completed_predictions = ModelPrediction.objects.filter(
            session=session,
            status='completed'
        ).select_related('model', 'detailed_result')
        
        if not completed_predictions.exists():
            logger.warning(f"No completed predictions found for session: {session_id}")
            return {'error': 'No completed predictions found'}
        
        # Perform analysis
        analyzer = ComparativeAnalyzer()
        analysis_result = analyzer.analyze_predictions(completed_predictions)
        
        # Store analysis results
        comparative_analysis, created = ComparativeAnalysis.objects.get_or_create(
            session=session,
            defaults=analysis_result
        )
        
        if not created:
            # Update existing analysis
            for key, value in analysis_result.items():
                setattr(comparative_analysis, key, value)
            comparative_analysis.save()
        
        # Update session with aggregated results
        session.aggregated_result = analysis_result
        session.confidence_score = analysis_result.get('consensus_score', 0.0)
        session.save()
        
        logger.info(f"Completed comparative analysis for session: {session_id}")
        return {'success': True, 'analysis': analysis_result}
        
    except PredictionSession.DoesNotExist:
        logger.error(f"Prediction session not found: {session_id}")
        return {'error': 'Session not found'}
    except Exception as e:
        logger.error(f"Error performing comparative analysis for session {session_id}: {str(e)}")
        return {'error': str(e)}


@shared_task(bind=True)
def cleanup_old_sessions(self, days_old: int = 30):
    """Clean up old prediction sessions and files"""
    try:
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days_old)
        
        # Find old sessions
        old_sessions = PredictionSession.objects.filter(created_at__lt=cutoff_date)
        
        deleted_count = 0
        for session in old_sessions:
            # Delete associated files
            if session.input_file_path and os.path.exists(session.input_file_path):
                try:
                    os.remove(session.input_file_path)
                except Exception as e:
                    logger.warning(f"Could not delete file {session.input_file_path}: {str(e)}")
            
            # Delete session (cascades to predictions and results)
            session.delete()
            deleted_count += 1
        
        logger.info(f"Cleaned up {deleted_count} old prediction sessions")
        return {'deleted_sessions': deleted_count}
        
    except Exception as e:
        logger.error(f"Error during cleanup: {str(e)}")
        return {'error': str(e)}
