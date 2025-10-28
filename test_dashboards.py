#!/usr/bin/env python
"""
Test all dashboard views for errors
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from accounts.views import (
    admin_dashboard, doctor_dashboard, receptionist_dashboard,
    lab_dashboard, pharmacy_dashboard, canteen_dashboard
)

User = get_user_model()
factory = RequestFactory()

print("Testing Dashboard Views...")
print("="*50)

# Test admin dashboard
try:
    admin_user = User.objects.filter(role='ADMIN').first()
    if admin_user:
        request = factory.get('/accounts/admin-dashboard/')
        request.user = admin_user
        response = admin_dashboard(request)
        print(f"✓ Admin Dashboard: {response.status_code}")
    else:
        print("✗ No admin user found")
except Exception as e:
    print(f"✗ Admin Dashboard Error: {e}")

# Test doctor dashboard
try:
    doctor = User.objects.filter(role='DOCTOR').first()
    if doctor:
        request = factory.get('/accounts/doctor-dashboard/')
        request.user = doctor
        response = doctor_dashboard(request)
        print(f"✓ Doctor Dashboard: {response.status_code}")
    else:
        print("✗ No doctor user found")
except Exception as e:
    print(f"✗ Doctor Dashboard Error: {e}")

# Test receptionist dashboard
try:
    receptionist = User.objects.filter(role='RECEPTIONIST').first()
    if receptionist:
        request = factory.get('/accounts/receptionist-dashboard/')
        request.user = receptionist
        response = receptionist_dashboard(request)
        print(f"✓ Receptionist Dashboard: {response.status_code}")
    else:
        print("✗ No receptionist user found")
except Exception as e:
    print(f"✗ Receptionist Dashboard Error: {e}")

# Test lab dashboard
try:
    lab_staff = User.objects.filter(role='LAB').first()
    if not lab_staff:
        # Create one for testing - provide all required fields
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO accounts_user (
                    username, first_name, last_name, role, 
                    password, is_active, is_staff, is_superuser, 
                    date_joined, qualification, email, phone, address,
                    specialization, license_number, created_at, updated_at
                ) VALUES (
                    'lab_test', 'Lab', 'Staff', 'LAB',
                    'pbkdf2_sha256$720000$dummy', 1, 0, 0,
                    datetime('now'), '', '', '', '',
                    '', '', datetime('now'), datetime('now')
                )
            """)
        lab_staff = User.objects.get(username='lab_test')
    request = factory.get('/accounts/lab-dashboard/')
    request.user = lab_staff
    response = lab_dashboard(request)
    print(f"✓ Lab Dashboard: {response.status_code}")
except Exception as e:
    print(f"✗ Lab Dashboard Error: {e}")

# Test pharmacy dashboard
try:
    pharmacy_staff = User.objects.filter(role='PHARMACY').first()
    if not pharmacy_staff:
        # Create one for testing
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO accounts_user (
                    username, first_name, last_name, role,
                    password, is_active, is_staff, is_superuser,
                    date_joined, qualification, email, phone, address,
                    specialization, license_number, created_at, updated_at
                ) VALUES (
                    'pharmacy_test', 'Pharmacy', 'Staff', 'PHARMACY',
                    'pbkdf2_sha256$720000$dummy', 1, 0, 0,
                    datetime('now'), '', '', '', '',
                    '', '', datetime('now'), datetime('now')
                )
            """)
        pharmacy_staff = User.objects.get(username='pharmacy_test')
    request = factory.get('/accounts/pharmacy-dashboard/')
    request.user = pharmacy_staff
    response = pharmacy_dashboard(request)
    print(f"✓ Pharmacy Dashboard: {response.status_code}")
except Exception as e:
    print(f"✗ Pharmacy Dashboard Error: {e}")

# Test canteen dashboard
try:
    canteen_staff = User.objects.filter(role='CANTEEN').first()
    if not canteen_staff:
        # Create one for testing
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO accounts_user (
                    username, first_name, last_name, role,
                    password, is_active, is_staff, is_superuser,
                    date_joined, qualification, email, phone, address,
                    specialization, license_number, created_at, updated_at
                ) VALUES (
                    'canteen_test', 'Canteen', 'Staff', 'CANTEEN',
                    'pbkdf2_sha256$720000$dummy', 1, 0, 0,
                    datetime('now'), '', '', '', '',
                    '', '', datetime('now'), datetime('now')
                )
            """)
        canteen_staff = User.objects.get(username='canteen_test')
    request = factory.get('/accounts/canteen-dashboard/')
    request.user = canteen_staff
    response = canteen_dashboard(request)
    print(f"✓ Canteen Dashboard: {response.status_code}")
except Exception as e:
    print(f"✗ Canteen Dashboard Error: {e}")

print("="*50)
print("Dashboard Testing Complete!")
