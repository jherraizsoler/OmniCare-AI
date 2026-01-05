from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, 
    AiAuditLogViewSet, 
    login_user, 
    register_user, 
    list_medicos, 
    delete_user,
    manage_patients,
    change_password,
    export_paciente_pdf,
    # Añadimos las nuevas funciones de persistencia
    guardar_consulta,
    historial_paciente
)

# El router se encarga de las rutas automáticas de los ViewSets
router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'audit-logs', AiAuditLogViewSet)

urlpatterns = [
    # Rutas del router (audit-logs, patients, etc)
    path('', include(router.urls)),
    
    # Rutas manuales de Autenticación
    path('login/', login_user),
    path('register/', register_user),
    path('change-password/', change_password),
    
    # Rutas de Supervisor
    path('medicos-list/', list_medicos),
    path('medicos-delete/<int:pk>/', delete_user),
    
    # Rutas de Gestión de Pacientes (Médicos)
    path('manage-patients/', manage_patients),
    
    # --- NUEVAS RUTAS DE PERSISTENCIA IA ---
    
    # 1. Guardar una nueva interacción del chat (POST)
    path('guardar-consulta/', guardar_consulta, name='guardar_consulta'),
    
    # 2. Obtener historial del paciente logueado (GET)
    path('historial-paciente/', historial_paciente, name='historial_paciente'),
    
    # 3. Obtener historial de un paciente específico (Vista Médico)
    path('historial-paciente/<str:patient_id>/', historial_paciente, name='historial_paciente_especifico'),
    
    # 4. Exportación PDF
    path('export-pdf/<str:patient_id>/', export_paciente_pdf, name='export-pdf'),
]