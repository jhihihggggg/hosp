from django.db import models
from django.conf import settings

class Department(models.Model):
    """Departments in the diagnostic center"""
    
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    head = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='departments_headed'
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class IncomeCategory(models.Model):
    """Categories for income tracking"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Income Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Income(models.Model):
    """Income/Revenue tracking"""
    
    SOURCE_CHOICES = [
        ('CONSULTATION', 'Consultation Fee'),
        ('LAB_TEST', 'Lab Test'),
        ('PHARMACY', 'Pharmacy Sales'),
        ('CANTEEN', 'Canteen'),
        ('OTHER', 'Other'),
    ]
    
    income_number = models.CharField(max_length=20, unique=True, editable=False)
    
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
    
    # Reference to related transaction
    reference_number = models.CharField(max_length=50, blank=True, help_text="Invoice/Receipt number")
    
    # Payment details
    payment_method = models.CharField(max_length=50, blank=True)
    
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-recorded_at']
    
    def __str__(self):
        return f"{self.income_number} - {self.source} - {self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.income_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_income = Income.objects.filter(
                income_number__startswith=f'INC{date_str}'
            ).order_by('income_number').last()
            
            if last_income:
                last_number = int(last_income.income_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.income_number = f'INC{date_str}{new_number:04d}'
        
        super().save(*args, **kwargs)


class ExpenseCategory(models.Model):
    """Categories for expense tracking"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Expense Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Expense(models.Model):
    """Expense tracking"""
    
    EXPENSE_TYPE_CHOICES = [
        ('SALARY', 'Salary'),
        ('RENT', 'Rent'),
        ('UTILITIES', 'Utilities'),
        ('EQUIPMENT', 'Equipment'),
        ('SUPPLIES', 'Supplies'),
        ('MAINTENANCE', 'Maintenance'),
        ('MARKETING', 'Marketing'),
        ('OTHER', 'Other'),
    ]
    
    expense_number = models.CharField(max_length=20, unique=True, editable=False)
    
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPE_CHOICES)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    
    # Payment details
    vendor = models.CharField(max_length=200, blank=True)
    invoice_number = models.CharField(max_length=50, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    
    # Approval
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_expenses'
    )
    is_approved = models.BooleanField(default=False)
    
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recorded_expenses'
    )
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    # Attachments
    receipt = models.FileField(upload_to='expense_receipts/', null=True, blank=True)
    
    class Meta:
        ordering = ['-date', '-recorded_at']
    
    def __str__(self):
        return f"{self.expense_number} - {self.expense_type} - {self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.expense_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_expense = Expense.objects.filter(
                expense_number__startswith=f'EXP{date_str}'
            ).order_by('expense_number').last()
            
            if last_expense:
                last_number = int(last_expense.expense_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.expense_number = f'EXP{date_str}{new_number:04d}'
        
        super().save(*args, **kwargs)


class Investor(models.Model):
    """Investor/Partner information"""
    
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    
    share_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Percentage share in profits"
    )
    investment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    investment_date = models.DateField()
    
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-share_percentage']
    
    def __str__(self):
        return f"{self.name} ({self.share_percentage}%)"


class InvestorPayout(models.Model):
    """Profit distribution to investors"""
    
    payout_number = models.CharField(max_length=20, unique=True, editable=False)
    
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='payouts')
    
    period_start = models.DateField()
    period_end = models.DateField()
    
    total_profit = models.DecimalField(max_digits=12, decimal_places=2, help_text="Total profit for period")
    share_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Investor's share")
    
    payout_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    
    notes = models.TextField(blank=True)
    
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    processed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-payout_date']
    
    def __str__(self):
        return f"{self.payout_number} - {self.investor.name} - {self.share_amount}"
    
    def save(self, *args, **kwargs):
        if not self.payout_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_payout = InvestorPayout.objects.filter(
                payout_number__startswith=f'PAY{date_str}'
            ).order_by('payout_number').last()
            
            if last_payout:
                last_number = int(last_payout.payout_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.payout_number = f'PAY{date_str}{new_number:04d}'
        
        super().save(*args, **kwargs)


class ConsultationFee(models.Model):
    """Consultation fee structure for doctors"""
    
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consultation_fees',
        limit_choices_to={'role': 'DOCTOR'}
    )
    
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    effective_from = models.DateField()
    effective_until = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-effective_from']
        verbose_name_plural = "Consultation Fees"
    
    def __str__(self):
        return f"{self.doctor.get_full_name()} - {self.fee_amount}"
