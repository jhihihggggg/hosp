from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    """Custom User model with role-based access"""
    
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('RECEPTIONIST', 'Receptionist'),
        ('LAB', 'Lab Staff'),
        ('PHARMACY', 'Pharmacy Staff'),
        ('CANTEEN', 'Canteen Staff'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='RECEPTIONIST')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, blank=True, help_text="For doctors")
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


# PC (Persistent Commission) System Models

class PCMember(models.Model):
    """PC (Persistent Commission) Member - Commission tracking system"""
    
    MEMBER_TYPE_CHOICES = [
        ('GENERAL', 'General Member'),
        ('LIFETIME', 'Lifetime Member'),
        ('INVESTOR', 'Investor Member'),
    ]
    
    # Member information
    pc_code = models.CharField(max_length=20, unique=True, editable=False)
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Commission settings
    commission_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Commission percentage (e.g., 30 for 30%)"
    )
    
    # Totals
    total_commission_earned = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        help_text="Total commission earned (paid amount)"
    )
    due_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Commission amount due (not yet paid)"
    )
    total_referrals = models.IntegerField(
        default=0,
        help_text="Total number of referrals"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_pc_members'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['pc_code']),
            models.Index(fields=['member_type']),
        ]
    
    def __str__(self):
        return f"{self.pc_code} - {self.name} ({self.get_member_type_display()})"
    
    def save(self, *args, **kwargs):
        if not self.pc_code:
            # Generate 5-digit PC code based on member type
            # Format: [Type Digit][4-digit Sequential Number]
            if self.member_type == 'GENERAL':
                prefix = '1'
                last_member = PCMember.objects.filter(
                    pc_code__startswith='1'
                ).order_by('pc_code').last()
            elif self.member_type == 'LIFETIME':
                prefix = '2'
                last_member = PCMember.objects.filter(
                    pc_code__startswith='2'
                ).order_by('pc_code').last()
            elif self.member_type == 'INVESTOR':
                prefix = '3'
                last_member = PCMember.objects.filter(
                    pc_code__startswith='3'
                ).order_by('pc_code').last()
            else:
                prefix = '9'
                last_member = None
            
            if last_member:
                last_number = int(last_member.pc_code[1:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            # 5-digit code: 1 digit prefix + 4 digit number (e.g., 10001, 20001, 30001)
            self.pc_code = f"{prefix}{new_number:04d}"
        
        super().save(*args, **kwargs)
    
    @property
    def color_code(self):
        """Return color code for frontend display"""
        if self.member_type == 'GENERAL':
            return 'white'
        elif self.member_type == 'LIFETIME':
            return 'blue'
        elif self.member_type == 'INVESTOR':
            return 'green'
        return 'gray'


class PCTransaction(models.Model):
    """PC Commission Transaction - Track each commission"""
    
    transaction_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # PC Member
    pc_member = models.ForeignKey(
        PCMember,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    
    # Patient/Appointment reference
    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    appointment = models.ForeignKey(
        'appointments.Appointment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Transaction details
    transaction_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total appointment/service amount"
    )
    commission_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Commission percentage applied"
    )
    commission_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Commission amount (percentage of total)"
    )
    admin_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount going to admin (remaining after commission)"
    )
    
    # Recorded by
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='pc_transactions_recorded'
    )
    
    # Payment status
    is_paid_to_member = models.BooleanField(
        default=False,
        help_text="Has commission been paid to PC member?"
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-transaction_date']
        indexes = [
            models.Index(fields=['transaction_date']),
            models.Index(fields=['pc_member', 'transaction_date']),
        ]
    
    def __str__(self):
        return f"{self.transaction_number} - {self.pc_member.pc_code} - ৳{self.commission_amount}"
    
    def save(self, *args, **kwargs):
        if not self.transaction_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_txn = PCTransaction.objects.filter(
                transaction_number__startswith=f'PC{date_str}'
            ).order_by('transaction_number').last()
            
            if last_txn:
                last_number = int(last_txn.transaction_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.transaction_number = f'PC{date_str}{new_number:04d}'
        
        # Calculate commission and admin amounts
        self.commission_amount = (self.total_amount * self.commission_percentage) / 100
        self.admin_amount = self.total_amount - self.commission_amount
        
        is_new = self.pk is None
        
        super().save(*args, **kwargs)
        
        # Update PC member totals (only for new transactions)
        if is_new:
            self.pc_member.due_amount += self.commission_amount
            self.pc_member.total_referrals += 1
            self.pc_member.save()

