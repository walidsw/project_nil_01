from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MedicalDomainViewSet, InputTypeViewSet, ResearchPaperViewSet,
    MedicalModelViewSet, ModelCategoryViewSet
)

router = DefaultRouter()
router.register(r'domains', MedicalDomainViewSet)
router.register(r'input-types', InputTypeViewSet)
router.register(r'papers', ResearchPaperViewSet)
router.register(r'models', MedicalModelViewSet)
router.register(r'categories', ModelCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
