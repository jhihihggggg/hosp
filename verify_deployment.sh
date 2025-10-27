#!/bin/bash

# Production Deployment Checklist Script
# Run this to verify your deployment is ready

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║    Hospital Management System - Deployment Verification      ║"
echo "║                   nazipuruhs.com:8005                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

check_mark="✓"
cross_mark="✗"
warn_mark="⚠"

# Check if running on VPS
if [ -f "/var/www/hosp/manage.py" ]; then
    ON_VPS=true
    echo "📍 Location: Running on VPS"
else
    ON_VPS=false
    echo "📍 Location: Running locally (dev environment)"
fi
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "FILE VERIFICATION"
echo "═══════════════════════════════════════════════════════════════"

files_to_check=(
    "diagcenter/production_settings.py:Configuration:Production Django settings"
    "gunicorn_config.py:Configuration:Gunicorn WSGI server config"
    "nginx_nazipuruhs.conf:Configuration:Nginx reverse proxy config"
    "hosp_supervisor.conf:Configuration:Supervisor process manager"
    "hosp.service:Configuration:Systemd service file"
    "deploy_production.sh:Script:Automated deployment script"
    "upload_to_vps.sh:Script:VPS file upload script"
    "create_production_doctors.py:Script:Doctor database population"
    "PRODUCTION_DEPLOYMENT_GUIDE.md:Docs:Complete deployment guide"
    "QUICK_VPS_DEPLOYMENT.md:Docs:Quick reference guide"
    "PRODUCTION_READY_SUMMARY.md:Docs:Overview and summary"
    "QUICK_START_CARD.txt:Docs:Quick start instructions"
)

for item in "${files_to_check[@]}"; do
    IFS=':' read -r file category desc <<< "$item"
    if [ -f "$file" ]; then
        echo "$check_mark [$category] $file"
    else
        echo "$cross_mark [$category] $file - MISSING!"
    fi
done

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "CONFIGURATION CHECKS"
echo "═══════════════════════════════════════════════════════════════"

# Check SECRET_KEY
if grep -q "CHANGE-THIS-IN-PRODUCTION" diagcenter/production_settings.py 2>/dev/null; then
    echo "$cross_mark SECRET_KEY: Still using default - MUST CHANGE!"
else
    echo "$check_mark SECRET_KEY: Custom key configured"
fi

# Check DEBUG setting
if grep -q "DEBUG = False" diagcenter/production_settings.py 2>/dev/null; then
    echo "$check_mark DEBUG: Set to False (production mode)"
else
    echo "$cross_mark DEBUG: Not set to False - SECURITY RISK!"
fi

# Check ALLOWED_HOSTS
if grep -q "nazipuruhs.com" diagcenter/production_settings.py 2>/dev/null; then
    echo "$check_mark ALLOWED_HOSTS: Domain configured"
else
    echo "$warn_mark ALLOWED_HOSTS: Verify VPS IP is added"
fi

echo ""

if [ "$ON_VPS" = true ]; then
    echo "═══════════════════════════════════════════════════════════════"
    echo "VPS ENVIRONMENT CHECKS"
    echo "═══════════════════════════════════════════════════════════════"
    
    # Check Python version
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version 2>&1)
        echo "$check_mark Python: $python_version"
    else
        echo "$cross_mark Python3 not installed"
    fi
    
    # Check virtual environment
    if [ -d "/var/www/hosp/venv" ]; then
        echo "$check_mark Virtual Environment: Exists"
    else
        echo "$cross_mark Virtual Environment: Not created"
    fi
    
    # Check Nginx
    if command -v nginx &> /dev/null; then
        echo "$check_mark Nginx: Installed"
        if systemctl is-active --quiet nginx; then
            echo "$check_mark Nginx: Running"
        else
            echo "$warn_mark Nginx: Not running"
        fi
    else
        echo "$cross_mark Nginx: Not installed"
    fi
    
    # Check Supervisor
    if command -v supervisorctl &> /dev/null; then
        echo "$check_mark Supervisor: Installed"
        if supervisorctl status hosp &> /dev/null; then
            echo "$check_mark Application: Running via Supervisor"
        else
            echo "$warn_mark Application: Not running"
        fi
    else
        echo "$cross_mark Supervisor: Not installed"
    fi
    
    # Check database
    if [ -f "/var/www/hosp/data/db_production.sqlite3" ]; then
        db_size=$(du -h /var/www/hosp/data/db_production.sqlite3 | cut -f1)
        echo "$check_mark Database: Exists ($db_size)"
    else
        echo "$cross_mark Database: Not created"
    fi
    
    # Check port 8005
    if netstat -tuln 2>/dev/null | grep -q ":8005"; then
        echo "$check_mark Port 8005: In use (application running)"
    else
        echo "$warn_mark Port 8005: Not in use (application not running?)"
    fi
    
    # Check firewall
    if command -v ufw &> /dev/null; then
        if ufw status | grep -q "Status: active"; then
            echo "$check_mark Firewall: Active"
        else
            echo "$warn_mark Firewall: Not active"
        fi
    fi
    
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "URL ACCESSIBILITY CHECKS"
    echo "═══════════════════════════════════════════════════════════════"
    
    # Test local connection
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8005 | grep -q "200\|302"; then
        echo "$check_mark Local access: http://localhost:8005 - OK"
    else
        echo "$cross_mark Local access: http://localhost:8005 - FAILED"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "DEPLOYMENT READINESS"
echo "═══════════════════════════════════════════════════════════════"

if [ "$ON_VPS" = false ]; then
    echo ""
    echo "📋 PRE-DEPLOYMENT CHECKLIST (Run locally before upload):"
    echo ""
    echo "  [ ] All configuration files created"
    echo "  [ ] Scripts are executable (chmod +x)"
    echo "  [ ] requirements.txt includes gunicorn"
    echo "  [ ] Domain DNS configured (nazipuruhs.com -> VPS IP)"
    echo "  [ ] VPS access verified (SSH working)"
    echo "  [ ] Port 8005 available on VPS"
    echo ""
    echo "🚀 READY TO UPLOAD?"
    echo ""
    echo "   Run: ./upload_to_vps.sh"
    echo ""
else
    echo ""
    echo "📋 POST-DEPLOYMENT CHECKLIST:"
    echo ""
    echo "  [ ] Application running (supervisorctl status hosp)"
    echo "  [ ] Nginx running (systemctl status nginx)"
    echo "  [ ] Database created and migrated"
    echo "  [ ] Superuser account created"
    echo "  [ ] Doctors created (6 doctors)"
    echo "  [ ] SECRET_KEY changed from default"
    echo "  [ ] VPS IP added to ALLOWED_HOSTS"
    echo "  [ ] All default passwords changed"
    echo "  [ ] Can access: http://nazipuruhs.com:8005"
    echo "  [ ] Can access admin: http://nazipuruhs.com:8005/admin/"
    echo "  [ ] Public booking works"
    echo "  [ ] Display monitor works"
    echo "  [ ] SSL certificate installed (optional)"
    echo "  [ ] Database backup configured"
    echo ""
fi

echo "═══════════════════════════════════════════════════════════════"
echo "NEXT STEPS"
echo "═══════════════════════════════════════════════════════════════"

if [ "$ON_VPS" = false ]; then
    echo ""
    echo "1. Review any missing files or failed checks above"
    echo "2. Upload files to VPS: ./upload_to_vps.sh"
    echo "3. SSH to VPS: ssh root@YOUR_VPS_IP"
    echo "4. Run deployment: cd /var/www/hosp && ./deploy_production.sh"
    echo "5. Run this script again on VPS to verify"
    echo ""
else
    echo ""
    echo "1. Review any failed checks above"
    echo "2. Access your site: http://nazipuruhs.com:8005"
    echo "3. Login to admin: http://nazipuruhs.com:8005/admin/"
    echo "4. Change all default passwords"
    echo "5. Test all features"
    echo "6. Configure SSL: certbot --nginx -d nazipuruhs.com"
    echo "7. Set up database backups"
    echo ""
    echo "📊 View logs:"
    echo "   tail -f /var/www/hosp/logs/gunicorn_error.log"
    echo ""
    echo "🔄 Restart application:"
    echo "   supervisorctl restart hosp"
    echo ""
fi

echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "For detailed instructions, see:"
echo "  - PRODUCTION_READY_SUMMARY.md"
echo "  - PRODUCTION_DEPLOYMENT_GUIDE.md"
echo "  - QUICK_VPS_DEPLOYMENT.md"
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           Deployment verification complete!                  ║"
echo "╚══════════════════════════════════════════════════════════════╝"
