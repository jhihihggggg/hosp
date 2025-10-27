from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from datetime import timedelta, datetime
from decimal import Decimal
import json

from .models import (
    Income, IncomeCategory, Expense, ExpenseCategory, 
    Department, Investor, InvestorPayout, ConsultationFee
)
from .forms import IncomeForm, ExpenseForm, InvoiceForm


# ========== INCOME VIEWS ==========

class IncomeListView(LoginRequiredMixin, ListView):
    """List all income records with filtering"""
    model = Income
    template_name = 'finance/income_list.html'
    context_object_name = 'income_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Income.objects.select_related('category', 'department', 'recorded_by')
        
        # Filters
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        source = self.request.GET.get('source')
        payment_method = self.request.GET.get('payment_method')
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if source:
            queryset = queryset.filter(source=source)
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        this_month_start = today.replace(day=1)
        
        # Statistics
        context['today_income'] = Income.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
        context['today_count'] = Income.objects.filter(date=today).count()
        
        context['month_income'] = Income.objects.filter(date__gte=this_month_start).aggregate(Sum('amount'))['amount__sum'] or 0
        context['month_count'] = Income.objects.filter(date__gte=this_month_start).count()
        
        context['total_income'] = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Average income
        total_count = Income.objects.count()
        context['avg_income'] = (context['total_income'] / total_count) if total_count > 0 else 0
        
        # Chart data - Last 7 days
        chart_labels = []
        chart_data = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            chart_labels.append(date.strftime('%d %b'))
            daily_income = Income.objects.filter(date=date).aggregate(Sum('amount'))['amount__sum'] or 0
            chart_data.append(float(daily_income))
        
        context['chart_labels'] = json.dumps(chart_labels)
        context['chart_data'] = json.dumps(chart_data)
        
        # Income by source
        source_data = Income.objects.values('source').annotate(total=Sum('amount')).order_by('-total')
        context['source_labels'] = json.dumps([item['source'] for item in source_data])
        context['source_data'] = json.dumps([float(item['total']) for item in source_data])
        
        # Page total
        context['page_total'] = sum(income.amount for income in context['income_list'])
        
        context['today'] = today
        
        return context


class IncomeCreateView(LoginRequiredMixin, CreateView):
    """Create new income record"""
    model = Income
    form_class = IncomeForm
    template_name = 'finance/income_form.html'
    success_url = reverse_lazy('finance:income_list')
    
    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        messages.success(self.request, f'Income record {form.instance.income_number} created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = IncomeCategory.objects.all()
        context['today'] = timezone.now().date()
        return context


# ========== EXPENSE VIEWS ==========

class ExpenseListView(LoginRequiredMixin, ListView):
    """List all expenses with filtering"""
    model = Expense
    template_name = 'finance/expense_list.html'
    context_object_name = 'expense_list'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Expense.objects.select_related('category', 'department', 'recorded_by', 'approved_by')
        
        # Filters
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        category = self.request.GET.get('category')
        status = self.request.GET.get('status')
        department = self.request.GET.get('department')
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if category:
            queryset = queryset.filter(category_id=category)
        if status:
            if status == 'APPROVED':
                queryset = queryset.filter(is_approved=True)
            elif status == 'PENDING':
                queryset = queryset.filter(is_approved=False)
        if department:
            queryset = queryset.filter(department_id=department)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        this_month_start = today.replace(day=1)
        
        # Statistics
        context['today_expenses'] = Expense.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
        context['today_count'] = Expense.objects.filter(date=today).count()
        
        context['month_expenses'] = Expense.objects.filter(date__gte=this_month_start).aggregate(Sum('amount'))['amount__sum'] or 0
        context['month_count'] = Expense.objects.filter(date__gte=this_month_start).count()
        
        context['pending_expenses'] = Expense.objects.filter(is_approved=False).aggregate(Sum('amount'))['amount__sum'] or 0
        context['pending_count'] = Expense.objects.filter(is_approved=False).count()
        
        context['total_expenses'] = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Budget usage (example: 100000 per month)
        monthly_budget = 100000
        context['budget_usage_percent'] = min(100, (float(context['month_expenses']) / monthly_budget) * 100) if monthly_budget > 0 else 0
        
        # Chart data
        chart_labels = []
        chart_data = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            chart_labels.append(date.strftime('%d %b'))
            daily_expense = Expense.objects.filter(date=date).aggregate(Sum('amount'))['amount__sum'] or 0
            chart_data.append(float(daily_expense))
        
        context['chart_labels'] = json.dumps(chart_labels)
        context['chart_data'] = json.dumps(chart_data)
        
        # Category breakdown
        category_data = Expense.objects.values('category__name').annotate(total=Sum('amount')).order_by('-total')[:5]
        context['category_labels'] = json.dumps([item['category__name'] or 'Uncategorized' for item in category_data])
        context['category_data'] = json.dumps([float(item['total']) for item in category_data])
        
        # Page total
        context['page_total'] = sum(expense.amount for expense in context['expense_list'])
        
        context['categories'] = ExpenseCategory.objects.all()
        context['departments'] = Department.objects.filter(is_active=True)
        
        return context


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    """Create new expense record"""
    model = Expense
    form_class = ExpenseForm
    template_name = 'finance/expense_form.html'
    success_url = reverse_lazy('finance:expense_list')
    
    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        messages.success(self.request, f'Expense record {form.instance.expense_number} created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ExpenseCategory.objects.all()
        context['departments'] = Department.objects.filter(is_active=True)
        context['today'] = timezone.now().date()
        return context


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    """Update expense record"""
    model = Expense
    form_class = ExpenseForm
    template_name = 'finance/expense_form.html'
    success_url = reverse_lazy('finance:expense_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'Expense record {form.instance.expense_number} updated successfully!')
        return super().form_valid(form)


@login_required
def expense_approve(request, pk):
    """Approve expense"""
    if request.method == 'POST':
        expense = get_object_or_404(Expense, pk=pk)
        expense.is_approved = True
        expense.approved_by = request.user
        expense.save()
        messages.success(request, f'Expense {expense.expense_number} approved!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def expense_reject(request, pk):
    """Reject expense"""
    if request.method == 'POST':
        expense = get_object_or_404(Expense, pk=pk)
        data = json.loads(request.body)
        reason = data.get('reason', 'No reason provided')
        
        # You could add a rejection_reason field to the model
        expense.is_approved = False
        expense.save()
        
        messages.success(request, f'Expense {expense.expense_number} rejected!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


# ========== INVOICE VIEWS ==========
# Note: Invoice model needs to be created. For now, using placeholder

@login_required
def invoice_list(request):
    """List all invoices"""
    # Placeholder - Invoice model to be created
    context = {
        'invoice_list': [],
        'total_invoiced': 0,
        'total_paid': 0,
        'total_pending': 0,
        'total_overdue': 0,
        'paid_count': 0,
        'pending_count': 0,
        'overdue_count': 0,
        'total_count': 0,
        'paid_percent': 0,
        'pending_percent': 0,
        'overdue_percent': 0,
        'page_total': 0,
        'chart_labels': json.dumps([]),
        'chart_data': json.dumps([]),
        'today': timezone.now().date(),
    }
    return render(request, 'finance/invoice_list.html', context)


@login_required
def invoice_create(request):
    """Create new invoice"""
    if request.method == 'POST':
        # Handle invoice creation
        messages.success(request, 'Invoice created successfully!')
        return redirect('finance:invoice_list')
    
    context = {
        'today': timezone.now().date(),
    }
    return render(request, 'finance/invoice_form.html', context)


# ========== UTILITY VIEWS ==========

@login_required
def finance_dashboard(request):
    """Finance dashboard"""
    today = timezone.now().date()
    this_month = today.replace(day=1)
    
    total_income = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'finance/finance_dashboard.html', {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_profit': total_income - total_expense
    })


@login_required
def income_list(request):
    """List income records"""
    incomes = Income.objects.all().order_by('-date')
    return render(request, 'finance/income_list.html', {'incomes': incomes})


@login_required
def income_add(request):
    """Add income record"""
    if request.method == 'POST':
        # TODO: Implement form handling
        messages.success(request, 'Income recorded successfully!')
        return redirect('finance:income_list')
    return render(request, 'finance/income_add.html')


@login_required
def expense_list(request):
    """List expenses"""
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'finance/expense_list.html', {'expenses': expenses})


@login_required
def expense_add(request):
    """Add expense"""
    if request.method == 'POST':
        # TODO: Implement form handling
        messages.success(request, 'Expense recorded successfully!')
        return redirect('finance:expense_list')
    return render(request, 'finance/expense_add.html')

@login_required
def financial_reports(request):
    """Financial reports main page"""
    return render(request, 'finance/financial_reports.html')

@login_required
def daily_report(request):
    """Daily financial report"""
    today = timezone.now().date()
    income = Income.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    expense = Expense.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'finance/daily_report.html', {
        'date': today,
        'income': income,
        'expense': expense,
        'profit': income - expense
    })

@login_required
def weekly_report(request):
    """Weekly financial report"""
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    income = Income.objects.filter(date__gte=week_start).aggregate(Sum('amount'))['amount__sum'] or 0
    expense = Expense.objects.filter(date__gte=week_start).aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'finance/weekly_report.html', {
        'week_start': week_start,
        'income': income,
        'expense': expense,
        'profit': income - expense
    })

@login_required
def monthly_report(request):
    """Monthly financial report"""
    today = timezone.now().date()
    month_start = today.replace(day=1)
    
    income = Income.objects.filter(date__gte=month_start).aggregate(Sum('amount'))['amount__sum'] or 0
    expense = Expense.objects.filter(date__gte=month_start).aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'finance/monthly_report.html', {
        'month': today.strftime('%B %Y'),
        'income': income,
        'expense': expense,
        'profit': income - expense
    })

@login_required
def yearly_report(request):
    """Yearly financial report"""
    today = timezone.now().date()
    year_start = today.replace(month=1, day=1)
    
    income = Income.objects.filter(date__gte=year_start).aggregate(Sum('amount'))['amount__sum'] or 0
    expense = Expense.objects.filter(date__gte=year_start).aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'finance/yearly_report.html', {
        'year': today.year,
        'income': income,
        'expense': expense,
        'profit': income - expense
    })

@login_required
def investor_list(request):
    """List investors"""
    investors = Investor.objects.filter(is_active=True)
    return render(request, 'finance/investor_list.html', {'investors': investors})
