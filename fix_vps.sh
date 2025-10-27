#!/bin/bash

# ============================================================================
# Fix VPS Deployment Issues for nazipuruhs.com
# Run this ON THE VPS after diagnosing issues
# Usage: sudo bash fix_vps.sh
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Fix VPS Deployment - nazipuruhs.com                 ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
PROJECT_DIR="/var/www/nazipuruhs"
SERVICE_NAME="nazipuruhs"
GITHUB_REPO="https://github.com/jhihihggggg/hosp.git"
BRANCH="main"
PORT="8005"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${YELLOW}This script will:${NC}"
echo "  1. Stop existing services"
echo "  2. Clone/pull repository if needed"
echo "  3. Set up Python environment"
echo "  4. Install dependencies"
echo "  5. Run migrations and collect static files"
echo "  6. Set up systemd service"
echo "  7. Configure nginx"
echo "  8. Start services"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Step 1: Stop services
echo -e "${GREEN}[1/12]${NC} Stopping services..."
systemctl stop $SERVICE_NAME 2>/dev/null || echo "Service not running"
echo -e "${GREEN}✓ Services stopped${NC}"
echo ""

# Step 2: Install required packages
echo -e "${GREEN}[2/12]${NC} Installing system packages..."
apt-get update -qq
apt-get install -y -qq python3 python3-pip python3-venv nginx git curl netcat-traditional
echo -e "${GREEN}✓ System packages installed${NC}"
echo ""

# Step 3: Set up project directory
echo -e "${GREEN}[3/12]${NC} Setting up project directory..."
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Cloning repository..."
    mkdir -p /var/www
    git clone $GITHUB_REPO $PROJECT_DIR
    cd $PROJECT_DIR
    git checkout $BRANCH
else
    echo "Updating existing repository..."
    cd $PROJECT_DIR
    git fetch origin
    git reset --hard origin/$BRANCH
fi
echo -e "${GREEN}✓ Repository ready${NC}"
echo ""

# Step 4: Create necessary directories
echo -e "${GREEN}[4/12]${NC} Creating directories..."
mkdir -p $PROJECT_DIR/data
mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/staticfiles
mkdir -p $PROJECT_DIR/media
mkdir -p /var/log/nazipuruhs
echo -e "${GREEN}✓ Directories created${NC}"
echo ""

# Step 5: Set up Python virtual environment
echo -e "${GREEN}[5/12]${NC} Setting up Python environment..."
if [ ! -d "$PROJECT_DIR/venv" ]; then
    python3 -m venv $PROJECT_DIR/venv
fi
source $PROJECT_DIR/venv/bin/activate
pip install --quiet --upgrade pip setuptools wheel
echo -e "${GREEN}✓ Virtual environment ready${NC}"
echo ""

# Step 6: Install Python dependencies
echo -e "${GREEN}[6/12]${NC} Installing Python dependencies..."
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install --quiet -r $PROJECT_DIR/requirements.txt
else
    echo -e "${YELLOW}No requirements.txt found, installing essential packages${NC}"
    pip install --quiet django gunicorn pillow channels daphne redis channels-redis
fi
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 7: Run migrations
echo -e "${GREEN}[7/12]${NC} Running database migrations..."
cd $PROJECT_DIR
python manage.py migrate --settings=diagcenter.production_settings
echo -e "${GREEN}✓ Migrations completed${NC}"
echo ""

# Step 8: Collect static files
echo -e "${GREEN}[8/12]${NC} Collecting static files..."
python manage.py collectstatic --noinput --settings=diagcenter.production_settings
echo -e "${GREEN}✓ Static files collected${NC}"
echo ""

# Step 9: Set up systemd service
echo -e "${GREEN}[9/12]${NC} Setting up systemd service..."
if [ -f "$PROJECT_DIR/hosp.service" ]; then
    cp $PROJECT_DIR/hosp.service /etc/systemd/system/$SERVICE_NAME.service
    systemctl daemon-reload
    systemctl enable $SERVICE_NAME
    echo -e "${GREEN}✓ Service configured${NC}"
else
    echo -e "${YELLOW}Service file not found in repository, creating one...${NC}"
    cat > /etc/systemd/system/$SERVICE_NAME.service <<EOF
[Unit]
Description=Nazipuruhs Hospital Management System
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=nazipuruhs
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=diagcenter.production_settings"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \\
    --bind 0.0.0.0:$PORT \\
    --workers 4 \\
    --timeout 120 \\
    --access-logfile /var/log/nazipuruhs/access.log \\
    --error-logfile /var/log/nazipuruhs/error.log \\
    diagcenter.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
    systemctl enable $SERVICE_NAME
    echo -e "${GREEN}✓ Service file created${NC}"
fi
echo ""

# Step 10: Set up nginx configuration
echo -e "${GREEN}[10/12]${NC} Configuring nginx..."
if [ -f "$PROJECT_DIR/nginx_nazipuruhs.conf" ]; then
    cp $PROJECT_DIR/nginx_nazipuruhs.conf /etc/nginx/sites-available/nazipuruhs.com
    # Enable site if not already enabled
    if [ ! -L "/etc/nginx/sites-enabled/nazipuruhs.com" ]; then
        ln -sf /etc/nginx/sites-available/nazipuruhs.com /etc/nginx/sites-enabled/
    fi
    # Test nginx config
    nginx -t
    echo -e "${GREEN}✓ Nginx configured${NC}"
else
    echo -e "${RED}Nginx config file not found in repository${NC}"
fi
echo ""

# Step 11: Set permissions
echo -e "${GREEN}[11/12]${NC} Setting permissions..."
chown -R www-data:www-data $PROJECT_DIR
chown -R www-data:www-data /var/log/nazipuruhs
chmod -R 755 $PROJECT_DIR
chmod -R 755 /var/log/nazipuruhs
echo -e "${GREEN}✓ Permissions set${NC}"
echo ""

# Step 12: Start services
echo -e "${GREEN}[12/12]${NC} Starting services..."
systemctl start $SERVICE_NAME
systemctl reload nginx
sleep 3
echo -e "${GREEN}✓ Services started${NC}"
echo ""

# Verification
echo -e "${YELLOW}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║              Verifying Deployment                     ║${NC}"
echo -e "${YELLOW}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Check service status
echo -e "${YELLOW}Service Status:${NC}"
if systemctl is-active --quiet $SERVICE_NAME; then
    echo -e "${GREEN}✓ $SERVICE_NAME service is running${NC}"
else
    echo -e "${RED}✗ $SERVICE_NAME service is NOT running${NC}"
    echo -e "${YELLOW}Checking logs:${NC}"
    journalctl -u $SERVICE_NAME -n 20 --no-pager
fi

# Check nginx status
echo ""
echo -e "${YELLOW}Nginx Status:${NC}"
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓ Nginx is running${NC}"
else
    echo -e "${RED}✗ Nginx is NOT running${NC}"
fi

# Check port
echo ""
echo -e "${YELLOW}Port Check:${NC}"
if netstat -tuln | grep -q ":$PORT "; then
    echo -e "${GREEN}✓ Application is listening on port $PORT${NC}"
else
    echo -e "${RED}✗ Application is NOT listening on port $PORT${NC}"
fi

# Test local connection
echo ""
echo -e "${YELLOW}Testing Local Connection:${NC}"
if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT | grep -q "200\|301\|302"; then
    echo -e "${GREEN}✓ Application responds to HTTP requests${NC}"
else
    echo -e "${RED}✗ Application does not respond (check logs)${NC}"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          Deployment Fix Completed!                    ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Access your application:${NC}"
echo "  URL: http://nazipuruhs.com"
echo "  Admin: http://nazipuruhs.com/admin"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  View logs:    sudo journalctl -u $SERVICE_NAME -f"
echo "  Restart app:  sudo systemctl restart $SERVICE_NAME"
echo "  Check status: sudo systemctl status $SERVICE_NAME"
echo "  Nginx logs:   sudo tail -f /var/log/nginx/nazipuruhs_error.log"
echo ""
echo -e "${YELLOW}If domain still not working:${NC}"
echo "  1. Check DNS: Make sure nazipuruhs.com points to your VPS IP"
echo "  2. Check firewall: sudo ufw allow 80/tcp"
echo "  3. Wait for DNS propagation (can take up to 48 hours)"
echo ""
