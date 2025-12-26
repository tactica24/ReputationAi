"""
Database connection management
Supports PostgreSQL (SQLAlchemy) and MongoDB
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from pymongo import MongoClient
from typing import Generator
import logging

logger = logging.getLogger(__name__)

# PostgreSQL Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./reputationai.db"  # SQLite for local development
    # "postgresql://postgres:postgres@localhost:5432/reputationai"  # PostgreSQL for production
)

# MongoDB URL from environment
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://localhost:27017/reputationai"
)

# SQLAlchemy engine for PostgreSQL
try:
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,  # For serverless/free tier compatibility
        echo=False,
        future=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("PostgreSQL connection initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize PostgreSQL: {e}")
    engine = None
    SessionLocal = None

# MongoDB client
try:
    mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    mongo_db = mongo_client.get_database()
    logger.info("MongoDB connection initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize MongoDB: {e}")
    mongo_client = None
    mongo_db = None


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for FastAPI to get database session
    Usage: db: Session = Depends(get_db)
    """
    if SessionLocal is None:
        raise Exception("Database not initialized")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_mongo():
    """
    Get MongoDB database instance
    """
    if mongo_db is None:
        logger.warning("MongoDB not available - using PostgreSQL fallback")
        return None
    return mongo_db


def init_database():
    """Initialize database tables"""
    from backend.database.models import Base
    
    if engine is None:
        logger.warning("Cannot initialize database - engine not available")
        return False
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        return False


def check_database_health() -> dict:
    """Check database connectivity"""
    health = {
        "postgresql": False,
        "mongodb": False
    }
    
    # Check PostgreSQL
    if engine:
        try:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            health["postgresql"] = True
        except Exception as e:
            logger.error(f"PostgreSQL health check failed: {e}")
    
    # Check MongoDB
    if mongo_client:
        try:
            mongo_client.admin.command('ping')
            health["mongodb"] = True
        except Exception as e:
            logger.error(f"MongoDB health check failed: {e}")
    
    return health
