#!/bin/bash

echo "🚀 Firebase Deployment for ReputationAI"
echo "========================================"
echo ""

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm run build
cd ..

echo ""
echo "✅ Build complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Login to Firebase:"
echo "   firebase login"
echo ""
echo "2. Initialize project (first time only):"
echo "   firebase init hosting"
echo "   - Choose: Use existing project (or create new)"
echo "   - Public directory: frontend/build"
echo "   - Single-page app: Yes"
echo "   - GitHub deploys: No"
echo ""
echo "3. Deploy:"
echo "   firebase deploy --only hosting"
echo ""
echo "⚠️  SECURITY WARNING:"
echo "Your MongoDB password was exposed in terminal!"
echo "Please change it immediately at:"
echo "https://cloud.mongodb.com"
echo ""
