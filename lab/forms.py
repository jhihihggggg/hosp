from django import forms
from django.core.exceptions import ValidationError
from .models import LabTest, LabOrder, LabResult
from patients.models import Patient


class LabOrderForm(forms.ModelForm):
    """Form for creating lab orders"""
    
    class Meta:
        model = LabOrder
        fields = ['patient', 'tests', 'clinical_notes', 'priority']
        widgets = {
            'patient': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'tests': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'clinical_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Clinical history, symptoms, suspected diagnosis...'
            }),
            'priority': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_tests(self):
        tests = self.cleaned_data.get('tests')
        if not tests or tests.count() == 0:
            raise ValidationError('Please select at least one test.')
        return tests


class LabResultForm(forms.Form):
    """Form for entering lab results"""
    
    test_id = forms.IntegerField(widget=forms.HiddenInput())
    result_value = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control result-input',
            'placeholder': 'Enter result',
            'required': True
        })
    )
    status = forms.ChoiceField(
        choices=[
            ('normal', 'Normal'),
            ('high', 'High'),
            ('low', 'Low'),
        ],
        initial='normal',
        widget=forms.HiddenInput()
    )
    methodology = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., ELISA, PCR, etc.'
        })
    )
    interpretation = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Optional interpretation or comments'
        })
    )


class LabTestForm(forms.ModelForm):
    """Form for managing lab tests"""
    
    class Meta:
        model = LabTest
        fields = [
            'test_code', 'test_name', 'category', 'description',
            'price', 'sample_type', 'sample_volume',
            'preparation_instructions', 'turnaround_time', 'is_active'
        ]
        widgets = {
            'test_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., CBC001',
                'required': True
            }),
            'test_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full test name',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Test description'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'required': True
            }),
            'sample_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Blood, Urine',
                'required': True
            }),
            'sample_volume': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 5ml'
            }),
            'preparation_instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'e.g., Fasting required for 8-12 hours'
            }),
            'turnaround_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 24 hours, Same day',
                'required': True
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price
    
    def clean_test_code(self):
        code = self.cleaned_data.get('test_code')
        if code:
            code = code.upper().strip()
            # Check for duplicates
            if self.instance.pk:
                # Editing existing test
                if LabTest.objects.filter(test_code=code).exclude(pk=self.instance.pk).exists():
                    raise ValidationError('Test code already exists.')
            else:
                # Creating new test
                if LabTest.objects.filter(test_code=code).exists():
                    raise ValidationError('Test code already exists.')
        return code
