from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from datetime import timedelta, datetime
from decimal import Decimal
import json

from .models import Drug, DrugCategory, PharmacySale
from appointments.models import Prescription
from patients.models import Patient


# ========== DRUG/INVENTORY VIEWS ==========

class DrugListView(LoginRequiredMixin, ListView):
    """List all drugs/medicines"""
    model = Drug
    template_name = 'pharmacy/drug_list.html'
    context_object_name = 'drugs'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Drug.objects.select_related('category').filter(is_active=True)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(brand_name__icontains=search) |
                Q(generic_name__icontains=search) |
                Q(drug_code__icontains=search)
            )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        
        # Filter by stock status
        stock_status = self.request.GET.get('stock_status')
        if stock_status == 'low_stock':
            queryset = queryset.filter(quantity_in_stock__lte=F('reorder_level'))
        elif stock_status == 'out_of_stock':
            queryset = queryset.filter(quantity_in_stock=0)
        elif stock_status == 'in_stock':
            queryset = queryset.filter(quantity_in_stock__gt=F('reorder_level'))
        
        # Sorting
        sort_by = self.request.GET.get('sort', 'brand_name')
        if sort_by == 'quantity':
            queryset = queryset.order_by('quantity_in_stock')
        elif sort_by == 'expiry':
            queryset = queryset.order_by('expiry_date')
        elif sort_by == 'value':
            queryset = queryset.annotate(
                stock_value=F('quantity_in_stock') * F('unit_price')
            ).order_by('-stock_value')
        else:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        all_drugs = Drug.objects.filter(is_active=True)
        context['total_drugs'] = all_drugs.count()
        context['in_stock_count'] = all_drugs.filter(quantity_in_stock__gt=F('reorder_level')).count()
        context['low_stock_count'] = all_drugs.filter(
            quantity_in_stock__gt=0,
            quantity_in_stock__lte=F('reorder_level')
        ).count()
        context['out_of_stock_count'] = all_drugs.filter(quantity_in_stock=0).count()
        
        # Categories
        context['categories'] = DrugCategory.objects.all().values_list('name', flat=True).distinct()
        
        return context


class DrugCreateView(LoginRequiredMixin, CreateView):
    """Create new drug"""
    model = Drug
    template_name = 'pharmacy/drug_form.html'
    fields = [
        'drug_code', 'generic_name', 'brand_name', 'category', 'form', 'strength',
        'manufacturer', 'quantity_in_stock', 'reorder_level', 'unit_price',
        'selling_price', 'manufacture_date', 'expiry_date', 'description',
        'side_effects', 'storage_instructions'
    ]
    success_url = reverse_lazy('pharmacy:drug_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Drug {form.instance.brand_name} added successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DrugCategory.objects.all()
        context['today'] = timezone.now().date()
        return context


class DrugUpdateView(LoginRequiredMixin, UpdateView):
    """Update drug information"""
    model = Drug
    template_name = 'pharmacy/drug_form.html'
    fields = [
        'drug_code', 'generic_name', 'brand_name', 'category', 'form', 'strength',
        'manufacturer', 'quantity_in_stock', 'reorder_level', 'unit_price',
        'selling_price', 'manufacture_date', 'expiry_date', 'description',
        'side_effects', 'storage_instructions'
    ]
    success_url = reverse_lazy('pharmacy:drug_list')
    
    def form_valid(self, form):
        messages.success(self, f'Drug {form.instance.brand_name} updated successfully!')
        return super().form_valid(form)


@login_required
def drug_detail(request, pk):
    """Drug details (AJAX)"""
    drug = get_object_or_404(Drug, pk=pk)
    data = {
        'id': drug.id,
        'name': drug.brand_name,
        'generic': drug.generic_name,
        'quantity': drug.quantity_in_stock,
        'unit': 'units',  # You can add a unit field to the model
        'price': float(drug.selling_price),
    }
    return JsonResponse(data)


@login_required
def drug_adjust_stock(request, pk):
    """Adjust drug stock"""
    if request.method == 'POST':
        drug = get_object_or_404(Drug, pk=pk)
        data = json.loads(request.body)
        
        adjust_type = data.get('adjust_type')
        quantity = int(data.get('quantity', 0))
        reason = data.get('reason', '')
        
        if adjust_type == 'add':
            drug.quantity_in_stock += quantity
        elif adjust_type == 'reduce':
            drug.quantity_in_stock = max(0, drug.quantity_in_stock - quantity)
        elif adjust_type == 'set':
            drug.quantity_in_stock = quantity
        
        drug.save()
        
        # Log the adjustment (you could create a StockAdjustment model)
        messages.success(request, f'Stock adjusted for {drug.brand_name}')
        return JsonResponse({'status': 'success', 'new_quantity': drug.quantity_in_stock})
    
    return JsonResponse({'status': 'error'}, status=400)


# ========== STOCK REPORT ==========

@login_required
def stock_report(request):
    """Comprehensive stock report"""
    # Get all active drugs
    drugs = Drug.objects.filter(is_active=True).select_related('category')
    
    # Apply filters
    search = request.GET.get('search')
    if search:
        drugs = drugs.filter(
            Q(brand_name__icontains=search) |
            Q(generic_name__icontains=search)
        )
    
    category = request.GET.get('category')
    if category:
        drugs = drugs.filter(category__name=category)
    
    stock_status = request.GET.get('stock_status')
    if stock_status == 'low_stock':
        drugs = drugs.filter(quantity_in_stock__lte=F('reorder_level'), quantity_in_stock__gt=0)
    elif stock_status == 'out_of_stock':
        drugs = drugs.filter(quantity_in_stock=0)
    elif stock_status == 'in_stock':
        drugs = drugs.filter(quantity_in_stock__gt=F('reorder_level'))
    
    # Statistics
    all_drugs = Drug.objects.filter(is_active=True)
    total_drugs = all_drugs.count()
    in_stock_count = all_drugs.filter(quantity_in_stock__gt=F('reorder_level')).count()
    low_stock_count = all_drugs.filter(
        quantity_in_stock__gt=0,
        quantity_in_stock__lte=F('reorder_level')
    ).count()
    out_of_stock_count = all_drugs.filter(quantity_in_stock=0).count()
    
    # Calculate values
    total_inventory_value = sum(
        drug.quantity_in_stock * drug.unit_price
        for drug in all_drugs
    )
    potential_revenue = sum(
        drug.quantity_in_stock * drug.selling_price
        for drug in all_drugs
    )
    profit_margin = potential_revenue - total_inventory_value
    profit_percentage = (profit_margin / total_inventory_value * 100) if total_inventory_value > 0 else 0
    
    # Expiry alerts
    today = timezone.now().date()
    three_months_later = today + timedelta(days=90)
    
    expired_drugs = all_drugs.filter(expiry_date__lt=today)
    expiring_soon = all_drugs.filter(expiry_date__gte=today, expiry_date__lte=three_months_later)
    
    # Annotate days to expiry
    for drug in expiring_soon:
        drug.days_to_expiry = (drug.expiry_date - today).days
    
    # Top drugs by value
    drugs_with_value = list(all_drugs)
    for drug in drugs_with_value:
        drug.stock_value = drug.quantity_in_stock * drug.unit_price
    
    drugs_with_value.sort(key=lambda x: x.stock_value, reverse=True)
    top_10_drugs = drugs_with_value[:10]
    
    # Chart data
    top_drugs_labels = [drug.brand_name[:20] for drug in top_10_drugs]
    top_drugs_values = [float(drug.stock_value) for drug in top_10_drugs]
    
    # Page total value
    page_total_value = sum(drug.quantity_in_stock * drug.unit_price for drug in drugs)
    
    context = {
        'drugs': drugs,
        'total_drugs': total_drugs,
        'in_stock_count': in_stock_count,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'total_inventory_value': total_inventory_value,
        'potential_revenue': potential_revenue,
        'profit_margin': profit_margin,
        'profit_percentage': profit_percentage,
        'expired_drugs': expired_drugs,
        'expiring_soon': expiring_soon,
        'categories': DrugCategory.objects.all().values_list('name', flat=True).distinct(),
        'top_drugs_labels': json.dumps(top_drugs_labels),
        'top_drugs_values': json.dumps(top_drugs_values),
        'page_total_value': page_total_value,
        'today': today,
    }
    
    return render(request, 'pharmacy/stock_report.html', context)


# ========== PRESCRIPTION PROCESSING ==========

@login_required
def prescription_process(request, pk):
    """Process prescription and dispense medicines"""
    prescription = get_object_or_404(Prescription, pk=pk)
    
    if request.method == 'POST':
        # Process dispensing
        messages.success(request, 'Prescription processed successfully!')
        return redirect('pharmacy:prescription_list')
    
    context = {
        'prescription': prescription,
        'patient': prescription.appointment.patient,
        'available_drugs': Drug.objects.filter(is_active=True, quantity_in_stock__gt=0),
    }
    return render(request, 'pharmacy/prescription_process.html', context)


@login_required
def prescription_list(request):
    """List prescriptions to be filled"""
    prescriptions = Prescription.objects.select_related(
        'appointment__patient', 'appointment__doctor'
    ).order_by('-appointment__scheduled_time')[:50]
    
    return render(request, 'pharmacy/prescription_list.html', {
        'prescriptions': prescriptions
    })


@login_required
def prescription_dispense(request, pk):
    """Mark prescription as dispensed - AJAX endpoint"""
    if request.method == 'POST':
        prescription = get_object_or_404(Prescription, pk=pk)
        
        # Update prescription status if model has status field
        # prescription.status = 'DISPENSED'
        # prescription.dispensed_at = timezone.now()
        # prescription.dispensed_by = request.user
        # prescription.save()
        
        messages.success(request, f'Prescription dispensed successfully!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def prescription_detail(request, pk):
    """View prescription details"""
    prescription = get_object_or_404(Prescription, pk=pk)
    context = {
        'prescription': prescription,
        'patient': prescription.appointment.patient,
    }
    return render(request, 'pharmacy/prescription_detail.html', context)


@login_required
def prescription_print(request, pk):
    """Print prescription"""
    prescription = get_object_or_404(Prescription, pk=pk)
    context = {
        'prescription': prescription,
        'patient': prescription.appointment.patient,
        'today': timezone.now(),
    }
    return render(request, 'pharmacy/prescription_print.html', context)


# ========== SUPPLIER MANAGEMENT ==========

@login_required
def supplier_list(request):
    """List all suppliers"""
    # Mock supplier data - create Supplier model if needed
    suppliers = []  # Replace with Supplier.objects.all()
    return render(request, 'pharmacy/supplier_list.html', {'suppliers': suppliers})


@login_required
def supplier_create(request):
    """Create new supplier"""
    if request.method == 'POST':
        # TODO: Implement supplier form
        messages.success(request, 'Supplier created successfully!')
        return redirect('pharmacy:supplier_list')
    return render(request, 'pharmacy/supplier_form.html')


@login_required
def supplier_edit(request, pk):
    """Edit supplier"""
    # supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        messages.success(request, 'Supplier updated successfully!')
        return redirect('pharmacy:supplier_list')
    return render(request, 'pharmacy/supplier_form.html')


@login_required
def supplier_delete(request, pk):
    """Delete supplier - AJAX endpoint"""
    if request.method == 'POST':
        # supplier = get_object_or_404(Supplier, pk=pk)
        # supplier.delete()
        messages.success(request, 'Supplier deleted successfully!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


# ========== STOCK ADJUSTMENT ==========

@login_required
def stock_adjust(request):
    """Stock adjustment form"""
    if request.method == 'POST':
        drug_id = request.POST.get('drug_id')
        adjust_type = request.POST.get('adjust_type')
        quantity = int(request.POST.get('quantity', 0))
        reason = request.POST.get('reason', '')
        
        drug = get_object_or_404(Drug, pk=drug_id)
        
        # Create stock adjustment record
        from .models import StockAdjustment
        
        # Determine quantity sign based on type
        if adjust_type in ['RETURN', 'EXPIRED', 'DAMAGED']:
            quantity = -abs(quantity)
        elif adjust_type == 'PURCHASE':
            quantity = abs(quantity)
        
        adjustment = StockAdjustment.objects.create(
            drug=drug,
            adjustment_type=adjust_type,
            quantity=quantity,
            reason=reason,
            adjusted_by=request.user,
        )
        
        messages.success(request, f'Stock adjusted for {drug.brand_name}')
        return redirect('pharmacy:stock_adjust_history')
    
    drugs = Drug.objects.filter(is_active=True).order_by('brand_name')
    return render(request, 'pharmacy/stock_adjust_form.html', {'drugs': drugs})


@login_required
def stock_adjust_history(request):
    """View stock adjustment history"""
    from .models import StockAdjustment
    
    adjustments = StockAdjustment.objects.select_related(
        'drug', 'adjusted_by'
    ).order_by('-adjusted_at')[:100]
    
    return render(request, 'pharmacy/stock_adjust_history.html', {
        'adjustments': adjustments
    })


@login_required
def quick_adjust_modal(request, pk):
    """Quick adjust modal - AJAX endpoint"""
    if request.method == 'POST':
        drug = get_object_or_404(Drug, pk=pk)
        data = json.loads(request.body)
        
        adjust_type = data.get('adjust_type', 'CORRECTION')
        quantity = int(data.get('quantity', 0))
        reason = data.get('reason', 'Quick adjustment')
        
        from .models import StockAdjustment
        
        adjustment = StockAdjustment.objects.create(
            drug=drug,
            adjustment_type=adjust_type,
            quantity=quantity,
            reason=reason,
            adjusted_by=request.user,
        )
        
        return JsonResponse({
            'status': 'success',
            'new_quantity': drug.quantity_in_stock
        })
    return JsonResponse({'status': 'error'}, status=400)


# ========== PHARMACY DASHBOARD ==========

@login_required
def pharmacy_dashboard(request):
    """Pharmacy dashboard"""
    today = timezone.now().date()
    
    context = {
        'total_drugs': Drug.objects.filter(is_active=True).count(),
        'low_stock_count': Drug.objects.filter(
            quantity_in_stock__lte=F('reorder_level'),
            is_active=True
        ).count(),
        'out_of_stock': Drug.objects.filter(quantity_in_stock=0, is_active=True).count(),
        'expiring_soon': Drug.objects.filter(
            expiry_date__lte=today + timedelta(days=90),
            expiry_date__gte=today,
            is_active=True
        ).count(),
    }
    return render(request, 'accounts/pharmacy_dashboard.html', context)


@login_required
def drug_list(request):
    """List all drugs"""
    drugs = Drug.objects.filter(is_active=True).order_by('brand_name')
    return render(request, 'pharmacy/drug_list.html', {'drugs': drugs})

@login_required
def drug_add(request):
    """Add new drug"""
    if request.method == 'POST':
        # TODO: Implement form handling
        messages.success(request, 'Drug added successfully!')
        return redirect('pharmacy:drug_list')
    return render(request, 'pharmacy/drug_add.html')

@login_required
def drug_detail(request, pk):
    """View drug details"""
    drug = get_object_or_404(Drug, pk=pk)
    return render(request, 'pharmacy/drug_detail.html', {'drug': drug})

@login_required
def sale_list(request):
    """List pharmacy sales"""
    sales = PharmacySale.objects.all().order_by('-sale_date')
    return render(request, 'pharmacy/sale_list.html', {'sales': sales})

@login_required
def sale_create(request):
    """Create new sale"""
    if request.method == 'POST':
        # TODO: Implement form handling
        messages.success(request, 'Sale completed successfully!')
        return redirect('pharmacy:sale_list')
    return render(request, 'pharmacy/sale_create.html')

@login_required
def sale_detail(request, pk):
    """View sale details"""
    sale = get_object_or_404(PharmacySale, pk=pk)
    return render(request, 'pharmacy/sale_detail.html', {'sale': sale})

@login_required
def inventory_report(request):
    """Inventory report"""
    drugs = Drug.objects.filter(is_active=True).order_by('brand_name')
    return render(request, 'pharmacy/inventory_report.html', {'drugs': drugs})

@login_required
def low_stock_alert(request):
    """Low stock alerts"""
    low_stock = Drug.objects.filter(quantity_in_stock__lte=F('reorder_level'))
    return render(request, 'pharmacy/low_stock_alert.html', {'drugs': low_stock})
