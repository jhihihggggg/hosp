"""
URL configuration for diagcenter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from accounts import views as account_views

# TEMP: Direct dashboard access for testing (bypass login)
from django.http import HttpResponse
from django.shortcuts import render, redirect

def temp_admin_dashboard(request):
    """Temporary admin dashboard without login"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    admin_user = User.objects.filter(role='ADMIN').first()
    if admin_user:
        from django.contrib.auth import login
        login(request, admin_user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('accounts:admin_dashboard')

def temp_doctor_dashboard(request):
    """Temporary doctor dashboard without login"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    doctor_user = User.objects.filter(role='DOCTOR').first()
    if doctor_user:
        from django.contrib.auth import login
        login(request, doctor_user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('accounts:doctor_dashboard')

def temp_reception_dashboard(request):
    """Temporary reception dashboard without login"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    reception_user = User.objects.filter(role='RECEPTIONIST').first()
    if reception_user:
        from django.contrib.auth import login
        login(request, reception_user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('accounts:receptionist_dashboard')

def temp_display_dashboard(request):
    """Temporary display monitor without login"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    display_user = User.objects.filter(role='DISPLAY').first()
    if display_user:
        from django.contrib.auth import login
        login(request, display_user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('accounts:display_monitor')

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # TEMP: Direct dashboard access (NO LOGIN REQUIRED)
    path("test-admin/", temp_admin_dashboard, name="test_admin"),
    path("test-doctor/", temp_doctor_dashboard, name="test_doctor"),
    path("test-reception/", temp_reception_dashboard, name="test_reception"),
    path("test-display/", temp_display_dashboard, name="test_display"),
    
    # Public landing page
    path("", account_views.landing_page, name="home"),
    
    # Authentication URLs (at root level for easy access)
    path("login/", account_views.user_login, name="login"),
    path("logout/", account_views.user_logout, name="logout"),
    
    # App URLs
    path("accounts/", include("accounts.urls")),
    path("patients/", include("patients.urls")),
    path("appointments/", include("appointments.urls")),
    path("lab/", include("lab.urls")),
    path("pharmacy/", include("pharmacy.urls")),
    path("finance/", include("finance.urls")),
    path("survey/", include("survey.urls")),
    
    # API URLs
    path("api/", include("diagcenter.api_urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
