"""
Production database initialization script for Render
Run this ONCE after deploying to Render to create the initial admin user
"""
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database.connection import engine, SessionLocal
from backend.database.models import Base, User
from backend.api.auth import hash_password


def init_production_database():
    """Initialize production database with tables and admin user"""
    
    print("🚀 Initializing production database...")
    
    # Create all tables
    print("📋 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.email == "admin@reputation.ai").first()
        
        if existing_admin:
            print("⚠️  Admin user already exists. Skipping creation.")
            return
        
        # Create super admin
        print("👤 Creating super admin user...")
        admin_user = User(
            email="admin@reputation.ai",
            password_hash=hash_password("Admin@2024!"),
            full_name="System Administrator",
            role="super_admin",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"   Email: admin@reputation.ai")
        print(f"   Password: Admin@2024!")
        print(f"   User ID: {admin_user.id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
    
    print("\n🎉 Production database initialized successfully!")
    print("🔐 Login at: https://reputation-ai-one.vercel.app/app")


if __name__ == "__main__":
    init_production_database()
