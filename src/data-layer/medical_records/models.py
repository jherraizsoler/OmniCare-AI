from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    # Este campo lo leerá el Agente de LangGraph para dar contexto
    clinical_history = models.TextField(help_text="Resumen clínico para contexto de IA")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_id} - {self.name}"

class ConsultationLog(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    ai_analysis = models.TextField()
    urgency_level = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class AiAuditLog(models.Model):
    patient_id = models.CharField(max_length=50)
    agent_name = models.CharField(max_length=100)
    input_symptoms = models.TextField()
    ai_analysis = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Auditoría {self.patient_id} - {self.agent_name} - {self.timestamp}"