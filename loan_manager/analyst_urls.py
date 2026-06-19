from django.urls import path
from . import analyst_views
 
urlpatterns = [
    path('login/', analyst_views.analyst_login, name='analyst_login'),
    path('logout/', analyst_views.analyst_logout, name='analyst_logout'),
    path('dashboard/', analyst_views.analyst_dashboard, name='analyst_dashboard'),
    path('application/<int:app_id>/', analyst_views.analyst_application_detail, name='analyst_application_detail'),
    path('update-status/<int:app_id>/', analyst_views.analyst_update_status, name='analyst_update_status'),
    path('application/<int:app_id>/update/', analyst_views.analyst_update_status_form, name='analyst_update_status_form'),
]
 