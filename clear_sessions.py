#!/usr/bin/env python
"""
Clear all Django sessions - forces all users to re-login
Run: python manage.py shell < clear_sessions.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.sessions.models import Session

print("\nClearing all sessions...")
count = Session.objects.count()
Session.objects.all().delete()
print(f"✓ Deleted {count} session(s)")
print("All users will need to login again.\n")
