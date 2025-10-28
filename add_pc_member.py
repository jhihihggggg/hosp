#!/usr/bin/env python
"""
Direct database script to add PC members
Usage: python add_pc_member.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import PCMember

def add_pc_member():
    """Add a PC member directly to the database"""
    
    print("\n" + "="*50)
    print("ADD PC MEMBER - Direct Database Entry")
    print("="*50 + "\n")
    
    # Get member information
    print("Member Type Options:")
    print("1. General Member (30% commission)")
    print("2. Lifetime Member (35% commission)")
    print("3. Investor Member (50% commission)")
    
    choice = input("\nSelect member type (1-3): ").strip()
    
    type_map = {
        '1': ('GENERAL', 30),
        '2': ('LIFETIME', 35),
        '3': ('INVESTOR', 50)
    }
    
    if choice not in type_map:
        print("❌ Invalid choice!")
        return
    
    member_type, commission = type_map[choice]
    
    # Get member details
    name = input("Enter member name: ").strip()
    if not name:
        print("❌ Name is required!")
        return
    
    phone = input("Enter phone number: ").strip()
    if not phone:
        print("❌ Phone is required!")
        return
    
    email = input("Enter email (optional, press Enter to skip): ").strip()
    address = input("Enter address (optional, press Enter to skip): ").strip()
    
    # Create the member
    try:
        member = PCMember.objects.create(
            member_type=member_type,
            name=name,
            phone=phone,
            email=email,
            address=address,
            commission_percentage=commission
        )
        
        print("\n" + "="*50)
        print("✅ PC MEMBER CREATED SUCCESSFULLY!")
        print("="*50)
        print(f"PC Code: {member.pc_code}")
        print(f"Name: {member.name}")
        print(f"Phone: {member.phone}")
        print(f"Type: {member.get_member_type_display()}")
        print(f"Commission: {member.commission_percentage}%")
        if member.email:
            print(f"Email: {member.email}")
        if member.address:
            print(f"Address: {member.address}")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error creating member: {str(e)}\n")

def list_members():
    """List all PC members"""
    print("\n" + "="*50)
    print("ALL PC MEMBERS")
    print("="*50 + "\n")
    
    members = PCMember.objects.all().order_by('-created_at')
    
    if not members:
        print("No PC members found.\n")
        return
    
    for member in members:
        print(f"Code: {member.pc_code} | {member.name} | {member.phone}")
        print(f"Type: {member.get_member_type_display()} ({member.commission_percentage}%)")
        print(f"Total Earned: ৳{member.total_commission_earned:.2f}")
        print("-" * 50)
    
    print()

if __name__ == '__main__':
    while True:
        print("\n" + "="*50)
        print("PC MEMBER MANAGEMENT")
        print("="*50)
        print("1. Add new PC member")
        print("2. List all PC members")
        print("3. Exit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == '1':
            add_pc_member()
        elif choice == '2':
            list_members()
        elif choice == '3':
            print("\n👋 Goodbye!\n")
            break
        else:
            print("\n❌ Invalid option!\n")
