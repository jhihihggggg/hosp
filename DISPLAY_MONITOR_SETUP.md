# Display Monitor Setup Guide

## Overview
The Display Monitor system provides a dedicated visual and audio announcement system for patient calls. When doctors call patients, the information is displayed on screens with Bengali-accented audio announcements.

## Features

### 1. **Dedicated Display Role**
- New user role: `DISPLAY` (Display Monitor)
- Used for dedicated display devices
- Restricted access to only the display monitor page

### 2. **Visual Display**
- Large, clear patient name display
- Serial number prominently shown
- Doctor name and room number
- Animated transitions
- Auto-hide after 15 seconds
- Beautiful gradient background
- Real-time clock

### 3. **Audio Announcements**
- **Bengali Accent**: Uses Bengali/Indian English voice
- Speaks: "Next patient. Serial number [X]. [Patient Name]. Please come to room [Room Number]"
- Adjustable speech rate and pitch for clarity
- Automatic fallback if Bengali voice not available

### 4. **Real-time Updates**
- WebSocket connection for instant updates
- Connection status indicator
- Auto-reconnect on disconnection
- No page refresh needed

## Setup Instructions

### Step 1: Create Display Monitor User

Run the setup script:
```bash
python create_display_user.py
```

Or create manually using Django shell:
```python
python manage.py shell

from accounts.models import User

User.objects.create_user(
    username='display1',
    password='display123',
    role='DISPLAY',
    first_name='Main Lobby Display',
    is_active=True
)
```

### Step 2: Configure Display Device

1. **Hardware Requirements**:
   - Any computer/tablet with web browser
   - Speakers or built-in audio
   - Internet/network connection
   - Minimum 15" screen recommended

2. **Browser Setup**:
   - Use Chrome, Edge, or Firefox (best compatibility)
   - Enable JavaScript
   - Allow audio autoplay (required)
   - Set browser to start on system boot (optional)

3. **Display Configuration**:
   - Login with display user credentials
   - Navigate to: `http://your-domain/appointments/display/`
   - Press F11 for fullscreen mode
   - Adjust volume appropriately

### Step 3: Test the System

1. **Login as Doctor/Receptionist**
2. **Create a test appointment**:
   ```
   - Patient: Rakib Ahmed
   - Doctor: Dr. Karim
   - Date: Today
   - Status: Waiting
   ```

3. **Call the patient**:
   - Go to queue display or doctor dashboard
   - Click "Call Next" button
   - Display monitor should show patient info
   - Audio should announce in Bengali accent

4. **Test with keyboard** (on display page):
   - Press 'T' key to trigger test announcement
   - Verify audio and visual display work

## Bengali Accent Configuration

The system automatically selects the best Bengali/Indian voice:

### Voice Priority:
1. Bengali voices (bn-IN, bn-BD)
2. Indian English voices (en-IN)
3. Hindi/Indian accented voices
4. Default system voice with adjusted parameters

### Speech Parameters:
- **Rate**: 0.85 (slightly slower for clarity)
- **Pitch**: 1.1 (slightly higher)
- **Volume**: 1.0 (full volume)

### Browser Voice Support:
- **Chrome/Edge**: Best Bengali voice support
- **Firefox**: Good support
- **Safari**: Limited Bengali voices (uses default with adjustments)

## Usage Workflow

### For Doctors/Receptionists:
1. Login to your dashboard
2. View today's appointment queue
3. Click "Call Next" on patient's row
4. Patient info broadcasts to all display monitors
5. Audio announcement plays automatically

### For Display Monitors:
1. Login once with display credentials
2. System runs 24/7 automatically
3. Screen stays awake (wake lock)
4. Auto-reconnects if connection drops
5. Shows each call for 15 seconds

## Multiple Display Monitors

You can have multiple displays in different locations:

```bash
# Create multiple display users
python create_display_user.py  # display1 - Main Lobby
python create_display_user.py  # display2 - Waiting Area Floor 1
python create_display_user.py  # display3 - Waiting Area Floor 2
```

All displays receive the same announcements simultaneously.

## Troubleshooting

### Audio Not Playing
1. Check browser audio permissions
2. Unmute browser tab
3. Increase system volume
4. Try Chrome/Edge browser
5. Check: chrome://settings/content/sound

### No Bengali Accent
1. Install language packs on Windows:
   - Settings → Time & Language → Speech
   - Add Bengali/Hindi voices
2. On Linux: Install espeak-ng or speech-dispatcher
3. Browser may use default voice (still functional)

### Display Not Updating
1. Check connection status (top-left indicator)
2. Refresh the page (F5)
3. Check WebSocket connectivity
4. Verify Django Channels is running
5. Check: `python manage.py runserver` includes Daphne

### Screen Going to Sleep
1. Disable screensaver
2. Disable power saving mode
3. Keep browser in foreground
4. Use fullscreen mode (F11)

## Customization

### Change Display Duration
Edit `templates/appointments/display_monitor.html`:
```javascript
// Line ~280
setTimeout(() => {
    // Change 15000 to desired milliseconds (e.g., 20000 = 20 seconds)
}, 15000);
```

### Change Hospital Name
Edit template or pass via context:
```html
<div class="hospital-name">{{ hospital_name|default:"Your Hospital Name" }}</div>
```

### Adjust Voice Settings
Edit `display_monitor.html`:
```javascript
utterance.rate = 0.85;  // Speed: 0.5 (slow) to 2.0 (fast)
utterance.pitch = 1.1;  // Pitch: 0 (low) to 2 (high)
utterance.volume = 1.0; // Volume: 0 (mute) to 1 (max)
```

### Change Color Scheme
Edit CSS in template:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Change to your preferred colors */
```

## Security Considerations

1. **Display User Permissions**:
   - Can only access display monitor page
   - Cannot book appointments
   - Cannot view patient records
   - Cannot access admin panel

2. **Network Security**:
   - Use HTTPS in production
   - Use WSS (secure WebSocket)
   - Keep display users separate from staff users

3. **Physical Security**:
   - Lock down display devices
   - Disable unnecessary applications
   - Use kiosk mode if possible

## Production Deployment

### 1. Update WebSocket URL
In production, ensure HTTPS:
```javascript
const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
```

### 2. Configure Daphne/Channels
```bash
# Install channels
pip install channels channels-redis

# Configure Redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
```

### 3. Run with Daphne
```bash
daphne -b 0.0.0.0 -p 8000 diagcenter.asgi:application
```

## Testing Checklist

- [ ] Display user created successfully
- [ ] Login works on display device
- [ ] Fullscreen mode activated
- [ ] Audio permission granted
- [ ] WebSocket connected (green indicator)
- [ ] Clock shows current time
- [ ] Test announcement works (press T)
- [ ] Doctor can call patient
- [ ] Display shows patient info
- [ ] Audio announces in Bengali accent
- [ ] Display auto-hides after 15 seconds
- [ ] Multiple calls work sequentially
- [ ] Auto-reconnect works after disconnect

## Support

For issues or questions:
1. Check Django logs: `python manage.py runserver`
2. Check browser console: F12 → Console tab
3. Test WebSocket: `ws://localhost:8000/ws/display/`
4. Verify Channels is installed: `pip show channels`

## Summary

The Display Monitor system provides a professional, multilingual patient call system with:
- ✅ Bengali-accented audio announcements
- ✅ Real-time visual display
- ✅ Multiple monitor support
- ✅ Automatic updates via WebSocket
- ✅ Dedicated display user role
- ✅ Beautiful, animated interface
- ✅ Production-ready and scalable

Perfect for hospitals, clinics, and medical centers serving Bengali-speaking communities!
