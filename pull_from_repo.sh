#!/bin/bash

# ============================================================================
# Pull and Deploy Hospital System on VPS - nazipuruhs.com
# Run this script ON THE VPS to pull from GitHub and deploy
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Deploy Hospital System - nazipuruhs.com (Port 8005)║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
PROJECT_DIR="/var/www/nazipuruhs"
SERVICE_NAME="nazipuruhs"
BRANCH="main"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${YELLOW}Configuration:${NC}"
echo "  Project: $PROJECT_DIR"
echo "  Service: $SERVICE_NAME"
echo "  Branch: $BRANCH"
echo "  Port: 8005"
echo ""

# Step 1: Stop the service
echo -e "${GREEN}[1/8]${NC} Stopping service..."
systemctl stop $SERVICE_NAME || true
echo -e "${GREEN}✓ Service stopped${NC}"

# Step 2: Backup current installation
echo -e "${GREEN}[2/8]${NC} Creating backup..."
if [ -d "$PROJECT_DIR" ]; then
    BACKUP_DIR="/root/backups/nazipuruhs_$(date +%Y%m%d_%H%M%S)"
    mkdir -p /root/backups
    cp -r $PROJECT_DIR $BACKUP_DIR
    echo -e "${GREEN}✓ Backup created: $BACKUP_DIR${NC}"
else
    echo -e "${YELLOW}No existing installation to backup${NC}"
fi

# Step 3: Pull from GitHub
echo -e "${GREEN}[3/8]${NC} Pulling latest code from GitHub..."
if [ -d "$PROJECT_DIR/.git" ]; then
    cd $PROJECT_DIR
    git fetch origin
    git reset --hard origin/$BRANCH
    echo -e "${GREEN}✓ Code pulled from GitHub${NC}"
else
    echo -e "${RED}Error: Git repository not initialized in $PROJECT_DIR${NC}"
    echo -e "${YELLOW}First time setup required:${NC}"
    echo "  1. Clone the repository:"
    echo "     git clone https://github.com/YOUR_USERNAME/hosp.git $PROJECT_DIR"
    echo "  2. Then run this script again"
    exit 1
fi

# Step 4: Install/Update dependencies
echo -e "${GREEN}[4/8]${NC} Setting up Python environment..."
if [ ! -d "$PROJECT_DIR/venv" ]; then
    python3 -m venv $PROJECT_DIR/venv
fi

source $PROJECT_DIR/venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r $PROJECT_DIR/requirements.txt || pip install --quiet django gunicorn pillow channels daphne redis channels-redis psycopg2-binary
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Step 5: Run migrations
echo -e "${GREEN}[5/8]${NC} Running database migrations..."
cd $PROJECT_DIR
python manage.py migrate --settings=diagcenter.production_settings
echo -e "${GREEN}✓ Migrations completed${NC}"

# Step 6: Collect static files
echo -e "${GREEN}[6/8]${NC} Collecting static files..."
python manage.py collectstatic --noinput --settings=diagcenter.production_settings
echo -e "${GREEN}✓ Static files collected${NC}"

# Step 7: Set permissions
echo -e "${GREEN}[7/8]${NC} Setting permissions..."
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
echo -e "${GREEN}✓ Permissions set${NC}"

# Step 8: Start the service
echo -e "${GREEN}[8/8]${NC} Starting service..."
systemctl daemon-reload
systemctl start $SERVICE_NAME
systemctl reload nginx
sleep 2
echo -e "${GREEN}✓ Service started${NC}"

# Verify service is running
echo ""
echo -e "${YELLOW}Checking service status...${NC}"
if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✓ Service is running${NC}"
else
    echo -e "${RED}✗ Service failed to start${NC}"
    echo -e "${YELLOW}Check logs with: journalctl -u $SERVICE_NAME -xe${NC}"
    exit 1
fi

# Check if port is listening
if netstat -tuln | grep -q ":8005 "; then
    echo -e "${GREEN}✓ Port 8005 is listening${NC}"
else
    echo -e "${RED}✗ Port 8005 is not listening${NC}"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          Deployment Completed Successfully!           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Access your hospital system:${NC}"
echo "  URL: https://nazipuruhs.com"
echo "  Admin: https://nazipuruhs.com/admin"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  Status:  systemctl status $SERVICE_NAME"
echo "  Logs:    journalctl -u $SERVICE_NAME -f"
echo "  Restart: systemctl restart $SERVICE_NAME"
echo ""
