#!/usr/bin/env python
"""
Verify and fix login credentials
Run: python manage.py shell < verify_and_fix_logins.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 60)
print("Verifying and Fixing Login Credentials")
print("=" * 60)
print()

# Check and fix admin
print("ADMIN ACCOUNT:")
try:
    admin = User.objects.get(username='admin')
    admin.set_password('Admin@123')
    admin.is_superuser = True
    admin.is_staff = True
    admin.is_active = True
    admin.role = 'ADMIN'
    admin.save()
    print(f"✓ Admin account ready")
    print(f"  Username: admin")
    print(f"  Password: Admin@123")
    print(f"  Is superuser: {admin.is_superuser}")
    print(f"  Is staff: {admin.is_staff}")
    print(f"  Is active: {admin.is_active}")
except User.DoesNotExist:
    print("✗ Admin not found - creating...")
    admin = User.objects.create_superuser(
        username='admin',
        password='Admin@123',
        first_name='Admin',
        last_name='User',
        role='ADMIN'
    )
    print("✓ Admin created")
print()

# Check and fix doctors
doctors = [
    ('dr.shakeb.sultana', 'ডাঃ শাকেব সুলতানা'),
    ('dr.ayesha.siddika', 'ডাঃ আয়েশা ছিদ্দিকা'),
    ('dr.khaja.amirul', 'ডাঃ খাজা আমিরুল ইসলাম'),
    ('dr.sm.khalid', 'ডাঃ এস.এম. খালিদ সাইফূল্লাহ'),
]

print("DOCTOR ACCOUNTS:")
for username, name in doctors:
    try:
        doctor = User.objects.get(username=username)
        doctor.set_password('Doctor@123')
        doctor.is_active = True
        doctor.role = 'DOCTOR'
        doctor.save()
        print(f"✓ {name}")
        print(f"  Username: {username}")
        print(f"  Password: Doctor@123")
        print(f"  Is active: {doctor.is_active}")
        print(f"  Role: {doctor.role}")
        print()
    except User.DoesNotExist:
        print(f"✗ {username} not found")
        print()

print("=" * 60)
print("Testing Login Credentials")
print("=" * 60)
print()

from django.contrib.auth import authenticate

# Test admin
admin_user = authenticate(username='admin', password='Admin@123')
if admin_user:
    print("✓ Admin login works!")
else:
    print("✗ Admin login failed")
print()

# Test doctors
for username, name in doctors:
    doctor_user = authenticate(username=username, password='Doctor@123')
    if doctor_user:
        print(f"✓ {username} login works!")
    else:
        print(f"✗ {username} login failed")

print()
print("=" * 60)
print("✅ Done!")
print("=" * 60)
