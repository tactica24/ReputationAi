# 🔐 ReputationAI - Login Credentials & Access

## 🌐 Application URLs

### Production Website
- **Primary**: https://reputationai-df869.web.app
- **Alternative**: https://reputationai-df869.firebaseapp.com
- **API Endpoint**: https://us-central1-reputationai-df869.cloudfunctions.net/api

### Firebase Console
- **Dashboard**: https://console.firebase.google.com/project/reputationai-df869
- **Authentication**: https://console.firebase.google.com/project/reputationai-df869/authentication
- **Firestore**: https://console.firebase.google.com/project/reputationai-df869/firestore
- **Functions**: https://console.firebase.google.com/project/reputationai-df869/functions
- **Hosting**: https://console.firebase.google.com/project/reputationai-df869/hosting

## 👤 User Accounts

### Admin Account (Full Access)
```
Email:    admin@reputationai.com
Password: Admin123!@#
Role:     Admin
```

**Permissions**:
- ✅ Full dashboard access
- ✅ User management
- ✅ Application approvals
- ✅ System settings
- ✅ Data management
- ✅ Analytics & reports

### Test User Account (Limited Access)
```
Email:    user@reputationai.com
Password: User123!@#
Role:     User
```

**Permissions**:
- ✅ View own entities
- ✅ View mentions
- ✅ View alerts
- ✅ Basic analytics
- ❌ No admin features
- ❌ Cannot manage other users

## 🔧 Firebase Configuration

### Project Details
```javascript
Project ID:          reputationai-df869
Project Number:      1055922829434
API Key:             AIzaSyCSFPZBzewPT-Tmj-XocBZKAYppGbnE72A
Auth Domain:         reputationai-df869.firebaseapp.com
Storage Bucket:      reputationai-df869.firebasestorage.app
Messaging Sender ID: 1055922829434
App ID:              1:1055922829434:web:0df16c120978c4b5c363c3
Measurement ID:      G-5N3W3R9NWS
```

### Firebase Services Enabled
- ✅ Authentication (Email/Password)
- ✅ Firestore Database
- ✅ Cloud Functions
- ✅ Hosting
- ✅ Storage
- ✅ Analytics

## 📊 Database Collections

### Firestore Collections
- `users` - User profiles and authentication data
- `entities` - Tracked entities (companies, people, products)
- `mentions` - Social media mentions and reviews
- `alerts` - Notifications and warnings
- `applications` - User applications and onboarding

### Sample Data Included
- **3 Users**: Admin, 2 test users
- **3 Entities**: TechCorp Inc, John Smith, AI Assistant Pro
- **5 Mentions**: Various social media posts with sentiment
- **3 Alerts**: Different severity levels
- **3 Applications**: Pending, approved, rejected

## 🔐 Security Notes

### ⚠️ IMPORTANT - Security Actions Required

1. **Change Default Passwords**
   - Login with default credentials
   - Go to Settings → Change Password
   - Use strong, unique passwords

2. **Review Firestore Rules**
   - Check [firestore.rules](firestore.rules)
   - Ensure rules match your security requirements
   - Test rules in Firebase Console

3. **API Security**
   - Rate limiting: 100 requests per 15 minutes
   - CORS configured for your domain
   - All endpoints require authentication

4. **Authentication**
   - Email verification optional (currently disabled)
   - Can enable 2FA in Firebase Console
   - Password reset via email

### Recommended Actions
- [ ] Change admin password
- [ ] Change test user password  
- [ ] Review Firestore security rules
- [ ] Set up billing alerts
- [ ] Enable email verification
- [ ] Configure password reset emails
- [ ] Add custom email templates
- [ ] Set up monitoring alerts

## 🚀 Deployment Credentials

### Firebase CLI
```bash
# Login to Firebase
firebase login

# View current project
firebase projects:list

# Deploy
firebase deploy
```

### GitHub Repository (if applicable)
```
Repository: https://github.com/tactica24/ReputationAi
Branch: main
```

## 📧 Email Configuration (Optional)

To enable email notifications:

1. Go to Firebase Console → Authentication → Templates
2. Configure email templates:
   - Email verification
   - Password reset
   - Email change

3. Set up custom SMTP (optional):
   - SendGrid
   - Mailgun
   - AWS SES

## 📱 Mobile App (Future)

When mobile app is ready:
- Use same Firebase project
- Add iOS/Android apps in Firebase Console
- Download google-services.json (Android)
- Download GoogleService-Info.plist (iOS)

## 💳 Billing & Usage

### Current Plan: Spark (Free)

**Quotas**:
- Hosting: 10GB storage, 360MB/day bandwidth
- Functions: 125K invocations/month
- Firestore: 50K reads, 20K writes, 20K deletes per day
- Authentication: Unlimited

### Upgrade to Blaze (Pay-as-you-go)
- Required for: Production scale, external API calls
- Set budget alerts to control costs
- Track usage in Firebase Console

## 🆘 Support & Resources

### Firebase Documentation
- https://firebase.google.com/docs

### Project Documentation
- [FIREBASE_DEPLOYMENT.md](FIREBASE_DEPLOYMENT.md) - Full deployment guide
- [QUICK_START_FIREBASE.md](QUICK_START_FIREBASE.md) - Quick start
- [firestore.rules](firestore.rules) - Security rules
- [firebase.json](firebase.json) - Configuration

### Getting Help
1. Check Firebase Console logs
2. Review error messages
3. Check [Cloud Functions Logs](https://console.firebase.google.com/project/reputationai-df869/functions/logs)
4. Verify Firestore data

## 📝 Change Log

### December 28, 2025
- ✅ Initial Firebase deployment
- ✅ Admin and test users created
- ✅ Database seeded with sample data
- ✅ Frontend deployed to Hosting
- ✅ Functions deployed
- ✅ Security rules configured

---

**⚠️ SECURITY REMINDER**: This file contains sensitive credentials. 
**DO NOT** commit this file to public repositories!

Add to `.gitignore`:
```
CREDENTIALS.md
.env
.env.local
serviceAccountKey.json
```

---

**Last Updated**: December 28, 2025  
**Project**: ReputationAI  
**Firebase Project**: reputationai-df869
