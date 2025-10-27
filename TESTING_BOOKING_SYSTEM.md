# 🚀 QUICK START GUIDE - Appointment Booking System

## ✅ System is READY!

Server is running at: **http://0.0.0.0:8000/**

---

## 📋 QUICK TEST GUIDE

### 1. Test Landing Page (Public Front Page)
**URL**: `http://0.0.0.0:8000/`

**What to see**:
- Beautiful hospital website
- "Book Appointment Now" button
- "Staff Login" button
- List of available doctors
- Features section

**Action**: Click "Book Appointment Now" →

---

### 2. Test Public Booking
**URL**: `http://0.0.0.0:8000/appointments/book/`

**What to see**:
- Simple booking form
- Fields: Name, Age, Phone, Gender, Doctor
- List of available doctors below form

**Test Case 1 - New Patient**:
```
Full Name: John Doe
Age: 35
Phone: 01712345678
Gender: Male
Doctor: (Select any doctor)
Reason: Fever and cold
```
**Expected**: Success page with Serial Number

**Test Case 2 - Existing Patient (same phone)**:
```
Full Name: John Doe
Age: 35
Phone: 01712345678  ← Same phone
Gender: Male
Doctor: (Select different doctor)
```
**Expected**: Uses existing patient, new appointment

---

### 3. Test Receptionist Interface
**URL**: `http://0.0.0.0:8000/appointments/receptionist-booking/`

**Prerequisites**: You need to be logged in as staff

**Steps**:
1. Go to: `http://0.0.0.0:8000/login/`
2. Login with any staff account
3. Navigate to: `http://0.0.0.0:8000/appointments/receptionist-booking/`

**What to see**:
- Same booking form (left side)
- Today's appointments (right side)
- Grouped by doctor
- Shows serial numbers, status, time

**Test**: Book appointment for walk-in patient
- System records which receptionist created it
- Appointment appears in "Today's" list

---

## 🔐 LOGIN CREDENTIALS

### To test receptionist interface:
```
Username: (your admin/receptionist account)
Password: (your password)
```

**Don't have a receptionist account?**
Create one:
```bash
python manage.py createsuperuser
# OR use existing superuser
```

---

## 📱 TEST SCENARIOS

### Scenario 1: First Time Patient
```
Visit home → Click "Book Appointment" → Fill form → Submit
Result: New patient created, serial #1 assigned
```

### Scenario 2: Returning Patient
```
Same phone number → System finds existing patient → New appointment
Result: No duplicate patient, new serial assigned
```

### Scenario 3: Multiple Doctors
```
Dr. A: Serials 1, 2, 3
Dr. B: Serials 1, 2
(Each doctor has independent serial numbering)
```

### Scenario 4: Same Day Multiple Appointments
```
John books at 9 AM → Serial #5
John books again at 2 PM → Serial #18
(If 13 other patients booked in between)
```

---

## 🐛 TROUBLESHOOTING

### Error: "No doctors available"
**Cause**: No doctor accounts in system
**Fix**:
```bash
python manage.py shell
```
```python
from accounts.models import User
User.objects.create_user(
    username='doctor1',
    password='doctor123',
    role='DOCTOR',
    first_name='John',
    last_name='Smith',
    specialization='General Physician'
)
```

### Error: Page not found
**Check**:
- Server is running: `python manage.py runserver`
- Correct URL format
- No typos

### Success page doesn't show
**Check**:
- Form validation passed
- Doctor selected
- Phone number format correct

---

## 📊 DATABASE VERIFICATION

### Check created patients:
```bash
python manage.py shell
```
```python
from patients.models import Patient
Patient.objects.all()
# Shows all patients with phone numbers
```

### Check created appointments:
```python
from appointments.models import Appointment
Appointment.objects.filter(appointment_date='2025-10-26')
# Shows today's appointments with serial numbers
```

### Check appointments by doctor:
```python
from appointments.models import Appointment
from accounts.models import User

doctor = User.objects.filter(role='DOCTOR').first()
appointments = Appointment.objects.filter(doctor=doctor)
for apt in appointments:
    print(f"Serial: {apt.serial_number}, Patient: {apt.patient.get_full_name()}")
```

---

## ✨ FEATURES TO DEMONSTRATE

### 1. Public Booking Flow (2 minutes)
1. Open landing page
2. Click book appointment
3. Fill form
4. Show success with serial number
5. Print ticket

### 2. Receptionist Flow (2 minutes)
1. Login as receptionist
2. Open quick booking
3. Book for walk-in patient
4. Show today's appointment list
5. Highlight serial numbers

### 3. Patient Recognition (1 minute)
1. Book with phone: 01712345678
2. Book again with same phone
3. Show system recognizes patient
4. Different serial number assigned

---

## 🎯 SUCCESS CRITERIA

✅ Landing page loads without errors  
✅ Public booking works without login  
✅ Serial numbers auto-increment  
✅ Existing patients are recognized by phone  
✅ New patients are created successfully  
✅ Success page displays correct information  
✅ Receptionist can login and book  
✅ Today's appointments display correctly  
✅ Mobile responsive design works  

---

## 📞 SUPPORT INFORMATION

**If everything works**:
- System is production-ready for Priority 1 ✅
- Move to Priority 2: Prescription Writing

**If issues found**:
- Check error logs in terminal
- Verify database has doctor accounts
- Ensure all migrations are applied: `python manage.py migrate`

---

## 🚀 NEXT STEPS

**After successful testing**:

1. **Deploy to production** (if ready)
2. **Add more doctors** via admin panel
3. **Train receptionists** on the interface
4. **Promote public booking URL** to patients
5. **Implement Priority 2**: Prescription Writing & Printing

**Priority 2 Preview**:
- Doctor dashboard shows today's serials
- Call next patient button
- Prescription writing form
- Print prescription with medicines
- Link to pharmacy

---

**Testing Status**: Ready for testing ✅  
**Documentation**: Complete ✅  
**Server**: Running ✅  
**Priority 1**: IMPLEMENTED ✅
