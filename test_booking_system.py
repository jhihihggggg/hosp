#!/usr/bin/env python
"""
Test the booking system with a sample appointment
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import User
from appointments.models import Appointment
from patients.models import Patient
from datetime import date

print("=" * 60)
print("Testing Booking System")
print("=" * 60)

# Get all doctors
doctors = User.objects.filter(role='DOCTOR', is_active=True)
print(f"\n✅ Found {doctors.count()} doctors:")
for dr in doctors:
    print(f"   - Dr. {dr.get_full_name()} ({dr.specialization})")

# Check today's appointments
today = date.today()
print(f"\n📅 Today's date: {today}")

appointments_today = Appointment.objects.filter(appointment_date=today)
print(f"\n📋 Total appointments today: {appointments_today.count()}")

# Show appointments by doctor
for doctor in doctors:
    apts = appointments_today.filter(doctor=doctor).order_by('serial_number')
    if apts.exists():
        print(f"\n🏥 Dr. {doctor.get_full_name()}:")
        for apt in apts:
            print(f"   Serial {apt.serial_number}: {apt.patient.get_full_name()} - {apt.status}")
    else:
        print(f"\n🏥 Dr. {doctor.get_full_name()}: No appointments yet")

print("\n" + "=" * 60)
print("✅ Booking system is working!")
print("=" * 60)
print("\n📌 To book an appointment, visit:")
print("   http://localhost:8000/appointments/book/")
print("\n🔗 Or from homepage:")
print("   http://localhost:8000/")
print("=" * 60)
