from rest_framework.routers import DefaultRouter

from .views import PatientProfileViewSet, HealthRecordViewSet, VitalSignViewSet, EmergencyAlertViewSet

router = DefaultRouter()
router.register("profiles", PatientProfileViewSet, basename="patient-profiles")
router.register("records", HealthRecordViewSet, basename="health-records")
router.register("vitals", VitalSignViewSet, basename="vital-signs")
router.register("alerts", EmergencyAlertViewSet, basename="emergency-alerts")

urlpatterns = router.urls

