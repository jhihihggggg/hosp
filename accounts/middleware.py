"""
Auto-login middleware for development/testing
REMOVE THIS IN PRODUCTION!
"""

from django.contrib.auth import login
from django.contrib.auth import get_user_model

class AutoLoginMiddleware:
    """
    Automatically logs in the first admin user if no user is authenticated.
    FOR DEVELOPMENT/TESTING ONLY!
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            User = get_user_model()
            # Try to get admin user, or any user if no admin exists
            user = User.objects.filter(role='ADMIN').first()
            if not user:
                user = User.objects.first()
            
            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        response = self.get_response(request)
        return response
