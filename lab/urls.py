from django.urls import path
from . import views

app_name = 'lab'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.lab_dashboard, name='lab_dashboard'),
    
    # Lab Orders
    path('orders/', views.LabOrderListView.as_view(), name='order_list'),
    path('order/create/', views.lab_order_create, name='order_create'),
    path('order/<int:pk>/', views.lab_order_detail, name='order_detail'),
    path('order/<int:pk>/details/', views.lab_order_detail, name='order_details'),  # AJAX
    path('order/<int:pk>/collect-sample/', views.collect_sample, name='collect_sample'),
    path('order/<int:pk>/start-testing/', views.start_testing, name='start_testing'),
    path('order/<int:pk>/cancel/', views.cancel_order, name='cancel_order'),
    
    # Lab Results
    path('order/<int:pk>/result-entry/', views.enter_results, name='result_entry'),
    path('result/<int:pk>/verify/', views.verify_result, name='verify_result'),
    path('order/<int:pk>/report/', views.view_report, name='report_view'),
    path('order/<int:pk>/report/print/', views.print_report, name='report_print'),
    path('order/<int:pk>/report/preview/', views.print_report, name='report_preview'),
    
    # Sample Collection & QC
    path('sample-collection/', views.sample_collection_view, name='sample_collection'),
    path('quality-control/', views.quality_control_view, name='quality_control'),
    
    # Lab Tests Management
    path('tests/', views.lab_test_list, name='test_list'),
    path('tests/manage/', views.lab_test_manage, name='test_manage'),
    path('tests/create/', views.lab_test_create, name='test_create'),
    path('tests/<int:pk>/edit/', views.lab_test_edit, name='test_edit'),
    path('tests/<int:pk>/delete/', views.lab_test_delete, name='test_delete'),
    
    # Legacy URLs (backward compatibility)
    path('', views.lab_order_list, name='lab_order_list'),
    path('order/<int:pk>/enter-results/', views.enter_results, name='enter_results'),
]
