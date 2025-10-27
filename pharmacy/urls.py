from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    # Dashboard
    path('', views.pharmacy_dashboard, name='pharmacy_dashboard'),
    path('dashboard/', views.pharmacy_dashboard, name='dashboard'),
    
    # Drug Management
    path('drugs/', views.DrugListView.as_view(), name='drug_list'),
    path('drugs/create/', views.DrugCreateView.as_view(), name='drug_create'),
    path('drugs/<int:pk>/', views.drug_detail, name='drug_detail'),
    path('drugs/<int:pk>/update/', views.DrugUpdateView.as_view(), name='drug_update'),
    path('drugs/<int:pk>/edit/', views.DrugUpdateView.as_view(), name='drug_edit'),
    path('drugs/<int:pk>/adjust-stock/', views.drug_adjust_stock, name='drug_adjust_stock'),
    path('drugs/<int:pk>/quick-adjust/', views.quick_adjust_modal, name='quick_adjust'),
    
    # Stock Management  
    path('stock-report/', views.stock_report, name='stock_report'),
    path('stock-adjust/', views.stock_adjust, name='stock_adjust'),
    path('stock-adjust-history/', views.stock_adjust_history, name='stock_adjust_history'),
    path('inventory/', views.stock_report, name='inventory_report'),
    path('low-stock/', views.stock_report, name='low_stock_alert'),
    
    # Prescription Processing
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescription/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('prescription/<int:pk>/process/', views.prescription_process, name='prescription_process'),
    path('prescription/<int:pk>/print/', views.prescription_print, name='prescription_print'),
    path('prescription/<int:pk>/dispense/', views.prescription_dispense, name='prescription_dispense'),
    
    # Supplier Management
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('supplier/create/', views.supplier_create, name='supplier_create'),
    path('supplier/<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    path('supplier/<int:pk>/delete/', views.supplier_delete, name='supplier_delete'),
    
    # Legacy URLs
    path('drugs/add/', views.DrugCreateView.as_view(), name='drug_add'),
]
