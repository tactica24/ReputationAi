"""
Billing Service - Admin level subscription management
Only accessible by admin users
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List
from enum import Enum


class SubscriptionTier(str, Enum):
    """Subscription tiers - prices set by admin"""
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class BillingService:
    """
    Manages billing and subscription information
    Admin-only functionality
    """
    
    # Default pricing (can be overridden by admin)
    DEFAULT_PRICING = {
        SubscriptionTier.PROFESSIONAL: {
            "base_price": 997.00,
            "currency": "USD",
            "billing_cycle": "monthly",
            "features": [
                "Personal brand protection",
                "Unlimited monitoring",
                "Instant threat alerts",
                "Crisis detection",
                "Monthly reports",
                "24/7 surveillance"
            ]
        },
        SubscriptionTier.ENTERPRISE: {
            "base_price": 4997.00,
            "currency": "USD",
            "billing_cycle": "monthly",
            "features": [
                "Company-wide protection",
                "Multiple executives/brands",
                "Dedicated account manager",
                "Custom alert protocols",
                "Legal report generation",
                "PR team integration",
                "Competitor tracking",
                "White-glove service"
            ]
        },
        SubscriptionTier.CUSTOM: {
            "base_price": None,  # Set by admin during onboarding
            "currency": "USD",
            "billing_cycle": "custom",
            "features": ["Fully customized solution"]
        }
    }
    
    @staticmethod
    def get_subscription_pricing(tier: SubscriptionTier, custom_price: Optional[float] = None) -> Dict:
        """
        Get pricing for a subscription tier
        Admin can set custom pricing during onboarding
        """
        pricing = BillingService.DEFAULT_PRICING.get(tier)
        
        if tier == SubscriptionTier.CUSTOM and custom_price:
            pricing["base_price"] = custom_price
            
        return pricing
    
    @staticmethod
    def create_subscription_offer(
        user_id: int,
        tier: SubscriptionTier,
        custom_price: Optional[float] = None,
        custom_features: Optional[List[str]] = None,
        discount_percent: float = 0,
        notes: Optional[str] = None
    ) -> Dict:
        """
        Admin creates a personalized subscription offer for a user
        This is sent during onboarding
        
        Args:
            user_id: User receiving the offer
            tier: Subscription tier
            custom_price: Custom pricing (overrides default)
            custom_features: Additional features beyond tier defaults
            discount_percent: Discount percentage (0-100)
            notes: Admin notes about this offer
            
        Returns:
            Subscription offer details
        """
        pricing = BillingService.get_subscription_pricing(tier, custom_price)
        base_price = pricing["base_price"]
        
        if base_price is None:
            raise ValueError("Price must be set for custom subscriptions")
        
        # Calculate final price with discount
        discount_amount = (base_price * discount_percent) / 100
        final_price = base_price - discount_amount
        
        # Merge features
        features = pricing["features"].copy()
        if custom_features:
            features.extend(custom_features)
        
        offer = {
            "offer_id": f"OFFER-{user_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "user_id": user_id,
            "tier": tier.value,
            "base_price": base_price,
            "discount_percent": discount_percent,
            "discount_amount": discount_amount,
            "final_price": final_price,
            "currency": pricing["currency"],
            "billing_cycle": pricing["billing_cycle"],
            "features": features,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=7)).isoformat(),
            "admin_notes": notes,
            "status": "pending"
        }
        
        return offer
    
    @staticmethod
    def generate_secure_payment_link(offer_id: str, user_email: str) -> str:
        """
        Generate a secure payment collection link
        This link is sent to the user during onboarding
        
        In production, this would integrate with:
        - Stripe Payment Links
        - PayPal
        - or custom secure payment gateway
        """
        # In production, integrate with payment processor
        # For now, return a placeholder secure link
        
        import hashlib
        import secrets
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        
        # Create hash for verification
        verification_hash = hashlib.sha256(
            f"{offer_id}{user_email}{token}".encode()
        ).hexdigest()[:16]
        
        # Construct secure payment URL
        payment_url = f"https://secure.reputationguardian.com/payment/{offer_id}?token={token}&verify={verification_hash}"
        
        return payment_url
    
    @staticmethod
    def generate_onboarding_portal_link(
        user_id: int,
        offer_id: str,
        include_document_upload: bool = True,
        include_video_upload: bool = True,
        include_photo_upload: bool = True
    ) -> str:
        """
        Generate secure onboarding portal link
        This portal allows users to:
        - Review subscription offer
        - Upload documents (ID, business docs, etc.)
        - Upload photos for profile
        - Record/upload video introduction
        - Input payment information
        
        Args:
            user_id: User ID
            offer_id: Subscription offer ID
            include_document_upload: Allow document uploads
            include_video_upload: Allow video uploads
            include_photo_upload: Allow photo uploads
            
        Returns:
            Secure onboarding portal URL
        """
        import secrets
        
        token = secrets.token_urlsafe(32)
        
        # Build portal URL with features
        features = []
        if include_document_upload:
            features.append("docs")
        if include_video_upload:
            features.append("video")
        if include_photo_upload:
            features.append("photos")
        
        portal_url = (
            f"https://onboarding.reputationguardian.com/complete/{user_id}?"
            f"offer={offer_id}&token={token}&features={','.join(features)}"
        )
        
        return portal_url
    
    @staticmethod
    def create_subscription(
        user_id: int,
        offer_id: str,
        payment_method_id: str,
        billing_details: Dict
    ) -> Dict:
        """
        Create active subscription after payment is collected
        
        Args:
            user_id: User ID
            offer_id: Accepted offer ID
            payment_method_id: Payment method token from payment processor
            billing_details: Billing address and details
            
        Returns:
            Subscription details
        """
        subscription = {
            "subscription_id": f"SUB-{user_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "user_id": user_id,
            "offer_id": offer_id,
            "payment_method_id": payment_method_id,
            "status": "active",
            "started_at": datetime.now().isoformat(),
            "current_period_start": datetime.now().isoformat(),
            "current_period_end": (datetime.now() + timedelta(days=30)).isoformat(),
            "billing_details": billing_details,
            "auto_renew": True
        }
        
        return subscription
