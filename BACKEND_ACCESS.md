# 🚀 Backend Access Guide - Quick Reference

## ✅ Your Backend is Running!

**Base URL**: http://localhost:8080

---

## 📍 Available Endpoints

### Public Endpoints (No Authentication Required)

#### 1. **Root / API Info**
```
GET http://localhost:8080/
```
Shows API version and available endpoints

#### 2. **Health Check**
```
GET http://localhost:8080/health
```
Returns server health status

#### 3. **API Documentation** (BEST WAY TO TEST!)
```
GET http://localhost:8080/api/docs
```
**👉 OPEN THIS IN YOUR BROWSER** - Interactive API testing interface

#### 4. **Submit Application** (User submits request)
```bash
curl -X POST http://localhost:8080/api/onboarding/apply \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "phone": "+1-555-0000",
    "title": "CEO",
    "entities": "John Doe, My Company",
    "urgency": "proactive",
    "agreement": true,
    "privacy": true
  }'
```

### Admin Endpoints

#### 5. **Create Subscription Offer** (Admin assigns pricing)
```bash
curl -X POST http://localhost:8080/api/admin/onboarding/create-offer \
  -H "Content-Type: application/json" \
  -d '{
    "application_id": "APP-123",
    "user_email": "client@example.com",
    "tier": "enterprise",
    "monthly_price": 4997,
    "discount_percent": 10,
    "custom_features": ["Priority support"],
    "notes": "VIP client"
  }'
```

This will:
- ✅ Create subscription offer
- ✅ Generate secure links
- ✅ Send email to user (printed to console in dev mode)

#### 6. **Get Offer Details**
```bash
curl http://localhost:8080/api/admin/onboarding/offers/OFFER-ID
```

---

## 🧪 Easy Testing Methods

### Method 1: Browser (Easiest!)
Open: **http://localhost:8080/api/docs**

This gives you:
- Interactive interface
- Try out all endpoints
- See request/response formats
- No need for curl commands

### Method 2: Run Test Script
```bash
cd /workspaces/ReputationAi
export PYTHONPATH=/workspaces/ReputationAi:$PYTHONPATH
python backend/test_admin_onboarding.py
```

This runs the complete flow:
1. Submit application
2. Create admin offer
3. Show email content
4. Complete onboarding

### Method 3: Frontend Form
Open the landing page and use the application form:
```bash
# In VS Code, right-click index.html → "Open with Live Server"
# Or open directly: file:///workspaces/ReputationAi/index.html
```

---

## 📧 Email Setup Status

**Current**: Console mode (emails print to terminal)

**To use real emails**:

Edit `/workspaces/ReputationAi/.env`:

### Gmail Option:
```env
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
```

### SendGrid Option:
```env
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=SG.your_api_key
```

Backend will auto-reload when you save .env

---

## 🔍 Troubleshooting

### "Not Found" Error
✅ **FIXED!** The root endpoint now works
- Try: http://localhost:8080/
- Or: http://localhost:8080/api/docs

### "Connection Refused"
❌ Backend not running
```bash
cd /workspaces/ReputationAi/backend
./start.sh
```

### Backend Logs
Check the terminal where you started the backend to see:
- Request details
- Email content (in console mode)
- Any errors

---

## 🎯 Common Tasks

### See All Endpoints
http://localhost:8080/api/docs

### Test Application Flow
http://localhost:8080/api/docs → `/api/onboarding/apply` → Try it out

### Create Admin Offer
http://localhost:8080/api/docs → `/api/admin/onboarding/create-offer` → Try it out

### Check Email Output
Look at the backend terminal - emails print there in console mode

---

## 📱 Quick Links

- **API Docs**: http://localhost:8080/api/docs
- **Health**: http://localhost:8080/health
- **Root**: http://localhost:8080/

**Backend is running and ready to go!** 🎉
