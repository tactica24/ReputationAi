# 📧 Free Notification Setup Guide

## Overview

Complete notification system using **FREE tiers**:
- ✅ **Email**: SendGrid (100 emails/day FREE)
- ✅ **SMS**: Twilio (trial credits, then $0.0075/SMS)
- ✅ **Push**: Firebase Cloud Messaging (FREE forever)

**Total monthly cost**: $0-$50/month

---

## 1. Email Notifications (FREE - SendGrid)

### Setup SendGrid (5 minutes)

**Step 1: Create Account**
1. Go to https://sendgrid.com/free/
2. Click "Start for free"
3. Fill in details (no credit card needed)
4. Verify email

**Step 2: Create API Key**
1. Login to SendGrid dashboard
2. Navigate to: **Settings → API Keys**
3. Click "Create API Key"
4. Name: `reputation-monitor-api`
5. Permissions: **Full Access** (or Mail Send only)
6. Click "Create & View"
7. **COPY the API key** (shown only once!)

**Step 3: Add to Environment**
```bash
# Add to .env file
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxx
FROM_EMAIL=alerts@yourcompany.com
```

**Step 4: Verify Sender**
1. In SendGrid: **Settings → Sender Authentication**
2. **Single Sender Verification** (free)
3. Add your email: `alerts@yourcompany.com`
4. Verify email sent to your inbox

**Limitations:**
- ✅ 100 emails/day FREE (3,000/month)
- ✅ Enough for 10-20 clients
- ✅ Upgrade to $20/month for 40,000 emails (200+ clients)

---

## 2. SMS Notifications (Twilio)

### Setup Twilio (10 minutes)

**Step 1: Create Account**
1. Go to https://www.twilio.com/try-twilio
2. Click "Sign up and start building"
3. Fill in details
4. Verify phone number
5. **Get $15 free trial credit**

**Step 2: Get Phone Number**
1. In Twilio console: **Phone Numbers → Manage → Buy a number**
2. Select your country
3. **Get a free trial number** (during trial)
4. After trial: $1/month for a number

**Step 3: Get Credentials**
1. In Twilio console dashboard
2. Copy:
   - **Account SID**: `ACxxxxxxxxxxxxxxx`
   - **Auth Token**: `xxxxxxxxxxxxx`
   - **Phone Number**: `+1234567890`

**Step 4: Add to Environment**
```bash
# Add to .env file
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxx
TWILIO_FROM_NUMBER=+1234567890
```

**Costs:**
- 💰 Trial: $15 FREE credit (~2,000 SMS)
- 💰 Production: $0.0075/SMS (~$7.50 per 1,000 SMS)
- 💰 Phone number: $1/month
- 💰 Example: 100 SMS/day = $22.50/month + $1 = $23.50/month

**Pro Tip**: Only enable SMS for CRITICAL alerts to save money!

---

## 3. Push Notifications (FREE - Firebase)

### Setup Firebase Cloud Messaging (15 minutes)

**Step 1: Create Firebase Project**
1. Go to https://console.firebase.google.com/
2. Click "Add project"
3. Name: `reputation-monitor`
4. Disable Google Analytics (optional)
5. Click "Create project"

**Step 2: Add App**
1. In Firebase console: Click "Add app"
2. Choose platform:
   - 📱 iOS: Select iOS icon
   - 🤖 Android: Select Android icon
   - 🌐 Web: Select Web icon
3. Register app with package name/bundle ID
4. Download config file:
   - iOS: `GoogleService-Info.plist`
   - Android: `google-services.json`
   - Web: Copy config object

**Step 3: Get Server Key**
1. In Firebase console: **Project Settings** (gear icon)
2. Click **Cloud Messaging** tab
3. Under "Cloud Messaging API (Legacy)":
   - If disabled, enable it
   - Copy **Server key**: `AAAAxxxxxxxxxxxxxxx`

**Step 4: Add to Environment**
```bash
# Add to .env file
FCM_SERVER_KEY=AAAAxxxxxxxxxxxxxxx
```

**Step 5: Test Push Notification**
```bash
# Test from command line
curl -X POST https://fcm.googleapis.com/fcm/send \
  -H "Authorization: key=YOUR_FCM_SERVER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "DEVICE_TOKEN_HERE",
    "notification": {
      "title": "Test",
      "body": "Push notification working!"
    }
  }'
```

**Costs:**
- ✅ **FREE forever** (no limits!)
- ✅ Unlimited notifications
- ✅ No credit card needed

---

## 4. Complete .env Configuration

### Your Final .env File:

```bash
# Database
DATABASE_URL=postgresql://repmonitor:password@localhost/reputation_monitor
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here

# SendGrid Email (FREE - 100/day)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxx
FROM_EMAIL=alerts@yourcompany.com

# Twilio SMS (Costs $0.0075/SMS)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxx
TWILIO_FROM_NUMBER=+1234567890

# Firebase Push (FREE forever)
FCM_SERVER_KEY=AAAAxxxxxxxxxxxxxxx

# Optional: Reddit, News APIs (all free)
REDDIT_CLIENT_ID=xxxxx
REDDIT_CLIENT_SECRET=xxxxx
NEWSAPI_KEY=xxxxx
```

---

## 5. Testing Notifications

### Test Email
```bash
cd /home/ubuntu/apps/ReputationAi
source venv/bin/activate

python3 -c "
import asyncio
import os
from backend.services.notifications.free_notification_service import FreeNotificationService

async def test():
    service = FreeNotificationService()
    result = await service.send_email(
        to_email='your@email.com',
        subject='Test Email',
        message='If you see this, SendGrid is working!',
        data={'severity': 'low'}
    )
    print(f'Email sent: {result}')

asyncio.run(test())
"
```

### Test SMS
```bash
python3 -c "
import asyncio
import os
from backend.services.notifications.free_notification_service import FreeNotificationService

async def test():
    service = FreeNotificationService()
    result = await service.send_sms(
        to_phone='+1234567890',  # Your phone number
        message='Test SMS from AI Reputation Guardian!'
    )
    print(f'SMS sent: {result} (Cost: \$0.0075)')

asyncio.run(test())
"
```

### Test Push
```bash
python3 -c "
import asyncio
import os
from backend.services.notifications.free_notification_service import FreeNotificationService

async def test():
    service = FreeNotificationService()
    result = await service.send_push(
        token='YOUR_DEVICE_TOKEN_HERE',
        title='Test Push',
        message='Push notification working!',
        data={'test': True}
    )
    print(f'Push sent: {result}')

asyncio.run(test())
"
```

---

## 6. Cost Breakdown

### Per Client (Monthly)

**Scenario 1: Email Only (Recommended for MVP)**
- Daily summary: 1 email/day = 30 emails/month
- Threat alerts: ~5 emails/month
- **Total: 35 emails/month = FREE** (within 100/day limit)

**Scenario 2: Email + Push**
- Email: 35/month = **FREE**
- Push: Unlimited = **FREE**
- **Total: $0/month per client**

**Scenario 3: Email + Push + SMS (Critical Only)**
- Email: 35/month = **FREE**
- Push: Unlimited = **FREE**
- SMS: 2 critical alerts/month = $0.015/month
- **Total: $0.015/month per client**

**Scenario 4: Full Service (Email + Push + SMS)**
- Email: 35/month = **FREE**
- Push: Unlimited = **FREE**
- SMS: 10 alerts/month = $0.075/month
- **Total: $0.075/month per client**

### Scale Examples

| Clients | Email/Day | Push/Day | SMS/Month | Monthly Cost |
|---------|-----------|----------|-----------|--------------|
| 10 | 30 (FREE) | Unlimited (FREE) | 100 | $0.75 |
| 50 | 150 (need paid plan) | Unlimited (FREE) | 500 | $20 + $3.75 = $23.75 |
| 100 | 300 (paid plan) | Unlimited (FREE) | 1000 | $20 + $7.50 = $27.50 |

**Pro Tip**: Use email + push for most alerts. Reserve SMS only for CRITICAL threats to minimize costs.

---

## 7. Notification Flow After Onboarding

### Immediate Actions When Application Approved:

**Step 1: Create User Account** (automated)
```
✅ User created in database
✅ Temporary password generated
✅ Monitored entities configured
✅ Monitoring started immediately
```

**Step 2: Send Welcome Email** (FREE)
```
📧 Subject: "Welcome to AI Reputation Guardian! 🛡️"
📧 Contains: Login credentials, dashboard link, next steps
📧 HTML template with branding
📧 Cost: $0
```

**Step 3: Send SMS Alert** (optional, $0.0075)
```
📱 Message: "Welcome! Your monitoring is ACTIVE. Check email for login."
📱 Immediate confirmation
📱 Cost: $0.0075
```

**Step 4: Push Notification Ready** (FREE)
```
📲 When user installs mobile app: Instant push configured
📲 Real-time threat alerts
📲 Cost: $0
```

**Step 5: Start Monitoring** (immediate)
```
🔍 AI scans begin within 15 minutes
🔍 First report sent within 24 hours
🔍 Real-time alerts enabled
```

---

## 8. Production Optimization

### Smart Notification Strategy

**Tier 1: Individual ($997/month)**
- Email: Daily summaries + high/critical alerts
- Push: High/critical threats only
- SMS: Disabled (save money)
- **Cost per client: $0/month**

**Tier 2: Executive ($2,497/month)**
- Email: Daily summaries + all alerts
- Push: All threats
- SMS: Critical only
- **Cost per client: $0.15/month**

**Tier 3: Enterprise ($4,997/month)**
- Email: Daily summaries + all alerts + weekly reports
- Push: All threats + instant updates
- SMS: Critical + high threats
- **Cost per client: $1.50/month**

### Maximize Free Tiers

**SendGrid Strategy:**
- Stay under 100 emails/day = FREE
- At 101 emails/day: Upgrade to $20/month (40,000 emails)
- Break-even: 34 clients sending 3 emails/day each

**Twilio Strategy:**
- Keep SMS disabled by default
- Only enable for:
  - Enterprise tier clients
  - Critical alerts only
  - Opt-in basis
- Most clients: $0/month
- Power users: $0.50-$2/month

**Firebase Strategy:**
- Always FREE
- No optimization needed
- Unlimited usage

---

## 9. Monitoring & Analytics

### Track Notification Costs

```python
# Add to your dashboard
from backend.services.notifications.free_notification_service import FreeNotificationService

service = FreeNotificationService()
stats = service.get_daily_stats()

print(f"""
Daily Notification Stats:
- Emails sent: {stats['emails_sent']}/100 (FREE limit)
- SMS sent: {stats['sms_sent']} (Cost: ${stats['total_cost']:.2f})
- Push sent: {stats['push_sent']} (FREE)
---
Total cost today: ${stats['total_cost']:.2f}
""")
```

### Alert When Approaching Limits

```python
# Add to cron job
if stats['emails_sent'] > 80:
    print("⚠️  WARNING: Approaching SendGrid daily limit (80/100)")
    # Consider upgrading to paid plan

if stats['total_cost'] > 5.00:
    print("⚠️  WARNING: Daily SMS costs exceed $5")
    # Review SMS strategy
```

---

## 10. Troubleshooting

### Email Not Sending
```bash
# Check SendGrid API key
curl -X GET https://api.sendgrid.com/v3/scopes \
  -H "Authorization: Bearer YOUR_API_KEY"

# Should return list of permissions
```

### SMS Not Sending
```bash
# Check Twilio credentials
curl -X GET "https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID.json" \
  -u "YOUR_ACCOUNT_SID:YOUR_AUTH_TOKEN"

# Should return account info
```

### Push Not Working
```bash
# Check FCM server key
curl -X POST https://fcm.googleapis.com/fcm/send \
  -H "Authorization: key=YOUR_FCM_KEY" \
  -H "Content-Type: application/json" \
  -d '{"to":"test","notification":{"title":"Test"}}'

# Should return error "InvalidRegistration" (key is valid)
```

---

## ✅ You're Ready!

After completing this setup:

✅ Clients receive **welcome email immediately** after approval  
✅ Clients get **SMS confirmation** (optional, $0.0075)  
✅ Clients can enable **push notifications** in mobile app (FREE)  
✅ **Total cost**: $0-$0.0075 per onboarding  
✅ **Ongoing cost**: $0-$1.50 per client per month  

**With 10 clients**: $0-$15/month notification costs  
**With 100 clients**: $0-$150/month notification costs  

**vs Enterprise solutions**: $500-$2,000/month for notification services alone!

---

**Next**: Test the complete onboarding flow! 🚀
