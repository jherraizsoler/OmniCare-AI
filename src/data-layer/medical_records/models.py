from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    # Relación con el médico (User)
    doctor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='doctor_patients', 
        null=True, 
        blank=True
        )
    
    patient_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    clinical_history = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Dr. {self.doctor.username if self.doctor else 'S/D'}"
    
class ConsultaIA(models.Model):
    # Relacionamos la consulta con el usuario (Paciente)
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultas')
    fecha = models.DateTimeField(auto_now_add=True)
    
    # Textos de la conversación
    mensaje_usuario = models.TextField()
    respuesta_ia = models.TextField()
    
    # Métricas de triaje (Big Data ready)
    dolor = models.IntegerField(default=0)
    urgencia = models.IntegerField(default=0)
    riesgo = models.IntegerField(default=0)

    def __str__(self):
        return f"Consulta de {self.paciente.username} - {self.fecha.strftime('%d/%m/%Y')}"