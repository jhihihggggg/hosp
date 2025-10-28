#!/bin/bash

#######################################################################
# Force Update VPS - Removes cache and pulls fresh code
# Use this when git pull has conflicts with .pyc files
#######################################################################

set -e

echo "=============================================================="
echo "🔄 FORCE UPDATE - CLEANING AND PULLING FRESH CODE"
echo "=============================================================="

PROJECT_DIR="/var/www/hosp"
PROJECT_NAME="hosp"

cd $PROJECT_DIR

echo "🧹 Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

echo "🗑️  Cleaning up any uncommitted changes..."
git reset --hard HEAD
git clean -fd

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
echo "✅ FORCE UPDATE COMPLETE!"
echo "=============================================================="
echo ""
echo "Application is running on port 8005"
echo ""
