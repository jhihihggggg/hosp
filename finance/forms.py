from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Income, Expense, IncomeCategory, ExpenseCategory, Department


class IncomeForm(forms.ModelForm):
    """Form for creating/editing income records"""
    
    class Meta:
        model = Income
        fields = [
            'source', 'category', 'department', 'amount', 'date',
            'description', 'reference_number', 'payment_method'
        ]
        widgets = {
            'source': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'department': forms.Select(attrs={
                'class': 'form-select',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'required': True
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter details about this income...'
            }),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Invoice/Receipt number'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select',
            }, choices=[
                ('', 'Select payment method'),
                ('CASH', 'Cash'),
                ('CARD', 'Card'),
                ('MOBILE', 'Mobile Banking'),
                ('BANK', 'Bank Transfer'),
            ]),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise ValidationError('Amount must be greater than zero.')
        return amount
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise ValidationError('Income date cannot be in the future.')
        return date


class ExpenseForm(forms.ModelForm):
    """Form for creating/editing expense records"""
    
    class Meta:
        model = Expense
        fields = [
            'expense_type', 'category', 'department', 'amount', 'date',
            'description', 'vendor', 'invoice_number', 'payment_method', 'receipt'
        ]
        widgets = {
            'expense_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'department': forms.Select(attrs={
                'class': 'form-select',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'required': True
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the expense...',
                'required': True
            }),
            'vendor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Vendor/Payee name'
            }),
            'invoice_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Invoice/Bill number'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select',
            }, choices=[
                ('', 'Select payment method'),
                ('CASH', 'Cash'),
                ('CARD', 'Card'),
                ('BANK', 'Bank Transfer'),
                ('CHECK', 'Cheque'),
            ]),
            'receipt': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf'
            }),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise ValidationError('Amount must be greater than zero.')
        if amount and amount > 1000000:  # Safety limit
            raise ValidationError('Amount seems unusually large. Please verify.')
        return amount
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise ValidationError('Expense date cannot be in the future.')
        return date


class InvoiceForm(forms.Form):
    """Form for creating invoices"""
    
    invoice_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'required': True
        })
    )
    
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        })
    )
    
    customer_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Customer name',
            'required': True
        })
    )
    
    customer_phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone number'
        })
    )
    
    customer_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    
    customer_address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Customer address'
        })
    )
    
    subtotal = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'readonly': True
        })
    )
    
    discount = forms.DecimalField(
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'value': '0'
        })
    )
    
    tax = forms.DecimalField(
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'value': '0'
        })
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Additional notes or terms...'
        })
    )
    
    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        subtotal = self.cleaned_data.get('subtotal', 0)
        if discount and discount > subtotal:
            raise ValidationError('Discount cannot be greater than subtotal.')
        return discount
    
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        invoice_date = self.cleaned_data.get('invoice_date')
        if due_date and invoice_date and due_date < invoice_date:
            raise ValidationError('Due date cannot be before invoice date.')
        return due_date


# Dynamic Invoice Item Formset
from django.forms import formset_factory

class InvoiceItemForm(forms.Form):
    """Form for individual invoice items"""
    
    description = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Item description',
            'required': True
        })
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'value': '1',
            'required': True
        })
    )
    
    unit_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': '0.00',
            'required': True
        })
    )
    
    def clean_unit_price(self):
        price = self.cleaned_data.get('unit_price')
        if price and price <= 0:
            raise ValidationError('Unit price must be greater than zero.')
        return price


# Create formset for multiple invoice items
InvoiceItemFormSet = formset_factory(
    InvoiceItemForm,
    extra=1,
    min_num=1,
    validate_min=True,
    can_delete=True
)
