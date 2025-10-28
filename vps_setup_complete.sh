#!/bin/bash

#######################################################################
# VPS Complete Setup Script - Nazipuruhs Hospital Management System
# This script does EVERYTHING needed to deploy on Ubuntu VPS
#######################################################################

set -e  # Exit on any error

echo "=============================================================="
echo "🏥 NAZIPURUHS HOSPITAL - VPS COMPLETE SETUP"
echo "=============================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/var/www/nazipuruhs"
PROJECT_NAME="nazipuruhs"
PORT=8005
DOMAIN="nazipuruhs.com"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Project: $PROJECT_NAME"
echo "  Directory: $PROJECT_DIR"
echo "  Port: $PORT"
echo "  Domain: $DOMAIN"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (sudo)${NC}"
    exit 1
fi

echo "=============================================================="
echo "📦 STEP 1: Installing System Dependencies"
echo "=============================================================="
apt-get update
apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    postgresql \
    postgresql-contrib \
    redis-server \
    git \
    curl \
    supervisor \
    build-essential \
    libpq-dev

echo -e "${GREEN}✅ System dependencies installed${NC}"
echo ""

echo "=============================================================="
echo "🐍 STEP 2: Setting up Python Virtual Environment"
echo "=============================================================="
cd $PROJECT_DIR

# Remove old venv if exists
if [ -d "venv" ]; then
    echo "Removing old virtual environment..."
    rm -rf venv
fi

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
echo -e "${GREEN}✅ Virtual environment created${NC}"
echo ""

echo "=============================================================="
echo "📚 STEP 3: Installing Python Dependencies"
echo "=============================================================="
pip install -r requirements.txt
echo -e "${GREEN}✅ Python packages installed${NC}"
echo ""

echo "=============================================================="
echo "🗄️  STEP 4: Database Setup"
echo "=============================================================="
echo "Running migrations..."
python manage.py migrate --noinput
echo -e "${GREEN}✅ Database migrations completed${NC}"
echo ""

echo "=============================================================="
echo "👥 STEP 5: Creating Production User Accounts"
echo "=============================================================="
echo "Creating admin, doctors, and staff accounts..."
python manage.py shell < create_production_accounts.py
echo -e "${GREEN}✅ User accounts created${NC}"
echo ""

echo "=============================================================="
echo "📁 STEP 6: Collecting Static Files"
echo "=============================================================="
python manage.py collectstatic --noinput
echo -e "${GREEN}✅ Static files collected${NC}"
echo ""

echo "=============================================================="
echo "🔧 STEP 7: Configuring Systemd Service"
echo "=============================================================="

cat > /etc/systemd/system/${PROJECT_NAME}.service << EOF
[Unit]
Description=Nazipuruhs Hospital Management System
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn diagcenter.asgi:application \\
    -k uvicorn.workers.UvicornWorker \\
    -b 0.0.0.0:$PORT \\
    --workers 4 \\
    --timeout 120 \\
    --access-logfile /var/log/${PROJECT_NAME}_access.log \\
    --error-logfile /var/log/${PROJECT_NAME}_error.log

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ${PROJECT_NAME}
echo -e "${GREEN}✅ Systemd service configured${NC}"
echo ""

echo "=============================================================="
echo "🌐 STEP 8: Configuring Nginx"
echo "=============================================================="

cat > /etc/nginx/sites-available/${PROJECT_NAME} << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    client_max_body_size 100M;
    
    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }
    
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 7d;
    }
    
    location /ws/ {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/${PROJECT_NAME} /etc/nginx/sites-enabled/

# Remove default if exists
if [ -f /etc/nginx/sites-enabled/default ]; then
    rm /etc/nginx/sites-enabled/default
fi

# Test nginx config
nginx -t

echo -e "${GREEN}✅ Nginx configured${NC}"
echo ""

echo "=============================================================="
echo "🔐 STEP 9: Setting Permissions"
echo "=============================================================="
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
chmod -R 775 $PROJECT_DIR/media 2>/dev/null || mkdir -p $PROJECT_DIR/media && chmod -R 775 $PROJECT_DIR/media
chmod -R 775 $PROJECT_DIR/staticfiles 2>/dev/null || true
echo -e "${GREEN}✅ Permissions set${NC}"
echo ""

echo "=============================================================="
echo "🚀 STEP 10: Starting Services"
echo "=============================================================="
systemctl restart redis-server
systemctl restart postgresql
systemctl restart ${PROJECT_NAME}
systemctl restart nginx

# Wait a moment for services to start
sleep 3

echo -e "${GREEN}✅ All services started${NC}"
echo ""

echo "=============================================================="
echo "🔍 STEP 11: Verifying Installation"
echo "=============================================================="

# Check service status
if systemctl is-active --quiet ${PROJECT_NAME}; then
    echo -e "${GREEN}✅ Application service is running${NC}"
else
    echo -e "${RED}❌ Application service is NOT running${NC}"
    systemctl status ${PROJECT_NAME} --no-pager
fi

if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✅ Nginx is running${NC}"
else
    echo -e "${RED}❌ Nginx is NOT running${NC}"
fi

if systemctl is-active --quiet redis-server; then
    echo -e "${GREEN}✅ Redis is running${NC}"
else
    echo -e "${RED}❌ Redis is NOT running${NC}"
fi

echo ""
echo "=============================================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=============================================================="
echo ""
echo -e "${GREEN}🎉 Your hospital management system is now live!${NC}"
echo ""
echo "Access URLs:"
echo "  - Local: http://localhost:$PORT"
echo "  - Network: http://$(hostname -I | awk '{print $1}'):$PORT"
echo "  - Domain: http://$DOMAIN (if DNS configured)"
echo ""
echo "=============================================================="
echo "🔑 LOGIN CREDENTIALS"
echo "=============================================================="
echo ""
echo "ADMIN:"
echo "  Username: 01332856000"
echo "  Password: 856000"
echo ""
echo "DOCTORS:"
echo "  Dr. Shakera: 01712765762 / 765762"
echo "  Dr. Khaja: 01761338884 / 338884"
echo "  Dr. Khalid: 01312025152 / 025152"
echo "  Dr. Ayesha: 01770928782 / 928782"
echo ""
echo "STAFF:"
echo "  Reception: 01332856002 / 856002"
echo "  Lab: 01332856005 / 856005"
echo "  Pharmacy: 01332856010 / 856010"
echo "  Canteen: 01332856015 / 856015"
echo "  Display: 01332856020 / 856020"
echo ""
echo "=============================================================="
echo "📝 USEFUL COMMANDS"
echo "=============================================================="
echo ""
echo "View application logs:"
echo "  sudo journalctl -u ${PROJECT_NAME} -f"
echo ""
echo "View nginx logs:"
echo "  sudo tail -f /var/log/nginx/error.log"
echo ""
echo "Restart application:"
echo "  sudo systemctl restart ${PROJECT_NAME}"
echo ""
echo "Check status:"
echo "  sudo systemctl status ${PROJECT_NAME}"
echo ""
echo "Update application:"
echo "  cd $PROJECT_DIR"
echo "  git pull origin main"
echo "  source venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  python manage.py migrate"
echo "  python manage.py collectstatic --noinput"
echo "  sudo systemctl restart ${PROJECT_NAME}"
echo ""
echo "=============================================================="
echo "✅ SETUP COMPLETE - ENJOY YOUR HOSPITAL SYSTEM! 🏥"
echo "=============================================================="
