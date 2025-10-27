from django.urls import path, include
from rest_framework.routers import DefaultRouter

# API Router (placeholder - implement ViewSets as needed)
router = DefaultRouter()

# Example:
# from patients.api import PatientViewSet
# router.register(r'patients', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
