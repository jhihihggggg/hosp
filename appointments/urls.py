from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    # Public booking (no login required)
    path('book/', views.public_booking, name='public_booking'),
    
    # API endpoints for calendar/schedule
    path('api/doctor/<int:doctor_id>/dates/', views.get_doctor_available_dates, name='doctor_available_dates'),
    path('api/doctor/<int:doctor_id>/slots/<str:date_str>/', views.get_doctor_time_slots, name='doctor_time_slots'),
    
    # Doctor Schedule Management (Admin only)
    path('schedules/', views.doctor_schedule_list, name='doctor_schedule_list'),
    path('schedules/create/', views.doctor_schedule_create, name='doctor_schedule_create'),
    path('schedules/<int:pk>/edit/', views.doctor_schedule_edit, name='doctor_schedule_edit'),
    path('schedules/<int:pk>/delete/', views.doctor_schedule_delete, name='doctor_schedule_delete'),
    
    # Receptionist quick booking
    path('receptionist-booking/', views.receptionist_booking, name='receptionist_booking'),
    
    # Regular appointment management
    path('', views.appointment_list, name='appointment_list'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/call/', views.call_patient, name='call_patient'),
    path('<int:pk>/complete/', views.complete_appointment, name='complete_appointment'),
    path('queue/', views.queue_display, name='queue_display'),
    path('monitor/', views.display_monitor, name='display_monitor'),
    
    # Prescriptions
    path('<int:appointment_id>/prescription/create/', views.prescription_create, name='prescription_create'),
    path('prescription/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('prescription/<int:pk>/print/', views.prescription_print, name='prescription_print'),
]
