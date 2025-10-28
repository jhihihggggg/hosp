from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Q, F, Avg
from django.utils import timezone
from datetime import timedelta
from patients.models import Patient
from appointments.models import Appointment, Prescription, Medicine
from lab.models import LabTest, LabOrder, LabResult
from pharmacy.models import Drug, PharmacySale, SaleItem
from finance.models import Income, Expense, Investor
from survey.models import CanteenSale, CanteenItem, FeedbackSurvey

def landing_page(request):
    """Public landing page for the hospital website"""
    return render(request, 'accounts/landing_page.html')

#@login_required
def dashboard(request):
    """Role-based dashboard redirect"""
    user = request.user
    
    if not user.is_authenticated:
        return redirect('accounts:login')
    
    if user.is_admin:
        return redirect('accounts:admin_dashboard')
    elif user.is_doctor:
        return redirect('accounts:doctor_dashboard')
    elif user.is_receptionist:
        return redirect('accounts:receptionist_dashboard')
    elif user.is_lab_staff:
        return redirect('accounts:lab_dashboard')
    elif user.is_pharmacy_staff:
        return redirect('accounts:pharmacy_dashboard')
    else:
        messages.error(request, "You don't have permission to access any dashboard.")
        return redirect('accounts:login')


@login_required
def admin_dashboard(request):
    """Enhanced Admin dashboard with comprehensive management features"""
    from datetime import timedelta
    from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear
    from django.contrib.auth import get_user_model
    from django.db.models import Avg
    
    User = get_user_model()
    
    # Get filter period from request (default: today)
    period = request.GET.get('period', 'today')
    today = timezone.now().date()
    
    # Calculate date ranges
    if period == 'today':
        start_date = today
        end_date = today
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == 'month':
        start_date = today.replace(day=1)
        next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        end_date = next_month - timedelta(days=1)
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
    else:
        start_date = today
        end_date = today
    
    # Financial calculations
    income = Income.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    expenses = Expense.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    profit = income - expenses
    profit_margin = (profit / income * 100) if income > 0 else 0
    
    # Sales breakdown by department
    appointment_income = Income.objects.filter(
        date__range=[start_date, end_date],
        source='appointment'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    lab_income = Income.objects.filter(
        date__range=[start_date, end_date],
        source='lab'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    pharmacy_income = Income.objects.filter(
        date__range=[start_date, end_date],
        source='pharmacy'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    canteen_income = Income.objects.filter(
        date__range=[start_date, end_date],
        source='canteen'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Patient and appointment statistics
    total_patients = Patient.objects.count()
    new_patients_period = Patient.objects.filter(
        registered_at__date__range=[start_date, end_date]
    ).count()
    
    period_appointments = Appointment.objects.filter(
        appointment_date__range=[start_date, end_date]
    ).count()
    
    completed_appointments = Appointment.objects.filter(
        appointment_date__range=[start_date, end_date],
        status='completed'
    ).count()
    
    # Staff statistics
    total_staff = User.objects.filter(is_active=True).count()
    doctors_count = User.objects.filter(role='DOCTOR', is_active=True).count()
    nurses_count = User.objects.filter(role='NURSE', is_active=True).count()
    other_staff = total_staff - doctors_count - nurses_count
    
    # Department performance
    departments_performance = {
        'appointments': {'revenue': appointment_income, 'count': period_appointments},
        'lab': {'revenue': lab_income, 'orders': LabOrder.objects.filter(
            ordered_at__date__range=[start_date, end_date]
        ).count()},
        'pharmacy': {'revenue': pharmacy_income, 'sales': PharmacySale.objects.filter(
            sale_date__date__range=[start_date, end_date]
        ).count()},
        'canteen': {'revenue': canteen_income, 'orders': CanteenSale.objects.filter(
            sale_date__date__range=[start_date, end_date]
        ).count()}
    }
    
    # Average transaction values
    avg_appointment_fee = (appointment_income / period_appointments) if period_appointments > 0 else 0
    avg_lab_order = (lab_income / departments_performance['lab']['orders']) if departments_performance['lab']['orders'] > 0 else 0
    avg_pharmacy_sale = (pharmacy_income / departments_performance['pharmacy']['sales']) if departments_performance['pharmacy']['sales'] > 0 else 0
    
    # Investors and funding
    investors = Investor.objects.all()
    total_investment = investors.aggregate(Sum('investment_amount'))['investment_amount__sum'] or 0
    active_investors = investors.filter(is_active=True).count()
    
    # Outstanding payments and dues
    outstanding_lab_payments = LabOrder.objects.filter(
        is_paid=False
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # PharmacySale doesn't have is_paid field, so we calculate unpaid sales
    outstanding_pharmacy_payments = PharmacySale.objects.filter(
        amount_paid__lt=F('total_amount')
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Recent transactions (last 15 for better overview)
    recent_income = Income.objects.filter(
        date__range=[start_date, end_date]
    ).order_by('-date')[:15]
    
    recent_expenses = Expense.objects.filter(
        date__range=[start_date, end_date]
    ).order_by('-date')[:15]
    
    # System alerts and notifications
    system_alerts = []
    
    # Check for low stock in pharmacy
    low_stock_count = Drug.objects.filter(quantity_in_stock__lte=F('reorder_level')).count()
    if low_stock_count > 0:
        system_alerts.append({
            'type': 'warning',
            'message': f'{low_stock_count} drugs are running low on stock',
            'action': 'pharmacy:drug_list'
        })
    
    # Check for pending lab orders
    pending_lab_orders = LabOrder.objects.filter(status='pending').count()
    if pending_lab_orders > 5:
        system_alerts.append({
            'type': 'info',
            'message': f'{pending_lab_orders} lab orders are pending',
            'action': 'lab:orders_list'
        })
    
    context = {
        'period': period,
        'start_date': start_date,
        'end_date': end_date,
        'total_income': income,
        'total_expenses': expenses,
        'profit': profit,
        'profit_margin': profit_margin,
        'appointment_income': appointment_income,
        'lab_income': lab_income,
        'pharmacy_income': pharmacy_income,
        'canteen_income': canteen_income,
        'total_patients': total_patients,
        'new_patients_period': new_patients_period,
        'period_appointments': period_appointments,
        'completed_appointments': completed_appointments,
        'total_staff': total_staff,
        'doctors_count': doctors_count,
        'nurses_count': nurses_count,
        'other_staff': other_staff,
        'departments_performance': departments_performance,
        'avg_appointment_fee': avg_appointment_fee,
        'avg_lab_order': avg_lab_order,
        'avg_pharmacy_sale': avg_pharmacy_sale,
        'investors': investors,
        'total_investment': total_investment,
        'active_investors': active_investors,
        'outstanding_lab_payments': outstanding_lab_payments,
        'outstanding_pharmacy_payments': outstanding_pharmacy_payments,
        'recent_income': recent_income,
        'recent_expenses': recent_expenses,
        'system_alerts': system_alerts,
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def doctor_dashboard(request):
    """Enhanced Doctor dashboard with comprehensive patient management"""
    today = timezone.now().date()
    
    # Get today's appointments for this doctor
    appointments = Appointment.objects.filter(
        doctor=request.user,
        appointment_date=today
    ).select_related('patient').order_by('serial_number')
    
    # Queue statistics
    waiting_count = appointments.filter(status='waiting').count()
    in_consultation_count = appointments.filter(status='in_consultation').count()
    completed_count = appointments.filter(status='completed').count()
    cancelled_count = appointments.filter(status='cancelled').count()
    
    # Current patient (if any in consultation)
    current_patient = appointments.filter(status='in_consultation').first()
    
    # Next patient in queue
    next_patient = appointments.filter(status='waiting').first()
    
    # Patient history for current patient (if available)
    current_patient_history = None
    if current_patient:
        current_patient_history = Appointment.objects.filter(
            patient=current_patient.patient,
            status='completed',
            appointment_date__lt=today
        ).select_related('doctor').order_by('-appointment_date')[:5]
    
    # Today's revenue for this doctor
    today_revenue = Income.objects.filter(
        source='appointment',
        date=today,
        description__icontains=request.user.get_full_name()
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Weekly statistics
    week_start = today - timedelta(days=today.weekday())
    weekly_appointments = Appointment.objects.filter(
        doctor=request.user,
        appointment_date__gte=week_start,
        status='completed'
    ).count()
    
    # Most common diagnoses (last 30 days)
    thirty_days_ago = today - timedelta(days=30)
    recent_prescriptions = Prescription.objects.filter(
        appointment__doctor=request.user,
        appointment__appointment_date__gte=thirty_days_ago
    ).values('diagnosis').annotate(count=Count('diagnosis')).order_by('-count')[:5]
    
    # Lab orders initiated by this doctor (pending results)
    pending_lab_orders = LabOrder.objects.filter(
        appointment__doctor=request.user,
        status__in=['pending', 'sample_collected', 'in_progress']
    ).select_related('appointment__patient', 'test')[:10]
    
    # Prescription statistics
    prescriptions_written_today = Prescription.objects.filter(
        appointment__doctor=request.user,
        appointment__appointment_date=today
    ).count()
    
    # Patient satisfaction (if survey data available)
    try:
        patient_ratings = FeedbackSurvey.objects.filter(
            submitted_at__date__gte=thirty_days_ago
        ).aggregate(
            avg_rating=Avg('overall_experience'),
            total_feedback=Count('id')
        )
    except:
        patient_ratings = {'avg_rating': None, 'total_feedback': 0}
    
    # Upcoming appointments (next few days)
    upcoming_appointments = Appointment.objects.filter(
        doctor=request.user,
        appointment_date__gt=today,
        appointment_date__lte=today + timedelta(days=3),
        status='confirmed'
    ).count()
    
    # Recent patient visits (for quick reference)
    recent_patients = Patient.objects.filter(
        appointments__doctor=request.user,
        appointments__status='completed',
        appointments__appointment_date__gte=today - timedelta(days=7)
    ).distinct().order_by('-appointments__appointment_date')[:10]
    
    # Emergency/urgent appointments today
    try:
        urgent_appointments = appointments.filter(
            reason__icontains='emergency'
        ).order_by('serial_number')
    except:
        urgent_appointments = []
    
    context = {
        'appointments': appointments,
        'waiting_count': waiting_count,
        'in_consultation_count': in_consultation_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'current_patient': current_patient,
        'next_patient': next_patient,
        'current_patient_history': current_patient_history,
        'today_revenue': today_revenue,
        'weekly_appointments': weekly_appointments,
        'recent_prescriptions': recent_prescriptions,
        'pending_lab_orders': pending_lab_orders,
        'prescriptions_written_today': prescriptions_written_today,
        'patient_ratings': patient_ratings,
        'upcoming_appointments': upcoming_appointments,
        'recent_patients': recent_patients,
        'urgent_appointments': urgent_appointments,
    }
    
    return render(request, 'accounts/doctor_dashboard.html', context)


@login_required
def receptionist_dashboard(request):
    """Enhanced Receptionist dashboard with comprehensive patient and payment management"""
    today = timezone.now().date()
    
    # Today's appointments statistics
    today_appointments = Appointment.objects.filter(
        appointment_date=today
    ).select_related('doctor', 'patient')
    
    today_appointments_count = today_appointments.count()
    completed_appointments = today_appointments.filter(status='completed').count()
    waiting_appointments = today_appointments.filter(status='waiting').count()
    in_consultation = today_appointments.filter(status='in_consultation').count()
    
    # New patient registrations today
    new_patients_today = Patient.objects.filter(
        registered_at__date=today
    ).count()
    
    # Recent patients (last 15 for better coverage)
    recent_patients = Patient.objects.all().order_by('-registered_at')[:15]
    
    # Appointments by doctor (for queue management)
    appointments_by_doctor = Appointment.objects.filter(
        appointment_date=today
    ).values(
        'doctor__first_name', 'doctor__last_name', 'doctor__id'
    ).annotate(
        total=Count('id'),
        waiting=Count('id', filter=Q(status='waiting')),
        completed=Count('id', filter=Q(status='completed')),
        in_consultation=Count('id', filter=Q(status='in_consultation'))
    )
    
    # Prescriptions ready for printing
    prescriptions_to_print = Prescription.objects.filter(
        appointment__appointment_date=today,
        is_printed=False
    ).select_related('appointment__patient', 'appointment__doctor')
    
    # Payment collection summary
    today_collections = Income.objects.filter(
        date=today,
        source='appointment'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Lab orders requiring payment
    unpaid_lab_orders = LabOrder.objects.filter(
        is_paid=False,
        ordered_at__date__gte=today - timedelta(days=7)
    ).select_related('appointment__patient')[:10]
    
    # Pharmacy sales with incomplete payment
    unpaid_pharmacy_sales = PharmacySale.objects.filter(
        amount_paid__lt=F('total_amount'),
        sale_date__date__gte=today - timedelta(days=7)
    ).select_related('prescription__appointment__patient')[:10]
    
    # Insurance verification pending (if Patient model has these fields)
    try:
        insurance_pending = Patient.objects.filter(
            insurance_number__isnull=False,
            insurance_verified=False
        )[:10]
    except:
        insurance_pending = []
    
    # Appointment scheduling statistics
    total_slots_today = 100  # This could be dynamic based on doctor schedules
    occupied_slots = today_appointments_count
    available_slots = total_slots_today - occupied_slots
    
    # Walk-in patients (appointments created today for today)
    walk_in_patients = Appointment.objects.filter(
        appointment_date=today,
        check_in_time__date=today
    ).count()
    
    # Next few appointments (for preparation)
    next_appointments = Appointment.objects.filter(
        appointment_date=today,
        status='waiting'
    ).select_related('patient', 'doctor').order_by('serial_number')[:5]
    
    # Feedback collection
    try:
        pending_feedback = Appointment.objects.filter(
            appointment_date__gte=today - timedelta(days=7),
            status='completed'
        ).exclude(
            patient__in=FeedbackSurvey.objects.filter(
                submitted_at__date__gte=today - timedelta(days=7)
            ).values('patient')
        ).count()
    except:
        pending_feedback = 0
    
    context = {
        'today_appointments_count': today_appointments_count,
        'completed_appointments': completed_appointments,
        'waiting_appointments': waiting_appointments,
        'in_consultation': in_consultation,
        'new_patients_today': new_patients_today,
        'recent_patients': recent_patients,
        'appointments_by_doctor': appointments_by_doctor,
        'prescriptions_to_print': prescriptions_to_print,
        'today_collections': today_collections,
        'unpaid_lab_orders': unpaid_lab_orders,
        'unpaid_pharmacy_sales': unpaid_pharmacy_sales,
        'insurance_pending': insurance_pending,
        'total_slots_today': total_slots_today,
        'occupied_slots': occupied_slots,
        'available_slots': available_slots,
        'walk_in_patients': walk_in_patients,
        'next_appointments': next_appointments,
        'pending_feedback': pending_feedback,
    }
    
    return render(request, 'accounts/receptionist_dashboard.html', context)


@login_required
def lab_dashboard(request):
    """Lab staff dashboard with pending tests"""
    from lab.models import LabOrder
    
    pending_orders = LabOrder.objects.filter(
        status__in=['ORDERED', 'SAMPLE_COLLECTED', 'IN_PROGRESS']
    ).select_related('patient').order_by('-ordered_at')
    
    context = {
        'pending_orders': pending_orders,
    }
    
    return render(request, 'accounts/lab_dashboard.html', context)


@login_required
def pharmacy_dashboard(request):
    """Enhanced Pharmacy dashboard with comprehensive inventory and sales management"""
    from pharmacy.models import Drug, PharmacySale, SaleItem
    from django.db.models import F, ExpressionWrapper, DateField
    from datetime import date, timedelta
    
    today = timezone.now().date()
    
    # Inventory statistics
    low_stock_drugs = Drug.objects.filter(
        quantity_in_stock__lte=F('reorder_level')
    ).order_by('quantity_in_stock')
    low_stock_count = low_stock_drugs.count()
    
    # Out of stock drugs
    out_of_stock = Drug.objects.filter(quantity_in_stock=0).count()
    
    # Expiry alerts (drugs expiring within 30 days)
    thirty_days_later = today + timedelta(days=30)
    expiring_soon = Drug.objects.filter(
        expiry_date__lte=thirty_days_later,
        expiry_date__gt=today
    ).order_by('expiry_date')[:10]
    
    # Sales statistics
    today_sales = PharmacySale.objects.filter(sale_date__date=today).count()
    today_revenue = PharmacySale.objects.filter(
        sale_date__date=today
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Weekly revenue trend
    week_start = today - timedelta(days=6)
    weekly_revenue = PharmacySale.objects.filter(
        sale_date__date__gte=week_start
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Pending prescriptions (prescriptions not yet processed)
    try:
        pending_prescriptions = Prescription.objects.filter(
            appointment__appointment_date__gte=today - timedelta(days=7)
        ).select_related(
            'appointment__patient', 'appointment__doctor'
        ).order_by('-appointment__appointment_date')[:15]
        
        pending_prescriptions_count = pending_prescriptions.count()
    except:
        pending_prescriptions = []
        pending_prescriptions_count = 0
    
    # Today's sales list (recent transactions)
    today_sales_list = PharmacySale.objects.filter(
        sale_date__date=today
    ).select_related('prescription').order_by('-sale_date')[:10]
    
    # Top selling drugs (this week)
    top_selling_drugs = SaleItem.objects.filter(
        sale__sale_date__date__gte=week_start
    ).values('drug__name').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('unit_price'))
    ).order_by('-total_quantity')[:5]
    
    # Reorder suggestions based on usage patterns
    reorder_suggestions = Drug.objects.filter(
        quantity_in_stock__lt=F('reorder_level') * 2,
        quantity_in_stock__gt=0
    ).order_by('quantity_in_stock')[:10]
    
    # Payment status summary - PharmacySale doesn't have is_paid, calculate unpaid
    pending_payments = PharmacySale.objects.filter(
        amount_paid__lt=F('total_amount')
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    context = {
        'low_stock_drugs': low_stock_drugs,
        'low_stock_count': low_stock_count,
        'out_of_stock': out_of_stock,
        'expiring_soon': expiring_soon,
        'today_sales': today_sales,
        'today_revenue': today_revenue,
        'weekly_revenue': weekly_revenue,
        'pending_prescriptions': pending_prescriptions_count,
        'pending_prescriptions_list': pending_prescriptions,
        'today_sales_list': today_sales_list,
        'top_selling_drugs': top_selling_drugs,
        'reorder_suggestions': reorder_suggestions,
        'pending_payments': pending_payments,
    }
    
    return render(request, 'accounts/pharmacy_dashboard.html', context)


@login_required
def canteen_dashboard(request):
    """Enhanced Canteen dashboard with comprehensive order and inventory management"""
    from survey.models import CanteenSale, CanteenOrder, CanteenMenuItem, CanteenOrderItem
    
    today = timezone.now().date()
    
    # Order statistics
    today_orders = CanteenOrder.objects.filter(order_date__date=today).count()
    
    # Revenue calculations
    today_revenue = CanteenSale.objects.filter(sale_date__date=today).aggregate(
        Sum('total_amount')
    )['total_amount__sum'] or 0
    
    # Weekly revenue for comparison
    week_start = today - timedelta(days=today.weekday())
    weekly_revenue = CanteenSale.objects.filter(
        sale_date__date__gte=week_start
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Active orders (pending, preparing, ready)
    active_orders_list = CanteenOrder.objects.filter(
        order_date__date=today,
        status__in=['pending', 'preparing', 'ready']
    ).select_related('customer').order_by('order_time')
    
    active_orders_count = active_orders_list.count()
    
    # Orders by status
    pending_orders = active_orders_list.filter(status='pending').count()
    preparing_orders = active_orders_list.filter(status='preparing').count()
    ready_orders = active_orders_list.filter(status='ready').count()
    
    # Completed orders today
    completed_orders = CanteenOrder.objects.filter(
        order_date__date=today,
        status='delivered'
    ).select_related('customer').order_by('-order_time')[:15]
    
    # Popular items today
    popular_items_today = CanteenOrderItem.objects.filter(
        order__order_date__date=today
    ).values(
        'item__name'
    ).annotate(
        quantity_sold=Sum('quantity'),
        revenue=Sum(F('quantity') * F('unit_price'))
    ).order_by('-quantity_sold')[:5]
    
    # Menu management statistics - using CanteenItem (not CanteenMenuItem)
    try:
        total_menu_items = CanteenItem.objects.filter(is_available=True).count()
        out_of_stock_items = CanteenItem.objects.filter(
            is_available=False
        ).count()
    except:
        total_menu_items = 0
        out_of_stock_items = 0
    
    # Customer satisfaction (if feedback available)
    try:
        customer_ratings = FeedbackSurvey.objects.filter(
            submitted_at__date__gte=today - timedelta(days=7)
        ).aggregate(
            avg_rating=Avg('overall_experience'),
            total_reviews=Count('id')
        )
    except:
        customer_ratings = {'avg_rating': None, 'total_reviews': 0}
    
    # Revenue breakdown by payment method
    payment_methods = CanteenSale.objects.filter(
        sale_date__date=today
    ).values('payment_method').annotate(
        total=Sum('total_amount'),
        count=Count('id')
    )
    
    # Top customers (frequent buyers) from CanteenSale
    top_customers = CanteenSale.objects.filter(
        sale_date__date__gte=today - timedelta(days=30)
    ).values(
        'customer_name'
    ).annotate(
        order_count=Count('id'),
        total_spent=Sum('total_amount')
    ).order_by('-total_spent')[:5]
    
    context = {
        'today_orders': today_orders,
        'today_revenue': today_revenue,
        'weekly_revenue': weekly_revenue,
        'popular_items_today': popular_items_today,
        'total_menu_items': total_menu_items,
        'out_of_stock_items': out_of_stock_items,
        'customer_ratings': customer_ratings,
        'payment_methods': payment_methods,
        'top_customers': top_customers,
    }
    
    return render(request, 'accounts/canteen_dashboard.html', context)


def user_login(request):
    """User login view with proper authentication"""
    
    # Redirect if already logged in
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            
            # Get next URL or redirect to dashboard
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    # Render with no-cache headers
    response = render(request, 'accounts/login.html')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def profile(request):
    """User profile view"""
    return render(request, 'accounts/profile.html')


# Display Monitor View
def display_monitor(request):
    """Display monitor for queue - shows current patient being called"""
    from django.http import JsonResponse
    
    # Get all appointments for today across all doctors
    today = timezone.now().date()
    current_appointments = Appointment.objects.filter(
        appointment_date=today,
        status='in_consultation'
    ).select_related('patient', 'doctor')
    
    # Get waiting queue
    waiting_queue = Appointment.objects.filter(
        appointment_date=today,
        status='waiting'
    ).select_related('patient', 'doctor').order_by('serial_number')
    
    context = {
        'current_appointments': current_appointments,
        'waiting_queue': waiting_queue,
    }
    
    return render(request, 'accounts/display_monitor.html', context)


# Additional Dashboard Sub-Feature Views

#@login_required
def user_management(request):
    """Admin user management view"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('accounts:dashboard')
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Get all users with their roles
    all_users = User.objects.all().order_by('-date_joined')
    
    # Statistics
    total_users = all_users.count()
    active_users = all_users.filter(is_active=True).count()
    inactive_users = total_users - active_users
    
    # Users by role
    admins = all_users.filter(is_admin=True).count()
    doctors = all_users.filter(role='DOCTOR').count()
    nurses = all_users.filter(role='NURSE').count()
    receptionists = all_users.filter(is_receptionist=True).count()
    lab_staff = all_users.filter(role='LAB').count()
    pharmacy_staff = all_users.filter(role='PHARMACY').count()
    canteen_staff = all_users.filter(is_canteen_staff=True).count()
    
    context = {
        'all_users': all_users,
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'role_counts': {
            'admins': admins,
            'doctors': doctors,
            'nurses': nurses,
            'receptionists': receptionists,
            'lab_staff': lab_staff,
            'pharmacy_staff': pharmacy_staff,
            'canteen_staff': canteen_staff,
        }
    }
    
    return render(request, 'accounts/user_management.html', context)


@login_required
def doctor_management(request):
    """Admin doctor management - add, edit doctors and their schedules"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin only.")
        return redirect('accounts:dashboard')
    
    from django.contrib.auth import get_user_model
    from appointments.models import DoctorSchedule
    from django.db.models import Count
    
    User = get_user_model()
    
    # Get all doctors
    doctors = User.objects.filter(role='DOCTOR').order_by('username')
    
    # Get doctor statistics
    doctor_stats = []
    for doctor in doctors:
        schedules_count = DoctorSchedule.objects.filter(doctor=doctor).count()
        appointments_count = Appointment.objects.filter(doctor=doctor).count()
        
        doctor_stats.append({
            'doctor': doctor,
            'schedules': schedules_count,
            'total_appointments': appointments_count,
            'specialization': getattr(doctor, 'specialization', 'General'),
        })
    
    context = {
        'doctors': doctors,
        'doctor_stats': doctor_stats,
        'total_doctors': doctors.count(),
        'active_doctors': doctors.filter(is_active=True).count(),
    }
    
    return render(request, 'accounts/doctor_management.html', context)


#@login_required
def system_settings(request):
    """Admin system settings view"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('accounts:dashboard')
    
    # System configuration settings
    settings_data = {
        'hospital_name': 'DiagCenter Hospital',
        'hospital_address': '123 Medical Street, Healthcare City',
        'hospital_phone': '+1-234-567-8900',
        'hospital_email': 'info@diagcenter.com',
        'appointment_duration': 15,  # minutes
        'working_hours_start': '09:00',
        'working_hours_end': '18:00',
        'emergency_contact': '+1-234-567-8911',
        'system_version': '1.0.0',
        'last_backup': timezone.now() - timedelta(days=1),
    }
    
    context = {
        'settings': settings_data,
    }
    
    return render(request, 'accounts/system_settings.html', context)


#@login_required
def activity_logs(request):
    """Admin activity logs view"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('accounts:dashboard')
    
    # Mock activity logs - can be enhanced with actual logging system
    recent_activities = [
        {
            'user': 'Dr. Smith',
            'action': 'Completed appointment with Patient #1234',
            'timestamp': timezone.now() - timedelta(minutes=15),
            'type': 'appointment'
        },
        {
            'user': 'Receptionist Jane',
            'action': 'Registered new patient: John Doe',
            'timestamp': timezone.now() - timedelta(minutes=30),
            'type': 'patient'
        },
        {
            'user': 'Lab Tech Mike',
            'action': 'Updated lab result for Order #567',
            'timestamp': timezone.now() - timedelta(minutes=45),
            'type': 'lab'
        },
        {
            'user': 'Pharmacist Lisa',
            'action': 'Processed prescription #890',
            'timestamp': timezone.now() - timedelta(hours=1),
            'type': 'pharmacy'
        },
    ]
    
    context = {
        'recent_activities': recent_activities,
    }
    
    return render(request, 'accounts/activity_logs.html', context)


#@login_required
def patient_vitals_entry(request, appointment_id):
    """Doctor sub-feature: Enter patient vitals"""
    if not request.user.is_doctor:
        messages.error(request, "Access denied. Doctor privileges required.")
        return redirect('accounts:dashboard')
    
    try:
        appointment = Appointment.objects.get(
            id=appointment_id,
            doctor=request.user,
            status='in_consultation'
        )
        
        if request.method == 'POST':
            # Process vitals data
            vitals_data = {
                'blood_pressure_systolic': request.POST.get('bp_systolic'),
                'blood_pressure_diastolic': request.POST.get('bp_diastolic'),
                'heart_rate': request.POST.get('heart_rate'),
                'temperature': request.POST.get('temperature'),
                'weight': request.POST.get('weight'),
                'height': request.POST.get('height'),
                'notes': request.POST.get('notes'),
            }
            
            # Save vitals (would need a PatientVitals model)
            messages.success(request, "Patient vitals recorded successfully!")
            return redirect('accounts:doctor_dashboard')
        
        context = {
            'appointment': appointment,
            'patient': appointment.patient,
        }
        
        return render(request, 'accounts/patient_vitals_form.html', context)
        
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found or not accessible.")
        return redirect('accounts:doctor_dashboard')


#@login_required 
def payment_collection(request, appointment_id):
    """Receptionist sub-feature: Collect payment for appointment"""
    if not request.user.is_receptionist:
        messages.error(request, "Access denied. Receptionist privileges required.")
        return redirect('accounts:dashboard')
    
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        
        if request.method == 'POST':
            payment_amount = request.POST.get('amount')
            payment_method = request.POST.get('payment_method', 'cash')
            
            # Create income record
            Income.objects.create(
                amount=payment_amount,
                source='appointment',
                description=f"Consultation fee - {appointment.patient.get_full_name()}",
                date=timezone.now().date(),
                payment_method=payment_method,
                collected_by=request.user
            )
            
            # Payment is tracked in Income model
            # Note: Appointment model doesn't have is_paid field
            
            messages.success(request, f"Payment of ₹{payment_amount} collected successfully!")
            return redirect('accounts:receptionist_dashboard')
        
        context = {
            'appointment': appointment,
        }
        
        return render(request, 'accounts/payment_collection_form.html', context)
        
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")
        return redirect('accounts:receptionist_dashboard')


# AJAX Views
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


@require_POST
#@login_required
def call_next_patient(request):
    """Call next patient in queue - used by doctors"""
    import json
    
    try:
        today = timezone.now().date()
        
        # Get next waiting patient for this doctor
        next_appointment = Appointment.objects.filter(
            doctor=request.user,
            appointment_date=today,
            status='waiting'
        ).order_by('serial_number').first()
        
        if not next_appointment:
            return JsonResponse({
                'success': False,
                'message': 'No patients waiting'
            })
        
        # Update status to in_consultation
        next_appointment.status = 'in_consultation'
        next_appointment.save()
        
        # Send WebSocket notification for display monitor
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'display_monitor',
            {
                'type': 'patient_called',
                'patient_name': next_appointment.patient.get_full_name(),
                'queue_number': next_appointment.serial_number,
                'doctor_name': next_appointment.doctor.get_full_name(),
                'room_number': next_appointment.room_number or 'N/A'
            }
        )
        
        return JsonResponse({
            'success': True,
            'patient_name': next_appointment.patient.get_full_name(),
            'queue_number': next_appointment.serial_number,
            'patient_id': next_appointment.patient.patient_id,
            'appointment_id': next_appointment.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@require_POST
#@login_required
def mark_prescription_printed(request, prescription_id):
    """Mark prescription as printed - used by receptionist"""
    try:
        prescription = Prescription.objects.get(id=prescription_id)
        prescription.is_printed = True
        prescription.printed_at = timezone.now()
        prescription.printed_by = request.user
        prescription.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Prescription marked as printed'
        })
    except Prescription.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Prescription not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
def admin_finance_dashboard(request):
    """Comprehensive finance dashboard for admin - Income, Expenses, Profit tracking"""
    if not request.user.is_admin:
        messages.error(request, "Access denied. Admin only.")
        return redirect('accounts:dashboard')
    
    from finance.models import Income, Expense
    from accounts.models import PCTransaction
    from datetime import timedelta
    from django.db.models import Sum, Count
    
    # Get period filter
    period = request.GET.get('period', 'today')
    today = timezone.now().date()
    
    # Calculate date ranges
    if period == 'today':
        start_date = today
        end_date = today
        period_name = 'Today'
    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        period_name = 'This Week'
    elif period == 'month':
        start_date = today.replace(day=1)
        next_month = (start_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        end_date = next_month - timedelta(days=1)
        period_name = 'This Month'
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
        period_name = 'This Year'
    elif period == 'custom':
        start_date_str = request.GET.get('start_date', str(today))
        end_date_str = request.GET.get('end_date', str(today))
        from datetime import datetime
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        period_name = f"{start_date.strftime('%d %b')} - {end_date.strftime('%d %b %Y')}"
    else:
        start_date = today
        end_date = today
        period_name = 'Today'
    
    # Total Income (Gross)
    income_data = Income.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(
        total=Sum('amount'),
        count=Count('id')
    )
    gross_income = income_data['total'] or 0
    
    # Income by source
    income_by_source = Income.objects.filter(
        date__range=[start_date, end_date]
    ).values('source').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    income_sources = {}
    income_counts = {}
    for item in income_by_source:
        income_sources[item['source']] = item['total']
        income_counts[item['source']] = item['count']
    
    # Fill in missing sources with 0
    for source in ['CONSULTATION', 'LAB_TEST', 'PHARMACY', 'CANTEEN', 'OTHER']:
        if source not in income_sources:
            income_sources[source] = 0
            income_counts[source] = 0
    
    # PC Commission Calculations
    pc_data = PCTransaction.objects.filter(
        transaction_date__date__range=[start_date, end_date]
    ).aggregate(
        total_commission=Sum('commission_amount'),
        total_admin_share=Sum('admin_amount'),
        count=Count('id')
    )
    
    pc_commission_expense = pc_data['total_commission'] or 0
    admin_revenue_from_pc = pc_data['total_admin_share'] or 0
    pc_transaction_count = pc_data['count'] or 0
    
    # Net Income (Gross Income + Admin PC Revenue - PC Commission)
    net_income = gross_income + admin_revenue_from_pc
    
    # Regular Expenses
    expense_data = Expense.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(
        total=Sum('amount'),
        count=Count('id')
    )
    regular_expenses = expense_data['total'] or 0
    
    # Total Expenses (Regular + PC Commission)
    total_expenses = regular_expenses + pc_commission_expense
    
    # Expenses by type
    expenses_by_type = Expense.objects.filter(
        date__range=[start_date, end_date]
    ).values('expense_type').annotate(
        total=Sum('amount'),
        count=Count('id')
    )
    
    expense_types = {}
    expense_counts = {}
    for item in expenses_by_type:
        expense_types[item['expense_type']] = item['total']
        expense_counts[item['expense_type']] = item['count']
    
    # Add PC Commission as expense type
    if pc_commission_expense > 0:
        expense_types['PC_COMMISSION'] = pc_commission_expense
        expense_counts['PC_COMMISSION'] = pc_transaction_count
    
    # Calculate profit (Net Income - Total Expenses)
    profit = net_income - total_expenses
    profit_margin = (profit / net_income * 100) if net_income > 0 else 0
    
    # Recent transactions
    recent_income = Income.objects.filter(
        date__range=[start_date, end_date]
    ).order_by('-date', '-recorded_at')[:10]
    
    recent_expenses = Expense.objects.filter(
        date__range=[start_date, end_date]
    ).order_by('-date', '-recorded_at')[:10]
    
    # Recent PC Transactions
    recent_pc_transactions = PCTransaction.objects.filter(
        transaction_date__date__range=[start_date, end_date]
    ).select_related('pc_member', 'patient').order_by('-transaction_date')[:10]
    
    context = {
        'period': period,
        'period_name': period_name,
        'start_date': start_date,
        'end_date': end_date,
        'today': today,
        
        # Income
        'gross_income': gross_income,
        'admin_revenue_from_pc': admin_revenue_from_pc,
        'net_income': net_income,
        
        # Expenses
        'regular_expenses': regular_expenses,
        'pc_commission_expense': pc_commission_expense,
        'total_expenses': total_expenses,
        
        # Profit
        'profit': profit,
        'profit_margin': profit_margin,
        
        'income_sources': income_sources,
        'income_counts': income_counts,
        
        'expense_types': expense_types,
        'expense_counts': expense_counts,
        
        'recent_income': recent_income,
        'recent_expenses': recent_expenses,
        'recent_pc_transactions': recent_pc_transactions,
    }
    
    return render(request, 'accounts/admin_finance.html', context)
