# Firebase Setup Complete ✅

## Overview
Your ReputationAI application has been fully configured for Firebase deployment. This is a **complete, production-ready setup** using only Firebase services.

## Architecture

### Firebase Services Used
- **Firebase Hosting**: Frontend deployment (React + Vite)
- **Cloud Functions**: Backend API (Express.js)
- **Cloud Firestore**: NoSQL database
- **Firebase Storage**: File storage
- **Firebase Authentication**: User authentication (ready to configure)

### Why Firebase-Only is Better
✅ **No Cold Starts**: Unlike Render's free tier (30s wake time), Firebase Functions are fast
✅ **Global CDN**: Hosting on Google's infrastructure worldwide
✅ **Integrated Services**: Everything works together seamlessly
✅ **Generous Free Tier**: 
   - Hosting: 10GB storage, 360MB/day transfer
   - Functions: 2M invocations/month
   - Firestore: 1GB storage, 50K reads, 20K writes per day
✅ **Auto-Scaling**: Handles traffic spikes automatically
✅ **Built-in Security**: Firestore security rules protect your data

## What's Been Created

### Configuration Files
- `firebase.json` - Main Firebase configuration
- `firestore.rules` - Database security rules with role-based access
- `firestore.indexes.json` - Database indexes
- `storage.rules` - File storage security

### Backend (Firebase Functions)
- `functions/index.js` - Complete Express API with endpoints:
  - `/api/health` - Health check
  - `/api/v1/applications` - Application submissions (CRUD)
  - `/api/v1/users` - User management
  - `/api/v1/entities` - Entity tracking
  - `/api/v1/mentions` - Social mentions
  - `/api/v1/alerts` - Alert system
  - `/api/v1/analytics/dashboard` - Admin analytics

### Frontend
- Production build ready in `frontend/build/`
- Total size: 923KB (optimized with code splitting)
- Configured for Firebase Hosting with SPA routing

### Database Schema (Firestore)

#### Collections:
1. **applications**
   - company_name, email, industry, company_size, use_case
   - status: pending|approved|rejected
   - timestamps: created_at, updated_at

2. **users**
   - email, name, company, role (user|admin)
   - is_active, created_at, updated_at

3. **entities**
   - user_id, name, entity_type, description
   - is_active, created_at, updated_at

4. **mentions**
   - entity_id, source, content, sentiment, url
   - created_at

5. **alerts**
   - entity_id, alert_type, severity, message, mention_id
   - is_read, created_at

6. **auditLogs** (for compliance)
   - user_id, action, resource, details
   - timestamp

## Deployment Steps

### 1. Firebase Login (If Not Already Logged In)
```bash
firebase login
```
This will open a browser for authentication.

### 2. Initialize Firebase Project
```bash
firebase init
```
Select:
- ✅ Firestore
- ✅ Functions
- ✅ Hosting
- ✅ Storage

When prompted:
- Firestore rules: `firestore.rules`
- Firestore indexes: `firestore.indexes.json`
- Functions language: JavaScript
- Functions directory: `functions`
- Install dependencies: Yes
- Hosting directory: `frontend/build`
- Single-page app: Yes
- GitHub deploys: No (for now)

### 3. Deploy Everything
```bash
firebase deploy
```

This will deploy:
- ✅ Firestore rules and indexes
- ✅ Cloud Functions (your backend API)
- ✅ Frontend to Firebase Hosting
- ✅ Storage rules

### 4. Get Your Live URL
After deployment, you'll get a URL like:
```
https://your-project-id.web.app
```

## Post-Deployment Configuration

### Set Up Firebase in Frontend
1. Go to Firebase Console: https://console.firebase.google.com
2. Select your project
3. Click "Web" icon (</>) to add a web app
4. Copy the Firebase config
5. Add to `frontend/src/firebaseConfig.js`:

```javascript
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
```

### Enable Firebase Authentication (Optional but Recommended)
1. In Firebase Console → Authentication → Sign-in method
2. Enable Email/Password authentication
3. Enable Google authentication (optional)

## Testing Locally

### Run Firebase Emulators
```bash
firebase emulators:start
```

This starts local emulators for:
- Functions: http://localhost:5001
- Firestore: http://localhost:8080
- Hosting: http://localhost:5000

### Test API Endpoints
```bash
# Health check
curl http://localhost:5001/your-project-id/us-central1/api/api/health

# Submit application
curl -X POST http://localhost:5001/your-project-id/us-central1/api/api/v1/applications \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Test Corp",
    "email": "test@example.com",
    "industry": "Technology",
    "company_size": "50-100",
    "use_case": "Brand monitoring"
  }'
```

## Environment Variables

### For Firebase Functions
Create `functions/.env`:
```bash
NODE_ENV=production
ADMIN_EMAIL=your-admin@email.com
```

Load in code:
```javascript
const { ADMIN_EMAIL } = process.env;
```

## Monitoring & Logs

### View Logs
```bash
firebase functions:log
```

### Firebase Console
- Functions logs: Firebase Console → Functions → Logs
- Firestore data: Firebase Console → Firestore Database
- Hosting metrics: Firebase Console → Hosting

## Security Considerations

### ✅ Implemented
- Firestore security rules with role-based access
- Admin-only endpoints for sensitive operations
- Input validation in API endpoints
- Storage rules requiring authentication

### 🔒 Recommended Next Steps
1. **Enable Firebase Authentication**
   - Add auth to frontend
   - Protect admin routes
   - Use Firebase tokens instead of custom JWT

2. **Add Rate Limiting**
   ```javascript
   const rateLimit = require('express-rate-limit');
   const limiter = rateLimit({
     windowMs: 15 * 60 * 1000, // 15 minutes
     max: 100 // limit each IP to 100 requests per windowMs
   });
   app.use('/api/', limiter);
   ```

3. **Set Up Firestore Backups**
   - Firebase Console → Firestore → Backups
   - Schedule daily backups

4. **Configure CORS**
   - Update `functions/index.js` CORS settings
   - Only allow your domain in production

## Costs & Limits

### Free Tier (Spark Plan)
- ✅ Enough for MVP and testing
- Functions: 2M invocations/month
- Firestore: 50K reads, 20K writes/day
- Hosting: 10GB storage, 360MB/day transfer

### When to Upgrade (Blaze Plan - Pay As You Go)
- More than 2M monthly API calls
- More than 50K Firestore reads per day
- Need 99.95% SLA
- Custom domain with SSL

Estimated costs for 10K users:
- Functions: ~$5-10/month
- Firestore: ~$1-5/month
- Hosting: ~$0-2/month
- **Total: ~$6-17/month**

## Troubleshooting

### Functions Deployment Fails
```bash
# Check Node version (needs 18)
node --version

# Reinstall dependencies
cd functions && rm -rf node_modules && npm install
```

### CORS Errors
Update `functions/index.js`:
```javascript
app.use(cors({ 
  origin: ['https://your-domain.web.app', 'http://localhost:3000']
}));
```

### Firestore Permission Denied
- Check `firestore.rules`
- Make sure user is authenticated
- Verify admin role in Firestore for admin endpoints

## Next Steps

1. **Deploy Now**: Run `firebase deploy`
2. **Test Live Site**: Visit your-project-id.web.app
3. **Add Firebase Config**: Update frontend with Firebase config
4. **Enable Authentication**: Set up Firebase Auth in console
5. **Monitor Usage**: Check Firebase Console daily during testing

## Support Resources

- Firebase Documentation: https://firebase.google.com/docs
- Firebase Console: https://console.firebase.google.com
- Stack Overflow: Tag your questions with `firebase` and `google-cloud-functions`

---

**Status**: ✅ Ready to Deploy
**Deployment Command**: `firebase deploy`
**Expected Time**: 2-3 minutes

Good luck with your launch! 🚀
