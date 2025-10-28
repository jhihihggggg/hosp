#!/usr/bin/env python
"""
Create production accounts for Nazipuruhs Hospital
Run: python manage.py shell < create_production_accounts.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 80)
print("CREATING PRODUCTION ACCOUNTS FOR NAZIPURUHS HOSPITAL")
print("=" * 80)
print()

# All users data with phone as username and last 6 digits as password
users_data = [
    # Admin
    {
        'username': '01332856000',
        'phone': '01332856000',
        'password': '856000',  # Last 6 digits
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@nazipuruhs.com',
        'role': 'ADMIN',
        'is_staff': True,
        'is_superuser': True,
    },
    
    # Doctors
    {
        'username': '01712765762',
        'phone': '01712765762',
        'password': '765762',  # Last 6 digits
        'first_name': 'ডাঃ শাকেরা',
        'last_name': 'সুলতানা',
        'email': 'dr.shakera@nazipuruhs.com',
        'role': 'DOCTOR',
        'specialization': 'ক্যান্সার বিশেষজ্ঞ',
        'license_number': 'DOC-001',
    },
    {
        'username': '01761338884',
        'phone': '01761338884',
        'password': '338884',  # Last 6 digits
        'first_name': 'ডাঃ খাজা',
        'last_name': 'মোহাম্মদ',
        'email': 'dr.khaja@nazipuruhs.com',
        'role': 'DOCTOR',
        'specialization': 'মেডিসিন বিশেষজ্ঞ',
        'license_number': 'DOC-002',
    },
    {
        'username': '01312025152',
        'phone': '01312025152',
        'password': '025152',  # Last 6 digits
        'first_name': 'ডাঃ খালিদ',
        'last_name': 'হোসেন',
        'email': 'dr.khalid@nazipuruhs.com',
        'role': 'DOCTOR',
        'specialization': 'সার্জন',
        'license_number': 'DOC-003',
    },
    {
        'username': '01770928782',
        'phone': '01770928782',
        'password': '928782',  # Last 6 digits
        'first_name': 'ডাঃ আয়েশা',
        'last_name': 'ছিদ্দিকা',
        'email': 'dr.ayesha@nazipuruhs.com',
        'role': 'DOCTOR',
        'specialization': 'প্রসূতি ও গাইনী বিশেষজ্ঞ',
        'license_number': 'DOC-004',
    },
    
    # Reception
    {
        'username': '01332856002',
        'phone': '01332856002',
        'password': '856002',  # Last 6 digits
        'first_name': 'রিসেপশন',
        'last_name': 'ডেস্ক',
        'email': 'reception@nazipuruhs.com',
        'role': 'RECEPTIONIST',
    },
    
    # Canteen
    {
        'username': '01332856015',
        'phone': '01332856015',
        'password': '856015',  # Last 6 digits
        'first_name': 'ক্যান্টিন',
        'last_name': 'স্টাফ',
        'email': 'canteen@nazipuruhs.com',
        'role': 'CANTEEN',
    },
    
    # Pharmacy
    {
        'username': '01332856016',
        'phone': '01332856016',
        'password': '856016',  # Last 6 digits
        'first_name': 'ফার্মেসি',
        'last_name': 'স্টাফ',
        'email': 'pharmacy@nazipuruhs.com',
        'role': 'PHARMACY',
    },
    
    # Lab
    {
        'username': '01332856017',
        'phone': '01332856017',
        'password': '856017',  # Last 6 digits
        'first_name': 'ল্যাব',
        'last_name': 'টেকনিশিয়ান',
        'email': 'lab@nazipuruhs.com',
        'role': 'LAB',
    },
]

print("Creating/Updating accounts...")
print()

created_count = 0
updated_count = 0

for user_data in users_data:
    username = user_data['username']
    
    # Check if user exists
    if User.objects.filter(username=username).exists():
        # Update existing user
        user = User.objects.get(username=username)
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        user.is_active = True
        
        if 'is_staff' in user_data:
            user.is_staff = user_data['is_staff']
        if 'is_superuser' in user_data:
            user.is_superuser = user_data['is_superuser']
        if 'specialization' in user_data:
            user.specialization = user_data['specialization']
        if 'license_number' in user_data:
            user.license_number = user_data['license_number']
            
        user.set_password(user_data['password'])
        user.save()
        
        print(f"✓ UPDATED: {username}")
        updated_count += 1
    else:
        # Create new user
        user_create_data = {
            'username': username,
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'role': user_data['role'],
            'phone': user_data['phone'],
            'is_active': True,
        }
        
        if 'is_staff' in user_data:
            user_create_data['is_staff'] = user_data['is_staff']
        if 'is_superuser' in user_data:
            user_create_data['is_superuser'] = user_data['is_superuser']
        if 'specialization' in user_data:
            user_create_data['specialization'] = user_data['specialization']
        if 'license_number' in user_data:
            user_create_data['license_number'] = user_data['license_number']
        
        user = User.objects.create_user(password=user_data['password'], **user_create_data)
        
        print(f"✓ CREATED: {username}")
        created_count += 1
    
    print(f"  Name: {user_data['first_name']} {user_data['last_name']}")
    print(f"  Role: {user_data['role']}")
    print(f"  Phone: {user_data['phone']}")
    print(f"  Email: {user_data['email']}")
    if 'specialization' in user_data:
        print(f"  Specialization: {user_data['specialization']}")
    print()

print("=" * 80)
print(f"✅ ACCOUNT CREATION COMPLETE!")
print(f"   Created: {created_count} accounts")
print(f"   Updated: {updated_count} accounts")
print("=" * 80)
print()
print("LOGIN CREDENTIALS (VPS READY)")
print("=" * 80)
print()

print("ADMIN:")
print("-" * 80)
print("Username: 01332856000")
print("Password: 856000")
print()

print("DOCTORS:")
print("-" * 80)
print("Dr. Shakera  - Username: 01712765762  Password: 765762")
print("Dr. Khaja    - Username: 01761338884  Password: 338884")
print("Dr. Khalid   - Username: 01312025152  Password: 025152")
print("Dr. Ayesha   - Username: 01770928782  Password: 928782")
print()

print("STAFF:")
print("-" * 80)
print("Reception    - Username: 01332856002  Password: 856002")
print("Canteen      - Username: 01332856015  Password: 856015")
print("Pharmacy     - Username: 01332856016  Password: 856016")
print("Lab          - Username: 01332856017  Password: 856017")
print()

print("=" * 80)
print("NOTE: All passwords are the last 6 digits of the phone number")
print("=" * 80)
