"""
CRUD operations for database models
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from backend.database.models import User, Entity, Mention, Alert, Application, AuditLog, UserRole


# ==================== USER CRUD ====================

def create_user(db: Session, email: str, username: str, hashed_password: str, full_name: str = None, role: UserRole = UserRole.VIEWER):
    """Create a new user"""
    user = User(
        email=email,
        username=username,
        hashed_password=hashed_password,
        full_name=full_name,
        role=role,
        is_active=True,
        gdpr_consent=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()


def update_user_status(db: Session, user_id: int, is_active: bool):
    """Update user active status"""
    user = get_user_by_id(db, user_id)
    if user:
        user.is_active = is_active
        db.commit()
        db.refresh(user)
    return user


# ==================== APPLICATION CRUD ====================

def create_application(db: Session, application_data: dict):
    """Create a new application"""
    from backend.database.models import Application, ApplicationStatus
    
    app = Application(
        application_id=application_data["application_id"],
        first_name=application_data["applicant"]["name"].split()[0],
        last_name=" ".join(application_data["applicant"]["name"].split()[1:]),
        email=application_data["applicant"]["email"],
        phone=application_data["applicant"]["phone"],
        company=application_data["applicant"].get("company"),
        title=application_data["applicant"]["title"],
        plan=application_data["protection_needs"]["plan"],
        entities_count=application_data["protection_needs"]["entities"],
        threats=application_data["protection_needs"].get("threats"),
        urgency=application_data["protection_needs"]["urgency"],
        how_heard=application_data.get("how_heard"),
        message=application_data.get("additional_message"),
        status=ApplicationStatus.PENDING
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def get_all_applications(db: Session, status: str = None, skip: int = 0, limit: int = 100):
    """Get all applications, optionally filtered by status"""
    query = db.query(Application)
    if status:
        query = query.filter(Application.status == status)
    return query.order_by(desc(Application.created_at)).offset(skip).limit(limit).all()


def get_pending_applications_count(db: Session) -> int:
    """Get count of pending applications"""
    from backend.database.models import ApplicationStatus
    return db.query(Application).filter(Application.status == ApplicationStatus.PENDING).count()


def update_application_status(db: Session, application_id: str, status: str, processed_by: int = None):
    """Update application status"""
    from backend.database.models import ApplicationStatus
    
    app = db.query(Application).filter(Application.application_id == application_id).first()
    if app:
        app.status = status
        app.processed_by = processed_by
        app.processed_at = datetime.utcnow()
        db.commit()
        db.refresh(app)
    return app


# ==================== ENTITY CRUD ====================

def create_entity(db: Session, owner_id: int, name: str, entity_type: str, keywords: List[str] = None):
    """Create a new monitored entity"""
    entity = Entity(
        name=name,
        entity_type=entity_type,
        owner_id=owner_id,
        keywords=keywords or [],
        monitoring_enabled=True,
        current_score=50.0
    )
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return entity


def get_entities_by_owner(db: Session, owner_id: int) -> List[Entity]:
    """Get all entities for a user"""
    return db.query(Entity).filter(Entity.owner_id == owner_id).all()


def get_entity_by_id(db: Session, entity_id: int) -> Optional[Entity]:
    """Get entity by ID"""
    return db.query(Entity).filter(Entity.id == entity_id).first()


def update_entity_score(db: Session, entity_id: int, new_score: float):
    """Update entity reputation score"""
    entity = get_entity_by_id(db, entity_id)
    if entity:
        entity.previous_score = entity.current_score
        entity.current_score = new_score
        
        # Determine trend
        if new_score > entity.previous_score + 5:
            entity.score_trend = "up"
        elif new_score < entity.previous_score - 5:
            entity.score_trend = "down"
        else:
            entity.score_trend = "stable"
        
        entity.last_scan_at = datetime.utcnow()
        db.commit()
        db.refresh(entity)
    return entity


# ==================== METRICS ====================

def get_system_metrics(db: Session) -> dict:
    """Get comprehensive system metrics"""
    from backend.database.models import ApplicationStatus
    
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    pending_apps = db.query(Application).filter(Application.status == ApplicationStatus.PENDING).count()
    total_entities = db.query(Entity).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "pending_applications": pending_apps,
        "total_entities": total_entities
    }


# ==================== AUDIT LOG ====================

def create_audit_log(db: Session, user_id: int, action: str, details: dict = None):
    """Create audit log entry"""
    log = AuditLog(
        user_id=user_id,
        action=action,
        details=details or {},
        ip_address="0.0.0.0"  # Should be captured from request
    )
    db.add(log)
    db.commit()
    return log
