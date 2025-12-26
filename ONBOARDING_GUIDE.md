# User Onboarding & Instant Monitoring Guide

## How It Works

When a new user is onboarded, the system **instantly** starts monitoring and can detect/send alerts within minutes.

## Quick Onboarding API

### Endpoint: POST /api/v1/onboarding/quick-start

This endpoint creates a user account and immediately starts monitoring.

**Request:**
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "entities_to_monitor": [
    "John Doe",
    "Doe Enterprises", 
    "JohnDoeOfficial"
  ],
  "phone": "+1234567890"
}
```

**Response:**
```json
{
  "success": true,
  "user_id": 5,
  "message": "Welcome John Doe! Your account is active and monitoring has started.",
  "login_email": "user@example.com",
  "temporary_password": "Welcome1234!",
  "monitoring_status": "ACTIVE - Real-time monitoring started",
  "entities_monitored": [
    "John Doe",
    "Doe Enterprises",
    "JohnDoeOfficial"
  ]
}
```

## What Happens Automatically

### 1. Account Creation (Instant)
✅ User account created in database  
✅ Temporary password generated  
✅ Login credentials ready

### 2. Entity Setup (< 1 minute)
✅ All entities added to monitoring list  
✅ Keywords configured  
✅ Monitoring sources activated:
   - Twitter/X
   - Reddit
   - News sites
   - Review platforms
   - LinkedIn

### 3. Monitoring Starts (Immediate)
✅ Background scrapers initialized  
✅ Real-time data collection begins  
✅ Sentiment analysis pipeline active  
✅ Alert triggers configured

### 4. Alert Detection (5-30 minutes)
✅ First scan completes  
✅ Mentions detected and scored  
✅ Negative sentiment flagged  
✅ Alerts generated if thresholds met

## Alert Triggers

Alerts are sent **automatically** when:

| Trigger | Threshold | Alert Type |
|---------|-----------|-----------|
| Negative mention spike | +50% vs baseline | 🔴 Critical |
| Sentiment drop | Score < 30/100 | 🟠 High |
| Viral negative content | 10K+ views in 1 hour | 🔴 Crisis |
| Fake news detected | AI confidence > 80% | 🟠 High |
| Review bomb | 5+ negative reviews/hour | 🟠 High |
| Impersonation | Brand similarity > 90% | 🔴 Critical |

## Testing the System

### Option 1: Using cURL

```bash
# Onboard a new user
curl -X POST http://localhost:8080/api/v1/onboarding/quick-start \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "entities_to_monitor": ["Test User", "Test Company"],
    "phone": "+1234567890"
  }'

# Check monitoring status
curl http://localhost:8080/api/v1/onboarding/status/5
```

### Option 2: From the Dashboard

Once logged in as admin, you can onboard users through the UI (if implemented).

## Timeline

| Time | Action |
|------|--------|
| **T+0s** | User submits onboarding request |
| **T+1s** | Account created, credentials generated |
| **T+2s** | Entities added to database |
| **T+5s** | Background monitoring initiated |
| **T+1min** | First Twitter scan completes |
| **T+2min** | Reddit scan completes |
| **T+5min** | News aggregation completes |
| **T+10min** | Initial reputation score calculated |
| **T+15min** | First alert (if negative content found) |
| **T+30min** | Full baseline established |
| **T+1hr** | Continuous monitoring active |

## Alert Delivery Methods

### 1. Email Alerts (Free - via SendGrid)
- Sent to user's registered email
- Include severity, source, and recommended actions
- 100 free emails/day on free tier

### 2. SMS Alerts (Paid - $0.0075 per SMS)
- Critical alerts only by default
- Sent to registered phone number
- Via Twilio

### 3. Push Notifications (Free - via Firebase)
- Mobile app notifications
- Real-time delivery
- Unlimited on free tier

### 4. In-App Alerts (Free)
- Dashboard notifications
- Real-time updates via WebSocket
- No external service needed

## Adding More Entities Later

Users can add more entities to monitor anytime:

```bash
curl -X POST http://localhost:8080/api/v1/onboarding/add-entity/5 \
  -H "Content-Type: application/json" \
  -d 'entity_name=New Brand&entity_type=brand'
```

Monitoring for the new entity starts **immediately**.

## Production Deployment

To make this work in production:

### 1. Backend Deployment
Deploy to Render/Railway/Heroku:
```bash
# Set environment variables
export DATABASE_URL="postgresql://..."
export SENDGRID_API_KEY="..."
export TWILIO_ACCOUNT_SID="..."
export TWILIO_AUTH_TOKEN="..."

# Deploy
git push heroku main
```

### 2. Scheduled Jobs
Set up cron jobs for continuous monitoring:
```bash
# Every 5 minutes - scan social media
*/5 * * * * python -m backend.scripts.run_scrapers

# Every hour - analyze sentiment
0 * * * * python -m backend.scripts.analyze_sentiments

# Every day - generate reports
0 0 * * * python -m backend.scripts.daily_reports
```

### 3. Alert Processing
Background worker for real-time alerts:
```bash
# Using Celery
celery -A backend.tasks worker --loglevel=info
```

## Cost Breakdown (Per User/Month)

| Service | Free Tier | Paid Cost |
|---------|-----------|-----------|
| **Email (SendGrid)** | 100/day | $0 |
| **SMS (Twilio)** | None | $0.0075/SMS |
| **Push (Firebase)** | Unlimited | $0 |
| **Database (PostgreSQL)** | 500MB | $0-7/month |
| **Hosting (Render)** | 750hrs | $0-7/month |
| **Total per user** | | **~$0.50-2/month** |

## Next Steps

1. **Start Backend**: `python -m uvicorn backend.main:app --reload --port 8080`
2. **Test Onboarding**: Use the cURL command above
3. **Check Status**: Verify monitoring is active
4. **Wait 15-30 min**: First alerts should appear
5. **View Dashboard**: See entities and mentions

Your system is now ready to **instantly onboard users and start detecting threats**! 🚀
