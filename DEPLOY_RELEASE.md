# 🚀 Quick Deploy & Release Guide

## ✅ Setup Complete!

Your project is now configured for deployment to Firebase and app stores.

---

## 📋 Prerequisites

### For Web Deployment
- [ ] Firebase account with project: `reputationai-70092432`
- [ ] Firebase CLI installed: `npm install -g firebase-tools`
- [ ] Logged in: `firebase login`

### For Android Release
- [ ] Android Studio installed
- [ ] Java JDK 17+
- [ ] Google Play Developer account ($25 one-time fee)

### For iOS Release
- [ ] macOS with Xcode
- [ ] Apple Developer account ($99/year)
- [ ] Valid certificates and provisioning profiles

---

## 🌐 Deploy Web App to Firebase

### Option 1: Automatic (Recommended)
```bash
./deploy-firebase.sh
```

### Option 2: Manual
```bash
firebase login
cd frontend
npm install
npm run build
cd ..
firebase deploy --only hosting
```

### Your Live URLs
- 🌐 **Production**: https://reputationai-70092432.web.app
- 🌐 **Firebase**: https://reputationai-70092432.firebaseapp.com

---

## 📱 Build Mobile Apps

### Android APK/AAB
```bash
./build-android.sh
```

**Output:**
- APK: `mobile/android/app/build/outputs/apk/release/app-release.apk`
- AAB: `mobile/android/app/build/outputs/bundle/release/app-release.aab`

**Next Steps:**
1. Test APK on Android device
2. Upload AAB to [Google Play Console](https://play.google.com/console)
3. Complete store listing
4. Submit for review

---

### iOS IPA (macOS only)
```bash
./build-ios.sh
```

**Output:**
- IPA: `mobile/ios/build/ReputationAI.ipa`

**Next Steps:**
1. Test via TestFlight
2. Upload to [App Store Connect](https://appstoreconnect.apple.com)
3. Complete app information
4. Submit for review

---

## 🔄 GitHub Actions (Automated)

Push code to trigger automatic builds:

### Web Deployment
```bash
git push origin main
# Automatically deploys to Firebase
```

### Mobile Builds
```bash
git tag v1.0.0
git push origin v1.0.0
# Builds Android and iOS apps
```

Download build artifacts from GitHub Actions page.

---

## 📦 What's Included

### Configuration Files
- ✅ `.firebaserc` - Firebase project config
- ✅ `firebase.json` - Hosting configuration
- ✅ `mobile/app.json` - Mobile app metadata
- ✅ `mobile/.env` - Environment variables
- ✅ GitHub Actions workflows

### Build Scripts
- ✅ `deploy-firebase.sh` - Web deployment
- ✅ `build-android.sh` - Android build
- ✅ `build-ios.sh` - iOS build

### Documentation
- ✅ `DEPLOYMENT_MOBILE_GUIDE.md` - Complete mobile guide
- ✅ `SECURITY_PRIVATE_APP.md` - Security documentation

---

## 🎯 First-Time Setup

### 1. Firebase Setup
```bash
# Login to Firebase
firebase login

# Verify project
firebase projects:list
firebase use reputationai-70092432

# Deploy security rules
firebase deploy --only firestore:rules,storage:rules
```

### 2. Android Keystore (First Time Only)
```bash
cd mobile/android/app
keytool -genkeypair -v -storetype PKCS12 \
  -keystore reputation-ai.keystore \
  -alias reputation-ai \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

**Save the password securely!** You'll need it for every release.

### 3. iOS Setup (macOS)
1. Open `mobile/ios/ReputationAI.xcworkspace` in Xcode
2. Sign in with Apple Developer account
3. Configure automatic signing
4. Update Team ID in `ExportOptions.plist`

---

## 📊 Testing

### Test Web App Locally
```bash
cd frontend
npm run dev
# Visit http://localhost:5173
```

### Test Production Build
```bash
cd frontend
npm run build
npm run preview
```

### Test Android APK
```bash
# Install on connected device
adb install mobile/android/app/build/outputs/apk/release/app-release.apk
```

---

## 🔐 Security Checklist

Before releasing:
- [ ] Update `.env` with production values
- [ ] Enable Firebase Authentication
- [ ] Deploy Firestore security rules
- [ ] Deploy Storage security rules
- [ ] Update CORS_ORIGINS to your domain
- [ ] Generate strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS enforcement
- [ ] Test authentication flow
- [ ] Verify user permissions

---

## 📝 App Store Requirements

### Information Needed
- App name: **AI Reputation Guardian**
- Category: **Business / Productivity**
- Description (see `DEPLOYMENT_MOBILE_GUIDE.md`)
- Screenshots (phone and tablet)
- App icon (1024x1024)
- Privacy policy URL
- Support email

### Screenshots Required
- **Android**: 1080x1920 (minimum 2)
- **iOS**: 1290x2796 (6.7" display)

---

## 🆘 Troubleshooting

### Firebase Deploy Failed
```bash
firebase logout
firebase login
firebase use reputationai-70092432
```

### Android Build Failed
```bash
cd mobile/android
./gradlew clean
./gradlew assembleRelease --stacktrace
```

### iOS Build Failed
```bash
cd mobile/ios
pod deintegrate
pod install
```

---

## 📱 Download & Install Apps

### For Testers (Before App Store)

**Android:**
1. Download APK from GitHub Actions or builds
2. Enable "Install from Unknown Sources"
3. Install APK file

**iOS:**
1. Join TestFlight beta
2. Install TestFlight app
3. Accept invitation
4. Install app from TestFlight

### After App Store Approval

**Android:**
- Google Play Store: Search "AI Reputation Guardian"

**iOS:**
- Apple App Store: Search "AI Reputation Guardian"

---

## 🎉 Next Steps

1. **Deploy web app** to Firebase
2. **Test thoroughly** on all platforms
3. **Create keystore** for Android signing
4. **Build mobile apps** for stores
5. **Prepare store listings** (screenshots, descriptions)
6. **Submit for review** to Google Play and App Store
7. **Monitor analytics** and user feedback

---

## 📞 Support

- **Documentation**: See `DEPLOYMENT_MOBILE_GUIDE.md`
- **Security**: See `SECURITY_PRIVATE_APP.md`
- **Firebase Console**: https://console.firebase.google.com/project/reputationai-70092432

---

## 🚀 Quick Commands

```bash
# Deploy everything
./deploy-firebase.sh
./build-android.sh
./build-ios.sh

# Or use Git tags for automated builds
git tag v1.0.0
git push origin v1.0.0
```

Good luck with your launch! 🎊
