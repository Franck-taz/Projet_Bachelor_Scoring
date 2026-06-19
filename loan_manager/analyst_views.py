from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
import json


def analyst_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('analyst_dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            username = None

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('analyst_dashboard')
        else:
            messages.error(request, "Access denied. Invalid credentials or insufficient permissions.")

    return render(request, 'loan_manager/analyst/login.html')


def analyst_logout(request):
    logout(request)
    return redirect('analyst_login')


@login_required
def analyst_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')

    from .models import LoanApplication
    applications = LoanApplication.objects.all().select_related('user').order_by('-created_at')

    total     = applications.count()
    pending   = applications.filter(final_decision__isnull=True).count()
    approved  = applications.filter(final_decision='Approved').count()
    rejected  = applications.filter(final_decision='Rejected').count()
    high_risk = applications.filter(risk_score__gte=80).count()

    ai_approved = applications.filter(ai_prediction='Approved').count()
    ai_pending  = applications.filter(ai_prediction='Pending').count()
    ai_rejected = applications.filter(ai_prediction='Rejected').count()

    context = {
        'applications': applications,
        'total':     total,
        'pending':   pending,
        'approved':  approved,
        'rejected':  rejected,
        'high_risk': high_risk,
        'ai_approved': ai_approved,
        'ai_pending':  ai_pending,
        'ai_rejected': ai_rejected,
    }
    return render(request, 'loan_manager/analyst/dashboard.html', context)


@login_required
def analyst_application_detail(request, app_id):
    if not request.user.is_staff:
        return redirect('login')

    from .models import LoanApplication, AnalystNote
    application = get_object_or_404(LoanApplication, id=app_id)
    notes = AnalystNote.objects.filter(application=application).order_by('-created_at')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_note':
            comment = request.POST.get('comment')
            if comment:
                AnalystNote.objects.create(
                    application=application,
                    analyst=request.user,
                    comment=comment
                )
        return redirect('analyst_application_detail', app_id=app_id)

    return render(request, 'loan_manager/analyst/detail.html', {
        'application': application,
        'notes': notes,
    })

@login_required
def analyst_update_status(request, app_id):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        from .models import LoanApplication
        application = get_object_or_404(LoanApplication, id=app_id)
        data = json.loads(request.body)
        new_status = data.get('status')

        if new_status in ['Approved', 'Rejected']:
            application.final_decision  = new_status
            application.save()
            return JsonResponse({'success': True, 'status': new_status})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

@login_required
def analyst_update_status_form(request, app_id):
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        from .models import LoanApplication
        application = get_object_or_404(LoanApplication, id=app_id)
        new_status = request.POST.get('status')
        if new_status in ['Approved', 'Rejected', 'Pending']:
            application.final_decision  = new_status
            application.save()
    return redirect('analyst_application_detail', app_id=app_id)