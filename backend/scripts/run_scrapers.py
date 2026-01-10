#!/usr/bin/env python3
"""
Run scrapers for all active monitored persons
Runs every 15 minutes via cron
"""

import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.services.scraping.free_web_scraper import PublicContentScraper, MonitoringOrchestrator
from backend.services.ai_detection.free_ai_engine import FreeAIDetectionEngine
from backend.database.models import SessionLocal, MonitoredPerson, Alert
from sqlalchemy import select


async def run_monitoring_cycle():
    """Run one monitoring cycle for all active persons"""
    
    print(f"[{datetime.now()}] Starting monitoring cycle...")
    
    # Initialize services
    scraper = PublicContentScraper()
    ai_engine = FreeAIDetectionEngine()
    orchestrator = MonitoringOrchestrator(scraper)
    
    # Get database session
    db = SessionLocal()
    
    try:
        # Get all active monitored persons
        stmt = select(MonitoredPerson).where(MonitoredPerson.is_active == True)
        result = db.execute(stmt)
        persons = result.scalars().all()
        
        print(f"Found {len(persons)} active monitored persons")
        
        from backend.services.notifications.notification_service import NotificationService, Notification, NotificationChannel, NotificationPriority, NotificationPreferences
        # ...existing code...
        for person in persons:
            try:
                print(f"\nMonitoring: {person.name}")
                # Scrape content
                scraped_content = await orchestrator.monitor_person(
                    person_name=person.name,
                    aliases=person.aliases or [],
                    social_handles=person.social_handles or {},
                    keywords=person.keywords or []
                )
                print(f"  Found {len(scraped_content)} new items")
                # Analyze each piece of content
                alerts_created = 0
                new_alerts = []
                for content in scraped_content:
                    # Run AI detection
                    fake_news_result = await ai_engine.detect_fake_news(
                        content.text,
                        content.url
                    )
                    sentiment_result = await ai_engine.detect_sentiment_threat(
                        content.text,
                        person.name
                    )
                    # Check if content is threatening
                    if (fake_news_result.is_fake or 
                        sentiment_result.severity in ['high', 'critical']):
                        # Create alert
                        alert = Alert(
                            monitored_person_id=person.id,
                            severity=sentiment_result.severity,
                            alert_type='fake_news' if fake_news_result.is_fake else 'negative_sentiment',
                            content=content.text,
                            source_url=content.url,
                            source_platform=content.platform,
                            confidence_score=max(
                                fake_news_result.confidence,
                                sentiment_result.confidence
                            ),
                            metadata={
                                'fake_news': fake_news_result.to_dict(),
                                'sentiment': sentiment_result.to_dict(),
                                'scraped_at': content.timestamp.isoformat()
                            }
                        )
                        db.add(alert)
                        new_alerts.append(alert)
                        alerts_created += 1
                if alerts_created > 0:
                    db.commit()
                    print(f"  ⚠️  Created {alerts_created} alerts")
                    # --- Automatic notification to user ---
                    # Fetch user email and notification preferences
                    user = getattr(person, 'user', None)
                    if user and user.email:
                        # Fetch notification preferences (pseudo-code, adapt as needed)
                        prefs = db.execute(
                            """
                            SELECT * FROM notification_preferences WHERE user_id = :uid
                            """, {"uid": user.id}
                        ).fetchone()
                        enabled_channels = [NotificationChannel.EMAIL]
                        if prefs:
                            if getattr(prefs, 'push_enabled', False):
                                enabled_channels.append(NotificationChannel.PUSH)
                            if getattr(prefs, 'sms_enabled', False):
                                enabled_channels.append(NotificationChannel.SMS)
                        notification_service = NotificationService(config={
                            'email': {
                                'smtp_host': 'smtp.gmail.com',
                                'smtp_port': 587,
                                'from_address': 'alerts@aiguardian.com',
                                'username': os.environ.get('EMAIL_USER', ''),
                                'password': os.environ.get('EMAIL_PASS', '')
                            }
                        })
                        for alert in new_alerts:
                            notification = Notification(
                                notification_id=f"alert_{alert.id}",
                                user_id=user.id,
                                entity_id=alert.entity_id if hasattr(alert, 'entity_id') else None,
                                entity_name=person.name,
                                priority=NotificationPriority.HIGH if alert.severity in ['high', 'critical'] else NotificationPriority.MEDIUM,
                                title=f"New Mention Alert: {person.name}",
                                message=f"Your name was mentioned: '{alert.content[:120]}...' on {alert.source_platform}. See dashboard for details.",
                                data={"url": alert.source_url},
                                channels=enabled_channels,
                                created_at=datetime.now()
                            )
                            preferences = NotificationPreferences(
                                user_id=user.id,
                                enabled_channels=enabled_channels,
                                email_address=user.email,
                                push_token=getattr(prefs, 'push_token', None),
                                phone_number=getattr(prefs, 'phone_number', None)
                            )
                            await notification_service.send_notification(notification, preferences)
                else:
                    print(f"  ✅ No threats detected")
            except Exception as e:
                print(f"  ❌ Error monitoring {person.name}: {e}")
                continue
        
        print(f"\n[{datetime.now()}] Monitoring cycle complete")
        
    finally:
        db.close()


async def main():
    """Main entry point"""
    try:
        await run_monitoring_cycle()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
