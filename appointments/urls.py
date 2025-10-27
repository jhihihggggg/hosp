from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    # Public booking (no login required)
    path('book/', views.public_booking, name='public_booking'),
    
    # Staff-only URLs (login required)
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
