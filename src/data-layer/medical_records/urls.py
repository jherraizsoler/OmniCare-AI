from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, AiAuditLogViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'audit-logs', AiAuditLogViewSet, basename='auditlog')

urlpatterns = [
    path('', include(router.urls)),
]