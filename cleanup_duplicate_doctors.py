#!/usr/bin/env python
"""
Clean up duplicate doctors and keep only the 4 correct ones
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# The 4 correct doctors we want to keep
CORRECT_DOCTORS = [
    'dr_shakeb_sultana',
    'dr_ayesha_siddika',
    'dr_khaja_amirul',
    'dr_khalid_saifullah',
]

def cleanup_doctors():
    """Remove all doctors except the 4 correct ones"""
    print("\n🔍 Checking for duplicate/old doctors...\n")
    
    # Get all doctors
    all_doctors = User.objects.filter(role='DOCTOR')
    print(f"Total doctors found: {all_doctors.count()}")
    
    # List all doctors
    for doctor in all_doctors:
        status = "✅ KEEP" if doctor.username in CORRECT_DOCTORS else "❌ DELETE"
        print(f"{status} | {doctor.username} | ডাঃ {doctor.get_full_name()}")
    
    # Delete doctors not in the correct list
    doctors_to_delete = all_doctors.exclude(username__in=CORRECT_DOCTORS)
    deleted_count = doctors_to_delete.count()
    
    if deleted_count > 0:
        print(f"\n🗑️ Deleting {deleted_count} old/duplicate doctor(s)...")
        for doctor in doctors_to_delete:
            print(f"   Deleting: {doctor.username} - ডাঃ {doctor.get_full_name()}")
            doctor.delete()
        print(f"✅ Deleted {deleted_count} doctor(s)")
    else:
        print("\n✅ No duplicate doctors to delete")
    
    # Final count
    final_doctors = User.objects.filter(role='DOCTOR')
    print(f"\n📊 Final doctor count: {final_doctors.count()}")
    print("\n✅ Cleanup complete! Current doctors:")
    for doctor in final_doctors.order_by('id'):
        print(f"   • ডাঃ {doctor.get_full_name()} ({doctor.specialization})")

if __name__ == '__main__':
    cleanup_doctors()
