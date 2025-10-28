#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import PCMember

# Add sample PC members
members_data = [
    {
        'member_type': 'GENERAL',
        'name': 'Karim Ahmed',
        'phone': '01711111111',
        'email': 'karim@example.com',
        'commission_percentage': 30
    },
    {
        'member_type': 'LIFETIME',
        'name': 'Rahim Khan',
        'phone': '01722222222',
        'email': 'rahim@example.com',
        'commission_percentage': 35
    },
    {
        'member_type': 'INVESTOR',
        'name': 'Salma Begum',
        'phone': '01733333333',
        'email': 'salma@example.com',
        'commission_percentage': 50
    }
]

print("\n" + "="*60)
print("CREATING PC MEMBERS")
print("="*60 + "\n")

for data in members_data:
    try:
        member = PCMember.objects.create(**data)
        print(f"✅ Created: {member.pc_code} - {member.name} ({member.get_member_type_display()})")
    except Exception as e:
        print(f"❌ Error creating {data['name']}: {str(e)}")

print("\n" + "="*60)
print(f"Total PC Members in database: {PCMember.objects.count()}")
print("="*60 + "\n")
