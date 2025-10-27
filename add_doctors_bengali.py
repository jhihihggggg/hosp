#!/usr/bin/env python
"""
Add Bengali doctors to the system with their schedules
Run: python manage.py shell < add_doctors_bengali.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import Doctor

User = get_user_model()

# Doctor data in Bengali
doctors_data = [
    {
        'username': 'dr.shakeb.sultana',
        'email': 'shakeb.sultana@nazipuruhs.com',
        'password': 'Doctor@123',
        'first_name': 'ডাঃ শাকেব',
        'last_name': 'সুলতানা',
        'name_bengali': 'ডাঃ শাকেব সুলতানা',
        'name_english': 'Dr. Shakeb Sultana',
        'specialization': 'ক্যান্সার বিশেষজ্ঞ',
        'specialization_english': 'Cancer Specialist (Oncologist)',
        'qualifications': 'এমবিবিএস, এম. ফিল (রেডিয়েশন অনকোলাজ), পিজিটি (মেডিসিন), ডিএমইউ (ঢাকা)',
        'qualifications_english': 'MBBS, M.Phil (Radiation Oncology), PGT (Medicine), DMEU (Dhaka)',
        'schedule': 'প্রতিদিন সকাল ১০টা হইতে রাত ৬টা পর্যন্ত',
        'schedule_english': 'Daily 10:00 AM to 6:00 PM',
        'available_days': 'Sunday,Monday,Tuesday,Wednesday,Thursday,Saturday',
        'consultation_fee': 500,
    },
    {
        'username': 'dr.ayesha.siddika',
        'email': 'ayesha.siddika@nazipuruhs.com',
        'password': 'Doctor@123',
        'first_name': 'ডাঃ আয়েশা',
        'last_name': 'ছিদ্দিকা',
        'name_bengali': 'ডাঃ আয়েশা ছিদ্দিকা',
        'name_english': 'Dr. Ayesha Siddika',
        'specialization': 'প্রসূতি, গাইনী, মেডিসিন, হরমোন ও ডায়াবেটিস রোগ চিকিৎসক',
        'specialization_english': 'Obstetrics, Gynecology, Medicine, Hormone & Diabetes Specialist',
        'qualifications': 'এমবিবিএস (রাজ), বি.সি.এস (স্বাস্থ্য), এফ সি জি পি (এফপি), মেডিসিন (এন্ডোক্রাইনোলজি), মেডিকেল অফিসার, উপজেলা স্বাস্থ্য কমপ্লেক্স, পত্নীতলা, নওগাঁ।',
        'qualifications_english': 'MBBS (Raj), BCS (Health), FCGP (FP), Medicine (Endocrinology), Medical Officer, Upazila Health Complex, Patnitala, Naogaon',
        'schedule': 'প্রতিদিন বিকাল ৩টা থেকে রাত ৮টা পর্যন্ত',
        'schedule_english': 'Daily 3:00 PM to 8:00 PM',
        'available_days': 'Sunday,Monday,Tuesday,Wednesday,Thursday,Saturday',
        'consultation_fee': 500,
    },
    {
        'username': 'dr.khaja.amirul',
        'email': 'khaja.amirul@nazipuruhs.com',
        'password': 'Doctor@123',
        'first_name': 'ডাঃ খাজা আমিরুল',
        'last_name': 'ইসলাম',
        'name_bengali': 'ডাঃ খাজা আমিরুল ইসলাম',
        'name_english': 'Dr. Khaja Amirul Islam',
        'specialization': 'থ্যালাসেমিয়া ও রক্ত রোগ বিশেষজ্ঞ',
        'specialization_english': 'Thalassemia & Blood Disease Specialist (Hematologist)',
        'qualifications': 'এমবিবিএস, এমডি, ফেলো- ইউরোপিয়ান হেমাটোলজি এসোসিয়েশন মাস্টার কোর্স, সহকারী অধ্যাপক ও বিভাগীয় প্রধান, টিএমএসএস হেমাটোলজি ও বোন ম্যারো ট্রান্সপ্লান্ট সেন্টার',
        'qualifications_english': 'MBBS, MD, Fellow- European Hematology Association Master Course, Assistant Professor & Head of Department, TMSS Hematology & Bone Marrow Transplant Center',
        'schedule': 'প্রতিদিন সকাল ১০টা হইতে রাত ৬টা পর্যন্ত',
        'schedule_english': 'Daily 10:00 AM to 6:00 PM',
        'available_days': 'Sunday,Monday,Tuesday,Wednesday,Thursday,Saturday',
        'consultation_fee': 600,
    },
    {
        'username': 'dr.sm.khalid',
        'email': 'sm.khalid@nazipuruhs.com',
        'password': 'Doctor@123',
        'first_name': 'ডাঃ এস.এম. খালিদ',
        'last_name': 'সাইফূল্লাহ',
        'name_bengali': 'ডাঃ এস.এম. খালিদ সাইফূল্লাহ',
        'name_english': 'Dr. S.M. Khalid Saifullah',
        'specialization': 'মেডিসিন, হাড়জোড়া, বাত-ব্যাথা, সার্জারি ও ডায়াবেটিস রোগ অভিজ্ঞ এবং সোনোলোজিস্ট',
        'specialization_english': 'Medicine, Orthopedics, Rheumatology, Surgery & Diabetes Specialist, Sonologist',
        'qualifications': 'এমবিবিএস (রাজ), বি.সি.এস (স্বাস্থ্য), এফ.সি.পি.এস (সার্জারী ট্রেনি), সি.পি.ডি (বারডেম), আই, এম, সি, আই (শিশু) পিজিটি (অর্থো-সার্জারী), উপজেলা স্বাস্থ্য ও পঃপঃ কর্মকর্তা, পত্নীতলা, নওগাঁ।',
        'qualifications_english': 'MBBS (Raj), BCS (Health), FCPS (Surgery Trainee), CPD (BIRDEM), IMCI (Child), PGT (Ortho-Surgery), Upazila Health & FP Officer, Patnitala, Naogaon',
        'schedule': 'নিয়মিত প্রতি বৃহস্পতিবার সন্ধ্যা ৭টা হইতে রাত ৯টা পর্যন্ত',
        'schedule_english': 'Every Thursday 7:00 PM to 9:00 PM',
        'available_days': 'Thursday',
        'consultation_fee': 500,
    },
]

print("=" * 60)
print("Adding Doctors to nazipuruhs.com Database")
print("=" * 60)
print()

for doctor_data in doctors_data:
    username = doctor_data['username']
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"⚠️  User '{username}' already exists. Skipping...")
        user = User.objects.get(username=username)
    else:
        # Create user
        user = User.objects.create_user(
            username=username,
            email=doctor_data['email'],
            password=doctor_data['password'],
            first_name=doctor_data['first_name'],
            last_name=doctor_data['last_name'],
            is_doctor=True,
            is_active=True
        )
        print(f"✓ Created user: {username}")
    
    # Create or update doctor profile
    doctor, created = Doctor.objects.update_or_create(
        user=user,
        defaults={
            'name_bengali': doctor_data['name_bengali'],
            'name_english': doctor_data['name_english'],
            'specialization': doctor_data['specialization'],
            'specialization_english': doctor_data['specialization_english'],
            'qualifications': doctor_data['qualifications'],
            'qualifications_english': doctor_data['qualifications_english'],
            'schedule': doctor_data['schedule'],
            'schedule_english': doctor_data['schedule_english'],
            'available_days': doctor_data['available_days'],
            'consultation_fee': doctor_data['consultation_fee'],
            'is_active': True,
        }
    )
    
    action = "Created" if created else "Updated"
    print(f"✓ {action} doctor profile: {doctor_data['name_bengali']}")
    print(f"  Username: {username}")
    print(f"  Password: {doctor_data['password']}")
    print(f"  Email: {doctor_data['email']}")
    print(f"  Specialization: {doctor_data['specialization']}")
    print(f"  Schedule: {doctor_data['schedule']}")
    print()

print("=" * 60)
print("✅ All doctors added successfully!")
print("=" * 60)
print()
print("Doctor Login Credentials:")
print("-" * 60)
for doctor_data in doctors_data:
    print(f"Username: {doctor_data['username']}")
    print(f"Password: {doctor_data['password']}")
    print(f"Name: {doctor_data['name_bengali']} ({doctor_data['name_english']})")
    print("-" * 60)
