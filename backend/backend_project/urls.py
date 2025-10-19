"""
URL configuration for backend_project project.
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def model_list(request):
    """Return a list of available ML models"""
    models = [
        {"id": "alzheimer-detection", "name": "Alzheimer's Detection"},
        {"id": "pneumonia-detection", "name": "Pneumonia Detection"},
        {"id": "skin-cancer-classification", "name": "Skin Cancer Classification"},
        {"id": "brain-tumor-segmentation", "name": "Brain Tumor Segmentation"},
    ]
    return JsonResponse(models, safe=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('models/', model_list, name='model-list'),
]