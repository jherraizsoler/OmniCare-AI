from django.contrib import admin
from .models import Patient, ConsultationLog, AiAuditLog

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
    list_display = ('patient_id', 'agent_name', 'timestamp')
    readonly_fields = ('timestamp',) # Para que no se pueda modificar la hora