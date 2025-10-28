#!/bin/bash

# Complete Deployment Script - Local to GitHub to VPS
# This script automates the entire deployment process

set -e

echo "================================"
echo "🚀 Complete Deployment Workflow"
echo "================================"

# Configuration
VPS_HOST="nazipuruhs.com"  # Change this to your VPS IP or hostname
VPS_USER="root"            # Change if using different user
APP_DIR="/var/www/hosp"

echo ""
echo "📋 Deployment Steps:"
echo "1. Push code to GitHub"
echo "2. SSH to VPS and pull from GitHub"
echo "3. Deploy application"
echo ""

# Step 1: Push to GitHub
echo "================================"
echo "Step 1: Pushing to GitHub..."
echo "================================"
./push_to_github.sh || {
    echo "❌ Push to GitHub failed!"
    exit 1
}

echo ""
echo "================================"
echo "Step 2: Deploying to VPS..."
echo "================================"

# Step 2: SSH to VPS and deploy
ssh $VPS_USER@$VPS_HOST << 'ENDSSH'
cd /var/www/hosp
bash pull_on_vps.sh
ENDSSH

echo ""
echo "================================"
echo "✅ Complete Deployment Successful!"
echo "================================"
echo ""
echo "🌐 Your application is now live at:"
echo "   https://nazipuruhs.com"
echo ""
echo "🔍 To verify deployment:"
echo "   ssh $VPS_USER@$VPS_HOST 'sudo systemctl status nazipuruhs'"
echo ""
