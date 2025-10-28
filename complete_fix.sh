#!/bin/bash

echo "=============================================================="
echo "🔧 COMPLETE FIX - Recreating Virtual Environment"
echo "=============================================================="

cd /var/www/hosp

echo "🗑️  Removing old virtual environment if exists..."
rm -rf venv

echo "🐍 Creating new virtual environment..."
python3 -m venv venv

echo "✅ Activating virtual environment..."
source venv/bin/activate

echo "📦 Upgrading pip..."
pip install --upgrade pip

echo "📚 Installing all dependencies from requirements.txt..."
pip install -r requirements.txt

echo "🗄️  Running migrations..."
python manage.py migrate --noinput

echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo "🔐 Setting correct permissions..."
sudo chown -R www-data:www-data /var/www/hosp
sudo chmod -R 755 /var/www/hosp

echo "🔄 Restarting service..."
sudo systemctl daemon-reload
sudo systemctl restart hosp

echo "⏳ Waiting for service to start..."
sleep 5

echo ""
echo "=============================================================="
echo "✅ Checking service status..."
echo "=============================================================="
sudo systemctl status hosp --no-pager

echo ""
echo "=============================================================="
echo "📋 Recent logs:"
echo "=============================================================="
sudo journalctl -u hosp -n 20 --no-pager

echo ""
echo "=============================================================="
echo "✅ FIX COMPLETE!"
echo "=============================================================="
echo ""
echo "If service is running: Access at http://YOUR_IP:8005"
echo "If still issues, check logs: sudo journalctl -u hosp -f"
echo ""
