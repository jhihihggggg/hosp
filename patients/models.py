from django.db import models
from django.conf import settings

class Patient(models.Model):
    """Patient information"""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    # Patient ID will be auto-generated
    patient_id = models.CharField(max_length=20, unique=True, editable=False)
    
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    
    # Contact Information
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)
    emergency_contact_relation = models.CharField(max_length=50)
    
    # Medical Information
    allergies = models.TextField(blank=True, help_text="List of known allergies")
    chronic_conditions = models.TextField(blank=True, help_text="List of chronic conditions")
    
    # Registration
    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='registered_patients'
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-registered_at']
        indexes = [
            models.Index(fields=['patient_id']),
            models.Index(fields=['phone']),
            models.Index(fields=['registered_at']),
        ]
    
    def __str__(self):
        return f"{self.patient_id} - {self.get_full_name()}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.patient_id:
            # Generate patient ID: PAT + year + sequential number
            from django.utils import timezone
            year = timezone.now().year
            last_patient = Patient.objects.filter(
                patient_id__startswith=f'PAT{year}'
            ).order_by('patient_id').last()
            
            if last_patient:
                last_number = int(last_patient.patient_id[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.patient_id = f'PAT{year}{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    @property
    def age(self):
        from django.utils import timezone
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or \
           (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
            age -= 1
        return age


class PatientHistory(models.Model):
    """Medical history record for patients"""
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_history')
    visit_date = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'DOCTOR'}
    )
    
    chief_complaint = models.TextField(help_text="Main reason for visit")
    symptoms = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Vitals
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="°F")
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    pulse_rate = models.IntegerField(null=True, blank=True, help_text="bpm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="cm")
    
    class Meta:
        ordering = ['-visit_date']
        verbose_name_plural = "Patient Histories"
    
    def __str__(self):
        return f"{self.patient.patient_id} - {self.visit_date.strftime('%Y-%m-%d')}"
