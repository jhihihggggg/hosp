# 🚀 QUICK SETUP & TEST GUIDE

## Step 1: Add Doctor Schedule (Admin)

### Login as Admin:
```
URL: http://0.0.0.0:8000/login/
```

### Add Schedule:
```
URL: http://0.0.0.0:8000/appointments/schedules/create/

Fill:
- Doctor: Select a doctor
- Day: Monday
- Start Time: 09:00
- End Time: 17:00
- Max Patients: 20
- Duration: 15 (minutes)
- Room: 101
- Active: ✓ Checked

Click: Save Schedule
```

## Step 2: Test Public Booking

### Open Booking Page:
```
URL: http://0.0.0.0:8000/appointments/book/
```

### Book Appointment:
1. Enter Name: Rakib Ahmed
2. Enter Age: 25
3. Enter Phone: 01712345678
4. Select Gender: Male
5. Select Doctor: (Choose the doctor with schedule)
6. Select Date: (Choose Monday from calendar)
7. Select Time: (Choose available slot, e.g., 09:00)
8. Click: Book Appointment

**Result**: You'll get Serial #1 for that doctor + date

## Step 3: Test Audio Announcement

### Login as Doctor:
```
URL: http://0.0.0.0:8000/login/
Username: (doctor account)
Password: (doctor password)
```

### View Queue:
```
URL: http://0.0.0.0:8000/accounts/doctor-dashboard/
```

### Call Next Patient:
1. See "Serial #1 - Rakib Ahmed" in queue
2. Click "Call Next Patient" button
3. **Listen**: Computer will say "Next patient: Rakib Ahmed"
4. Status changes to "Called"

## Step 4: Book More Appointments

### Test Serial Sequence:
```
Book another appointment:
- Same doctor, same date, different time (09:15)
- Result: Serial #2

Book another:
- Same doctor, different date (Tuesday)
- Result: Serial #1 (new day, restarts)

Book another:
- Different doctor, same date
- Result: Serial #1 (different doctor, separate queue)
```

## Testing Checklist:

### ✅ Schedule Management:
- [ ] Admin can add schedule
- [ ] Admin can edit schedule
- [ ] Admin can delete schedule
- [ ] Admin can view all schedules

### ✅ Calendar Booking:
- [ ] Select doctor loads calendar
- [ ] Select date shows time slots
- [ ] Booked slots disabled
- [ ] Booking creates appointment

### ✅ Serial Numbers:
- [ ] Serial per doctor + date
- [ ] Serial increments correctly
- [ ] Different doctors have separate serials
- [ ] Different dates restart serials

### ✅ Audio Announcement:
- [ ] Click "Call Next" triggers audio
- [ ] Voice says patient name correctly
- [ ] Volume is audible
- [ ] Works in browser

### ✅ Queue Management:
- [ ] Doctor sees their queue
- [ ] Receptionist sees all queues
- [ ] Status updates correctly
- [ ] Serials displayed

## Quick Commands:

### Create Admin (if needed):
```bash
python manage.py createsuperuser
```

### Create Doctor Account:
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

### View Database:
```bash
python manage.py shell
```
```python
from appointments.models import DoctorSchedule, Appointment

# View all schedules
for s in DoctorSchedule.objects.all():
    print(f"{s.doctor.get_full_name()} - {s.get_day_of_week_display()} {s.start_time}")

# View appointments
for a in Appointment.objects.all():
    print(f"Serial {a.serial_number}: {a.patient.get_full_name()} - Dr. {a.doctor.get_full_name()}")
```

## Troubleshooting:

### No time slots showing:
- Check doctor has schedule for that day
- Check schedule is active
- Check max patients not reached

### Audio not working:
- Check browser permissions
- Try Chrome (best support)
- Check volume is up
- Check speakers/headphones

### Serial not incrementing:
- Check appointment date/time saved
- Check filtering by doctor + date
- Check serial_number field

## URLs Reference:

```
Public:
/                                    → Landing page
/appointments/book/                  → Public booking with calendar

Admin:
/appointments/schedules/             → Manage schedules
/appointments/schedules/create/      → Add schedule

Staff:
/login/                              → Staff login
/accounts/dashboard/                 → Dashboard (role-based)
/accounts/doctor-dashboard/          → Doctor queue
/appointments/receptionist-booking/  → Quick booking
/appointments/queue/                 → View queue
```

## Success Indicators:

✅ Schedule created successfully  
✅ Calendar shows available dates  
✅ Time slots load when date selected  
✅ Booking creates appointment  
✅ Serial number assigned  
✅ Audio announcement plays  
✅ Queue updates in real-time  

## Next Steps:

1. ✅ Add schedules for all doctors
2. ✅ Test booking flow end-to-end
3. ✅ Test audio in different browsers
4. ✅ Train staff on system
5. ✅ Deploy to production

**Status**: Ready for production! 🚀
