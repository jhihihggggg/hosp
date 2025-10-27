#!/bin/bash
# PASTE THIS INTO YOUR VPS TERMINAL - All in one fix

echo "=== Fixing nazipuruhs.com in one go ==="

# Step 1: Stash and pull
cd /var/www/hosp
git stash
git pull origin main

# Step 2: Create directories
mkdir -p /var/www/hosp/static /var/www/hosp/staticfiles /var/www/hosp/data /var/www/hosp/logs /var/www/hosp/media /var/log/nazipuruhs

# Step 3: Kill any process on port 8005
lsof -ti :8005 | xargs kill -9 2>/dev/null || true

# Step 4: Update service
cp /var/www/hosp/hosp.service /etc/systemd/system/nazipuruhs.service
systemctl daemon-reload
systemctl enable nazipuruhs

# Step 5: Set permissions
chown -R www-data:www-data /var/www/hosp /var/log/nazipuruhs
chmod -R 755 /var/www/hosp

# Step 6: Start service
systemctl start nazipuruhs
sleep 3

# Step 7: Check status
echo ""
echo "=== Service Status ==="
systemctl status nazipuruhs --no-pager -l | head -15

echo ""
echo "=== Port Check ==="
netstat -tuln | grep 8005

echo ""
echo "=== Test Connection ==="
curl -I http://localhost:8005 2>&1 | head -5

echo ""
echo "✓ Done! Check: http://nazipuruhs.com"
