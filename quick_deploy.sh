#!/bin/bash

# Quick Deploy Script - Works from current directory
# Run this on VPS: bash quick_deploy.sh

set -e

APP_DIR="$(pwd)"
SERVICE_NAME="nazipuruhs"

echo "🚀 Quick Deploy from: $APP_DIR"
echo ""

# Pull latest code
echo "⬇️  Pulling from GitHub..."
git fetch --all
git reset --hard origin/main
git pull origin main

# Activate venv and update
echo "📚 Updating dependencies..."
source venv/bin/activate
pip install -r requirements.txt -q

# Run migrations
echo "🗄️  Running migrations..."
python manage.py migrate --settings=diagcenter.production_settings --noinput

# Collect static
echo "📁 Collecting static files..."
python manage.py collectstatic --settings=diagcenter.production_settings --noinput --clear

# Fix permissions
echo "🔒 Setting permissions..."
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR

# Setup/restart service
echo "⚙️  Setting up service..."
# Update service file paths
sed -i "s|WorkingDirectory=.*|WorkingDirectory=$APP_DIR|g" $APP_DIR/hosp.service
sed -i "s|ExecStart=.*|ExecStart=$APP_DIR/venv/bin/gunicorn --config $APP_DIR/gunicorn_config.py diagcenter.wsgi:application|g" $APP_DIR/hosp.service

sudo cp $APP_DIR/hosp.service /etc/systemd/system/$SERVICE_NAME.service
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🔍 Service status:"
sudo systemctl status $SERVICE_NAME --no-pager -l

echo ""
echo "📊 To view logs:"
echo "   sudo journalctl -u $SERVICE_NAME -f"
