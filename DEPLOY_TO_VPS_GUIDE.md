# 🚀 Deploy to Ubuntu VPS - Complete Guide

## Quick Deploy (3 Steps)

### Step 1: Push Code to GitHub (Already Done ✅)
```bash
# Already completed
git push origin main
```

### Step 2: Pull on VPS
```bash
# SSH to your VPS
ssh root@your-vps-ip

# Clone or pull the repository
cd /var/www
git clone https://github.com/jhihihggggg/hosp.git nazipuruhs
# OR if already cloned:
cd /var/www/nazipuruhs
git pull origin main
```

### Step 3: Run Setup Script
```bash
cd /var/www/nazipuruhs
chmod +x vps_setup_complete.sh
./vps_setup_complete.sh
```

That's it! ✅

---

## 📋 What the Script Does

1. **System Setup**: Installs Python, Nginx, PostgreSQL, Redis
2. **Virtual Environment**: Creates and activates venv
3. **Dependencies**: Installs all Python packages
4. **Database Setup**: Runs migrations
5. **Static Files**: Collects static files
6. **User Creation**: Creates all production accounts (admin, doctors, staff)
7. **Service Setup**: Configures systemd service
8. **Nginx Setup**: Configures web server
9. **Starts Application**: Launches the app

---

## 🔑 Login Credentials (After Setup)

### Admin Account
- **Username**: `01332856000`
- **Password**: `856000`
- **URL**: http://your-vps-ip:8005/accounts/login/

### Doctor Accounts
1. **Dr. Shakera Sultana**: `01712765762` / `765762`
2. **Dr. Khaja Mohammad**: `01761338884` / `338884`
3. **Dr. Khalid Hosen**: `01312025152` / `025152`
4. **Dr. Ayesha Siddika**: `01770928782` / `928782`

### Staff Accounts
- **Reception**: `01332856002` / `856002`
- **Canteen**: `01332856015` / `856015`
- **Pharmacy**: `01332856010` / `856010`
- **Lab**: `01332856005` / `856005`
- **Display Monitor**: `01332856020` / `856020`

---

## 🔧 Manual Setup (If Script Fails)

### 1. Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx postgresql redis-server git
```

### 2. Create Virtual Environment
```bash
cd /var/www/nazipuruhs
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup Database
```bash
python manage.py migrate
```

### 5. Create Superuser & Accounts
```bash
# Create all production accounts
python manage.py shell < create_production_accounts.py
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 7. Start Application
```bash
# Test run
python manage.py runserver 0.0.0.0:8005

# OR use gunicorn
gunicorn diagcenter.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8005
```

---

## 🌐 Nginx Configuration

Create `/etc/nginx/sites-available/nazipuruhs`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8005;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static/ {
        alias /var/www/nazipuruhs/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/nazipuruhs/media/;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/nazipuruhs /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔄 Systemd Service

Create `/etc/systemd/system/nazipuruhs.service`:

```ini
[Unit]
Description=Nazipuruhs Hospital Management System
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/nazipuruhs
Environment="PATH=/var/www/nazipuruhs/venv/bin"
ExecStart=/var/www/nazipuruhs/venv/bin/gunicorn diagcenter.asgi:application \
    -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:8005 \
    --workers 4 \
    --timeout 120

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable nazipuruhs
sudo systemctl start nazipuruhs
sudo systemctl status nazipuruhs
```

---

## 🐛 Troubleshooting

### Check Service Status
```bash
sudo systemctl status nazipuruhs
sudo journalctl -u nazipuruhs -f
```

### Check Nginx Logs
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Test Database Connection
```bash
cd /var/www/nazipuruhs
source venv/bin/activate
python manage.py dbshell
```

### Recreate Users
```bash
python manage.py shell < create_production_accounts.py
```

### Check Permissions
```bash
sudo chown -R www-data:www-data /var/www/nazipuruhs
sudo chmod -R 755 /var/www/nazipuruhs
```

---

## 🔄 Update Deployment

When you make changes and want to deploy:

```bash
# On local machine
git add -A
git commit -m "Your changes"
git push origin main

# On VPS
cd /var/www/nazipuruhs
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart nazipuruhs
```

---

## ✅ Post-Deployment Checklist

- [ ] Application accessible at http://your-vps-ip:8005
- [ ] Admin login works (01332856000 / 856000)
- [ ] Doctor logins work
- [ ] Staff logins work
- [ ] No login redirect loops
- [ ] Static files loading correctly
- [ ] WebSocket connections working (for real-time features)
- [ ] Database migrations applied
- [ ] All services running (nginx, nazipuruhs)

---

## 📞 Support

If you encounter issues:
1. Check systemd logs: `sudo journalctl -u nazipuruhs -f`
2. Check nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Verify users exist: `python manage.py shell` then `from accounts.models import User; User.objects.all()`
4. Test login manually in Django shell
