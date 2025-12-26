"""
Quick User Onboarding & Instant Monitoring Setup
Automatically creates user account and starts monitoring when approved
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from datetime import datetime
import bcrypt
from typing import List

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])


class QuickOnboardRequest(BaseModel):
    email: EmailStr
    full_name: str
    entities_to_monitor: List[str]  # ["Your Name", "Your Company", "Your Brand"]
    phone: str = None


class OnboardResponse(BaseModel):
    success: bool
    user_id: int
    message: str
    login_email: str
    temporary_password: str
    monitoring_status: str
    entities_monitored: List[str]


async def start_monitoring(user_id: int, entities: List[str]):
    """
    Background task to immediately start monitoring entities
    Sets up:
    - Social media scrapers (Twitter, Reddit, LinkedIn)
    - News monitoring
    - Review site monitoring  
    - Alert triggers
    """
    print(f"🔍 MONITORING STARTED for User #{user_id}")
    print(f"📍 Tracking: {', '.join(entities)}")
    
    # In production, this would:
    # 1. Initialize scrapers for each entity
    # 2. Set up real-time monitoring
    # 3. Configure alert thresholds
    # 4. Start sentiment analysis
    
    return True


@router.post("/quick-start", response_model=OnboardResponse)
async def quick_onboard_user(
    request: QuickOnboardRequest,
    background_tasks: BackgroundTasks
):
    """
    Instantly onboard a new user and start monitoring
    
    Steps:
    1. Create user account with temp password
    2. Add entities to monitor
    3. Start monitoring immediately
    4. Send login credentials
    
    NO approval needed - instant activation!
    """
    from backend.database.connection import SessionLocal
    from backend.database.models import User, Entity, UserRole
    from backend.api.auth import hash_password
    import secrets
    
    db = SessionLocal()
    
    try:
        # Check if user exists
        existing = db.query(User).filter(User.email == request.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists. Please login.")
        
        # Generate temporary password
        temp_password = f"Welcome{secrets.randbelow(9999):04d}!"
        
        # Create user
        new_user = User(
            email=request.email,
            username=request.email.split('@')[0],
            full_name=request.full_name,
            hashed_password=hash_password(temp_password),
            role=UserRole.VIEWER,  # Can upgrade later
            is_active=True,
            is_verified=True,
            gdpr_consent=True,
            created_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.flush()  # Get user ID
        
        # Create monitored entities
        created_entities = []
        for entity_name in request.entities_to_monitor:
            entity = Entity(
                name=entity_name.strip(),
                entity_type='person',  # Can be person, brand, company
                owner_id=new_user.id,
                current_score=50.0,
                monitoring_enabled=True,
                keywords=[entity_name.strip()],
                monitored_sources=['twitter', 'reddit', 'news', 'reviews'],
                created_at=datetime.utcnow()
            )
            db.add(entity)
            created_entities.append(entity_name.strip())
        
        db.commit()
        
        # Start monitoring in background
        background_tasks.add_task(
            start_monitoring,
            new_user.id,
            created_entities
        )
        
        # Send welcome email (in production)
        # background_tasks.add_task(send_welcome_email, new_user.email, temp_password)
        
        return OnboardResponse(
            success=True,
            user_id=new_user.id,
            message=f"Welcome {request.full_name}! Your account is active and monitoring has started.",
            login_email=request.email,
            temporary_password=temp_password,
            monitoring_status="ACTIVE - Real-time monitoring started",
            entities_monitored=created_entities
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Onboarding failed: {str(e)}")
    finally:
        db.close()


@router.post("/add-entity/{user_id}")
async def add_entity_to_monitor(
    user_id: int,
    entity_name: str,
    entity_type: str = "person",
    background_tasks: BackgroundTasks = None
):
    """
    Add a new entity to monitor for existing user
    Starts monitoring immediately
    """
    from backend.database.connection import SessionLocal
    from backend.database.models import Entity
    
    db = SessionLocal()
    
    try:
        entity = Entity(
            name=entity_name,
            entity_type=entity_type,
            owner_id=user_id,
            current_score=50.0,
            monitoring_enabled=True,
            keywords=[entity_name],
            monitored_sources=['twitter', 'reddit', 'news', 'reviews'],
            created_at=datetime.utcnow()
        )
        
        db.add(entity)
        db.commit()
        
        # Start monitoring
        if background_tasks:
            background_tasks.add_task(start_monitoring, user_id, [entity_name])
        
        return {
            "success": True,
            "message": f"Now monitoring: {entity_name}",
            "entity_id": entity.id,
            "monitoring_status": "ACTIVE"
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get("/status/{user_id}")
async def get_monitoring_status(user_id: int):
    """
    Get current monitoring status for a user
    """
    from backend.database.connection import SessionLocal
    from backend.database.models import Entity, Mention
    from sqlalchemy import func
    
    db = SessionLocal()
    
    try:
        # Get user's entities
        entities = db.query(Entity).filter(Entity.owner_id == user_id).all()
        
        # Get mention counts
        entity_status = []
        for entity in entities:
            mention_count = db.query(func.count(Mention.id)).filter(
                Mention.entity_id == entity.id
            ).scalar() or 0
            
            entity_status.append({
                "name": entity.name,
                "type": entity.entity_type,
                "mentions_found": mention_count,
                "reputation_score": entity.current_score,
                "monitoring_active": entity.monitoring_enabled,
                "sources": entity.monitored_sources
            })
        
        return {
            "user_id": user_id,
            "entities_monitored": len(entities),
            "total_mentions": sum(e['mentions_found'] for e in entity_status),
            "monitoring_status": "ACTIVE",
            "entities": entity_status
        }
        
    finally:
        db.close()
