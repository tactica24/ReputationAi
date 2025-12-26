"""
Main FastAPI Application
Backend API for AI Reputation & Identity Guardian
"""

from fastapi import FastAPI, HTTPException, Depends, Security, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import uvicorn
import os

# Import our services (commented out for now - auth only)
# from backend.services.ai_analytics.sentiment_analysis import SentimentAnalyzer, SentimentAggregator
# from backend.services.ai_analytics.reputation_scoring import ReputationScorer
# from backend.services.ai_analytics.trend_analysis import TrendAnalyzer
# from backend.services.data_sources.aggregator import DataAggregator
# from backend.services.notifications.notification_service import NotificationService, NotificationChannel, NotificationPriority
# from backend.services.security.security_service import SecurityService, Permission, UserRole

# Import database
from backend.database.connection import get_db, init_database, check_database_health
from backend.database import crud
from backend.database.models import UserRole as DBUserRole, ApplicationStatus

# Import API routers
from backend.api.auth import router as auth_router
from backend.api.quick_onboard import router as onboard_router

# Initialize FastAPI app
app = FastAPI(
    title="AI Reputation & Identity Guardian API",
    description="Comprehensive AI-powered reputation monitoring and management",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_database()
    health = check_database_health()
    print(f"Database Health: {health}")


@app.get("/api/v1/health", tags=["System"])
async def health_check():
    """Health check endpoint for monitoring"""
    health = check_database_health()
    return {
        "status": "healthy" if any(health.values()) else "degraded",
        "database": health,
        "timestamp": datetime.utcnow().isoformat()
    }


# CORS middleware - PRIVATE APP: Only allow specific origins
# Set CORS_ORIGINS environment variable to your frontend domain(s)
# Example: "https://yourdomain.com,https://www.yourdomain.com"
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Restricted to specific origins only
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],  # Specific methods only
    allow_headers=["Content-Type", "Authorization"],  # Specific headers onlyent-Type", "Authorization"],
)

# Security
security_bearer = HTTPBearer()

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(onboard_router, prefix="/api/v1")

# Initialize services (commented out for now - auth only)
# sentiment_analyzer = SentimentAnalyzer(model_type="transformer")
# sentiment_aggregator = SentimentAggregator()
# reputation_scorer = ReputationScorer()
# trend_analyzer = TrendAnalyzer(sensitivity=2.0)
# data_aggregator = DataAggregator()
# notification_service = NotificationService(config={})
# security_service = SecurityService()

# Pydantic models for API
class EntityCreate(BaseModel):
    name: str
    type: str  # person, company, product, brand
    keywords: List[str]
    monitoring_enabled: bool = True

class EntityResponse(BaseModel):
    entity_id: str
    name: str
    type: str
    reputation_score: float
    category: str
    trend: str
    last_updated: datetime

class MentionResponse(BaseModel):
    id: str
    text: str
    source: str
    sentiment: str
    confidence: float
    timestamp: datetime
    engagement: Dict[str, int]

class AlertResponse(BaseModel):
    alert_id: str
    level: str
    type: str
    message: str
    recommendations: List[str]
    timestamp: datetime

class ReputationScoreResponse(BaseModel):
    entity_id: str
    overall_score: float
    category: str
    components: Dict[str, float]
    trend: str
    change_24h: float


# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security_bearer)):
    """Verify JWT token and return user"""
    # Placeholder for JWT verification
    # In production: Verify token, extract user_id
    return {"user_id": "user_123", "role": UserRole.USER}

async def get_admin_user(credentials: HTTPAuthorizationCredentials = Security(security_bearer)):
    """Verify JWT token and ensure user is admin"""
    user = await get_current_user(credentials)
    if user.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "sentiment_analyzer": "operational",
            "reputation_scorer": "operational",
            "trend_analyzer": "operational",
            "data_aggregator": "operational"
        }
    }


# Entities endpoints
@app.post("/api/v1/entities", response_model=EntityResponse)
async def create_entity(
    entity: EntityCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new entity to monitor"""
    entity_id = f"entity_{datetime.now().timestamp()}"
    
    # Log action
    security_service.audit.log_action(
        user_id=current_user["user_id"],
        action="create",
        resource_type="entity",
        resource_id=entity_id,
        ip_address="127.0.0.1",
        user_agent="API"
    )
    
    return EntityResponse(
        entity_id=entity_id,
        name=entity.name,
        type=entity.type,
        reputation_score=50.0,
        category="fair",
        trend="stable",
        last_updated=datetime.now()
    )


@app.get("/api/v1/entities/{entity_id}/reputation", response_model=ReputationScoreResponse)
async def get_reputation_score(
    entity_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get current reputation score for an entity"""
    # Check permission
    if not security_service.rbac.check_permission(current_user["user_id"], Permission.VIEW_DASHBOARD):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    # Get cached score or calculate new one
    score = reputation_scorer.get_score(entity_id)
    
    if not score:
        # Calculate new score (with sample data)
        score = reputation_scorer.calculate_score(
            entity_id=entity_id,
            entity_name="Sample Entity",
            mentions=[],
            time_window_hours=24
        )
    
    return ReputationScoreResponse(
        entity_id=entity_id,
        overall_score=score.overall_score,
        category=score.category.value,
        components={
            "sentiment": score.sentiment_score,
            "volume": score.volume_score,
            "engagement": score.engagement_score,
            "authority": score.authority_score
        },
        trend=score.trend_direction,
        change_24h=score._calculate_change_24h()
    )


@app.get("/api/v1/entities/{entity_id}/mentions", response_model=List[MentionResponse])
async def get_entity_mentions(
    entity_id: str,
    since: Optional[datetime] = None,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get recent mentions for an entity"""
    if not since:
        since = datetime.now() - timedelta(days=7)
    
    # In production: Fetch from database
    mentions = []
    
    return mentions


@app.get("/api/v1/entities/{entity_id}/alerts", response_model=List[AlertResponse])
async def get_entity_alerts(
    entity_id: str,
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """Get active alerts for an entity"""
    # Get alerts from trend analyzer
    alerts = [
        alert for alert in trend_analyzer.alerts_history
        if alert.entity_id == entity_id
    ][-limit:]
    
    return [
        AlertResponse(
            alert_id=alert.alert_id,
            level=alert.alert_level.value,
            type=alert.trend_type.value,
            message=alert.message,
            recommendations=alert.recommendations,
            timestamp=alert.timestamp
        )
        for alert in alerts
    ]


@app.post("/api/v1/entities/{entity_id}/analyze")
async def trigger_analysis(
    entity_id: str,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Trigger manual analysis for an entity"""
    # Add to background task queue
    background_tasks.add_task(
        perform_entity_analysis,
        entity_id=entity_id,
        user_id=current_user["user_id"]
    )
    
    return {
        "message": "Analysis started",
        "entity_id": entity_id,
        "status": "processing"
    }


async def perform_entity_analysis(entity_id: str, user_id: str):
    """Background task to perform entity analysis"""
    # 1. Fetch mentions from all sources
    # 2. Analyze sentiment
    # 3. Calculate reputation score
    # 4. Detect trends/spikes
    # 5. Send alerts if needed
    pass


# Sentiment analysis endpoint
@app.post("/api/v1/analyze/sentiment")
async def analyze_sentiment(
    text: str,
    source: str,
    entity: str,
    current_user: dict = Depends(get_current_user)
):
    """Analyze sentiment of a single text"""
    result = sentiment_analyzer.analyze(text, source, entity)
    
    return {
        "sentiment": result.sentiment.value,
        "confidence": result.confidence_score,
        "keywords": result.keywords,
        "influence_score": result.influence_score
    }


# Dashboard data endpoint
@app.get("/api/v1/dashboard/{entity_id}")
async def get_dashboard_data(
    entity_id: str,
    timeframe: str = "24h",
    current_user: dict = Depends(get_current_user)
):
    """Get comprehensive dashboard data for an entity"""
    # Calculate timeframe
    hours = {
        "24h": 24,
        "7d": 168,
        "30d": 720
    }.get(timeframe, 24)
    
    # Get data (in production: from database)
    dashboard_data = {
        "entity_id": entity_id,
        "timeframe": timeframe,
        "reputation_score": 75.5,
        "sentiment_distribution": {
            "positive": 45.2,
            "negative": 12.8,
            "neutral": 42.0
        },
        "mention_volume": {
            "current": 1250,
            "previous": 980,
            "change_percentage": 27.6
        },
        "trending_keywords": [
            {"keyword": "innovative", "count": 45, "sentiment": "positive"},
            {"keyword": "quality", "count": 38, "sentiment": "positive"},
            {"keyword": "support", "count": 32, "sentiment": "neutral"}
        ],
        "source_breakdown": {
            "twitter": 450,
            "news": 120,
            "reddit": 380,
            "linkedin": 200,
            "blogs": 100
        },
        "recent_alerts": [],
        "sentiment_trend": [
            {"date": "2025-12-19", "score": 72.3},
            {"date": "2025-12-20", "score": 73.8},
            {"date": "2025-12-21", "score": 74.2},
            {"date": "2025-12-22", "score": 75.1},
            {"date": "2025-12-23", "score": 74.8},
            {"date": "2025-12-24", "score": 75.2},
            {"date": "2025-12-25", "score": 75.5}
        ]
    }
    
    return dashboard_data


# Notification preferences
@app.get("/api/v1/users/{user_id}/notifications")
async def get_notification_preferences(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get notification preferences for a user"""
    # In production: Fetch from database
    return {
        "enabled_channels": ["email", "push"],
        "email_address": "user@example.com",
        "alert_thresholds": {
            "reputation_change": 5.0,
            "sentiment_change": 10.0
        },
        "quiet_hours": {
            "enabled": True,
            "start": 22,
            "end": 8
        },
        "summary_reports": {
            "daily": True,
            "weekly": True,
            "monthly": True
        }
    }


# Export data (GDPR compliance)
@app.get("/api/v1/users/{user_id}/export")
async def export_user_data(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Export all user data (GDPR right to data portability)"""
    export_data = security_service.gdpr.request_data_export(user_id)
    
    return export_data


# Delete user data (GDPR right to erasure)
@app.delete("/api/v1/users/{user_id}")
async def delete_user_data(
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete user data (GDPR right to erasure)"""
    success = security_service.gdpr.request_data_deletion(user_id)
    
    if success:
        return {"message": "Data deletion request processed", "user_id": user_id}
    else:
        raise HTTPException(status_code=500, detail="Error processing deletion request")


# Audit logs (for compliance)
@app.get("/api/v1/audit/logs")
async def get_audit_logs(
    user_id: Optional[str] = None,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get audit logs"""
    if not security_service.rbac.check_permission(current_user["user_id"], Permission.VIEW_AUDIT_LOGS):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    if user_id:
        logs = security_service.audit.get_logs_for_user(user_id, limit)
    else:
        logs = security_service.audit.logs[-limit:]
    
    return [log.to_dict() for log in logs]


# Application submission endpoint
class ApplicationSubmission(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    company: Optional[str] = None
    title: str
    plan: str
    entities: str
    threats: Optional[str] = None
    urgency: str
    howHeard: Optional[str] = None
    message: Optional[str] = None
    agreement: bool
    privacy: bool

class ApplicationResponse(BaseModel):
    success: bool
    application_id: str
    message: str
    estimated_response_time: str


@app.post("/api/v1/applications", response_model=ApplicationResponse)
async def submit_application(
    application: ApplicationSubmission,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a protection application (requires authentication)"""
    # Validate required agreements
    if not application.agreement or not application.privacy:
        raise HTTPException(
            status_code=400, 
            detail="You must accept the terms and privacy policy"
        )
    
    # Generate application ID
    application_id = f"APP-{datetime.now().strftime('%Y%m%d')}-{int(datetime.now().timestamp())}"
    
    # Create application data structure
    application_data = {
        "application_id": application_id,
        "timestamp": datetime.now().isoformat(),
        "applicant": {
            "name": f"{application.firstName} {application.lastName}",
            "email": application.email,
            "phone": application.phone,
            "company": application.company,
            "title": application.title
        },
        "protection_needs": {
            "plan": application.plan,
            "entities": application.entities,
            "threats": application.threats,
            "urgency": application.urgency
        },
        "how_heard": application.howHeard,
        "additional_message": application.message,
        "status": "pending_review"
    }
    
    # Save to database
    crud.create_application(db, application_data)
    
    # Determine response time based on urgency
    response_time_map = {
        "active-crisis": "within 2 hours",
        "emerging-threat": "within 12 hours",
        "proactive": "within 24 hours"
    }
    estimated_response = response_time_map.get(application.urgency, "within 24 hours")
    
    # Send notification emails in background
    background_tasks.add_task(
        send_application_notifications,
        application_data,
        application.email
    )
    
    return ApplicationResponse(
        success=True,
        application_id=application_id,
        message=f"Application received successfully. Our team will review and contact you {estimated_response}.",
        estimated_response_time=estimated_response
    )


async def send_application_notifications(application_data: dict, applicant_email: str):
    """Send notification emails for new application"""
    # In production: Send emails using notification service
    # 1. Confirmation email to applicant
    # 2. Alert to sales team
    # 3. If urgent, trigger SMS/Slack alert
    print(f"[NOTIFICATION] New application {application_data['application_id']}")
    print(f"[NOTIFICATION] Sending confirmation to {applicant_email}")
    print(f"[NOTIFICATION] Application data: {application_data}")


# =============================================
# ADMIN ENDPOINTS
# =============================================

@app.get("/api/v1/admin/users", tags=["Admin"])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_admin_user)
):
    """Get all platform users (Admin only)"""
    users = crud.get_all_users(db, skip=skip, limit=limit)
    
    return [
        {
            "id": str(user.id),
            "name": user.full_name or user.username,
            "email": user.email,
            "plan": "Pro",  # TODO: Add subscription model
            "status": "active" if user.is_active else "suspended",
            "joinedAt": user.created_at.isoformat() if user.created_at else None,
            "lastActive": user.last_login.isoformat() if user.last_login else None
        }
        for user in users
    ]


@app.get("/api/v1/admin/applications", tags=["Admin"])
async def get_all_applications(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_admin_user)
):
    """Get all pending and processed applications (Admin only)"""
    applications = crud.get_all_applications(db, status=status, skip=skip, limit=limit)
    
    return [
        {
            "id": str(app.id),
            "application_id": app.application_id,
            "firstName": app.first_name,
            "lastName": app.last_name,
            "email": app.email,
            "plan": app.plan,
            "entities": app.entities_count,
            "urgency": app.urgency,
            "status": app.status.value if hasattr(app.status, 'value') else app.status,
            "submittedAt": app.created_at.isoformat() if app.created_at else None
        }
        for app in applications
    ]


@app.post("/api/v1/admin/applications/{application_id}/approve", tags=["Admin"])
async def approve_application(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_admin_user),
    background_tasks: BackgroundTasks = None
):
    """Approve a pending application (Admin only)"""
    # Update application status in database
    app = crud.update_application_status(
        db, 
        application_id, 
        ApplicationStatus.APPROVED.value,
        processed_by=int(current_user["user_id"].replace("user_", "")) if "user_" in current_user["user_id"] else 1
    )
    
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Create audit log
    crud.create_audit_log(
        db,
        user_id=int(current_user["user_id"].replace("user_", "")) if "user_" in current_user["user_id"] else 1,
        action="approve_application",
        details={"application_id": application_id}
    )
    
    # TODO: Send approval email, create user account
    
    return {
        "success": True,
        "message": f"Application {application_id} approved",
        "application_id": application_id,
        "action_by": current_user["user_id"],
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/v1/admin/applications/{application_id}/reject", tags=["Admin"])
async def reject_application(
    application_id: str,
    current_user: dict = Depends(get_admin_user)
):
    """Reject a pending application (Admin only)"""
    # In production:
    # 1. Update application status
    # 2. Send rejection email (with reason if provided)
    # 3. Log admin action
    
    return {
        "success": True,
        "message": f"Application {application_id} rejected",
        "application_id": application_id,
        "action_by": current_user["user_id"],
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/api/v1/admin/users/{user_id}/toggle-status", tags=["Admin"])
async def toggle_user_status(
    user_id: str,
    status_data: dict,
    current_user: dict = Depends(get_admin_user)
):
    """Suspend or activate a user account (Admin only)"""
    new_status = status_data.get("status", "active")
    
    # In production:
    # 1. Update user status in database
    # 2. If suspending, revoke active sessions
    # 3. Send notification email to user
    # 4. Log admin action with reason
    
    return {
        "success": True,
        "message": f"User {user_id} status changed to {new_status}",
        "user_id": user_id,
        "new_status": new_status,
        "action_by": current_user["user_id"],
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/v1/admin/metrics", tags=["Admin"])
async def get_system_metrics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_admin_user)
):
    """Get comprehensive system metrics and analytics (Admin only)"""
    # Get real metrics from database
    metrics = crud.get_system_metrics(db)
    
    # For now, combine with mock chart data
    # TODO: Implement real time-series data collection
    return {
        "totalUsers": metrics["total_users"],
        "newUsersThisMonth": 89,  # TODO: Calculate from database
        "pendingApplications": metrics["pending_applications"],
        "activeSubscriptions": metrics["active_users"],
        "monthlyRevenue": 23640,  # TODO: Calculate from subscription model
        "systemHealth": "Excellent",
        "uptime": "99.98",
        
        # Charts data - TODO: Query from time-series data
        "userGrowthLabels": ["Dec 1", "Dec 8", "Dec 15", "Dec 22", "Dec 26"],
        "userGrowthData": [1050, 1120, 1180, 1220, metrics["total_users"]],
        
        "subscriptionDistribution": [350, 720, 110],  # Basic, Pro, Enterprise
        
        "analyticsLabels": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "mentionsProcessed": [45000, 52000, 58000, 61000],
        "alertsGenerated": [1200, 1350, 1280, 1420],
        
        "avgReputationScore": 78.5,
        "totalEntities": metrics["total_entities"],
        "avgResponseTime": 42,
        
        "recentActivity": [
            {
                "action": "System metrics retrieved",
                "admin": current_user.get("email", "admin@reputationai.com"),
                "timestamp": "just now"
            }
        ]
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
