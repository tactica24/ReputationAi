/**
 * Simple client-side initialization script
 * This creates admin users directly using Firebase SDK
 * Run this in browser console after opening the app
 */

import { initializeApp } from 'firebase/app';
import { getAuth, createUserWithEmailAndPassword } from 'firebase/auth';
import { getFirestore, doc, setDoc } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: "AIzaSyCSFPZBzewPT-Tmj-XocBZKAYppGbnE72A",
  authDomain: "reputationai-df869.firebaseapp.com",
  projectId: "reputationai-df869",
  storageBucket: "reputationai-df869.firebasestorage.app",
  messagingSenderId: "1055922829434",
  appId: "1:1055922829434:web:0df16c120978c4b5c363c3",
  measurementId: "G-5N3W3R9NWS"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

async function createAdmin() {
  try {
    // Create admin user in Firebase Auth
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      'admin@reputationai.com',
      'Admin123!@#'
    );

    // Create user document in Firestore
    await setDoc(doc(db, 'users', userCredential.user.uid), {
      uid: userCredential.user.uid,
      email: 'admin@reputationai.com',
      name: 'Admin User',
      role: 'admin',
      company: 'ReputationAI',
      is_active: true,
      created_at: new Date(),
      updated_at: new Date()
    });

    console.log('✅ Admin user created successfully!');
    console.log('Email: admin@reputationai.com');
    console.log('Password: Admin123!@#');
    console.log('UID:', userCredential.user.uid);

  } catch (error) {
    if (error.code === 'auth/email-already-in-use') {
      console.log('⚠️ Admin user already exists');
    } else {
      console.error('Error:', error);
    }
  }
}

async function createTestUser() {
  try {
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      'user@reputationai.com',
      'User123!@#'
    );

    await setDoc(doc(db, 'users', userCredential.user.uid), {
      uid: userCredential.user.uid,
      email: 'user@reputationai.com',
      name: 'Test User',
      role: 'user',
      company: 'Test Company',
      is_active: true,
      created_at: new Date(),
      updated_at: new Date()
    });

    console.log('✅ Test user created successfully!');
    console.log('Email: user@reputationai.com');
    console.log('Password: User123!@#');

  } catch (error) {
    if (error.code === 'auth/email-already-in-use') {
      console.log('⚠️ Test user already exists');
    } else {
      console.error('Error:', error);
    }
  }
}

// Run both
createAdmin();
createTestUser();
