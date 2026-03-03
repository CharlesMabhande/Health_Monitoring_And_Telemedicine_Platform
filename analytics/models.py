from django.db import models

from patients.models import PatientProfile


class RiskScore(models.Model):
    """
    Stores AI-generated risk scores / early warning indicators.
    """

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="risk_scores")
    score = models.FloatField()
    label = models.CharField(max_length=255, help_text="e.g. 'Diabetes risk', 'Cardiac event risk'")
    generated_at = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50, blank=True)
