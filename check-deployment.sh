#!/bin/bash

# Firebase Deployment Status Check
# Run this to verify your deployment is complete and working

echo "🔍 ReputationAI - Deployment Status Check"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Firebase CLI
echo -n "Checking Firebase CLI... "
if command -v firebase &> /dev/null; then
    echo -e "${GREEN}✓ Installed${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
    echo "Install with: npm install -g firebase-tools"
fi

# Check Node.js
echo -n "Checking Node.js... "
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    echo -e "${GREEN}✓ $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
fi

# Check npm
echo -n "Checking npm... "
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm -v)
    echo -e "${GREEN}✓ $NPM_VERSION${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
fi

echo ""
echo "📦 Project Files Check"
echo "----------------------"

# Check frontend build
echo -n "Frontend build directory... "
if [ -d "frontend/build" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
    BUILD_SIZE=$(du -sh frontend/build | cut -f1)
    echo "   Size: $BUILD_SIZE"
else
    echo -e "${RED}✗ Not found${NC}"
    echo "   Run: cd frontend && npm run build"
fi

# Check functions dependencies
echo -n "Functions node_modules... "
if [ -d "functions/node_modules" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
    echo "   Run: cd functions && npm install"
fi

# Check Firebase config files
echo -n "firebase.json... "
if [ -f "firebase.json" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
fi

echo -n "firestore.rules... "
if [ -f "firestore.rules" ]; then
    echo -e "${GREEN}✓ Exists${NC}"
else
    echo -e "${RED}✗ Not found${NC}"
fi

echo ""
echo "🔐 Firebase Login Check"
echo "------------------------"

if firebase projects:list &> /dev/null 2>&1; then
    echo -e "${GREEN}✓ Logged in to Firebase${NC}"
    echo ""
    echo "Current project:"
    firebase use
else
    echo -e "${RED}✗ Not logged in${NC}"
    echo "Run: firebase login"
fi

echo ""
echo "📊 Deployment Status"
echo "--------------------"

# Check if we can reach the hosting URL
echo -n "Testing hosting URL... "
if curl -s -o /dev/null -w "%{http_code}" https://reputationai-df869.web.app | grep -q "200"; then
    echo -e "${GREEN}✓ Deployed and accessible${NC}"
else
    echo -e "${YELLOW}⚠ Not accessible yet${NC}"
    echo "   Deploy with: firebase deploy"
fi

# Check if functions are deployed
echo -n "Testing Functions API... "
if curl -s -o /dev/null -w "%{http_code}" https://us-central1-reputationai-df869.cloudfunctions.net/api/api/health | grep -q "200"; then
    echo -e "${GREEN}✓ Deployed and accessible${NC}"
else
    echo -e "${YELLOW}⚠ Not accessible yet${NC}"
    echo "   Deploy with: firebase deploy --only functions"
fi

echo ""
echo "📝 Next Steps"
echo "-------------"
echo ""

if [ ! -d "frontend/build" ]; then
    echo "1. Build frontend:"
    echo "   cd frontend && npm run build"
    echo ""
fi

if ! firebase projects:list &> /dev/null 2>&1; then
    echo "2. Login to Firebase:"
    echo "   firebase login"
    echo ""
fi

echo "3. Deploy everything:"
echo "   ./deploy-complete.sh"
echo ""
echo "4. Or deploy manually:"
echo "   firebase deploy"
echo ""

echo "✅ Quick Links"
echo "--------------"
echo "• Website: https://reputationai-df869.web.app"
echo "• Firebase Console: https://console.firebase.google.com/project/reputationai-df869"
echo "• Functions Logs: https://console.firebase.google.com/project/reputationai-df869/functions/logs"
echo ""

echo "📚 Documentation"
echo "----------------"
echo "• Quick Start: QUICK_START_FIREBASE.md"
echo "• Full Guide: FIREBASE_DEPLOYMENT.md"
echo "• Credentials: CREDENTIALS.md"
echo "• Migration Summary: FIREBASE_MIGRATION_COMPLETE.md"
echo ""
