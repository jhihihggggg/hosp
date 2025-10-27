# 🏥 Hospital System Deployment - nazipuruhs.com

Complete deployment guide for the hospital management system on **nazipuruhs.com** running on **Port 8005**.

---

## 📋 System Configuration

- **Domain**: nazipuruhs.com
- **Port**: 8005
- **Directory**: /var/www/nazipuruhs
- **Service**: nazipuruhs.service
- **Other Apps on VPS**: madrasha, saro (running on other ports)

---

## 🚀 Quick Deployment (3 Commands)

### On Your Local Machine (Codespace)

```bash
cd /workspaces/hosp
chmod +x push_to_vps.sh
./push_to_vps.sh
```

### On Your VPS

```bash
ssh root@nazipuruhs.com
cd /var/www/nazipuruhs
bash pull_from_repo.sh
```

**Done!** Access at: https://nazipuruhs.com

---

## 📦 Initial Setup (First Time Only)

### Step 1: Install System Dependencies (On VPS)

```bash
ssh root@nazipuruhs.com

# Update system
apt-get update
apt-get upgrade -y

# Install dependencies
apt-get install -y python3 python3-pip python3-venv nginx supervisor \
    postgresql postgresql-contrib redis-server git curl wget

# Install SSL certificate (if not already installed)
apt-get install -y certbot python3-certbot-nginx
certbot --nginx -d nazipuruhs.com -d www.nazipuruhs.com
```

### Step 2: Create Project Directory

```bash
mkdir -p /var/www/nazipuruhs
cd /var/www/nazipuruhs
```

### Step 3: Upload Initial Code

**On local machine:**
```bash
cd /workspaces/hosp
./push_to_vps.sh
```

### Step 4: Extract and Setup

**On VPS:**
```bash
cd /var/www/nazipuruhs
tar -xzf /tmp/hospital_deploy.tar.gz

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure Production Settings

The production settings are already in `diagcenter/production_settings.py` with:
- Domain: nazipuruhs.com
- Port: 8005
- Database: PostgreSQL or SQLite

### Step 6: Setup Database

```bash
cd /var/www/nazipuruhs
source venv/bin/activate

# Run migrations
python manage.py migrate --settings=diagcenter.production_settings

# Create superuser
python manage.py createsuperuser --settings=diagcenter.production_settings

# Collect static files
python manage.py collectstatic --noinput --settings=diagcenter.production_settings
```

### Step 7: Install System Service

```bash
# Copy service file
cp /var/www/nazipuruhs/hosp.service /etc/systemd/system/nazipuruhs.service

# Enable and start
systemctl daemon-reload
systemctl enable nazipuruhs
systemctl start nazipuruhs
```

### Step 8: Configure Nginx

```bash
# Copy nginx config
cp /var/www/nazipuruhs/nginx_nazipuruhs.conf /etc/nginx/sites-available/nazipuruhs

# Enable site
ln -s /etc/nginx/sites-available/nazipuruhs /etc/nginx/sites-enabled/

# Test and reload
nginx -t
systemctl reload nginx
```

### Step 9: Create Log Directory

```bash
mkdir -p /var/log/nazipuruhs
chown www-data:www-data /var/log/nazipuruhs
```

### Step 10: Set Permissions

```bash
chown -R www-data:www-data /var/www/nazipuruhs
chmod -R 755 /var/www/nazipuruhs
```

---

## 🔄 Regular Updates (After Initial Setup)

### Push Code from Local to VPS

```bash
cd /workspaces/hosp
./push_to_vps.sh
```

### Pull and Deploy on VPS

```bash
ssh root@nazipuruhs.com
cd /var/www/nazipuruhs
bash pull_from_repo.sh
```

The `pull_from_repo.sh` script automatically:
1. Stops the service
2. Creates a backup
3. Extracts new code
4. Runs migrations
5. Collects static files
6. Restarts the service

---

## 🐛 Troubleshooting

### Check Service Status

```bash
systemctl status nazipuruhs
journalctl -u nazipuruhs -f
```

### Check if Port 8005 is Listening

```bash
netstat -tulpn | grep 8005
ss -tulpn | grep 8005
```

### View Logs

```bash
# Service logs
journalctl -u nazipuruhs -n 100

# Application logs
tail -f /var/log/nazipuruhs/error.log
tail -f /var/log/nazipuruhs/access.log

# Nginx logs
tail -f /var/log/nginx/nazipuruhs_error.log
tail -f /var/log/nginx/nazipuruhs_access.log
```

### Service Won't Start

```bash
# Check for errors
journalctl -u nazipuruhs -xe

# Verify port is not in use
netstat -tulpn | grep 8005

# Check permissions
ls -la /var/www/nazipuruhs
chown -R www-data:www-data /var/www/nazipuruhs

# Restart
systemctl restart nazipuruhs
```

### 502 Bad Gateway

```bash
# Check if service is running
systemctl status nazipuruhs

# Check gunicorn is bound to correct port
ps aux | grep gunicorn

# Restart everything
systemctl restart nazipuruhs
systemctl reload nginx
```

### Static Files Not Loading

```bash
cd /var/www/nazipuruhs
source venv/bin/activate
python manage.py collectstatic --noinput --settings=diagcenter.production_settings
chown -R www-data:www-data /var/www/nazipuruhs/staticfiles
```

### Database Issues

```bash
cd /var/www/nazipuruhs
source venv/bin/activate

# Check migrations
python manage.py showmigrations --settings=diagcenter.production_settings

# Run migrations
python manage.py migrate --settings=diagcenter.production_settings
```

---

## 🔐 Security Checklist

- [x] SSL certificate installed (Let's Encrypt)
- [x] HTTPS redirect configured
- [x] Firewall configured (allow 80, 443, 8005)
- [x] Service running as www-data (not root)
- [x] Debug mode disabled in production
- [x] Secret key changed from default
- [x] Database credentials secured
- [x] Static files served with cache headers

### Enable Firewall

```bash
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8005/tcp
ufw allow 22/tcp
ufw enable
```

---

## 📊 Performance Monitoring

### Check Resource Usage

```bash
# CPU and Memory
htop

# Disk usage
df -h
du -sh /var/www/nazipuruhs

# Service resource usage
systemctl status nazipuruhs
```

### Database Performance

```bash
# If using PostgreSQL
sudo -u postgres psql
\l
\c nazipuruhs_db
\dt
```

---

## 💾 Backup & Restore

### Backup Database

```bash
# SQLite
cp /var/www/nazipuruhs/db.sqlite3 /root/backups/db_$(date +%Y%m%d).sqlite3

# PostgreSQL
sudo -u postgres pg_dump nazipuruhs_db > /root/backups/db_$(date +%Y%m%d).sql
```

### Backup Media Files

```bash
tar -czf /root/backups/media_$(date +%Y%m%d).tar.gz /var/www/nazipuruhs/media/
```

### Full Backup

```bash
tar -czf /root/backups/nazipuruhs_full_$(date +%Y%m%d).tar.gz \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  --exclude='venv' \
  /var/www/nazipuruhs
```

### Restore from Backup

```bash
systemctl stop nazipuruhs
cd /var/www
rm -rf nazipuruhs
tar -xzf /root/backups/nazipuruhs_full_YYYYMMDD.tar.gz
chown -R www-data:www-data nazipuruhs
systemctl start nazipuruhs
```

---

## 🔧 Useful Commands

### Service Management

```bash
systemctl start nazipuruhs      # Start service
systemctl stop nazipuruhs       # Stop service
systemctl restart nazipuruhs    # Restart service
systemctl status nazipuruhs     # Check status
systemctl enable nazipuruhs     # Enable on boot
```

### Django Management

```bash
cd /var/www/nazipuruhs
source venv/bin/activate

# All commands need --settings flag
python manage.py [command] --settings=diagcenter.production_settings

# Examples:
python manage.py shell --settings=diagcenter.production_settings
python manage.py dbshell --settings=diagcenter.production_settings
python manage.py createsuperuser --settings=diagcenter.production_settings
```

### Nginx

```bash
nginx -t                         # Test configuration
systemctl reload nginx          # Reload config
systemctl restart nginx         # Restart nginx
systemctl status nginx          # Check status
```

---

## 📞 Support

### VPS Information
- Provider: Contabo
- Support: support@contabo.com

### Quick Diagnostics

```bash
# System info
uname -a
cat /etc/os-release

# Service status
systemctl status nazipuruhs
systemctl status nginx

# Port check
netstat -tulpn | grep 8005

# Process check
ps aux | grep gunicorn

# Disk space
df -h

# Memory
free -h
```

---

## 🎯 Domain & DNS Configuration

Make sure your domain DNS is configured:

```
A Record:  nazipuruhs.com → YOUR_VPS_IP
A Record:  www.nazipuruhs.com → YOUR_VPS_IP
```

Check DNS propagation:
```bash
dig nazipuruhs.com
nslookup nazipuruhs.com
```

---

## ✅ Deployment Checklist

Before going live:

- [ ] Code pushed to VPS
- [ ] Database migrations run
- [ ] Static files collected
- [ ] SSL certificate installed
- [ ] Service running on port 8005
- [ ] Nginx configured and running
- [ ] Firewall rules set
- [ ] Superuser account created
- [ ] Backup system configured
- [ ] Monitoring tools set up
- [ ] DNS pointing to VPS IP
- [ ] Domain accessible via HTTPS

---

## 🚀 Quick Reference

```bash
# LOCAL: Push code
./push_to_vps.sh

# VPS: Deploy code
bash pull_from_repo.sh

# VPS: View logs
journalctl -u nazipuruhs -f

# VPS: Restart
systemctl restart nazipuruhs

# VPS: Check status
systemctl status nazipuruhs
```

---

**Ready to deploy! 🎉**

Access your hospital system at: https://nazipuruhs.com
