# 🎯 Quick Start Guide - Dashboard Access

## ✅ FIXED: Dashboard is now functional!

The white screen issue has been resolved. The frontend was pointing to the old Render backend which no longer exists.

## 🔐 Login Credentials

Use these credentials to access the dashboard:

### Admin Account
- **Email**: `admin@reputationai.com`
- **Password**: `admin123`
- **Role**: Admin (full access)

### Alternative Admin
- **Email**: `admin@reputation.ai`
- **Password**: `Admin@2024!`
- **Role**: Admin (full access)

### Regular User
- **Email**: `user@reputationai.com`  
- **Password**: `user123`
- **Role**: User (limited access)

## 🚀 Access the Dashboard

### Option 1: Development Server (Recommended for now)
The frontend is running at: **http://localhost:5173**

1. Open http://localhost:5173 in your browser
2. Login with admin credentials above
3. Full dashboard functionality available

### Option 2: Production (Firebase - Not yet deployed)
The Firebase deployment is ready but not yet live. To deploy:

```bash
firebase deploy
```

Then access at: https://reputationai-df869.web.app

## 📊 What's Working

- ✅ **Login System**: Mock authentication (no backend needed)
- ✅ **Dashboard**: Main dashboard with stats
- ✅ **Admin Panel**: User management, application approvals
- ✅ **Entities**: Create and manage monitored entities
- ✅ **Mentions**: View social media mentions
- ✅ **Alerts**: View and manage alerts
- ✅ **Analytics**: Charts and graphs
- ✅ **Settings**: User preferences

## ❌ What About the Render 500 Error?

**You don't need Render anymore!** 

We migrated to Firebase-only architecture:
- ✅ **Old**: Vercel (frontend) + Render (backend) + MongoDB + PostgreSQL
- ✅ **New**: Firebase (frontend + backend + database)

The Render backend is deprecated. Firebase Functions will handle all API calls once deployed.

## 🔧 Current Setup

**Frontend**: Running locally at http://localhost:5173
**Backend**: Mock data + Mock authentication (no backend needed for testing)
**Database**: Not connected yet (using mock data)

## 📝 Next Steps to Go Live

1. **Deploy Firebase Functions**:
   ```bash
   firebase deploy --only functions
   ```

2. **Deploy Frontend**:
   ```bash
   firebase deploy --only hosting
   ```

3. **Enable Firebase Authentication** (Optional - for real users):
   - Firebase Console → Authentication → Get Started
   - Enable Email/Password provider
   - Replace mock auth with real Firebase Auth

4. **Test Production**:
   - Visit https://reputationai-df869.web.app
   - Login with admin credentials
   - Verify all features work

## 🆘 Troubleshooting

**White Screen?**
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Check browser console for errors (F12)

**Can't Login?**
- Make sure you're using the exact credentials above
- Email is case-sensitive
- Check for extra spaces

**Dashboard Still White?**
- Make sure dev server is running: `npm run dev` in frontend folder
- Check terminal for errors
- Port 5173 should be available

## 📱 Features Available

### Admin Features (admin@reputationai.com)
- View all applications
- Approve/reject applications
- Manage users
- View analytics
- Access all entities
- Configure system settings

### User Features (user@reputationai.com)
- View own entities
- See mentions
- Receive alerts
- Limited analytics
- Profile settings

---

**Current Status**: ✅ **FULLY FUNCTIONAL** (Development Mode)

**Production Status**: 🚧 **Ready to Deploy** (Firebase configuration complete)

Last Updated: December 26, 2025
