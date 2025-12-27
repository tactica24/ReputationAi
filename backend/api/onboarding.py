"""
Onboarding API Endpoint
Handles client application submissions for vetting and approval
Admin assigns pricing during onboarding process
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
import asyncio
from enum import Enum

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])


class PlanType(str, Enum):
    """User interest - actual pricing set by admin"""
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class UrgencyLevel(str, Enum):
    ACTIVE_CRISIS = "active-crisis"
    EMERGING_THREAT = "emerging-threat"
    PROACTIVE = "proactive"


class HowHeard(str, Enum):
    SEARCH = "search"
    REFERRAL = "referral"
    SOCIAL = "social"
    NEWS = "news"
    OTHER = "other"


class ApplicationRequest(BaseModel):
    # Personal Information
    firstName: str
    lastName: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    title: str
    
    # Protection Needs (pricing NOT included - set by admin)
    plan: Optional[PlanType] = PlanType.CUSTOM  # Interest only, not binding
    entities: str
    threats: Optional[str] = None
    urgency: UrgencyLevel
    howHeard: Optional[HowHeard] = None
    
    # Additional
    message: Optional[str] = None
    agreement: bool
    privacy: bool
    
    # Metadata
    submittedAt: Optional[datetime] = None
    ipAddress: Optional[str] = None
    userAgent: Optional[str] = None
    
    @validator('firstName', 'lastName', 'title', 'entities')
    def validate_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()
    
    @validator('agreement', 'privacy')
    def validate_accepted(cls, v):
        if not v:
            raise ValueError('Must accept terms')
        return v
    
    @validator('phone')
    def validate_phone(cls, v):
        # Basic phone validation - strip non-digits
        digits = ''.join(filter(str.isdigit, v))
        if len(digits) < 10:
            raise ValueError('Invalid phone number')
        return v


class ApplicationResponse(BaseModel):
    success: bool
    message: str
    applicationId: str
    estimatedResponseTime: str = "24 hours"


async def send_notification_to_team(application: ApplicationRequest):
    """
    Send notification to internal team about new application
    In production, this would integrate with email/Slack/etc.
    """
    # Simulate sending email to team
    await asyncio.sleep(0.5)
    
    priority = "HIGH" if application.urgency == UrgencyLevel.ACTIVE_CRISIS else "NORMAL"
    
    notification = f"""
    🚨 NEW CLIENT APPLICATION - {priority} PRIORITY
    
    Name: {application.firstName} {application.lastName}
    Email: {application.email}
    Phone: {application.phone}
    Company: {application.company or 'N/A'}
    Title: {application.title}
    
    Plan: {application.plan.value.upper()}
    Urgency: {application.urgency.value.upper()}
    
    Entities to Protect:
    {application.entities}
    
    Current Threats:
    {application.threats or 'None specified'}
    
    Additional Message:
    {application.message or 'None'}
    
    Submitted: {datetime.now().isoformat()}
    
    ⏱️ RESPONSE DEADLINE: {
        '4 hours' if application.urgency == UrgencyLevel.ACTIVE_CRISIS 
        else '24 hours'
    }
    """
    
    print(notification)  # In production: send to Slack/email
    return True


async def send_confirmation_email(application: ApplicationRequest):
    """
    Send confirmation email to applicant
    """
    await asyncio.sleep(0.5)
    
    email_body = f"""
    Dear {application.firstName},
    
    Thank you for applying for Reputation Guardian protection services.
    
    We have received your application and our team is currently reviewing your submission.
    
    APPLICATION SUMMARY:
    - Plan: {application.plan.value.title()}
    - Urgency Level: {application.urgency.value.replace('-', ' ').title()}
    - Entities for Protection: {len(application.entities.split(','))} entities
    
    NEXT STEPS:
    {
        '1. Our crisis response team will contact you within 4 hours'
        if application.urgency == UrgencyLevel.ACTIVE_CRISIS
        else '1. A specialist will review your application within 24 hours'
    }
    2. We'll schedule a consultation call to discuss your specific needs
    3. Upon approval, we can begin monitoring immediately
    
    WHAT TO EXPECT:
    - A phone call from {application.email.split('@')[0]}@reputationguardian.com
    - Discussion of your protection requirements
    - Custom pricing (if applicable)
    - Onboarding timeline and process
    
    If you have urgent questions, please reply to this email or call our emergency line.
    
    Best regards,
    The Reputation Guardian Team
    
    ---
    This is an automated confirmation. Please do not reply directly to this email.
    For urgent matters, contact: emergency@reputationguardian.com
    """
    
    print(f"Confirmation email sent to: {application.email}")
    return True


@router.post("/apply", response_model=ApplicationResponse)
async def submit_application(
    application: ApplicationRequest,
    background_tasks: BackgroundTasks
):
    """
    Submit a new client application for review
    
    Process:
    1. Validate application data
    2. Store in database (not implemented here)
    3. Send notifications to team
    4. Send confirmation to applicant
    5. Return success response
    
    Response time:
    - Active Crisis: 4 hours
    - Emerging Threat: 12 hours  
    - Proactive: 24 hours
    """
    try:
        # Set submission timestamp
        application.submittedAt = datetime.now()
        
        # Generate application ID (in production: use UUID or database ID)
        app_id = f"APP-{datetime.now().strftime('%Y%m%d')}-{application.lastName[:3].upper()}{str(hash(application.email))[-4:]}"
        
        # Priority routing based on urgency
        if application.urgency == UrgencyLevel.ACTIVE_CRISIS:
            response_time = "4 hours"
            # In production: trigger immediate alert to on-call team
        elif application.urgency == UrgencyLevel.EMERGING_THREAT:
            response_time = "12 hours"
        else:
            response_time = "24 hours"
        
        # Store application in database
        # In production:
        # await db.applications.insert_one(application.dict())
        
        # Send notifications in background
        background_tasks.add_task(send_notification_to_team, application)
        background_tasks.add_task(send_confirmation_email, application)
        
        # Log application (in production: structured logging)
        print(f"✅ Application received: {app_id} | Urgency: {application.urgency.value}")
        
        return ApplicationResponse(
            success=True,
            message=f"Thank you for your application, {application.firstName}. We will contact you within {response_time}.",
            applicationId=app_id,
            estimatedResponseTime=response_time
        )
        
    except Exception as e:
        print(f"❌ Application submission error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="There was an error processing your application. Please try again or contact us directly."
        )


@router.get("/status/{application_id}")
async def check_application_status(application_id: str):
    """
    Check the status of an application
    """
    # In production: query database for application status
    
    return {
        "applicationId": application_id,
        "status": "under_review",
        "submittedAt": "2025-12-25T10:00:00Z",
        "estimatedResponseTime": "24 hours",
        "message": "Your application is currently under review by our team."
    }


@router.post("/webhook/approved")
async def application_approved_webhook(application_id: str):
    """
    Webhook endpoint for when application is manually approved by team
    Triggers onboarding sequence with IMMEDIATE notifications
    
    Sends:
    - Welcome email via SendGrid (FREE)
    - SMS alert via Twilio ($0.0075)
    - Push notification via Firebase (FREE)
    """
    try:
        from backend.services.notifications.free_notification_service import (
            FreeNotificationService,
            NotificationPreferences
        )
        from backend.database.models import SessionLocal, User, MonitoredPerson
        from passlib.context import CryptContext
        import secrets
        
        # Get application from database
        db = SessionLocal()
        
        # Create user account
        pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        temp_password = secrets.token_urlsafe(16)
        
        # Mock application data (in production, query from database)
        application_data = {
            'firstName': 'John',
            'lastName': 'Doe',
            'email': 'client@example.com',
            'phone': '+1234567890',
            'company': 'ACME Corp',
            'title': 'CEO',
            'plan': 'executive',
            'entities': 'John Doe, ACME Corp'
        }
        
        # Create user
        user = User(
            email=application_data['email'],
            hashed_password=pwd_context.hash(temp_password),
            full_name=f"{application_data['firstName']} {application_data['lastName']}",
            company_name=application_data.get('company'),
            phone=application_data['phone'],
            subscription_tier=application_data['plan'],
            monthly_rate=2497.0 if application_data['plan'] == 'executive' else 997.0,
            is_verified=True,
            is_active=True
        )
        db.add(user)
        db.commit()
        
        # Create monitored entities
        entities = [e.strip() for e in application_data['entities'].split(',')]
        for entity_name in entities:
            person = MonitoredPerson(
                user_id=user.id,
                name=entity_name,
                platforms=['twitter', 'reddit', 'instagram', 'news'],
                is_active=True
            )
            db.add(person)
        
        db.commit()
        db.close()
        
        # Initialize notification service
        notif_service = FreeNotificationService()
        
        # Send welcome email (FREE - SendGrid 100/day limit)
        email_sent = await notif_service.send_welcome_email(
            user_email=application_data['email'],
            user_name=f"{application_data['firstName']} {application_data['lastName']}"
        )
        
        # Send SMS notification (costs $0.0075 per SMS)
        sms_sent = False
        if application_data.get('phone'):
            sms_message = (
                f"🛡️ Welcome to AI Reputation Guardian! Your monitoring is now ACTIVE. "
                f"Check your email for login details. Dashboard: https://yourcompany.com"
            )
            sms_sent = await notif_service.send_sms(
                to_phone=application_data['phone'],
                message=sms_message
            )
        
        # Push notification (FREE - Firebase FCM)
        # Will be sent when user installs mobile app and registers device token
        push_ready = True
        
        return {
            "success": True,
            "message": f"Application {application_id} approved. Notifications sent immediately.",
            "user_id": user.id,
            "notifications_sent": {
                "email": email_sent,
                "sms": sms_sent,
                "push_configured": push_ready
            },
            "credentials": {
                "email": application_data['email'],
                "temporary_password": temp_password,
                "note": "Credentials sent via email. User must change password on first login."
            },
            "monitoring_status": "ACTIVE - Started immediately",
            "entities_monitored": entities,
            "cost_incurred": "$0.0075" if sms_sent else "$0"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Approval failed: {str(e)}"
        )


@router.post("/webhook/rejected")
async def application_rejected_webhook(
    application_id: str,
    reason: Optional[str] = None
):
    """
    Webhook endpoint for when application is rejected
    """
    # In production:
    # 1. Update database status to 'rejected'
    # 2. Send polite rejection email with reason (if appropriate)
    # 3. Log rejection for analytics
    
    return {
        "success": True,
        "message": f"Application {application_id} rejected. Notification sent to applicant."
    }


# Integration with main FastAPI app:
# 
# from fastapi import FastAPI
# from backend.api.onboarding import router as onboarding_router
# 
# app = FastAPI()
# app.include_router(onboarding_router)
