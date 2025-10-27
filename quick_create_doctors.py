#!/usr/bin/env python
"""
Quick create doctors and admin - Direct approach
Run: python manage.py shell < quick_create_doctors.py
"""

import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

# Doctors and admin data
users = [
    {
        'username': 'admin',
        'password': 'Admin@123',
        'first_name': 'Admin',
        'last_name': 'User',
        'role': 'ADMIN',
        'specialization': 'System Administrator',
        'qualification': 'Administrator',
        'is_superuser': True,
        'is_staff': True,
    },
    {
        'username': 'dr.shakeb.sultana',
        'password': 'Doctor@123',
        'first_name': 'ডাঃ শাকেব সুলতানা',
        'last_name': '',
        'role': 'DOCTOR',
        'specialization': 'ক্যান্সার বিশেষজ্ঞ (Cancer Specialist)',
        'qualification': 'এমবিবিএস, এম. ফিল (রেডিয়েশন অনকোলাজ)',
    },
    {
        'username': 'dr.ayesha.siddika',
        'password': 'Doctor@123',
        'first_name': 'ডাঃ আয়েশা ছিদ্দিকা',
        'last_name': '',
        'role': 'DOCTOR',
        'specialization': 'প্রসূতি, গাইনী, মেডিসিন, হরমোন ও ডায়াবেটিস',
        'qualification': 'এমবিবিএস (রাজ), বি.সি.এস (স্বাস্থ্য)',
    },
    {
        'username': 'dr.khaja.amirul',
        'password': 'Doctor@123',
        'first_name': 'ডাঃ খাজা আমিরুল ইসলাম',
        'last_name': '',
        'role': 'DOCTOR',
        'specialization': 'থ্যালাসেমিয়া ও রক্ত রোগ বিশেষজ্ঞ',
        'qualification': 'এমবিবিএস, এমডি',
    },
    {
        'username': 'dr.sm.khalid',
        'password': 'Doctor@123',
        'first_name': 'ডাঃ এস.এম. খালিদ সাইফূল্লাহ',
        'last_name': '',
        'role': 'DOCTOR',
        'specialization': 'মেডিসিন, হাড়জোড়া, বাত-ব্যাথা, সার্জারি ও ডায়াবেটিস',
        'qualification': 'এমবিবিএস (রাজ), বি.সি.এস (স্বাস্থ্য)',
    },
]

print("=" * 60)
print("Creating Admin & Doctors for nazipuruhs.com")
print("=" * 60)
print()

for user_data in users:
    try:
        username = user_data['username']
        
        # Check if exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            # Update existing
            user.first_name = user_data['first_name']
            user.last_name = user_data.get('last_name', '')
            user.role = user_data['role']
            user.specialization = user_data['specialization']
            user.qualification = user_data['qualification']
            user.is_active = True
            if user_data.get('is_superuser'):
                user.is_superuser = True
                user.is_staff = True
            user.save()
            print(f"✓ Updated: {user_data['first_name']}")
        else:
            # Create using raw SQL to bypass validation
            with connection.cursor() as cursor:
                # Get table info to build proper insert
                cursor.execute("SELECT date('now')")
                now = cursor.fetchone()[0]
                
                hashed_password = make_password(user_data['password'])
                
                is_superuser = 1 if user_data.get('is_superuser') else 0
                is_staff = 1 if user_data.get('is_staff') else 0
                
                cursor.execute("""
                    INSERT INTO accounts_user 
                    (password, last_login, is_superuser, username, first_name, last_name,
                     email, is_staff, is_active, date_joined, role, phone, address,
                     specialization, license_number, qualification, created_at, updated_at)
                    VALUES (?, NULL, ?, ?, ?, ?, '', ?, 1, ?, ?, '', '', ?, '', ?, ?, ?)
                """, [
                    hashed_password,
                    is_superuser,
                    username,
                    user_data['first_name'],
                    user_data['last_name'],
                    is_staff,
                    now,
                    user_data['role'],
                    user_data['specialization'],
                    user_data['qualification'],
                    now,
                    now
                ])
            
            print(f"✓ Created: {user_data['first_name']}")
        
        print(f"  Username: {username}")
        print(f"  Password: {user_data['password']}")
        print(f"  Role: {user_data['role']}")
        print()
        
    except Exception as e:
        print(f"✗ Error for {user_data['username']}: {str(e)}")
        import traceback
        traceback.print_exc()
        print()

print("=" * 60)
print("✅ Complete!")
print("=" * 60)
print()
print("🔐 Login Credentials:")
print("-" * 60)
print("ADMIN ACCOUNT:")
print("  Username: admin")
print("  Password: Admin@123")
print("  URL: http://nazipuruhs.com/admin")
print("-" * 60)
print("DOCTOR ACCOUNTS:")
for user_data in users[1:]:  # Skip admin
    print(f"  Username: {user_data['username']}")
    print(f"  Name: {user_data['first_name']}")
    print(f"  Password: {user_data['password']}")
    print()
print("-" * 60)
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
User = get_user_model()

docs = [
    ('dr.shakeb.sultana', 'ডাঃ শাকেব সুলতানা', 'ক্যান্সার বিশেষজ্ঞ', 'এমবিবিএস, এম. ফিল'),
    ('dr.ayesha.siddika', 'ডাঃ আয়েশা ছিদ্দিকা', 'প্রসূতি, গাইনী, মেডিসিন', 'এমবিবিএস (রাজ), বি.সি.এস'),
    ('dr.khaja.amirul', 'ডাঃ খাজা আমিরুল ইসলাম', 'থ্যালাসেমিয়া ও রক্ত রোগ', 'এমবিবিএস, এমডি'),
    ('dr.sm.khalid', 'ডাঃ এস.এম. খালিদ সাইফূল্লাহ', 'মেডিসিন, হাড়জোড়া, সার্জারি', 'এমবিবিএস (রাজ)'),
]

print("Creating doctors...")
for username, name, spec, qual in docs:
    try:
        if User.objects.filter(username=username).exists():
            u = User.objects.get(username=username)
            u.first_name, u.role, u.specialization, u.qualification, u.is_active = name, 'DOCTOR', spec, qual, True
            u.save()
            print(f"✓ Updated: {name}")
        else:
            u = User(username=username, first_name=name, email=f"{username}@h.local", 
                    password=make_password('Doctor@123'), role='DOCTOR', specialization=spec,
                    qualification=qual, is_active=True, is_staff=False, is_superuser=False)
            u.save()
            print(f"✓ Created: {name} | Login: {username} / Doctor@123")
    except Exception as e:
        print(f"✗ {username}: {e}")
print("\n✅ Done! All doctors can login with password: Doctor@123")
