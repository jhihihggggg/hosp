from django.db import models
from django.conf import settings
from patients.models import Patient

class Appointment(models.Model):
    """Appointment/Queue management"""
    
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('called', 'Called'),
        ('in_consultation', 'In Consultation'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    check_in_time = models.DateTimeField(auto_now_add=True)
    called_time = models.DateTimeField(null=True, blank=True)
    started_time = models.DateTimeField(null=True, blank=True)
    completed_time = models.DateTimeField(null=True, blank=True)
    
    # Payment information
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    payment_status = models.CharField(max_length=20, choices=[
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
    ], default='unpaid')
    
    # Appointment type
    appointment_type = models.CharField(max_length=20, choices=[
        ('walk_in', 'Walk-in'),
        ('scheduled', 'Scheduled'),
        ('emergency', 'Emergency'),
    ], default='walk_in')
    
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
        self.status = 'called'
        self.called_time = timezone.now()
        self.save()
    
    def start_consultation(self):
        """Start the consultation"""
        from django.utils import timezone
        self.status = 'in_consultation'
        self.started_time = timezone.now()
        self.save()
    
    def complete(self):
        """Complete the appointment"""
        from django.utils import timezone
        self.status = 'completed'
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
    created_at = models.DateTimeField(auto_now_add=True)
    
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


class DoctorSchedule(models.Model):
    """Doctor's weekly recurring schedule"""
    
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
    max_patients = models.IntegerField(default=20, help_text="Maximum patients for this session")
    consultation_duration = models.IntegerField(default=15, help_text="Minutes per consultation")
    room_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
        unique_together = ['doctor', 'day_of_week', 'start_time']
    
    def __str__(self):
        return f"Dr. {self.doctor.get_full_name()} - {self.day_of_week} {self.start_time}-{self.end_time}"


class DoctorAvailability(models.Model):
    """Doctor's availability for specific dates (overrides schedule)"""
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='availabilities',
        limit_choices_to={'role': 'DOCTOR'}
    )
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True, help_text="False = doctor is unavailable on this date")
    reason = models.CharField(max_length=200, blank=True, help_text="e.g., On leave, Conference")
    max_patients = models.IntegerField(null=True, blank=True)
    room_number = models.CharField(max_length=20, blank=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['doctor', 'date', 'start_time']
        verbose_name_plural = 'Doctor availabilities'
    
    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        return f"Dr. {self.doctor.get_full_name()} - {self.date} ({status})"
