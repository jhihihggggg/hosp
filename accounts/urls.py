from django.urls import path
from . import views
from . import pc_views

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-finance/', views.admin_finance_dashboard, name='admin_finance'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('receptionist-dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    
    # Reception Features - TODO: implement these views
    # path('reception/register-patient/', views.reception_register_patient, name='reception_register_patient'),
    # path('reception/billing/', views.reception_billing, name='reception_billing'),
    # path('reception/voucher/<int:appointment_id>/', views.reception_print_voucher, name='reception_print_voucher'),
    # path('reception/prescription/<int:prescription_id>/', views.reception_print_prescription, name='reception_print_prescription'),
    # path('reception/doctor-serials/<int:doctor_id>/', views.reception_doctor_serials, name='reception_doctor_serials'),
    
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
    path('doctor-management/', views.doctor_management, name='doctor_management'),
    path('system-settings/', views.system_settings, name='system_settings'),
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    path('vitals/<int:appointment_id>/', views.patient_vitals_entry, name='patient_vitals_entry'),
    path('payment/<int:appointment_id>/', views.payment_collection, name='payment_collection'),
    
    # PC (Persistent Commission) System
    path('pc-dashboard/', pc_views.pc_dashboard, name='pc_dashboard'),
    path('pc-members/<str:member_type>/', pc_views.pc_member_list, name='pc_member_list'),
    path('pc-members/create/', pc_views.pc_member_create, name='pc_member_create'),
    path('pc-member/<str:pc_code>/', pc_views.pc_member_detail, name='pc_member_detail'),
    path('pc-member/<str:pc_code>/mark-paid/', pc_views.pc_mark_paid, name='pc_mark_paid'),
    path('pc-transaction/create/', pc_views.pc_transaction_create, name='pc_transaction_create'),
    
    # AJAX APIs
    path('api/pc-lookup/', pc_views.pc_lookup_api, name='pc_lookup_api'),
    path('api/call-next-patient/', views.call_next_patient, name='call_next_patient'),
    path('api/prescription/<int:prescription_id>/mark-printed/', views.mark_prescription_printed, name='mark_prescription_printed'),
]

