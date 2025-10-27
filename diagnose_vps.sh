#!/bin/bash

# ============================================================================
# Diagnostic Script for nazipuruhs.com VPS Deployment Issues
# Run this ON THE VPS to diagnose why the app and domain aren't working
# Usage: sudo bash diagnose_vps.sh
# ============================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   VPS Diagnostic Tool - nazipuruhs.com               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
PROJECT_DIR="/var/www/nazipuruhs"
SERVICE_NAME="nazipuruhs"
PORT="8005"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${YELLOW}=== 1. Checking Project Directory ===${NC}"
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${GREEN}✓ Project directory exists: $PROJECT_DIR${NC}"
    ls -la $PROJECT_DIR | head -20
else
    echo -e "${RED}✗ Project directory NOT found: $PROJECT_DIR${NC}"
    echo -e "${YELLOW}You need to clone the repository first!${NC}"
fi
echo ""

echo -e "${YELLOW}=== 2. Checking Python Virtual Environment ===${NC}"
if [ -d "$PROJECT_DIR/venv" ]; then
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
    $PROJECT_DIR/venv/bin/python --version
else
    echo -e "${RED}✗ Virtual environment NOT found${NC}"
fi
echo ""

echo -e "${YELLOW}=== 3. Checking Service File ===${NC}"
if [ -f "/etc/systemd/system/$SERVICE_NAME.service" ]; then
    echo -e "${GREEN}✓ Service file exists${NC}"
    cat /etc/systemd/system/$SERVICE_NAME.service
else
    echo -e "${RED}✗ Service file NOT found: /etc/systemd/system/$SERVICE_NAME.service${NC}"
fi
echo ""

echo -e "${YELLOW}=== 4. Checking Service Status ===${NC}"
systemctl status $SERVICE_NAME --no-pager || echo -e "${RED}Service not running or not found${NC}"
echo ""

echo -e "${YELLOW}=== 5. Checking if Port $PORT is Listening ===${NC}"
if netstat -tuln | grep ":$PORT "; then
    echo -e "${GREEN}✓ Port $PORT is listening${NC}"
else
    echo -e "${RED}✗ Port $PORT is NOT listening${NC}"
fi
echo ""

echo -e "${YELLOW}=== 6. Checking Nginx Configuration ===${NC}"
if [ -f "/etc/nginx/sites-available/nazipuruhs.com" ]; then
    echo -e "${GREEN}✓ Nginx config exists${NC}"
    if [ -L "/etc/nginx/sites-enabled/nazipuruhs.com" ]; then
        echo -e "${GREEN}✓ Nginx config is enabled${NC}"
    else
        echo -e "${RED}✗ Nginx config NOT enabled${NC}"
    fi
    echo ""
    echo "Configuration content:"
    cat /etc/nginx/sites-available/nazipuruhs.com
else
    echo -e "${RED}✗ Nginx config NOT found${NC}"
fi
echo ""

echo -e "${YELLOW}=== 7. Checking Nginx Status ===${NC}"
systemctl status nginx --no-pager || echo -e "${RED}Nginx not running${NC}"
echo ""

echo -e "${YELLOW}=== 8. Testing Nginx Configuration ===${NC}"
nginx -t
echo ""

echo -e "${YELLOW}=== 9. Checking Recent Service Logs ===${NC}"
journalctl -u $SERVICE_NAME --no-pager -n 50
echo ""

echo -e "${YELLOW}=== 10. Checking Nginx Error Logs ===${NC}"
if [ -f "/var/log/nginx/nazipuruhs_error.log" ]; then
    echo "Last 20 lines of error log:"
    tail -20 /var/log/nginx/nazipuruhs_error.log
else
    echo -e "${YELLOW}No error log found${NC}"
fi
echo ""

echo -e "${YELLOW}=== 11. Checking Database ===${NC}"
if [ -f "$PROJECT_DIR/data/db_production.sqlite3" ]; then
    echo -e "${GREEN}✓ Production database exists${NC}"
    ls -lh $PROJECT_DIR/data/db_production.sqlite3
else
    echo -e "${RED}✗ Production database NOT found${NC}"
    echo "Looking for other databases:"
    find $PROJECT_DIR -name "*.sqlite3" 2>/dev/null
fi
echo ""

echo -e "${YELLOW}=== 12. Checking Static Files ===${NC}"
if [ -d "$PROJECT_DIR/staticfiles" ]; then
    echo -e "${GREEN}✓ Static files directory exists${NC}"
    du -sh $PROJECT_DIR/staticfiles
else
    echo -e "${RED}✗ Static files NOT collected${NC}"
fi
echo ""

echo -e "${YELLOW}=== 13. Checking File Permissions ===${NC}"
ls -la $PROJECT_DIR | head -10
echo ""

echo -e "${YELLOW}=== 14. DNS Check ===${NC}"
echo "Checking DNS resolution for nazipuruhs.com:"
nslookup nazipuruhs.com || echo -e "${RED}DNS resolution failed${NC}"
echo ""

echo -e "${YELLOW}=== 15. Testing Local Connection ===${NC}"
echo "Testing connection to localhost:$PORT..."
curl -I http://localhost:$PORT 2>&1 | head -10 || echo -e "${RED}Connection failed${NC}"
echo ""

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              Diagnostic Complete                      ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Summary of Issues Found:${NC}"
echo ""

# Provide recommendations based on findings
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}[CRITICAL]${NC} Project directory missing - Clone repository first"
fi

if [ ! -f "/etc/systemd/system/$SERVICE_NAME.service" ]; then
    echo -e "${RED}[CRITICAL]${NC} Service file missing - Copy hosp.service to /etc/systemd/system/$SERVICE_NAME.service"
fi

if ! systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${RED}[CRITICAL]${NC} Service not running - Check logs above for errors"
fi

if ! netstat -tuln | grep -q ":$PORT "; then
    echo -e "${RED}[CRITICAL]${NC} App not listening on port $PORT - Service may have crashed"
fi

if [ ! -f "/etc/nginx/sites-enabled/nazipuruhs.com" ]; then
    echo -e "${RED}[CRITICAL]${NC} Nginx site not enabled"
fi

if ! systemctl is-active --quiet nginx; then
    echo -e "${RED}[CRITICAL]${NC} Nginx not running"
fi

echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Fix any CRITICAL issues above"
echo "2. Run: sudo bash fix_vps.sh (if you have it)"
echo "3. Or manually fix issues one by one"
echo ""
