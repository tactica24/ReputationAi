/**
 * Seed Script for Firebase Firestore
 * Populates the database with sample data for testing
 * 
 * Run this script with: node seed-firebase.js
 */

const admin = require('firebase-admin');

// Initialize Firebase Admin SDK
// Make sure to set your service account key
const serviceAccount = {
  projectId: "reputationai-df869",
  // Add your service account credentials here or use environment variables
};

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  projectId: "reputationai-df869"
});

const db = admin.firestore();

// Sample data
const sampleUsers = [
  {
    email: 'admin@reputationai.com',
    name: 'Admin User',
    role: 'admin',
    company: 'ReputationAI',
    is_active: true
  },
  {
    email: 'john@techcorp.com',
    name: 'John Smith',
    role: 'user',
    company: 'TechCorp Inc',
    is_active: true
  },
  {
    email: 'sarah@startup.io',
    name: 'Sarah Johnson',
    role: 'user',
    company: 'StartupIO',
    is_active: true
  }
];

const sampleEntities = [
  {
    name: 'TechCorp Inc',
    entity_type: 'company',
    description: 'Leading technology company specializing in AI solutions',
    is_active: true,
    ownerId: null // Will be set after users are created
  },
  {
    name: 'John Smith',
    entity_type: 'person',
    description: 'CEO and Founder of TechCorp',
    is_active: true,
    ownerId: null
  },
  {
    name: 'AI Assistant Pro',
    entity_type: 'product',
    description: 'Advanced AI-powered virtual assistant',
    is_active: true,
    ownerId: null
  }
];

const sampleMentions = [
  {
    text: 'TechCorp\'s new AI Assistant Pro is revolutionary! Best product I\'ve used this year.',
    source: 'Twitter',
    url: 'https://twitter.com/user1/status/123',
    sentiment: 'positive',
    sentiment_score: 0.92,
    author: '@techfan2024',
    entityId: null // Will be set after entities are created
  },
  {
    text: 'Had a great experience with TechCorp support team. They resolved my issue quickly!',
    source: 'Reddit',
    url: 'https://reddit.com/r/tech/comments/xyz',
    sentiment: 'positive',
    sentiment_score: 0.85,
    author: 'u/happycustomer',
    entityId: null
  },
  {
    text: 'The customer service could be better, but the product quality is decent.',
    source: 'ProductHunt',
    url: 'https://producthunt.com/posts/ai-assistant-pro',
    sentiment: 'neutral',
    sentiment_score: 0.5,
    author: 'techreviewer99',
    entityId: null
  },
  {
    text: 'Not happy with the latest update. Some features are missing now.',
    source: 'Twitter',
    url: 'https://twitter.com/user2/status/456',
    sentiment: 'negative',
    sentiment_score: 0.25,
    author: '@disappointeduser',
    entityId: null
  },
  {
    text: 'John Smith gave an excellent keynote at TechSummit 2024. Very inspiring!',
    source: 'LinkedIn',
    url: 'https://linkedin.com/posts/user-123',
    sentiment: 'positive',
    sentiment_score: 0.88,
    author: 'Tech Enthusiast',
    entityId: null
  }
];

const sampleAlerts = [
  {
    alert_type: 'negative_mention',
    severity: 'high',
    message: 'Negative mention detected on Twitter',
    is_read: false,
    userId: null,
    mentionId: null
  },
  {
    alert_type: 'trending',
    severity: 'medium',
    message: 'Your brand is trending on social media',
    is_read: false,
    userId: null,
    mentionId: null
  },
  {
    alert_type: 'review_spike',
    severity: 'low',
    message: 'Increase in positive reviews detected',
    is_read: true,
    userId: null,
    mentionId: null
  }
];

const sampleApplications = [
  {
    company_name: 'Acme Corporation',
    email: 'contact@acme.com',
    industry: 'Technology',
    company_size: '50-200',
    use_case: 'Brand reputation monitoring',
    status: 'pending'
  },
  {
    company_name: 'Global Enterprises',
    email: 'info@globalent.com',
    industry: 'Finance',
    company_size: '200-1000',
    use_case: 'Executive reputation management',
    status: 'approved'
  },
  {
    company_name: 'Small Biz LLC',
    email: 'hello@smallbiz.com',
    industry: 'Retail',
    company_size: '1-50',
    use_case: 'Customer feedback analysis',
    status: 'rejected'
  }
];

async function seedDatabase() {
  console.log('🌱 Starting database seeding...\n');

  try {
    // Clear existing data (optional - comment out if you want to preserve existing data)
    console.log('🗑️  Clearing existing data...');
    const collections = ['users', 'entities', 'mentions', 'alerts', 'applications'];
    for (const collectionName of collections) {
      const snapshot = await db.collection(collectionName).get();
      const batch = db.batch();
      snapshot.docs.forEach((doc) => {
        batch.delete(doc.ref);
      });
      await batch.commit();
      console.log(`   Cleared ${collectionName}`);
    }
    console.log('✅ Existing data cleared\n');

    // Seed Users
    console.log('👤 Seeding users...');
    const userIds = [];
    for (const user of sampleUsers) {
      const docRef = await db.collection('users').add({
        ...user,
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      });
      userIds.push(docRef.id);
      console.log(`   Created user: ${user.email} (${docRef.id})`);
    }
    console.log('✅ Users seeded\n');

    // Seed Entities (link to first user)
    console.log('🏢 Seeding entities...');
    const entityIds = [];
    for (const entity of sampleEntities) {
      const docRef = await db.collection('entities').add({
        ...entity,
        ownerId: userIds[1], // Link to John Smith
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      });
      entityIds.push(docRef.id);
      console.log(`   Created entity: ${entity.name} (${docRef.id})`);
    }
    console.log('✅ Entities seeded\n');

    // Seed Mentions (link to entities)
    console.log('💬 Seeding mentions...');
    const mentionIds = [];
    for (let i = 0; i < sampleMentions.length; i++) {
      const mention = sampleMentions[i];
      const docRef = await db.collection('mentions').add({
        ...mention,
        entityId: entityIds[i % entityIds.length], // Distribute mentions across entities
        created_at: admin.firestore.FieldValue.serverTimestamp()
      });
      mentionIds.push(docRef.id);
      console.log(`   Created mention: ${mention.sentiment} (${docRef.id})`);
    }
    console.log('✅ Mentions seeded\n');

    // Seed Alerts (link to users and mentions)
    console.log('🔔 Seeding alerts...');
    for (let i = 0; i < sampleAlerts.length; i++) {
      const alert = sampleAlerts[i];
      const docRef = await db.collection('alerts').add({
        ...alert,
        userId: userIds[1], // Link to John Smith
        mentionId: mentionIds[i % mentionIds.length],
        created_at: admin.firestore.FieldValue.serverTimestamp()
      });
      console.log(`   Created alert: ${alert.alert_type} (${docRef.id})`);
    }
    console.log('✅ Alerts seeded\n');

    // Seed Applications
    console.log('📝 Seeding applications...');
    for (const app of sampleApplications) {
      const docRef = await db.collection('applications').add({
        ...app,
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      });
      console.log(`   Created application: ${app.company_name} (${docRef.id})`);
    }
    console.log('✅ Applications seeded\n');

    // Summary
    console.log('═══════════════════════════════════════');
    console.log('✅ Database seeding completed!');
    console.log('═══════════════════════════════════════');
    console.log(`📊 Summary:`);
    console.log(`   Users: ${userIds.length}`);
    console.log(`   Entities: ${entityIds.length}`);
    console.log(`   Mentions: ${mentionIds.length}`);
    console.log(`   Alerts: ${sampleAlerts.length}`);
    console.log(`   Applications: ${sampleApplications.length}`);
    console.log('═══════════════════════════════════════\n');

    console.log('🔑 Login Credentials:');
    console.log('   Admin: admin@reputationai.com / admin123');
    console.log('   User:  john@techcorp.com / user123');
    console.log('\n⚠️  Note: You\'ll need to create these users in Firebase Authentication manually');
    console.log('   or use the Firebase Admin SDK to create them programmatically.\n');

  } catch (error) {
    console.error('❌ Error seeding database:', error);
    process.exit(1);
  }

  process.exit(0);
}

// Run the seed function
seedDatabase();
