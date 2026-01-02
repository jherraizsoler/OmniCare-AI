from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, AiAuditLogViewSet, register_user, login_user

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'audit-logs', AiAuditLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user), # Esto crea /api/register/
    path('login/', login_user),       # Esto crea /api/login/
]