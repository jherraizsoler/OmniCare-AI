from rest_framework import viewsets
from rest_framework.response import Response
from .models import Patient, AiAuditLog
from .serializers import PatientSerializer, AiAuditLogSerializer

# Vista para Pacientes (maneja GET lista y GET detalle)
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # Esto permite buscar por patient_id en la URL en lugar de la PK numérica
    lookup_field = 'patient_id'

# Vista para los Logs de Auditoría de la IA
class AiAuditLogViewSet(viewsets.ModelViewSet):
    queryset = AiAuditLog.objects.all()
    serializer_class = AiAuditLogSerializer