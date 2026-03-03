from django.urls import path

from .views import (
    DashboardOverviewView,
    appointments_list,
    appointment_create,
    patients_list,
    alerts_list,
    symptom_checker_view,
)

urlpatterns = [
    # JSON API overview (used under /api/dashboard/)
    path("overview/", DashboardOverviewView.as_view(), name="dashboard-overview"),
    # HTML views (used under /dashboard/ and linked from home)
    path("patients/", patients_list, name="dashboard-patients"),
    path("appointments/", appointments_list, name="dashboard-appointments"),
    path("appointments/new/", appointment_create, name="dashboard-appointment-create"),
    path("alerts/", alerts_list, name="dashboard-alerts"),
    path("symptom-checker/", symptom_checker_view, name="dashboard-symptom-checker"),
]

