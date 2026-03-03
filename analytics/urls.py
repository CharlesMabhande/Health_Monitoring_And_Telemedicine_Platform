from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RiskScoreViewSet
from .views_ai import SymptomCheckerView

router = DefaultRouter()
router.register("risk-scores", RiskScoreViewSet, basename="risk-scores")

urlpatterns = [
    path("symptom-checker/", SymptomCheckerView.as_view(), name="symptom-checker"),
] + router.urls


