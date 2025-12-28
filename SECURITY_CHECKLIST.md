# Security Configuration for Production Deployment

## ⚠️ CRITICAL SECURITY ITEMS - DO BEFORE DEPLOYING

### 1. Environment Variables (.env file)
**Location**: `/workspaces/ReputationAi/.env`

**ACTION REQUIRED**: This file contains development secrets and MUST NOT be deployed.

```bash
# DELETE OR UPDATE these before going live:
SECRET_KEY=dev-secret-key-change-in-production-12345678  # ❌ CHANGE THIS
JWT_SECRET_KEY=dev-jwt-secret-12345678  # ❌ CHANGE THIS
ENCRYPTION_KEY=dev-encryption-key-must-be-32-bytes-long-12345  # ❌ CHANGE THIS
```

**Fix**:
```bash
# Generate secure random keys:
openssl rand -hex 32  # For SECRET_KEY
openssl rand -hex 32  # For JWT_SECRET_KEY
openssl rand -base64 32  # For ENCRYPTION_KEY
```

### 2. MongoDB Credentials Exposed
**Location**: Previous terminal commands and FIREBASE_DEPLOY.md

**EXPOSED**: `mongodb+srv://okwafa_db_user:MyPass123@cluster0.ewqncgb.mongodb.net/reputationai`

**ACTION REQUIRED**:
1. Go to https://cloud.mongodb.com
2. Navigate to Database Access
3. Change password for user `okwafa_db_user`
4. Update any applications using the old password
5. Delete FIREBASE_DEPLOY.md (contains exposed credentials)

### 3. Firebase Security Rules
**Status**: ✅ CONFIGURED
- Firestore rules: Require authentication for all operations
- Storage rules: Authenticated access only
- Admin-only operations properly restricted

### 4. CORS Configuration
**Status**: ✅ SECURED
**Location**: `functions/index.js`

Current allowed origins:
- https://reputationai-df869.web.app
- https://reputationai-df869.firebaseapp.com
- http://localhost:3000 (dev only - remove in production)
- http://localhost:5173 (dev only - remove in production)

**ACTION**: Remove localhost origins before deploying to production.

### 5. Input Validation
**Status**: ✅ IMPLEMENTED
- Email validation
- String sanitization (XSS prevention)
- Required field validation
- Enum validation for status, role, severity
- Payload size limits (10MB)

### 6. Rate Limiting
**Status**: ⚠️ RECOMMENDED
**Location**: Add to `functions/index.js`

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});

app.use('/api/', limiter);
```

**ACTION**: Install express-rate-limit:
```bash
cd functions && npm install express-rate-limit
```

### 7. Firebase Authentication
**Status**: ⚠️ NOT CONFIGURED
**Current**: API endpoints are publicly accessible (except those protected by Firestore rules)

**ACTION REQUIRED**:
1. Enable Firebase Authentication in Firebase Console
2. Add authentication middleware to Functions:

```javascript
// Middleware to verify Firebase ID tokens
const authenticate = async (req, res, next) => {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  const idToken = authHeader.split('Bearer ')[1];
  
  try {
    const decodedToken = await admin.auth().verifyIdToken(idToken);
    req.user = decodedToken;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// Protect endpoints
app.get('/api/v1/users', authenticate, async (req, res) => {
  // ...
});
```

3. Update frontend to use Firebase Auth

### 8. HTTPS/SSL
**Status**: ✅ AUTOMATIC
Firebase Hosting automatically provides SSL certificates for all deployed apps.

### 9. Data Encryption
**Status**: ✅ AUTOMATIC for Firestore
- Data encrypted in transit (HTTPS)
- Data encrypted at rest (Firestore automatic)

**⚠️ WARNING**: Sensitive data (passwords, tokens) should be hashed before storage.

### 10. Admin Access Control
**Status**: ⚠️ NEEDS IMPROVEMENT

**Current**: Firestore rules check admin role, but no middleware verification in Functions.

**ACTION REQUIRED**:
```javascript
// Middleware to check admin role
const requireAdmin = async (req, res, next) => {
  if (!req.user) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  
  try {
    const userDoc = await db.collection('users').doc(req.user.uid).get();
    
    if (!userDoc.exists || userDoc.data().role !== 'admin') {
      return res.status(403).json({ error: 'Forbidden: Admin access required' });
    }
    
    next();
  } catch (error) {
    return res.status(500).json({ error: 'Failed to verify admin status' });
  }
};

// Use on admin endpoints
app.get('/api/v1/applications', authenticate, requireAdmin, async (req, res) => {
  // Only admins can see all applications
});
```

## Security Checklist Before Deployment

- [ ] Change all default secrets in .env files
- [ ] Rotate MongoDB password (currently exposed)
- [ ] Remove localhost from CORS allowed origins
- [ ] Add rate limiting to Functions
- [ ] Enable Firebase Authentication
- [ ] Add authentication middleware to all protected endpoints
- [ ] Add admin role verification middleware
- [ ] Test all Firestore security rules
- [ ] Enable Firebase App Check (bot protection)
- [ ] Set up monitoring and alerts for suspicious activity
- [ ] Review and update storage rules for uploaded files
- [ ] Implement proper error handling (don't expose stack traces)
- [ ] Add logging for security events (failed auth, rate limits)
- [ ] Set up Cloud Armor (DDoS protection) - Optional but recommended

## Recommended Additional Security Measures

### 1. Firebase App Check
Protects against bots and abuse.

```bash
# Enable in Firebase Console → App Check
```

### 2. Security Headers
Add to Functions:

```javascript
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  next();
});
```

### 3. Content Security Policy
Add to hosting headers in firebase.json:

```json
{
  "key": "Content-Security-Policy",
  "value": "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
}
```

### 4. Audit Logging
Already configured in Firestore rules. Make sure critical operations create audit log entries.

### 5. Backup Strategy
- Enable Firestore daily backups in Firebase Console
- Set up scheduled exports to Cloud Storage
- Test restore procedures

## Monitoring & Alerts

1. **Firebase Console Alerts**:
   - Set up budget alerts
   - Monitor function execution errors
   - Track authentication failures

2. **Cloud Logging**:
   - Review function logs regularly
   - Set up log-based alerts for errors
   - Monitor for suspicious patterns

3. **Performance Monitoring**:
   - Enable Firebase Performance Monitoring
   - Track API response times
   - Monitor for degraded performance

## Compliance Considerations

For production use with sensitive data:
- [ ] GDPR compliance (if EU users)
- [ ] Data retention policies
- [ ] User data export/deletion endpoints
- [ ] Privacy policy and terms of service
- [ ] Cookie consent mechanism
- [ ] Regular security audits
- [ ] Penetration testing

## Emergency Procedures

### If a Breach is Detected:
1. Disable affected Firebase services immediately
2. Rotate all secrets and API keys
3. Force logout all users
4. Review audit logs
5. Patch vulnerability
6. Notify affected users (if required by law)

### Incident Response Contacts:
- Firebase Support: https://firebase.google.com/support
- Google Cloud Security: https://cloud.google.com/security

---

**Last Updated**: December 26, 2025
**Review Frequency**: Before each deployment
**Owner**: Development Team
