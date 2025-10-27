# Quick VPS Deployment Commands for nazipuruhs.com

## 📋 Pre-Deployment Checklist

- [ ] VPS running Ubuntu 20.04 or later
- [ ] Root or sudo access
- [ ] Domain nazipuruhs.com pointing to VPS IP
- [ ] Port 8005 available (other servers on different ports)
- [ ] At least 2GB RAM, 20GB storage

---

## 🚀 One-Command Deployment

```bash
# On your LOCAL machine - Upload files to VPS
cd /workspaces/hosp
scp -r * root@YOUR_VPS_IP:/tmp/hosp_deploy/

# On VPS - Run deployment
ssh root@YOUR_VPS_IP
mv /tmp/hosp_deploy /var/www/hosp
cd /var/www/hosp
chmod +x deploy_production.sh
./deploy_production.sh
```

---

## 🔧 Manual Step-by-Step Deployment

### 1. Upload Files to VPS

```bash
# From your local machine
cd /workspaces/hosp
tar -czf hosp.tar.gz .
scp hosp.tar.gz root@YOUR_VPS_IP:/tmp/

# On VPS
ssh root@YOUR_VPS_IP
mkdir -p /var/www/hosp
cd /var/www/hosp
tar -xzf /tmp/hosp.tar.gz
```

### 2. Install Dependencies

```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv nginx supervisor git sqlite3
```

### 3. Create Application User

```bash
useradd -m -s /bin/bash hosp
passwd hosp
chown -R hosp:hosp /var/www/hosp
```

### 4. Setup Python Environment

```bash
su - hosp
cd /var/www/hosp
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### 5. Setup Database

```bash
# Still as hosp user
mkdir -p /var/www/hosp/data /var/www/hosp/logs /var/www/hosp/media
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 6. Create Doctors

```bash
# Still as hosp user
python create_production_doctors.py
```

### 7. Configure Supervisor

```bash
# Exit to root user
exit

# Copy supervisor config
cp /var/www/hosp/hosp_supervisor.conf /etc/supervisor/conf.d/hosp.conf
supervisorctl reread
supervisorctl update
supervisorctl start hosp
supervisorctl status hosp
```

### 8. Configure Nginx

```bash
# As root
cp /var/www/hosp/nginx_nazipuruhs.conf /etc/nginx/sites-available/nazipuruhs.com
ln -s /etc/nginx/sites-available/nazipuruhs.com /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### 9. Configure Firewall

```bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8005/tcp
ufw enable
```

---

## 🔐 Security Setup

### Generate New Secret Key

```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### Update Production Settings

```bash
nano /var/www/hosp/diagcenter/production_settings.py
```

Change:
- `SECRET_KEY` = paste the generated key
- Add your VPS IP to `ALLOWED_HOSTS`
- Verify `DEBUG = False`

### Restart Application

```bash
supervisorctl restart hosp
```

---

## 🌐 DNS Configuration

### Update Domain DNS Records

In your domain registrar (e.g., GoDaddy, Namecheap):

```
Type: A
Name: @
Value: YOUR_VPS_IP
TTL: 3600

Type: A
Name: www
Value: YOUR_VPS_IP
TTL: 3600
```

Wait 24-48 hours for DNS propagation.

---

## 🔒 SSL Certificate Setup (Recommended)

```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Get certificate
certbot --nginx -d nazipuruhs.com -d www.nazipuruhs.com

# Auto-renewal is configured automatically
certbot renew --dry-run
```

After SSL:
1. Edit `/var/www/hosp/diagcenter/production_settings.py`
2. Uncomment SSL-related settings (SECURE_SSL_REDIRECT, etc.)
3. Restart: `supervisorctl restart hosp`

---

## 📊 Post-Deployment Testing

### Test URLs

```bash
# Test application is running
curl http://localhost:8005

# Test from outside
curl http://nazipuruhs.com:8005
```

### Access Points

- **Main Site**: http://nazipuruhs.com:8005
- **Admin Panel**: http://nazipuruhs.com:8005/admin/
- **Public Booking**: http://nazipuruhs.com:8005/public/booking/
- **Display Monitor**: http://nazipuruhs.com:8005/display/monitor/

### Login Credentials

**Superuser**: Created during deployment  
**Doctors**: username format `dr.firstname`, password: `doctor123`

⚠️ **Change all default passwords immediately!**

---

## 🛠️ Maintenance Commands

### Check Status

```bash
# Application status
sudo supervisorctl status hosp

# Nginx status
sudo systemctl status nginx

# View application logs
sudo tail -f /var/www/hosp/logs/gunicorn_error.log

# View supervisor logs
sudo tail -f /var/www/hosp/logs/supervisor.log
```

### Restart Services

```bash
# Restart application only
sudo supervisorctl restart hosp

# Restart nginx
sudo systemctl restart nginx

# Restart both
sudo supervisorctl restart hosp && sudo systemctl restart nginx
```

### Database Backup

```bash
# Create backup
sudo su - hosp
cd /var/www/hosp/data
cp db_production.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Automated daily backup (add to crontab)
crontab -e
# Add: 0 2 * * * cp /var/www/hosp/data/db_production.sqlite3 /var/www/hosp/data/backup_$(date +\%Y\%m\%d).sqlite3
```

### Update Application

```bash
# SSH to VPS
ssh root@YOUR_VPS_IP

# Switch to hosp user
sudo su - hosp
cd /var/www/hosp
source venv/bin/activate

# Pull changes (if using git)
git pull origin main

# Or upload new files via SCP from local:
# scp -r /workspaces/hosp/* hosp@YOUR_VPS_IP:/var/www/hosp/

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Exit and restart
exit
sudo supervisorctl restart hosp
```

---

## 🐛 Troubleshooting

### Application won't start

```bash
# Check logs
sudo tail -100 /var/www/hosp/logs/gunicorn_error.log
sudo supervisorctl tail hosp stderr

# Check if port is in use
sudo netstat -tulpn | grep 8005

# Check permissions
sudo chown -R hosp:hosp /var/www/hosp
sudo chmod 664 /var/www/hosp/data/db_production.sqlite3
```

### 502 Bad Gateway

```bash
# Check if gunicorn is running
sudo supervisorctl status hosp

# Restart application
sudo supervisorctl restart hosp

# Check nginx logs
sudo tail -50 /var/log/nginx/nazipuruhs_error.log
```

### Database locked errors

```bash
# Stop application
sudo supervisorctl stop hosp

# Check database
cd /var/www/hosp
sudo su - hosp
source venv/bin/activate
python manage.py dbshell
# Type: .exit

# Fix permissions
exit
sudo chown hosp:hosp /var/www/hosp/data/db_production.sqlite3
sudo chmod 664 /var/www/hosp/data/db_production.sqlite3

# Restart
sudo supervisorctl start hosp
```

### Static files not loading

```bash
sudo su - hosp
cd /var/www/hosp
source venv/bin/activate
python manage.py collectstatic --noinput --clear
exit
sudo supervisorctl restart hosp
```

---

## 📱 Mobile Access

The system is mobile-responsive. Users can access from phones:
- Patients: Book appointments via public booking page
- Doctors: View appointments on mobile
- Receptionists: Manage queue on tablets
- Display: Large screen for waiting room

---

## 🔄 Port Configuration Note

Since you have 2 other servers running:
- **This server**: Port 8005 (nazipuruhs.com)
- **Other servers**: Different ports (e.g., 8000, 8001)

Nginx is configured to reverse proxy to port 8005.  
Users access via: `http://nazipuruhs.com` (port 80) → proxied to localhost:8005

---

## 📞 Support

If you encounter issues:

1. Check logs first: `/var/www/hosp/logs/`
2. Verify services are running: `supervisorctl status`
3. Test database connection: `python manage.py dbshell`
4. Check firewall: `sudo ufw status`
5. Verify DNS: `nslookup nazipuruhs.com`

---

## ✅ Final Checklist

- [ ] Application running on port 8005
- [ ] Domain pointing to VPS IP
- [ ] SSL certificate installed (optional)
- [ ] Firewall configured
- [ ] Database created and migrated
- [ ] Superuser created
- [ ] Doctors created with schedules
- [ ] Static files collected
- [ ] All passwords changed from defaults
- [ ] Backup strategy in place
- [ ] Tested public booking
- [ ] Tested admin panel
- [ ] Tested display monitor

**🎉 Your hospital management system is now live at nazipuruhs.com!**
