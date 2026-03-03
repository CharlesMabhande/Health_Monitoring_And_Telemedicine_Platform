from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User, DoctorProfile
from patients.models import PatientProfile, EmergencyAlert, VitalSign
from consultations.models import Appointment, ConsultationSession, Prescription
from analytics.models import RiskScore


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "scheduled_time"]
        widgets = {
            "scheduled_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class IsStaffOrDoctor(permissions.BasePermission):
    """
    Allow access only to admin/staff users or doctors.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return getattr(user, "role", None) == getattr(User.Roles, "DOCTOR", "DOCTOR")


class DashboardOverviewView(APIView):
    """
    Returns high-level metrics for doctor/admin dashboards.
    """

    permission_classes = [permissions.IsAuthenticated, IsStaffOrDoctor]

    def get(self, request):
        data = {
            "users": {
                "total": User.objects.count(),
                "patients": PatientProfile.objects.count(),
                "doctors": DoctorProfile.objects.count(),
            },
            "appointments": {
                "total": Appointment.objects.count(),
                "pending": Appointment.objects.filter(status=Appointment.Status.PENDING).count(),
                "approved": Appointment.objects.filter(status=Appointment.Status.APPROVED).count(),
                "completed": Appointment.objects.filter(status=Appointment.Status.COMPLETED).count(),
            },
            "consultations": {
                "sessions": ConsultationSession.objects.count(),
                "prescriptions": Prescription.objects.count(),
            },
            "alerts": {
                "total": EmergencyAlert.objects.count(),
                "unresolved": EmergencyAlert.objects.filter(resolved=False).count(),
            },
            "analytics": {
                "risk_scores": RiskScore.objects.count(),
                "vital_sign_entries": VitalSign.objects.count(),
            },
        }
        return Response(data)


@login_required
def dashboard_home(request):
    """
    HTML dashboard view for doctors/admins at '/'.
    """

    user = request.user
    if not (user.is_staff or user.is_superuser or getattr(user, "role", None) == getattr(User.Roles, "DOCTOR", "DOCTOR")):
        # Non-doctor/pure patients: simple message
        return render(request, "dashboard/forbidden.html", status=403)

    context = {
        "users": {
            "total": User.objects.count(),
            "patients": PatientProfile.objects.count(),
            "doctors": DoctorProfile.objects.count(),
        },
        "appointments": {
            "total": Appointment.objects.count(),
            "pending": Appointment.objects.filter(status=Appointment.Status.PENDING).count(),
            "approved": Appointment.objects.filter(status=Appointment.Status.APPROVED).count(),
            "completed": Appointment.objects.filter(status=Appointment.Status.COMPLETED).count(),
        },
        "consultations": {
            "sessions": ConsultationSession.objects.count(),
            "prescriptions": Prescription.objects.count(),
        },
        "alerts": {
            "total": EmergencyAlert.objects.count(),
            "unresolved": EmergencyAlert.objects.filter(resolved=False).count(),
        },
        "analytics": {
            "risk_scores": RiskScore.objects.count(),
            "vital_sign_entries": VitalSign.objects.count(),
        },
    }
    return render(request, "dashboard/home.html", context)


@login_required
def patients_list(request):
    user = request.user
    if not (user.is_staff or user.is_superuser or getattr(user, "role", None) == getattr(User.Roles, "DOCTOR", "DOCTOR")):
        return render(request, "dashboard/forbidden.html", status=403)

    patients = PatientProfile.objects.select_related("user").all()
    return render(request, "dashboard/patients.html", {"patients": patients})


@login_required
def appointments_list(request):
    user = request.user
    if not (user.is_staff or user.is_superuser or getattr(user, "role", None) == getattr(User.Roles, "DOCTOR", "DOCTOR")):
        return render(request, "dashboard/forbidden.html", status=403)

    qs = Appointment.objects.select_related("patient__user", "doctor__user").order_by("-scheduled_time")
    if hasattr(user, "doctor_profile"):
        qs = qs.filter(doctor=user.doctor_profile)
    return render(request, "dashboard/appointments.html", {"appointments": qs})


@login_required
def appointment_create(request):
    user = request.user
    if not (user.is_staff or user.is_superuser or hasattr(user, "doctor_profile")):
        return render(request, "dashboard/forbidden.html", status=403)

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        # If logged-in user is a doctor (not just admin), force doctor field
        if hasattr(user, "doctor_profile") and not (user.is_staff or user.is_superuser):
            form.fields["doctor"].queryset = DoctorProfile.objects.filter(pk=user.doctor_profile.pk)
        if form.is_valid():
            appt = form.save(commit=False)
            if hasattr(user, "doctor_profile") and not (user.is_staff or user.is_superuser):
                appt.doctor = user.doctor_profile
            appt.save()
            return redirect("dashboard-appointments")
    else:
        form = AppointmentForm()
        if hasattr(user, "doctor_profile") and not (user.is_staff or user.is_superuser):
            form.fields["doctor"].queryset = DoctorProfile.objects.filter(pk=user.doctor_profile.pk)
    return render(request, "dashboard/appointment_form.html", {"form": form})


@login_required
def alerts_list(request):
    user = request.user
    if not (user.is_staff or user.is_superuser or getattr(user, "role", None) == getattr(User.Roles, "DOCTOR", "DOCTOR")):
        return render(request, "dashboard/forbidden.html", status=403)

    alerts = EmergencyAlert.objects.select_related("patient__user").order_by("-triggered_at")

    if request.method == "POST":
        alert_id = request.POST.get("alert_id")
        alert = get_object_or_404(EmergencyAlert, id=alert_id)
        alert.resolved = True
        alert.save()
        return redirect("dashboard-alerts")

    return render(request, "dashboard/alerts.html", {"alerts": alerts})


@login_required
def symptom_checker_view(request):
    """
    Simple HTML wrapper around the AI symptom checker.
    Currently uses the same dummy logic as the API; later you can plug in a real model.
    """

    result = None
    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "")
        result = {
            "input_symptoms": symptoms,
            "possible_conditions": [
                {"name": "Example Condition A", "probability": 0.4},
                {"name": "Example Condition B", "probability": 0.25},
            ],
            "references": [
                "https://www.who.int/",
                "https://www.ncbi.nlm.nih.gov/pubmed/",
            ],
        }

    return render(request, "dashboard/symptom_checker.html", {"result": result})

