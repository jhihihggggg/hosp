#!/bin/bash

echo "=============================================================="
echo "🔍 DIAGNOSING VPS DEPLOYMENT ISSUE"
echo "=============================================================="

echo ""
echo "1️⃣ Checking service status..."
echo "=============================================================="
systemctl status hosp.service --no-pager -l

echo ""
echo "2️⃣ Checking recent error logs..."
echo "=============================================================="
journalctl -u hosp.service -n 50 --no-pager

echo ""
echo "3️⃣ Checking if gunicorn is installed..."
echo "=============================================================="
cd /var/www/hosp
source venv/bin/activate
which gunicorn
pip list | grep gunicorn

echo ""
echo "4️⃣ Testing if the app can start manually..."
echo "=============================================================="
python manage.py check --deploy

echo ""
echo "=============================================================="
echo "📝 DIAGNOSIS COMPLETE"
echo "=============================================================="
