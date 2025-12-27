# Backend Setup & Access Guide

## 🚀 Quick Start - Access the Backend

### Step 1: Install Dependencies

```bash
cd /workspaces/ReputationAi/backend
pip install -r ../requirements.txt
```

### Step 2: Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cd /workspaces/ReputationAi
cp .env.example .env
```

Then edit `.env` with your configuration (see below).

### Step 3: Start the Backend

```bash
cd /workspaces/ReputationAi/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

The backend will be accessible at:
- **Local**: http://localhost:8080
- **API Docs**: http://localhost:8080/api/docs
- **Health Check**: http://localhost:8080/health

---

## 📧 Email Configuration

### Option 1: SendGrid (Recommended - FREE for 100 emails/day)

1. **Sign up for SendGrid**:
   - Go to https://sendgrid.com/
   - Create free account
   - Get your API key

2. **Add to `.env`**:
```env
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=your_sendgrid_api_key_here
EMAIL_FROM=noreply@reputationguardian.com
EMAIL_FROM_NAME=Reputation Guardian
```

3. **Update the email service**:

Create `/workspaces/ReputationAi/backend/services/email_service.py`:

```python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_onboarding_email(to_email, subject, html_content):
    message = Mail(
        from_email=os.getenv('EMAIL_FROM'),
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
```

### Option 2: Gmail SMTP (Free, easier for testing)

1. **Set up Gmail App Password**:
   - Go to your Google Account settings
   - Enable 2-factor authentication
   - Generate an App Password

2. **Add to `.env`**:
```env
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
EMAIL_FROM=your-email@gmail.com
EMAIL_FROM_NAME=Reputation Guardian
```

### Option 3: AWS SES (Production - Pay as you go)

```env
EMAIL_PROVIDER=aws_ses
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
EMAIL_FROM=noreply@reputationguardian.com
```

---

## 💳 Payment Gateway Setup

### Stripe (Recommended)

1. **Create Stripe Account**:
   - Go to https://stripe.com/
   - Sign up for free account
   - Get API keys from Dashboard

2. **Add to `.env`**:
```env
PAYMENT_PROVIDER=stripe
STRIPE_SECRET_KEY=sk_test_your_test_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_test_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

3. **Test Mode**:
   - Use test keys (start with `sk_test_` and `pk_test_`)
   - Test card: 4242 4242 4242 4242
   - Any future expiry date
   - Any CVC

---

## 🗄️ Database Configuration

The system uses PostgreSQL. For development, you can use:

### Option 1: Local PostgreSQL (if installed)

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/reputationai
```

### Option 2: Cloud PostgreSQL (Render, Supabase, etc.)

```env
DATABASE_URL=postgresql://user:password@host:5432/database
```

### Option 3: SQLite (Development Only)

```env
DATABASE_URL=sqlite:///./reputationai.db
```

---

## 📝 Complete .env Configuration

Here's a complete example `.env` file:

```env
# Environment
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/reputationai

# Email (Choose one provider)
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com
EMAIL_FROM_NAME=Reputation Guardian

# Payment Gateway
PAYMENT_PROVIDER=stripe
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_key

# Security
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application URLs
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8080
ONBOARDING_PORTAL_URL=https://onboarding.reputationguardian.com
PAYMENT_PORTAL_URL=https://secure.reputationguardian.com

# Admin
ADMIN_EMAIL=admin@reputation.ai
ADMIN_PASSWORD=Admin@2024!
```

---

## 🧪 Testing the Backend

### 1. Test Backend is Running

```bash
curl http://localhost:8080/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-12-27T..."
}
```

### 2. Test Application Submission

```bash
curl -X POST http://localhost:8080/api/onboarding/apply \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "phone": "+1-555-123-4567",
    "company": "Test Corp",
    "title": "CEO",
    "entities": "John Doe, Test Corp",
    "urgency": "proactive",
    "agreement": true,
    "privacy": true
  }'
```

### 3. Test Admin Offer Creation

```bash
python /workspaces/ReputationAi/backend/test_admin_onboarding.py
```

### 4. Access API Documentation

Open in browser:
- http://localhost:8080/api/docs

This gives you an interactive API explorer!

---

## 🔧 Common Issues & Solutions

### Issue: "Connection refused"
**Solution**: Backend is not running. Start it with:
```bash
cd /workspaces/ReputationAi/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Issue: "Database connection error"
**Solution**: 
1. Check DATABASE_URL in `.env`
2. Ensure PostgreSQL is running
3. Or use SQLite for testing: `DATABASE_URL=sqlite:///./test.db`

### Issue: "Module not found"
**Solution**: Install dependencies:
```bash
pip install -r /workspaces/ReputationAi/requirements.txt
```

### Issue: "Email not sending"
**Solution**: 
1. Check email credentials in `.env`
2. For Gmail, ensure you're using App Password, not regular password
3. Check spam folder

---

## 📱 Access Points

Once running, you can access:

### Backend API
- **Base URL**: http://localhost:8080
- **API Docs**: http://localhost:8080/api/docs
- **Admin Panel**: http://localhost:8080/admin (if implemented)

### Frontend
- **Development**: http://localhost:3000
- **Production**: Your deployed URL

### Endpoints

**Public**:
- `POST /api/onboarding/apply` - Submit application
- `GET /health` - Health check

**Admin** (requires authentication):
- `POST /api/admin/onboarding/create-offer` - Create subscription offer
- `GET /api/admin/onboarding/offers/{offer_id}` - Get offer details

---

## 🎯 Next Steps

1. **Start the backend** (see above)
2. **Configure email** (Gmail SMTP is easiest for testing)
3. **Test application submission** (use curl or the test script)
4. **Create an admin offer** (run test_admin_onboarding.py)
5. **Check email** (you should receive the onboarding email)

---

## 🆘 Need Help?

If you're still having issues:

1. **Check backend logs** - They show detailed error messages
2. **Verify .env file** - Make sure all required variables are set
3. **Test database connection** - Try SQLite first if PostgreSQL issues
4. **Use test mode** - Set `DEBUG=true` for more detailed logs

Let me know what specific error you're seeing and I can help troubleshoot!
