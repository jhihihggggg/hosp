#!/bin/bash

echo "=============================================================="
echo "🔧 FIXING LOG FILE PERMISSIONS"
echo "=============================================================="

echo "📝 Creating and setting permissions for log files..."
sudo touch /var/log/hosp_access.log
sudo touch /var/log/hosp_error.log
sudo chown www-data:www-data /var/log/hosp_access.log
sudo chown www-data:www-data /var/log/hosp_error.log
sudo chmod 644 /var/log/hosp_access.log
sudo chmod 644 /var/log/hosp_error.log

echo "🔄 Restarting service..."
sudo systemctl restart hosp

echo "⏳ Waiting for service to start..."
sleep 3

echo ""
echo "=============================================================="
echo "✅ Service Status:"
echo "=============================================================="
sudo systemctl status hosp --no-pager

echo ""
echo "=============================================================="
echo "If running, access at: http://YOUR_IP:8005"
echo "=============================================================="
