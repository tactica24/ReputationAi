# 🚀 Deployment & Distribution Guide

## Firebase Web App Deployment

### Prerequisites
- Firebase CLI installed: `npm install -g firebase-tools`
- Logged in to Firebase: `firebase login`

### Quick Deploy
```bash
./deploy-firebase.sh
```

Or manually:
```bash
cd frontend
npm install
npm run build
cd ..
firebase deploy --only hosting
```

### Your Live URLs
- **Production**: https://reputationai-70092432.web.app
- **Firebase**: https://reputationai-70092432.firebaseapp.com

---

## Mobile App Distribution

### 📱 Android (Google Play Store)

#### Prerequisites
1. **Android Studio** installed
2. **Java JDK 17** or higher
3. **Keystore file** for signing (create one if you don't have it)

#### Create Keystore (First Time Only)
```bash
cd mobile/android/app
keytool -genkeypair -v -storetype PKCS12 \
  -keystore reputation-ai.keystore \
  -alias reputation-ai \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

Save your keystore password securely!

#### Build APK/AAB
```bash
./build-android.sh
```

#### Output Files
- **APK**: `mobile/android/app/build/outputs/apk/release/app-release.apk`
- **AAB**: `mobile/android/app/build/outputs/bundle/release/app-release.aab`

#### Upload to Google Play
1. Go to [Google Play Console](https://play.google.com/console)
2. Create a new app or select existing
3. Upload the AAB file (NOT APK)
4. Fill in store listing details
5. Submit for review

---

### 🍎 iOS (Apple App Store)

#### Prerequisites
1. **macOS** with Xcode installed
2. **Apple Developer Account** ($99/year)
3. **Provisioning Profile** and **Certificate**

#### Setup
1. Open Xcode
2. Sign in with Apple ID (Xcode > Preferences > Accounts)
3. Configure signing in project settings

#### Build IPA
```bash
./build-ios.sh
```

#### Output File
- **IPA**: `mobile/ios/build/ReputationAI.ipa`

#### Upload to App Store
1. Open Xcode
2. Go to Window > Organizer
3. Select your archive
4. Click "Distribute App"
5. Choose "App Store Connect"
6. Follow the wizard

Or use Transporter app:
1. Download Apple Transporter
2. Sign in with Apple ID
3. Drag and drop IPA file
4. Click "Deliver"

---

## Firebase Configuration

Your project is configured with:
- **Project ID**: `reputationai-70092432`
- **Console**: https://console.firebase.google.com/project/reputationai-70092432

### Services Enabled
- ✅ Authentication
- ✅ Firestore Database  
- ✅ Cloud Storage
- ✅ Hosting
- ✅ Cloud Functions (optional)

---

## Environment Configuration

### Web (.env)
```bash
VITE_FIREBASE_PROJECT_ID=reputationai-70092432
VITE_API_URL=https://reputationai-70092432.web.app/api/v1
```

### Mobile (.env)
```bash
API_URL=https://reputationai-70092432.web.app/api/v1
FIREBASE_PROJECT_ID=reputationai-70092432
ENVIRONMENT=production
```

---

## App Store Metadata

### Package Names
- **Android**: `com.reputationai.app`
- **iOS**: `com.reputationai.app`

### App Information
- **Name**: AI Reputation Guardian
- **Version**: 1.0.0
- **Category**: Business / Productivity
- **Age Rating**: 4+ (No objectionable content)

### Required Screenshots
- **Android**: 
  - Phone: 1080x1920 (minimum 2 screenshots)
  - Tablet: 1920x1080 (optional)
- **iOS**:
  - iPhone: 1290x2796 (6.7" display)
  - iPad: 2048x2732 (12.9" display)

### Description Template
```
AI Reputation Guardian - Enterprise reputation monitoring and identity protection.

Monitor your online reputation across social media, news, and review platforms in real-time. Get instant alerts about potential threats and take action to protect your brand.

Features:
• Real-time reputation monitoring
• AI-powered sentiment analysis
• Multi-platform coverage
• Instant threat alerts
• Comprehensive analytics
• Secure biometric authentication

Perfect for:
- Business executives
- Public figures
- Brands and companies
- Anyone concerned about their online presence

Your privacy is protected with enterprise-grade security including end-to-end encryption and biometric authentication.
```

---

## Testing Before Release

### Web App
```bash
# Test locally
cd frontend
npm run dev

# Test production build
npm run build
npm run preview
```

### Android
```bash
# Install APK on device
adb install mobile/android/app/build/outputs/apk/release/app-release.apk

# View logs
adb logcat | grep ReactNative
```

### iOS
```bash
# Test on simulator
cd mobile/ios
npx react-native run-ios --configuration Release

# Test on device (requires Xcode)
# Open .xcworkspace in Xcode and run on connected device
```

---

## Troubleshooting

### Firebase Deploy Fails
```bash
# Re-authenticate
firebase logout
firebase login

# Check project
firebase projects:list
firebase use reputationai-70092432
```

### Android Build Fails
```bash
# Clean and rebuild
cd mobile/android
./gradlew clean
./gradlew assembleRelease --stacktrace
```

### iOS Build Fails
```bash
# Clean derived data
rm -rf ~/Library/Developer/Xcode/DerivedData

# Reinstall pods
cd mobile/ios
pod deintegrate
pod install
```

---

## Release Checklist

### Before Submitting

- [ ] All features working on production
- [ ] Firebase security rules deployed
- [ ] Environment variables configured
- [ ] App tested on multiple devices
- [ ] Screenshots prepared
- [ ] App description written
- [ ] Privacy policy URL ready
- [ ] Terms of service URL ready
- [ ] Support email configured
- [ ] App icon and splash screens added
- [ ] Version numbers updated

### App Store Specific

#### Google Play
- [ ] Keystore safely stored
- [ ] Content rating completed
- [ ] Target audience selected
- [ ] Privacy policy linked
- [ ] App signing enabled

#### Apple App Store
- [ ] Apple Developer account active
- [ ] Certificates and provisioning profiles valid
- [ ] App privacy details submitted
- [ ] Age rating completed
- [ ] Export compliance information

---

## Post-Release

### Monitor
- Firebase Analytics
- Crash reports (Crashlytics)
- User reviews
- App performance

### Update Process
1. Increment version number
2. Build new release
3. Test thoroughly
4. Submit update to stores
5. Monitor rollout

---

## Support & Resources

- **Firebase Console**: https://console.firebase.google.com
- **Google Play Console**: https://play.google.com/console
- **App Store Connect**: https://appstoreconnect.apple.com
- **React Native Docs**: https://reactnative.dev

---

## Security Notes

⚠️ **Important**: Never commit these files to Git:
- Keystore files (.keystore, .jks)
- Provisioning profiles
- .env files with secrets
- google-services.json (Android)
- GoogleService-Info.plist (iOS)

All sensitive files are already in .gitignore.
