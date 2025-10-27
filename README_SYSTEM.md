# 🏥 Multi-User Diagnostic Center Management System

A comprehensive, role-based Django management system for diagnostic centers with real-time queue management, patient records, lab tests, pharmacy, and financial tracking.

## 🎯 Features

### Multi-Role Access Control
- **Admin** - Complete system oversight, financial reports, user management
- **Doctor** - Patient queue, prescriptions, medical records
- **Receptionist** - Patient registration, appointments, billing
- **Lab Staff** - Test orders, sample collection, results entry
- **Pharmacy Staff** - Medicine sales, inventory management

### Core Modules

#### 1. Patient Management
- Patient registration with auto-generated ID
- Complete medical history tracking
- Emergency contact information
- Allergy and chronic condition records

#### 2. Appointment & Queue System
- Doctor-wise appointment scheduling
- Real-time queue display via WebSocket
- Serial number management
- Voice announcement support (pyttsx3/gTTS)
- Live monitor for waiting area

#### 3. Prescription System
- Digital prescription creation
- Medicine dosage and frequency tracking
- Print-ready prescription format
- Prescription history

#### 4. Laboratory
- Lab test catalog with pricing
- Test order management
- Sample collection tracking
- Result entry and verification
- Printable lab reports

#### 5. Pharmacy
- Drug inventory with expiry tracking
- Stock management and alerts
- Sales transactions
- Low-stock notifications
- Purchase and adjustment tracking

#### 6. Finance & Reporting
- Income tracking by source
- Expense management with approval workflow
- Investor share management
- Daily/Weekly/Monthly/Yearly reports
- Chart.js visualizations
- Department-wise financial tracking

#### 7. Survey & Feedback
- Patient satisfaction surveys
- Canteen sales tracking
- System announcements
- Feedback analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Redis (for WebSocket channels)

### Installation

1. **Clone or navigate to the project directory**
```bash
cd /workspaces/hosp
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Apply migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create superuser**
```bash
python manage.py createsuperuser
```

5. **Start Redis (for WebSocket support)**
```bash
# In a separate terminal
redis-server
```

6. **Run the development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Admin Panel: http://127.0.0.1:8000/admin/
- Login Page: http://127.0.0.1:8000/accounts/login/
- Dashboard: http://127.0.0.1:8000/accounts/dashboard/

## 📊 Database Models

### User & Authentication
- **Custom User Model** with role-based permissions
- Roles: Admin, Doctor, Receptionist, Lab, Pharmacy, Canteen

### Patient Module
- `Patient` - Patient demographics and contact info
- `PatientHistory` - Medical visit history with vitals

### Appointments Module
- `Appointment` - Queue and appointment management
- `Prescription` - Doctor prescriptions
- `Medicine` - Prescribed medications

### Lab Module
- `LabTest` - Available lab tests catalog
- `LabOrder` - Test orders from doctors
- `LabResult` - Test results and reports

### Pharmacy Module
- `Drug` - Medicine inventory
- `PharmacySale` - Sales transactions
- `SaleItem` - Individual sale items
- `StockAdjustment` - Inventory adjustments

### Finance Module
- `Income` - Revenue tracking
- `Expense` - Expense management
- `Investor` - Investor/partner information
- `InvestorPayout` - Profit distribution
- `Department` - Organizational departments
- `ConsultationFee` - Doctor fee structure

### Survey Module
- `CanteenItem` - Canteen menu items
- `CanteenSale` - Canteen transactions
- `FeedbackSurvey` - Patient feedback
- `Announcement` - System notices

## 🔌 WebSocket Endpoints

Real-time features powered by Django Channels:

- `ws/queue/<doctor_id>/` - Doctor-specific queue updates
- `ws/display-monitor/` - Public display monitor for called patients

## 🎨 Tech Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite (default) - can be changed to PostgreSQL/MySQL
- **Real-time**: Django Channels + Redis
- **API**: Django REST Framework
- **Frontend**: Bootstrap 5 (mobile-responsive)
- **Charts**: Chart.js
- **Voice**: pyttsx3 / gTTS

## 📱 API Endpoints

REST API available at `/api/` for mobile applications:
- Patient CRUD operations
- Appointment management
- Lab order tracking
- Pharmacy sales
- Authentication

## 👥 User Roles & Permissions

### Admin
- Full system access
- User management via Django admin
- Financial reports and analytics
- System configuration

### Doctor
- View personal appointment queue
- Call next patient (triggers voice + monitor update)
- Create prescriptions
- Request lab tests
- View patient history

### Receptionist
- Register new patients
- Create appointments
- Print prescriptions
- Handle billing and payments
- View queue display

### Lab Staff
- Receive test orders
- Mark samples collected
- Enter test results
- Verify and print reports

### Pharmacy Staff
- Process medicine sales
- Manage inventory
- Track stock levels
- Generate sales reports

## 📈 Reporting Features

### Admin Reports
- Day/Week/Month/Year financial summaries
- Revenue vs Expenses with charts
- Department-wise performance
- Patient statistics
- Lab activity metrics
- Pharmacy sales trends

### Export Options
- PDF reports (planned)
- Excel exports (planned)
- Print-friendly formats

## 🔐 Security Features

- Role-based access control (RBAC)
- Django's built-in authentication
- Permission decorators on views
- Session management
- CSRF protection

## 🛠️ Configuration

### Settings Highlights
```python
# diagcenter/settings.py

AUTH_USER_MODEL = 'accounts.User'
ASGI_APPLICATION = 'diagcenter.asgi.application'

# Channels for WebSocket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('127.0.0.1', 6379)]},
    },
}

# Timezone (adjust as needed)
TIME_ZONE = 'Asia/Dhaka'
```

## 📝 Development Tasks

### Create Sample Data
```bash
python manage.py shell
```

```python
from accounts.models import User
from django.contrib.auth.models import Group

# Create roles
roles = ['ADMIN', 'DOCTOR', 'RECEPTIONIST', 'LAB', 'PHARMACY']
for role in roles:
    Group.objects.get_or_create(name=role)

# Create a doctor user
doctor = User.objects.create_user(
    username='doctor1',
    password='doctor123',
    first_name='Dr. John',
    last_name='Doe',
    role='DOCTOR',
    specialization='General Medicine',
    email='doctor@example.com'
)
```

### Run Tests
```bash
python manage.py test
```

## 🚧 Future Enhancements

- [ ] SMS notifications for appointments
- [ ] Email prescription delivery
- [ ] Mobile app integration
- [ ] Payment gateway integration
- [ ] Video consultation support
- [ ] Document scanning and OCR
- [ ] Barcode/QR code for patients
- [ ] Biometric authentication
- [ ] Multi-language support
- [ ] Cloud backup integration

## 📞 Support & Documentation

For detailed API documentation and advanced features, refer to:
- Django Admin: Create users, configure settings
- API Documentation: `/api/docs/` (when implemented)
- WebSocket Events: See `appointments/consumers.py`

## 📄 License

This project is for educational and commercial use.

## 👨‍💻 Development

**Project Structure:**
```
diagcenter/
├── accounts/          # User authentication & roles
├── patients/          # Patient management
├── appointments/      # Queue & appointments
├── lab/              # Laboratory management
├── pharmacy/         # Pharmacy & inventory
├── finance/          # Financial tracking
├── survey/           # Feedback & surveys
├── diagcenter/       # Main project settings
├── templates/        # HTML templates
├── static/           # CSS, JS, images
└── media/            # Uploaded files
```

## 🎯 Getting Started for Developers

1. Set up user roles via Django admin
2. Create departments in Finance module
3. Add lab tests to the catalog
4. Stock pharmacy with medicines
5. Register test patients
6. Create sample appointments
7. Test the complete workflow

---

**Built with ❤️ using Django 5 + Bootstrap 5 + Channels**
