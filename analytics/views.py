from rest_framework import permissions, viewsets

from .models import RiskScore
from .serializers import RiskScoreSerializer


class RiskScoreViewSet(viewsets.ModelViewSet):
    queryset = RiskScore.objects.all()
    serializer_class = RiskScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

