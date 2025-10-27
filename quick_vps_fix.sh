#!/bin/bash
# Quick fix for immediate VPS issue
# Run this ON VPS: sudo bash quick_vps_fix.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Quick VPS Fix for nazipuruhs.com ===${NC}"
echo ""

# Step 1: Stash local changes and pull
echo -e "${YELLOW}[1/8] Pulling latest changes...${NC}"
cd /var/www/hosp
git stash
git pull origin main
echo -e "${GREEN}✓ Code updated${NC}"
echo ""

# Step 2: Create necessary directories
echo -e "${YELLOW}[2/8] Creating directories...${NC}"
mkdir -p /var/www/hosp/data
mkdir -p /var/www/hosp/logs
mkdir -p /var/www/hosp/staticfiles
mkdir -p /var/www/hosp/media
mkdir -p /var/log/nazipuruhs
echo -e "${GREEN}✓ Directories ready${NC}"
echo ""

# Step 3: Set up venv if needed
echo -e "${YELLOW}[3/8] Checking Python environment...${NC}"
if [ ! -d "/var/www/hosp/venv" ]; then
    python3 -m venv /var/www/hosp/venv
fi
source /var/www/hosp/venv/bin/activate
pip install --quiet --upgrade pip
echo -e "${GREEN}✓ Python environment ready${NC}"
echo ""

# Step 4: Install dependencies
echo -e "${YELLOW}[4/8] Installing dependencies...${NC}"
pip install --quiet -r /var/www/hosp/requirements.txt || pip install --quiet django gunicorn pillow channels daphne
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 5: Run migrations
echo -e "${YELLOW}[5/8] Running migrations...${NC}"
cd /var/www/hosp
python manage.py migrate --settings=diagcenter.production_settings
echo -e "${GREEN}✓ Migrations done${NC}"
echo ""

# Step 6: Collect static files
echo -e "${YELLOW}[6/8] Collecting static files...${NC}"
python manage.py collectstatic --noinput --settings=diagcenter.production_settings
echo -e "${GREEN}✓ Static files collected${NC}"
echo ""

# Step 7: Update service and nginx configs
echo -e "${YELLOW}[7/8] Updating configurations...${NC}"
cp /var/www/hosp/hosp.service /etc/systemd/system/nazipuruhs.service
cp /var/www/hosp/nginx_nazipuruhs.conf /etc/nginx/sites-available/nazipuruhs.com
ln -sf /etc/nginx/sites-available/nazipuruhs.com /etc/nginx/sites-enabled/ 2>/dev/null || true
nginx -t
systemctl daemon-reload
echo -e "${GREEN}✓ Configurations updated${NC}"
echo ""

# Step 8: Set permissions and restart
echo -e "${YELLOW}[8/8] Setting permissions and restarting...${NC}"
chown -R www-data:www-data /var/www/hosp
chown -R www-data:www-data /var/log/nazipuruhs
chmod -R 755 /var/www/hosp

systemctl restart nazipuruhs
systemctl reload nginx
sleep 3
echo -e "${GREEN}✓ Services restarted${NC}"
echo ""

# Verify
echo -e "${GREEN}=== Verification ===${NC}"
if systemctl is-active --quiet nazipuruhs; then
    echo -e "${GREEN}✓ Service is running${NC}"
else
    echo -e "${RED}✗ Service failed - checking logs:${NC}"
    journalctl -u nazipuruhs -n 20 --no-pager
fi

if netstat -tuln | grep -q ":8005 "; then
    echo -e "${GREEN}✓ Port 8005 is listening${NC}"
else
    echo -e "${RED}✗ Port 8005 not listening${NC}"
fi

echo ""
echo -e "${GREEN}Done! Check: http://nazipuruhs.com${NC}"
