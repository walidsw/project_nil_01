from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .services.model_manager import ModelManager
from .services.image_processor import ImageProcessor

model_manager = ModelManager(settings.MODEL_PATH)
image_processor = ImageProcessor()

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS

class IndexView(APIView):
    def get(self, request):
        return Response({
            "name": "DeepMed Backend Server (Django)",
            "version": "1.0.0",
            "endpoints": {"predict": "/predict", "health": "/health", "models": "/models"}
        })

class HealthCheckView(APIView):
    def get(self, request):
        return Response({
            "status": "healthy",
            "models_loaded": len(model_manager.models),
            "ready": True
        })

class ModelListView(APIView):
    def get(self, request):
        models_info = [
            {"name": name, "description": info['description'], "paper_url": info['paper_url']}
            for name, info in model_manager.models.items()
        ]
        return Response({"total_models": len(models_info), "models": models_info})

class PredictView(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file part in the request'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        if not file.name or not allowed_file(file.name):
            return Response({'error': f"Invalid file or file type. Allowed: {settings.ALLOWED_EXTENSIONS}"}, status=status.HTTP_400_BAD_REQUEST)
        
        if file.size > settings.MAX_CONTENT_LENGTH:
            return Response({'error': 'File too large'}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        try:
            image = image_processor.read_image(file.read())
            if not image_processor.validate_medical_format(image):
                return Response({'error': 'Image does not meet minimum requirements (min 224x224)'}, status=status.HTTP_400_BAD_REQUEST)
            
            results = model_manager.predict(image)
            results['metadata'] = {'filename': file.name, 'image_size': image.size, 'format': image.format}
            return Response(results)
        except ValueError as ve:
            return Response({'error': f'Invalid image: {ve}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'An error occurred: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)