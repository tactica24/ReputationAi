"""
Notification & Alert System
Real-time alerts via email, SMS, push notifications with customizable thresholds
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class NotificationChannel(Enum):
    """Notification delivery channels"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    WEBHOOK = "webhook"
    SLACK = "slack"
    TEAMS = "teams"


class NotificationPriority(Enum):
    """Notification priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class NotificationPreferences:
    """User notification preferences"""
    user_id: str
    enabled_channels: List[NotificationChannel]
    email_address: Optional[str] = None
    phone_number: Optional[str] = None
    push_token: Optional[str] = None
    webhook_url: Optional[str] = None
    
    # Threshold settings
    min_reputation_change: float = 5.0
    min_sentiment_change: float = 10.0
    alert_on_spike: bool = True
    alert_on_negative_trend: bool = True
    
    # Scheduling
    quiet_hours_start: Optional[int] = None  # Hour (0-23)
    quiet_hours_end: Optional[int] = None
    
    # Report frequency
    daily_summary: bool = True
    weekly_summary: bool = True
    monthly_summary: bool = True


@dataclass
class Notification:
    """Notification message"""
    notification_id: str
    user_id: str
    entity_id: str
    entity_name: str
    priority: NotificationPriority
    title: str
    message: str
    data: Dict
    channels: List[NotificationChannel]
    created_at: datetime
    sent_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "priority": self.priority.value,
            "title": self.title,
            "message": self.message,
            "data": self.data,
            "channels": [c.value for c in self.channels],
            "created_at": self.created_at.isoformat(),
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None
        }


class NotificationService:
    """
    Unified notification service supporting multiple channels
    """
    
    def __init__(self, config: Dict):
        """
        Initialize notification service
        
        Args:
            config: Configuration with API keys and credentials
        """
        self.config = config
        self.notification_queue: List[Notification] = []
        self.sent_notifications: List[Notification] = []
        
        # Initialize channel handlers
        self.email_config = config.get('email', {})
        self.sms_config = config.get('sms', {})
        self.push_config = config.get('push', {})
    
    async def send_notification(
        self,
        notification: Notification,
        preferences: NotificationPreferences
    ) -> Dict[str, bool]:
        """
        Send notification through configured channels
        
        Args:
            notification: Notification to send
            preferences: User preferences
            
        Returns:
            Dictionary of channel success status
        """
        results = {}
        
        # Check quiet hours
        if self._is_quiet_hours(preferences):
            if notification.priority != NotificationPriority.URGENT:
                self.notification_queue.append(notification)
                return {"queued": True}
        
        # Send through each channel
        for channel in notification.channels:
            if channel in preferences.enabled_channels:
                try:
                    if channel == NotificationChannel.EMAIL:
                        results['email'] = await self._send_email(notification, preferences)
                    elif channel == NotificationChannel.SMS:
                        results['sms'] = await self._send_sms(notification, preferences)
                    elif channel == NotificationChannel.PUSH:
                        results['push'] = await self._send_push(notification, preferences)
                    elif channel == NotificationChannel.WEBHOOK:
                        results['webhook'] = await self._send_webhook(notification, preferences)
                    elif channel == NotificationChannel.SLACK:
                        results['slack'] = await self._send_slack(notification, preferences)
                except Exception as e:
                    results[channel.value] = False
                    print(f"Error sending {channel.value} notification: {e}")
        
        notification.sent_at = datetime.now()
        self.sent_notifications.append(notification)
        
        return results
    
    async def _send_email(self, notification: Notification, preferences: NotificationPreferences) -> bool:
        """Send email notification"""
        if not preferences.email_address:
            return False
        
        try:
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"[{notification.priority.value.upper()}] {notification.title}"
            msg['From'] = self.email_config.get('from_address', 'noreply@aiguardian.com')
            msg['To'] = preferences.email_address
            
            # Create HTML content
            html_content = self._generate_email_html(notification)
            
            # Attach both plain text and HTML
            text_part = MIMEText(notification.message, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.email_config.get('smtp_host', 'smtp.gmail.com'), 
                            self.email_config.get('smtp_port', 587)) as server:
                server.starttls()
                server.login(
                    self.email_config.get('username'),
                    self.email_config.get('password')
                )
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email send error: {e}")
            return False
    
    async def _send_sms(self, notification: Notification, preferences: NotificationPreferences) -> bool:
        """Send SMS notification"""
        if not preferences.phone_number:
            return False
        
        # Placeholder for SMS integration (Twilio, AWS SNS, etc.)
        """
        from twilio.rest import Client
        
        client = Client(
            self.sms_config.get('account_sid'),
            self.sms_config.get('auth_token')
        )
        
        message = client.messages.create(
            body=f"{notification.title}: {notification.message}",
            from_=self.sms_config.get('from_number'),
            to=preferences.phone_number
        )
        
        return message.status in ['queued', 'sent']
        """
        return True
    
    async def _send_push(self, notification: Notification, preferences: NotificationPreferences) -> bool:
        """Send push notification"""
        if not preferences.push_token:
            return False
        
        # Placeholder for push notification (Firebase FCM, OneSignal, etc.)
        """
        from firebase_admin import messaging
        
        message = messaging.Message(
            notification=messaging.Notification(
                title=notification.title,
                body=notification.message
            ),
            token=preferences.push_token,
            data=notification.data
        )
        
        response = messaging.send(message)
        return bool(response)
        """
        return True
    
    async def _send_webhook(self, notification: Notification, preferences: NotificationPreferences) -> bool:
        """Send webhook notification"""
        if not preferences.webhook_url:
            return False
        
        # Placeholder for webhook
        """
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                preferences.webhook_url,
                json=notification.to_dict(),
                timeout=10.0
            )
            return response.status_code == 200
        """
        return True
    
    async def _send_slack(self, notification: Notification, preferences: NotificationPreferences) -> bool:
        """Send Slack notification"""
        # Placeholder for Slack integration
        """
        from slack_sdk.webhook import WebhookClient
        
        webhook = WebhookClient(preferences.webhook_url)
        
        response = webhook.send(
            text=notification.title,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{notification.title}*\n{notification.message}"
                    }
                }
            ]
        )
        
        return response.status_code == 200
        """
        return True
    
    def _generate_email_html(self, notification: Notification) -> str:
        """Generate HTML email content"""
        priority_colors = {
            NotificationPriority.LOW: "#4CAF50",
            NotificationPriority.MEDIUM: "#FF9800",
            NotificationPriority.HIGH: "#FF5722",
            NotificationPriority.URGENT: "#F44336"
        }
        
        color = priority_colors.get(notification.priority, "#2196F3")
        
        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: {color}; color: white; padding: 20px; border-radius: 5px 5px 0 0; }}
                .content {{ background: #f5f5f5; padding: 20px; }}
                .footer {{ background: #333; color: white; padding: 10px; text-align: center; border-radius: 0 0 5px 5px; }}
                .button {{ background: {color}; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🛡️ AI Guardian Alert</h2>
                    <p>{notification.title}</p>
                </div>
                <div class="content">
                    <p><strong>Entity:</strong> {notification.entity_name}</p>
                    <p><strong>Priority:</strong> {notification.priority.value.upper()}</p>
                    <p>{notification.message}</p>
                    <br>
                    <a href="https://app.aiguardian.com/alerts/{notification.notification_id}" class="button">
                        View Details
                    </a>
                </div>
                <div class="footer">
                    <p>AI Reputation & Identity Guardian</p>
                    <p><small>Sent at {notification.created_at.strftime('%Y-%m-%d %H:%M:%S')}</small></p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _is_quiet_hours(self, preferences: NotificationPreferences) -> bool:
        """Check if current time is within quiet hours"""
        if preferences.quiet_hours_start is None or preferences.quiet_hours_end is None:
            return False
        
        current_hour = datetime.now().hour
        
        if preferences.quiet_hours_start < preferences.quiet_hours_end:
            return preferences.quiet_hours_start <= current_hour < preferences.quiet_hours_end
        else:  # Quiet hours span midnight
            return current_hour >= preferences.quiet_hours_start or current_hour < preferences.quiet_hours_end
    
    async def send_summary_report(
        self,
        user_id: str,
        entity_id: str,
        report_data: Dict,
        report_type: str = "daily"
    ) -> bool:
        """
        Send scheduled summary report
        
        Args:
            user_id: User ID
            entity_id: Entity ID
            report_data: Report data dictionary
            report_type: Type of report (daily, weekly, monthly)
            
        Returns:
            Success status
        """
        # Generate report notification
        notification = Notification(
            notification_id=f"report_{user_id}_{datetime.now().timestamp()}",
            user_id=user_id,
            entity_id=entity_id,
            entity_name=report_data.get('entity_name', 'Unknown'),
            priority=NotificationPriority.LOW,
            title=f"{report_type.capitalize()} Reputation Report",
            message=self._generate_report_summary(report_data),
            data=report_data,
            channels=[NotificationChannel.EMAIL],
            created_at=datetime.now()
        )
        
        # Get user preferences (placeholder - would fetch from database)
        preferences = NotificationPreferences(
            user_id=user_id,
            enabled_channels=[NotificationChannel.EMAIL],
            email_address="user@example.com"
        )
        
        results = await self.send_notification(notification, preferences)
        return results.get('email', False)
    
    def _generate_report_summary(self, report_data: Dict) -> str:
        """Generate summary text for report"""
        return f"""
        Summary for {report_data.get('entity_name')}:
        
        • Reputation Score: {report_data.get('reputation_score', 'N/A')}/100
        • Total Mentions: {report_data.get('total_mentions', 0)}
        • Sentiment: {report_data.get('average_sentiment', 'Neutral')}
        • Trend: {report_data.get('trend_direction', 'Stable')}
        
        View full report in your dashboard.
        """


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_notifications():
        # Initialize service
        service = NotificationService(config={
            'email': {
                'smtp_host': 'smtp.gmail.com',
                'smtp_port': 587,
                'from_address': 'alerts@aiguardian.com',
                'username': 'your_email@gmail.com',
                'password': 'your_password'
            }
        })
        
        # Create test notification
        notification = Notification(
            notification_id="test_123",
            user_id="user_456",
            entity_id="entity_789",
            entity_name="Test Company",
            priority=NotificationPriority.HIGH,
            title="Reputation Alert: Negative Sentiment Spike",
            message="We detected a 35% increase in negative mentions in the last 2 hours.",
            data={'spike_percentage': 35, 'source': 'twitter'},
            channels=[NotificationChannel.EMAIL],
            created_at=datetime.now()
        )
        
        # User preferences
        preferences = NotificationPreferences(
            user_id="user_456",
            enabled_channels=[NotificationChannel.EMAIL],
            email_address="test@example.com"
        )
        
        # Send notification
        results = await service.send_notification(notification, preferences)
        print(f"Notification sent: {results}")
    
    asyncio.run(test_notifications())
