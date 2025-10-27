# 🔧 Troubleshooting Guide

## Common Issues & Solutions

### 1. NoReverseMatch Error for 'login'

**Error Message:**
```
NoReverseMatch: Reverse for 'login' not found. 'login' is not a valid view function or pattern name.
```

**Solution:**
✅ FIXED - Login URL is now at root level `/login/` in `diagcenter/urls.py`

The login view is accessible at:
- Direct URL: http://localhost:8000/login/
- Also available at: http://localhost:8000/accounts/login/

---

### 2. Static Files Not Loading

**Issue:** CSS/JS not loading in templates

**Solution:**
```bash
# Create static directory
mkdir -p static/css static/js

# In production, collect static files
python manage.py collectstatic
```

**Settings Check:**
```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
```

---

### 3. WebSocket Connection Failed

**Error:** `WebSocket connection failed`

**Cause:** Redis not running

**Solution:**
```bash
# Start Redis server
redis-server

# Or install Redis first
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis                  # macOS
```

**Test Redis:**
```bash
redis-cli ping
# Should return: PONG
```

---

### 4. Template Does Not Exist

**Error:** `TemplateDoesNotExist at /some/url/`

**Cause:** Template files not created yet

**Solution:**
Most view functions are created but templates need to be built. For now:
1. Use Django Admin for data entry
2. Create templates as needed using the base template structure

**Template Structure:**
```
templates/
├── base.html                    ✅ Created
├── accounts/
│   ├── login.html              ✅ Created
│   ├── admin_dashboard.html    ✅ Created
│   └── profile.html            ✅ Created
├── patients/                    ⚠️ Needs templates
├── appointments/                ⚠️ Needs templates
└── [other apps]/                ⚠️ Needs templates
```

---

### 5. Database Locked (SQLite)

**Error:** `database is locked`

**Cause:** Multiple processes accessing SQLite

**Solution:**
```bash
# Stop all Django processes
pkill -f runserver

# Restart server
python manage.py runserver
```

For production, use PostgreSQL instead of SQLite.

---

### 6. Import Errors

**Error:** `ModuleNotFoundError: No module named 'channels'`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install missing package individually
pip install channels channels-redis daphne
```

---

### 7. Migration Issues

**Error:** `No changes detected` or migration conflicts

**Solution:**
```bash
# Reset migrations (DANGER: loses data)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
rm db.sqlite3

# Recreate everything
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

### 8. Permission Denied

**Issue:** User can't access certain pages

**Cause:** Role-based permissions

**Solution:**
1. Check user role in Django Admin
2. Verify `@login_required` decorator on views
3. Check role properties:
   - `user.is_admin`
   - `user.is_doctor`
   - `user.is_receptionist`
   - `user.is_lab_staff`
   - `user.is_pharmacy_staff`

---

### 9. Port Already in Use

**Error:** `Error: That port is already in use.`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
python manage.py runserver 8001
```

---

### 10. CSRF Token Missing

**Error:** `CSRF verification failed`

**Solution:**
Ensure templates include:
```django
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

---

## Quick Fixes Checklist

### Server Won't Start
- [ ] Check if port is available
- [ ] Verify all dependencies installed
- [ ] Check for syntax errors in Python files
- [ ] Review recent code changes

### Login Issues
- [ ] URL configuration correct
- [ ] User exists in database
- [ ] Password is correct
- [ ] User is active (`is_active=True`)

### WebSocket Not Working
- [ ] Redis is running
- [ ] Daphne is installed
- [ ] ASGI configuration correct
- [ ] Channel layers configured

### Database Errors
- [ ] Migrations applied
- [ ] Database file exists
- [ ] Permissions correct
- [ ] No locks on database

---

## Getting Help

### Check Logs
```bash
# View server output
python manage.py runserver --verbosity 3

# Check Django debug page (if DEBUG=True)
# Visit the error URL in browser
```

### Test Components

**Test Database:**
```bash
python manage.py dbshell
```

**Test Migrations:**
```bash
python manage.py showmigrations
```

**Test URLs:**
```bash
python manage.py show_urls  # if django-extensions installed
```

**Test Imports:**
```bash
python manage.py shell
>>> from accounts.models import User
>>> User.objects.count()
```

---

## Quick Start Commands

```bash
# Fresh start
python manage.py migrate
python manage.py shell < create_sample_data.py
python manage.py runserver

# Access system
# Login: http://localhost:8000/login/
# Admin: admin / admin123
```

---

## Environment Check

```bash
# Python version
python --version  # Should be 3.12+

# Django version
python -m django --version  # Should be 5.2.7

# Installed packages
pip list | grep -i django

# Redis status
redis-cli ping  # Should return PONG
```

---

## Development vs Production

### Development (Current)
- DEBUG = True
- SQLite database
- runserver
- No Redis needed (unless testing WebSocket)

### Production (To Deploy)
- DEBUG = False
- PostgreSQL database
- Gunicorn/Daphne + Nginx
- Redis required for WebSocket
- Static files collected
- HTTPS enabled

---

## Contact & Support

If issues persist:
1. Check Django error page (DEBUG=True)
2. Review server console output
3. Inspect browser console for JS errors
4. Check database with Django Admin
5. Review model definitions and relationships

**System Status:**
✅ All models created and migrated
✅ Basic views implemented
✅ Authentication working
✅ Admin panel accessible
✅ Sample data script available

**Need Templates:**
Most CRUD operations need HTML forms to be created. Use Django forms with crispy-bootstrap5 for rapid development.
