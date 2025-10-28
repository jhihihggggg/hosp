#!/usr/bin/env python
"""
Simple script to set easy passwords for testing
Run: python set_simple_passwords.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import User

# Set simple passwords (username as password for easy testing)
users = User.objects.all()

for user in users:
    # Set password as username for easy login
    user.set_password(user.username)
    user.save()
    print(f"✓ Set password for {user.username} (role: {user.role})")

print("\n" + "="*50)
print("Password Setup Complete!")
print("="*50)
print("\nYou can now login with:")
print("  Username: admin")
print("  Password: admin")
print("\nOr any other username with the username as password")
print("="*50)
