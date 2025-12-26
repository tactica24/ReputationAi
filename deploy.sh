#!/bin/bash

# ReputationAI Deployment Script
# This script helps you deploy to Vercel and provides deployment instructions

set -e

echo "🚀 ReputationAI Deployment Assistant"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo -e "${BLUE}Step 1: Checking Prerequisites${NC}"
echo "--------------------------------"

# Check for Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
else
    echo "✅ Vercel CLI installed"
fi

# Check for git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install git first."
    exit 1
else
    echo "✅ Git installed"
fi

echo ""
echo -e "${BLUE}Step 2: Ensure Latest Code is Pushed${NC}"
echo "--------------------------------------"

# Check if there are uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. Committing them now..."
    git add -A
    git commit -m "chore: Pre-deployment commit" || true
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

echo ""
echo -e "${GREEN}✅ Code pushed successfully!${NC}"
echo ""

echo -e "${BLUE}Step 3: Database Setup${NC}"
echo "----------------------"
echo ""
echo "Before deploying, you need to set up free databases:"
echo ""
echo -e "${YELLOW}A. PostgreSQL (Neon.tech):${NC}"
echo "   1. Visit: https://neon.tech"
echo "   2. Create a new project"
echo "   3. Copy the connection string"
echo ""
echo -e "${YELLOW}B. MongoDB (Atlas):${NC}"
echo "   1. Visit: https://www.mongodb.com/cloud/atlas"
echo "   2. Create a free M0 cluster"
echo "   3. Add database user and allow all IPs (0.0.0.0/0)"
echo "   4. Copy the connection string"
echo ""
read -p "Press Enter when you have both database URLs ready..."

echo ""
echo -e "${BLUE}Step 4: Deploy Backend to Render${NC}"
echo "----------------------------------"
echo ""
echo "To deploy the backend:"
echo ""
echo "1. Go to: https://dashboard.render.com"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect your GitHub repo: tactica24/ReputationAi"
echo "4. Render will auto-detect render.yaml configuration"
echo "5. Add these environment variables:"
echo "   - DATABASE_URL: [your Neon PostgreSQL URL]"
echo "   - MONGODB_URI: [your MongoDB Atlas URL]"
echo "   - SECRET_KEY: [generate with: python -c \"import secrets; print(secrets.token_urlsafe(32))\"]"
echo "   - CORS_ORIGINS: *"
echo "   - ENVIRONMENT: production"
echo "6. Click 'Create Web Service'"
echo "7. Wait for deployment (3-5 minutes)"
echo ""
read -p "Enter your Render backend URL (e.g., https://reputationai-backend-xxxx.onrender.com): " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    echo "⚠️  No backend URL provided. You'll need to set it manually later."
    BACKEND_URL="https://your-backend-url.onrender.com"
fi

echo ""
echo -e "${BLUE}Step 5: Deploy Frontend to Vercel${NC}"
echo "-----------------------------------"
echo ""
echo "Deploying frontend to Vercel..."
echo ""

cd frontend

# Check if already logged in to Vercel
if vercel whoami &> /dev/null; then
    echo "✅ Already logged in to Vercel"
else
    echo "Please login to Vercel..."
    vercel login
fi

# Deploy to production
echo ""
echo "🚀 Deploying to Vercel..."
VERCEL_OUTPUT=$(vercel --prod --yes 2>&1) || true

# Extract deployment URL
FRONTEND_URL=$(echo "$VERCEL_OUTPUT" | grep -o 'https://[^ ]*\.vercel\.app' | head -1)

if [ -z "$FRONTEND_URL" ]; then
    echo "⚠️  Could not automatically detect frontend URL"
    echo "Please check the Vercel dashboard for your deployment URL"
    read -p "Enter your Vercel frontend URL: " FRONTEND_URL
fi

echo ""
echo -e "${GREEN}✅ Frontend deployed!${NC}"
echo "Frontend URL: $FRONTEND_URL"

# Set environment variable
echo ""
echo "Setting backend API URL..."
vercel env add VITE_API_URL production <<EOF
${BACKEND_URL}/api/v1
EOF

# Redeploy with environment variable
echo "Redeploying with environment variables..."
vercel --prod --yes

cd ..

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}Your Application URLs:${NC}"
echo "Frontend: $FRONTEND_URL"
echo "Backend:  $BACKEND_URL"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Update CORS on Render:"
echo "   - Go to Render dashboard → Your service → Environment"
echo "   - Update CORS_ORIGINS to: $FRONTEND_URL,http://localhost:3000"
echo ""
echo "2. Test your deployment:"
echo "   - Visit: $FRONTEND_URL"
echo "   - Check health: ${BACKEND_URL}/api/v1/health"
echo ""
echo "3. Create admin user (optional):"
echo "   - Connect to your Neon database"
echo "   - Run the SQL in DEPLOY_NOW.md"
echo ""
echo -e "${BLUE}📖 Full deployment guide: DEPLOY_NOW.md${NC}"
echo ""
