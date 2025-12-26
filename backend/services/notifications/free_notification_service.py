"""
FREE Notification Service
Complete notification system using FREE tiers:
- Email: SendGrid (100 emails/day free)
- SMS: Twilio (trial credits, then $0.0075/SMS)
- Push: Firebase Cloud Messaging (free forever)

Total cost: $0-$50/month
"""

import os
import asyncio
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import aiohttp
import json


class NotificationChannel(Enum):
    """Notification delivery channels"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationPriority(Enum):
    """Notification priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class NotificationPreferences:
    """User notification preferences"""
    user_id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    push_token: Optional[str] = None
    
    # Channel preferences
    email_enabled: bool = True
    sms_enabled: bool = False  # Disabled by default (costs money)
    push_enabled: bool = True
    
    # Alert thresholds
    notify_on_high_threats: bool = True
    notify_on_medium_threats: bool = True
    notify_on_low_threats: bool = False
    
    # Frequency
    daily_summary: bool = True
    instant_alerts: bool = True


@dataclass
class Notification:
    """Notification message"""
    user_id: str
    title: str
    message: str
    priority: NotificationPriority
    data: Dict
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class FreeNotificationService:
    """
    Production-ready notification service using FREE tiers
    
    Cost breakdown:
    - SendGrid: 100 emails/day FREE
    - Twilio SMS: $0.0075 per SMS (optional)
    - Firebase FCM: FREE forever
    
    Total: $0/month for email + push
           $0.01-$1/month for SMS (if enabled)
    """
    
    def __init__(self):
        """Initialize with environment variables"""
        # SendGrid (FREE - 100 emails/day)
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('FROM_EMAIL', 'alerts@yourcompany.com')
        
        # Twilio (Optional - costs $0.0075/SMS)
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_from_number = os.getenv('TWILIO_FROM_NUMBER')
        
        # Firebase Cloud Messaging (FREE forever)
        self.fcm_server_key = os.getenv('FCM_SERVER_KEY')
        
        # Stats
        self.emails_sent_today = 0
        self.sms_sent_today = 0
        self.push_sent_today = 0
    
    
    async def send_alert(
        self,
        preferences: NotificationPreferences,
        notification: Notification
    ) -> Dict[str, bool]:
        """
        Send alert through all enabled channels
        
        Returns dict with success status for each channel
        """
        results = {}
        
        # Send email (FREE - SendGrid 100/day)
        if preferences.email_enabled and preferences.email:
            results['email'] = await self.send_email(
                to_email=preferences.email,
                subject=f"[{notification.priority.value.upper()}] {notification.title}",
                message=notification.message,
                data=notification.data
            )
        
        # Send SMS (COSTS MONEY - only for critical alerts or if enabled)
        if (preferences.sms_enabled and preferences.phone and 
            notification.priority == NotificationPriority.CRITICAL):
            results['sms'] = await self.send_sms(
                to_phone=preferences.phone,
                message=f"{notification.title}: {notification.message}"
            )
        
        # Send push notification (FREE - Firebase)
        if preferences.push_enabled and preferences.push_token:
            results['push'] = await self.send_push(
                token=preferences.push_token,
                title=notification.title,
                message=notification.message,
                data=notification.data
            )
        
        return results
    
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        message: str,
        data: Dict = None
    ) -> bool:
        """
        Send email via SendGrid (FREE - 100/day)
        
        Get API key: https://sendgrid.com/free/
        """
        if not self.sendgrid_api_key:
            print("⚠️  SendGrid API key not configured")
            return False
        
        if self.emails_sent_today >= 100:
            print("⚠️  Daily SendGrid limit reached (100 emails)")
            return False
        
        try:
            # Create HTML email
            html_content = self._create_email_html(subject, message, data)
            
            # SendGrid API payload
            payload = {
                "personalizations": [{
                    "to": [{"email": to_email}],
                    "subject": subject
                }],
                "from": {"email": self.from_email},
                "content": [
                    {
                        "type": "text/plain",
                        "value": message
                    },
                    {
                        "type": "text/html",
                        "value": html_content
                    }
                ]
            }
            
            # Send via SendGrid API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.sendgrid.com/v3/mail/send',
                    headers={
                        'Authorization': f'Bearer {self.sendgrid_api_key}',
                        'Content-Type': 'application/json'
                    },
                    json=payload
                ) as response:
                    if response.status == 202:
                        self.emails_sent_today += 1
                        print(f"✅ Email sent to {to_email}")
                        return True
                    else:
                        error = await response.text()
                        print(f"❌ Email failed: {error}")
                        return False
        
        except Exception as e:
            print(f"❌ Email error: {e}")
            return False
    
    
    async def send_sms(
        self,
        to_phone: str,
        message: str
    ) -> bool:
        """
        Send SMS via Twilio
        
        COST: $0.0075 per SMS (~$7.50 per 1000 SMS)
        FREE trial: $15 credit
        
        Get credentials: https://www.twilio.com/try-twilio
        """
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_from_number]):
            print("⚠️  Twilio credentials not configured")
            return False
        
        try:
            # Twilio API endpoint
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_account_sid}/Messages.json"
            
            # Payload
            payload = {
                'From': self.twilio_from_number,
                'To': to_phone,
                'Body': message[:160]  # SMS limit
            }
            
            # Send via Twilio API
            import base64
            auth = base64.b64encode(
                f"{self.twilio_account_sid}:{self.twilio_auth_token}".encode()
            ).decode()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers={'Authorization': f'Basic {auth}'},
                    data=payload
                ) as response:
                    if response.status in [200, 201]:
                        self.sms_sent_today += 1
                        print(f"✅ SMS sent to {to_phone} (Cost: $0.0075)")
                        return True
                    else:
                        error = await response.text()
                        print(f"❌ SMS failed: {error}")
                        return False
        
        except Exception as e:
            print(f"❌ SMS error: {e}")
            return False
    
    
    async def send_push(
        self,
        token: str,
        title: str,
        message: str,
        data: Dict = None
    ) -> bool:
        """
        Send push notification via Firebase Cloud Messaging (FREE forever)
        
        Get server key: https://console.firebase.google.com/
        Project Settings → Cloud Messaging → Server Key
        """
        if not self.fcm_server_key:
            print("⚠️  Firebase FCM server key not configured")
            return False
        
        try:
            # FCM API payload
            payload = {
                "to": token,
                "notification": {
                    "title": title,
                    "body": message,
                    "sound": "default",
                    "badge": "1"
                },
                "data": data or {},
                "priority": "high"
            }
            
            # Send via FCM API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://fcm.googleapis.com/fcm/send',
                    headers={
                        'Authorization': f'key={self.fcm_server_key}',
                        'Content-Type': 'application/json'
                    },
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result.get('success') == 1:
                            self.push_sent_today += 1
                            print(f"✅ Push notification sent")
                            return True
                        else:
                            print(f"❌ Push failed: {result}")
                            return False
                    else:
                        error = await response.text()
                        print(f"❌ Push failed: {error}")
                        return False
        
        except Exception as e:
            print(f"❌ Push error: {e}")
            return False
    
    
    def _create_email_html(self, subject: str, message: str, data: Dict = None) -> str:
        """Create HTML email template"""
        
        # Determine severity color
        severity_colors = {
            'critical': '#dc2626',
            'high': '#ea580c',
            'medium': '#f59e0b',
            'low': '#10b981'
        }
        
        severity = data.get('severity', 'medium') if data else 'medium'
        color = severity_colors.get(severity, '#6366f1')
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f3f4f6;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f3f4f6; padding: 40px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 700;">
                                🛡️ AI Reputation Guardian
                            </h1>
                        </td>
                    </tr>
                    
                    <!-- Alert Banner -->
                    <tr>
                        <td style="background-color: {color}; padding: 20px; text-align: center;">
                            <p style="color: #ffffff; margin: 0; font-size: 16px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                                {severity.upper()} ALERT
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="color: #1f2937; margin: 0 0 20px 0; font-size: 20px; font-weight: 600;">
                                {subject}
                            </h2>
                            
                            <p style="color: #4b5563; margin: 0 0 20px 0; font-size: 16px; line-height: 1.6;">
                                {message}
                            </p>
                            
                            {self._create_data_section(data) if data else ''}
                        </td>
                    </tr>
                    
                    <!-- Action Button -->
                    <tr>
                        <td style="padding: 0 30px 40px 30px; text-align: center;">
                            <a href="{data.get('url', '#') if data else '#'}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; padding: 14px 32px; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px;">
                                View Dashboard
                            </a>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f9fafb; padding: 30px; text-align: center; border-top: 1px solid #e5e7eb;">
                            <p style="color: #6b7280; margin: 0 0 10px 0; font-size: 14px;">
                                AI Reputation & Identity Guardian
                            </p>
                            <p style="color: #9ca3af; margin: 0; font-size: 12px;">
                                Protecting your reputation 24/7
                            </p>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
        """
        
        return html
    
    
    def _create_data_section(self, data: Dict) -> str:
        """Create additional data section for email"""
        if not data:
            return ""
        
        sections = []
        
        # Threat details
        if 'threat_type' in data:
            sections.append(f"""
                <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <p style="margin: 0; color: #92400e; font-weight: 600;">Threat Type:</p>
                    <p style="margin: 5px 0 0 0; color: #78350f;">{data['threat_type']}</p>
                </div>
            """)
        
        # Source information
        if 'source_url' in data:
            sections.append(f"""
                <div style="background-color: #e0e7ff; border-left: 4px solid #6366f1; padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <p style="margin: 0; color: #3730a3; font-weight: 600;">Source:</p>
                    <p style="margin: 5px 0 0 0; color: #4338ca;">
                        <a href="{data['source_url']}" style="color: #4338ca; text-decoration: underline;">
                            {data.get('source_platform', 'View Source')}
                        </a>
                    </p>
                </div>
            """)
        
        # Confidence score
        if 'confidence' in data:
            confidence_pct = int(data['confidence'] * 100)
            sections.append(f"""
                <div style="background-color: #f3f4f6; padding: 15px; margin: 20px 0; border-radius: 4px;">
                    <p style="margin: 0; color: #374151; font-weight: 600;">AI Confidence:</p>
                    <p style="margin: 5px 0 0 0; color: #1f2937; font-size: 24px; font-weight: 700;">
                        {confidence_pct}%
                    </p>
                </div>
            """)
        
        return ''.join(sections)
    
    
    async def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email after onboarding approval"""
        
        subject = "Welcome to AI Reputation Guardian! 🛡️"
        
        message = f"""
Dear {user_name},

Welcome to AI Reputation Guardian!

Your application has been approved and your account is now active. We're excited to help protect your reputation 24/7.

What happens next:
✅ Our AI will begin monitoring for threats immediately
✅ You'll receive real-time alerts via email and push notifications
✅ Daily reports will be sent to your inbox at 8 AM
✅ Access your dashboard anytime at https://yourcompany.com/dashboard

Your monitoring is now LIVE and running.

If you have any questions, reply to this email or contact support@yourcompany.com.

Best regards,
The AI Guardian Team
        """
        
        data = {
            'severity': 'low',
            'url': 'https://yourcompany.com/dashboard',
            'welcome': True
        }
        
        return await self.send_email(user_email, subject, message, data)
    
    
    async def send_threat_alert(
        self,
        preferences: NotificationPreferences,
        threat_details: Dict
    ) -> Dict[str, bool]:
        """Send immediate threat alert"""
        
        notification = Notification(
            user_id=preferences.user_id,
            title=f"⚠️ {threat_details['threat_type']} Detected",
            message=threat_details['message'],
            priority=NotificationPriority[threat_details['severity'].upper()],
            data=threat_details
        )
        
        return await self.send_alert(preferences, notification)
    
    
    def get_daily_stats(self) -> Dict:
        """Get daily notification stats"""
        return {
            'emails_sent': self.emails_sent_today,
            'sms_sent': self.sms_sent_today,
            'push_sent': self.push_sent_today,
            'total_cost': self.sms_sent_today * 0.0075  # Only SMS costs money
        }


# Example usage
async def example_usage():
    """Example of how to use the notification service"""
    
    # Initialize service
    notif_service = FreeNotificationService()
    
    # User preferences
    preferences = NotificationPreferences(
        user_id="user_123",
        email="client@example.com",
        phone="+1234567890",
        push_token="firebase_token_here",
        email_enabled=True,
        sms_enabled=True,  # Only for critical alerts
        push_enabled=True
    )
    
    # Send welcome email after onboarding
    await notif_service.send_welcome_email(
        user_email="client@example.com",
        user_name="John Doe"
    )
    
    # Send threat alert
    threat_details = {
        'threat_type': 'Fake News Detected',
        'severity': 'critical',
        'message': 'False article claiming company bankruptcy detected on social media',
        'source_url': 'https://twitter.com/example',
        'source_platform': 'Twitter',
        'confidence': 0.95
    }
    
    results = await notif_service.send_threat_alert(preferences, threat_details)
    print(f"Alert sent: {results}")
    
    # Check daily stats
    stats = notif_service.get_daily_stats()
    print(f"Daily stats: {stats}")


if __name__ == "__main__":
    asyncio.run(example_usage())
