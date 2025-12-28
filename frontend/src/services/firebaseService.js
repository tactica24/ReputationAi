import { 
  collection, 
  doc, 
  getDoc, 
  getDocs, 
  addDoc, 
  updateDoc, 
  deleteDoc, 
  query, 
  where, 
  orderBy, 
  limit,
  serverTimestamp,
  Timestamp
} from 'firebase/firestore';
import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged
} from 'firebase/auth';
import { db, auth } from '../config/firebase';

// ============ Authentication Services ============

export const authService = {
  // Login with email and password
  login: async (email, password) => {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const userDoc = await getDoc(doc(db, 'users', userCredential.user.uid));
      
      if (!userDoc.exists()) {
        throw new Error('User profile not found');
      }
      
      const userData = userDoc.data();
      const token = await userCredential.user.getIdToken();
      
      return {
        user: {
          id: userCredential.user.uid,
          email: userCredential.user.email,
          ...userData
        },
        token
      };
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // Register new user
  register: async (email, password, userData) => {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      
      // Create user document in Firestore
      await addDoc(collection(db, 'users'), {
        uid: userCredential.user.uid,
        email,
        name: userData.name || '',
        company: userData.company || '',
        role: 'user', // Default role
        is_active: true,
        created_at: serverTimestamp(),
        updated_at: serverTimestamp()
      });
      
      return userCredential.user;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  // Logout
  logout: async () => {
    try {
      await signOut(auth);
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  },

  // Get current user
  getCurrentUser: () => {
    return auth.currentUser;
  },

  // Listen to auth state changes
  onAuthStateChange: (callback) => {
    return onAuthStateChanged(auth, callback);
  }
};

// ============ User Services ============

export const userService = {
  // Get all users
  getAll: async () => {
    try {
      const q = query(
        collection(db, 'users'),
        orderBy('created_at', 'desc'),
        limit(100)
      );
      const querySnapshot = await getDocs(q);
      
      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
    } catch (error) {
      console.error('Error fetching users:', error);
      throw error;
    }
  },

  // Get user by ID
  getById: async (userId) => {
    try {
      const docRef = doc(db, 'users', userId);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        return { id: docSnap.id, ...docSnap.data() };
      }
      return null;
    } catch (error) {
      console.error('Error fetching user:', error);
      throw error;
    }
  },

  // Update user
  update: async (userId, userData) => {
    try {
      const docRef = doc(db, 'users', userId);
      await updateDoc(docRef, {
        ...userData,
        updated_at: serverTimestamp()
      });
      
      return await userService.getById(userId);
    } catch (error) {
      console.error('Error updating user:', error);
      throw error;
    }
  },

  // Delete user
  delete: async (userId) => {
    try {
      await deleteDoc(doc(db, 'users', userId));
    } catch (error) {
      console.error('Error deleting user:', error);
      throw error;
    }
  }
};

// ============ Entity Services ============

export const entityService = {
  // Get all entities
  getAll: async (userId = null) => {
    try {
      let q;
      if (userId) {
        q = query(
          collection(db, 'entities'),
          where('ownerId', '==', userId),
          where('is_active', '==', true),
          orderBy('created_at', 'desc')
        );
      } else {
        q = query(
          collection(db, 'entities'),
          where('is_active', '==', true),
          orderBy('created_at', 'desc'),
          limit(100)
        );
      }
      
      const querySnapshot = await getDocs(q);
      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
    } catch (error) {
      console.error('Error fetching entities:', error);
      throw error;
    }
  },

  // Get entity by ID
  getById: async (entityId) => {
    try {
      const docRef = doc(db, 'entities', entityId);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        return { id: docSnap.id, ...docSnap.data() };
      }
      return null;
    } catch (error) {
      console.error('Error fetching entity:', error);
      throw error;
    }
  },

  // Create entity
  create: async (entityData) => {
    try {
      const docRef = await addDoc(collection(db, 'entities'), {
        ...entityData,
        is_active: true,
        created_at: serverTimestamp(),
        updated_at: serverTimestamp()
      });
      
      return await entityService.getById(docRef.id);
    } catch (error) {
      console.error('Error creating entity:', error);
      throw error;
    }
  },

  // Update entity
  update: async (entityId, entityData) => {
    try {
      const docRef = doc(db, 'entities', entityId);
      await updateDoc(docRef, {
        ...entityData,
        updated_at: serverTimestamp()
      });
      
      return await entityService.getById(entityId);
    } catch (error) {
      console.error('Error updating entity:', error);
      throw error;
    }
  },

  // Delete entity (soft delete)
  delete: async (entityId) => {
    try {
      const docRef = doc(db, 'entities', entityId);
      await updateDoc(docRef, {
        is_active: false,
        updated_at: serverTimestamp()
      });
    } catch (error) {
      console.error('Error deleting entity:', error);
      throw error;
    }
  }
};

// ============ Mention Services ============

export const mentionService = {
  // Get all mentions
  getAll: async (entityId = null) => {
    try {
      let q;
      if (entityId) {
        q = query(
          collection(db, 'mentions'),
          where('entityId', '==', entityId),
          orderBy('created_at', 'desc'),
          limit(100)
        );
      } else {
        q = query(
          collection(db, 'mentions'),
          orderBy('created_at', 'desc'),
          limit(100)
        );
      }
      
      const querySnapshot = await getDocs(q);
      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
    } catch (error) {
      console.error('Error fetching mentions:', error);
      throw error;
    }
  },

  // Get mention by ID
  getById: async (mentionId) => {
    try {
      const docRef = doc(db, 'mentions', mentionId);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        return { id: docSnap.id, ...docSnap.data() };
      }
      return null;
    } catch (error) {
      console.error('Error fetching mention:', error);
      throw error;
    }
  },

  // Create mention
  create: async (mentionData) => {
    try {
      const docRef = await addDoc(collection(db, 'mentions'), {
        ...mentionData,
        created_at: serverTimestamp()
      });
      
      return await mentionService.getById(docRef.id);
    } catch (error) {
      console.error('Error creating mention:', error);
      throw error;
    }
  },

  // Update mention
  update: async (mentionId, mentionData) => {
    try {
      const docRef = doc(db, 'mentions', mentionId);
      await updateDoc(docRef, {
        ...mentionData,
        updated_at: serverTimestamp()
      });
      
      return await mentionService.getById(mentionId);
    } catch (error) {
      console.error('Error updating mention:', error);
      throw error;
    }
  },

  // Delete mention
  delete: async (mentionId) => {
    try {
      await deleteDoc(doc(db, 'mentions', mentionId));
    } catch (error) {
      console.error('Error deleting mention:', error);
      throw error;
    }
  }
};

// ============ Alert Services ============

export const alertService = {
  // Get all alerts
  getAll: async (userId = null) => {
    try {
      let q;
      if (userId) {
        q = query(
          collection(db, 'alerts'),
          where('userId', '==', userId),
          orderBy('created_at', 'desc'),
          limit(100)
        );
      } else {
        q = query(
          collection(db, 'alerts'),
          orderBy('created_at', 'desc'),
          limit(100)
        );
      }
      
      const querySnapshot = await getDocs(q);
      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
    } catch (error) {
      console.error('Error fetching alerts:', error);
      throw error;
    }
  },

  // Mark alert as read
  markAsRead: async (alertId) => {
    try {
      const docRef = doc(db, 'alerts', alertId);
      await updateDoc(docRef, {
        is_read: true,
        updated_at: serverTimestamp()
      });
    } catch (error) {
      console.error('Error marking alert as read:', error);
      throw error;
    }
  },

  // Create alert
  create: async (alertData) => {
    try {
      const docRef = await addDoc(collection(db, 'alerts'), {
        ...alertData,
        is_read: false,
        created_at: serverTimestamp()
      });
      
      return { id: docRef.id, ...alertData };
    } catch (error) {
      console.error('Error creating alert:', error);
      throw error;
    }
  }
};

// ============ Application Services ============

export const applicationService = {
  // Get all applications
  getAll: async () => {
    try {
      const q = query(
        collection(db, 'applications'),
        orderBy('created_at', 'desc'),
        limit(100)
      );
      
      const querySnapshot = await getDocs(q);
      return querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
    } catch (error) {
      console.error('Error fetching applications:', error);
      throw error;
    }
  },

  // Get application by ID
  getById: async (appId) => {
    try {
      const docRef = doc(db, 'applications', appId);
      const docSnap = await getDoc(docRef);
      
      if (docSnap.exists()) {
        return { id: docSnap.id, ...docSnap.data() };
      }
      return null;
    } catch (error) {
      console.error('Error fetching application:', error);
      throw error;
    }
  },

  // Create application
  create: async (appData) => {
    try {
      const docRef = await addDoc(collection(db, 'applications'), {
        ...appData,
        status: 'pending',
        created_at: serverTimestamp(),
        updated_at: serverTimestamp()
      });
      
      return { id: docRef.id, ...appData };
    } catch (error) {
      console.error('Error creating application:', error);
      throw error;
    }
  },

  // Update application status
  updateStatus: async (appId, status) => {
    try {
      const docRef = doc(db, 'applications', appId);
      await updateDoc(docRef, {
        status,
        updated_at: serverTimestamp()
      });
      
      return await applicationService.getById(appId);
    } catch (error) {
      console.error('Error updating application:', error);
      throw error;
    }
  }
};

// ============ Analytics Services ============

export const analyticsService = {
  // Get dashboard analytics
  getDashboardStats: async () => {
    try {
      const [
        applicationsSnapshot,
        usersSnapshot,
        entitiesSnapshot,
        mentionsSnapshot,
        alertsSnapshot
      ] = await Promise.all([
        getDocs(collection(db, 'applications')),
        getDocs(collection(db, 'users')),
        getDocs(collection(db, 'entities')),
        getDocs(collection(db, 'mentions')),
        getDocs(collection(db, 'alerts'))
      ]);

      // Application stats
      const applications = applicationsSnapshot.docs.map(doc => doc.data());
      const applicationStats = {
        total: applications.length,
        pending: applications.filter(a => a.status === 'pending').length,
        approved: applications.filter(a => a.status === 'approved').length,
        rejected: applications.filter(a => a.status === 'rejected').length
      };

      // User stats
      const users = usersSnapshot.docs.map(doc => doc.data());
      const userStats = {
        total: users.length,
        active: users.filter(u => u.is_active).length,
        admins: users.filter(u => u.role === 'admin').length
      };

      // Entity stats
      const entities = entitiesSnapshot.docs.map(doc => doc.data());
      const entityStats = {
        total: entities.length,
        active: entities.filter(e => e.is_active).length
      };

      // Mention stats
      const mentions = mentionsSnapshot.docs.map(doc => doc.data());
      const mentionStats = {
        total: mentions.length,
        positive: mentions.filter(m => m.sentiment === 'positive').length,
        negative: mentions.filter(m => m.sentiment === 'negative').length,
        neutral: mentions.filter(m => m.sentiment === 'neutral').length
      };

      // Alert stats
      const alerts = alertsSnapshot.docs.map(doc => doc.data());
      const alertStats = {
        total: alerts.length,
        unread: alerts.filter(a => !a.is_read).length,
        critical: alerts.filter(a => a.severity === 'critical').length
      };

      return {
        applications: applicationStats,
        users: userStats,
        entities: entityStats,
        mentions: mentionStats,
        alerts: alertStats,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
      throw error;
    }
  }
};

export default {
  auth: authService,
  users: userService,
  entities: entityService,
  mentions: mentionService,
  alerts: alertService,
  applications: applicationService,
  analytics: analyticsService
};
