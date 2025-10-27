#!/bin/bash
# Emergency fix for nazipuruhs.com service issues
# Run: sudo bash emergency_fix.sh

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== Emergency Fix for nazipuruhs.com ===${NC}"
echo ""

cd /var/www/hosp

# Fix 1: Create static directory
echo -e "${YELLOW}[1/7] Creating missing static directory...${NC}"
mkdir -p /var/www/hosp/static
mkdir -p /var/www/hosp/staticfiles
mkdir -p /var/www/hosp/data
mkdir -p /var/www/hosp/logs
mkdir -p /var/www/hosp/media
mkdir -p /var/log/nazipuruhs
echo -e "${GREEN}✓ Directories created${NC}"

# Fix 2: Check for conflicting nginx configs
echo -e "${YELLOW}[2/7] Checking nginx conflicts...${NC}"
echo "Existing nginx sites:"
ls -la /etc/nginx/sites-enabled/
echo ""

# Fix 3: Stop all potentially conflicting services
echo -e "${YELLOW}[3/7] Stopping services...${NC}"
systemctl stop nazipuruhs 2>/dev/null || true
systemctl stop hosp 2>/dev/null || true
echo -e "${GREEN}✓ Services stopped${NC}"

# Fix 4: Check if gunicorn is already running on port 8005
echo -e "${YELLOW}[4/7] Checking port 8005...${NC}"
if lsof -i :8005 >/dev/null 2>&1; then
    echo -e "${RED}Port 8005 is in use!${NC}"
    echo "Processes using port 8005:"
    lsof -i :8005
    echo ""
    echo "Killing processes..."
    lsof -ti :8005 | xargs kill -9 2>/dev/null || true
    sleep 2
    echo -e "${GREEN}✓ Port 8005 freed${NC}"
else
    echo -e "${GREEN}✓ Port 8005 is available${NC}"
fi

# Fix 5: Update service file and enable
echo -e "${YELLOW}[5/7] Setting up service...${NC}"
cp /var/www/hosp/hosp.service /etc/systemd/system/nazipuruhs.service
systemctl daemon-reload
systemctl enable nazipuruhs
echo -e "${GREEN}✓ Service configured${NC}"

# Fix 6: Set permissions
echo -e "${YELLOW}[6/7] Setting permissions...${NC}"
chown -R www-data:www-data /var/www/hosp
chown -R www-data:www-data /var/log/nazipuruhs
chmod -R 755 /var/www/hosp
echo -e "${GREEN}✓ Permissions set${NC}"

# Fix 7: Start service and check
echo -e "${YELLOW}[7/7] Starting service...${NC}"
systemctl start nazipuruhs
sleep 3

# Check status
echo ""
echo -e "${GREEN}=== Service Status ===${NC}"
if systemctl is-active --quiet nazipuruhs; then
    echo -e "${GREEN}✓ nazipuruhs service is RUNNING${NC}"
    systemctl status nazipuruhs --no-pager -l | head -20
else
    echo -e "${RED}✗ nazipuruhs service FAILED${NC}"
    echo ""
    echo "Last 30 lines of logs:"
    journalctl -u nazipuruhs -n 30 --no-pager
    exit 1
fi

# Check port
echo ""
echo -e "${GREEN}=== Port Check ===${NC}"
if netstat -tuln | grep -q ":8005 "; then
    echo -e "${GREEN}✓ Application listening on port 8005${NC}"
    netstat -tuln | grep ":8005"
else
    echo -e "${RED}✗ Port 8005 not listening${NC}"
fi

# Test connection
echo ""
echo -e "${GREEN}=== Connection Test ===${NC}"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8005 2>/dev/null || echo "000")
if [ "$HTTP_CODE" != "000" ]; then
    echo -e "${GREEN}✓ Application responds with HTTP $HTTP_CODE${NC}"
else
    echo -e "${RED}✗ Cannot connect to application${NC}"
fi

# Reload nginx
echo ""
echo -e "${YELLOW}Reloading nginx...${NC}"
nginx -t && systemctl reload nginx
echo -e "${GREEN}✓ Nginx reloaded${NC}"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Emergency Fix Complete!            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Your site: http://nazipuruhs.com${NC}"
echo ""
