// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCSFPZBzewPT-Tmj-XocBZKAYppGbnE72A",
  authDomain: "verisignal-ai.firebaseapp.com",
  projectId: "verisignal-ai",
  storageBucket: "verisignal-ai.appspot.com",
  messagingSenderId: "1055922829434",
  appId: "1:1055922829434:web:0df16c120978c4b5c363c3",
  measurementId: "G-5N3W3R9NWS"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);

export { app, analytics, auth, db, storage };
