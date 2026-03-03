from django.urls import path

from .views import MeView, PatientRegisterView, DoctorRegisterView


urlpatterns = [
    path("me/", MeView.as_view(), name="accounts-me"),
    path("register/patient/", PatientRegisterView.as_view(), name="accounts-register-patient"),
    path("register/doctor/", DoctorRegisterView.as_view(), name="accounts-register-doctor"),
]

