"""
Database initialization script
Creates database tables and default admin user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.database.connection import engine, SessionLocal
from backend.database.models import Base, User, UserRole
from backend.api.auth import hash_password
from datetime import datetime

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")

def create_admin_user():
    """Create default admin user"""
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == "admin@reputation.ai").first()
        
        if existing_admin:
            print("⚠ Admin user already exists")
            return existing_admin
        
        # Create admin user
        admin = User(
            email="admin@reputation.ai",
            username="admin",
            full_name="System Administrator",
            hashed_password=hash_password("Admin@2024!"),
            role=UserRole.SUPER_ADMIN,
            is_active=True,
            is_verified=True,
            gdpr_consent=True,
            created_at=datetime.utcnow()
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print("✓ Admin user created successfully")
        print(f"  Email: admin@reputation.ai")
        print(f"  Password: Admin@2024!")
        print(f"  Role: {admin.role.value}")
        print(f"  User ID: {admin.id}")
        
        return admin
        
    except Exception as e:
        print(f"✗ Error creating admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_demo_users():
    """Create additional demo users for testing"""
    db = SessionLocal()
    
    try:
        demo_users = [
            {
                "email": "manager@reputation.ai",
                "username": "manager",
                "full_name": "Demo Manager",
                "password": "Manager@2024!",
                "role": UserRole.MANAGER
            },
            {
                "email": "analyst@reputation.ai",
                "username": "analyst",
                "full_name": "Demo Analyst",
                "password": "Analyst@2024!",
                "role": UserRole.ANALYST
            },
            {
                "email": "user@reputation.ai",
                "username": "viewer",
                "full_name": "Demo Viewer",
                "password": "User@2024!",
                "role": UserRole.VIEWER
            }
        ]
        
        for user_data in demo_users:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(
                    email=user_data["email"],
                    username=user_data["username"],
                    full_name=user_data["full_name"],
                    hashed_password=hash_password(user_data["password"]),
                    role=user_data["role"],
                    is_active=True,
                    is_verified=True,
                    gdpr_consent=True,
                    created_at=datetime.utcnow()
                )
                db.add(user)
                print(f"✓ Created {user_data['role'].value}: {user_data['email']}")
        
        db.commit()
        print("✓ Demo users created successfully")
        
    except Exception as e:
        print(f"✗ Error creating demo users: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main initialization function"""
    print("=" * 60)
    print("AI Reputation Guardian - Database Initialization")
    print("=" * 60)
    print()
    
    try:
        # Initialize database
        init_database()
        print()
        
        # Create admin user
        create_admin_user()
        print()
        
        # Create demo users
        print("Creating additional demo users...")
        create_demo_users()
        print()
        
        print("=" * 60)
        print("✓ Database initialization completed successfully!")
        print("=" * 60)
        print()
        print("Login Credentials:")
        print("-" * 60)
        print("SUPER ADMIN:")
        print("  Email:    admin@reputation.ai")
        print("  Password: Admin@2024!")
        print()
        print("MANAGER:")
        print("  Email:    manager@reputation.ai")
        print("  Password: Manager@2024!")
        print()
        print("ANALYST:")
        print("  Email:    analyst@reputation.ai")
        print("  Password: Analyst@2024!")
        print()
        print("VIEWER:")
        print("  Email:    user@reputation.ai")
        print("  Password: User@2024!")
        print("-" * 60)
        
    except Exception as e:
        print(f"\n✗ Initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
