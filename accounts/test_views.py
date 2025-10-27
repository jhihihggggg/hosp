"""
Test views that look like real dashboards - NO database queries
"""
from django.shortcuts import render
from django.http import HttpResponse

def test_admin(request):
    """Full featured test admin dashboard"""
    context = {
        'period': 'today',
        'total_income': 125000,
        'total_expenses': 45000,
        'profit': 80000,
        'profit_margin': 64.0,
        'appointment_income': 35000,
        'lab_income': 45000,
        'pharmacy_income': 30000,
        'canteen_income': 15000,
        'total_patients': 450,
        'new_patients_period': 12,
        'period_appointments': 28,
        'completed_appointments': 24,
        'total_staff': 35,
        'doctors_count': 8,
        'nurses_count': 12,
        'other_staff': 15,
        'active_investors': 5,
        'total_investment': 5000000,
        'outstanding_lab_payments': 12000,
        'outstanding_pharmacy_payments': 8000,
        'low_stock_count': 3,
        'pending_lab_orders': 6,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

def test_doctor(request):
    """Full featured test doctor dashboard"""
    context = {
        'today_appointments': 8,
        'pending_appointments': 3,
        'completed_today': 5,
        'total_patients': 120,
        'upcoming_appointments': [],
        'recent_prescriptions': [],
        'doctor': {'first_name': 'Test', 'specialization': 'General Medicine'},
    }
    return render(request, 'accounts/doctor_dashboard.html', context)

def test_reception(request):
    """Full featured test reception dashboard"""
    context = {
        'today_appointments': 15,
        'pending_appointments': 5,
        'completed_appointments': 10,
        'walk_in_patients': 3,
        'total_patients': 450,
        'recent_appointments': [],
        'available_doctors': [],
    }
    return render(request, 'accounts/receptionist_dashboard.html', context)

def test_display(request):
    """Full featured test display monitor"""
    context = {
        'current_serial': 15,
        'waiting_count': 8,
        'doctors_available': 4,
        'appointments': [],
        'announcements': 'Welcome to Nazipuruhs Hospital',
    }
    return render(request, 'accounts/display_monitor.html', context)
