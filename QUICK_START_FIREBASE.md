# 🎯 Quick Start Guide - ReputationAI on Firebase

## ⚡ Deploy in 3 Steps

### Step 1: Login to Firebase
```bash
firebase login
```

### Step 2: Run Deployment Script
```bash
cd /workspaces/ReputationAi
./deploy-complete.sh
```

### Step 3: Open Your App
```bash
https://reputationai-df869.web.app
```

## 🔑 Login Credentials

### Admin
- **Email**: `admin@reputationai.com`
- **Password**: `Admin123!@#`

### Test User
- **Email**: `user@reputationai.com`
- **Password**: `User123!@#`

## 📦 What's Included

✅ **Frontend**: React app with Firebase integration
✅ **Backend**: Firebase Cloud Functions (RESTful API)
✅ **Database**: Firestore with security rules
✅ **Auth**: Firebase Authentication
✅ **Hosting**: Firebase Hosting (CDN-powered)
✅ **Sample Data**: Pre-seeded entities, mentions, alerts

## 🚀 Manual Commands

### Build Only
```bash
cd frontend
npm run build
```

### Deploy Only Hosting
```bash
firebase deploy --only hosting
```

### Deploy Only Functions
```bash
firebase deploy --only functions
```

### Create Admin User
```bash
cd functions
node create-admin.js
```

### Seed Database
```bash
cd functions
node seed-firebase.js
```

## 📊 Firebase Console

Access your Firebase project:
```
https://console.firebase.google.com/project/reputationai-df869
```

### Important Sections:
- **Authentication**: Manage users
- **Firestore**: View/edit database
- **Functions**: Monitor API logs
- **Hosting**: View deployment history
- **Usage**: Track quotas

## 🔧 Troubleshooting

### Build Errors?
```bash
cd frontend
rm -rf node_modules build
npm install --legacy-peer-deps
npm run build
```

### Can't Login?
1. Check Firebase Console → Authentication
2. Verify user exists
3. Run `node create-admin.js` again

### No Data in Dashboard?
1. Run `node seed-firebase.js`
2. Check Firestore Console
3. Verify security rules

### Functions Not Working?
```bash
firebase deploy --only functions
firebase functions:log
```

## 📱 Application Features

### Admin Dashboard
- User management
- Application approvals
- System analytics
- Entity monitoring

### User Features
- Entity tracking
- Mention monitoring
- Sentiment analysis
- Alert notifications

## 🛡️ Security

### Firestore Rules
- Users can only access their own data
- Admins have full access
- All mutations require authentication

### API Security
- CORS enabled
- Rate limiting (100 req/15min)
- Input validation
- Helmet.js protection

## 💰 Cost Estimate

### Firebase Spark Plan (FREE)
- **Hosting**: 10GB storage, 360MB/day bandwidth
- **Functions**: 125K invocations/month
- **Firestore**: 50K reads, 20K writes, 20K deletes per day

This should cover initial development and testing!

## 📈 Next Steps

1. ✅ Test the deployed app
2. ✅ Change default passwords
3. ⚠️ Review security rules
4. 📧 Set up email notifications (optional)
5. 🌐 Add custom domain (optional)
6. 📊 Connect analytics (optional)

## 🆘 Need Help?

### Check Logs
```bash
# Functions logs
firebase functions:log

# Hosting logs
firebase hosting:log
```

### View Errors
```bash
# Browser console (F12)
# Firebase Console → Functions → Logs
# Firebase Console → Firestore → Usage
```

## 🎉 Success Checklist

- [ ] Frontend deployed to Hosting
- [ ] Functions deployed and accessible
- [ ] Admin user created
- [ ] Can login with admin credentials
- [ ] Dashboard shows data
- [ ] Firestore has seeded data
- [ ] No errors in console

---

**Project**: ReputationAI  
**Firebase Project**: reputationai-df869  
**Updated**: December 28, 2025
