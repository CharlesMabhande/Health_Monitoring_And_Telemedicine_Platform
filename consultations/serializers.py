from rest_framework import serializers

from .models import Appointment, ConsultationSession, Prescription


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class ConsultationSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationSession
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"

