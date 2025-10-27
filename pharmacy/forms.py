from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Drug, DrugCategory


class DrugForm(forms.ModelForm):
    """Form for creating/updating drugs"""
    
    class Meta:
        model = Drug
        fields = [
            'drug_code', 'generic_name', 'brand_name', 'category', 'form', 'strength',
            'manufacturer', 'quantity_in_stock', 'reorder_level', 'unit_price',
            'selling_price', 'manufacture_date', 'expiry_date', 'description',
            'side_effects', 'storage_instructions'
        ]
        widgets = {
            'drug_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., DRG001'}),
            'generic_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Generic name'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand name'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'form': forms.Select(attrs={'class': 'form-select'}),
            'strength': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manufacturer'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'manufacture_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'side_effects': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'storage_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def clean_drug_code(self):
        """Ensure drug code is unique"""
        drug_code = self.cleaned_data.get('drug_code')
        if drug_code:
            drug_code = drug_code.upper()
            # Check if drug code exists (exclude current instance if updating)
            qs = Drug.objects.filter(drug_code=drug_code)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('This drug code already exists.')
        return drug_code
    
    def clean_quantity_in_stock(self):
        """Ensure quantity is not negative"""
        quantity = self.cleaned_data.get('quantity_in_stock')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError('Quantity cannot be negative.')
        return quantity
    
    def clean_unit_price(self):
        """Validate unit price"""
        price = self.cleaned_data.get('unit_price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Unit price must be greater than 0.')
        return price
    
    def clean_selling_price(self):
        """Validate selling price"""
        price = self.cleaned_data.get('selling_price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Selling price must be greater than 0.')
        return price
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        manufacture_date = cleaned_data.get('manufacture_date')
        expiry_date = cleaned_data.get('expiry_date')
        unit_price = cleaned_data.get('unit_price')
        selling_price = cleaned_data.get('selling_price')
        
        # Check manufacture date is before expiry date
        if manufacture_date and expiry_date:
            if manufacture_date >= expiry_date:
                raise forms.ValidationError('Manufacture date must be before expiry date.')
        
        # Check expiry date is not in the past (with grace period for existing drugs)
        if expiry_date and not self.instance.pk:  # Only for new drugs
            today = timezone.now().date()
            if expiry_date < today:
                raise forms.ValidationError('Expiry date cannot be in the past.')
            
            # Warn if expiry is less than 6 months away
            six_months_later = today + timedelta(days=180)
            if expiry_date < six_months_later:
                self.add_error('expiry_date', 
                    forms.ValidationError('Warning: This drug expires in less than 6 months.', code='warning'))
        
        # Warn if selling price is less than unit price
        if unit_price and selling_price:
            if selling_price < unit_price:
                self.add_error('selling_price',
                    forms.ValidationError('Warning: Selling price is less than unit price. This will result in a loss.', code='warning'))
        
        return cleaned_data


class StockAdjustmentForm(forms.Form):
    """Form for adjusting drug stock"""
    
    ADJUSTMENT_TYPE_CHOICES = [
        ('add', 'Add Stock'),
        ('reduce', 'Reduce Stock'),
        ('set', 'Set Stock'),
    ]
    
    adjust_type = forms.ChoiceField(
        choices=ADJUSTMENT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Adjustment Type'
    )
    quantity = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        label='Quantity'
    )
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for adjustment'}),
        label='Reason',
        required=True
    )
    
    def clean_quantity(self):
        """Ensure quantity is positive"""
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError('Quantity must be a positive number.')
        return quantity


class PrescriptionProcessForm(forms.Form):
    """Form for processing prescriptions"""
    
    medicine_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    quantity_dispensed = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        label='Quantity Dispensed'
    )
    dosage_instructions = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label='Dosage Instructions',
        required=False
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label='Pharmacist Notes',
        required=False
    )


class DrugSearchForm(forms.Form):
    """Form for searching drugs"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, code, or generic name...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=DrugCategory.objects.all(),
        required=False,
        empty_label='All Categories',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    stock_status = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All'),
            ('in_stock', 'In Stock'),
            ('low_stock', 'Low Stock'),
            ('out_of_stock', 'Out of Stock'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class SaleForm(forms.Form):
    """Form for creating pharmacy sales"""
    
    customer_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer name (optional)'})
    )
    customer_phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number (optional)'})
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('CASH', 'Cash'),
            ('CARD', 'Card'),
            ('MOBILE', 'Mobile Money'),
            ('INSURANCE', 'Insurance'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Payment Method'
    )
    discount_percentage = forms.DecimalField(
        required=False,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        label='Discount %',
        initial=0
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        label='Notes'
    )
