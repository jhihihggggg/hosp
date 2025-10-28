# Quick Fix Guide for nazipuruhs.com VPS Issue

## Problem
After pulling from VPS, the app is not running and the domain is not working.

## Solution Steps

### Step 1: Push Fixed Files to GitHub (Run on LOCAL machine)
```bash
cd /workspaces/hosp
git add nginx_nazipuruhs.conf diagnose_vps.sh fix_vps.sh
git commit -m "Fix nginx paths and add diagnostic scripts"
git push origin main
```

### Step 2: Connect to Your VPS
```bash
ssh root@YOUR_VPS_IP
# or
ssh your_username@nazipuruhs.com
```

### Step 3: Run Diagnostic (On VPS)
```bash
cd /var/www/hosp
git pull origin main
sudo bash diagnose_vps.sh > diagnostic_output.txt
cat diagnostic_output.txt
```

### Step 4: Run Fix Script (On VPS)
```bash
sudo bash fix_vps.sh
```

### Step 5: If Issues Persist - Manual Fixes

#### Check Service Status
```bash
sudo systemctl status nazipuruhs
sudo journalctl -u nazipuruhs -n 50
```

#### Check Nginx
```bash
sudo nginx -t
sudo systemctl status nginx
sudo tail -50 /var/log/nginx/nazipuruhs_error.log
```

#### Check if Port is Listening
```bash
sudo netstat -tuln | grep 8005
```

#### Restart Everything
```bash
sudo systemctl restart nazipuruhs
sudo systemctl reload nginx
```

## Common Issues & Fixes

### Issue 1: "Module not found" errors
**Fix:**
```bash
cd /var/www/hosp
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart nazipuruhs
```

### Issue 2: Database errors
**Fix:**
```bash
cd /var/www/hosp
source venv/bin/activate
python manage.py migrate --settings=diagcenter.production_settings
sudo systemctl restart nazipuruhs
```

### Issue 3: Static files not loading
**Fix:**
```bash
cd /var/www/hosp
source venv/bin/activate
python manage.py collectstatic --noinput --settings=diagcenter.production_settings
sudo systemctl restart nazipuruhs
```

### Issue 4: Permission denied errors
**Fix:**
```bash
sudo chown -R www-data:www-data /var/www/hosp
sudo chmod -R 755 /var/www/hosp
sudo systemctl restart nazipuruhs
```

### Issue 5: Domain not working but localhost:8005 works
**Fix:**
1. Check DNS settings - nazipuruhs.com should point to your VPS IP
2. Check firewall:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw status
```

3. Test nginx config:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Issue 6: Port 8005 not listening
**Fix:**
```bash
# Check what's blocking the port
sudo lsof -i :8005

# Check service logs
sudo journalctl -u nazipuruhs -n 100 --no-pager

# Try running manually to see error
cd /var/www/hosp
source venv/bin/activate
gunicorn --bind 0.0.0.0:8005 diagcenter.wsgi:application
```

## Quick Health Check Commands

```bash
# All-in-one health check
echo "=== Service Status ===" && sudo systemctl status nazipuruhs --no-pager && \
echo "" && echo "=== Port Check ===" && sudo netstat -tuln | grep 8005 && \
echo "" && echo "=== Nginx Status ===" && sudo systemctl status nginx --no-pager && \
echo "" && echo "=== Test Connection ===" && curl -I http://localhost:8005
```

## Production Settings Checklist

Make sure your production settings have:
- [ ] DEBUG = False
- [ ] Correct ALLOWED_HOSTS (nazipuruhs.com, www.nazipuruhs.com, VPS IP)
- [ ] Correct STATIC_ROOT and MEDIA_ROOT paths
- [ ] Database path exists: /var/www/hosp/data/db_production.sqlite3

## If All Else Fails - Complete Reinstall

```bash
# Stop and remove everything
sudo systemctl stop nazipuruhs
sudo systemctl disable nazipuruhs
sudo rm /etc/systemd/system/nazipuruhs.service
sudo rm -rf /var/www/hosp

# Clone fresh
cd /var/www
sudo git clone https://github.com/jhihihggggg/hosp.git nazipuruhs
cd nazipuruhs

# Run fix script
sudo bash fix_vps.sh
```

## Contact Info After Fix

Your site should be accessible at:
- http://nazipuruhs.com
- http://www.nazipuruhs.com
- http://YOUR_VPS_IP:8005 (direct access)

Admin panel:
- http://nazipuruhs.com/admin
