from rest_framework import serializers
from .models import LoanApplication


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = "__all__"
        read_only_fields = [
            "risk_score",
            "risk_flag",
            "ai_prediction",
            "final_decision",
            "user"
        ]


class PredictSerializer(serializers.Serializer):
    age = serializers.IntegerField(
        min_value=18, max_value=80,
        help_text="Applicant's age (18–80)"
    )
    income = serializers.FloatField(
        min_value=0,
        help_text="Annual income in dollars"
    )
    experience = serializers.IntegerField(
        min_value=0, max_value=50,
        help_text="Total professional experience in years"
    )
    current_house_yrs = serializers.IntegerField(
        min_value=0,
        help_text="Number of years at current address"
    )
    cur_job_years = serializers.IntegerField(
        min_value=0, max_value=50,
        help_text="Number of years in current job"
    )
    marital_status = serializers.ChoiceField(
        choices=["married", "single"],
        help_text="Marital status: 'married' or 'single'"
    )
    house_ownership = serializers.ChoiceField(
        choices=["owned", "rented", "norent_noown"],
        help_text="Housing situation: 'owned', 'rented', or 'norent_noown'"
    )
    car_ownership = serializers.ChoiceField(
        choices=["yes", "no"],
        help_text="Whether the applicant owns a car: 'yes' or 'no'"
    )
    region = serializers.ChoiceField(
        choices=[
            "North India", "South India", "West India",
            "East India", "Central India", "North-East India"
        ],
        help_text="Geographic region of the applicant"
    )
    job_category = serializers.ChoiceField(
        choices=[
            "Engineering", "Technology & IT", "IT, Data & Analytics",
            "Healthcare & Medical", "Creative, Design & Media",
            "Law, Government & Public Service",
            "Business, Finance & Administration",
            "Aviation, Defense & Security",
            "Education, Research & Documentation",
            "Hospitality & Services"
        ],
        help_text="Professional sector of the applicant"
    )


class PredictResponseSerializer(serializers.Serializer):
    probability = serializers.FloatField(
        help_text="Risk probability as a percentage (0–100). Higher means riskier."
    )
    decision = serializers.ChoiceField(
        choices=["Approved", "Pending", "Rejected"],
        help_text="AI decision: Approved (≤30%), Pending (30–80%), Rejected (≥80%)"
    )