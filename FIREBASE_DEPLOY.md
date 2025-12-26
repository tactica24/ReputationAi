# Firebase Deployment Guide

## Step 1: Login to Firebase
```bash
firebase login
```
Follow the prompts and login with your Google account.

## Step 2: Initialize Firebase (if needed)
```bash
firebase init hosting
```
- Select "Use an existing project" or create new
- Public directory: `frontend/dist`
- Single-page app: Yes
- Automatic builds with GitHub: No (for now)

## Step 3: Build Frontend
```bash
cd frontend
npm run build
cd ..
```

## Step 4: Deploy
```bash
firebase deploy --only hosting
```

## Your MongoDB Connection (SAVE THIS):
```
mongodb+srv://okwafa_db_user:MyPass123@cluster0.ewqncgb.mongodb.net/reputationai
```

⚠️ **IMPORTANT**: Change your MongoDB password! It was exposed in the terminal.

## Next Steps:
1. Login to MongoDB Atlas
2. Change the password for user `okwafa_db_user`
3. Update the connection string everywhere you used it
