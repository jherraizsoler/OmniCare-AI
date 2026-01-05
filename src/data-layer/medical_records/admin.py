from django.contrib import admin
from .models import Patient, ConsultationLog, AiAuditLog, ConsultaIA

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'name', 'created_at')
    search_fields = ('patient_id', 'name')

@admin.register(ConsultationLog)
class ConsultationLogAdmin(admin.ModelAdmin):
    list_display = ('patient', 'urgency_level', 'timestamp')
    list_filter = ('urgency_level',)
    
@admin.register(AiAuditLog)
class AiAuditLogAdmin(admin.ModelAdmin):
    # Ahora sí incluimos agent_name porque existe en el modelo
    list_display = ('id', 'patient', 'agent_name', 'model_used', 'created_at')
    
    # Cambiamos 'timestamp' por 'created_at' que es el nombre en tu modelo
    readonly_fields = ('created_at',)

@admin.register(ConsultaIA)
class ConsultaIAAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha', 'urgencia', 'riesgo')
    list_filter = ('urgencia', 'fecha')
    search_fields = ('paciente__username', 'mensaje_usuario')