from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Appointment, Prescription, Medicine, DoctorSchedule, DoctorAvailability
from .forms import QuickAppointmentForm, DoctorScheduleForm, DoctorAvailabilityForm
from accounts.models import User
from datetime import datetime, timedelta, date
import calendar


def get_doctor_available_dates(request, doctor_id):
    """API endpoint to get available dates for a doctor"""
    try:
        doctor = User.objects.get(id=doctor_id, role='DOCTOR')
        
        # Get next 30 days
        available_dates = []
        today = date.today()
        
        for i in range(30):
            check_date = today + timedelta(days=i)
            day_name = check_date.strftime('%A').upper()
            
            # Check if doctor has schedule for this day
            schedules = DoctorSchedule.objects.filter(
                doctor=doctor,
                day_of_week=day_name,
                is_active=True
            )
            
            # Check specific availability/unavailability
            availability = DoctorAvailability.objects.filter(
                doctor=doctor,
                date=check_date
            ).first()
            
            if availability:
                if availability.is_available:
                    available_dates.append({
                        'date': check_date.isoformat(),
                        'day': check_date.strftime('%A'),
                        'slots_available': True
                    })
            elif schedules.exists():
                # Check if not fully booked
                total_appointments = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=check_date,
                    status__in=['WAITING', 'CALLED', 'IN_PROGRESS']
                ).count()
                
                max_patients = schedules.first().max_patients
                
                if total_appointments < max_patients:
                    available_dates.append({
                        'date': check_date.isoformat(),
                        'day': check_date.strftime('%A'),
                        'slots_available': True,
                        'remaining': max_patients - total_appointments
                    })
        
        return JsonResponse({'dates': available_dates})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def get_doctor_time_slots(request, doctor_id, date_str):
    """API endpoint to get available time slots for a doctor on a specific date"""
    try:
        doctor = User.objects.get(id=doctor_id, role='DOCTOR')
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_name = appointment_date.strftime('%A').upper()
        
        # Get schedule for this day
        schedule = DoctorSchedule.objects.filter(
            doctor=doctor,
            day_of_week=day_name,
            is_active=True
        ).first()
        
        if not schedule:
            return JsonResponse({'slots': []})
        
        # Generate time slots
        slots = []
        current_time = datetime.combine(appointment_date, schedule.start_time)
        end_time = datetime.combine(appointment_date, schedule.end_time)
        
        while current_time < end_time:
            slot_time = current_time.time()
            
            # Check if this slot is already booked
            is_booked = Appointment.objects.filter(
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=slot_time,
                status__in=['WAITING', 'CALLED', 'IN_PROGRESS']
            ).exists()
            
            slots.append({
                'time': slot_time.strftime('%H:%M'),
                'display': slot_time.strftime('%I:%M %p'),
                'available': not is_booked
            })
            
            current_time += timedelta(minutes=schedule.consultation_duration)
        
        return JsonResponse({'slots': slots, 'room': schedule.room_number})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def doctor_schedule_list(request):
    """List all doctor schedules"""
    schedules = DoctorSchedule.objects.select_related('doctor').all()
    return render(request, 'appointments/doctor_schedule_list.html', {'schedules': schedules})


@login_required
def doctor_schedule_create(request):
    """Create new doctor schedule"""
    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor schedule created successfully!')
            return redirect('appointments:doctor_schedule_list')
    else:
        form = DoctorScheduleForm()
    
    return render(request, 'appointments/doctor_schedule_form.html', {'form': form, 'title': 'Add Doctor Schedule'})


@login_required
def doctor_schedule_edit(request, pk):
    """Edit doctor schedule"""
    schedule = get_object_or_404(DoctorSchedule, pk=pk)
    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor schedule updated successfully!')
            return redirect('appointments:doctor_schedule_list')
    else:
        form = DoctorScheduleForm(instance=schedule)
    
    return render(request, 'appointments/doctor_schedule_form.html', {'form': form, 'title': 'Edit Schedule', 'schedule': schedule})


@login_required
def doctor_schedule_delete(request, pk):
    """Delete doctor schedule"""
    schedule = get_object_or_404(DoctorSchedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Schedule deleted successfully!')
        return redirect('appointments:doctor_schedule_list')
    
    return render(request, 'appointments/doctor_schedule_confirm_delete.html', {'schedule': schedule})


def public_booking(request):
    """Public-facing appointment booking page (no login required)"""
    if request.method == 'POST':
        form = QuickAppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment, patient = form.save(created_by=None)
                messages.success(
                    request, 
                    f'Appointment booked successfully! Your serial number is {appointment.serial_number} for Dr. {appointment.doctor.get_full_name()}'
                )
                return render(request, 'appointments/booking_success.html', {
                    'appointment': appointment,
                    'patient': patient
                })
            except Exception as e:
                messages.error(request, f'Error booking appointment: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuickAppointmentForm()
    
    # Get list of doctors for display
    doctors = User.objects.filter(role='DOCTOR', is_active=True).order_by('first_name')
    
    return render(request, 'appointments/public_booking.html', {
        'form': form,
        'doctors': doctors
    })


@login_required
def receptionist_booking(request):
    """Receptionist interface for booking appointments for walk-in patients"""
    if request.method == 'POST':
        form = QuickAppointmentForm(request.POST)
        if form.is_valid():
            try:
                appointment, patient = form.save(created_by=request.user)
                messages.success(
                    request, 
                    f'Serial {appointment.serial_number} assigned for {patient.get_full_name()} with Dr. {appointment.doctor.get_full_name()}'
                )
                return redirect('appointments:receptionist_booking')
            except Exception as e:
                messages.error(request, f'Error creating appointment: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = QuickAppointmentForm()
    
    # Get today's appointments
    from django.utils import timezone
    today = timezone.now().date()
    appointments = Appointment.objects.filter(
        appointment_date=today
    ).select_related('patient', 'doctor').order_by('doctor', 'serial_number')
    
    # Group appointments by doctor
    appointments_by_doctor = {}
    for apt in appointments:
        doctor_name = apt.doctor.get_full_name()
        if doctor_name not in appointments_by_doctor:
            appointments_by_doctor[doctor_name] = []
        appointments_by_doctor[doctor_name].append(apt)
    
    return render(request, 'appointments/receptionist_booking.html', {
        'form': form,
        'appointments_by_doctor': appointments_by_doctor,
        'today': today
    })


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
    """Call next patient with audio announcement support - broadcasts to ALL display monitors"""
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.call_next()
    
    # Get room number from doctor's schedule or appointment
    room_number = 'Consultation Room'
    if hasattr(appointment, 'room_number') and appointment.room_number:
        room_number = appointment.room_number
    else:
        # Try to get from doctor's schedule
        today_day = appointment.appointment_date.strftime('%A').upper()
        doctor_schedule = DoctorSchedule.objects.filter(
            doctor=appointment.doctor,
            day_of_week=today_day,
            is_active=True
        ).first()
        if doctor_schedule and doctor_schedule.room_number:
            room_number = doctor_schedule.room_number
    
    # Broadcast to ALL display monitors via WebSocket
    # This reaches every display monitor in the hospital
    channel_layer = get_channel_layer()
    if channel_layer:
        try:
            async_to_sync(channel_layer.group_send)(
                'display_monitor',  # ALL displays receive this
                {
                    'type': 'patient_called',
                    'patient_name': appointment.patient.get_full_name(),
                    'serial_number': appointment.serial_number,
                    'queue_number': appointment.serial_number,
                    'doctor_name': appointment.doctor.get_full_name(),
                    'doctor_id': appointment.doctor.id,
                    'room_number': room_number,
                    'appointment_id': appointment.id,
                }
            )
            print(f"✅ Broadcast to ALL displays - Dr. {appointment.doctor.get_full_name()} calling {appointment.patient.get_full_name()}")
        except Exception as e:
            print(f"❌ Error broadcasting to display: {e}")
    
    # If AJAX request, return JSON with patient name for audio
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'patient_name': appointment.patient.get_full_name(),
            'serial_number': appointment.serial_number,
            'message': f'Serial {appointment.serial_number} - {appointment.patient.get_full_name()} has been called'
        })
    
    messages.success(request, f'Patient {appointment.patient.get_full_name()} (Serial {appointment.serial_number}) called!')
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
    """Public display monitor - shows patient name and plays audio when doctor calls"""
    # This view is for dedicated display devices logged in with DISPLAY role
    if not request.user.is_display and not request.user.is_admin:
        messages.error(request, 'Access denied. This page is for display monitors only.')
        return redirect('accounts:dashboard')
    
    return render(request, 'appointments/display_monitor.html')

@login_required
def prescription_create(request, appointment_id):
    """Create prescription with medicines"""
    from .forms import PrescriptionForm, MedicineFormSet
    
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Check if user is the doctor for this appointment or admin
    if not (request.user == appointment.doctor or request.user.is_admin):
        messages.error(request, 'You do not have permission to write prescription for this appointment.')
        return redirect('appointments:appointment_detail', pk=appointment_id)
    
    # Check if prescription already exists
    existing_prescription = Prescription.objects.filter(appointment=appointment).first()
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=existing_prescription)
        medicine_formset = MedicineFormSet(request.POST, instance=existing_prescription or form.instance)
        
        if form.is_valid() and medicine_formset.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()
            
            # Save medicines
            medicines = medicine_formset.save(commit=False)
            for medicine in medicines:
                medicine.prescription = prescription
                medicine.save()
            
            # Handle deleted medicines
            for obj in medicine_formset.deleted_objects:
                obj.delete()
            
            messages.success(request, 'Prescription saved successfully!')
            
            # Check if print was requested
            if request.POST.get('print'):
                return redirect('appointments:prescription_print', pk=prescription.pk)
            
            return redirect('appointments:appointment_detail', pk=appointment_id)
    else:
        form = PrescriptionForm(instance=existing_prescription)
        medicine_formset = MedicineFormSet(instance=existing_prescription)
    
    # Get previous prescriptions for this patient
    previous_prescriptions = Prescription.objects.filter(
        appointment__patient=appointment.patient
    ).exclude(
        id=existing_prescription.id if existing_prescription else None
    ).order_by('-created_at')[:5]
    
    return render(request, 'appointments/prescription_form.html', {
        'form': form,
        'medicine_formset': medicine_formset,
        'appointment': appointment,
        'previous_prescriptions': previous_prescriptions
    })

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
