from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from datetime import timedelta
import json

from .models import LabTest, LabOrder, LabResult
from patients.models import Patient


# ========== LAB ORDER VIEWS ==========

class LabOrderListView(LoginRequiredMixin, ListView):
    """List all lab orders with status filtering"""
    model = LabOrder
    template_name = 'lab/lab_order_list.html'
    context_object_name = 'order_list'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = LabOrder.objects.select_related(
            'patient', 'ordered_by', 'appointment'
        ).prefetch_related('tests')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by priority
        if self.request.GET.get('priority'):
            queryset = queryset.filter(priority=True)
        
        return queryset.order_by('-ordered_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Status counts
        context['ordered_count'] = LabOrder.objects.filter(status='ORDERED').count()
        context['collected_count'] = LabOrder.objects.filter(status='SAMPLE_COLLECTED').count()
        context['progress_count'] = LabOrder.objects.filter(status='IN_PROGRESS').count()
        
        # Completed today
        today = timezone.now().date()
        context['completed_count'] = LabOrder.objects.filter(
            status='COMPLETED',
            ordered_at__date=today
        ).count()
        
        context['urgent_count'] = LabOrder.objects.filter(priority=True).exclude(status='COMPLETED').count()
        context['total_count'] = LabOrder.objects.count()
        
        return context


@login_required
def lab_order_list(request):
    """List lab orders - function-based view"""
    orders = LabOrder.objects.all().select_related('patient').order_by('-ordered_at')
    return render(request, 'lab/lab_order_list.html', {'orders': orders})


@login_required
def lab_order_create(request):
    """Create lab order"""
    if request.method == 'POST':
        # TODO: Implement form handling
        messages.success(request, 'Lab order created successfully!')
        return redirect('lab:order_list')
    
    context = {
        'tests': LabTest.objects.filter(is_active=True).order_by('category', 'test_name'),
        'patients': Patient.objects.filter(is_active=True).order_by('-created_at')[:50],
        'today': timezone.now().date(),
    }
    return render(request, 'lab/lab_order_form.html', context)


@login_required
def lab_order_detail(request, pk):
    """View lab order details"""
    order = get_object_or_404(LabOrder, pk=pk)
    return render(request, 'lab/lab_order_detail.html', {'order': order})


@login_required
def collect_sample(request, pk):
    """Mark sample collected"""
    if request.method == 'POST':
        order = get_object_or_404(LabOrder, pk=pk)
        order.status = 'SAMPLE_COLLECTED'
        order.sample_collected_at = timezone.now()
        order.sample_collected_by = request.user
        order.save()
        
        messages.success(request, f'Sample collected for order {order.order_number}')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def start_testing(request, pk):
    """Start testing process"""
    if request.method == 'POST':
        order = get_object_or_404(LabOrder, pk=pk)
        order.status = 'IN_PROGRESS'
        order.save()
        
        messages.success(request, f'Testing started for order {order.order_number}')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def cancel_order(request, pk):
    """Cancel lab order"""
    if request.method == 'POST':
        order = get_object_or_404(LabOrder, pk=pk)
        data = json.loads(request.body)
        reason = data.get('reason', 'No reason provided')
        
        order.status = 'CANCELLED'
        order.save()
        
        messages.success(request, f'Order {order.order_number} cancelled')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def enter_results(request, pk):
    """Enter lab results"""
    order = get_object_or_404(LabOrder, pk=pk)
    
    if request.method == 'POST':
        # Process result form
        order.status = 'COMPLETED'
        order.save()
        
        messages.success(request, f'Results saved for order {order.order_number}')
        return redirect('lab:order_list')
    
    context = {
        'order': order,
        'tests': order.tests.all(),
        'total_tests': order.tests.count(),
        'technicians': request.user.__class__.objects.filter(role='LAB_TECH') if hasattr(request.user, 'role') else [],
        'today': timezone.now().date().isoformat(),
        'now': timezone.now().time().strftime('%H:%M'),
    }
    return render(request, 'lab/lab_result_form.html', context)


@login_required
def view_report(request, pk):
    """View lab report"""
    order = get_object_or_404(LabOrder, pk=pk)
    
    if order.status != 'COMPLETED':
        messages.warning(request, 'Results are not yet complete for this order.')
        return redirect('lab:order_list')
    
    context = {
        'order': order,
        'tests': order.tests.all(),
        'patient': order.patient,
    }
    return render(request, 'lab/lab_report_detail.html', context)


@login_required
def print_report(request, pk):
    """Print lab report"""
    order = get_object_or_404(LabOrder, pk=pk)
    
    context = {
        'order': order,
        'tests': order.tests.all(),
        'patient': order.patient,
        'today': timezone.now(),
    }
    return render(request, 'lab/lab_report_print.html', context)


@login_required
def lab_test_list(request):
    """List available lab tests"""
    tests = LabTest.objects.filter(is_active=True).order_by('category', 'test_name')
    return render(request, 'lab/lab_test_list.html', {'tests': tests})


@login_required
def lab_dashboard(request):
    """Lab dashboard"""
    today = timezone.now().date()
    
    context = {
        'pending_orders': LabOrder.objects.filter(status='ORDERED').count(),
        'in_progress': LabOrder.objects.filter(status='IN_PROGRESS').count(),
        'completed_today': LabOrder.objects.filter(
            status='COMPLETED',
            ordered_at__date=today
        ).count(),
        'total_orders': LabOrder.objects.count(),
        'recent_orders': LabOrder.objects.select_related('patient', 'ordered_by').order_by('-ordered_at')[:10],
    }
    return render(request, 'accounts/lab_dashboard.html', context)


@login_required
def verify_result(request, pk):
    """Verify lab result - AJAX endpoint"""
    if request.method == 'POST':
        order = get_object_or_404(LabOrder, pk=pk)
        
        # Get or create result for each test
        for test in order.tests.all():
            result, created = LabResult.objects.get_or_create(
                order=order,
                test=test,
                defaults={
                    'performed_by': request.user,
                    'result_data': {}
                }
            )
            result.is_verified = True
            result.verified_by = request.user
            result.verified_at = timezone.now()
            result.save()
        
        messages.success(request, 'Results verified successfully!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def sample_collection_view(request):
    """Sample collection interface"""
    pending_orders = LabOrder.objects.filter(status='ORDERED').select_related('patient', 'ordered_by')[:20]
    
    # Recent collections (last 2 hours)
    two_hours_ago = timezone.now() - timedelta(hours=2)
    recent_collections = LabOrder.objects.filter(
        status__in=['SAMPLE_COLLECTED', 'IN_PROGRESS', 'COMPLETED'],
        sample_collected_at__gte=two_hours_ago
    ).select_related('patient', 'sample_collected_by').order_by('-sample_collected_at')[:10]
    
    context = {
        'pending_orders': pending_orders,
        'recent_collections': recent_collections,
    }
    return render(request, 'lab/sample_collection.html', context)


@login_required
def quality_control_view(request):
    """Quality control dashboard"""
    today = timezone.now().date()
    seven_days_ago = today - timedelta(days=7)
    
    # Mock QC data - replace with actual QC model when available
    context = {
        'qc_runs_7d': LabOrder.objects.filter(
            ordered_at__date__gte=seven_days_ago
        ).count(),
        'qc_failed': 0,  # Add QC failure tracking
        'instruments_online': 5,  # Mock data
        'qc_pending': 2,  # Mock data
        'recent_qc_logs': [],  # Add QC log model
        'qc_actions': [
            {'title': 'Calibrate Hematology Analyzer', 'detail': 'Last calibration 7 days ago'},
            {'title': 'Review Control Values', 'detail': 'Weekly review due'},
        ],
    }
    return render(request, 'lab/quality_control.html', context)
