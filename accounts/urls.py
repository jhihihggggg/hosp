from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('receptionist-dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    path('lab-dashboard/', views.lab_dashboard, name='lab_dashboard'),
    path('pharmacy-dashboard/', views.pharmacy_dashboard, name='pharmacy_dashboard'),
    path('canteen-dashboard/', views.canteen_dashboard, name='canteen_dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Display Monitor
    path('display-monitor/', views.display_monitor, name='display_monitor'),
    
    # Dashboard Sub-Features
    path('user-management/', views.user_management, name='user_management'),
    path('system-settings/', views.system_settings, name='system_settings'),
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    path('vitals/<int:appointment_id>/', views.patient_vitals_entry, name='patient_vitals_entry'),
    path('payment/<int:appointment_id>/', views.payment_collection, name='payment_collection'),
    
    # AJAX APIs
    path('api/call-next-patient/', views.call_next_patient, name='call_next_patient'),
    path('api/prescription/<int:prescription_id>/mark-printed/', views.mark_prescription_printed, name='mark_prescription_printed'),
]
