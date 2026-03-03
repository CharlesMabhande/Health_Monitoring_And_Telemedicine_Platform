from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


class SymptomCheckerView(APIView):
    """
    Placeholder AI symptom checker endpoint.

    In production, connect this to a TensorFlow/PyTorch model
    that takes symptom text / structured features and returns
    ranked possible conditions with confidence scores.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        symptoms = request.data.get("symptoms", "")
        # TODO: integrate real model here
        dummy_result = {
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
        return Response(dummy_result, status=status.HTTP_200_OK)

