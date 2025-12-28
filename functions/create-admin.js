/**
 * Create Admin User in Firebase
 * This script creates an admin user in Firebase Authentication and Firestore
 */

const admin = require('firebase-admin');

// Initialize Firebase Admin
admin.initializeApp({
  projectId: 'reputationai-df869'
});

const auth = admin.auth();
const db = admin.firestore();

async function createAdminUser() {
  const adminEmail = 'admin@reputationai.com';
  const adminPassword = 'Admin123!@#'; // Change this to a secure password
  const adminName = 'Admin User';

  console.log('👤 Creating admin user in Firebase Authentication...\n');

  try {
    // Create user in Firebase Authentication
    let userRecord;
    try {
      userRecord = await auth.createUser({
        email: adminEmail,
        password: adminPassword,
        displayName: adminName,
        emailVerified: true
      });
      console.log(`✅ Admin user created in Auth: ${userRecord.uid}`);
    } catch (error) {
      if (error.code === 'auth/email-already-exists') {
        console.log('⚠️  User already exists in Authentication, fetching...');
        userRecord = await auth.getUserByEmail(adminEmail);
        console.log(`✅ Found existing user: ${userRecord.uid}`);
      } else {
        throw error;
      }
    }

    // Create user document in Firestore
    const userDocRef = db.collection('users').doc(userRecord.uid);
    await userDocRef.set({
      uid: userRecord.uid,
      email: adminEmail,
      name: adminName,
      role: 'admin',
      company: 'ReputationAI',
      is_active: true,
      created_at: admin.firestore.FieldValue.serverTimestamp(),
      updated_at: admin.firestore.FieldValue.serverTimestamp()
    }, { merge: true });

    console.log('✅ Admin user document created in Firestore');
    console.log('\n═══════════════════════════════════════');
    console.log('✅ Admin user setup complete!');
    console.log('═══════════════════════════════════════');
    console.log('📧 Email:', adminEmail);
    console.log('🔑 Password:', adminPassword);
    console.log('👤 UID:', userRecord.uid);
    console.log('═══════════════════════════════════════\n');

    // Also create a regular user for testing
    console.log('👤 Creating test user...\n');
    const testEmail = 'user@reputationai.com';
    const testPassword = 'User123!@#';
    
    let testUserRecord;
    try {
      testUserRecord = await auth.createUser({
        email: testEmail,
        password: testPassword,
        displayName: 'Test User',
        emailVerified: true
      });
      console.log(`✅ Test user created in Auth: ${testUserRecord.uid}`);
    } catch (error) {
      if (error.code === 'auth/email-already-exists') {
        console.log('⚠️  Test user already exists');
        testUserRecord = await auth.getUserByEmail(testEmail);
      } else {
        console.error('Error creating test user:', error.message);
      }
    }

    if (testUserRecord) {
      await db.collection('users').doc(testUserRecord.uid).set({
        uid: testUserRecord.uid,
        email: testEmail,
        name: 'Test User',
        role: 'user',
        company: 'Test Company',
        is_active: true,
        created_at: admin.firestore.FieldValue.serverTimestamp(),
        updated_at: admin.firestore.FieldValue.serverTimestamp()
      }, { merge: true });
      
      console.log('✅ Test user document created in Firestore');
      console.log('\n📧 Test User Email:', testEmail);
      console.log('🔑 Test User Password:', testPassword);
      console.log('👤 Test User UID:', testUserRecord.uid);
    }

    console.log('\n🎉 All users created successfully!');
    console.log('\nYou can now login at: https://reputationai-df869.web.app\n');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ Error creating admin user:', error);
    process.exit(1);
  }
}

createAdminUser();
