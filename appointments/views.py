from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment, Prescription, Medicine

@login_required
def appointment_list(request):
    """List all appointments"""
    appointments = Appointment.objects.all().select_related('patient', 'doctor').order_by('-appointment_date', 'serial_number')
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def appointment_create(request):
    """Create new appointment"""
    if request.method == 'POST':
        # TODO: Implement form handling
        messages.success(request, 'Appointment created successfully!')
        return redirect('appointments:appointment_list')
    return render(request, 'appointments/appointment_create.html')

@login_required
def appointment_detail(request, pk):
    """View appointment details"""
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/appointment_detail.html', {'appointment': appointment})

@login_required
def call_patient(request, pk):
    """Call next patient"""
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.call_next()
    messages.success(request, f'Patient {appointment.serial_number} called!')
    return redirect('appointments:queue_display')

@login_required
def complete_appointment(request, pk):
    """Complete appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.complete()
    messages.success(request, 'Appointment completed!')
    return redirect('appointments:appointment_list')

@login_required
def queue_display(request):
    """Display patient queue"""
    from django.utils import timezone
    today = timezone.now().date()
    
    appointments = Appointment.objects.filter(
        appointment_date=today,
        status__in=['WAITING', 'CALLED', 'IN_PROGRESS']
    ).select_related('patient', 'doctor').order_by('serial_number')
    
    return render(request, 'appointments/queue_display.html', {'appointments': appointments})

@login_required
def display_monitor(request):
    """Public display monitor"""
    return render(request, 'appointments/display_monitor.html')

@login_required
def prescription_create(request, appointment_id):
    """Create prescription"""
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        # TODO: Implement form handling
        messages.success(request, 'Prescription created successfully!')
        return redirect('appointments:appointment_detail', pk=appointment_id)
    return render(request, 'appointments/prescription_create.html', {'appointment': appointment})

@login_required
def prescription_detail(request, pk):
    """View prescription"""
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'appointments/prescription_detail.html', {'prescription': prescription})

@login_required
def prescription_print(request, pk):
    """Print prescription"""
    prescription = get_object_or_404(Prescription, pk=pk)
    return render(request, 'appointments/prescription_print.html', {'prescription': prescription})
