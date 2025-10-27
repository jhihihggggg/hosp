#!/bin/bash

# Production Deployment Script for nazipuruhs.com
# Run this script on your Ubuntu VPS

set -e  # Exit on error

echo "=========================================="
echo "Hospital Management System Deployment"
echo "Domain: nazipuruhs.com"
echo "Port: 8005"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/var/www/hosp"
APP_USER="hosp"
DOMAIN="nazipuruhs.com"
PORT="8005"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${GREEN}Step 1: Installing system packages...${NC}"
apt update
apt install -y python3 python3-pip python3-venv nginx supervisor git sqlite3

echo -e "${GREEN}Step 2: Creating application user...${NC}"
if id "$APP_USER" &>/dev/null; then
    echo "User $APP_USER already exists"
else
    useradd -m -s /bin/bash $APP_USER
    echo "User $APP_USER created"
    echo "Please set password for user $APP_USER:"
    passwd $APP_USER
fi

echo -e "${GREEN}Step 3: Creating application directory...${NC}"
mkdir -p $APP_DIR
mkdir -p $APP_DIR/logs
mkdir -p $APP_DIR/data
mkdir -p $APP_DIR/media
chown -R $APP_USER:$APP_USER $APP_DIR

echo -e "${YELLOW}Step 4: Copying application files...${NC}"
echo "Please upload your application files to $APP_DIR"
echo "You can use: scp -r /path/to/hosp/* $APP_USER@your-vps-ip:$APP_DIR/"
echo "Press Enter when files are uploaded..."
read

echo -e "${GREEN}Step 5: Setting up Python virtual environment...${NC}"
su - $APP_USER -c "cd $APP_DIR && python3 -m venv venv"
su - $APP_USER -c "cd $APP_DIR && source venv/bin/activate && pip install --upgrade pip"
su - $APP_USER -c "cd $APP_DIR && source venv/bin/activate && pip install -r requirements.txt"
su - $APP_USER -c "cd $APP_DIR && source venv/bin/activate && pip install gunicorn"

echo -e "${GREEN}Step 6: Setting up database...${NC}"
su - $APP_USER -c "cd $APP_DIR && source venv/bin/activate && python manage.py makemigrations"
su - $APP_USER -c "cd $APP_DIR && source venv/bin/activate && python manage.py migrate"

echo -e "${YELLOW}Step 7: Creating Django superuser...${NC}"
echo "Please create a superuser account:"
su - $APP_USER -c "cd $APP_DIR && source venv/bin/activate && python manage.py createsuperuser"

echo -e "${GREEN}Step 8: Collecting static files...${NC}"
su - $APP_USER -c "cd $APP_DIR && source venv/bin/activate && python manage.py collectstatic --noinput"

echo -e "${GREEN}Step 9: Setting file permissions...${NC}"
chown -R $APP_USER:$APP_USER $APP_DIR
chmod -R 755 $APP_DIR
chmod 664 $APP_DIR/data/*.sqlite3 2>/dev/null || true

echo -e "${GREEN}Step 10: Configuring Supervisor...${NC}"
cp $APP_DIR/hosp_supervisor.conf /etc/supervisor/conf.d/hosp.conf
supervisorctl reread
supervisorctl update
supervisorctl start hosp

echo -e "${GREEN}Step 11: Configuring Nginx...${NC}"
cp $APP_DIR/nginx_nazipuruhs.conf /etc/nginx/sites-available/$DOMAIN
ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/

# Test nginx configuration
nginx -t

# Reload nginx
systemctl reload nginx
systemctl enable nginx

echo -e "${GREEN}Step 12: Configuring firewall...${NC}"
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow $PORT/tcp
ufw --force enable

echo -e "${GREEN}Step 13: Checking application status...${NC}"
supervisorctl status hosp
systemctl status nginx

echo ""
echo -e "${GREEN}=========================================="
echo "Deployment completed successfully!"
echo "=========================================="
echo ""
echo "Application URLs:"
echo "  - Main Site: http://$DOMAIN:$PORT"
echo "  - Admin Panel: http://$DOMAIN:$PORT/admin/"
echo "  - Public Booking: http://$DOMAIN:$PORT/public/booking/"
echo ""
echo "Management Commands:"
echo "  - Check status: sudo supervisorctl status hosp"
echo "  - Restart app: sudo supervisorctl restart hosp"
echo "  - View logs: sudo tail -f $APP_DIR/logs/gunicorn_error.log"
echo ""
echo "Next Steps:"
echo "1. Point your domain DNS A record to this server's IP"
echo "2. Wait for DNS propagation (24-48 hours)"
echo "3. Install SSL certificate: sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo "4. Create doctors and schedules via admin panel"
echo "5. Test all features"
echo ""
echo -e "${YELLOW}IMPORTANT: Update production_settings.py with:${NC}"
echo "  - SECRET_KEY (generate new one)"
echo "  - Add your VPS IP to ALLOWED_HOSTS"
echo "  - Set DEBUG = False"
echo -e "${NC}"
