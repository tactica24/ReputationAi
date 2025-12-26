const functions = require('firebase-functions');
const admin = require('firebase-admin');
const express = require('express');
const cors = require('cors');

admin.initializeApp();
const db = admin.firestore();
const app = express();

app.use(cors({ origin: true }));
app.use(express.json());

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', service: 'ReputationAI API', timestamp: new Date().toISOString() });
});

// Applications endpoints
app.post('/api/v1/applications', async (req, res) => {
  try {
    const { company_name, email, industry, company_size, use_case } = req.body;
    
    const applicationData = {
      company_name,
      email,
      industry,
      company_size,
      use_case,
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
    res.status(500).json({ error: 'Failed to submit application' });
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
});

app.post('/api/v1/users', async (req, res) => {
  try {
    const { email, name, company, role } = req.body;
    
    const userData = {
      email,
      name,
      company,
      role: role || 'user',
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
    res.status(500).json({ error: 'Failed to create user' });
  }
});

// Entities endpoints
app.post('/api/v1/entities', async (req, res) => {
  try {
    const { user_id, name, entity_type, description } = req.body;
    
    const entityData = {
      user_id,
      name,
      entity_type,
      description,
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
    res.status(500).json({ error: 'Failed to create entity' });
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
    
    const mentionData = {
      entity_id,
      source,
      content,
      sentiment: sentiment || 'neutral',
      url,
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
    res.status(500).json({ error: 'Failed to create mention' });
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
    
    const alertData = {
      entity_id,
      alert_type,
      severity: severity || 'medium',
      message,
      mention_id,
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
    res.status(500).json({ error: 'Failed to create alert' });
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
