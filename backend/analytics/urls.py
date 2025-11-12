from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonalRecordViewSet, ProgressSnapshotViewSet, AnalyticsViewSet

router = DefaultRouter()
router.register(r'personal-records', PersonalRecordViewSet, basename='personal-record')
router.register(r'progress-snapshots', ProgressSnapshotViewSet, basename='progress-snapshot')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
]
