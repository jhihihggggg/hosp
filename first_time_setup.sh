#!/bin/bash

# First Time Setup Script for VPS
# Run this once to set up the environment

set -e

APP_DIR="$(pwd)"
SERVICE_NAME="nazipuruhs"

echo "================================"
echo "🔧 First Time Setup"
echo "================================"
echo "Working directory: $APP_DIR"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate and install dependencies
echo ""
echo "📚 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "📁 Creating necessary directories..."
mkdir -p data
mkdir -p media/patient_photos
mkdir -p staticfiles
mkdir -p logs

# Fix permissions first (so Django can create database)
echo ""
echo "🔒 Setting initial permissions..."
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR
# Allow current user to also work with files
sudo chmod -R g+w $APP_DIR
sudo usermod -a -G www-data $(whoami) || true

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
sudo -u www-data $APP_DIR/venv/bin/python manage.py migrate --settings=diagcenter.production_settings --noinput

# Collect static files
echo ""
echo "📁 Collecting static files..."
sudo -u www-data $APP_DIR/venv/bin/python manage.py collectstatic --settings=diagcenter.production_settings --noinput

# Create superuser prompt
echo ""
echo "👤 Do you want to create a superuser now? (y/n)"
read -p "Create superuser? " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo -u www-data $APP_DIR/venv/bin/python manage.py createsuperuser --settings=diagcenter.production_settings
fi

# Final permissions fix
echo ""
echo "🔒 Final permissions check..."
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR
sudo chmod 664 $APP_DIR/data/db_production.sqlite3 2>/dev/null || true
sudo chmod 775 $APP_DIR/data 2>/dev/null || true

# Setup systemd service
echo ""
echo "⚙️  Setting up systemd service..."
# Update service file paths
sed -i "s|WorkingDirectory=.*|WorkingDirectory=$APP_DIR|g" $APP_DIR/hosp.service
sed -i "s|ExecStart=.*|ExecStart=$APP_DIR/venv/bin/gunicorn --config $APP_DIR/gunicorn_config.py diagcenter.wsgi:application|g" $APP_DIR/hosp.service

sudo cp $APP_DIR/hosp.service /etc/systemd/system/$SERVICE_NAME.service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo ""
echo "================================"
echo "✅ Setup Complete!"
echo "================================"
echo ""
echo "🔍 Service status:"
sudo systemctl status $SERVICE_NAME --no-pager

echo ""
echo "📊 Useful commands:"
echo "   View logs:        sudo journalctl -u $SERVICE_NAME -f"
echo "   Restart service:  sudo systemctl restart $SERVICE_NAME"
echo "   Stop service:     sudo systemctl stop $SERVICE_NAME"
echo "   Check status:     sudo systemctl status $SERVICE_NAME"
echo ""
echo "🚀 For future updates, run: bash quick_deploy.sh"
echo ""
