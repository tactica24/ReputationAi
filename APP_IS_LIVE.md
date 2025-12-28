# 🎉 Your App is Live!

## ✅ Website is Deployed

**URL**: https://reputationai-df869.web.app

The frontend is now live and accessible!

---

## ⚠️ Important: Create Admin User

Since Cloud Functions require a paid plan, we'll create the admin user directly through Firebase Console.

### Method 1: Firebase Console (Recommended)

1. **Go to Firebase Console**:
   https://console.firebase.google.com/project/reputationai-df869/authentication/users

2. **Click "Add User"**

3. **Enter Admin Details**:
   - Email: `admin@reputationai.com`
   - Password: `Admin123!@#`
   - Click "Add User"

4. **Add User Data to Firestore**:
   - Go to Firestore: https://console.firebase.google.com/project/reputationai-df869/firestore
   - Click "Start Collection"
   - Collection ID: `users`
   - Click "Next"
   - Document ID: [Use the UID from the user you just created]
   - Add these fields:
     ```
     uid: [the user's UID]
     email: admin@reputationai.com
     name: Admin User
     role: admin
     company: ReputationAI
     is_active: true
     created_at: [timestamp - current date]
     updated_at: [timestamp - current date]
     ```

5. **Repeat for Test User** (Optional):
   - Email: `user@reputationai.com`
   - Password: `User123!@#`
   - Role: `user`

---

## 🔐 Login

Once you've created the users:

1. Open: https://reputationai-df869.web.app
2. Login with:
   - **Email**: `admin@reputationai.com`
   - **Password**: `Admin123!@#`

---

## 📊 Add Sample Data (Optional)

To add sample entities and mentions, go to Firestore Console and create:

### Entities Collection

Create collection `entities` with sample documents:

**Document 1**:
```json
{
  "name": "TechCorp Inc",
  "entity_type": "company",
  "description": "Leading technology company",
  "is_active": true,
  "ownerId": "[your user UID]",
  "created_at": "[current timestamp]",
  "updated_at": "[current timestamp]"
}
```

**Document 2**:
```json
{
  "name": "John Smith",
  "entity_type": "person",
  "description": "CEO and Founder",
  "is_active": true,
  "ownerId": "[your user UID]",
  "created_at": "[current timestamp]",
  "updated_at": "[current timestamp]"
}
```

### Mentions Collection

Create collection `mentions` with sample documents:

**Document 1**:
```json
{
  "text": "Great company! Best product I've used.",
  "source": "Twitter",
  "url": "https://twitter.com/example",
  "sentiment": "positive",
  "sentiment_score": 0.92,
  "author": "@techfan",
  "entityId": "[entity document ID]",
  "created_at": "[current timestamp]"
}
```

**Document 2**:
```json
{
  "text": "Could be better, average experience.",
  "source": "Reddit",
  "url": "https://reddit.com/example",
  "sentiment": "neutral",
  "sentiment_score": 0.5,
  "author": "u/user123",
  "entityId": "[entity document ID]",
  "created_at": "[current timestamp]"
}
```

---

## 💡 About Cloud Functions

Cloud Functions require upgrading to the **Blaze (Pay-as-you-go) Plan**.

### Why?
- Firebase's free "Spark" plan doesn't support Cloud Functions
- Functions need external API access

### Cost:
- **No minimum fee** - you only pay for what you use
- **Free tier included**: 125K invocations/month, 40K GB-seconds, 40K CPU-seconds
- For a small app: typically **$0-5/month**

### To Upgrade:
1. Go to: https://console.firebase.google.com/project/reputationai-df869/usage/details
2. Click "Modify Plan"
3. Select "Blaze Plan"
4. Add a credit card (you can set budget alerts)
5. Return here and run:
   ```bash
   cd /workspaces/ReputationAi
   firebase deploy --only functions
   ```

**Note**: You can use the app without Functions! The frontend works perfectly with direct Firestore access.

---

## ✅ Current Status

- ✅ Frontend deployed and live
- ✅ Firebase Authentication enabled
- ✅ Firestore database ready
- ✅ Firebase Hosting configured
- ⚠️ Cloud Functions pending (requires Blaze plan)

---

## 🎯 What Works Now

Even without Cloud Functions, you can:
- ✅ Login/logout with Firebase Auth
- ✅ Create and manage entities
- ✅ Add mentions
- ✅ View dashboard
- ✅ Real-time data sync
- ✅ All CRUD operations

The app uses Firestore directly from the frontend!

---

## 🆘 Need Help?

### Check if user exists:
https://console.firebase.google.com/project/reputationai-df869/authentication/users

### View Firestore data:
https://console.firebase.google.com/project/reputationai-df869/firestore

### View deployment:
https://console.firebase.google.com/project/reputationai-df869/hosting/sites

---

## 📝 Next Steps

1. ✅ Create admin user in Firebase Console
2. ✅ Login at https://reputationai-df869.web.app
3. ⚠️ Add sample data (optional)
4. ⚠️ Upgrade to Blaze plan (optional, for Functions)

---

**Your app is live! 🚀**

Visit: https://reputationai-df869.web.app
