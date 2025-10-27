from django.db import models
from django.conf import settings
from django.utils import timezone
from patients.models import Patient


class DoctorSchedule(models.Model):
    """Regular weekly schedule for doctors"""
    
    DAY_CHOICES = [
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    ]
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='schedules',
        limit_choices_to={'role': 'DOCTOR'}
    )
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_patients = models.IntegerField(default=20, help_text="Maximum patients per session")
    consultation_duration = models.IntegerField(default=15, help_text="Minutes per patient")
    is_active = models.BooleanField(default=True)
    room_number = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
        unique_together = ['doctor', 'day_of_week', 'start_time']
    
    def __str__(self):
        return f"Dr. {self.doctor.get_full_name()} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"
    
    def get_available_slots(self, date):
        """Get available appointment slots for a specific date"""
        from datetime import datetime, timedelta
        
        slots = []
        current_time = datetime.combine(date, self.start_time)
        end_time = datetime.combine(date, self.end_time)
        
        while current_time < end_time:
            # Check if slot is already booked
            booked = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=date,
                appointment_time=current_time.time(),
                status__in=['WAITING', 'CALLED', 'IN_PROGRESS']
            ).exists()
            
            slots.append({
                'time': current_time.time(),
                'available': not booked
            })
            
            current_time += timedelta(minutes=self.consultation_duration)
        
        return slots


class DoctorAvailability(models.Model):
    """Specific date availability/unavailability for doctors"""
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='availabilities',
        limit_choices_to={'role': 'DOCTOR'}
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_patients = models.IntegerField(default=20)
    is_available = models.BooleanField(default=True)
    reason = models.CharField(max_length=200, blank=True, help_text="Reason if unavailable")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['doctor', 'date', 'start_time']
        verbose_name_plural = 'Doctor Availabilities'
    
    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        return f"Dr. {self.doctor.get_full_name()} - {self.date} ({status})"


class Appointment(models.Model):
    """Appointment/Queue management"""
    
    STATUS_CHOICES = [
        ('WAITING', 'Waiting'),
        ('CALLED', 'Called'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    ]
    
    # Appointment details
    appointment_number = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_appointments',
        limit_choices_to={'role': 'DOCTOR'}
    )
    
    # Serial/Queue information
    serial_number = models.IntegerField(help_text="Queue serial number for the day")
    appointment_date = models.DateField()
    appointment_time = models.TimeField(null=True, blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='WAITING')
    check_in_time = models.DateTimeField(default=timezone.now)
    called_time = models.DateTimeField(null=True, blank=True)
    started_time = models.DateTimeField(null=True, blank=True)
    completed_time = models.DateTimeField(null=True, blank=True)
    
    # Additional information
    reason = models.TextField(blank=True, help_text="Reason for visit")
    notes = models.TextField(blank=True)
    
    # Created by
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_appointments'
    )
    
    # Room/Chamber info
    room_number = models.CharField(max_length=20, blank=True)
    
    class Meta:
        ordering = ['appointment_date', 'serial_number']
        unique_together = ['doctor', 'appointment_date', 'serial_number']
        indexes = [
            models.Index(fields=['appointment_date', 'doctor', 'status']),
            models.Index(fields=['appointment_number']),
        ]
    
    def __str__(self):
        return f"{self.appointment_number} - {self.patient.get_full_name()} (Serial: {self.serial_number})"
    
    def save(self, *args, **kwargs):
        if not self.appointment_number:
            # Generate appointment number: APT + date + sequential
            from django.utils import timezone
            date_str = self.appointment_date.strftime('%Y%m%d')
            last_apt = Appointment.objects.filter(
                appointment_number__startswith=f'APT{date_str}'
            ).order_by('appointment_number').last()
            
            if last_apt:
                last_number = int(last_apt.appointment_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.appointment_number = f'APT{date_str}{new_number:04d}'
        
        # Auto-assign serial number if not set
        if not self.serial_number:
            last_serial = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date
            ).aggregate(models.Max('serial_number'))['serial_number__max']
            
            self.serial_number = (last_serial or 0) + 1
        
        super().save(*args, **kwargs)
    
    def call_next(self):
        """Mark this appointment as called"""
        from django.utils import timezone
        self.status = 'CALLED'
        self.called_time = timezone.now()
        self.save()
    
    def start_consultation(self):
        """Start the consultation"""
        from django.utils import timezone
        self.status = 'IN_PROGRESS'
        self.started_time = timezone.now()
        self.save()
    
    def complete(self):
        """Complete the appointment"""
        from django.utils import timezone
        self.status = 'COMPLETED'
        self.completed_time = timezone.now()
        self.save()


class Prescription(models.Model):
    """Doctor's prescription for patient"""
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='prescriptions_written'
    )
    
    # Prescription details
    prescription_number = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Clinical information
    diagnosis = models.TextField()
    chief_complaint = models.TextField(blank=True)
    
    # Advice and follow-up
    advice = models.TextField(blank=True, help_text="Doctor's advice to patient")
    follow_up_date = models.DateField(null=True, blank=True)
    
    # Status
    is_printed = models.BooleanField(default=False)
    printed_at = models.DateTimeField(null=True, blank=True)
    printed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='printed_prescriptions'
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.prescription_number} - {self.patient.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.prescription_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_rx = Prescription.objects.filter(
                prescription_number__startswith=f'RX{date_str}'
            ).order_by('prescription_number').last()
            
            if last_rx:
                last_number = int(last_rx.prescription_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.prescription_number = f'RX{date_str}{new_number:04d}'
        
        super().save(*args, **kwargs)


class Medicine(models.Model):
    """Medicine prescribed in a prescription"""
    
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    
    medicine_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100, help_text="e.g., 500mg")
    frequency = models.CharField(max_length=100, help_text="e.g., 1+0+1 (morning, noon, night)")
    duration = models.CharField(max_length=100, help_text="e.g., 7 days")
    instructions = models.TextField(blank=True, help_text="e.g., After meal")
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.medicine_name} - {self.dosage}"
