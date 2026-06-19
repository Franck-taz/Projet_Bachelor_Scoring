from django import forms
from django.core.exceptions import ValidationError
from .models import LoanApplication
from django.contrib.auth.models import User


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            'age', 'income', 'experience', 'current_house_yrs',
            'cur_job_years', 'loan_amount', 'marital_status', 'house_ownership',
            'car_ownership', 'region', 'job_category'
        ]
        widgets = {
            'job_category': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'income': forms.NumberInput(attrs={'placeholder': 'Ex: 45000'}),
            'loan_amount': forms.NumberInput(attrs={'placeholder': 'Ex: 15000'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')
        experience = cleaned_data.get('experience')
        cur_job_years = cleaned_data.get('cur_job_years')
        income = cleaned_data.get('income')
        loan_amount = cleaned_data.get('loan_amount')

        # Age
        if age is not None:
            if age < 18:
                self.add_error('age', "You must be at least 18 years old.")
            elif age > 80:
                self.add_error('age', "Age cannot exceed 80 years.")

        # Income
        if income is not None and income <= 0:
            self.add_error('income', "Annual income must be greater than 0.")

        # Loan amount
        if loan_amount is not None and loan_amount < 1000:
            self.add_error('loan_amount', "Loan amount must be at least $1,000.")

        # Experience ≤ age - 18
        if age is not None and experience is not None:
            max_exp = age - 18
            if experience < 0:
                self.add_error('experience', "Experience cannot be negative.")
            elif experience > max_exp:
                self.add_error('experience',
                    f"Experience cannot exceed {max_exp} years for someone aged {age}.")

        # Years in current job ≤ experience
        if experience is not None and cur_job_years is not None:
            if cur_job_years < 0:
                self.add_error('cur_job_years', "Years in current job cannot be negative.")
            elif cur_job_years > experience:
                self.add_error('cur_job_years',
                    f"Years in current job cannot exceed total experience ({experience} years).")
        # Years at current address ≤ age
        current_house_yrs = cleaned_data.get('current_house_yrs')
        if age is not None and current_house_yrs is not None:
            if current_house_yrs < 0:
                self.add_error('current_house_yrs', "Years at current address cannot be negative.")
            elif current_house_yrs > age:
                self.add_error('current_house_yrs',
                    f"Years at current address cannot exceed your age ({age} years).")

        return cleaned_data


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        if password and len(password) < 8:
            raise ValidationError("Password must be at least 8 characters.")
        return cleaned_data


class ProfileUpdateForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label="Last Name", max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(label="Email Address",
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    new_password = forms.CharField(label="New Password", required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Leave blank to keep current'}))
    confirm_new_password = forms.CharField(label="Confirm New Password", required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exclude(pk=self.user.pk).exists():
            raise ValidationError("This email is already used by another account.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_new_password")
        if new_password:
            if len(new_password) < 8:
                self.add_error('new_password', "Password must be at least 8 characters.")
            elif new_password != confirm:
                self.add_error('confirm_new_password', "Passwords do not match.")
        return cleaned_data