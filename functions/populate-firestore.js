/**
 * Populate Firestore with sample data
 * Use this in Firebase Functions or Cloud Shell
 */

const admin = require('firebase-admin');

// Initialize Firebase Admin SDK
admin.initializeApp({
  projectId: 'reputationai-df869'
});

const db = admin.firestore();

async function populateFirestore() {
  console.log('🚀 Populating Firestore with sample data...\n');

  try {
    // 1. Create Users
    console.log('👤 Creating users...');
    
    const adminUser = await db.collection('users').add({
      email: 'admin@reputationai.com',
      name: 'Admin User',
      role: 'admin',
      company: 'ReputationAI',
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log(`   ✅ Admin user created: ${adminUser.id}`);

    const testUser = await db.collection('users').add({
      email: 'user@reputationai.com',
      name: 'Test User',
      role: 'user',
      company: 'Test Company',
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log(`   ✅ Test user created: ${testUser.id}`);

    // 2. Create Entities
    console.log('\n🏢 Creating entities...');

    const entity1 = await db.collection('entities').add({
      name: 'TechCorp Inc',
      entity_type: 'company',
      description: 'Leading technology company specializing in AI solutions',
      is_active: true,
      ownerId: testUser.id,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log(`   ✅ Entity 1 created: ${entity1.id}`);

    const entity2 = await db.collection('entities').add({
      name: 'John Smith',
      entity_type: 'person',
      description: 'CEO and Founder of TechCorp',
      is_active: true,
      ownerId: testUser.id,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log(`   ✅ Entity 2 created: ${entity2.id}`);

    const entity3 = await db.collection('entities').add({
      name: 'AI Assistant Pro',
      entity_type: 'product',
      description: 'Advanced AI-powered virtual assistant',
      is_active: true,
      ownerId: testUser.id,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    });
    console.log(`   ✅ Entity 3 created: ${entity3.id}`);

    // 3. Create Mentions
    console.log('\n💬 Creating mentions...');

    const mentions = [
      {
        text: "TechCorp's new AI Assistant Pro is revolutionary! Best product I've used this year.",
        source: 'Twitter',
        url: 'https://twitter.com/user1/status/123',
        sentiment: 'positive',
        sentiment_score: 0.92,
        author: '@techfan2024',
        entityId: entity1.id,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        text: 'Had a great experience with TechCorp support team. They resolved my issue quickly!',
        source: 'Reddit',
        url: 'https://reddit.com/r/tech/comments/xyz',
        sentiment: 'positive',
        sentiment_score: 0.85,
        author: 'u/happycustomer',
        entityId: entity1.id,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        text: 'The customer service could be better, but the product quality is decent.',
        source: 'ProductHunt',
        url: 'https://producthunt.com/posts/ai-assistant-pro',
        sentiment: 'neutral',
        sentiment_score: 0.5,
        author: 'techreviewer99',
        entityId: entity3.id,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        text: 'Not happy with the latest update. Some features are missing now.',
        source: 'Twitter',
        url: 'https://twitter.com/user2/status/456',
        sentiment: 'negative',
        sentiment_score: 0.25,
        author: '@disappointeduser',
        entityId: entity3.id,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        text: 'John Smith gave an excellent keynote at TechSummit 2024. Very inspiring!',
        source: 'LinkedIn',
        url: 'https://linkedin.com/posts/user-123',
        sentiment: 'positive',
        sentiment_score: 0.88,
        author: 'Tech Enthusiast',
        entityId: entity2.id,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      }
    ];

    for (let i = 0; i < mentions.length; i++) {
      await db.collection('mentions').add(mentions[i]);
      console.log(`   ✅ Mention ${i + 1} created (${mentions[i].sentiment})`);
    }

    // 4. Create Alerts
    console.log('\n🔔 Creating alerts...');

    const alerts = [
      {
        alert_type: 'negative_mention',
        severity: 'high',
        message: 'Negative mention detected on Twitter',
        is_read: false,
        userId: testUser.id,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        alert_type: 'trending',
        severity: 'medium',
        message: 'Your brand is trending on social media',
        is_read: false,
        userId: testUser.id,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        alert_type: 'review_spike',
        severity: 'low',
        message: 'Increase in positive reviews detected',
        is_read: true,
        userId: testUser.id,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      }
    ];

    for (let i = 0; i < alerts.length; i++) {
      await db.collection('alerts').add(alerts[i]);
      console.log(`   ✅ Alert ${i + 1} created (${alerts[i].severity} severity)`);
    }

    // 5. Create Applications
    console.log('\n📝 Creating applications...');

    const applications = [
      {
        company_name: 'Acme Corporation',
        email: 'contact@acme.com',
        industry: 'Technology',
        company_size: '50-200',
        use_case: 'Brand reputation monitoring',
        status: 'pending',
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        company_name: 'Global Enterprises',
        email: 'info@globalent.com',
        industry: 'Finance',
        company_size: '200-1000',
        use_case: 'Executive reputation management',
        status: 'approved',
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      },
      {
        company_name: 'Small Biz LLC',
        email: 'hello@smallbiz.com',
        industry: 'Retail',
        company_size: '1-50',
        use_case: 'Customer feedback analysis',
        status: 'rejected',
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      }
    ];

    for (let i = 0; i < applications.length; i++) {
      await db.collection('applications').add(applications[i]);
      console.log(`   ✅ Application ${i + 1} created (${applications[i].status})`);
    }

    console.log('\n' + '='.repeat(50));
    console.log('✅ ALL SAMPLE DATA CREATED SUCCESSFULLY!');
    console.log('='.repeat(50));
    console.log('\n📊 Summary:');
    console.log('   • Users: 2');
    console.log('   • Entities: 3');
    console.log('   • Mentions: 5');
    console.log('   • Alerts: 3');
    console.log('   • Applications: 3');

    console.log('\n🔑 Login Credentials:');
    console.log('   Admin: admin@reputationai.com / Admin123!@#');
    console.log('   User:  user@reputationai.com / User123!@#');

    console.log('\n📝 Next Steps:');
    console.log('   1. Go to: https://console.firebase.google.com/project/reputationai-df869/authentication');
    console.log('   2. Create these 2 users in Firebase Authentication');
    console.log('   3. Set passwords: Admin123!@ and User123!@#');
    console.log('   4. Visit: https://reputationai-df869.web.app');
    console.log('   5. Login with admin credentials');
    console.log('   6. Dashboard will show all the sample data!');
    console.log('\n');

  } catch (error) {
    console.error('❌ Error:', error);
    process.exit(1);
  }

  process.exit(0);
}

populateFirestore();
