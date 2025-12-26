# 🚀 Quick Deployment Guide - ReputationAI

## Status: Ready for Production Deployment

All code has been updated to use **real databases** instead of mock data. The application is now production-ready!

---

## 📋 Pre-Deployment Checklist

✅ Backend configured with PostgreSQL + MongoDB  
✅ Mock data removed - all endpoints use database
✅ Environment variables configured  
✅ Health check endpoint added (`/api/v1/health`)  
✅ CORS properly configured  
✅ Database models and CRUD operations complete  
✅ Admin dashboard with real data  
✅ Application submission saves to database  

---

## 🎯 Deployment Steps

### Step 1: Set Up Free Databases (5 minutes)

#### A. PostgreSQL - Neon (Free)
1. Go to: https://neon.tech
2. Sign up/Login with GitHub
3. Create a new project: "ReputationAI"
4. Copy the connection string:
   ```
   postgresql://[user]:[password]@[host]/[database]
   ```
5. **Save this URL** - you'll need it for Render

#### B. MongoDB - Atlas (Free)
1. Go to: https://www.mongodb.com/cloud/atlas
2. Sign up/Login
3. Create free M0 cluster
4. Database Access → Add user (username/password)
5. Network Access → Add IP: `0.0.0.0/0` (allow all)
6. Copy connection string:
   ```
   mongodb+srv://[username]:[password]@cluster0.xxxxx.mongodb.net/reputationai
   ```
7. **Save this URL** - you'll need it for Render

---

### Step 2: Deploy Backend to Render (3 minutes)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign up with GitHub (recommended)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub account if not already connected
   - Select repository: `tactica24/ReputationAi`
   - Click "Connect"

3. **Configure Service** (Render auto-detects render.yaml)
   - Name: `reputationai-backend`
   - Region: Choose closest to you
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Instance Type: **Free**

4. **Add Environment Variables**
   Click "Environment" → Add these variables:
   
   ```env
   DATABASE_URL = [your-neon-postgresql-url]
   MONGODB_URI = [your-mongodb-atlas-url]
   SECRET_KEY = your-random-secret-key-here-min-32-chars
   CORS_ORIGINS = *
   ENVIRONMENT = production
   ```

   To generate SECRET_KEY:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Your backend URL will be: `https://reputationai-backend-xxxx.onrender.com`
   - **Copy this URL** - you'll need it for frontend

---

### Step 3: Deploy Frontend to Vercel (2 minutes)

1. **Install Vercel CLI** (already done):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```
   - Follow the prompts to authenticate

3. **Deploy Frontend**:
   ```bash
   cd /workspaces/ReputationAi
   vercel --prod
   ```

4. **Follow the prompts**:
   - Set up and deploy? **Yes**
   - Which scope? Select your account
   - Link to existing project? **No**
   - Project name? `reputationai` or your choice
   - Directory? **./frontend** (IMPORTANT!)
   - Override settings? **No**

5. **Set Environment Variable**:
   After deployment, add the backend URL:
   ```bash
   vercel env add VITE_API_URL production
   ```
   Enter value: `https://reputationai-backend-xxxx.onrender.com/api/v1`
   (Replace with your actual Render backend URL)

6. **Redeploy with Environment Variable**:
   ```bash
   vercel --prod
   ```

7. **Your frontend URL**:
   ```
   https://reputationai-xxxx.vercel.app
   ```

---

### Step 4: Update CORS on Backend

1. Go back to Render dashboard
2. Your backend service → Environment
3. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS = https://your-vercel-frontend-url.vercel.app,http://localhost:3000
   ```
4. Save changes (auto-redeploys)

---

## ✅ Verify Deployment

### 1. Check Backend Health
```bash
curl https://your-backend-url.onrender.com/api/v1/health
```
Expected response:
```json
{
  "status": "healthy",
  "database": {
    "postgresql": true,
    "mongodb": true
  },
  "timestamp": "2025-12-26T..."
}
```

### 2. Check Frontend
- Visit: `https://your-frontend-url.vercel.app`
- Should load without errors
- Check browser console for API connection

### 3. Test Application Submission
- Go to homepage
- Fill out "Get Protection" form
- Submit application
- Check Render logs to see database insert

### 4. Test Admin Dashboard (Optional)
- Create admin user in database OR
- Temporarily modify `get_current_user` to return admin role
- Visit: `https://your-frontend-url.vercel.app/admin`

---

## 🗄️ Database Initial Setup (Optional)

### Create Admin User
Connect to your Neon database and run:

```sql
INSERT INTO users (
  email, 
  username, 
  hashed_password, 
  full_name, 
  role, 
  is_active, 
  is_verified, 
  gdpr_consent
) VALUES (
  'admin@reputationai.com',
  'admin',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewKq.iQA/U7J7VYu', -- password: admin123
  'Admin User',
  'admin',
  true,
  true,
  true
);
```

**Important**: Change the password immediately after first login!

---

## 📊 Monitor Your Deployment

### Render Logs
- Dashboard → Your Service → Logs tab
- Real-time application logs
- Look for database connection success/errors

### Vercel Deployment Logs
- Dashboard → Your Project → Deployments
- Build logs and runtime logs

---

## 🎉 You're Live!

Your application is now deployed with:
- ✅ **Frontend**: Vercel (https://your-app.vercel.app)
- ✅ **Backend**: Render (https://your-backend.onrender.com)
- ✅ **Database**: Neon PostgreSQL (Free tier)
- ✅ **NoSQL**: MongoDB Atlas (Free tier)
- ✅ **Cost**: $0/month (all free tiers!)

---

## 🔄 Future Deployments

### Update Frontend
```bash
cd /workspaces/ReputationAi
git push origin main
vercel --prod
```

### Update Backend
Just push to GitHub - Render auto-deploys:
```bash
git push origin main
```

---

## 🚨 Important Notes

### Free Tier Limitations
1. **Render Free**: App sleeps after 15 min inactivity
   - First request after sleep: ~30 seconds
   - Solution: Use UptimeRobot to ping every 14 minutes

2. **Vercel Free**: 100 GB bandwidth/month
   - More than enough for testing and small-scale deployment

3. **Neon Free**: 3 GB storage
   - Plenty for early stage

4. **MongoDB Atlas Free**: 512 MB storage
   - Good for document storage

### Security Checklist
- [ ] Change all default passwords
- [ ] Update SECRET_KEY to strong random value
- [ ] Enable HTTPS only (default on Vercel/Render)
- [ ] Set up proper CORS origins (not `*`)
- [ ] Enable database backups
- [ ] Set up monitoring/alerting

---

## 🆘 Troubleshooting

### Backend won't start
- Check Render logs for errors
- Verify DATABASE_URL is correct
- Check Python version (should be 3.12)

### Frontend can't reach backend
- Check VITE_API_URL environment variable
- Check CORS_ORIGINS on backend
- Look at browser console for errors

### Database connection failed
- Verify connection strings
- Check network access (MongoDB)
- Ensure databases are running

---

## 📞 Need Help?

1. Check Render logs: Dashboard → Service → Logs
2. Check Vercel logs: Dashboard → Project → Deployments
3. Test health endpoint: `/api/v1/health`
4. Review error messages in browser console

---

**Ready to Deploy?** Start with Step 1 above! 🚀
