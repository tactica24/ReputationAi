/**
 * Seed Firebase Firestore with sample data
 * Run: GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json node seed-database.js
 * Or run without credentials to use default project
 */

const admin = require('firebase-admin');

// Initialize Firebase Admin (will use default project from Firebase CLI)
admin.initializeApp({
  projectId: 'reputationai-df869'
});

const db = admin.firestore();

async function seedDatabase() {
  console.log('🌱 Seeding Firestore database...\n');

  try {
    // 1. Create Admin User
    console.log('Creating admin user...');
    const adminUser = await db.collection('users').add({
      email: 'admin@reputationai.com',
      name: 'Admin User',
      company: 'ReputationAI',
      role: 'admin',
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log('✅ Admin user created:', adminUser.id);

    // 2. Create Regular Users
    console.log('\nCreating regular users...');
    const user1 = await db.collection('users').add({
      email: 'john@techcorp.com',
      name: 'John Smith',
      company: 'Tech Corp',
      role: 'user',
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
    
    const user2 = await db.collection('users').add({
      email: 'sarah@innovation.io',
      name: 'Sarah Johnson',
      company: 'Innovation Inc',
      role: 'user',
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log('✅ Users created:', user1.id, user2.id);

    // 3. Create Applications
    console.log('\nCreating applications...');
    const apps = [
      {
        company_name: 'TechStart Inc',
        email: 'contact@techstart.com',
        industry: 'Technology',
        company_size: '50-100',
        use_case: 'Brand reputation monitoring for our SaaS product',
        status: 'pending',
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        company_name: 'Global Finance Ltd',
        email: 'info@globalfinance.com',
        industry: 'Finance',
        company_size: '100-500',
        use_case: 'Executive reputation monitoring and threat detection',
        status: 'approved',
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        company_name: 'HealthTech Solutions',
        email: 'hello@healthtech.io',
        industry: 'Healthcare',
        company_size: '10-50',
        use_case: 'Medical practice reputation management',
        status: 'rejected',
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      }
    ];

    for (const app of apps) {
      await db.collection('applications').add(app);
    }
    console.log('✅ Created', apps.length, 'applications');

    // 4. Create Entities
    console.log('\nCreating entities...');
    const entity1 = await db.collection('entities').add({
      user_id: user1.id,
      name: 'Tech Corp',
      entity_type: 'company',
      description: 'Leading technology company',
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });

    const entity2 = await db.collection('entities').add({
      user_id: user1.id,
      name: 'John Smith',
      entity_type: 'person',
      description: 'CEO of Tech Corp',
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });

    const entity3 = await db.collection('entities').add({
      user_id: user2.id,
      name: 'Innovation Inc',
      entity_type: 'company',
      description: 'Innovation consulting firm',
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log('✅ Created 3 entities');

    // 5. Create Mentions
    console.log('\nCreating mentions...');
    const mentions = [
      {
        entity_id: entity1.id,
        source: 'Twitter',
        content: 'Tech Corp just released an amazing new feature! Love the innovation.',
        sentiment: 'positive',
        url: 'https://twitter.com/example/status/123',
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        entity_id: entity1.id,
        source: 'Reddit',
        content: 'Has anyone tried Tech Corp products? Thinking of switching.',
        sentiment: 'neutral',
        url: 'https://reddit.com/r/tech/comments/abc',
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        entity_id: entity2.id,
        source: 'LinkedIn',
        content: 'Great insights from John Smith at the tech conference today.',
        sentiment: 'positive',
        url: 'https://linkedin.com/posts/example',
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        entity_id: entity1.id,
        source: 'Twitter',
        content: 'Tech Corp customer service is terrible. Been waiting 3 days for response.',
        sentiment: 'negative',
        url: 'https://twitter.com/example/status/456',
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        entity_id: entity3.id,
        source: 'Google Reviews',
        content: 'Innovation Inc helped transform our business. Highly recommended!',
        sentiment: 'positive',
        url: 'https://google.com/reviews/example',
        created_at: admin.firestore.FieldValue.serverTimestamp()
      }
    ];

    for (const mention of mentions) {
      await db.collection('mentions').add(mention);
    }
    console.log('✅ Created', mentions.length, 'mentions');

    // 6. Create Alerts
    console.log('\nCreating alerts...');
    const alerts = [
      {
        entity_id: entity1.id,
        alert_type: 'negative_sentiment',
        severity: 'high',
        message: 'Negative mention detected on Twitter regarding customer service',
        mention_id: null,
        is_read: false,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        entity_id: entity2.id,
        alert_type: 'mention_spike',
        severity: 'medium',
        message: 'Unusual increase in mentions detected (50% above baseline)',
        mention_id: null,
        is_read: false,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        entity_id: entity1.id,
        alert_type: 'brand_crisis',
        severity: 'critical',
        message: 'Multiple negative mentions detected in short timeframe',
        mention_id: null,
        is_read: true,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      }
    ];

    for (const alert of alerts) {
      await db.collection('alerts').add(alert);
    }
    console.log('✅ Created', alerts.length, 'alerts');

    // 7. Create Audit Logs
    console.log('\nCreating audit logs...');
    const logs = [
      {
        user_id: adminUser.id,
        action: 'user_login',
        resource: 'authentication',
        details: 'Admin user logged in successfully',
        timestamp: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        user_id: adminUser.id,
        action: 'application_approved',
        resource: 'applications',
        details: 'Approved application from Global Finance Ltd',
        timestamp: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        user_id: user1.id,
        action: 'entity_created',
        resource: 'entities',
        details: 'Created new entity: Tech Corp',
        timestamp: admin.firestore.FieldValue.serverTimestamp()
      }
    ];

    for (const log of logs) {
      await db.collection('auditLogs').add(log);
    }
    console.log('✅ Created', logs.length, 'audit logs');

    console.log('\n✅ Database seeding completed successfully!');
    console.log('\n📊 Summary:');
    console.log('   - 3 users (1 admin, 2 regular)');
    console.log('   - 3 applications (pending, approved, rejected)');
    console.log('   - 3 entities');
    console.log('   - 5 mentions');
    console.log('   - 3 alerts');
    console.log('   - 3 audit logs');
    console.log('\n🔐 Login with:');
    console.log('   Email: admin@reputationai.com');
    console.log('   Password: (set up Firebase Auth)');

    process.exit(0);
  } catch (error) {
    console.error('\n❌ Error seeding database:', error);
    process.exit(1);
  }
}

// Run the seeder
seedDatabase();
