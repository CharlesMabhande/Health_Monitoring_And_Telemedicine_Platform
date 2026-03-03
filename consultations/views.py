from rest_framework import permissions, viewsets

from .models import Appointment, ConsultationSession, Prescription
from .serializers import (
    AppointmentSerializer,
    ConsultationSessionSerializer,
    PrescriptionSerializer,
)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class ConsultationSessionViewSet(viewsets.ModelViewSet):
    queryset = ConsultationSession.objects.all()
    serializer_class = ConsultationSessionSerializer
    permission_classes = [permissions.IsAuthenticated]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

