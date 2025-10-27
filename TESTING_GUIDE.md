# Testing Guide - Core Features

## 🚀 Quick Start Testing

### 1. Server Status
The server should be running on port 8000. Check terminal for:
```
Starting ASGI/Daphne development server at http://0.0.0.0:8000/
```

### 2. Test User Credentials
Created via `create_sample_data.py`:
- **Admin:** `admin` / `admin123`
- **Doctor:** `doctor1` / `doctor123`
- **Receptionist:** `reception1` / `reception123`

## 📋 Feature Testing Checklist

### ✅ Test 1: Login & Role-Based Redirect
1. Go to your Codespaces URL (e.g., `https://xxx-xxx-xxx.github.dev/login/`)
2. Login as `admin` / `admin123`
3. **Expected:** Redirect to Admin Dashboard (`/accounts/admin-dashboard/`)
4. Logout
5. Login as `doctor1` / `doctor123`
6. **Expected:** Redirect to Doctor Dashboard
7. Logout
8. Login as `reception1` / `reception123`
9. **Expected:** Redirect to Receptionist Dashboard

**Status:** Should work now (NoReverseMatch fixed)

---

### ✅ Test 2: Admin Dashboard - Financial Calculations

**Steps:**
1. Login as admin
2. Check default view (today's data)
3. Test period filters:
   - Click URL manually: `/accounts/admin-dashboard/?period=week`
   - Try: `?period=month`
   - Try: `?period=year`

**Expected Results:**
- Should see income, expenses, profit calculations
- Different totals for each period
- Breakdown by source (appointments, lab, pharmacy, canteen)
- List of investors (if any)
- Recent transactions

**What to Check:**
- [ ] Page loads without errors
- [ ] Period filter works (day/week/month/year)
- [ ] Financial calculations display
- [ ] Income sources breakdown shows
- [ ] Recent transactions list appears

---

### ✅ Test 3: Doctor Dashboard - Queue Display

**Steps:**
1. Login as `doctor1`
2. Check dashboard layout

**Expected to See:**
- 3 stat cards: Waiting / In Consultation / Completed
- "Call Next Patient" section (may show "No patients waiting" if no data)
- Today's appointments table (may be empty)

**What to Check:**
- [ ] Dashboard loads without errors
- [ ] Statistics cards display
- [ ] Layout is responsive
- [ ] No template errors

**Known Issue:** Will show "No patients waiting" because we haven't created test appointments yet.

---

### ✅ Test 4: Display Monitor

**Steps:**
1. Open new browser tab/window
2. Go to: `/accounts/display-monitor/`
3. **Do NOT login** (it's public or should be accessible)

**Expected:**
- Full-screen beautiful gradient display
- Header: "Diagnostic Center - Patient Queue"
- Current time display (updates every second)
- "No patients in queue" message (if no data)

**What to Check:**
- [ ] Page loads with nice gradient background
- [ ] Time updates every second
- [ ] Layout looks good on big screen
- [ ] No errors in browser console

---

### 🔴 Test 5: Call Next Patient (NEEDS DATA)

**Prerequisites:** Need to create test appointments first

**To Create Test Data:**
```python
python manage.py shell
```
```python
from accounts.models import User
from patients.models import Patient
from appointments.models import Appointment
from django.utils import timezone

# Get doctor
doctor = User.objects.get(username='doctor1')

# Create test patient
patient = Patient.objects.create(
    first_name='John',
    last_name='Doe',
    phone='1234567890',
    email='john@example.com',
    date_of_birth='1990-01-01',
    gender='M'
)

# Create appointment
appointment = Appointment.objects.create(
    patient=patient,
    doctor=doctor,
    appointment_date=timezone.now().date(),
    appointment_time=timezone.now().time(),
    status='waiting',
    room_number='Room 101'
)

print(f"Created appointment: {appointment.appointment_number}")
print(f"Serial number: {appointment.serial_number}")
```

**Then Test:**
1. Refresh doctor dashboard
2. Should see "Next Patient: John Doe (Queue #1)"
3. Click "CALL NEXT PATIENT" button
4. **Expected:**
   - Button changes to "CALLING..."
   - Success notification appears
   - Page reloads
   - Patient moves to "Current Patient" section

5. Open display monitor in another tab
6. Should see patient details appear with animation
7. **Voice announcement should play** (if browser allows)

**What to Check:**
- [ ] Button works (no JavaScript errors)
- [ ] WebSocket connection established
- [ ] Display monitor updates
- [ ] Voice plays (check browser console if not)
- [ ] Patient status changes in database

---

### ✅ Test 6: Receptionist Dashboard

**Steps:**
1. Login as `reception1`
2. View dashboard

**Expected:**
- Today's appointment count
- Recent patients list (if any)
- Prescriptions to print section (empty if none)

**What to Check:**
- [ ] Dashboard loads
- [ ] Quick action buttons present
- [ ] Layout responsive

---

### ✅ Test 7: WebSocket Connection

**How to Test:**
1. Open Browser Developer Tools (F12)
2. Go to Console tab
3. Go to display monitor page
4. Look for WebSocket connection messages

**Expected Console Messages:**
```
WebSocket connection established
Connected to ws://yoursite/ws/display/
```

**If Errors:**
- Check if Redis is running: `redis-cli ping` (should return PONG)
- Check if Daphne server is running
- Check browser console for specific error

---

## 🐛 Troubleshooting

### Issue: "No patients waiting"
**Solution:** Need to create test appointments (see Test 5)

### Issue: WebSocket fails
**Causes:**
1. Redis not running
2. Channels not configured properly
3. ASGI server not running (should use Daphne, not runserver)

**Check:**
```bash
# Check Redis
redis-cli ping

# Should see in terminal:
Daphne running on port 8000
```

### Issue: Voice doesn't play
**Causes:**
1. Browser blocks autoplay
2. Need user interaction first
3. Speech synthesis not supported

**Solutions:**
- Click anywhere on page first
- Check browser console for errors
- Try different browser (Chrome/Edge best for speech)

### Issue: CSRF errors on AJAX calls
**Check:**
- CSRF token in form: `{{ csrf_token }}`
- Header in fetch: `'X-CSRFToken': csrftoken`

### Issue: Templates not found
**Check paths:**
- Files should be in `templates/accounts/`
- Names: `admin_dashboard.html`, `doctor_dashboard.html`, etc.

---

## 📊 Sample Data Creation

### Create Complete Test Scenario

```python
python manage.py shell
```

```python
from accounts.models import User
from patients.models import Patient
from appointments.models import Appointment
from django.utils import timezone
from datetime import timedelta

doctor = User.objects.get(username='doctor1')

# Create 5 test patients with appointments
for i in range(1, 6):
    patient = Patient.objects.create(
        first_name=f'Patient',
        last_name=f'Test{i}',
        phone=f'987654321{i}',
        email=f'patient{i}@test.com',
        date_of_birth='1990-01-01',
        gender='M' if i % 2 == 0 else 'F'
    )
    
    Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        appointment_date=timezone.now().date(),
        appointment_time=(timezone.now() + timedelta(minutes=i*15)).time(),
        status='waiting',
        room_number='Room 101'
    )
    
    print(f"Created: Patient Test{i}")

print("✅ Created 5 test appointments!")
```

### Create Financial Test Data

```python
from finance.models import Income, Expense, Investor
from django.utils import timezone

# Create income records
Income.objects.create(
    date=timezone.now().date(),
    source='appointment',
    description='Consultation fees',
    amount=5000,
    payment_method='cash'
)

Income.objects.create(
    date=timezone.now().date(),
    source='lab',
    description='Lab tests',
    amount=3000,
    payment_method='card'
)

# Create expenses
Expense.objects.create(
    date=timezone.now().date(),
    category='salary',
    description='Staff salaries',
    amount=10000,
    paid_to='Staff'
)

# Create investor
Investor.objects.create(
    name='John Investor',
    investment_amount=100000,
    investment_date=timezone.now().date(),
    share_percentage=25.0
)

print("✅ Created financial test data!")
```

---

## ✅ Success Criteria

### Minimum Working Features:
- [x] All dashboards load without errors
- [x] Role-based login redirects work
- [ ] Doctor can call next patient (needs test data)
- [ ] Display monitor shows queue (needs test data)
- [ ] Voice announcement plays (needs test + browser permission)
- [x] Admin sees financial calculations
- [x] WebSocket consumers created

### Next Phase:
- [ ] Prescription printing
- [ ] Bill editing
- [ ] Mobile views
- [ ] Complete survey/canteen features

---

**Created:** October 26, 2025
**Last Updated:** October 26, 2025
**Test Status:** Ready for basic testing, needs sample data for full feature testing
