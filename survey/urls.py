from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    # Dashboard
    path('', views.survey_dashboard, name='survey_dashboard'),
    path('dashboard/', views.survey_dashboard, name='dashboard'),
    
    # Canteen
    path('canteen/', views.canteen_dashboard, name='canteen_dashboard'),
    path('canteen/menu/', views.canteen_menu, name='canteen_menu'),
    path('canteen/orders/', views.canteen_order_list, name='canteen_order_list'),
    path('canteen/orders/create/', views.canteen_order_create, name='canteen_order_create'),  # AJAX
    path('canteen/items/<int:pk>/', views.canteen_item_detail, name='canteen_item_detail'),  # AJAX
    
    # Feedback/Survey
    path('feedback/', views.FeedbackListView.as_view(), name='feedback_list'),
    path('feedback/create/', views.feedback_create, name='feedback_create'),
    path('feedback/report/', views.feedback_report, name='feedback_report'),
    
    # Announcements
    path('announcements/', views.announcement_list, name='announcement_list'),
    
    # Legacy URLs
    path('canteen/sale/create/', views.canteen_order_create, name='canteen_sale_create'),
    path('feedback/create/<int:patient_id>/', views.feedback_create, name='feedback_create_patient'),
]
