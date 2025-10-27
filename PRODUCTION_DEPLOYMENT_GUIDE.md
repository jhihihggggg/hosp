# Production Deployment Guide for nazipuruhs.com

## VPS Configuration for Ubuntu with Domain nazipuruhs.com (Port 8005)

### Prerequisites
- Ubuntu VPS with root/sudo access
- Domain: nazipuruhs.com
- Port: 8005 (avoiding conflicts with existing servers)
- Python 3.8+
- SQLite database

---

## Step 1: VPS Initial Setup

```bash
# SSH into your VPS
ssh root@your-vps-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git

# Create application user
sudo useradd -m -s /bin/bash hosp
sudo passwd hosp  # Set a password

# Create application directory
sudo mkdir -p /var/www/hosp
sudo chown hosp:hosp /var/www/hosp
```

---

## Step 2: Deploy Application

```bash
# Switch to hosp user
sudo su - hosp

# Navigate to application directory
cd /var/www/hosp

# Clone or upload your application
# Option A: Using git
git clone <your-repo-url> .

# Option B: Upload files via SCP from local machine
# From your local machine:
# scp -r /workspaces/hosp/* hosp@your-vps-ip:/var/www/hosp/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

---

## Step 3: Database Setup

```bash
# Still as hosp user in /var/www/hosp
source venv/bin/activate

# Create database directory
mkdir -p /var/www/hosp/data
chmod 755 /var/www/hosp/data

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
# Username: admin
# Email: admin@nazipuruhs.com
# Password: (set a strong password)

# Collect static files
python manage.py collectstatic --noinput

# Create media directory
mkdir -p /var/www/hosp/media
chmod 755 /var/www/hosp/media
```

---

## Step 4: Create Production Settings

The production settings file has been created at `diagcenter/production_settings.py`

Update the following in production:
- Set SECRET_KEY to a new random value
- Set ALLOWED_HOSTS = ['nazipuruhs.com', 'www.nazipuruhs.com', 'your-vps-ip']
- Configure email settings if needed
- Set DEBUG = False

---

## Step 5: Configure Gunicorn

Create Gunicorn configuration:

```bash
# As hosp user
cat > /var/www/hosp/gunicorn_config.py << 'EOF'
# See gunicorn_config.py file created
EOF
```

Test Gunicorn:
```bash
cd /var/www/hosp
source venv/bin/activate
gunicorn -c gunicorn_config.py diagcenter.wsgi:application
# Press Ctrl+C to stop after testing
```

---

## Step 6: Configure Supervisor

```bash
# Exit hosp user back to root/sudo user
exit

# Create supervisor configuration
sudo nano /etc/supervisor/conf.d/hosp.conf
# Copy content from hosp_supervisor.conf file
```

Reload supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start hosp
sudo supervisorctl status hosp
```

---

## Step 7: Configure Nginx

```bash
# Create nginx configuration
sudo nano /etc/nginx/sites-available/nazipuruhs.com
# Copy content from nginx_nazipuruhs.conf file

# Enable the site
sudo ln -s /etc/nginx/sites-available/nazipuruhs.com /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
sudo systemctl enable nginx
```

---

## Step 8: Configure Firewall

```bash
# Allow necessary ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 8005/tcp # Application port

# Enable firewall
sudo ufw enable
sudo ufw status
```

---

## Step 9: Setup SSL (Optional but Recommended)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d nazipuruhs.com -d www.nazipuruhs.com

# Certbot will automatically configure nginx for HTTPS
# Certificates auto-renew via cron
```

---

## Step 10: Create Sample Doctors in Production

```bash
# SSH into VPS as hosp user
sudo su - hosp
cd /var/www/hosp
source venv/bin/activate

# Run the doctor creation script
python create_doctors_from_signboard.py

# Or create manually via Django admin
python manage.py createsuperuser  # if not done already
# Then access: http://nazipuruhs.com/admin/
```

---

## Management Commands

### Check application status:
```bash
sudo supervisorctl status hosp
```

### Restart application:
```bash
sudo supervisorctl restart hosp
```

### View logs:
```bash
# Application logs
sudo tail -f /var/www/hosp/logs/gunicorn.log
sudo tail -f /var/www/hosp/logs/gunicorn_error.log

# Nginx logs
sudo tail -f /var/log/nginx/nazipuruhs_access.log
sudo tail -f /var/log/nginx/nazipuruhs_error.log
```

### Database backup:
```bash
# Backup database
sudo su - hosp
cd /var/www/hosp
cp data/db_production.sqlite3 data/db_backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Restore database
cp data/db_backup_YYYYMMDD_HHMMSS.sqlite3 data/db_production.sqlite3
sudo supervisorctl restart hosp
```

### Update application:
```bash
sudo su - hosp
cd /var/www/hosp
source venv/bin/activate

# Pull latest code
git pull origin main

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
exit
sudo supervisorctl restart hosp
```

---

## URLs

- Main Site: http://nazipuruhs.com:8005 (or https://nazipuruhs.com if SSL configured)
- Admin Panel: http://nazipuruhs.com:8005/admin/
- Public Booking: http://nazipuruhs.com:8005/public/booking/
- Display Monitor: http://nazipuruhs.com:8005/display/monitor/

---

## Troubleshooting

### Application won't start:
```bash
# Check supervisor logs
sudo supervisorctl tail hosp stderr

# Check if port is in use
sudo netstat -tulpn | grep 8005

# Check permissions
sudo chown -R hosp:hosp /var/www/hosp
```

### Database errors:
```bash
# Check database permissions
ls -la /var/www/hosp/data/
sudo chown hosp:hosp /var/www/hosp/data/db_production.sqlite3
sudo chmod 664 /var/www/hosp/data/db_production.sqlite3
```

### Static files not loading:
```bash
# Recollect static files
sudo su - hosp
cd /var/www/hosp
source venv/bin/activate
python manage.py collectstatic --noinput --clear
exit
sudo supervisorctl restart hosp
```

---

## Security Checklist

- [ ] Changed SECRET_KEY in production_settings.py
- [ ] Set DEBUG = False
- [ ] Configured ALLOWED_HOSTS correctly
- [ ] Created strong passwords for all admin users
- [ ] Configured firewall (ufw)
- [ ] Installed SSL certificate (optional but recommended)
- [ ] Set up regular database backups
- [ ] Restricted file permissions (chmod 600 for sensitive files)
- [ ] Disabled directory listing in nginx
- [ ] Set up fail2ban for SSH protection (optional)

---

## Next Steps After Deployment

1. Test all features:
   - Public booking system
   - Admin panel
   - Doctor dashboard
   - Display monitor
   - Audio announcements

2. Create sample data:
   - Add doctors with schedules
   - Create test appointments
   - Test prescription writing

3. Monitor:
   - Check logs regularly
   - Monitor disk space
   - Set up automated backups

4. Configure domain DNS:
   - Point nazipuruhs.com A record to VPS IP
   - Wait for DNS propagation (can take 24-48 hours)

---

## Contact & Support

For issues or questions, check logs first:
- Application: `/var/www/hosp/logs/`
- Nginx: `/var/log/nginx/`
- Supervisor: `sudo supervisorctl tail hosp`
