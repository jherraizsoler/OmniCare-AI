from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient,ConsultaIA # Añadimos el nuevo modelo aquí

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_id', 'name', 'clinical_history']

# --- NUEVO SERIALIZADOR PARA AUDITORÍA ---
class AiAuditLogSerializer(serializers.ModelSerializer):
    """
    Este serializador ahora apunta a ConsultaIA. 
    Mapeamos los campos para que el Dashboard de Auditoría siga funcionando.
    """
    # Usamos SlugRelatedField para que en el Dashboard aparezca el nombre/DNI del paciente
    paciente = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = ConsultaIA
        fields = [
            'id', 
            'paciente', 
            'mensaje_usuario', 
            'respuesta_ia', 
            'fecha', 
            'urgencia', 
            'riesgo', 
            'dolor'
        ]