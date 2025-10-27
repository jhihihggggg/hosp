#!/usr/bin/env python
"""Quick doctor creator - Run: python manage.py shell < quick_create_doctors.py"""
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
