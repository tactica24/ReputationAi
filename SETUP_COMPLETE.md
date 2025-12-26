# 🎯 Complete Setup Guide - ReputationAI

## Your SECRET_KEY (Save This!)
```
UvLKMdV5dxSVwL6WrpJ8mM3vIXUhJD7oyYGUfewu8zs
```

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### STEP 1: Create PostgreSQL Database (2 minutes)

**Instructions:**
1. Open in new tab: https://neon.tech
2. Click "Sign up" → Use GitHub
3. After login, click "Create a project"
   - Name: `ReputationAI`
   - Region: Choose closest to you
   - Click "Create"
4. Copy the connection string shown (looks like this):
   ```
   postgresql://username:password@ep-xxxx-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
5. **PASTE IT HERE:** ________________________________

**✅ Done? Check this box: [ ]**

---

### STEP 2: Create MongoDB Database (2 minutes)

**Instructions:**
1. Open in new tab: https://www.mongodb.com/cloud/atlas/register
2. Sign up → Choose "Shared" (Free tier)
3. Create cluster:
   - Provider: AWS
   - Region: Choose closest
   - Cluster Name: `ReputationAI`
   - Click "Create"
4. Security:
   - **Database Access:** Click "Add New Database User"
     - Username: `reputationai`
     - Password: (auto-generate and SAVE IT)
     - Click "Add User"
   - **Network Access:** Click "Add IP Address"
     - Choose "Allow Access from Anywhere" (0.0.0.0/0)
     - Click "Confirm"
5. Get Connection String:
   - Click "Connect" → "Connect your application"
   - Copy the string (looks like this):
   ```
   mongodb+srv://reputationai:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
   - Replace `<password>` with your actual password
6. **PASTE IT HERE:** ________________________________

**✅ Done? Check this box: [ ]**

---

### STEP 3: Deploy Backend to Render (3 minutes)

**Instructions:**
1. Open: https://dashboard.render.com/register
2. Sign up with GitHub → Authorize Render
3. Click "New +" → "Web Service"
4. Click "Connect account" if not already connected
5. Find and select repository: `tactica24/ReputationAi`
6. Click "Connect"
7. Configuration (some will auto-fill from render.yaml):
   - **Name:** `reputationai-backend`
   - **Region:** Oregon (US West) or closest
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Free
8. **IMPORTANT - Add Environment Variables:**
   Click "Advanced" → "Add Environment Variable" for EACH:
   
   ```
   Key: DATABASE_URL
   Value: [YOUR NEON POSTGRESQL URL FROM STEP 1]
   
   Key: MONGODB_URI
   Value: [YOUR MONGODB URL FROM STEP 2]
   
   Key: SECRET_KEY
   Value: UvLKMdV5dxSVwL6WrpJ8mM3vIXUhJD7oyYGUfewu8zs
   
   Key: CORS_ORIGINS
   Value: *
   
   Key: ENVIRONMENT
   Value: production
   ```

9. Click "Create Web Service"
10. Wait 3-5 minutes for deployment
11. Your backend URL will be shown at the top (e.g., `https://reputationai-backend-xxxx.onrender.com`)
12. **PASTE BACKEND URL HERE:** ________________________________

**✅ Done? Check this box: [ ]**

**Test Backend:**
```bash
curl YOUR_BACKEND_URL/api/v1/health
```
Should return: `{"status":"healthy",...}`

---

### STEP 4: Deploy Frontend to Vercel (2 minutes)

**Run these commands in order:**

```bash
# 1. Login to Vercel
cd /workspaces/ReputationAi
vercel login
# (Opens browser - login with GitHub)

# 2. Deploy frontend
cd frontend
vercel --prod

# Follow prompts:
# - Set up and deploy? YES
# - Which scope? [Your account]
# - Link to existing project? NO
# - Project name? reputationai (or your choice)
# - Override settings? NO

# 3. After deployment, set backend URL
# Replace YOUR_BACKEND_URL with URL from Step 3
vercel env add VITE_API_URL production
# When prompted, enter: YOUR_BACKEND_URL/api/v1

# 4. Redeploy with environment variable
vercel --prod
```

**Your frontend URL will be shown** (e.g., `https://reputationai-xxxx.vercel.app`)

**PASTE FRONTEND URL HERE:** ________________________________

**✅ Done? Check this box: [ ]**

---

### STEP 5: Update CORS (1 minute)

**Instructions:**
1. Go back to Render dashboard
2. Click on your `reputationai-backend` service
3. Click "Environment" in left sidebar
4. Find `CORS_ORIGINS` variable
5. Click "Edit"
6. Change value to: `YOUR_FRONTEND_URL,http://localhost:3000`
   (Replace YOUR_FRONTEND_URL with URL from Step 4)
7. Click "Save Changes"
8. Service will auto-redeploy (30 seconds)

**✅ Done? Check this box: [ ]**

---

## 🎉 VERIFICATION

### Test Your Deployment:

1. **Backend Health Check:**
   ```bash
   curl YOUR_BACKEND_URL/api/v1/health
   ```
   Expected: `{"status":"healthy","database":{"postgresql":true,"mongodb":true}}`

2. **Frontend:**
   - Open: YOUR_FRONTEND_URL
   - Should load homepage
   - Check browser console (F12) - no errors

3. **Full Integration Test:**
   - Go to homepage
   - Fill out "Get Protection" form
   - Submit
   - Should see success message
   - Check Render logs to see database insert

---

## 🗄️ OPTIONAL: Create Admin User

**Connect to Neon Database:**
1. Go to: https://console.neon.tech
2. Click your project
3. Click "SQL Editor"
4. Run this SQL:

```sql
INSERT INTO users (
  email, 
  username, 
  hashed_password, 
  full_name, 
  role, 
  is_active, 
  is_verified, 
  gdpr_consent,
  created_at
) VALUES (
  'admin@reputationai.com',
  'admin',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewKq.iQA/U7J7VYu',
  'Admin User',
  'admin',
  true,
  true,
  true,
  NOW()
);
```

**Login credentials:**
- Email: `admin@reputationai.com`
- Password: `admin123`

**⚠️ IMPORTANT:** Change this password after first login!

---

## 📊 YOUR DEPLOYMENT SUMMARY

Once complete, fill this in:

```
✅ Frontend URL: ________________________________
✅ Backend URL:  ________________________________
✅ PostgreSQL:   Neon.tech (Free tier - 3GB)
✅ MongoDB:      Atlas (Free tier - 512MB)
✅ Cost:         $0/month
✅ Status:       🟢 LIVE
```

---

## 🔧 FUTURE UPDATES

**Update Frontend:**
```bash
git add -A
git commit -m "update: Your changes"
git push origin main
cd frontend && vercel --prod
```

**Update Backend:**
```bash
git add -A
git commit -m "update: Your changes"
git push origin main
# Render auto-deploys from GitHub!
```

---

## 🚨 TROUBLESHOOTING

**Backend won't start:**
- Check Render logs for errors
- Verify all 5 environment variables are set
- Check DATABASE_URL format is correct

**Frontend can't reach backend:**
- Check VITE_API_URL in Vercel dashboard
- Verify CORS_ORIGINS includes your frontend URL
- Open browser console for errors

**Database connection failed:**
- PostgreSQL: Check Neon connection string
- MongoDB: Verify password and IP whitelist (0.0.0.0/0)

---

## 📞 MONITORING

**Render Logs:**
- Dashboard → Service → Logs tab
- Real-time backend logs

**Vercel Logs:**
- Dashboard → Project → Deployments
- Build and runtime logs

**Database Monitoring:**
- Neon: https://console.neon.tech
- MongoDB: https://cloud.mongodb.com

---

## ⚡ FREE TIER LIMITS

| Service | Limit | Notes |
|---------|-------|-------|
| Render | 750 hrs/month | Sleeps after 15 min (30s wake) |
| Vercel | 100 GB/month | More than enough |
| Neon | 3 GB storage | Plenty for start |
| MongoDB | 512 MB storage | Good for documents |

**Total Cost:** $0/month 🎉

---

**Ready to deploy?** Start with Step 1!
