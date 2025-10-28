#!/bin/bash

# ============================================================================
# First-Time VPS Setup - nazipuruhs.com
# Run this ONCE on your VPS to clone the repository
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   First-Time Setup - nazipuruhs.com Hospital System  ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# Configuration
PROJECT_DIR="/var/www/hosp"
SERVICE_NAME="nazipuruhs"
BRANCH="main"

echo -e "${YELLOW}Enter your GitHub repository URL:${NC}"
echo "Example: https://github.com/YOUR_USERNAME/hosp.git"
read -p "Repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo -e "${RED}Repository URL is required!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}[1/10]${NC} Installing system dependencies..."
apt-get update -qq
apt-get install -y git python3 python3-pip python3-venv nginx supervisor > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"

echo ""
echo -e "${GREEN}[2/10]${NC} Cloning repository from GitHub..."
if [ -d "$PROJECT_DIR" ]; then
    echo -e "${YELLOW}Directory exists, removing...${NC}"
    rm -rf $PROJECT_DIR
fi

git clone -b $BRANCH $REPO_URL $PROJECT_DIR
echo -e "${GREEN}✓ Repository cloned${NC}"

echo ""
echo -e "${GREEN}[3/10]${NC} Creating virtual environment..."
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate
pip install --quiet --upgrade pip
echo -e "${GREEN}✓ Virtual environment created${NC}"

echo ""
echo -e "${GREEN}[4/10]${NC} Installing Python packages..."
if [ -f "requirements.txt" ]; then
    pip install --quiet -r requirements.txt
else
    pip install --quiet django gunicorn pillow channels daphne redis channels-redis psycopg2-binary
fi
echo -e "${GREEN}✓ Python packages installed${NC}"

echo ""
echo -e "${GREEN}[5/10]${NC} Running database migrations..."
python manage.py migrate --settings=diagcenter.production_settings
echo -e "${GREEN}✓ Migrations completed${NC}"

echo ""
echo -e "${GREEN}[6/10]${NC} Collecting static files..."
python manage.py collectstatic --noinput --settings=diagcenter.production_settings
echo -e "${GREEN}✓ Static files collected${NC}"

echo ""
echo -e "${GREEN}[7/10]${NC} Installing systemd service..."
cp hosp.service /etc/systemd/system/$SERVICE_NAME.service
mkdir -p /var/log/nazipuruhs
chown www-data:www-data /var/log/nazipuruhs
systemctl daemon-reload
systemctl enable $SERVICE_NAME
echo -e "${GREEN}✓ Service installed${NC}"

echo ""
echo -e "${GREEN}[8/10]${NC} Configuring Nginx..."
cp nginx_nazipuruhs.conf /etc/nginx/sites-available/nazipuruhs
ln -sf /etc/nginx/sites-available/nazipuruhs /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
echo -e "${GREEN}✓ Nginx configured${NC}"

echo ""
echo -e "${GREEN}[9/10]${NC} Setting permissions..."
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR
echo -e "${GREEN}✓ Permissions set${NC}"

echo ""
echo -e "${GREEN}[10/10]${NC} Starting service..."
systemctl start $SERVICE_NAME
sleep 2
echo -e "${GREEN}✓ Service started${NC}"

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          First-Time Setup Completed! ✓                ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "1. Create a superuser:"
echo -e "   ${BLUE}cd $PROJECT_DIR${NC}"
echo -e "   ${BLUE}source venv/bin/activate${NC}"
echo -e "   ${BLUE}python manage.py createsuperuser --settings=diagcenter.production_settings${NC}"
echo ""
echo "2. Install SSL certificate (optional but recommended):"
echo -e "   ${BLUE}apt-get install certbot python3-certbot-nginx${NC}"
echo -e "   ${BLUE}certbot --nginx -d nazipuruhs.com -d www.nazipuruhs.com${NC}"
echo ""
echo "3. Check service status:"
echo -e "   ${BLUE}systemctl status $SERVICE_NAME${NC}"
echo ""
echo "4. Access your site:"
echo -e "   ${BLUE}https://nazipuruhs.com${NC}"
echo ""
echo -e "${YELLOW}For future updates:${NC}"
echo "  Just run: bash pull_from_repo.sh"
echo ""
