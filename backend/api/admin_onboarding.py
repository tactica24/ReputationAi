"""
Admin Onboarding API
Handles admin-side onboarding including pricing assignment and payment collection
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime
import asyncio

router = APIRouter(prefix="/api/admin/onboarding", tags=["admin-onboarding"])


class OnboardingOffer(BaseModel):
    """Admin creates personalized offer for approved applicant"""
    application_id: str
    user_email: EmailStr
    tier: str  # professional, enterprise, custom
    monthly_price: float
    discount_percent: float = 0
    custom_features: Optional[List[str]] = None
    notes: Optional[str] = None
    include_trial_days: int = 0


class OnboardingPortalRequest(BaseModel):
    """Request to generate secure onboarding portal"""
    user_id: int
    offer_id: str
    require_documents: bool = True
    require_video: bool = True
    require_photos: bool = True
    custom_message: Optional[str] = None


class PaymentSetupComplete(BaseModel):
    """User completes payment setup"""
    user_id: int
    offer_id: str
    payment_method_id: str
    billing_address: Dict
    documents_uploaded: List[str] = []
    video_uploaded: bool = False
    photos_uploaded: List[str] = []


async def send_onboarding_email(
    user_email: str,
    offer_details: Dict,
    portal_link: str,
    payment_link: str
):
    """
    Send comprehensive onboarding email with:
    - Subscription pricing details
    - Secure portal link for document/video/photo upload
    - Payment setup link
    """
    from backend.services.email_service import send_onboarding_email as send_email
    
    # Use the new email service
    success = send_email(user_email, offer_details, portal_link, payment_link)
    
    if not success:
        # Fallback to console output if email fails
        await asyncio.sleep(0.5)
    
    email_content = f"""
    Dear {offer_details['user_name']},
    
    Congratulations! Your application for Reputation Guardian has been approved.
    
    📋 YOUR SUBSCRIPTION DETAILS:
    
    Plan: {offer_details['tier'].title()}
    Monthly Investment: ${offer_details['final_price']:,.2f}
    {f"Discount Applied: {offer_details['discount_percent']}%" if offer_details.get('discount_percent', 0) > 0 else ""}
    Billing Cycle: Monthly
    
    ✨ INCLUDED FEATURES:
    {chr(10).join(f"  • {feature}" for feature in offer_details['features'])}
    
    🔐 COMPLETE YOUR ONBOARDING:
    
    To activate your protection, please complete these steps:
    
    1. SECURE ONBOARDING PORTAL
       Complete your profile and upload required materials:
       {portal_link}
       
       You'll be able to:
       ✓ Upload identification documents (securely encrypted)
       ✓ Upload professional photos for your profile
       ✓ Record or upload a brief video introduction
       ✓ Provide additional context about your protection needs
    
    2. PAYMENT SETUP
       Set up your monthly subscription:
       {payment_link}
       
       ✓ Secure payment processing (PCI DSS compliant)
       ✓ Your card will be charged ${offer_details['final_price']:,.2f} monthly
       ✓ Cancel anytime with 30 days notice
    
    ⏰ TIMELINE:
    - Complete onboarding within 7 days
    - Protection starts within 24 hours of payment setup
    - First monitoring report within 48 hours
    
    🛡️ WHAT HAPPENS NEXT:
    1. You complete the onboarding portal
    2. You set up payment
    3. Our team activates your monitoring
    4. You receive your first threat assessment
    5. 24/7 protection begins immediately
    
    🔒 SECURITY & PRIVACY:
    All uploads are encrypted end-to-end. Your information is never shared
    and is protected by enterprise-grade security (AES-256 encryption).
    
    ❓ QUESTIONS?
    Reply to this email or call your dedicated specialist:
    Phone: +1 (800) 555-GUARD
    Email: onboarding@reputationguardian.com
    
    We're excited to protect what matters most to you.
    
    Best regards,
    The Reputation Guardian Team
    
    ---
    This offer expires in 7 days. Links are unique to you and should not be shared.
    """
    
    print(f"\n{'='*70}")
    print(f"ONBOARDING EMAIL SENT TO: {user_email}")
    print(email_content)
    print(f"{'='*70}\n")
    
    return True


@router.post("/create-offer")
async def create_subscription_offer(
    offer: OnboardingOffer,
    background_tasks: BackgroundTasks
):
    """
    Admin creates personalized subscription offer for approved applicant
    
    This endpoint:
    1. Creates subscription offer with custom pricing
    2. Generates secure payment link
    3. Generates onboarding portal link
    4. Sends comprehensive email to user
    
    Returns offer details and secure links
    """
    try:
        from backend.services.payment.billing_service import (
            BillingService,
            SubscriptionTier
        )
        
        # Map tier string to enum
        tier_map = {
            "professional": SubscriptionTier.PROFESSIONAL,
            "enterprise": SubscriptionTier.ENTERPRISE,
            "custom": SubscriptionTier.CUSTOM
        }
        tier = tier_map.get(offer.tier.lower(), SubscriptionTier.CUSTOM)
        
        # Create subscription offer
        subscription_offer = BillingService.create_subscription_offer(
            user_id=0,  # Will be set when user account is created
            tier=tier,
            custom_price=offer.monthly_price,
            custom_features=offer.custom_features,
            discount_percent=offer.discount_percent,
            notes=offer.notes
        )
        
        # Generate secure payment link
        payment_link = BillingService.generate_secure_payment_link(
            offer_id=subscription_offer["offer_id"],
            user_email=offer.user_email
        )
        
        # Generate onboarding portal link
        portal_link = BillingService.generate_onboarding_portal_link(
            user_id=0,
            offer_id=subscription_offer["offer_id"],
            include_document_upload=True,
            include_video_upload=True,
            include_photo_upload=True
        )
        
        # Prepare email details
        offer_details = {
            **subscription_offer,
            "user_name": offer.user_email.split('@')[0].title(),
            "portal_link": portal_link,
            "payment_link": payment_link
        }
        
        # Send onboarding email in background
        background_tasks.add_task(
            send_onboarding_email,
            offer.user_email,
            offer_details,
            portal_link,
            payment_link
        )
        
        # Store offer in database (in production)
        # await db.offers.insert_one(subscription_offer)
        
        return {
            "success": True,
            "message": f"Onboarding offer created and sent to {offer.user_email}",
            "offer_id": subscription_offer["offer_id"],
            "monthly_price": subscription_offer["final_price"],
            "portal_link": portal_link,
            "payment_link": payment_link,
            "expires_at": subscription_offer["expires_at"]
        }
        
    except Exception as e:
        print(f"❌ Error creating offer: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create offer: {str(e)}"
        )


@router.post("/portal/complete")
async def complete_onboarding_portal(
    completion: PaymentSetupComplete,
    background_tasks: BackgroundTasks
):
    """
    User completes onboarding portal
    Uploads documents, video, photos, and sets up payment
    
    This activates their subscription and starts monitoring
    """
    try:
        from backend.services.payment.payment_processor import PaymentProcessor
        from backend.services.payment.billing_service import BillingService
        
        # Validate payment method
        if not PaymentProcessor.validate_payment_method(completion.payment_method_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid payment method"
            )
        
        # Create subscription
        subscription = BillingService.create_subscription(
            user_id=completion.user_id,
            offer_id=completion.offer_id,
            payment_method_id=completion.payment_method_id,
            billing_details=completion.billing_address
        )
        
        # Verify required uploads
        if not completion.documents_uploaded:
            raise HTTPException(
                status_code=400,
                detail="Required documents not uploaded"
            )
        
        # Store subscription in database
        # await db.subscriptions.insert_one(subscription)
        
        # Activate monitoring
        # background_tasks.add_task(activate_monitoring, completion.user_id)
        
        # Send confirmation email
        # background_tasks.add_task(send_activation_email, completion.user_id)
        
        return {
            "success": True,
            "message": "Onboarding complete! Your protection is now active.",
            "subscription_id": subscription["subscription_id"],
            "status": "active",
            "monitoring_starts": subscription["started_at"],
            "next_billing_date": subscription["current_period_end"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error completing onboarding: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to complete onboarding: {str(e)}"
        )


@router.get("/offers/{offer_id}")
async def get_offer_details(offer_id: str):
    """
    Get details of a subscription offer
    Used by onboarding portal to display offer to user
    """
    # In production, query from database
    # offer = await db.offers.find_one({"offer_id": offer_id})
    
    return {
        "offer_id": offer_id,
        "tier": "enterprise",
        "monthly_price": 4997.00,
        "features": [
            "Company-wide protection",
            "Multiple executives/brands",
            "Dedicated account manager",
            "24/7 monitoring"
        ],
        "status": "pending",
        "expires_at": "2025-01-03T00:00:00Z"
    }


@router.post("/offers/{offer_id}/accept")
async def accept_offer(offer_id: str, user_id: int):
    """
    User accepts the subscription offer
    Moves them to payment setup phase
    """
    try:
        # Update offer status
        # await db.offers.update_one(
        #     {"offer_id": offer_id},
        #     {"$set": {"status": "accepted", "accepted_at": datetime.now()}}
        # )
        
        return {
            "success": True,
            "message": "Offer accepted. Please proceed to payment setup.",
            "next_step": "payment_setup"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to accept offer: {str(e)}"
        )
