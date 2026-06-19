from django.db import models
from django.contrib.auth.models import User # Ne pas oublier l'import !
# En haut de models.py, après les imports
from django.core.exceptions import ValidationError

def validate_age(value):
    if value < 18:
        raise ValidationError("You must be at least 18 years old.")
    if value > 80:
        raise ValidationError("Age cannot exceed 80 years.")

def validate_income(value):
    if value <= 0:
        raise ValidationError("Annual income must be greater than 0.")

def validate_experience(value):
    if value < 0 or value > 50:
        raise ValidationError("Experience must be between 0 and 50 years.")

def validate_house_years(value):
    if value < 0 or value > 50:
        raise ValidationError("Years at address must be between 0 and 50.")

def validate_job_years(value):
    if value < 0 or value > 50:
        raise ValidationError("Years in job must be between 0 and 50.")

def validate_loan_amount(value):
    if value < 1000:
        raise ValidationError("Loan amount must be at least $1,000.")

class LoanApplication(models.Model):
    # LIEN AVEC L'UTILISATEUR
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")

    # CHOIX (Inchangés mais regroupés pour la lisibilité)
    MARITAL_STATUS_CHOICES = [("married", "Married"), ("single", "Single")]
    HOUSE_CHOICES = [("owned", "Owned"), ("rented", "Rented"), ("norent_noown", "No House No Rent")]
    CAR_CHOICES = [("yes", "Yes"), ("no", "No")]
    REGION_CHOICES = [
        ("North India", "North"), ("South India", "South"), 
        ("West India", "West"), ("East India", "East"),
        ("Central India", "Central"), ("North-East India", "Northeast")
    ]
    # Tes catégories de jobs sont parfaites pour CatBoost !
    JOB_CATEGORY_CHOICES = [
        ("Engineering", "Engineering"), ("Technology & IT", "Technology & IT"),
        ("IT, Data & Analytics", "IT, Data & Analytics"), ("Healthcare & Medical", "Healthcare & Medical"),
        ("Creative, Design & Media", "Creative, Design & Media"), ("Law, Government & Public Service", "Law, Government & Public Service"),
        ("Business, Finance & Administration", "Business, Finance & Administration"), ("Aviation, Defense & Security", "Aviation, Defense & Security"),
        ("Education, Research & Documentation", "Education, Research & Documentation"), ("Hospitality & Services", "Hospitality & Services"),
    ]

    # CHAMPS NUMÉRIQUES
    age = models.IntegerField(validators=[validate_age])
    income = models.FloatField(validators=[validate_income])
    experience = models.IntegerField(validators=[validate_experience])
    current_house_yrs = models.IntegerField(validators=[validate_house_years])
    cur_job_years = models.IntegerField(validators=[validate_job_years])
    # INFORMATIONS DU PRÊT
    loan_amount = models.FloatField(validators=[validate_loan_amount])

    # CHAMPS CATÉGORIELS
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    house_ownership = models.CharField(max_length=15, choices=HOUSE_CHOICES)
    car_ownership = models.CharField(max_length=5, choices=CAR_CHOICES)
    region = models.CharField(max_length=20, choices=REGION_CHOICES)
    job_category = models.CharField(max_length=50, choices=JOB_CATEGORY_CHOICES)

    # RÉSULTATS IA
    risk_score = models.FloatField(null=True, blank=True)
    risk_flag = models.IntegerField(null=True, blank=True)  # 0 ou 1
    ai_prediction = models.CharField(
    max_length=20, null=True, blank=True,
    choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")] )

# DÉCISION FINALE ANALYSTE
    final_decision = models.CharField(
    max_length=20, null=True, blank=True,
    choices=[("Approved", "Approved"), ("Rejected", "Rejected")])

    # TIMESTAMPS
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Correction ici : on utilise risk_flag au lieu de risk_label
        return f"Application {self.id} - User: {self.user.username} - Risk: {self.risk_flag}"
    @property
    def reference(self):
        return f"APP-{self.created_at.year}-{self.id:06d}"

# N'OUBLIE PAS CETTE TABLE POUR TON RAPPORT
class AnalystNote(models.Model):
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name="notes")
    analyst = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'is_staff': True})
    comment = models.TextField()
    is_read = models.BooleanField(default=False)  # ← nouveau
    created_at = models.DateTimeField(auto_now_add=True)


class ClientProfile(models.Model):
    """Profil étendu pour les clients (demandeurs de prêt)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Client: {self.user.first_name} {self.user.last_name}"
    

class AnalystProfile(models.Model):
    """Profil étendu pour les analystes de risque (staff interne)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="analyst_profile")
    department = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analyst: {self.user.first_name} {self.user.last_name}"
    


class Document(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('payslip', 'Pay Slip'),
        ('electricity', 'Electricity Bill'),
        ('rent', 'Rent Receipt'),
        ('contract', 'Work Contract'),
        ('other', 'Other'),
    ]
    application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='documents/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} – Application {self.application.id}"