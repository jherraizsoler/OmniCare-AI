from rest_framework import serializers
from .models import Patient, AiAuditLog # Añadimos el nuevo modelo aquí

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_id', 'name', 'clinical_history']

# --- NUEVO SERIALIZADOR PARA AUDITORÍA ---
class AiAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiAuditLog
        fields = '__all__'