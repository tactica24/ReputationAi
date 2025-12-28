const admin = require('firebase-admin');

// Initialize Firebase Admin
admin.initializeApp({
  projectId: 'reputationai-df869'
});

const db = admin.firestore();
const auth = admin.auth();

async function setAdminClaims(email) {
  try {
    // Get user by email
    const user = await auth.getUserByEmail(email);
    console.log(`✅ Found user: ${user.email} (UID: ${user.uid})`);
    
    // Set custom claims
    await auth.setCustomUserClaims(user.uid, {
      admin: true,
      role: 'admin'
    });
    console.log(`✅ Admin claims set successfully for ${email}`);
    
    // Update Firestore user document
    const userRef = db.collection('users').doc(user.uid);
    const userDoc = await userRef.get();
    
    if (userDoc.exists) {
      await userRef.update({
        role: 'admin',
        isAdmin: true
      });
      console.log('✅ Updated Firestore user document');
    } else {
      await userRef.set({
        email: email,
        role: 'admin',
        isAdmin: true,
        name: 'Admin User',
        createdAt: admin.firestore.FieldValue.serverTimestamp(),
        updatedAt: admin.firestore.FieldValue.serverTimestamp()
      });
      console.log('✅ Created Firestore user document');
    }
    
    console.log(`\n🎉 ${email} is now an admin!`);
    console.log('   The user needs to sign out and sign in again for changes to take effect.');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
  
  process.exit(0);
}

// Get email from command line
const email = process.argv[2];
if (!email) {
  console.log('Usage: node set-admin.js <email>');
  console.log('\nExample:');
  console.log('  node set-admin.js admin@reputationai.com');
  process.exit(1);
}

setAdminClaims(email);
