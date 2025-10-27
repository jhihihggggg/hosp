from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    # Dashboard
    path('', views.finance_dashboard, name='finance_dashboard'),
    
    # Income URLs
    path('income/', views.IncomeListView.as_view(), name='income_list'),
    path('income/create/', views.IncomeCreateView.as_view(), name='income_create'),
    path('income/<int:pk>/details/', views.income_list, name='income_details'),  # AJAX
    path('income/<int:pk>/receipt/', views.income_list, name='income_receipt'),  # Print
    path('income/<int:pk>/delete/', views.income_list, name='income_delete'),
    
    # Expense URLs
    path('expense/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expense/create/', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('expense/<int:pk>/update/', views.ExpenseUpdateView.as_view(), name='expense_update'),
    path('expense/<int:pk>/details/', views.expense_list, name='expense_details'),  # AJAX
    path('expense/<int:pk>/approve/', views.expense_approve, name='expense_approve'),
    path('expense/<int:pk>/reject/', views.expense_reject, name='expense_reject'),
    
    # Invoice URLs
    path('invoice/', views.invoice_list, name='invoice_list'),
    path('invoice/create/', views.invoice_create, name='invoice_create'),
    path('invoice/<int:pk>/', views.invoice_list, name='invoice_detail'),
    path('invoice/<int:pk>/update/', views.invoice_create, name='invoice_update'),
    path('invoice/<int:pk>/print/', views.invoice_list, name='invoice_print'),
    path('invoice/<int:pk>/record-payment/', views.invoice_list, name='invoice_record_payment'),
    path('invoice/<int:pk>/email/', views.invoice_list, name='invoice_email'),
    path('invoices/export/', views.invoice_list, name='invoices_export'),
    
    # Legacy URLs (keep for compatibility)
    path('income/add/', views.income_add, name='income_add'),
    path('expense/add/', views.expense_add, name='expense_add'),
    path('reports/', views.financial_reports, name='financial_reports'),
    path('reports/daily/', views.daily_report, name='daily_report'),
    path('reports/weekly/', views.weekly_report, name='weekly_report'),
    path('reports/monthly/', views.monthly_report, name='monthly_report'),
    path('reports/yearly/', views.yearly_report, name='yearly_report'),
    path('investors/', views.investor_list, name='investor_list'),
]
