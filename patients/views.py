from rest_framework import permissions, viewsets

from .models import PatientProfile, HealthRecord, VitalSign, EmergencyAlert
from .serializers import (
    PatientProfileSerializer,
    HealthRecordSerializer,
    VitalSignSerializer,
    EmergencyAlertSerializer,
)


class IsPatientOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if isinstance(obj, PatientProfile):
            return hasattr(user, "patient_profile") and obj.user_id == user.id
        return True


class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatientOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HealthRecordViewSet(viewsets.ModelViewSet):
    queryset = HealthRecord.objects.all()
    serializer_class = HealthRecordSerializer
    permission_classes = [permissions.IsAuthenticated]


class VitalSignViewSet(viewsets.ModelViewSet):
    queryset = VitalSign.objects.all()
    serializer_class = VitalSignSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmergencyAlertViewSet(viewsets.ModelViewSet):
    queryset = EmergencyAlert.objects.all()
    serializer_class = EmergencyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

