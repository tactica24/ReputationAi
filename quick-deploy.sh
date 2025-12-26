#!/bin/bash

# Quick Deployment Script for ReputationAI
# This automates the Vercel deployment process

set -e

echo "🚀 ReputationAI - Quick Deploy to Vercel"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if in correct directory
if [ ! -d "frontend" ]; then
    echo -e "${RED}❌ Error: frontend directory not found${NC}"
    echo "Please run this script from the project root"
    exit 1
fi

echo -e "${BLUE}Step 1: Prerequisites Check${NC}"
echo "----------------------------"

# Check for Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi
echo -e "${GREEN}✅ Vercel CLI ready${NC}"

# Check git status
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
    read -p "Commit changes now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add -A
        git commit -m "chore: Pre-deployment commit"
        git push origin main
        echo -e "${GREEN}✅ Changes committed and pushed${NC}"
    fi
fi

echo ""
echo -e "${BLUE}Step 2: Vercel Login${NC}"
echo "--------------------"
echo "Opening Vercel login..."
vercel login

echo ""
echo -e "${BLUE}Step 3: Deploy Frontend${NC}"
echo "-----------------------"
echo "Deploying to Vercel..."

cd frontend

# Deploy
vercel --prod --yes

echo ""
echo -e "${GREEN}✅ Frontend deployed!${NC}"
echo ""

echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Get your backend URL from Render (see SETUP_COMPLETE.md)"
echo "2. Set environment variable:"
echo "   vercel env add VITE_API_URL production"
echo "   Enter: https://your-backend-url.onrender.com/api/v1"
echo ""
echo "3. Redeploy:"
echo "   vercel --prod"
echo ""
echo -e "${BLUE}📖 Full guide: SETUP_COMPLETE.md${NC}"
