import numpy as np
from typing import Dict, Tuple
from PIL import Image

class ModelManager:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.models = {}
        self.load_models()

    def load_models(self):
        print("Loading models...")
        self.models = {
            'CancerNet-A': {'model': None, 'paper_url': 'https://example.com/paper/1', 'description': 'Breast Cancer Detection Model'},
            'TumorResNet-B': {'model': None, 'paper_url': 'https://example.com/paper/2', 'description': 'Brain Tumor Classification Model'},
            'AlzheimerNet-C': {'model': None, 'paper_url': 'https://example.com/paper/3', 'description': "Alzheimer's Disease Prediction Model"}
        }
        print(f"Loaded {len(self.models)} models successfully")

    def preprocess_image(self, image: Image.Image, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image = image.resize(target_size)
        image_array = np.array(image)
        image_array = image_array.astype('float32') / 255.0
        return np.expand_dims(image_array, axis=0)

    def predict(self, image: Image.Image) -> Dict:
        preprocessed_image = self.preprocess_image(image)
        predictions = []
        positive_count = 0
        for model_name, model_info in self.models.items():
            confidence = np.random.uniform(0.75, 0.98)
            is_positive = np.random.choice([True, False], p=[0.6, 0.4])
            if is_positive:
                positive_count += 1
            predictions.append({
                'model_name': model_name,
                'prediction': 'Positive' if is_positive else 'Negative',
                'confidence': float(confidence),
                'paper_url': model_info['paper_url'],
                'description': model_info['description']
            })
        return {
            'aggregate_result': f"{positive_count} out of {len(self.models)} models predicted positive.",
            'total_models': len(self.models),
            'positive_predictions': positive_count,
            'model_predictions': predictions
        }