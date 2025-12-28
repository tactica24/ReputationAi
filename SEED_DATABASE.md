# Database Seeding Instructions

## Option 1: Quick Seed (No Service Account Needed)

Since you're already authenticated with Firebase, use this simple method:

```bash
cd /workspaces/ReputationAi/functions
node seed-database-simple.js
```

## Option 2: Using Service Account

1. **Get Service Account Key** (if you need it later):
   - Go to: https://console.firebase.google.com/project/reputationai-df869/settings/serviceaccounts/adminsdk
   - Click "Generate new private key"
   - Save as `service-account-key.json` in `/functions` folder
   - **NEVER commit this file to git!**

2. **Run seeder**:
   ```bash
   cd /workspaces/ReputationAi/functions
   node seed-database.js
   ```

## What Gets Created

The seeder will create:
- ✅ 3 users (1 admin, 2 regular)
- ✅ 3 applications (pending, approved, rejected)
- ✅ 3 entities (2 companies, 1 person)
- ✅ 5 social media mentions (positive, neutral, negative)
- ✅ 3 alerts (high, medium, critical)
- ✅ 3 audit logs

## After Seeding

Your dashboard will show:
- Real application data in admin panel
- Entities to monitor
- Social mentions with sentiment analysis
- Active alerts
- Analytics charts with real data

## Login Credentials

After enabling Firebase Authentication:
- Email: admin@reputationai.com
- Password: (set via Firebase Console)

For now (mock auth):
- Email: admin@reputationai.com
- Password: admin123
