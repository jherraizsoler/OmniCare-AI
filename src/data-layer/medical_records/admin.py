from django.contrib import admin
from .models import Patient, ConsultaIA

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'name', 'created_at')
    search_fields = ('patient_id', 'name')

@admin.register(ConsultaIA)
class ConsultaIAAdmin(admin.ModelAdmin):
    # Esta es tu tabla principal de "Single Source of Truth"
    list_display = ('paciente', 'fecha', 'urgencia', 'riesgo')
    list_filter = ('urgencia', 'fecha', 'riesgo')
    search_fields = ('paciente__username', 'mensaje_usuario', 'respuesta_ia')
    readonly_fields = ('fecha',) # Para que no se pueda alterar el registro de la IA