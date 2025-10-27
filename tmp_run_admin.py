from accounts.views import admin_dashboard
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

User = get_user_model()
factory = RequestFactory()

admin_user = User.objects.filter(is_superuser=True).first() or User.objects.filter(role='ADMIN').first()
print('Admin user found:', bool(admin_user))
req = factory.get('/accounts/admin-dashboard/')
req.user = admin_user if admin_user else AnonymousUser()
try:
    response = admin_dashboard(req)
    print('Admin dashboard executed, response type:', type(response))
    if hasattr(response, 'status_code'):
        print('Status code:', response.status_code)
except Exception as e:
    import traceback
    traceback.print_exc()
