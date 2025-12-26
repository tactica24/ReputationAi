#!/bin/bash

# Android Release Build Script
# Builds production APK and AAB for Google Play Store

set -e

echo "🤖 Android Release Build"
echo "========================"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Navigate to mobile directory
cd mobile

# Check if android directory exists
if [ ! -d "android" ]; then
    echo -e "${RED}❌ Android directory not found${NC}"
    echo -e "${YELLOW}Run 'npx react-native init' first${NC}"
    exit 1
fi

# Install dependencies
echo -e "${YELLOW}📦 Installing dependencies...${NC}"
npm install

# Clean previous builds
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
cd android
./gradlew clean

# Build Release APK
echo -e "${YELLOW}🔨 Building Release APK...${NC}"
./gradlew assembleRelease

# Build Release AAB (for Play Store)
echo -e "${YELLOW}🔨 Building Release AAB...${NC}"
./gradlew bundleRelease

cd ..

echo -e "${GREEN}✅ Build complete!${NC}"
echo -e "${GREEN}📱 APK: mobile/android/app/build/outputs/apk/release/app-release.apk${NC}"
echo -e "${GREEN}📦 AAB: mobile/android/app/build/outputs/bundle/release/app-release.aab${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Test the APK on a device"
echo "2. Upload AAB to Google Play Console"
echo "3. Follow the Play Store review process"
