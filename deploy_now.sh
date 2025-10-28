#!/bin/bash

# ============================================================================
# ONE-COMMAND DEPLOYMENT FOR NAZIPURUHS.COM
# Run this from your local machine/codespace
# Push to GitHub → VPS pulls from GitHub
# ============================================================================

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🏥 NAZIPURUHS.COM - HOSPITAL DEPLOYMENT 🏥         ║
║                                                           ║
║          Push to GitHub → VPS pulls from GitHub          ║
║                    Port 8005 Setup                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}This script will:${NC}"
echo "  1. Commit your code"
echo "  2. Push to GitHub"
echo "  3. SSH to VPS"
echo "  4. Pull from GitHub on VPS"
echo "  5. Deploy automatically"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

# Configuration
VPS="nazipuruhs.com"
VPS_USER="root"
VPS_PATH="/var/www/hosp"
BRANCH="main"

# Check if Git remote exists
if ! git remote get-url origin >/dev/null 2>&1; then
    echo -e "${RED}Error: No GitHub remote configured!${NC}"
    echo ""
    echo "Please run: ./setup_git.sh first"
    echo "Then add your GitHub repository:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/hosp.git"
    exit 1
fi

echo ""
echo -e "${GREEN}[1/4]${NC} Committing and pushing to GitHub..."
git add .
COMMIT_MSG="Deploy to nazipuruhs.com - $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG" || echo "Nothing to commit"
git push origin $BRANCH

echo ""
echo -e "${GREEN}[2/4]${NC} Uploading pull script to VPS..."
scp pull_from_repo.sh $VPS_USER@$VPS:$VPS_PATH/

echo ""
echo -e "${GREEN}[3/4]${NC} Connecting to VPS..."
echo ""
echo -e "${GREEN}[4/4]${NC} Pulling from GitHub and deploying on VPS..."
ssh $VPS_USER@$VPS "cd $VPS_PATH && bash pull_from_repo.sh"

echo ""
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              ✅ DEPLOYMENT SUCCESSFUL! ✅                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${YELLOW}Your hospital system is now live at:${NC}"
echo "  🌐 https://nazipuruhs.com"
echo "  🔑 https://nazipuruhs.com/admin"
echo ""
echo -e "${YELLOW}Check status:${NC}"
echo "  ssh $VPS_USER@$VPS"
echo "  systemctl status nazipuruhs"
echo ""
