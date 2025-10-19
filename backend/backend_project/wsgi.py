"""
WSGI project for backend_project project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')

application = get_wsgi_application()

# filepath: /Users/swadhin/Documents/Academic/Project/project_nil_01-main/backend/backend_project/urls.py
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