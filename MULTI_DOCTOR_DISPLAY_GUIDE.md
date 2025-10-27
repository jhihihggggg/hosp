# Multi-Doctor Display System Guide

## How It Works - All Doctors Share Same Displays! 🏥

The display monitor system is designed to show calls from **ALL DOCTORS** on **ALL DISPLAY MONITORS** throughout the hospital.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Hospital Display System                   │
└─────────────────────────────────────────────────────────────┘

Doctor 1 (Room 101)          Doctor 2 (Room 202)          Doctor 3 (Room 303)
      │                              │                              │
      │ Clicks "Call Next"           │ Clicks "Call Next"           │ Clicks "Call Next"
      │                              │                              │
      └──────────────────────────────┼──────────────────────────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │  WebSocket Broadcast   │
                        │  'display_monitor'     │
                        │  (Single Channel)      │
                        └────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
         ▼                           ▼                           ▼
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│   Display 1     │        │   Display 2     │        │   Display 3     │
│  Main Lobby     │        │  Floor 1 Wait   │        │  Floor 2 Wait   │
│                 │        │                 │        │                 │
│  Shows ALL      │        │  Shows ALL      │        │  Shows ALL      │
│  doctor calls   │        │  doctor calls   │        │  doctor calls   │
└─────────────────┘        └─────────────────┘        └─────────────────┘
```

## Real Example Scenario

### Setup:
- **Display 1**: Main lobby (login: display1)
- **Display 2**: First floor (login: display2)
- **Display 3**: Second floor (login: display3)

### Doctors:
- **Dr. Ahmed** - Room 101 - Cardiology
- **Dr. Karim** - Room 202 - General Medicine
- **Dr. Fatima** - Room 303 - Pediatrics

### What Happens:

#### 10:00 AM - Dr. Ahmed calls next patient
```
Dr. Ahmed clicks "Call Next" in Room 101
    ↓
System broadcasts to ALL displays:
    ↓
ALL 3 Displays show:
┌──────────────────────────────────┐
│       🔔 Now Calling             │
│                                  │
│     RAKIB AHMED                  │
│                                  │
│     Serial: #5                   │
│     Dr. Ahmed                    │
│     Room: 101                    │
└──────────────────────────────────┘

Audio on ALL displays (Bengali accent):
"Next patient. Serial number 5. Rakib Ahmed. Please come to room 101"
```

#### 10:02 AM - Dr. Karim calls next patient
```
Dr. Karim clicks "Call Next" in Room 202
    ↓
System broadcasts to ALL displays:
    ↓
ALL 3 Displays show:
┌──────────────────────────────────┐
│       🔔 Now Calling             │
│                                  │
│     FATEMA BEGUM                 │
│                                  │
│     Serial: #12                  │
│     Dr. Karim                    │
│     Room: 202                    │
└──────────────────────────────────┘

Audio on ALL displays (Bengali accent):
"Next patient. Serial number 12. Fatema Begum. Please come to room 202"
```

#### 10:03 AM - Dr. Fatima calls next patient
```
Dr. Fatima clicks "Call Next" in Room 303
    ↓
System broadcasts to ALL displays:
    ↓
ALL 3 Displays show:
┌──────────────────────────────────┐
│       🔔 Now Calling             │
│                                  │
│     AYESHA KHATUN                │
│                                  │
│     Serial: #8                   │
│     Dr. Fatima                   │
│     Room: 303                    │
└──────────────────────────────────┘

Audio on ALL displays (Bengali accent):
"Next patient. Serial number 8. Ayesha Khatun. Please come to room 303"
```

## Key Features

### ✅ **Centralized Broadcasting**
- All doctors share ONE broadcast channel: `'display_monitor'`
- Any doctor's call reaches ALL displays
- No need to configure per-doctor

### ✅ **Sequential Display**
- Displays show one call at a time
- Each call displays for 15 seconds
- Then returns to waiting screen
- Next call appears immediately

### ✅ **Doctor Identification**
- Patient name (large)
- Serial number
- **Doctor name** (shows which doctor is calling)
- **Room number** (tells patient where to go)

### ✅ **Audio Announcement**
- Speaks in Bengali accent
- Includes doctor name (implicit via room)
- Clear room number direction

## Setup Multiple Displays

### Create Display Users:

```bash
# Display 1 - Main Lobby
python manage.py shell -c "
from accounts.models import User
User.objects.create_user(
    username='display1',
    password='display123',
    role='DISPLAY',
    first_name='Main Lobby Display'
)
"

# Display 2 - Floor 1
python manage.py shell -c "
from accounts.models import User
User.objects.create_user(
    username='display2',
    password='display123',
    role='DISPLAY',
    first_name='Floor 1 Display'
)
"

# Display 3 - Floor 2
python manage.py shell -c "
from accounts.models import User
User.objects.create_user(
    username='display3',
    password='display123',
    role='DISPLAY',
    first_name='Floor 2 Display'
)
"
```

### Configure Each Display Device:

**Device 1** (Main Lobby TV/Monitor):
1. Open browser
2. Go to: `http://hospital-server:8000/accounts/login/`
3. Login: `display1` / `display123`
4. Press F11 for fullscreen
5. Leave running 24/7

**Device 2** (Floor 1 TV/Monitor):
1. Open browser
2. Go to: `http://hospital-server:8000/accounts/login/`
3. Login: `display2` / `display123`
4. Press F11 for fullscreen
5. Leave running 24/7

**Device 3** (Floor 2 TV/Monitor):
1. Open browser
2. Go to: `http://hospital-server:8000/accounts/login/`
3. Login: `display3` / `display123`
4. Press F11 for fullscreen
5. Leave running 24/7

## How Doctors Use It

### From Doctor Dashboard:

```
┌─────────────────────────────────────────┐
│  Dr. Ahmed's Dashboard - Room 101       │
├─────────────────────────────────────────┤
│                                         │
│  Today's Queue:                         │
│                                         │
│  ✓ #1  Kamal Hassan      (Completed)   │
│  ✓ #2  Jamila Begum      (Completed)   │
│  ✓ #3  Rubel Ahmed       (Completed)   │
│  ✓ #4  Shireen Akter     (Completed)   │
│  → #5  Rakib Ahmed       [Call Next] ← Click this
│    #6  Nasrin Sultana    (Waiting)     │
│    #7  Habib Rahman      (Waiting)     │
│                                         │
└─────────────────────────────────────────┘
```

When Dr. Ahmed clicks **[Call Next]**:
1. Rakib's status changes to "Called"
2. **ALL displays** in hospital show: "Rakib Ahmed - Room 101"
3. Audio plays on **ALL displays**
4. Next patient in queue moves up

### From Queue Display:

```
┌───────────────────────────────────────────────────┐
│           Today's Appointment Queue                │
├───────────────────────────────────────────────────┤
│  Dr. Ahmed (Room 101)           | Status          │
│  #5  Rakib Ahmed                | [Call] ← Click  │
│  #6  Nasrin Sultana             | Waiting         │
│                                                    │
│  Dr. Karim (Room 202)           | Status          │
│  #12 Fatema Begum               | [Call] ← Click  │
│  #13 Abdul Jabbar               | Waiting         │
│                                                    │
│  Dr. Fatima (Room 303)          | Status          │
│  #8  Ayesha Khatun              | [Call] ← Click  │
│  #9  Rahim Uddin                | Waiting         │
└───────────────────────────────────────────────────┘
```

Receptionist can call patients for any doctor from one screen!

## Testing Multi-Doctor Scenario

### Test Script:

```bash
# Create test appointments for multiple doctors
python manage.py shell -c "
from appointments.models import Appointment
from patients.models import Patient
from accounts.models import User
from datetime import date

# Get doctors
dr_ahmed = User.objects.filter(first_name='Ahmed', role='DOCTOR').first()
dr_karim = User.objects.filter(first_name='Karim', role='DOCTOR').first()

# Get patients
patient1 = Patient.objects.first()
patient2 = Patient.objects.last()

if dr_ahmed and dr_karim and patient1 and patient2:
    # Appointment for Dr. Ahmed
    apt1 = Appointment.objects.create(
        patient=patient1,
        doctor=dr_ahmed,
        appointment_date=date.today(),
        status='WAITING'
    )
    
    # Appointment for Dr. Karim
    apt2 = Appointment.objects.create(
        patient=patient2,
        doctor=dr_karim,
        appointment_date=date.today(),
        status='WAITING'
    )
    
    print(f'✅ Created appointments:')
    print(f'   Dr. Ahmed - Patient: {patient1.get_full_name()}')
    print(f'   Dr. Karim - Patient: {patient2.get_full_name()}')
else:
    print('❌ Need at least 2 doctors and 2 patients')
"
```

### Test Steps:

1. **Open Display Monitor**:
   - Browser 1: Login as `display1`
   - Browser 2: Login as `display2` (if you have multiple screens)

2. **Open Doctor Dashboards**:
   - Browser 3: Login as Dr. Ahmed
   - Browser 4: Login as Dr. Karim

3. **Test Calls**:
   - Dr. Ahmed clicks "Call Next"
   - **Check**: ALL displays show Dr. Ahmed's patient
   - Wait 15 seconds
   - Dr. Karim clicks "Call Next"
   - **Check**: ALL displays now show Dr. Karim's patient

4. **Verify Audio**:
   - Each call should play audio on ALL displays
   - Audio should say patient name + room number
   - Bengali accent should be used

## Troubleshooting

### Display not showing calls from some doctors?

**Check:**
1. WebSocket connection (green dot on display)
2. Django Channels is running
3. Redis is running (if using Redis backend)
4. Check browser console for errors

**Solution:**
```bash
# Restart Django with Channels support
python manage.py runserver
# or with Daphne
daphne -b 0.0.0.0 -p 8000 diagcenter.asgi:application
```

### Calls overlapping (multiple doctors calling at once)?

**This is normal!** The display shows calls sequentially:
- First call displays for 15 seconds
- If another call comes during this time, it queues
- After 15 seconds, next call displays

**To adjust timing:**
```javascript
// In display_monitor.html, line ~330
setTimeout(() => {
    // Change 15000 to desired milliseconds
    // 10000 = 10 seconds
    // 20000 = 20 seconds
}, 15000);
```

### Want to show multiple calls simultaneously?

**Option 1: Split Screen**
Modify template to show 2-4 calls in grid layout

**Option 2: Scrolling List**
Show recent calls in a scrolling list

**Option 3: Per-Doctor Displays**
Create separate WebSocket channels per doctor

## Summary

✅ **Single Broadcast Channel**: All doctors → 'display_monitor' → All displays

✅ **Automatic Distribution**: No configuration needed per doctor

✅ **Clear Identification**: Display shows which doctor + room

✅ **Bengali Accent Audio**: Works for all doctors' calls

✅ **Easy to Scale**: Add more displays by creating more display users

✅ **Receptionist Control**: Can call patients for any doctor

✅ **Doctor Control**: Each doctor calls their own patients

✅ **Real-time Updates**: Instant broadcast via WebSocket

## Production Tips

### For Large Hospitals:

**Option 1: Departmental Displays**
- Cardiology Wing: Shows only cardiology doctors
- Pediatrics Wing: Shows only pediatrics doctors
- General: Shows all doctors

**Option 2: Floor-based Displays**
- Floor 1: Shows doctors on floor 1
- Floor 2: Shows doctors on floor 2
- Lobby: Shows all doctors

**Option 3: Priority System**
- Emergency calls shown immediately
- Regular calls shown in sequence
- Different colors for different departments

### Current Implementation:
✅ **All doctors share all displays** (simplest, works for most clinics)

This is the most common setup and works perfectly for small to medium-sized hospitals where all patients can see all displays!

---

**Status**: ✅ FULLY FUNCTIONAL  
**Setup Time**: 5 minutes per display  
**Maintenance**: Zero - automatic operation  
**Scalability**: Unlimited displays, unlimited doctors
