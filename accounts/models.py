from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User model with role-based access"""
    
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('RECEPTIONIST', 'Receptionist'),
        ('LAB', 'Lab Staff'),
        ('PHARMACY', 'Pharmacy Staff'),
        ('CANTEEN', 'Canteen Staff'),
        ('DISPLAY', 'Display Monitor'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='RECEPTIONIST')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, blank=True, help_text="For doctors")
    qualification = models.TextField(blank=True, help_text="Educational qualifications")
    license_number = models.CharField(max_length=50, blank=True, help_text="Professional license")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    @property
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser
    
    @property
    def is_doctor(self):
        return self.role == 'DOCTOR'
    
    @property
    def is_receptionist(self):
        return self.role == 'RECEPTIONIST'
    
    @property
    def is_lab_staff(self):
        return self.role == 'LAB'
    
    @property
    def is_pharmacy_staff(self):
        return self.role == 'PHARMACY'
    
    @property
    def is_canteen_staff(self):
        return self.role == 'CANTEEN'
    
    @property
    def is_nurse(self):
        return self.role == 'NURSE'
    
    @property
    def is_display(self):
        return self.role == 'DISPLAY'
