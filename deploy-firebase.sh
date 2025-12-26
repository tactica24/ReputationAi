#!/bin/bash

# Firebase Deployment Script
# Deploys web app to Firebase Hosting

set -e

echo "🚀 Firebase Deployment Script"
echo "================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if logged in
echo -e "${YELLOW}📋 Checking Firebase authentication...${NC}"
if ! firebase projects:list &> /dev/null; then
    echo -e "${RED}❌ Not logged in to Firebase${NC}"
    echo -e "${YELLOW}Please run: firebase login${NC}"
    exit 1
fi

# Build frontend
echo -e "${YELLOW}🔨 Building frontend...${NC}"
cd frontend
npm install
npm run build
cd ..

# Deploy to Firebase
echo -e "${YELLOW}🚀 Deploying to Firebase...${NC}"
firebase deploy --only hosting --project reputationai-70092432

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${GREEN}🌐 Your app is live at: https://reputationai-70092432.web.app${NC}"
echo -e "${GREEN}🌐 Or custom domain: https://reputationai-70092432.firebaseapp.com${NC}"
