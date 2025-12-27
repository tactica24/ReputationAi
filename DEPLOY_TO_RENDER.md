# 🚀 Deploy to Render - Live in 5 Minutes!

## ✅ Code is Pushed to GitHub!

Your changes are now live on GitHub and ready to deploy to Render.

---

## 🌐 Deploy to Render (Make it Publicly Accessible)

### Option 1: Automatic Deploy via Blueprint (Recommended - 1 Click!)

**If you already have Render connected:**
- Render should automatically detect the push and start deploying
- Go to: https://dashboard.render.com
- Check your services - deployment should be in progress

**If this is your first deployment:**

1. **Go to Render Dashboard**:
   ```
   https://dashboard.render.com/select-repo?type=blueprint
   ```

2. **Connect GitHub Repository**:
   - Click "Connect account" (if not connected)
   - Authorize Render
   - Select: `tactica24/ReputationAi`

3. **Apply Blueprint**:
   - Render detects `render.yaml`
   - Click "Apply"
   - This creates:
     * 🗄️ PostgreSQL Database (`reputationai-db`)
     * 🌐 Backend Service (`reputationai-backend`)

4. **Wait for Deployment** (3-5 minutes):
   - Watch the logs
   - Wait for: "Application startup complete"

5. **Your Backend Will Be Live At**:
   ```
   https://reputationai-backend.onrender.com
   ```

### Option 2: Manual Deploy (If Blueprint Doesn't Work)

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repo: `tactica24/ReputationAi`
4. Configure:
   - **Name**: `reputationai-backend`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
5. Add Environment Variables (see below)
6. Click "Create Web Service"

---

## 🔧 Environment Variables (Render Dashboard)

After deployment starts, add these in Render Dashboard → Environment:

### Required Variables:
```
ENVIRONMENT=production
PYTHON_VERSION=3.12.0

# Email (Choose one)
EMAIL_PROVIDER=console
# Or for real emails:
# EMAIL_PROVIDER=smtp
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=your-email@gmail.com
# SMTP_PASSWORD=your-app-password

# Payment (for production)
PAYMENT_PROVIDER=test
# Or add real Stripe keys:
# STRIPE_SECRET_KEY=sk_live_your_key
# STRIPE_PUBLISHABLE_KEY=pk_live_your_key

# CORS (your frontend URL)
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

Render auto-generates:
- `DATABASE_URL` (from PostgreSQL database)
- `SECRET_KEY`
- `JWT_SECRET_KEY`

---

## ✅ Verify Deployment

Once deployed, test these URLs:

### 1. API Homepage:
```
https://reputationai-backend.onrender.com/
```

### 2. Health Check:
```
https://reputationai-backend.onrender.com/health
```

### 3. API Documentation:
```
https://reputationai-backend.onrender.com/api/docs
```

### 4. Submit Test Application:
```bash
curl -X POST https://reputationai-backend.onrender.com/api/onboarding/apply \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Test",
    "lastName": "User",
    "email": "test@example.com",
    "phone": "+1-555-0000",
    "title": "CEO",
    "entities": "Test User",
    "urgency": "proactive",
    "agreement": true,
    "privacy": true
  }'
```

---

## 📊 Monitor Your Deployment

### View Logs:
1. Go to Render Dashboard
2. Click on `reputationai-backend`
3. Click "Logs" tab
4. Watch for:
   ```
   ✅ Application startup complete
   INFO: Uvicorn running on http://0.0.0.0:10000
   ```

### Common Issues:

**Build Failed**:
- Check logs for missing dependencies
- Verify `requirements.txt` is up to date

**Database Connection Error**:
- Ensure PostgreSQL database is created
- Check `DATABASE_URL` environment variable

**Module Not Found**:
- Update start command to: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

---

## 🎯 What You'll Have After Deployment

### Public URLs:
- **Backend API**: `https://reputationai-backend.onrender.com`
- **API Docs**: `https://reputationai-backend.onrender.com/api/docs`
- **Database**: Managed PostgreSQL on Render

### Features Live:
- ✅ Application submission endpoint
- ✅ Admin onboarding with pricing
- ✅ Email service (console or real)
- ✅ Payment integration ready
- ✅ Secure document/video upload flow

### Next Steps:
1. Update frontend to use: `https://reputationai-backend.onrender.com`
2. Configure real email service
3. Add Stripe payment keys
4. Test complete flow

---

## 🔄 Auto-Deploy Setup

**Already enabled!** Every time you push to GitHub `main` branch:
1. Render detects the push
2. Automatically rebuilds
3. Deploys new version
4. Takes 2-3 minutes

---

## 🆘 Need Help?

**Check Deployment Status**:
https://dashboard.render.com

**View Logs**:
Dashboard → Your Service → Logs tab

**Test Endpoint**:
https://reputationai-backend.onrender.com/health

---

## 🎉 You're Done!

Your backend is now deployed and publicly accessible!

**Next**: Share the API URL with your team or integrate it with your frontend.

**API Base URL**: `https://reputationai-backend.onrender.com`
