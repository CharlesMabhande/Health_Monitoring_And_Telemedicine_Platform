from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with role-based access control.
    """

    class Roles(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PATIENT,
    )

    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def is_patient(self) -> bool:
        return self.role == self.Roles.PATIENT

    def is_doctor(self) -> bool:
        return self.role == self.Roles.DOCTOR

    def is_admin(self) -> bool:
        return self.role == self.Roles.ADMIN


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialization = models.CharField(max_length=255)
    license_number = models.CharField(max_length=100, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    verification_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Dr. {self.user.get_full_name()} ({self.specialization})"
