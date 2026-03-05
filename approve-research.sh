#!/bin/bash
# Safe Research Approval Workflow
# Only merges staging to main after validation passes

echo "🔍 Checking staging branch for new research..."

cd /Users/rivervally/.openclaw/workspace-designailab/research

# Switch to staging and pull latest
git fetch origin
git checkout staging
git pull origin staging

echo "🛡️  Validating design format..."

# Run validation
python3 validate-design.py ai-design-research.html

if [ $? -eq 0 ]; then
    echo "✅ Validation passed!"
    echo ""
    echo "📊 What's new in staging:"
    git log main..staging --oneline
    echo ""
    echo "🚀 Merging to main and deploying..."
    
    # Merge to main
    git checkout main
    git merge staging --no-ff -m "✅ Approved research update (validated)"
    
    # Update index.html
    cp ai-design-research.html index.html
    git add index.html
    git commit -m "📦 Update index.html for GitHub Pages"
    
    # Push to GitHub
    git push origin main
    
    echo "✅ DEPLOYED! Check: https://lasithalokuge.github.io/Craftit-Ai-Design-Tech/"
    
else
    echo "❌ Validation failed - NOT deploying to main"
    echo "🔧 Fix the design issues in staging first"
    exit 1
fi