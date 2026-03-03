from django.conf import settings
from django.db import models


class PatientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=255, blank=True)
    emergency_contact_phone = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        return f"Patient: {self.user.get_full_name()}"


class HealthRecord(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="health_records")
    diagnosis = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class VitalSign(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="vital_signs")
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True)
    spo2 = models.PositiveIntegerField(null=True, blank=True, help_text="Oxygen saturation")
    glucose_level = models.FloatField(null=True, blank=True)
    source = models.CharField(max_length=100, blank=True, help_text="Wearable or device name")
    recorded_at = models.DateTimeField(auto_now_add=True)


class EmergencyAlert(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="emergency_alerts")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    triggered_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
