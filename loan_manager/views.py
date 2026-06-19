from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import LoanApplicationForm, RegistrationForm, ProfileUpdateForm
from .models import LoanApplication, ClientProfile
from django.contrib import messages
from .ml.predictor import predict_risk


@login_required
def apply_loan(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)
        if form.is_valid():
            request.session['loan_application_data'] = form.cleaned_data
            return redirect('review_loan')
    else:
        form = LoanApplicationForm()
    return render(request, 'loan_manager/apply.html', {'form': form})


@login_required
def review_loan(request):
    data = request.session.get('loan_application_data')
    if not data:
        return redirect('apply_loan')

    if request.method == 'POST':
        from .models import Document
        application = LoanApplication(**data)
        application.user = request.user

        score = predict_risk(data)
        application.risk_score = round(score * 100, 2)
        application.risk_flag = 1 if score >= 0.5 else 0
        application.ai_prediction = (
            "Approved" if score <= 0.3 else
            "Rejected" if score >= 0.8 else
            "Pending"
        )
        application.save()

        files = request.FILES.getlist('documents')
        doc_types = request.POST.getlist('document_types')
        for i, f in enumerate(files):
            doc_type = doc_types[i] if i < len(doc_types) else 'other'
            Document.objects.create(
                application=application,
                document_type=doc_type,
                file=f
            )

        del request.session['loan_application_data']
        return redirect('success_page')

    return render(request, 'loan_manager/review.html', {'data': data})


@login_required
def success_page(request):
    application = LoanApplication.objects.filter(user=request.user).last()
    return render(request, 'loan_manager/success.html', {'application': application})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid email or password.")
    return render(request, "loan_manager/login.html")


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(username=email).exists():
                messages.error(request, "An account with this email already exists. Please log in.")
                return render(request, 'loan_manager/register.html', {'form': form})
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.username = email
            user.save()
            ClientProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'loan_manager/register.html', {'form': form})


@login_required
def dashboard(request):
    from .models import AnalystNote
    applications = LoanApplication.objects.filter(user=request.user).order_by('-created_at')
    unread_count = AnalystNote.objects.filter(
        application__user=request.user,
        is_read=False
    ).count()
    return render(request, 'loan_manager/dashboard.html', {
        'applications': applications,
        'unread_count': unread_count,
    })


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def messages_view(request):
    from .models import AnalystNote
    notes = AnalystNote.objects.filter(
        application__user=request.user
    ).order_by('-created_at')
    notes.filter(is_read=False).update(is_read=True)
    return render(request, 'loan_manager/messages.html', {'notes': notes})


@login_required
def unread_count(request):
    from .models import AnalystNote
    from django.http import JsonResponse
    count = AnalystNote.objects.filter(
        application__user=request.user,
        is_read=False
    ).count()
    return JsonResponse({'count': count})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            new_email = form.cleaned_data['email']
            user.email = new_email
            user.username = new_email
            if form.cleaned_data['new_password']:
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                login(request, user)
                messages.success(request, "Profile updated successfully (password changed).")
            else:
                user.save()
                messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(user=request.user, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    return render(request, 'loan_manager/profile.html', {'form': form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted.")
        return redirect('login')
    return redirect('profile')


def about_view(request):
    return render(request, 'loan_manager/about.html')

def legal_view(request):
    return render(request, 'loan_manager/legal.html')