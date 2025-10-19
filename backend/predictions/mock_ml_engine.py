"""
Mock ML Engine for testing without heavy ML dependencies
"""
import os
import json
import logging
import random
from typing import Dict, List, Any, Optional, Tuple
from django.conf import settings
from medical_models.models import MedicalModel

# Mock numpy functionality
class MockNumpy:
    @staticmethod
    def random():
        return MockNumpy()
    
    @staticmethod
    def random_sample(size):
        if isinstance(size, tuple):
            return [[random.random() for _ in range(size[1])] for _ in range(size[0])]
        return [random.random() for _ in range(size)]
    
    @staticmethod
    def array(data):
        return data
    
    @staticmethod
    def argmax(data):
        if isinstance(data, list):
            return data.index(max(data))
        return 0
    
    @staticmethod
    def sum(data):
        if isinstance(data, list):
            return sum(data)
        return data
    
    @staticmethod
    def mean(data):
        if isinstance(data, list):
            return sum(data) / len(data)
        return data
    
    @staticmethod
    def std(data):
        if isinstance(data, list):
            mean_val = sum(data) / len(data)
            variance = sum((x - mean_val) ** 2 for x in data) / len(data)
            return variance ** 0.5
        return 0.0
    
    @staticmethod
    def sqrt(value):
        return value ** 0.5
    
    @staticmethod
    def exp(value):
        return 2.718281828459045 ** value
    
    @staticmethod
    def sign(value):
        return 1 if value >= 0 else -1
    
    @staticmethod
    def pad(data, padding):
        return data  # Simple mock
    
    @staticmethod
    def expand_dims(data, axis):
        return [data]  # Simple mock
    
    @staticmethod
    def float32(value):
        return float(value)
    
    @staticmethod
    def int(value):
        return int(value)

# Use mock numpy
np = MockNumpy()

logger = logging.getLogger(__name__)


class MockModelLoader:
    """Mock model loader for testing"""
    
    @staticmethod
    def load_model(medical_model: MedicalModel):
        """Mock model loading"""
        logger.info(f"Mock loading model: {medical_model.name}")
        return {
            'model': f"mock_model_{medical_model.id}",
            'medical_model': medical_model,
            'config': medical_model.preprocessing_config
        }


class MockImagePreprocessor:
    """Mock image preprocessor"""
    
    @staticmethod
    def preprocess_mri_image(image_path: str, config: Dict[str, Any]):
        """Mock MRI preprocessing"""
        logger.info(f"Mock preprocessing MRI image: {image_path}")
        # Return mock preprocessed data
        target_size = config.get('target_size', (224, 224))
        return np.random.random((1, *target_size, 1)).astype(np.float32)

    @staticmethod
    def preprocess_general_image(image_path: str, config: Dict[str, Any]):
        """Mock general image preprocessing"""
        logger.info(f"Mock preprocessing general image: {image_path}")
        target_size = config.get('target_size', (224, 224))
        return np.random.random((1, *target_size, 3)).astype(np.float32)


class MockDataPreprocessor:
    """Mock data preprocessor"""
    
    @staticmethod
    def preprocess_tabular_data(data: Dict[str, Any], config: Dict[str, Any]):
        """Mock tabular data preprocessing"""
        logger.info("Mock preprocessing tabular data")
        feature_columns = config.get('feature_columns', [])
        features = np.random.random((1, len(feature_columns) if feature_columns else 10))
        return features


class MockMLInferenceEngine:
    """Mock inference engine for testing"""
    
    def __init__(self):
        self.loaded_models = {}
    
    def load_model(self, medical_model: MedicalModel):
        """Load and cache mock model"""
        model_key = f"{medical_model.id}_{medical_model.version}"
        
        if model_key not in self.loaded_models:
            try:
                model_info = MockModelLoader.load_model(medical_model)
                self.loaded_models[model_key] = model_info
                logger.info(f"Mock loaded model: {medical_model.name}")
            except Exception as e:
                logger.error(f"Mock failed to load model {medical_model.name}: {str(e)}")
                raise
        
        return self.loaded_models[model_key]
    
    def preprocess_input(self, input_data: Any, input_type: str, config: Dict[str, Any]):
        """Mock preprocess input based on type"""
        if input_type.lower() == 'mri':
            return MockImagePreprocessor.preprocess_mri_image(input_data, config)
        elif input_type.lower() in ['image', 'xray', 'ct', 'ultrasound']:
            return MockImagePreprocessor.preprocess_general_image(input_data, config)
        elif input_type.lower() in ['tabular', 'structured', 'data']:
            return MockDataPreprocessor.preprocess_tabular_data(input_data, config)
        else:
            raise ValueError(f"Unsupported input type: {input_type}")
    
    def run_inference(self, medical_model: MedicalModel, input_data: Any) -> Dict[str, Any]:
        """Run mock inference on a single model"""
        try:
            # Load model
            model_info = self.load_model(medical_model)
            config = model_info['config']
            
            # Preprocess input
            processed_input = self.preprocess_input(input_data, medical_model.input_type.name, config)
            
            # Mock inference - generate random but realistic predictions
            output_classes = medical_model.output_classes or ['class_0', 'class_1']
            
            # Generate probabilities that sum to 1
            probabilities = np.random.random(len(output_classes))
            probabilities = probabilities / np.sum(probabilities)
            
            # Process predictions
            result = self.process_predictions(probabilities, medical_model)
            
            return {
                'success': True,
                'predictions': result,
                'model_name': medical_model.name,
                'model_version': medical_model.version,
                'framework': medical_model.framework
            }
            
        except Exception as e:
            logger.error(f"Mock inference failed for model {medical_model.name}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model_name': medical_model.name,
                'model_version': medical_model.version
            }
    
    def process_predictions(self, predictions, medical_model: MedicalModel) -> Dict[str, Any]:
        """Process mock predictions into interpretable results"""
        try:
            # Get output classes
            output_classes = medical_model.output_classes or ['class_0', 'class_1']
            
            # Convert to dictionary
            class_probabilities = {}
            for i, class_name in enumerate(output_classes):
                if i < len(predictions):
                    class_probabilities[class_name] = float(predictions[i])
                else:
                    class_probabilities[class_name] = 0.0
            
            # Find predicted class
            predicted_class_idx = np.argmax(predictions)
            predicted_class = output_classes[predicted_class_idx]
            confidence = float(predictions[predicted_class_idx])
            
            return {
                'predicted_class': predicted_class,
                'confidence': confidence,
                'class_probabilities': class_probabilities,
                'raw_predictions': predictions.tolist()
            }
            
        except Exception as e:
            logger.error(f"Error processing mock predictions: {str(e)}")
            raise


# Global mock inference engine instance
mock_inference_engine = MockMLInferenceEngine()
