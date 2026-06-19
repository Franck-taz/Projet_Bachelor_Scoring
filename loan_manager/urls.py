from django.urls import path
from loan_manager.api_views import PredictRiskAPIView
from . import views
from .views import login_view

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('apply/', views.apply_loan, name='apply_loan'),
    path('success/', views.success_page, name='success_page'),
    path('api/predict/', PredictRiskAPIView.as_view(), name='api_predict'),
    path('messages/', views.messages_view, name='messages'),
    path('messages/unread/', views.unread_count, name='unread_count'),
    path('apply/review/', views.review_loan, name='review_loan'),
    path('about/', views.about_view, name='about'),
    path('legal/', views.legal_view, name='legal'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/delete/', views.delete_account, name='delete_account'),
]