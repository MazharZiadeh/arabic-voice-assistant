#!/bin/bash

# Arabic Voice Assistant - GitHub Setup Script
# This script will help you push the project to GitHub

echo "🚀 Setting up GitHub repository for Arabic Voice Assistant"
echo "=================================================="

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo "Please install it first:"
    echo "  Ubuntu/Debian: sudo apt install gh"
    echo "  Or visit: https://cli.github.com/"
    exit 1
fi

# Check if user is logged in to GitHub
if ! gh auth status &> /dev/null; then
    echo "❌ Not logged in to GitHub."
    echo "Please login first:"
    echo "  gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is ready"

# Create private repository
echo "📦 Creating private GitHub repository..."
REPO_NAME="arabic-voice-assistant"
REPO_DESCRIPTION="Complete Arabic voice assistant for office use with memory, task management, and natural language processing"

gh repo create $REPO_NAME \
    --private \
    --description "$REPO_DESCRIPTION" \
    --add-readme=false

if [ $? -eq 0 ]; then
    echo "✅ Repository created successfully!"
    
    # Add remote origin
    echo "🔗 Adding remote origin..."
    git remote add origin https://github.com/$(gh api user --jq .login)/$REPO_NAME.git
    
    # Push to GitHub
    echo "📤 Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo "🎉 Successfully pushed to GitHub!"
        echo "Repository URL: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
    else
        echo "❌ Failed to push to GitHub"
        exit 1
    fi
else
    echo "❌ Failed to create repository"
    exit 1
fi

echo "=================================================="
echo "🎊 Your Arabic Voice Assistant is now on GitHub!"
echo "Repository: https://github.com/$(gh api user --jq .login)/$REPO_NAME"
echo "=================================================="
