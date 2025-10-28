from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Max
from .models import Appointment, Prescription, Medicine
from .forms import QuickAppointmentForm
from patients.models import Patient
from accounts.models import User

def public_booking(request):
    """Public appointment booking page (no login required)"""
    if request.method == 'POST':
        form = QuickAppointmentForm(request.POST)
        if form.is_valid():
            try:
                # Get or create patient
                phone = form.cleaned_data['phone']
                patient, created = Patient.objects.get_or_create(
                    phone=phone,
                    defaults={
                        'name': form.cleaned_data['full_name'],
                        'age': form.cleaned_data['age'],
                        'gender': form.cleaned_data['gender'],
                    }
                )
                
                # Update patient info if exists
                if not created:
                    patient.name = form.cleaned_data['full_name']
                    patient.age = form.cleaned_data['age']
                    patient.gender = form.cleaned_data['gender']
                    patient.save()
                
                # Get doctor
                doctor = form.cleaned_data['doctor']
                
                # Get next serial number for today
                today = timezone.now().date()
                last_serial = Appointment.objects.filter(
                    doctor=doctor,
                    appointment_date=today
                ).aggregate(Max('serial_number'))['serial_number__max']
                
                next_serial = (last_serial or 0) + 1
                
                # Generate appointment number
                appointment_number = f"APT-{today.strftime('%Y%m%d')}-{doctor.id}-{next_serial:03d}"
                
                # Create appointment
                appointment = Appointment.objects.create(
                    appointment_number=appointment_number,
                    patient=patient,
                    doctor=doctor,
                    serial_number=next_serial,
                    appointment_date=today,
                    status='WAITING',
                    reason=form.cleaned_data.get('reason', ''),
                    created_by=None  # Public booking
                )
                
                messages.success(
                    request,
                    f'✅ সিরিয়াল নিশ্চিত করা হয়েছে! আপনার সিরিয়াল নম্বর: {next_serial}<br>'
                    f'Appointment confirmed! Your serial number: {next_serial}<br>'
                    f'ডাক্তার: {doctor.get_full_name()}<br>'
                    f'Phone: {phone}'
                )
                
                # Redirect to success or back to form
                return redirect('appointments:public_booking')
                
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'দয়া করে সকল তথ্য সঠিকভাবে পূরণ করুন / Please fill all fields correctly')
    else:
        form = QuickAppointmentForm()
    
    return render(request, 'appointments/public_booking.html', {'form': form})

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
    """Create or edit prescription - Doctors can write prescriptions"""
    from .forms import PrescriptionForm, MedicineFormSet
    from datetime import datetime
    
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    # Check if prescription already exists
    try:
        prescription = Prescription.objects.get(appointment=appointment)
        is_edit = True
    except Prescription.DoesNotExist:
        prescription = None
        is_edit = False
    
    # Only doctor or admin can write prescriptions
    if not (request.user.is_doctor or request.user.is_admin):
        messages.error(request, 'Only doctors can write prescriptions!')
        return redirect('appointments:appointment_detail', pk=appointment_id)
    
    if request.method == 'POST':
        if prescription:
            # Edit existing prescription
            form = PrescriptionForm(request.POST, instance=prescription)
        else:
            # Create new prescription
            form = PrescriptionForm(request.POST)
        
        formset = MedicineFormSet(request.POST, instance=prescription if prescription else None)
        
        if form.is_valid() and formset.is_valid():
            # Save prescription
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.patient = appointment.patient
            prescription.doctor = request.user
            
            # Generate prescription number if new
            if not prescription.prescription_number:
                today = datetime.now()
                prefix = f"RX{today.strftime('%Y%m%d')}"
                last_prescription = Prescription.objects.filter(
                    prescription_number__startswith=prefix
                ).order_by('prescription_number').last()
                
                if last_prescription:
                    last_number = int(last_prescription.prescription_number[-4:])
                    new_number = last_number + 1
                else:
                    new_number = 1
                
                prescription.prescription_number = f"{prefix}{new_number:04d}"
            
            prescription.save()
            
            # Save medicines
            medicines = formset.save(commit=False)
            for medicine in medicines:
                medicine.prescription = prescription
                medicine.save()
            
            # Delete removed medicines
            for obj in formset.deleted_objects:
                obj.delete()
            
            messages.success(request, 'Prescription saved successfully! You can now print it.')
            return redirect('appointments:prescription_detail', pk=prescription.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        if prescription:
            form = PrescriptionForm(instance=prescription)
            formset = MedicineFormSet(instance=prescription)
        else:
            form = PrescriptionForm()
            formset = MedicineFormSet()
    
    # Get previous prescriptions for reference
    previous_prescriptions = Prescription.objects.filter(
        patient=appointment.patient
    ).exclude(pk=prescription.pk if prescription else None).order_by('-created_at')[:5]
    
    context = {
        'appointment': appointment,
        'prescription': prescription,
        'form': form,
        'formset': formset,
        'is_edit': is_edit,
        'previous_prescriptions': previous_prescriptions,
    }
    
    return render(request, 'appointments/prescription_form.html', context)

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
