from django.db import models
from django.conf import settings
from patients.models import Patient
from appointments.models import Appointment

class LabTest(models.Model):
    """Available lab tests"""
    
    CATEGORY_CHOICES = [
        ('BLOOD', 'Blood Test'),
        ('URINE', 'Urine Test'),
        ('STOOL', 'Stool Test'),
        ('IMAGING', 'Imaging'),
        ('BIOCHEMISTRY', 'Biochemistry'),
        ('MICROBIOLOGY', 'Microbiology'),
        ('PATHOLOGY', 'Pathology'),
        ('OTHER', 'Other'),
    ]
    
    test_code = models.CharField(max_length=20, unique=True)
    test_name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Sample requirements
    sample_type = models.CharField(max_length=100, help_text="e.g., Blood, Urine")
    sample_volume = models.CharField(max_length=50, blank=True, help_text="Required volume")
    preparation_instructions = models.TextField(blank=True, help_text="e.g., Fasting required")
    
    # Turnaround time
    turnaround_time = models.CharField(max_length=50, help_text="e.g., 24 hours, Same day")
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['test_name']
    
    def __str__(self):
        return f"{self.test_code} - {self.test_name}"


class LabOrder(models.Model):
    """Lab test order from doctor"""
    
    STATUS_CHOICES = [
        ('ORDERED', 'Ordered'),
        ('SAMPLE_COLLECTED', 'Sample Collected'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_orders')
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lab_orders'
    )
    
    # Ordering doctor
    ordered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ordered_lab_tests'
    )
    ordered_at = models.DateTimeField(auto_now_add=True)
    
    # Tests ordered
    tests = models.ManyToManyField(LabTest, related_name='orders')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ORDERED')
    
    # Sample collection
    sample_collected_at = models.DateTimeField(null=True, blank=True)
    sample_collected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='collected_samples'
    )
    
    # Clinical notes
    clinical_notes = models.TextField(blank=True, help_text="Clinical information from doctor")
    priority = models.BooleanField(default=False, help_text="Mark as urgent")
    
    # Billing
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-ordered_at']
    
    def __str__(self):
        return f"{self.order_number} - {self.patient.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_order = LabOrder.objects.filter(
                order_number__startswith=f'LAB{date_str}'
            ).order_by('order_number').last()
            
            if last_order:
                last_number = int(last_order.order_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.order_number = f'LAB{date_str}{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    def calculate_total(self):
        """Calculate total cost of all tests"""
        total = sum(test.price for test in self.tests.all())
        self.total_amount = total
        self.save()
        return total


class LabResult(models.Model):
    """Lab test result"""
    
    order = models.ForeignKey(LabOrder, on_delete=models.CASCADE, related_name='results')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    
    # Results
    result_data = models.JSONField(
        help_text="Store test parameters and values as JSON",
        default=dict
    )
    interpretation = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Verification
    tested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='performed_tests'
    )
    tested_at = models.DateTimeField(auto_now_add=True)
    
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_results'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    # Report
    report_file = models.FileField(upload_to='lab_reports/', null=True, blank=True)
    is_printed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-tested_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.test.test_name}"
    
    def verify(self, user):
        """Verify the test result"""
        from django.utils import timezone
        self.is_verified = True
        self.verified_by = user
        self.verified_at = timezone.now()
        self.save()
