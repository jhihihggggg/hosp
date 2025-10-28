# Authentication System - Simple & Secure

## Overview
The hospital management system now uses proper password-based authentication. All dashboard and sensitive pages require login.

## Login Credentials (Testing)

For easy testing, all users have their **username as their password**:

### Admin Access
- **Username:** `admin`
- **Password:** `admin`

### Doctor Access
- **Username:** `dr_ayesha_siddika`
- **Password:** `dr_ayesha_siddika`

- **Username:** `dr_shakeb_sultana`
- **Password:** `dr_shakeb_sultana`

- **Username:** `dr_khaja_amirul`
- **Password:** `dr_khaja_amirul`

- **Username:** `dr_khalid_saifullah`
- **Password:** `dr_khalid_saifullah`

### Receptionist Access
- **Username:** `reception1`
- **Password:** `reception1`

### Display Monitor Access
- **Username:** `display1`
- **Password:** `display1`

## How to Login

1. Navigate to: `http://localhost:8000/login/`
2. Enter your username and password
3. Click "Sign In"
4. You'll be redirected to your role-specific dashboard

## URLs

- **Login Page:** `/login/`
- **Logout:** `/logout/`
- **Dashboard:** `/accounts/dashboard/` (redirects based on role)
- **Admin Dashboard:** `/accounts/admin-dashboard/`
- **Doctor Dashboard:** `/accounts/doctor-dashboard/`
- **Receptionist Dashboard:** `/accounts/receptionist-dashboard/`
- **Lab Dashboard:** `/accounts/lab-dashboard/`
- **Pharmacy Dashboard:** `/accounts/pharmacy-dashboard/`

## Features

✅ **Password-based authentication** - Uses Django's secure password hashing
✅ **Role-based access** - Users are automatically redirected to their appropriate dashboard
✅ **Login required** - All protected pages require authentication
✅ **Secure sessions** - Uses Django's session management
✅ **No auto-login** - Removed development auto-login middleware

## Setting Custom Passwords

To change a user's password, you can:

### Option 1: Django Admin
1. Login to admin: `http://localhost:8000/admin/`
2. Go to Users
3. Click on a user
4. Use "Change password" link

### Option 2: Django Shell
```python
python manage.py shell

from accounts.models import User
user = User.objects.get(username='admin')
user.set_password('newpassword123')
user.save()
```

### Option 3: Management Command
```bash
python manage.py changepassword admin
```

## Creating New Users

```python
python manage.py shell

from accounts.models import User

# Create a new user
user = User.objects.create_user(
    username='newuser',
    password='secure_password',
    first_name='John',
    last_name='Doe',
    role='RECEPTIONIST',  # or ADMIN, DOCTOR, LAB, PHARMACY, CANTEEN
    email='john@hospital.com'
)
```

## Security Notes

- Passwords are hashed using Django's PBKDF2 algorithm
- Sessions expire after browser close (can be configured)
- CSRF protection is enabled on all forms
- Only authenticated users can access dashboards

## Production Deployment

Before deploying to production:

1. ✅ Change `SECRET_KEY` in `settings.py`
2. ✅ Set `DEBUG = False`
3. ✅ Update `ALLOWED_HOSTS`
4. ✅ Change all default passwords
5. ✅ Use strong passwords (not username=password)
6. ✅ Enable HTTPS
7. ✅ Configure proper session security settings

## Troubleshooting

### Can't login?
- Check username/password are correct
- Check if user account is active: `user.is_active = True`
- Reset password using Django admin or shell

### Redirects not working?
- Check `LOGIN_URL` in settings.py: `/login/`
- Check `LOGIN_REDIRECT_URL` in settings.py: `/accounts/dashboard/`

### Session issues?
- Clear browser cookies
- Check `django.contrib.sessions` is in `INSTALLED_APPS`
- Check `SessionMiddleware` is in `MIDDLEWARE`
