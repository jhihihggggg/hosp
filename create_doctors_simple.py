#!/usr/bin/env python
"""
Simple script to add 4 Bengali doctors
Run: python manage.py shell < create_doctors_simple.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Doctor data - simplified
doctors = [
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
print("Creating Doctors for nazipuruhs.com")
print("=" * 60)
print()

for doc in doctors:
    try:
        # Check if exists
        if User.objects.filter(username=doc['username']).exists():
            user = User.objects.get(username=doc['username'])
            # Update
            user.first_name = doc['first_name']
            user.role = doc['role']
            user.specialization = doc['specialization']
            if hasattr(user, 'qualification'):
                user.qualification = doc['qualification']
            user.is_active = True
            user.save()
            print(f"✓ Updated: {doc['first_name']}")
        else:
            # Create new - first without qualification
            user = User.objects.create_user(
                username=doc['username'],
                password=doc['password'],
                first_name=doc['first_name'],
                last_name=doc.get('last_name', ''),
                is_active=True,
            )
            
            # Now set additional fields
            user.role = doc['role']
            user.specialization = doc['specialization']
            if hasattr(user, 'qualification'):
                user.qualification = doc['qualification']
            user.save()
            
            print(f"✓ Created: {doc['first_name']}")
        
        print(f"  Username: {doc['username']}")
        print(f"  Password: {doc['password']}")
        print(f"  Specialization: {doc['specialization']}")
        print()
        
    except Exception as e:
        print(f"✗ Error for {doc['username']}: {str(e)}")
        print()

print("=" * 60)
print("✅ Done!")
print("=" * 60)
print()
print("Login credentials:")
print("-" * 60)
for doc in doctors:
    print(f"Username: {doc['username']} | Password: {doc['password']}")
print("-" * 60)
