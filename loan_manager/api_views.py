from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import PredictSerializer, PredictResponseSerializer
from .ml.predictor import predict_risk


@extend_schema(
    tags=["Risk Scoring"],
    summary="Predict loan risk",
    description=(
        "Submits applicant data to the CatBoost ML model and returns a risk probability "
        "and an AI decision. The decision is based on the following thresholds: "
        "Approved (probability ≤ 30%), Pending (30% < probability < 80%), "
        "Rejected (probability ≥ 80%). "
        "This endpoint is used internally by the platform after a loan application is submitted. "
        "Note: the final decision always requires human analyst validation (GDPR Article 22)."
    ),
    request=PredictSerializer,
    responses={
        200: PredictResponseSerializer,
        400: OpenApiExample(
            "Validation Error",
            value={"age": ["A valid integer is required."]},
            response_only=True,
            status_codes=["400"]
        )
    },
    examples=[
        OpenApiExample(
            "Example Request — Low Risk",
            value={
                "age": 35,
                "income": 75000,
                "experience": 10,
                "current_house_yrs": 5,
                "cur_job_years": 4,
                "marital_status": "married",
                "house_ownership": "owned",
                "car_ownership": "yes",
                "region": "South India",
                "job_category": "Engineering"
            },
            request_only=True,
        ),
        OpenApiExample(
            "Example Response — Low Risk",
            value={
                "probability": 18.45,
                "decision": "Approved"
            },
            response_only=True,
            status_codes=["200"]
        ),
        OpenApiExample(
            "Example Request — High Risk",
            value={
                "age": 22,
                "income": 18000,
                "experience": 1,
                "current_house_yrs": 1,
                "cur_job_years": 0,
                "marital_status": "single",
                "house_ownership": "rented",
                "car_ownership": "no",
                "region": "North-East India",
                "job_category": "Hospitality & Services"
            },
            request_only=True,
        ),
        OpenApiExample(
            "Example Response — High Risk",
            value={
                "probability": 84.72,
                "decision": "Rejected"
            },
            response_only=True,
            status_codes=["200"]
        ),
    ]
)
class PredictRiskAPIView(APIView):

    def post(self, request):
        serializer = PredictSerializer(data=request.data)
        if serializer.is_valid():
            score = predict_risk(serializer.validated_data)
            return Response({
                "probability": round(score * 100, 2),
                "decision": "Approved" if score <= 0.3 else "Rejected" if score >= 0.8 else "Pending"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)