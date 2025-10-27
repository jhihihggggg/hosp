#!/bin/bash

# Display Monitor Quick Setup Script
# This script helps quickly setup and test the display monitor system

echo "=========================================="
echo "Display Monitor - Quick Setup & Test"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check if display user exists
echo -e "${BLUE}Step 1: Checking display user...${NC}"
python manage.py shell -c "
from accounts.models import User
display = User.objects.filter(username='display1').first()
if display:
    print('✅ Display user exists: display1')
else:
    print('❌ Creating display user...')
    User.objects.create_user(
        username='display1',
        password='display123',
        role='DISPLAY',
        first_name='Main Lobby Display',
        is_active=True
    )
    print('✅ Display user created!')
"
echo ""

# Step 2: System check
echo -e "${BLUE}Step 2: Running system check...${NC}"
python manage.py check
echo ""

# Step 3: Create test appointment if none exist
echo -e "${BLUE}Step 3: Checking test data...${NC}"
python manage.py shell -c "
from appointments.models import Appointment
from patients.models import Patient
from accounts.models import User
from datetime import date

today = date.today()
today_appointments = Appointment.objects.filter(appointment_date=today)

if today_appointments.exists():
    print(f'✅ Found {today_appointments.count()} appointment(s) for today')
    apt = today_appointments.first()
    print(f'   Patient: {apt.patient.get_full_name()}')
    print(f'   Doctor: Dr. {apt.doctor.get_full_name()}')
    print(f'   Serial: #{apt.serial_number}')
else:
    print('⚠️  No appointments for today')
    print('   Create an appointment to test the system')
"
echo ""

# Step 4: Display URLs and credentials
echo -e "${GREEN}=========================================="
echo "✅ Setup Complete!"
echo "==========================================${NC}"
echo ""
echo -e "${YELLOW}📱 Display Monitor Access:${NC}"
echo "   URL: http://localhost:8000/accounts/login/"
echo "   Username: display1"
echo "   Password: display123"
echo ""
echo -e "${YELLOW}🖥️  After Login:${NC}"
echo "   1. Will auto-redirect to display monitor"
echo "   2. Press F11 for fullscreen"
echo "   3. Press T to test announcement"
echo "   4. Allow audio in browser"
echo ""
echo -e "${YELLOW}👨‍⚕️  To Test with Doctor:${NC}"
echo "   1. Login as doctor in another browser/tab"
echo "   2. Go to doctor dashboard"
echo "   3. Click 'Call Next Patient'"
echo "   4. Display will update with audio"
echo ""
echo -e "${YELLOW}🔧 Troubleshooting:${NC}"
echo "   - Audio not playing? Unmute browser tab"
echo "   - No updates? Check WebSocket connection (green dot)"
echo "   - No Bengali accent? Install language pack"
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "   - DISPLAY_MONITOR_SETUP.md (Full guide)"
echo "   - BENGALI_AUDIO_DISPLAY_COMPLETE.md (Implementation summary)"
echo ""
echo -e "${GREEN}Ready to go! 🚀${NC}"
