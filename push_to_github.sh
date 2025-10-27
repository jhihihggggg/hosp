#!/bin/bash

# Push to GitHub Script
# Commits and pushes all changes to GitHub repository

set -e

echo "================================"
echo "📤 Pushing to GitHub..."
echo "================================"

# Check if there are changes
if [[ -z $(git status -s) ]]; then
    echo "✅ No changes to commit"
    echo "📦 Pushing any unpushed commits..."
    git push origin main
    exit 0
fi

echo ""
echo "📝 Changes detected:"
git status -s

echo ""
read -p "Enter commit message (or press Enter for default): " COMMIT_MSG

if [[ -z "$COMMIT_MSG" ]]; then
    COMMIT_MSG="Update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

echo ""
echo "📦 Committing changes..."
git add .
git commit -m "$COMMIT_MSG"

echo ""
echo "⬆️  Pushing to GitHub..."
git push origin main

echo ""
echo "================================"
echo "✅ Successfully pushed to GitHub!"
echo "================================"
echo ""
echo "🔗 Repository: https://github.com/jhihihggggg/hosp"
echo ""
echo "📌 Next steps:"
echo "   1. SSH to your VPS"
echo "   2. Run: cd /var/www/nazipuruhs && bash pull_on_vps.sh"
echo "   Or use: ./deploy_complete.sh"
echo ""
