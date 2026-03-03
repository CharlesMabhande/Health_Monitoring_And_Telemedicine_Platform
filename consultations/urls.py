from rest_framework.routers import DefaultRouter

from .views import AppointmentViewSet, ConsultationSessionViewSet, PrescriptionViewSet

router = DefaultRouter()
router.register("appointments", AppointmentViewSet, basename="appointments")
router.register("sessions", ConsultationSessionViewSet, basename="consultation-sessions")
router.register("prescriptions", PrescriptionViewSet, basename="prescriptions")

urlpatterns = router.urls

