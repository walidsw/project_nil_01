from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('health', views.HealthCheckView.as_view(), name='health_check'),
    path('models', views.ModelListView.as_view(), name='list_models'),
    path('predict', views.PredictView.as_view(), name='predict'),
]