#!/bin/bash

# Simple File Upload Script to VPS
# This script helps you upload your application to the VPS

echo "=========================================="
echo "Upload Hospital System to VPS"
echo "=========================================="
echo ""

# Get VPS IP
read -p "Enter your VPS IP address: " VPS_IP
echo ""

# Get VPS user (default: root)
read -p "Enter VPS username (default: root): " VPS_USER
VPS_USER=${VPS_USER:-root}
echo ""

echo "Creating deployment package..."
cd /workspaces/hosp

# Create tar archive excluding unnecessary files
tar -czf hosp_deploy.tar.gz \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='*.sqlite3' \
    --exclude='media/*' \
    --exclude='.git' \
    --exclude='venv' \
    --exclude='staticfiles' \
    --exclude='logs' \
    .

echo "✓ Package created: hosp_deploy.tar.gz"
echo ""

echo "Uploading to VPS..."
echo "Target: $VPS_USER@$VPS_IP:/tmp/"
echo ""

# Upload to VPS
scp hosp_deploy.tar.gz $VPS_USER@$VPS_IP:/tmp/

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Upload successful!"
    echo ""
    echo "=========================================="
    echo "Next Steps:"
    echo "=========================================="
    echo ""
    echo "1. SSH into your VPS:"
    echo "   ssh $VPS_USER@$VPS_IP"
    echo ""
    echo "2. Extract and deploy:"
    echo "   mkdir -p /var/www/hosp"
    echo "   cd /var/www/hosp"
    echo "   tar -xzf /tmp/hosp_deploy.tar.gz"
    echo "   chmod +x deploy_production.sh"
    echo "   ./deploy_production.sh"
    echo ""
    echo "3. Follow the deployment script prompts"
    echo ""
    echo "=========================================="
else
    echo ""
    echo "✗ Upload failed!"
    echo "Please check:"
    echo "  - VPS IP address is correct"
    echo "  - SSH access is working"
    echo "  - You have permission to upload"
    echo ""
    echo "Try manual upload:"
    echo "  scp hosp_deploy.tar.gz $VPS_USER@$VPS_IP:/tmp/"
fi

# Clean up
rm hosp_deploy.tar.gz
echo ""
echo "Local package cleaned up."
