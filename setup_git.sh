#!/bin/bash

# Quick Git Setup for nazipuruhs.com deployment

echo "Setting up Git for deployment..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✓ Git initialized"
fi

# Add all files
git add .

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
*.pyc
__pycache__/
*.sqlite3
db.sqlite3
*.log
venv/
env/
.env
staticfiles/
media/temp/
.DS_Store
.vscode/
*.swp
*.swo
*~
.idea/
node_modules/
EOF
    echo "✓ .gitignore created"
fi

# Initial commit
git add .gitignore
git commit -m "Initial commit - Hospital Management System for nazipuruhs.com" || echo "Already committed"

echo ""
echo "✓ Git is ready!"
echo ""
echo "Optional: To add GitHub remote, run:"
echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
echo "  git push -u origin main"
echo ""
