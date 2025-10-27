# Quick Test Script for Diagnostic Center Management System
# Run this after migrations to create sample data

from django.contrib.auth import get_user_model
from patients.models import Patient
from finance.models import Department, IncomeCategory, ExpenseCategory
from lab.models import LabTest
from pharmacy.models import DrugCategory
from datetime import date

User = get_user_model()

# Create users
print("Creating users...")
admin_user, _ = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@diagcenter.com',
        'first_name': 'System',
        'last_name': 'Administrator',
        'role': 'ADMIN',
        'is_staff': True,
        'is_superuser': True
    }
)
admin_user.set_password('admin123')
admin_user.save()
print(f"✅ Created admin user: {admin_user.username}")

doctor, _ = User.objects.get_or_create(
    username='doctor1',
    defaults={
        'email': 'doctor@diagcenter.com',
        'first_name': 'Dr. John',
        'last_name': 'Doe',
        'role': 'DOCTOR',
        'specialization': 'General Medicine',
        'license_number': 'MED12345'
    }
)
doctor.set_password('doctor123')
doctor.save()
print(f"✅ Created doctor: {doctor.username}")

receptionist, _ = User.objects.get_or_create(
    username='reception1',
    defaults={
        'email': 'reception@diagcenter.com',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'role': 'RECEPTIONIST'
    }
)
receptionist.set_password('reception123')
receptionist.save()
print(f"✅ Created receptionist: {receptionist.username}")

# Create departments
print("\nCreating departments...")
for dept_data in [
    ('CONS', 'Consultation'),
    ('LAB', 'Laboratory'),
    ('PHARM', 'Pharmacy'),
    ('CANT', 'Canteen'),
]:
    dept, created = Department.objects.get_or_create(
        code=dept_data[0],
        defaults={'name': dept_data[1]}
    )
    if created:
        print(f"✅ Created department: {dept.name}")

# Create income/expense categories
print("\nCreating categories...")
for cat in ['Consultation Fee', 'Lab Tests', 'Pharmacy Sales', 'Other']:
    IncomeCategory.objects.get_or_create(name=cat)
    
for cat in ['Salaries', 'Rent', 'Utilities', 'Supplies', 'Equipment']:
    ExpenseCategory.objects.get_or_create(name=cat)
print("✅ Created income/expense categories")

# Create sample lab tests
print("\nCreating sample lab tests...")
tests = [
    ('CBC001', 'Complete Blood Count (CBC)', 'BLOOD', 500),
    ('URINE01', 'Urine Routine Examination', 'URINE', 200),
    ('BLOOD01', 'Blood Glucose (Fasting)', 'BLOOD', 150),
    ('XRAY01', 'Chest X-Ray', 'IMAGING', 800),
]
for test_data in tests:
    test, created = LabTest.objects.get_or_create(
        test_code=test_data[0],
        defaults={
            'test_name': test_data[1],
            'category': test_data[2],
            'price': test_data[3],
            'sample_type': 'Blood' if test_data[2] == 'BLOOD' else test_data[1].split()[0],
            'turnaround_time': '24 hours'
        }
    )
    if created:
        print(f"✅ Created lab test: {test.test_name}")

# Create drug categories
print("\nCreating drug categories...")
for cat in ['Antibiotics', 'Analgesics', 'Cardiovascular', 'Diabetes', 'Vitamins']:
    DrugCategory.objects.get_or_create(name=cat)
print("✅ Created drug categories")

# Create sample patient
print("\nCreating sample patient...")
patient, created = Patient.objects.get_or_create(
    phone='01712345678',
    defaults={
        'first_name': 'Test',
        'last_name': 'Patient',
        'date_of_birth': date(1990, 1, 1),
        'gender': 'M',
        'blood_group': 'O+',
        'email': 'patient@example.com',
        'address': '123 Test Street',
        'city': 'Dhaka',
        'emergency_contact_name': 'Emergency Contact',
        'emergency_contact_phone': '01798765432',
        'emergency_contact_relation': 'Spouse',
        'registered_by': receptionist
    }
)
if created:
    print(f"✅ Created patient: {patient.get_full_name()} (ID: {patient.patient_id})")

print("\n" + "="*50)
print("🎉 Sample data created successfully!")
print("="*50)
print("\n📝 Test Credentials:")
print("-" * 50)
print("Admin:        username: admin       password: admin123")
print("Doctor:       username: doctor1     password: doctor123")
print("Receptionist: username: reception1  password: reception123")
print("-" * 50)
