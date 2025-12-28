# 🔥 How to Add Data to Firestore (Manual Setup)

Since automated scripts need special credentials, here's the easiest way to set up your dashboard with real data:

## ✅ Step 1: Create Users in Firebase Authentication

### Go to Firebase Authentication
https://console.firebase.google.com/project/reputationai-df869/authentication/users

1. Click **"Add User"** button
2. Create **Admin User**:
   - Email: `admin@reputationai.com`
   - Password: `Admin123!@#`
   - Click **"Add User"**

3. Create **Test User**:
   - Email: `user@reputationai.com`
   - Password: `User123!@#`
   - Click **"Add User"**

✅ **You now have 2 users!**

---

## ✅ Step 2: Create User Documents in Firestore

### Go to Firestore Console
https://console.firebase.google.com/project/reputationai-df869/firestore

### Create the "users" Collection

1. Click **"Start Collection"**
2. Collection ID: `users`
3. Click **"Next"**
4. Document ID: **Copy the UID from the admin user** (from Authentication step)
5. Add these fields:

| Field | Type | Value |
|-------|------|-------|
| `uid` | String | [Admin User's UID] |
| `email` | String | admin@reputationai.com |
| `name` | String | Admin User |
| `role` | String | admin |
| `company` | String | ReputationAI |
| `is_active` | Boolean | true |
| `created_at` | Timestamp | Today's date |
| `updated_at` | Timestamp | Today's date |

6. Click **"Save"**

### Add Test User Document

1. In the **"users"** collection, click **"Add Document"**
2. Document ID: **Copy the UID from the test user**
3. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `uid` | String | [Test User's UID] |
| `email` | String | user@reputationai.com |
| `name` | String | Test User |
| `role` | String | user |
| `company` | String | Test Company |
| `is_active` | Boolean | true |
| `created_at` | Timestamp | Today's date |
| `updated_at` | Timestamp | Today's date |

4. Click **"Save"**

✅ **You now have user documents!**

---

## ✅ Step 3: Create Entities Collection

### Create Collection
1. Click **"Start Collection"** (if not in a collection)
2. Collection ID: `entities`
3. Click **"Next"**

### Add Entity 1: TechCorp Inc
1. Document ID: **Auto ID** (click the auto ID icon)
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `name` | String | TechCorp Inc |
| `entity_type` | String | company |
| `description` | String | Leading technology company specializing in AI solutions |
| `is_active` | Boolean | true |
| `ownerId` | String | [Test User's UID] |
| `created_at` | Timestamp | Today's date |
| `updated_at` | Timestamp | Today's date |

3. Click **"Save"**

### Add Entity 2: John Smith
1. Click **"Add Document"** in entities collection
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `name` | String | John Smith |
| `entity_type` | String | person |
| `description` | String | CEO and Founder of TechCorp |
| `is_active` | Boolean | true |
| `ownerId` | String | [Test User's UID] |
| `created_at` | Timestamp | Today's date |
| `updated_at` | Timestamp | Today's date |

3. Click **"Save"**

### Add Entity 3: AI Assistant Pro
1. Click **"Add Document"** in entities collection
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `name` | String | AI Assistant Pro |
| `entity_type` | String | product |
| `description` | String | Advanced AI-powered virtual assistant |
| `is_active` | Boolean | true |
| `ownerId` | String | [Test User's UID] |
| `created_at` | Timestamp | Today's date |
| `updated_at` | Timestamp | Today's date |

3. Click **"Save"**

✅ **You now have 3 entities!**

---

## ✅ Step 4: Create Mentions Collection

### Create Collection
1. Click **"Start Collection"**
2. Collection ID: `mentions`
3. Click **"Next"**

### Add Mention 1 (Positive)
1. Document ID: **Auto ID**
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `text` | String | TechCorp's new AI Assistant Pro is revolutionary! Best product I've used this year. |
| `source` | String | Twitter |
| `url` | String | https://twitter.com/user1/status/123 |
| `sentiment` | String | positive |
| `sentiment_score` | Number | 0.92 |
| `author` | String | @techfan2024 |
| `entityId` | String | [ID of TechCorp Inc entity] |
| `created_at` | Timestamp | Today's date |

3. Click **"Save"**

### Add Mention 2 (Positive)
1. Click **"Add Document"** in mentions collection
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `text` | String | Had a great experience with TechCorp support team. They resolved my issue quickly! |
| `source` | String | Reddit |
| `url` | String | https://reddit.com/r/tech/comments/xyz |
| `sentiment` | String | positive |
| `sentiment_score` | Number | 0.85 |
| `author` | String | u/happycustomer |
| `entityId` | String | [ID of TechCorp Inc entity] |
| `created_at` | Timestamp | Today's date |

3. Click **"Save"**

### Add Mention 3 (Neutral)
1. Click **"Add Document"** in mentions collection
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `text` | String | The customer service could be better, but the product quality is decent. |
| `source` | String | ProductHunt |
| `url` | String | https://producthunt.com/posts/ai-assistant-pro |
| `sentiment` | String | neutral |
| `sentiment_score` | Number | 0.5 |
| `author` | String | techreviewer99 |
| `entityId` | String | [ID of AI Assistant Pro entity] |
| `created_at` | Timestamp | Today's date |

3. Click **"Save"**

### Add Mention 4 (Negative)
1. Click **"Add Document"** in mentions collection
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `text` | String | Not happy with the latest update. Some features are missing now. |
| `source` | String | Twitter |
| `url` | String | https://twitter.com/user2/status/456 |
| `sentiment` | String | negative |
| `sentiment_score` | Number | 0.25 |
| `author` | String | @disappointeduser |
| `entityId` | String | [ID of AI Assistant Pro entity] |
| `created_at` | Timestamp | Today's date |

3. Click **"Save"**

### Add Mention 5 (Positive)
1. Click **"Add Document"** in mentions collection
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `text` | String | John Smith gave an excellent keynote at TechSummit 2024. Very inspiring! |
| `source` | String | LinkedIn |
| `url` | String | https://linkedin.com/posts/user-123 |
| `sentiment` | String | positive |
| `sentiment_score` | Number | 0.88 |
| `author` | String | Tech Enthusiast |
| `entityId` | String | [ID of John Smith entity] |
| `created_at` | Timestamp | Today's date |

3. Click **"Save"**

✅ **You now have 5 mentions!**

---

## ✅ Step 5: Create Alerts Collection

### Create Collection
1. Click **"Start Collection"**
2. Collection ID: `alerts`
3. Click **"Next"**

### Add Alert 1 (High Severity)
1. Document ID: **Auto ID**
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `alert_type` | String | negative_mention |
| `severity` | String | high |
| `message` | String | Negative mention detected on Twitter |
| `is_read` | Boolean | false |
| `userId` | String | [Test User's UID] |
| `created_at` | Timestamp | Today's date |

3. Click **"Save"**

### Add Alert 2 (Medium Severity)
1. Click **"Add Document"** in alerts collection
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `alert_type` | String | trending |
| `severity` | String | medium |
| `message` | String | Your brand is trending on social media |
| `is_read` | Boolean | false |
| `userId` | String | [Test User's UID] |
| `created_at` | Timestamp | Today's date |

3. Click **"Save"**

### Add Alert 3 (Low Severity)
1. Click **"Add Document"** in alerts collection
2. Add fields:

| Field | Type | Value |
|-------|------|-------|
| `alert_type` | String | review_spike |
| `severity` | String | low |
| `message` | String | Increase in positive reviews detected |
| `is_read` | Boolean | true |
| `userId` | String | [Test User's UID] |
| `created_at` | Timestamp | Today's date |

3. Click **"Save"**

✅ **You now have 3 alerts!**

---

## ✅ Step 6: Test Your Dashboard

1. Go to: **https://reputationai-df869.web.app**
2. Login with:
   - Email: `admin@reputationai.com`
   - Password: `Admin123!@#`
3. You should see:
   - ✅ Dashboard with data
   - ✅ Entities list
   - ✅ Mentions
   - ✅ Alerts
   - ✅ Analytics

---

## 🎉 You're Done!

Your dashboard now has:
- ✅ 2 Users (Admin + Test)
- ✅ 3 Entities (Company, Person, Product)
- ✅ 5 Mentions (Various sentiments)
- ✅ 3 Alerts (Different severity levels)
- ✅ Real data showing on dashboard!

---

## 💡 Tip: Copy UIDs Easily

When you need to copy a UID:
1. Go to Authentication
2. Click on a user
3. Copy the "User UID" from the top right

---

**That's it! Your ReputationAI dashboard is now fully functional with real data! 🚀**
