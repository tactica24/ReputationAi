#!/bin/bash

# Complete Firebase Deployment Script for ReputationAI
# This script deploys everything to Firebase: Hosting, Functions, and seeds the database

set -e  # Exit on error

echo "🚀 ReputationAI - Complete Firebase Deployment"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Check if Firebase CLI is installed
echo -e "${BLUE}📦 Step 1: Checking Firebase CLI...${NC}"
if ! command -v firebase &> /dev/null; then
    echo -e "${RED}❌ Firebase CLI not found!${NC}"
    echo "Installing Firebase CLI..."
    npm install -g firebase-tools
fi
echo -e "${GREEN}✅ Firebase CLI is ready${NC}"
echo ""

# Step 2: Login to Firebase
echo -e "${BLUE}🔐 Step 2: Checking Firebase login...${NC}"
if ! firebase projects:list &> /dev/null; then
    echo "Please login to Firebase:"
    firebase login
fi
echo -e "${GREEN}✅ Logged in to Firebase${NC}"
echo ""

# Step 3: Build Frontend
echo -e "${BLUE}🏗️  Step 3: Building frontend...${NC}"
cd /workspaces/ReputationAi/frontend
echo "Installing frontend dependencies..."
npm install --legacy-peer-deps

echo "Building production bundle..."
npm run build

if [ ! -d "build" ]; then
    echo -e "${RED}❌ Build failed! 'build' directory not found.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Frontend built successfully${NC}"
echo ""

# Step 4: Install Functions dependencies
echo -e "${BLUE}📦 Step 4: Installing Functions dependencies...${NC}"
cd /workspaces/ReputationAi/functions
npm install
echo -e "${GREEN}✅ Functions dependencies installed${NC}"
echo ""

# Step 5: Create Admin User
echo -e "${BLUE}👤 Step 5: Creating admin user...${NC}"
echo "This will create the admin user in Firebase Authentication and Firestore"
read -p "Do you want to create/update admin user? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd /workspaces/ReputationAi/functions
    GOOGLE_APPLICATION_CREDENTIALS="" node create-admin.js || echo -e "${YELLOW}⚠️  Admin creation skipped or already exists${NC}"
fi
echo ""

# Step 6: Seed Database
echo -e "${BLUE}🌱 Step 6: Seeding database with sample data...${NC}"
read -p "Do you want to seed the database with sample data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cd /workspaces/ReputationAi/functions
    GOOGLE_APPLICATION_CREDENTIALS="" node seed-firebase.js || echo -e "${YELLOW}⚠️  Seeding skipped${NC}"
fi
echo ""

# Step 7: Deploy to Firebase
echo -e "${BLUE}🚀 Step 7: Deploying to Firebase...${NC}"
cd /workspaces/ReputationAi
echo "Deploying Hosting, Functions, Firestore Rules, and Storage Rules..."
firebase deploy --only hosting,functions,firestore:rules,storage:rules

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    exit 1
fi
echo ""

# Step 8: Summary
echo "═══════════════════════════════════════════════════════"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "📱 Application URLs:"
echo "   • Hosting: https://reputationai-df869.web.app"
echo "   • Hosting (alt): https://reputationai-df869.firebaseapp.com"
echo "   • Functions: https://us-central1-reputationai-df869.cloudfunctions.net/api"
echo ""
echo "🔑 Login Credentials:"
echo "   • Admin: admin@reputationai.com / Admin123!@#"
echo "   • User:  user@reputationai.com / User123!@#"
echo ""
echo "📊 Firebase Console:"
echo "   • https://console.firebase.google.com/project/reputationai-df869"
echo ""
echo "═══════════════════════════════════════════════════════"
echo ""
echo -e "${YELLOW}⚠️  Important Notes:${NC}"
echo "   1. Change default passwords immediately!"
echo "   2. Review Firestore security rules before going live"
echo "   3. Monitor Functions usage in Firebase Console"
echo "   4. Set up billing alerts to avoid unexpected charges"
echo ""
echo "✅ Next Steps:"
echo "   1. Test the application at https://reputationai-df869.web.app"
echo "   2. Verify admin login works correctly"
echo "   3. Check that data appears in the dashboard"
echo "   4. Review Firebase Console for any errors"
echo ""
