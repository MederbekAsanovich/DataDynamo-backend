from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataSetViewSet, DataAnalysisTaskViewSet

router = DefaultRouter()
router.register(r'datasets', DataSetViewSet)
router.register(r'tasks', DataAnalysisTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
