#!/bin/bash

# VPS Deployment Script - Pull from GitHub and Deploy
# Run this script on VPS to update the application

set -e

echo "================================"
echo "🚀 Deploying from GitHub..."
echo "================================"

# Configuration - Use current directory
APP_DIR="$(pwd)"
APP_NAME="$(basename $APP_DIR)"
SERVICE_NAME="nazipuruhs"
BACKUP_DIR="/var/backups/$APP_NAME"

# Create backup directory if needed
mkdir -p $BACKUP_DIR

echo ""
echo "📦 Step 1: Stopping service..."
if systemctl is-active --quiet $SERVICE_NAME; then
    sudo systemctl stop $SERVICE_NAME
    echo "Service stopped"
else
    echo "Service not running (will set up later)"
fi

echo ""
echo "💾 Step 2: Creating backup..."
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).tar.gz"
cd $(dirname $APP_DIR)
tar -czf $BACKUP_FILE $APP_NAME/db.sqlite3 $APP_NAME/media/ 2>/dev/null || echo "Backup created"

echo ""
echo "⬇️  Step 3: Pulling latest code from GitHub..."
cd $APP_DIR
git fetch --all
git reset --hard origin/main
git pull origin main

echo ""
echo "📚 Step 4: Installing/updating dependencies..."
source venv/bin/activate
pip install -r requirements.txt --quiet

echo ""
echo "🗄️  Step 5: Running migrations..."
python manage.py migrate --settings=diagcenter.production_settings --noinput

echo ""
echo "📁 Step 6: Collecting static files..."
python manage.py collectstatic --settings=diagcenter.production_settings --noinput --clear

echo ""
echo "🔒 Step 7: Setting permissions..."
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR

echo ""
echo "⚙️  Step 8: Setting up systemd service..."
# Update service file with current directory
sed -i "s|WorkingDirectory=.*|WorkingDirectory=$APP_DIR|g" $APP_DIR/hosp.service
sed -i "s|ExecStart=.*|ExecStart=$APP_DIR/venv/bin/gunicorn --config $APP_DIR/gunicorn_config.py diagcenter.wsgi:application|g" $APP_DIR/hosp.service

# Copy service file if not exists or update it
sudo cp $APP_DIR/hosp.service /etc/systemd/system/$SERVICE_NAME.service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

echo ""
echo "▶️  Step 9: Starting service..."
sudo systemctl start $SERVICE_NAME
sleep 2
sudo systemctl status $SERVICE_NAME --no-pager

echo ""
echo "================================"
echo "✅ Deployment Complete!"
echo "================================"
echo ""
echo "🌐 Your application is now running at:"
echo "   https://nazipuruhs.com"
echo ""
echo "📊 Check logs with:"
echo "   sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "💾 Backup saved to: $BACKUP_FILE"
echo ""
