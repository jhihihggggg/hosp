#!/bin/bash

#######################################################################
# Quick VPS Update Script
# Run this on VPS after pushing code changes to GitHub
#######################################################################

set -e

echo "=============================================================="
echo "🔄 UPDATING NAZIPURUHS HOSPITAL SYSTEM"
echo "=============================================================="

PROJECT_DIR="/var/www/nazipuruhs"
PROJECT_NAME="nazipuruhs"

cd $PROJECT_DIR

echo "📥 Pulling latest code from GitHub..."
git pull origin main

echo "🐍 Activating virtual environment..."
source venv/bin/activate

echo "📚 Installing/updating dependencies..."
pip install -r requirements.txt

echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔄 Restarting application..."
sudo systemctl restart $PROJECT_NAME

echo "⏳ Waiting for service to start..."
sleep 3

echo "✅ Checking service status..."
sudo systemctl status $PROJECT_NAME --no-pager

echo ""
echo "=============================================================="
echo "✅ UPDATE COMPLETE!"
echo "=============================================================="
echo ""
echo "Application is running on port 8005"
echo ""
echo "View logs: sudo journalctl -u $PROJECT_NAME -f"
echo ""
