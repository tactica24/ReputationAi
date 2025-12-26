#!/bin/bash

# iOS Release Build Script  
# Builds production IPA for App Store

set -e

echo "🍎 iOS Release Build"
echo "===================="

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ iOS builds require macOS${NC}"
    exit 1
fi

# Navigate to mobile directory
cd mobile

# Check if ios directory exists
if [ ! -d "ios" ]; then
    echo -e "${RED}❌ iOS directory not found${NC}"
    echo -e "${YELLOW}Run 'npx react-native init' first${NC}"
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
npm install

# Install pods
echo -e "${YELLOW}📦 Installing CocoaPods...${NC}"
cd ios
pod install

# Build for release
echo -e "${YELLOW}🔨 Building Release IPA...${NC}"
xcodebuild -workspace ReputationAI.xcworkspace \
           -scheme ReputationAI \
           -configuration Release \
           -archivePath build/ReputationAI.xcarchive \
           archive

# Export IPA
xcodebuild -exportArchive \
           -archivePath build/ReputationAI.xcarchive \
           -exportPath build \
           -exportOptionsPlist ExportOptions.plist

cd ..

echo -e "${GREEN}✅ Build complete!${NC}"
echo -e "${GREEN}📱 IPA: mobile/ios/build/ReputationAI.ipa${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Test the IPA on a device via TestFlight"
echo "2. Upload to App Store Connect"
echo "3. Submit for App Store review"
