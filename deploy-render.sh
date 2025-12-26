#!/bin/bash

# 🚀 Quick Render Deployment Script
# This script helps you deploy to Render quickly

echo "🚀 ReputationAI - Render Deployment Helper"
echo "=========================================="
echo ""

# Check if logged in to Render CLI
if ! command -v render &> /dev/null; then
    echo "⚠️  Render CLI not installed."
    echo "📥 Install it with: npm install -g render-cli"
    echo ""
    echo "Or deploy via web dashboard:"
    echo "👉 https://dashboard.render.com/select-repo?type=blueprint"
    echo ""
    exit 1
fi

echo "✅ Render CLI detected"
echo ""

# Deploy using render.yaml blueprint
echo "📤 Deploying backend to Render..."
echo ""
echo "Please follow these steps:"
echo ""
echo "1️⃣  Go to: https://dashboard.render.com/select-repo?type=blueprint"
echo ""
echo "2️⃣  Connect your GitHub repository: tactica24/ReputationAi"
echo ""
echo "3️⃣  Render will detect render.yaml and create:"
echo "   📦 reputationai-db (PostgreSQL database)"
echo "   🌐 reputationai-backend (Web service)"
echo ""
echo "4️⃣  Click 'Apply' to start deployment"
echo ""
echo "5️⃣  Wait 3-5 minutes for deployment to complete"
echo ""
echo "6️⃣  Once deployed, initialize the database:"
echo "   - Go to your service in Render dashboard"
echo "   - Click 'Shell' tab"
echo "   - Run: python backend/init_production_db.py"
echo ""
echo "7️⃣  Your backend will be live at:"
echo "   https://reputationai-backend.onrender.com"
echo ""
echo "=========================================="
echo "📖 Full guide: See RENDER_DEPLOYMENT.md"
echo "=========================================="
