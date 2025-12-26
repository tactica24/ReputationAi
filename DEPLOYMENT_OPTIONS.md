# Deployment Guide - ReputationAI

## 🎯 Current Architecture

**Backend**: FastAPI (Python) - Requires Python runtime
**Frontend**: React + Vite - Static build output
**Database**: PostgreSQL + MongoDB (currently using mock data)

---

## 🚀 Deployment Options

### Option 1: Vercel (Frontend) + Render (Backend) ⭐ RECOMMENDED

#### Advantages:
- ✅ Free tiers for both
- ✅ Automatic deployments from GitHub
- ✅ Easy setup (5-10 minutes)
- ✅ Great performance
- ✅ Built-in SSL/HTTPS

#### Setup Steps:

##### 1️⃣ Deploy Backend to Render
```bash
# Create render.yaml (already provided below)
# Push to GitHub
# Connect GitHub to Render
# Render will auto-deploy
```

##### 2️⃣ Deploy Frontend to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd frontend
vercel

# Follow the prompts:
# - Set up and deploy: Yes
# - Scope: Your account
# - Link to existing project: No
# - Project name: reputationai
# - Directory: ./ (current directory)
# - Build command: npm run build
# - Output directory: dist
```

##### 3️⃣ Set Up Databases (Free Tiers)

**PostgreSQL** - Neon (Free):
- Sign up: https://neon.tech
- Create database
- Copy connection string

**MongoDB** - Atlas (Free):
- Sign up: https://www.mongodb.com/cloud/atlas
- Create free cluster (M0)
- Create database user
- Get connection string

##### 4️⃣ Environment Variables

**Backend (Render)**:
```env
DATABASE_URL=postgresql://user:pass@neon.tech/db
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/db
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

**Frontend (Vercel)**:
```env
VITE_API_URL=https://your-render-app.onrender.com/api/v1
VITE_ENVIRONMENT=production
```

---

### Option 2: Railway (All-in-One) 💎

Deploy everything in one platform!

#### Advantages:
- ✅ $5 free credit/month
- ✅ Deploy backend, frontend, and databases together
- ✅ Simple dashboard
- ✅ One-click PostgreSQL and MongoDB

#### Setup Steps:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Add services:
# - PostgreSQL (one-click)
# - MongoDB (template)
# - Python service (backend)
# - Static service (frontend build)
```

---

### Option 3: Fly.io (Backend) + Vercel (Frontend)

#### Advantages:
- ✅ Free tier includes 3 VMs
- ✅ Great for Python/FastAPI
- ✅ Global edge network

#### Setup Steps:
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Initialize (in backend directory)
cd backend
flyctl launch

# Deploy
flyctl deploy
```

---

## 📦 Pre-Deployment Checklist

### ✅ 1. Create Production Build Configuration

**Frontend**: Already configured in `vite.config.js`

**Backend**: Create `render.yaml`:
```yaml
services:
  - type: web
    name: reputationai-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.12
```

### ✅ 2. Update CORS Origins

Update `backend/main.py` to allow your frontend URL:
```python
origins = [
    "https://your-frontend.vercel.app",
    "http://localhost:3000",
]
```

### ✅ 3. Set Up Environment Variables

Create `.env` files (add to `.gitignore`):
```bash
# Never commit these files!
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".env.production" >> .gitignore
```

### ✅ 4. Database Migration

Replace mock data with real database connections:
- Set up PostgreSQL schema
- Set up MongoDB collections
- Run migrations: `alembic upgrade head`

---

## 🎬 Quick Start - Deploy in 10 Minutes

### Fastest Path: Vercel + Render

```bash
# 1. Push latest code to GitHub
git add -A
git commit -m "Ready for production deployment"
git push origin main

# 2. Deploy Frontend to Vercel (2 minutes)
cd frontend
npx vercel --prod

# 3. Deploy Backend to Render (via Dashboard - 3 minutes)
# Go to: https://dashboard.render.com
# - Click "New +"
# - Select "Web Service"
# - Connect GitHub repo: ReputationAi
# - Root directory: . (leave empty)
# - Build command: pip install -r requirements.txt
# - Start command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
# - Click "Create Web Service"

# 4. Set up databases (5 minutes)
# Neon: https://console.neon.tech
# MongoDB Atlas: https://cloud.mongodb.com
```

---

## 🔧 Post-Deployment Configuration

### Update Frontend API URL
Once backend is deployed, update frontend environment variable:

**On Vercel Dashboard**:
- Settings → Environment Variables
- Add: `VITE_API_URL = https://your-backend.onrender.com/api/v1`
- Redeploy

### Test Production URLs
```bash
# Backend health check
curl https://your-backend.onrender.com/health

# Frontend
open https://your-frontend.vercel.app
```

---

## 💡 Cost Breakdown (Free Tier)

| Service | Free Tier | Limit |
|---------|-----------|-------|
| **Vercel** | Yes | 100 GB bandwidth/month |
| **Render** | Yes | 750 hours/month |
| **Neon** | Yes | 3 GB storage |
| **MongoDB Atlas** | Yes | 512 MB storage |
| **Railway** | $5 credit | ~20 hours/month |

**Total Monthly Cost**: **$0** (using free tiers)

---

## 🚨 Important Notes

### Backend Limitations on Free Tier
- **Render Free**: App sleeps after 15 min of inactivity (cold starts ~30s)
- **Railway**: $5 credit = ~140 hours (not 24/7)
- **Fly.io**: 3 VMs shared across all apps

### Recommendation for Production
- Start with free tiers for testing
- Upgrade to paid when you have users:
  - Render: $7/month (no sleep)
  - Railway: $5/month + usage
  - Vercel: Usually stays free

---

## 📞 Support & Resources

**Vercel Docs**: https://vercel.com/docs
**Render Docs**: https://render.com/docs
**Railway Docs**: https://docs.railway.app
**Neon Docs**: https://neon.tech/docs
**MongoDB Atlas**: https://docs.atlas.mongodb.com

---

## Next Steps

Choose your deployment option and follow the setup steps above. The **Vercel + Render** combination is recommended for beginners due to its simplicity and generous free tiers.
