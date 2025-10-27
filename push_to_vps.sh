#!/bin/bash

# ============================================================================
# Push Hospital Code to GitHub - nazipuruhs.com
# This script commits and pushes your code to GitHub
# Then VPS will pull from GitHub
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Push Hospital System to GitHub                    ║${NC}"
echo -e "${BLUE}║     nazipuruhs.com - Port 8005                        ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Configuration
BRANCH="main"
REPO_NAME="hosp"

echo -e "${YELLOW}Configuration:${NC}"
echo "  Repository: $REPO_NAME"
echo "  Branch: $BRANCH"
echo "  Domain: nazipuruhs.com"
echo "  Port: 8005"
echo ""

# Step 1: Check if Git is initialized
echo -e "${GREEN}[1/5]${NC} Checking Git status..."
if [ ! -d ".git" ]; then
    echo -e "${RED}Git not initialized!${NC}"
    echo -e "${YELLOW}Run './setup_git.sh' first to initialize Git${NC}"
    exit 1
fi

# Step 2: Check if GitHub remote exists
echo -e "${GREEN}[2/5]${NC} Checking GitHub remote..."
if ! git remote get-url origin >/dev/null 2>&1; then
    echo -e "${RED}No GitHub remote configured!${NC}"
    echo ""
    echo -e "${YELLOW}Please add your GitHub repository:${NC}"
    echo "  1. Create a new repository on GitHub: https://github.com/new"
    echo "  2. Run: git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
    echo ""
    echo "Or if you already have a repo, run:"
    read -p "Enter your GitHub repo URL (or press Enter to skip): " REPO_URL
    if [ ! -z "$REPO_URL" ]; then
        git remote add origin "$REPO_URL"
        echo -e "${GREEN}✓ Remote added${NC}"
    else
        echo -e "${RED}Cannot continue without GitHub remote${NC}"
        exit 1
    fi
fi

REPO_URL=$(git remote get-url origin)
echo -e "${GREEN}✓ Repository: $REPO_URL${NC}"

# Step 3: Stage all changes
echo -e "${GREEN}[3/5]${NC} Staging changes..."
git add .
echo -e "${GREEN}✓ Changes staged${NC}"

# Step 4: Commit changes
echo -e "${GREEN}[4/5]${NC} Committing changes..."
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}No changes to commit${NC}"
else
    read -p "Enter commit message (or press Enter for default): " COMMIT_MSG
    if [ -z "$COMMIT_MSG" ]; then
        COMMIT_MSG="Deploy to nazipuruhs.com - $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    git commit -m "$COMMIT_MSG"
    echo -e "${GREEN}✓ Committed: $COMMIT_MSG${NC}"
fi

# Step 5: Push to GitHub
echo -e "${GREEN}[5/5]${NC} Pushing to GitHub..."
git push origin $BRANCH

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Pushed to GitHub Successfully! ✓              ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "Now SSH to your VPS and pull the code:"
echo ""
echo -e "${BLUE}ssh root@nazipuruhs.com${NC}"
echo -e "${BLUE}cd /var/www/nazipuruhs${NC}"
echo -e "${BLUE}bash pull_from_repo.sh${NC}"
echo ""
echo -e "Or run the auto-deploy: ${BLUE}./deploy_now.sh${NC}"
echo ""
