from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PredictionSessionViewSet, ModelPredictionViewSet, PredictionStatusView
)

router = DefaultRouter()
router.register(r'sessions', PredictionSessionViewSet)
router.register(r'predictions', ModelPredictionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('status/<str:session_id>/', PredictionStatusView.as_view(), name='prediction-status'),
]
