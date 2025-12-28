#!/usr/bin/env python3
"""
Set admin custom claims for Firebase Authentication users
Usage: python3 set_admin_claims.py <email>
"""

import sys
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase Admin SDK
try:
    firebase_admin.initialize_app()
except ValueError:
    pass

def set_admin_claims(email):
    """Set admin custom claims for a user"""
    try:
        # Get user by email
        user = auth.get_user_by_email(email)
        print(f"✅ Found user: {user.email} (UID: {user.uid})")
        
        # Set custom claims
        auth.set_custom_user_claims(user.uid, {
            'admin': True,
            'role': 'admin'
        })
        print(f"✅ Admin claims set successfully for {email}")
        
        # Update Firestore user document
        db = firestore.client()
        user_ref = db.collection('users').document(user.uid)
        
        # Check if user document exists
        user_doc = user_ref.get()
        if user_doc.exists:
            user_ref.update({
                'role': 'admin',
                'isAdmin': True
            })
            print(f"✅ Updated Firestore user document")
        else:
            # Create user document
            user_ref.set({
                'email': email,
                'role': 'admin',
                'isAdmin': True,
                'name': 'Admin User',
                'createdAt': firestore.SERVER_TIMESTAMP,
                'updatedAt': firestore.SERVER_TIMESTAMP
            })
            print(f"✅ Created Firestore user document")
        
        print(f"\n🎉 {email} is now an admin!")
        print(f"   The user needs to sign out and sign in again for changes to take effect.")
        
    except auth.UserNotFoundError:
        print(f"❌ No user found with email: {email}")
        print(f"   Please create the user first via admin-setup.html")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 set_admin_claims.py <email>")
        print("\nExample:")
        print("  python3 set_admin_claims.py admin@reputationai.com")
        sys.exit(1)
    
    email = sys.argv[1]
    set_admin_claims(email)
