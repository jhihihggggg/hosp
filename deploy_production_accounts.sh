#!/bin/bash

# Quick Deploy Production Accounts to VPS
# This script deploys the production accounts to your VPS

echo "=========================================="
echo "DEPLOYING PRODUCTION ACCOUNTS TO VPS"
echo "=========================================="
echo ""

# Check if we're in the correct directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run from project root."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the account creation script
echo "Creating/Updating production accounts..."
python manage.py shell < create_production_accounts.py

# Check if successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo "=========================================="
    echo ""
    echo "Accounts created:"
    echo "  - 1 Admin"
    echo "  - 4 Doctors"
    echo "  - 4 Staff (Reception, Lab, Pharmacy, Canteen)"
    echo ""
    echo "See PRODUCTION_ACCOUNTS.txt for login credentials"
    echo ""
else
    echo ""
    echo "❌ DEPLOYMENT FAILED!"
    echo "Please check the error messages above."
    exit 1
fi
