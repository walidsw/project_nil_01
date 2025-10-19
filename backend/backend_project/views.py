from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import random
import json

# Dummy model database
DUMMY_MODELS = {
    "Brain MRI": [
        {"id": "alz-mri-resnet", "name": "Alzheimer's ResNet", "paper_url": "https://arxiv.org/abs/1512.03385"},
        {"id": "alz-mri-vgg", "name": "Alzheimer's VGG16", "paper_url": "https://arxiv.org/abs/1409.1556"},
        {"id": "tumor-mri-seg", "name": "Brain Tumor Segmentation", "paper_url": "https://arxiv.org/abs/1505.04597"},
    ],
    "PET Scan": [
        {"id": "alz-pet-unet", "name": "PET Scan U-Net", "paper_url": "https://arxiv.org/abs/1505.04597"},
        {"id": "alz-pet-gan", "name": "PET Scan GAN", "paper_url": "https://arxiv.org/abs/1406.2661"},
    ],
    "CT Scan": [
        {"id": "stroke-ct-cnn", "name": "Stroke Detection CNN", "paper_url": "https://arxiv.org/abs/1512.03385"},
    ],
    "Dermatoscopic Image": [
        {"id": "skin-cancer-effnet", "name": "Skin Cancer EfficientNet", "paper_url": "https://arxiv.org/abs/1905.11946"},
        {"id": "skin-cancer-mobilenet", "name": "Skin Cancer MobileNet", "paper_url": "https://arxiv.org/abs/1704.04861"},
    ],
    "Mammogram": [
        {"id": "breast-cancer-mammo", "name": "Breast Cancer Detection", "paper_url": "https://arxiv.org/abs/1611.05431"},
    ],
    "Chest X-Ray": [
        {"id": "pneumonia-xray-cnn", "name": "Pneumonia Detection CNN", "paper_url": "https://arxiv.org/abs/1711.05225"},
        {"id": "pneumonia-xray-densenet", "name": "Pneumonia DenseNet", "paper_url": "https://arxiv.org/abs/1608.06993"},
    ],
}

def simulate_prediction():
    """Simulate a model prediction with random results"""
    predictions = ["Positive", "Negative", "Uncertain"]
    return {
        "prediction": random.choice(predictions),
        "confidence": round(random.uniform(0.85, 0.99), 2)
    }

@csrf_exempt
@require_http_methods(["POST"])
def predict_single(request):
    """Handle single model prediction"""
    try:
        # Get the uploaded image and model_id
        image = request.FILES.get('image')
        model_id = request.POST.get('model_id')
        
        if not image:
            return JsonResponse({'error': 'No image provided'}, status=400)
        
        # Simulate prediction
        result = simulate_prediction()
        
        # Find model info (for demo purposes, using first model from any modality)
        model_name = model_id or "Unknown Model"
        paper_url = "https://arxiv.org/abs/1512.03385"
        
        # For a real model, you would find it in DUMMY_MODELS
        for modality, models in DUMMY_MODELS.items():
            for model in models:
                if model['id'] == model_id or model['name'] == model_id:
                    model_name = model['name']
                    paper_url = model['paper_url']
                    break
        
        return JsonResponse({
            'model_name': model_name,
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'paper_url': paper_url,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def predict_multi(request):
    """Handle multi-model prediction"""
    try:
        # Get the uploaded image and modality
        image = request.FILES.get('image')
        modality = request.POST.get('modality')
        
        if not image:
            return JsonResponse({'error': 'No image provided'}, status=400)
        
        # Get models for this modality
        models = DUMMY_MODELS.get(modality, [])
        
        if not models:
            return JsonResponse({'error': f'No models found for modality: {modality}'}, status=404)
        
        # Simulate predictions for all models
        individual_results = []
        for model in models:
            result = simulate_prediction()
            individual_results.append({
                'model_name': model['name'],
                'prediction': result['prediction'],
                'confidence': result['confidence'],
                'paper_url': model['paper_url'],
            })
        
        # Calculate average confidence
        avg_confidence = sum(r['confidence'] for r in individual_results) / len(individual_results)
        
        # Determine overall prediction (majority vote)
        prediction_counts = {}
        for result in individual_results:
            pred = result['prediction']
            prediction_counts[pred] = prediction_counts.get(pred, 0) + 1
        
        overall_prediction = max(prediction_counts, key=prediction_counts.get)
        
        return JsonResponse({
            'overall_prediction': overall_prediction,
            'average_confidence': round(avg_confidence, 2),
            'individual_results': individual_results,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)