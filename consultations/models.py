from django.conf import settings
from django.db import models

from patients.models import PatientProfile
from accounts.models import DoctorProfile


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="appointments")
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)


class ConsultationSession(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="consultation")
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    video_session_id = models.CharField(max_length=255, blank=True, help_text="WebRTC/third-party session identifier")
    recording_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)


class Prescription(models.Model):
    consultation = models.OneToOneField(
        ConsultationSession,
        on_delete=models.CASCADE,
        related_name="prescription",
    )
    prescribed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="prescriptions_issued",
    )
    content = models.TextField(help_text="Prescription details including medicines and dosage")
    created_at = models.DateTimeField(auto_now_add=True)
