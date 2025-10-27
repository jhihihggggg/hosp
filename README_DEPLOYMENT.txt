╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║      �� NAZIPURUHS.COM - HOSPITAL SYSTEM DEPLOYMENT 🏥          ║
║                                                                  ║
║                  Domain: nazipuruhs.com                          ║
║                  Port: 8005                                      ║
║                  Path: /var/www/nazipuruhs                       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════

✅ CONFIGURATION COMPLETED

All files have been configured for:
  ✓ Domain: nazipuruhs.com
  ✓ Port: 8005 (won't conflict with other apps)
  ✓ Service name: nazipuruhs
  ✓ Directory: /var/www/nazipuruhs

═══════════════════════════════════════════════════════════════════

🚀 DEPLOY IN 1 COMMAND

    chmod +x deploy_now.sh
    ./deploy_now.sh

This will:
  1. Commit & push your code
  2. Upload to VPS
  3. Deploy automatically
  4. Restart service

═══════════════════════════════════════════════════════════════════

📦 FILES READY FOR DEPLOYMENT

✓ push_to_vps.sh          - Upload code from local to VPS
✓ pull_from_repo.sh       - Deploy on VPS (run on server)
✓ deploy_now.sh           - ONE-CLICK full deployment
✓ nginx_nazipuruhs.conf   - Nginx config (port 8005)
✓ hosp.service            - Systemd service (port 8005)
✓ gunicorn_config.py      - Gunicorn config (port 8005)

═══════════════════════════════════════════════════════════════════

📋 DEPLOYMENT METHODS

METHOD 1: ONE-CLICK (Easiest) ⭐
────────────────────────────────
    ./deploy_now.sh


METHOD 2: MANUAL PUSH & PULL
────────────────────────────────
On Local:
    ./push_to_vps.sh

On VPS:
    ssh root@nazipuruhs.com
    cd /var/www/nazipuruhs
    bash pull_from_repo.sh


METHOD 3: GIT-BASED
────────────────────────────────
If you have GitHub set up:
    git push origin main

On VPS:
    ssh root@nazipuruhs.com
    cd /var/www/nazipuruhs
    git pull
    bash pull_from_repo.sh

═══════════════════════════════════════════════════════════════════

📖 DOCUMENTATION FILES

• DEPLOYMENT_nazipuruhs.md    - Complete deployment guide
• QUICK_DEPLOY_nazipuruhs.txt - Quick reference
• README_DEPLOYMENT.txt        - This file

═══════════════════════════════════════════════════════════════════

⚡ AFTER DEPLOYMENT

Check Status:
    ssh root@nazipuruhs.com
    systemctl status nazipuruhs

View Logs:
    journalctl -u nazipuruhs -f

Access Website:
    https://nazipuruhs.com

═══════════════════════════════════════════════════════════════════

🎯 NEXT STEPS

1. Run the deployment:
   ./deploy_now.sh

2. SSH to VPS and verify:
   ssh root@nazipuruhs.com
   systemctl status nazipuruhs

3. Access your site:
   https://nazipuruhs.com

4. Create superuser (if first time):
   cd /var/www/nazipuruhs
   source venv/bin/activate
   python manage.py createsuperuser --settings=diagcenter.production_settings

═══════════════════════════════════════════════════════════════════

🐛 TROUBLESHOOTING

If deployment fails:
    journalctl -u nazipuruhs -xe

If port conflict:
    netstat -tulpn | grep 8005

If permission error:
    chown -R www-data:www-data /var/www/nazipuruhs

═══════════════════════════════════════════════════════════════════

✅ READY TO DEPLOY!

Run: ./deploy_now.sh

═══════════════════════════════════════════════════════════════════
