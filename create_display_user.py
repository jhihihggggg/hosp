#!/usr/bin/env python
"""
Script to create a display monitor user account
This account will be used on dedicated display devices
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from accounts.models import User

def create_display_user():
    """Create a display monitor user"""
    
    username = input("Enter username for display monitor (e.g., 'display1', 'display_lobby'): ").strip()
    
    if not username:
        print("Username cannot be empty!")
        return
    
    # Check if user exists
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists!")
        return
    
    password = input("Enter password (default: 'display123'): ").strip()
    if not password:
        password = 'display123'
    
    first_name = input("Enter display location (e.g., 'Main Lobby', 'Waiting Area'): ").strip()
    if not first_name:
        first_name = 'Display Monitor'
    
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            role='DISPLAY',
            first_name=first_name,
            last_name='',
            is_active=True
        )
        
        print("\n" + "="*60)
        print("✅ Display Monitor User Created Successfully!")
        print("="*60)
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Role: DISPLAY")
        print(f"Location: {first_name}")
        print("\nLogin URL: http://your-domain/accounts/login/")
        print("Display URL: http://your-domain/appointments/display/")
        print("\nIMPORTANT:")
        print("1. Login with these credentials on your display device")
        print("2. Navigate to the display monitor page")
        print("3. Make it fullscreen (F11)")
        print("4. Audio announcements will play in Bengali accent")
        print("="*60)
        
    except Exception as e:
        print(f"Error creating user: {e}")

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Display Monitor User Creation")
    print("="*60)
    print("\nThis will create a dedicated user account for display monitors.")
    print("Use this account on devices that show patient call announcements.\n")
    
    create_display_user()
