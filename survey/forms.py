from django import forms
from django.utils import timezone
from .models import FeedbackSurvey, CanteenItem, CanteenSale, Announcement
from patients.models import Patient


class FeedbackForm(forms.ModelForm):
    """Patient feedback and satisfaction survey form"""
    
    class Meta:
        model = FeedbackSurvey
        fields = [
            'patient', 'overall_experience', 'staff_behavior', 'cleanliness',
            'waiting_time', 'facility_quality', 'positive_feedback',
            'negative_feedback', 'suggestions', 'would_recommend'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'overall_experience': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'staff_behavior': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'cleanliness': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'waiting_time': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'facility_quality': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'positive_feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What did you like about our services?'
            }),
            'negative_feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What can we improve?'
            }),
            'suggestions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any suggestions for us?'
            }),
            'would_recommend': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'overall_experience': 'Overall Experience',
            'staff_behavior': 'Staff Behavior',
            'cleanliness': 'Cleanliness',
            'waiting_time': 'Waiting Time',
            'facility_quality': 'Facility Quality',
            'positive_feedback': 'What did you like?',
            'negative_feedback': 'What can we improve?',
            'suggestions': 'Suggestions',
            'would_recommend': 'Would you recommend us to others?',
        }
    
    def clean(self):
        """Validate that at least one rating is provided"""
        cleaned_data = super().clean()
        
        ratings = [
            cleaned_data.get('overall_experience'),
            cleaned_data.get('staff_behavior'),
            cleaned_data.get('cleanliness'),
            cleaned_data.get('waiting_time'),
            cleaned_data.get('facility_quality'),
        ]
        
        if not any(ratings):
            raise forms.ValidationError('Please provide at least one rating.')
        
        return cleaned_data


class CanteenOrderForm(forms.Form):
    """Form for creating canteen orders"""
    
    customer_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Customer name (optional)'
        }),
        label='Customer Name'
    )
    
    payment_method = forms.ChoiceField(
        choices=[
            ('CASH', 'Cash'),
            ('CARD', 'Card'),
            ('MOBILE', 'Mobile Money'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Payment Method',
        initial='CASH'
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Order notes (optional)'
        }),
        label='Notes'
    )


class CanteenItemForm(forms.ModelForm):
    """Form for creating/updating canteen menu items"""
    
    class Meta:
        model = CanteenItem
        fields = [
            'item_code', 'name', 'category', 'description',
            'price', 'cost', 'is_available'
        ]
        widgets = {
            'item_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., CNT001'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item name'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Item description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_item_code(self):
        """Ensure item code is unique"""
        item_code = self.cleaned_data.get('item_code')
        if item_code:
            item_code = item_code.upper()
            # Check if item code exists (exclude current instance if updating)
            qs = CanteenItem.objects.filter(item_code=item_code)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('This item code already exists.')
        return item_code
    
    def clean_price(self):
        """Validate price"""
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Price must be greater than 0.')
        return price
    
    def clean_cost(self):
        """Validate cost"""
        cost = self.cleaned_data.get('cost')
        if cost is not None and cost < 0:
            raise forms.ValidationError('Cost cannot be negative.')
        return cost
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        cost = cleaned_data.get('cost')
        
        # Warn if price is less than cost
        if price and cost and price < cost:
            self.add_error('price',
                forms.ValidationError(
                    'Warning: Selling price is less than cost. This will result in a loss.',
                    code='warning'
                ))
        
        return cleaned_data


class AnnouncementForm(forms.ModelForm):
    """Form for creating announcements"""
    
    class Meta:
        model = Announcement
        fields = [
            'title', 'content', 'priority', 'target_roles',
            'is_active', 'expires_at'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Announcement title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Announcement content'
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'target_roles': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '5'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
    
    def clean_expires_at(self):
        """Validate expiry date is in the future"""
        expires_at = self.cleaned_data.get('expires_at')
        if expires_at and expires_at <= timezone.now():
            raise forms.ValidationError('Expiry date must be in the future.')
        return expires_at


class FeedbackFilterForm(forms.Form):
    """Form for filtering feedback"""
    
    min_rating = forms.ChoiceField(
        required=False,
        choices=[('', 'All Ratings')] + [(i, f'{i} Stars') for i in range(1, 6)],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Minimum Rating'
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='From Date'
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='To Date'
    )
    
    def clean(self):
        """Validate date range"""
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError('From date cannot be after To date.')
        
        return cleaned_data
