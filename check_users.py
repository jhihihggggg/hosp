#!/usr/bin/env python
"""
Quick check of all users in database
Run: python manage.py shell < check_users.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "=" * 60)
print("ALL USERS IN DATABASE")
print("=" * 60)

users = User.objects.all()
print(f"\nTotal users: {users.count()}\n")

for user in users:
    print(f"Username: {user.username}")
    print(f"  Name: {user.first_name} {user.last_name}")
    print(f"  Role: {user.role}")
    print(f"  Active: {user.is_active}")
    print(f"  Staff: {user.is_staff}")
    print(f"  Superuser: {user.is_superuser}")
    print(f"  Has usable password: {user.has_usable_password()}")
    print()

print("=" * 60)
