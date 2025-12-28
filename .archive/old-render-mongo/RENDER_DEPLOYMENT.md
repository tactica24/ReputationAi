# 🚀 Deploy Backend to Render

Complete step-by-step guide to get your backend live on Render.

## Prerequisites

✅ Render account created  
✅ GitHub repository connected  
✅ render.yaml configuration ready

## Step 1: Connect Repository to Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → Select **"Blueprint"**
3. **Connect GitHub Repository**:
   - Click "Connect account" if not connected
   - Authorize Render to access your GitHub
   - Select repository: `tactica24/ReputationAi`
4. **Deploy Blueprint**:
   - Render will automatically detect `render.yaml`
   - Click "Apply" to create services

## Step 2: What Gets Created Automatically

Render will create:

### 🗄️ PostgreSQL Database
- **Name**: `reputationai-db`
- **Plan**: Free (256 MB storage, expires after 90 days)
- **Region**: Oregon
- **Connection**: Automatically linked to backend

### 🌐 Backend Web Service
- **Name**: `reputationai-backend`
- **Plan**: Free (750 hours/month)
- **Python Version**: 3.12
- **Auto-deploy**: Enabled on git push

## Step 3: Monitor Deployment

1. **Watch Build Logs**:
   - Click on `reputationai-backend` service
   - View "Logs" tab
   - Wait for: `Application startup complete`

2. **Expected Build Time**: 3-5 minutes

3. **Success Indicators**:
   ```
   ✅ Installing dependencies from requirements.txt
   ✅ Starting uvicorn server
   ✅ Application startup complete
   ✅ Uvicorn running on http://0.0.0.0:XXXXX
   ```

## Step 4: Get Your Backend URL

Once deployed, you'll get a URL like:
```
https://reputationai-backend.onrender.com
```

**Find it here:**
- Render Dashboard → `reputationai-backend` → Top of page

## Step 5: Initialize Production Database

After first deployment, you need to create the admin user:

1. **Go to Render Dashboard** → `reputationai-backend`
2. **Click "Shell"** tab (top right)
3. **Run this command**:
   ```bash
   python backend/init_production_db.py
   ```

4. **Verify Output**:
   ```
   🚀 Initializing production database...
   📋 Creating database tables...
   ✅ Tables created successfully!
   👤 Creating super admin user...
   ✅ Admin user created successfully!
      Email: admin@reputation.ai
      Password: Admin@2024!
   ```

## Step 6: Test Your Backend

Test the deployed backend:

```bash
# Health check
curl https://YOUR-BACKEND-URL.onrender.com/health

# Test login
curl -X POST https://YOUR-BACKEND-URL.onrender.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@reputation.ai","password":"Admin@2024!"}'
```

**Expected Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {...}
}
```

## Step 7: Update Frontend to Use Live Backend

I'll update your frontend environment variables to point to the live backend.

**Current Status:**
- ❌ Frontend using mock authentication
- ❌ No real backend connection

**After Update:**
- ✅ Frontend connects to Render backend
- ✅ Real database authentication
- ✅ Live data and alerts

## Render Free Tier Limits

| Resource | Free Tier | Notes |
|----------|-----------|-------|
| **Web Service** | 750 hrs/month | Enough for 1 app 24/7 |
| **PostgreSQL** | 256 MB | Expires after 90 days |
| **Bandwidth** | 100 GB/month | More than enough |
| **Auto-sleep** | After 15 min idle | Wakes in ~30 seconds |

## Important Notes

### ⚠️ Database Expiration
The free PostgreSQL database **expires after 90 days**. Before expiration:
- Upgrade to paid plan ($7/month)
- Or export data and create new free database

### 🌙 Auto-Sleep Behavior
Free tier services sleep after 15 minutes of inactivity:
- First request takes ~30 seconds (cold start)
- Subsequent requests are instant
- No data loss during sleep

### 🔄 Auto-Deploy
Every `git push` to main branch triggers:
- Automatic rebuild
- Automatic deployment
- ~3-5 minute deployment time

## Troubleshooting

### Build Fails
**Check:**
- `requirements.txt` has all dependencies
- Python version compatibility (3.12)
- Environment variables set correctly

**Fix:**
- View build logs in Render dashboard
- Common issue: missing dependencies

### Database Connection Error
**Check:**
- DATABASE_URL environment variable
- PostgreSQL service is running
- Database initialization completed

**Fix:**
```bash
# In Render Shell
python backend/init_production_db.py
```

### API Returns 404
**Check:**
- Correct URL format: `https://YOUR-APP.onrender.com/api/v1/...`
- Service is running (not sleeping)
- Routes registered in `backend/main.py`

## Next Steps

After backend is live:

1. ✅ Backend deployed on Render
2. ⏭️ Update frontend environment variables
3. ⏭️ Deploy updated frontend to Vercel
4. ⏭️ Test complete authentication flow
5. ⏭️ Set up monitoring and alerts

---

**Ready to proceed?** Just let me know once your Render deployment completes, and I'll update the frontend to connect to your live backend! 🚀
