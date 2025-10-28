#!/usr/bin/env python
"""
Quick script to create sample PC members for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import User, PCMember, PCTransaction
from decimal import Decimal

def create_sample_pc_members():
    """Create sample PC members for each type"""
    
    # Get or create admin user
    admin = User.objects.filter(role='ADMIN').first()
    if not admin:
        print("⚠️  No admin user found. Creating one...")
        admin = User.objects.create_user(
            username='admin',
            password='admin123',
            role='ADMIN',
            first_name='System',
            last_name='Admin',
            is_staff=True,
            is_superuser=True
        )
        print(f"✅ Created admin user: {admin.username}")
    
    print("\n" + "="*60)
    print("Creating Sample PC Members")
    print("="*60 + "\n")
    
    # Create General Members
    print("📝 Creating GENERAL MEMBERS (1000x)...")
    general_members = [
        {
            'name': 'Abdul Karim',
            'phone': '01712345671',
            'email': 'karim@example.com',
            'commission_percentage': Decimal('30.00'),
            'address': 'Dhaka, Bangladesh'
        },
        {
            'name': 'Fatima Begum',
            'phone': '01712345672',
            'email': 'fatima@example.com',
            'commission_percentage': Decimal('25.00'),
            'address': 'Chittagong, Bangladesh'
        },
        {
            'name': 'Rahman Ali',
            'phone': '01712345673',
            'commission_percentage': Decimal('30.00'),
        },
    ]
    
    for data in general_members:
        member, created = PCMember.objects.get_or_create(
            phone=data['phone'],
            defaults={
                'member_type': 'GENERAL',
                'name': data['name'],
                'email': data.get('email', ''),
                'commission_percentage': data['commission_percentage'],
                'address': data.get('address', ''),
                'created_by': admin,
                'is_active': True,
            }
        )
        if created:
            print(f"  ✅ {member.pc_code} - {member.name} (Commission: {member.commission_percentage}%)")
        else:
            print(f"  ℹ️  {member.pc_code} - {member.name} (Already exists)")
    
    # Create Lifetime Members
    print("\n📝 Creating LIFETIME MEMBERS (2000x)...")
    lifetime_members = [
        {
            'name': 'Dr. Hafizur Rahman',
            'phone': '01812345671',
            'email': 'hafiz@example.com',
            'commission_percentage': Decimal('35.00'),
            'address': 'Sylhet, Bangladesh'
        },
        {
            'name': 'Nazma Khatun',
            'phone': '01812345672',
            'commission_percentage': Decimal('40.00'),
        },
    ]
    
    for data in lifetime_members:
        member, created = PCMember.objects.get_or_create(
            phone=data['phone'],
            defaults={
                'member_type': 'LIFETIME',
                'name': data['name'],
                'email': data.get('email', ''),
                'commission_percentage': data['commission_percentage'],
                'address': data.get('address', ''),
                'created_by': admin,
                'is_active': True,
            }
        )
        if created:
            print(f"  ✅ {member.pc_code} - {member.name} (Commission: {member.commission_percentage}%)")
        else:
            print(f"  ℹ️  {member.pc_code} - {member.name} (Already exists)")
    
    # Create Investor Members
    print("\n📝 Creating INVESTOR MEMBERS (3000x)...")
    investor_members = [
        {
            'name': 'Kamal Investment Group',
            'phone': '01912345671',
            'email': 'kamal.invest@example.com',
            'commission_percentage': Decimal('50.00'),
            'address': 'Gulshan, Dhaka'
        },
        {
            'name': 'Rahim Enterprises',
            'phone': '01912345672',
            'commission_percentage': Decimal('45.00'),
        },
    ]
    
    for data in investor_members:
        member, created = PCMember.objects.get_or_create(
            phone=data['phone'],
            defaults={
                'member_type': 'INVESTOR',
                'name': data['name'],
                'email': data.get('email', ''),
                'commission_percentage': data['commission_percentage'],
                'address': data.get('address', ''),
                'created_by': admin,
                'is_active': True,
            }
        )
        if created:
            print(f"  ✅ {member.pc_code} - {member.name} (Commission: {member.commission_percentage}%)")
        else:
            print(f"  ℹ️  {member.pc_code} - {member.name} (Already exists)")
    
    # Create some sample transactions
    print("\n" + "="*60)
    print("Creating Sample Transactions")
    print("="*60 + "\n")
    
    # Get first member of each type
    general = PCMember.objects.filter(member_type='GENERAL').first()
    lifetime = PCMember.objects.filter(member_type='LIFETIME').first()
    investor = PCMember.objects.filter(member_type='INVESTOR').first()
    
    transactions_data = [
        (general, Decimal('5000.00')),
        (general, Decimal('3000.00')),
        (lifetime, Decimal('10000.00')),
        (investor, Decimal('25000.00')),
    ]
    
    for member, amount in transactions_data:
        if member:
            txn = PCTransaction.objects.create(
                pc_member=member,
                total_amount=amount,
                commission_percentage=member.commission_percentage,
                recorded_by=admin,
            )
            print(f"  ✅ {txn.transaction_number} - {member.name}")
            print(f"     Total: ৳{txn.total_amount} | Commission: ৳{txn.commission_amount} | Admin: ৳{txn.admin_amount}")
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    print(f"Total PC Members: {PCMember.objects.count()}")
    print(f"  - General: {PCMember.objects.filter(member_type='GENERAL').count()}")
    print(f"  - Lifetime: {PCMember.objects.filter(member_type='LIFETIME').count()}")
    print(f"  - Investor: {PCMember.objects.filter(member_type='INVESTOR').count()}")
    print(f"Total Transactions: {PCTransaction.objects.count()}")
    print(f"Total Commission: ৳{PCTransaction.objects.aggregate(total=django.db.models.Sum('commission_amount'))['total'] or 0}")
    print("\n✨ Sample PC members created successfully!")
    print("\n🔗 Access PC Dashboard: http://localhost:8000/accounts/pc-dashboard/")
    print("   Login with admin credentials to view")

if __name__ == '__main__':
    import django.db.models
    create_sample_pc_members()
