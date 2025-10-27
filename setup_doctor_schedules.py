#!/usr/bin/env python
"""
Setup doctor schedules based on the exact information provided
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model
from appointments.models import DoctorSchedule
from datetime import time

User = get_user_model()

# Doctor schedule data matching the exact information
SCHEDULES = [
    {
        'username': 'dr_shakeb_sultana',
        'schedules': [
            {'day': 'MONDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 15, 'max_patients': 32},
            {'day': 'TUESDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 15, 'max_patients': 32},
            {'day': 'WEDNESDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 15, 'max_patients': 32},
            {'day': 'THURSDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 15, 'max_patients': 32},
            {'day': 'FRIDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 15, 'max_patients': 32},
            {'day': 'SATURDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 15, 'max_patients': 32},
        ]
    },
    {
        'username': 'dr_ayesha_siddika',
        'schedules': [
            {'day': 'SUNDAY', 'start': time(15, 0), 'end': time(20, 0), 'duration': 20, 'max_patients': 15},
            {'day': 'MONDAY', 'start': time(15, 0), 'end': time(20, 0), 'duration': 20, 'max_patients': 15},
            {'day': 'TUESDAY', 'start': time(15, 0), 'end': time(20, 0), 'duration': 20, 'max_patients': 15},
            {'day': 'WEDNESDAY', 'start': time(15, 0), 'end': time(20, 0), 'duration': 20, 'max_patients': 15},
            {'day': 'THURSDAY', 'start': time(15, 0), 'end': time(20, 0), 'duration': 20, 'max_patients': 15},
            {'day': 'FRIDAY', 'start': time(15, 0), 'end': time(20, 0), 'duration': 20, 'max_patients': 15},
            {'day': 'SATURDAY', 'start': time(15, 0), 'end': time(20, 0), 'duration': 20, 'max_patients': 15},
        ]
    },
    {
        'username': 'dr_khaja_amirul',
        'schedules': [
            {'day': 'MONDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 20, 'max_patients': 24},
            {'day': 'TUESDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 20, 'max_patients': 24},
            {'day': 'WEDNESDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 20, 'max_patients': 24},
            {'day': 'THURSDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 20, 'max_patients': 24},
            {'day': 'FRIDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 20, 'max_patients': 24},
            {'day': 'SATURDAY', 'start': time(10, 0), 'end': time(18, 0), 'duration': 20, 'max_patients': 24},
        ]
    },
    {
        'username': 'dr_khalid_saifullah',
        'schedules': [
            {'day': 'THURSDAY', 'start': time(19, 0), 'end': time(21, 0), 'duration': 15, 'max_patients': 8},
        ]
    },
]

def setup_schedules():
    """Create doctor schedules in database"""
    print("\n📅 Setting up doctor schedules...\n")
    
    # Clear existing schedules
    print("🗑️  Clearing old schedules...")
    DoctorSchedule.objects.all().delete()
    
    total_created = 0
    
    for doctor_info in SCHEDULES:
        try:
            doctor = User.objects.get(username=doctor_info['username'])
            print(f"\n👨‍⚕️ Setting schedule for: ডাঃ {doctor.get_full_name()}")
            
            for schedule_data in doctor_info['schedules']:
                # Use only fields that exist in the database
                schedule = DoctorSchedule(
                    doctor=doctor,
                    day_of_week=schedule_data['day'],
                    start_time=schedule_data['start'],
                    end_time=schedule_data['end'],
                    max_patients=schedule_data['max_patients'],
                    consultation_duration=schedule_data['duration'],
                    is_active=True,
                    room_number=''
                )
                # Save without triggering auto_now_add fields
                schedule.save()
                day_display = schedule.get_day_of_week_display()
                print(f"   ✅ {day_display}: {schedule_data['start'].strftime('%I:%M %p')} - {schedule_data['end'].strftime('%I:%M %p')} ({schedule_data['max_patients']} patients max)")
                total_created += 1
                
        except User.DoesNotExist:
            print(f"   ❌ Doctor {doctor_info['username']} not found")
    
    print(f"\n✅ Created {total_created} schedule entries for {len(SCHEDULES)} doctors")
    print("\n📋 Summary:")
    print("   • ডাঃ শাকেব সুলতানা: Mon-Sat, 10 AM - 6 PM")
    print("   • ডাঃ আয়েশা ছিদ্দিকা: Every day, 3 PM - 8 PM")
    print("   • ডাঃ খাজা আমিরুল ইসলাম: Mon-Sat, 10 AM - 6 PM")
    print("   • ডাঃ এস.এম. খালিদ সাইফূল্লাহ: Thursday only, 7 PM - 9 PM")

if __name__ == '__main__':
    setup_schedules()
