from django.db import models
from django.conf import settings
from patients.models import Patient

class CanteenItem(models.Model):
    """Canteen menu items"""
    
    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('BEVERAGE', 'Beverage'),
        ('SNACK', 'Snack'),
        ('OTHER', 'Other'),
    ]
    
    item_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cost = models.DecimalField(max_digits=8, decimal_places=2, help_text="Cost to prepare/buy")
    
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.price}"
    
    @property
    def profit_margin(self):
        return self.price - self.cost


class CanteenSale(models.Model):
    """Canteen sales transaction"""
    
    sale_number = models.CharField(max_length=20, unique=True, editable=False)
    
    sale_date = models.DateTimeField(auto_now_add=True)
    
    # Customer (optional patient link)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='canteen_purchases'
    )
    customer_name = models.CharField(max_length=200, blank=True)
    
    # Payment
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, default='CASH')
    
    served_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='canteen_sales'
    )
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-sale_date']
    
    def __str__(self):
        return f"{self.sale_number} - {self.total_amount}"
    
    def save(self, *args, **kwargs):
        if not self.sale_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_sale = CanteenSale.objects.filter(
                sale_number__startswith=f'CNT{date_str}'
            ).order_by('sale_number').last()
            
            if last_sale:
                last_number = int(last_sale.sale_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.sale_number = f'CNT{date_str}{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    def calculate_total(self):
        """Calculate total amount"""
        self.total_amount = sum(item.total_price for item in self.items.all())
        self.save()


class CanteenSaleItem(models.Model):
    """Items in a canteen sale"""
    
    sale = models.ForeignKey(CanteenSale, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(CanteenItem, on_delete=models.PROTECT)
    
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.item.name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class FeedbackSurvey(models.Model):
    """Patient feedback and satisfaction survey"""
    
    RATING_CHOICES = [
        (1, '⭐ Poor'),
        (2, '⭐⭐ Fair'),
        (3, '⭐⭐⭐ Good'),
        (4, '⭐⭐⭐⭐ Very Good'),
        (5, '⭐⭐⭐⭐⭐ Excellent'),
    ]
    
    survey_number = models.CharField(max_length=20, unique=True, editable=False)
    
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='feedback_surveys'
    )
    
    # Ratings
    overall_experience = models.IntegerField(choices=RATING_CHOICES)
    staff_behavior = models.IntegerField(choices=RATING_CHOICES)
    cleanliness = models.IntegerField(choices=RATING_CHOICES)
    waiting_time = models.IntegerField(choices=RATING_CHOICES)
    facility_quality = models.IntegerField(choices=RATING_CHOICES)
    
    # Comments
    positive_feedback = models.TextField(blank=True, help_text="What did you like?")
    negative_feedback = models.TextField(blank=True, help_text="What can we improve?")
    suggestions = models.TextField(blank=True)
    
    # Would recommend?
    would_recommend = models.BooleanField(null=True)
    
    # Submission
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = "Feedback Surveys"
    
    def __str__(self):
        return f"{self.survey_number} - {self.patient.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.survey_number:
            from django.utils import timezone
            date_str = timezone.now().strftime('%Y%m%d')
            last_survey = FeedbackSurvey.objects.filter(
                survey_number__startswith=f'SUR{date_str}'
            ).order_by('survey_number').last()
            
            if last_survey:
                last_number = int(last_survey.survey_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.survey_number = f'SUR{date_str}{new_number:04d}'
        
        super().save(*args, **kwargs)
    
    @property
    def average_rating(self):
        """Calculate average rating across all categories"""
        ratings = [
            self.overall_experience,
            self.staff_behavior,
            self.cleanliness,
            self.waiting_time,
            self.facility_quality
        ]
        return sum(ratings) / len(ratings)


class Announcement(models.Model):
    """System announcements and notices"""
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    # Target audience
    target_roles = models.JSONField(
        default=list,
        help_text="List of roles to show this announcement to"
    )
    
    is_active = models.BooleanField(default=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.priority})"
    
    @property
    def is_expired(self):
        if not self.expires_at:
            return False
        from django.utils import timezone
        return timezone.now() > self.expires_at
