/**
 * Simple test admin creation for Firebase
 * Run this locally to create an admin user in Firestore
 */

const admin = require('firebase-admin');

// Initialize Firebase Admin
admin.initializeApp({
  projectId: 'reputationai-df869'
});

const db = admin.firestore();

async function createAdminUser() {
  try {
    const adminUser = {
      email: 'admin@reputationai.com',
      name: 'Admin User',
      company: 'ReputationAI',
      role: 'admin',
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    };

    const docRef = await db.collection('users').add(adminUser);
    
    console.log('✅ Admin user created successfully!');
    console.log('Document ID:', docRef.id);
    console.log('Email:', adminUser.email);
    console.log('Role:', adminUser.role);
    console.log('\nUse these credentials to login (you\'ll need Firebase Auth enabled)');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ Error creating admin user:', error);
    process.exit(1);
  }
}

createAdminUser();
