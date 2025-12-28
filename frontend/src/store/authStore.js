import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { onAuthStateChanged } from 'firebase/auth';
import { auth, db } from '../config/firebase';
import { doc, getDoc } from 'firebase/firestore';

export const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      loading: true,
      
      login: (user, token) => {
        set({ user, token, isAuthenticated: true, loading: false });
        localStorage.setItem('auth_token', token);
      },
      
      logout: () => {
        set({ user: null, token: null, isAuthenticated: false, loading: false });
        localStorage.removeItem('auth_token');
      },
      
      updateUser: (user) => {
        set({ user });
      },

      setLoading: (loading) => {
        set({ loading });
      },

      // Initialize auth state listener
      initAuth: () => {
        return onAuthStateChanged(auth, async (firebaseUser) => {
          if (firebaseUser) {
            try {
              // Get user data from Firestore
              const userDoc = await getDoc(doc(db, 'users', firebaseUser.uid));
              const token = await firebaseUser.getIdToken();
              
              if (userDoc.exists()) {
                const userData = userDoc.data();
                set({ 
                  user: {
                    id: firebaseUser.uid,
                    email: firebaseUser.email,
                    ...userData
                  },
                  token,
                  isAuthenticated: true,
                  loading: false
                });
                localStorage.setItem('auth_token', token);
              } else {
                // User exists in Auth but not in Firestore
                console.warn('User not found in Firestore');
                set({ user: null, token: null, isAuthenticated: false, loading: false });
              }
            } catch (error) {
              console.error('Error fetching user data:', error);
              set({ user: null, token: null, isAuthenticated: false, loading: false });
            }
          } else {
            set({ user: null, token: null, isAuthenticated: false, loading: false });
            localStorage.removeItem('auth_token');
          }
        });
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
