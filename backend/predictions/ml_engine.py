"""
ML Engine for handling model loading, preprocessing, and inference
"""
import os
import json
import logging
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
import torch
from typing import Dict, List, Any, Optional, Tuple
from django.conf import settings
from medical_models.models import MedicalModel

logger = logging.getLogger(__name__)


class ModelLoader:
    """Handles loading of different ML model formats"""
    
    @staticmethod
    def load_tensorflow_model(model_path: str) -> tf.keras.Model:
        """Load TensorFlow/Keras model"""
        try:
            model = tf.keras.models.load_model(model_path)
            logger.info(f"Successfully loaded TensorFlow model from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load TensorFlow model from {model_path}: {str(e)}")
            raise

    @staticmethod
    def load_pytorch_model(model_path: str) -> torch.nn.Module:
        """Load PyTorch model"""
        try:
            model = torch.load(model_path, map_location='cpu')
            model.eval()
            logger.info(f"Successfully loaded PyTorch model from {model_path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load PyTorch model from {model_path}: {str(e)}")
            raise

    @staticmethod
    def load_model(medical_model: MedicalModel):
        """Load model based on framework"""
        model_path = os.path.join(settings.MODEL_STORAGE_PATH, medical_model.model_file_path)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        if medical_model.framework.lower() == 'tensorflow':
            return ModelLoader.load_tensorflow_model(model_path)
        elif medical_model.framework.lower() == 'pytorch':
            return ModelLoader.load_pytorch_model(model_path)
        else:
            raise ValueError(f"Unsupported framework: {medical_model.framework}")


class ImagePreprocessor:
    """Handles image preprocessing for medical images"""
    
    @staticmethod
    def preprocess_mri_image(image_path: str, config: Dict[str, Any]) -> np.ndarray:
        """Preprocess MRI image based on model requirements"""
        try:
            # Load image
            if image_path.lower().endswith(('.nii', '.nii.gz')):
                # Handle NIfTI files (would need nibabel library)
                raise NotImplementedError("NIfTI support not implemented yet")
            else:
                # Handle regular image formats
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if image is None:
                    raise ValueError(f"Could not load image: {image_path}")
            
            # Apply preprocessing based on config
            target_size = config.get('target_size', (224, 224))
            normalize = config.get('normalize', True)
            augment = config.get('augment', False)
            
            # Resize image
            image = cv2.resize(image, target_size)
            
            # Normalize if required
            if normalize:
                image = image.astype(np.float32) / 255.0
            
            # Add channel dimension if needed
            if len(image.shape) == 2:
                image = np.expand_dims(image, axis=-1)
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            return image
            
        except Exception as e:
            logger.error(f"Error preprocessing MRI image: {str(e)}")
            raise

    @staticmethod
    def preprocess_general_image(image_path: str, config: Dict[str, Any]) -> np.ndarray:
        """Preprocess general medical images"""
        try:
            image = Image.open(image_path)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize
            target_size = config.get('target_size', (224, 224))
            image = image.resize(target_size)
            
            # Convert to numpy array
            image_array = np.array(image, dtype=np.float32)
            
            # Normalize
            if config.get('normalize', True):
                image_array = image_array / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            logger.error(f"Error preprocessing general image: {str(e)}")
            raise


class DataPreprocessor:
    """Handles preprocessing of structured data"""
    
    @staticmethod
    def preprocess_tabular_data(data: Dict[str, Any], config: Dict[str, Any]) -> np.ndarray:
        """Preprocess tabular/structured data"""
        try:
            # Extract features based on config
            feature_columns = config.get('feature_columns', [])
            if not feature_columns:
                feature_columns = list(data.keys())
            
            # Convert to numpy array
            features = []
            for col in feature_columns:
                if col in data:
                    features.append(float(data[col]))
                else:
                    # Handle missing values
                    default_value = config.get('default_values', {}).get(col, 0.0)
                    features.append(default_value)
            
            # Apply scaling if configured
            if config.get('scale', False):
                # This would typically use a fitted scaler
                # For now, we'll do simple normalization
                features = np.array(features)
                features = (features - np.mean(features)) / (np.std(features) + 1e-8)
            else:
                features = np.array(features)
            
            # Add batch dimension
            features = np.expand_dims(features, axis=0)
            
            return features
            
        except Exception as e:
            logger.error(f"Error preprocessing tabular data: {str(e)}")
            raise


class MLInferenceEngine:
    """Main inference engine for running predictions"""
    
    def __init__(self):
        self.loaded_models = {}
    
    def load_model(self, medical_model: MedicalModel):
        """Load and cache model"""
        model_key = f"{medical_model.id}_{medical_model.version}"
        
        if model_key not in self.loaded_models:
            try:
                model = ModelLoader.load_model(medical_model)
                self.loaded_models[model_key] = {
                    'model': model,
                    'medical_model': medical_model,
                    'config': medical_model.preprocessing_config
                }
                logger.info(f"Loaded model: {medical_model.name}")
            except Exception as e:
                logger.error(f"Failed to load model {medical_model.name}: {str(e)}")
                raise
        
        return self.loaded_models[model_key]
    
    def preprocess_input(self, input_data: Any, input_type: str, config: Dict[str, Any]) -> np.ndarray:
        """Preprocess input based on type"""
        if input_type.lower() == 'mri':
            return ImagePreprocessor.preprocess_mri_image(input_data, config)
        elif input_type.lower() in ['image', 'xray', 'ct', 'ultrasound']:
            return ImagePreprocessor.preprocess_general_image(input_data, config)
        elif input_type.lower() in ['tabular', 'structured', 'data']:
            return DataPreprocessor.preprocess_tabular_data(input_data, config)
        else:
            raise ValueError(f"Unsupported input type: {input_type}")
    
    def run_inference(self, medical_model: MedicalModel, input_data: Any) -> Dict[str, Any]:
        """Run inference on a single model"""
        try:
            # Load model
            model_info = self.load_model(medical_model)
            model = model_info['model']
            config = model_info['config']
            
            # Preprocess input
            processed_input = self.preprocess_input(input_data, medical_model.input_type.name, config)
            
            # Run inference
            if medical_model.framework.lower() == 'tensorflow':
                predictions = model.predict(processed_input, verbose=0)
            elif medical_model.framework.lower() == 'pytorch':
                with torch.no_grad():
                    input_tensor = torch.from_numpy(processed_input)
                    predictions = model(input_tensor).numpy()
            else:
                raise ValueError(f"Unsupported framework: {medical_model.framework}")
            
            # Process predictions
            result = self.process_predictions(predictions, medical_model)
            
            return {
                'success': True,
                'predictions': result,
                'model_name': medical_model.name,
                'model_version': medical_model.version,
                'framework': medical_model.framework
            }
            
        except Exception as e:
            logger.error(f"Inference failed for model {medical_model.name}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'model_name': medical_model.name,
                'model_version': medical_model.version
            }
    
    def process_predictions(self, predictions: np.ndarray, medical_model: MedicalModel) -> Dict[str, Any]:
        """Process raw model predictions into interpretable results"""
        try:
            # Get output classes
            output_classes = medical_model.output_classes or ['class_0', 'class_1']
            
            # Handle different prediction formats
            if len(predictions.shape) == 1:
                # Single prediction
                probabilities = predictions
            else:
                # Batch prediction (take first item)
                probabilities = predictions[0]
            
            # Ensure probabilities are in correct format
            if len(probabilities) != len(output_classes):
                # Handle binary classification
                if len(probabilities) == 1:
                    prob = float(probabilities[0])
                    probabilities = [1 - prob, prob]
                else:
                    # Pad or truncate as needed
                    if len(probabilities) > len(output_classes):
                        probabilities = probabilities[:len(output_classes)]
                    else:
                        probabilities = np.pad(probabilities, (0, len(output_classes) - len(probabilities)))
            
            # Convert to dictionary
            class_probabilities = {}
            for i, class_name in enumerate(output_classes):
                class_probabilities[class_name] = float(probabilities[i])
            
            # Find predicted class
            predicted_class_idx = np.argmax(probabilities)
            predicted_class = output_classes[predicted_class_idx]
            confidence = float(probabilities[predicted_class_idx])
            
            return {
                'predicted_class': predicted_class,
                'confidence': confidence,
                'class_probabilities': class_probabilities,
                'raw_predictions': probabilities.tolist()
            }
            
        except Exception as e:
            logger.error(f"Error processing predictions: {str(e)}")
            raise


# Global inference engine instance
inference_engine = MLInferenceEngine()
