#!/bin/bash

echo "=============================================================="
echo "🔧 FIXING SERVICE - Installing Missing Dependencies"
echo "=============================================================="

cd /var/www/hosp
source venv/bin/activate

echo "📦 Installing gunicorn and uvicorn..."
pip install gunicorn==23.0.0
pip install 'uvicorn[standard]==0.34.0'
pip install whitenoise==6.8.2

echo ""
echo "🔄 Restarting service..."
sudo systemctl daemon-reload
sudo systemctl restart hosp

echo ""
echo "⏳ Waiting for service..."
sleep 3

echo ""
echo "✅ Checking service status..."
sudo systemctl status hosp --no-pager

echo ""
echo "=============================================================="
echo "If still failing, check logs with:"
echo "  sudo journalctl -u hosp -f"
echo "=============================================================="
