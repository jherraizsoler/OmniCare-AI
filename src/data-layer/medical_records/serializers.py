from rest_framework import serializers
from .models import Patient, AiAuditLog # Añadimos el nuevo modelo aquí

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_id', 'name', 'clinical_history']

# --- NUEVO SERIALIZADOR PARA AUDITORÍA ---
class AiAuditLogSerializer(serializers.ModelSerializer):
    # Usamos SlugRelatedField para que el grafo pueda enviar "PAC-001" 
    # en lugar de un ID numérico interno
    patient = serializers.SlugRelatedField(
        slug_field='patient_id', 
        queryset=Patient.objects.all()
    )

    class Meta:
        model = AiAuditLog
        fields = '__all__'