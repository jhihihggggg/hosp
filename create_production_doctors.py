#!/usr/bin/env python
"""
Production Doctor Setup Script
Run this on the VPS after deployment to create doctors in the production database
"""

import os
import sys
import django

# Setup Django environment for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.production_settings')
django.setup()

from django.contrib.auth import get_user_model
from appointments.models import DoctorSchedule
from datetime import time

User = get_user_model()

def create_doctors():
    """Create doctors from the signboard/roster"""
    
    doctors_data = [
        {
            'username': 'dr.altaf',
            'email': 'dr.altaf@nazipuruhs.com',
            'first_name': 'ডা. মোঃ আলতাফ',
            'last_name': 'হোসেন',
            'phone': '01732-853303',
            'specialization': 'মেডিসিন, বক্ষব্যাধি ও হৃদরোগ বিশেষজ্ঞ',
            'qualification': 'এমবিবিএস, বিসিএস (স্বাস্থ্য)',
            'registration': 'বিএমডিসি রেজিঃ-৮৮৩২৩',
            'schedules': [
                {'day': 'SUNDAY', 'start': '09:00', 'end': '14:00'},
                {'day': 'MONDAY', 'start': '09:00', 'end': '14:00'},
                {'day': 'TUESDAY', 'start': '09:00', 'end': '14:00'},
                {'day': 'WEDNESDAY', 'start': '09:00', 'end': '14:00'},
                {'day': 'THURSDAY', 'start': '09:00', 'end': '14:00'},
                {'day': 'SATURDAY', 'start': '09:00', 'end': '14:00'},
            ]
        },
        {
            'username': 'dr.jewel',
            'email': 'dr.jewel@nazipuruhs.com',
            'first_name': 'ডা. মোঃ জুয়েল',
            'last_name': 'রানা',
            'phone': '01719-364424',
            'specialization': 'শিশু রোগ বিশেষজ্ঞ',
            'qualification': 'এমবিবিএস, বিসিএস (স্বাস্থ্য), এমডি (শিশু)',
            'registration': 'বিএমডিসি রেজিঃ-৭৬৯৮৭',
            'schedules': [
                {'day': 'SUNDAY', 'start': '17:00', 'end': '20:00'},
                {'day': 'MONDAY', 'start': '17:00', 'end': '20:00'},
                {'day': 'TUESDAY', 'start': '17:00', 'end': '20:00'},
                {'day': 'WEDNESDAY', 'start': '17:00', 'end': '20:00'},
                {'day': 'THURSDAY', 'start': '17:00', 'end': '20:00'},
            ]
        },
        {
            'username': 'dr.shahana',
            'email': 'dr.shahana@nazipuruhs.com',
            'first_name': 'ডা. শাহানা',
            'last_name': 'আক্তার',
            'phone': '01914-989147',
            'specialization': 'স্ত্রী ও প্রসূতি রোগ বিশেষজ্ঞ',
            'qualification': 'এমবিবিএস, ডিজিও',
            'registration': 'বিএমডিসি রেজিঃ-৫৬৭৮৯',
            'schedules': [
                {'day': 'SUNDAY', 'start': '16:00', 'end': '20:00'},
                {'day': 'TUESDAY', 'start': '16:00', 'end': '20:00'},
                {'day': 'THURSDAY', 'start': '16:00', 'end': '20:00'},
            ]
        },
        {
            'username': 'dr.anisur',
            'email': 'dr.anisur@nazipuruhs.com',
            'first_name': 'ডা. মোঃ আনিসুর',
            'last_name': 'রহমান',
            'phone': '01911-154902',
            'specialization': 'হাড়, জয়েন্ট ও ট্রমা বিশেষজ্ঞ',
            'qualification': 'এমবিবিএস, বিসিএস (স্বাস্থ্য), এমএস (অর্থো)',
            'registration': 'বিএমডিসি রেজিঃ-৬৫৪৩২',
            'schedules': [
                {'day': 'SATURDAY', 'start': '17:00', 'end': '20:00'},
                {'day': 'SUNDAY', 'start': '17:00', 'end': '20:00'},
                {'day': 'MONDAY', 'start': '17:00', 'end': '20:00'},
            ]
        },
        {
            'username': 'dr.toslima',
            'email': 'dr.toslima@nazipuruhs.com',
            'first_name': 'ডা. তসলিমা',
            'last_name': 'খাতুন',
            'phone': '01734-789012',
            'specialization': 'চর্ম ও যৌন রোগ বিশেষজ্ঞ',
            'qualification': 'এমবিবিএস, ডিডিভি',
            'registration': 'বিএমডিসি রেজিঃ-৭৮৯০১',
            'schedules': [
                {'day': 'WEDNESDAY', 'start': '17:00', 'end': '20:00'},
                {'day': 'FRIDAY', 'start': '17:00', 'end': '20:00'},
            ]
        },
        {
            'username': 'dr.nasrin',
            'email': 'dr.nasrin@nazipuruhs.com',
            'first_name': 'ডা. নাসরিন',
            'last_name': 'সুলতানা',
            'phone': '01723-456789',
            'specialization': 'নাক, কান ও গলা বিশেষজ্ঞ',
            'qualification': 'এমবিবিএস, ডিএলও',
            'registration': 'বিএমডিসি রেজিঃ-৮৯০১২',
            'schedules': [
                {'day': 'SATURDAY', 'start': '10:00', 'end': '13:00'},
                {'day': 'WEDNESDAY', 'start': '10:00', 'end': '13:00'},
            ]
        },
    ]
    
    print("=" * 60)
    print("Creating Doctors for Production Database")
    print("=" * 60)
    
    created_count = 0
    updated_count = 0
    
    for doc_data in doctors_data:
        username = doc_data['username']
        schedules = doc_data.pop('schedules')
        
        # Check if doctor already exists
        doctor, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': doc_data['email'],
                'first_name': doc_data['first_name'],
                'last_name': doc_data['last_name'],
                'role': 'DOCTOR',
                'is_active': True,
            }
        )
        
        if created:
            # Set password
            doctor.set_password('doctor123')  # Change this in production
            doctor.save()
            created_count += 1
            print(f"✓ Created: {doc_data['first_name']} {doc_data['last_name']}")
        else:
            updated_count += 1
            print(f"→ Already exists: {doc_data['first_name']} {doc_data['last_name']}")
        
        # Update additional fields
        doctor.phone = doc_data.get('phone', '')
        doctor.specialization = doc_data.get('specialization', '')
        doctor.qualification = doc_data.get('qualification', '')
        doctor.registration_number = doc_data.get('registration', '')
        doctor.save()
        
        # Create schedules
        for sched in schedules:
            start_time = time.fromisoformat(sched['start'])
            end_time = time.fromisoformat(sched['end'])
            
            schedule, sched_created = DoctorSchedule.objects.get_or_create(
                doctor=doctor,
                day_of_week=sched['day'],
                start_time=start_time,
                defaults={
                    'end_time': end_time,
                    'max_patients': 20,
                    'consultation_duration': 15,
                    'is_active': True,
                }
            )
            
            if sched_created:
                print(f"  ✓ Schedule added: {sched['day']} {sched['start']}-{sched['end']}")
            else:
                # Update existing schedule
                schedule.end_time = end_time
                schedule.is_active = True
                schedule.save()
                print(f"  → Schedule updated: {sched['day']} {sched['start']}-{sched['end']}")
    
    print()
    print("=" * 60)
    print(f"Summary:")
    print(f"  New doctors created: {created_count}")
    print(f"  Existing doctors updated: {updated_count}")
    print(f"  Total doctors: {User.objects.filter(role='DOCTOR').count()}")
    print()
    print("Default password for all doctors: doctor123")
    print("⚠️  IMPORTANT: Change passwords after first login!")
    print("=" * 60)

if __name__ == '__main__':
    try:
        create_doctors()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
