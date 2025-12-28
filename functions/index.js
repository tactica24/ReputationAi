const functions = require('firebase-functions');
const admin = require('firebase-admin');
const express = require('express');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');

admin.initializeApp();
const db = admin.firestore();
const app = express();

// SECURITY: HTTP security headers
app.use(helmet());

// SECURITY: CORS configuration - restrict to your domain
const allowedOrigins = [
  'https://reputationai-df869.web.app',
  'https://reputationai-df869.firebaseapp.com',
  'http://localhost:3000', // Development only - REMOVE IN PRODUCTION
  'http://localhost:5173'  // Development only - REMOVE IN PRODUCTION
];

app.use(cors({
  origin: function(origin, callback) {
    // Allow requests with no origin (mobile apps, curl, etc.)
    if (!origin) return callback(null, true);
    if (allowedOrigins.indexOf(origin) === -1) {
      return callback(new Error('CORS policy violation'), false);
    }
    return callback(null, true);
  },
  credentials: true
}));

app.use(express.json({ limit: '10mb' })); // Limit payload size

// SECURITY: Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: { error: 'Too many requests from this IP, please try again later.' },
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', limiter);

// SECURITY: Input validation middleware
const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

const sanitizeString = (str) => {
  if (typeof str !== 'string') return '';
  return str.trim().replace(/[<>]/g, '');
};

const validateRequired = (fields, data) => {
  const missing = fields.filter(field => !data[field]);
  if (missing.length > 0) {
    throw new Error(`Missing required fields: ${missing.join(', ')}`);
  }
};

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', service: 'ReputationAI API', timestamp: new Date().toISOString() });
});

// Applications endpoints
app.post('/api/v1/applications', async (req, res) => {
  try {
    const { company_name, email, industry, company_size, use_case } = req.body;
    
    // SECURITY: Input validation
    validateRequired(['company_name', 'email', 'industry', 'company_size', 'use_case'], req.body);
    
    if (!validateEmail(email)) {
      return res.status(400).json({ error: 'Invalid email address' });
    }
    
    const applicationData = {
      company_name: sanitizeString(company_name),
      email: email.toLowerCase().trim(),
      industry: sanitizeString(industry),
      company_size: sanitizeString(company_size),
      use_case: sanitizeString(use_case),
      status: 'pending',
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    };
    
    const docRef = await db.collection('applications').add(applicationData);
    
    res.status(201).json({
      id: docRef.id,
      ...applicationData,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error creating application:', error);
    res.status(500).json({ error: error.message || 'Failed to submit application' });
  }
});

app.get('/api/v1/applications', async (req, res) => {
  try {
    const snapshot = await db.collection('applications')
      .orderBy('created_at', 'desc')
      .limit(100)
      .get();
    
    const applications = [];
    snapshot.forEach(doc => {
      applications.push({ id: doc.id, ...doc.data() });
    });
    
    res.json(applications);
  } catch (error) {
    console.error('Error fetching applications:', error);
    res.status(500).json({ error: 'Failed to fetch applications' });
  }
});

app.get('/api/v1/applications/:id', async (req, res) => {
  try {
    const doc = await db.collection('applications').doc(req.params.id).get();
    
    if (!doc.exists) {
      return res.status(404).json({ error: 'Application not found' });
    }
    
    res.json({ id: doc.id, ...doc.data() });
  } catch (error) {
    console.error('Error fetching application:', error);
    res.status(500).json({ error: 'Failed to fetch application' });
  }// SECURITY: Validate status value
    const validStatuses = ['pending', 'approved', 'rejected'];
    if (!validStatuses.includes(status)) {
      return res.status(400).json({ error: 'Invalid status value' });
    }
    
    
});

app.patch('/api/v1/applications/:id', async (req, res) => {
  try {
    const { status } = req.body;
    
    await db.collection('applications').doc(req.params.id).update({
      status,
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
    
    const doc = await db.collection('applications').doc(req.params.id).get();
    res.json({ id: doc.id, ...doc.data() });
  } catch (error) {
    console.error('Error updating application:', error);
    res.status(500).json({ error: 'Failed to update application' });
  }
});

// Users endpoints
app.get('/api/v1/users', async (req, res) => {
  try {
    const snapshot = await db.collection('users')
      .orderBy('created_at', 'desc')
      .limit(100)
      .get();
    
    const users = [];
    snapshot.forEach(doc => {
      const userData = doc.data();
      delete userData.password; // Don't send passwords
      users.push({ id: doc.id, ...userData });
    });
    
    res.json(users);
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({ error: 'Failed to fetch users' });
  }
});// SECURITY: Input validation
    validateRequired(['email', 'name'], req.body);
    
    if (!validateEmail(email)) {
      return res.status(400).json({ error: 'Invalid email address' });
    }
    
    // Validate role
    const validRoles = ['user', 'admin'];
    const userRole = role && validRoles.includes(role) ? role : 'user';
    
    const userData = {
      email: email.toLowerCase().trim(),
      name: sanitizeString(name),
      company: sanitizeString(company || ''),
      role: userRole,
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    };
    
    const docRef = await db.collection('users').add(userData);
    
    res.status(201).json({
      id: docRef.id,
      ...userData,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error creating user:', error);
    res.status(500).json({ error: error.message ||
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error creating user:', error);
    res.status(500).json({ error: 'Failed to create user' });
  }
});

// Entities endpoints
app.post('/api/v1/entities', async (req, res) => {
  try {
    const { user_id, name, entity_type, description } = req.body;
    
    // SECURITY: Input validation
    validateRequired(['user_id', 'name', 'entity_type'], req.body);
    
    const validEntityTypes = ['person', 'company', 'brand', 'product'];
    if (!validEntityTypes.includes(entity_type)) {
      return res.status(400).json({ error: 'Invalid entity type' });
    }
    
    const entityData = {
      user_id: sanitizeString(user_id),
      name: sanitizeString(name),
      entity_type: entity_type,
      description: sanitizeString(description || ''),
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    };
    
    const docRef = await db.collection('entities').add(entityData);
    
    res.status(201).json({
      id: docRef.id,
      ...entityData,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error creating entity:', error);
    res.status(500).json({ error: error.message || 'Failed to create entity' });
  }
});

app.get('/api/v1/entities', async (req, res) => {
  try {
    const snapshot = await db.collection('entities')
      .where('is_active', '==', true)
      .orderBy('created_at', 'desc')
      .limit(100)
      .get();
    
    const entities = [];
    snapshot.forEach(doc => {
      entities.push({ id: doc.id, ...doc.data() });
    });
    
    res.json(entities);
  } catch (error) {
    console.error('Error fetching entities:', error);
    res.status(500).json({ error: 'Failed to fetch entities' });
  }
});

// Mentions endpoints
app.get('/api/v1/mentions', async (req, res) => {
  try {
    const { entity_id } = req.query;
    
    let query = db.collection('mentions')
      .orderBy('created_at', 'desc')
      .limit(100);
    
    if (entity_id) {
      query = query.where('entity_id', '==', entity_id);
    }
    
    const snapshot = await query.get();
    
    const mentions = [];
    snapshot.forEach(doc => {
      mentions.push({ id: doc.id, ...doc.data() });
    });
    
    res.json(mentions);
  } catch (error) {
    console.error('Error fetching mentions:', error);
    res.status(500).json({ error: 'Failed to fetch mentions' });
  }
});

app.post('/api/v1/mentions', async (req, res) => {
  try {
    const { entity_id, source, content, sentiment, url } = req.body;
    
    // SECURITY: Input validation
    validateRequired(['entity_id', 'source', 'content'], req.body);
    
    const validSentiments = ['positive', 'neutral', 'negative'];
    const validatedSentiment = sentiment && validSentiments.includes(sentiment) ? sentiment : 'neutral';
    
    const mentionData = {
      entity_id: sanitizeString(entity_id),
      source: sanitizeString(source),
      content: sanitizeString(content),
      sentiment: validatedSentiment,
      url: url ? sanitizeString(url) : null,
      created_at: admin.firestore.FieldValue.serverTimestamp()
    };
    
    const docRef = await db.collection('mentions').add(mentionData);
    
    res.status(201).json({
      id: docRef.id,
      ...mentionData,
      created_at: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error creating mention:', error);
    res.status(500).json({ error: error.message || 'Failed to create mention' });
  }
});

// Alerts endpoints
app.get('/api/v1/alerts', async (req, res) => {
  try {
    const { entity_id } = req.query;
    
    let query = db.collection('alerts')
      .orderBy('created_at', 'desc')
      .limit(50);
    
    if (entity_id) {
      query = query.where('entity_id', '==', entity_id);
    }
    
    const snapshot = await query.get();
    
    const alerts = [];
    snapshot.forEach(doc => {
      alerts.push({ id: doc.id, ...doc.data() });
    });
    
    res.json(alerts);
  } catch (error) {
    console.error('Error fetching alerts:', error);
    res.status(500).json({ error: 'Failed to fetch alerts' });
  }
});

app.post('/api/v1/alerts', async (req, res) => {
  try {
    const { entity_id, alert_type, severity, message, mention_id } = req.body;
    
    // SECURITY: Input validation
    validateRequired(['entity_id', 'alert_type', 'message'], req.body);
    
    const validSeverities = ['low', 'medium', 'high', 'critical'];
    const validatedSeverity = severity && validSeverities.includes(severity) ? severity : 'medium';
    
    const alertData = {
      entity_id: sanitizeString(entity_id),
      alert_type: sanitizeString(alert_type),
      severity: validatedSeverity,
      message: sanitizeString(message),
      mention_id: mention_id ? sanitizeString(mention_id) : null,
      is_read: false,
      created_at: admin.firestore.FieldValue.serverTimestamp()
    };
    
    const docRef = await db.collection('alerts').add(alertData);
    
    res.status(201).json({
      id: docRef.id,
      ...alertData,
      created_at: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error creating alert:', error);
    res.status(500).json({ error: error.message || 'Failed to create alert' });
  }
});

// Analytics endpoints
app.get('/api/v1/analytics/dashboard', async (req, res) => {
  try {
    const [applicationsSnapshot, usersSnapshot, entitiesSnapshot, mentionsSnapshot] = await Promise.all([
      db.collection('applications').get(),
      db.collection('users').get(),
      db.collection('entities').get(),
      db.collection('mentions').get()
    ]);
    
    // Application stats
    const applications = [];
    applicationsSnapshot.forEach(doc => applications.push(doc.data()));
    
    const applicationStats = {
      total: applications.length,
      pending: applications.filter(a => a.status === 'pending').length,
      approved: applications.filter(a => a.status === 'approved').length,
      rejected: applications.filter(a => a.status === 'rejected').length
    };
    
    // User stats
    const users = [];
    usersSnapshot.forEach(doc => users.push(doc.data()));
    
    const userStats = {
      total: users.length,
      active: users.filter(u => u.is_active).length,
      admins: users.filter(u => u.role === 'admin').length
    };
    
    // Entity stats
    const entityStats = {
      total: entitiesSnapshot.size,
      active: 0
    };
    entitiesSnapshot.forEach(doc => {
      if (doc.data().is_active) entityStats.active++;
    });
    
    // Mention stats
    const mentions = [];
    mentionsSnapshot.forEach(doc => mentions.push(doc.data()));
    
    const mentionStats = {
      total: mentions.length,
      positive: mentions.filter(m => m.sentiment === 'positive').length,
      negative: mentions.filter(m => m.sentiment === 'negative').length,
      neutral: mentions.filter(m => m.sentiment === 'neutral').length
    };
    
    res.json({
      applications: applicationStats,
      users: userStats,
      entities: entityStats,
      mentions: mentionStats,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error fetching dashboard analytics:', error);
    res.status(500).json({ error: 'Failed to fetch analytics' });
  }
});

// Export the Express app as a Firebase Function
exports.api = functions.https.onRequest(app);
