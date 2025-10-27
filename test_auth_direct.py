#!/usr/bin/env python
"""
Direct authentication test - mimics exactly what login view does
Run: python manage.py shell < test_auth_direct.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "=" * 60)
print("DIRECT AUTHENTICATION TEST")
print("=" * 60)
print()

# Test credentials
test_logins = [
    ('admin', 'Admin@123'),
    ('dr.shakeb.sultana', 'Doctor@123'),
    ('dr.ayesha.siddika', 'Doctor@123'),
]

for username, password in test_logins:
    print(f"Testing: {username} / {password}")
    
    # Check if user exists
    try:
        user = User.objects.get(username=username)
        print(f"  ✓ User exists")
        print(f"    - is_active: {user.is_active}")
        print(f"    - has_usable_password: {user.has_usable_password()}")
        print(f"    - role: {user.role}")
        
        # Test password check
        password_correct = user.check_password(password)
        print(f"    - check_password(): {password_correct}")
        
        # Test authenticate (this is what the login view uses)
        auth_user = authenticate(username=username, password=password)
        if auth_user:
            print(f"  ✓ authenticate() WORKS - Login should succeed")
        else:
            print(f"  ✗ authenticate() FAILED - This is the problem!")
            
    except User.DoesNotExist:
        print(f"  ✗ User not found")
    
    print()

print("=" * 60)
print("If authenticate() returns None but check_password() is True,")
print("there might be a custom authentication backend issue.")
print("=" * 60)
