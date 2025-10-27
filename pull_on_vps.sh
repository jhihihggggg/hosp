#!/bin/bash

# VPS Deployment Script - Pull from GitHub and Deploy
# Run this script on VPS to update the application

set -e

echo "================================"
echo "🚀 Deploying from GitHub..."
echo "================================"

# Configuration
APP_DIR="/var/www/nazipuruhs"
SERVICE_NAME="nazipuruhs"
BACKUP_DIR="/var/backups/nazipuruhs"

# Create backup directory if needed
mkdir -p $BACKUP_DIR

echo ""
echo "📦 Step 1: Stopping service..."
sudo systemctl stop $SERVICE_NAME || echo "Service not running"

echo ""
echo "💾 Step 2: Creating backup..."
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).tar.gz"
cd /var/www
tar -czf $BACKUP_FILE nazipuruhs/db.sqlite3 nazipuruhs/media/ 2>/dev/null || echo "Backup created"

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
echo "▶️  Step 8: Starting service..."
sudo systemctl start $SERVICE_NAME
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
