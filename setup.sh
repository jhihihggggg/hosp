#!/bin/bash

# Multi-User Diagnostic Center Setup Script

echo "🏥 Setting up Diagnostic Center Management System..."
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create database and migrations
echo "🗄️  Creating database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Creating superuser account..."
echo "Please create an admin account:"
python manage.py createsuperuser

# Collect static files (for production)
# python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the development server, run:"
echo "   python manage.py runserver"
echo ""
echo "🔗 Access the application at:"
echo "   - Login: http://127.0.0.1:8000/accounts/login/"
echo "   - Admin: http://127.0.0.1:8000/admin/"
echo ""
echo "📝 Default user roles:"
echo "   - ADMIN: Full system access"
echo "   - DOCTOR: Patient queue and prescriptions"
echo "   - RECEPTIONIST: Patient registration and appointments"
echo "   - LAB: Laboratory test management"
echo "   - PHARMACY: Medicine sales and inventory"
echo ""
echo "💡 For WebSocket support (real-time queue), start Redis:"
echo "   redis-server"
echo ""
