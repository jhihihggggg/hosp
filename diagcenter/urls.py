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
from accounts import test_views

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # TEMP: Simple test pages (NO LOGIN REQUIRED)
    path("test-admin/", test_views.test_admin, name="test_admin"),
    path("test-doctor/", test_views.test_doctor, name="test_doctor"),
    path("test-reception/", test_views.test_reception, name="test_reception"),
    path("test-display/", test_views.test_display, name="test_display"),
    path("test-pharmacy/", test_views.test_pharmacy, name="test_pharmacy"),
    path("test-canteen/", test_views.test_canteen, name="test_canteen"),
    
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
