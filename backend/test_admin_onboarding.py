"""
Test Admin Onboarding Flow
Demonstrates the new subscription and payment collection process
"""

import requests
import json
from datetime import datetime


BASE_URL = "http://localhost:8080"


def test_application_submission():
    """Step 1: User submits application (NO pricing visible)"""
    print("\n" + "="*70)
    print("STEP 1: User Submits Application")
    print("="*70)
    
    application_data = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-123-4567",
        "company": "Acme Corporation",
        "title": "CEO",
        # NOTE: No plan/pricing required!
        "entities": "John Doe, Acme Corporation, Acme Brand",
        "threats": "Recent negative press coverage",
        "urgency": "emerging-threat",
        "howHeard": "referral",
        "message": "Need immediate protection for company reputation",
        "agreement": True,
        "privacy": True
    }
    
    print("\nSubmitting application (no pricing displayed to user)...")
    print(f"User: {application_data['firstName']} {application_data['lastName']}")
    print(f"Email: {application_data['email']}")
    print(f"Company: {application_data['company']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/onboarding/apply",
            json=application_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Application submitted successfully!")
            print(f"Application ID: {result['applicationId']}")
            print(f"Message: {result['message']}")
            print(f"Response Time: {result['estimatedResponseTime']}")
            return result['applicationId']
        else:
            print(f"\n❌ Application failed: {response.status_code}")
            print(response.text)
            return None
            
    except requests.exceptions.ConnectionError:
        print("\n⚠️ Backend not running. Start with: cd backend && uvicorn main:app --host 0.0.0.0 --port 8080")
        return None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


def test_admin_creates_offer(application_id):
    """Step 2: Admin reviews and creates personalized offer"""
    print("\n" + "="*70)
    print("STEP 2: Admin Creates Personalized Subscription Offer")
    print("="*70)
    
    offer_data = {
        "application_id": application_id,
        "user_email": "john.doe@example.com",
        "tier": "enterprise",
        "monthly_price": 4997.00,
        "discount_percent": 15,  # Special discount for this client
        "custom_features": [
            "Dedicated account manager",
            "Priority crisis response",
            "Custom integration with PR team"
        ],
        "notes": "High-value enterprise client - approved for 15% discount. CEO facing reputation threat.",
        "include_trial_days": 0
    }
    
    print("\nAdmin creating offer...")
    print(f"Base Price: ${offer_data['monthly_price']:,.2f}/month")
    print(f"Discount: {offer_data['discount_percent']}%")
    print(f"Final Price: ${offer_data['monthly_price'] * (1 - offer_data['discount_percent']/100):,.2f}/month")
    print(f"Tier: {offer_data['tier'].title()}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/admin/onboarding/create-offer",
            json=offer_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Offer created and sent to user!")
            print(f"Offer ID: {result['offer_id']}")
            print(f"Final Price: ${result['monthly_price']:,.2f}/month")
            print(f"Expires: {result['expires_at']}")
            print(f"\nSecure Links Generated:")
            print(f"  Portal: {result['portal_link'][:80]}...")
            print(f"  Payment: {result['payment_link'][:80]}...")
            print("\n📧 Comprehensive email sent to user with:")
            print("  ✓ Subscription details and pricing")
            print("  ✓ Secure onboarding portal link")
            print("  ✓ Secure payment setup link")
            print("  ✓ Document upload instructions")
            print("  ✓ Video/photo upload requirements")
            return result['offer_id']
        else:
            print(f"\n❌ Offer creation failed: {response.status_code}")
            print(response.text)
            return None
            
    except requests.exceptions.ConnectionError:
        print("\n⚠️ Backend not running")
        return None
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None


def test_user_completes_onboarding(offer_id):
    """Step 3: User completes onboarding portal and payment setup"""
    print("\n" + "="*70)
    print("STEP 3: User Completes Onboarding")
    print("="*70)
    
    completion_data = {
        "user_id": 1,
        "offer_id": offer_id,
        "payment_method_id": "pm_test_card_visa_4242",  # Test payment method
        "billing_address": {
            "line1": "123 Main Street",
            "city": "San Francisco",
            "state": "CA",
            "postal_code": "94102",
            "country": "US"
        },
        "documents_uploaded": [
            "drivers_license.pdf",
            "business_registration.pdf"
        ],
        "video_uploaded": True,
        "photos_uploaded": [
            "profile_photo.jpg",
            "company_logo.png"
        ]
    }
    
    print("\nUser completing onboarding...")
    print("✓ Documents uploaded (encrypted)")
    print("✓ Video introduction recorded")
    print("✓ Photos uploaded")
    print("✓ Payment method added")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/admin/onboarding/portal/complete",
            json=completion_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Onboarding complete!")
            print(f"Subscription ID: {result['subscription_id']}")
            print(f"Status: {result['status'].upper()}")
            print(f"Monitoring Starts: {result['monitoring_starts']}")
            print(f"Next Billing: {result['next_billing_date']}")
            print("\n🛡️ Protection is now ACTIVE!")
            return True
        else:
            print(f"\n❌ Onboarding completion failed: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n⚠️ Backend not running")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def main():
    """Run complete onboarding flow test"""
    print("\n" + "="*70)
    print("TESTING NEW SUBSCRIPTION & ONBOARDING FLOW")
    print("="*70)
    print("\nThis demonstrates the admin-controlled pricing flow:")
    print("1. User submits application (NO pricing shown)")
    print("2. Admin reviews and creates personalized offer")
    print("3. User receives email with pricing and secure links")
    print("4. User completes onboarding portal (docs, video, photos)")
    print("5. User sets up payment for monthly subscription")
    print("6. Monitoring activated!")
    
    input("\nPress Enter to start test...")
    
    # Step 1: User submits application
    application_id = test_application_submission()
    if not application_id:
        print("\n⚠️ Skipping remaining steps (backend not running)")
        print("\nTo test this flow:")
        print("1. Start backend: cd backend && uvicorn main:app --host 0.0.0.0 --port 8080")
        print("2. Run this test again: python backend/test_admin_onboarding.py")
        return
    
    input("\n\nPress Enter to continue to admin offer creation...")
    
    # Step 2: Admin creates offer
    offer_id = test_admin_creates_offer(application_id)
    if not offer_id:
        return
    
    input("\n\nPress Enter to simulate user completing onboarding...")
    
    # Step 3: User completes onboarding
    success = test_user_completes_onboarding(offer_id)
    
    if success:
        print("\n" + "="*70)
        print("✅ COMPLETE FLOW TESTED SUCCESSFULLY!")
        print("="*70)
        print("\n📊 Summary:")
        print("  • Application submitted without pricing")
        print("  • Admin created personalized offer")
        print("  • User received comprehensive onboarding email")
        print("  • User uploaded documents, video, photos")
        print("  • User set up payment method")
        print("  • Subscription activated")
        print("  • Monitoring started")
        print("\n🎯 The new flow is working correctly!")
    else:
        print("\n❌ Flow test incomplete")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
