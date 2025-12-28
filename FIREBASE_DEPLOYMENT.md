# 🚀 ReputationAI - Firebase Deployment Guide

## Overview

This project is now fully configured for Firebase deployment with:
- ✅ Firebase Authentication (Admin & User login)
- ✅ Firestore Database (Real-time data storage)
- ✅ Firebase Hosting (Static site hosting)
- ✅ Firebase Functions (Backend API)
- ✅ Firebase Storage (File uploads)

## Prerequisites

1. **Node.js** (v18 or higher)
2. **Firebase CLI** (`npm install -g firebase-tools`)
3. **Firebase Project**: `reputationai-df869`

## Quick Start

### 1. Install Dependencies

```bash
# Install frontend dependencies
cd frontend
npm install --legacy-peer-deps

# Install functions dependencies
cd ../functions
npm install
```

### 2. One-Command Deployment

```bash
cd /workspaces/ReputationAi
./deploy-complete.sh
```

This script will:
- ✅ Build the frontend
- ✅ Install all dependencies
- ✅ Create admin user in Firebase Auth
- ✅ Seed database with sample data
- ✅ Deploy to Firebase Hosting & Functions

## Manual Deployment Steps

If you prefer to deploy manually:

### Step 1: Build Frontend

```bash
cd frontend
npm run build
```

### Step 2: Create Admin User

```bash
cd functions
node create-admin.js
```

This creates:
- **Admin**: `admin@reputationai.com` / `Admin123!@#`
- **Test User**: `user@reputationai.com` / `User123!@#`

### Step 3: Seed Database (Optional)

```bash
cd functions
node seed-firebase.js
```

This populates Firestore with sample data:
- Users
- Entities (Companies, People, Products)
- Mentions (Social media posts)
- Alerts
- Applications

### Step 4: Deploy to Firebase

```bash
cd ..
firebase deploy
```

Or deploy specific services:

```bash
# Deploy only hosting
firebase deploy --only hosting

# Deploy only functions
firebase deploy --only functions

# Deploy only Firestore rules
firebase deploy --only firestore:rules
```

## Project Structure

```
ReputationAI/
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── services/      # Firebase services & API
│   │   ├── config/        # Firebase configuration
│   │   └── store/         # State management (Zustand)
│   └── build/             # Production build (generated)
│
├── functions/             # Firebase Cloud Functions
│   ├── index.js          # Main API endpoints
│   ├── create-admin.js   # Admin user creation script
│   └── seed-firebase.js  # Database seeding script
│
├── firebase.json          # Firebase configuration
├── firestore.rules       # Firestore security rules
├── firestore.indexes.json # Firestore indexes
└── storage.rules         # Firebase Storage rules
```

## Firebase Configuration

The project is configured for Firebase project: **reputationai-df869**

```javascript
{
  apiKey: "AIzaSyCSFPZBzewPT-Tmj-XocBZKAYppGbnE72A",
  authDomain: "reputationai-df869.firebaseapp.com",
  projectId: "reputationai-df869",
  storageBucket: "reputationai-df869.firebasestorage.app",
  messagingSenderId: "1055922829434",
  appId: "1:1055922829434:web:0df16c120978c4b5c363c3",
  measurementId: "G-5N3W3R9NWS"
}
```

## Application URLs

After deployment:

- **Website**: https://reputationai-df869.web.app
- **Alternative**: https://reputationai-df869.firebaseapp.com
- **API**: https://us-central1-reputationai-df869.cloudfunctions.net/api
- **Firebase Console**: https://console.firebase.google.com/project/reputationai-df869

## Login Credentials

### Admin Account
```
Email: admin@reputationai.com
Password: Admin123!@#
```

### Test User Account
```
Email: user@reputationai.com
Password: User123!@#
```

⚠️ **IMPORTANT**: Change these passwords immediately after first login!

## Features

### Frontend (React + Firebase)
- ✅ Firebase Authentication integration
- ✅ Real-time Firestore data sync
- ✅ Admin dashboard
- ✅ Entity management
- ✅ Mention tracking
- ✅ Alert system
- ✅ Analytics dashboard

### Backend (Firebase Functions)
- ✅ RESTful API endpoints
- ✅ User management
- ✅ Entity CRUD operations
- ✅ Mention tracking
- ✅ Alert management
- ✅ Analytics aggregation
- ✅ Security & rate limiting

### Database (Firestore)
- ✅ Users collection
- ✅ Entities collection
- ✅ Mentions collection
- ✅ Alerts collection
- ✅ Applications collection
- ✅ Security rules configured

## Security

### Firestore Rules
- Users can only read/update their own data
- Admins have full access
- All write operations require authentication
- Audit logs are immutable

### API Security
- CORS configured
- Rate limiting enabled (100 requests per 15 minutes)
- Input validation and sanitization
- Helmet.js security headers

## Development

### Local Development

```bash
# Start frontend development server
cd frontend
npm run dev

# Start Firebase emulators (optional)
firebase emulators:start
```

### Environment Variables

No environment variables needed! Everything is configured through Firebase.

## Troubleshooting

### Build Errors

If you encounter build errors:

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm run build
```

### Firebase Login Issues

```bash
firebase logout
firebase login
firebase projects:list
```

### Functions Deployment Errors

```bash
cd functions
npm install
firebase deploy --only functions
```

### Clear and Redeploy

```bash
# Delete build folder
rm -rf frontend/build

# Rebuild
cd frontend
npm run build

# Redeploy
cd ..
firebase deploy
```

## Database Seeding

The `seed-firebase.js` script creates:

- **3 Users**: 1 admin, 2 regular users
- **3 Entities**: Company, Person, Product
- **5 Mentions**: Social media posts with sentiment
- **3 Alerts**: Various alert types
- **3 Applications**: Different statuses

To re-seed:

```bash
cd functions
node seed-firebase.js
```

⚠️ This will **clear existing data** in development. Comment out the clear section if you want to preserve data.

## Monitoring

### Firebase Console
- View logs: https://console.firebase.google.com/project/reputationai-df869/functions/logs
- Firestore data: https://console.firebase.google.com/project/reputationai-df869/firestore
- Authentication: https://console.firebase.google.com/project/reputationai-df869/authentication

### Usage Tracking
- Monitor Functions invocations
- Track Hosting bandwidth
- Watch Firestore read/write operations

## Cost Optimization

Firebase Spark Plan (Free):
- 10GB Hosting storage
- 360MB/day Hosting bandwidth
- 50K Firestore reads/day
- 20K Firestore writes/day
- 125K Functions invocations/month

To stay within free tier:
- Enable caching in frontend
- Optimize Firestore queries
- Use pagination for large datasets
- Monitor usage in Firebase Console

## Next Steps

1. ✅ Deploy the application
2. ✅ Test admin login
3. ✅ Verify data in Firestore
4. ⚠️ Change default passwords
5. ⚠️ Review security rules
6. ⚠️ Set up billing alerts
7. 📱 Optional: Configure custom domain
8. 📧 Optional: Set up email notifications
9. 🔔 Optional: Configure push notifications
10. 📊 Optional: Connect Google Analytics

## Support

For issues or questions:
1. Check Firebase Console logs
2. Review Firestore rules
3. Verify Functions deployment status
4. Check browser console for errors

## License

Proprietary - ReputationAI

---

**Last Updated**: December 28, 2025
**Firebase Project**: reputationai-df869
**Version**: 1.0.0
