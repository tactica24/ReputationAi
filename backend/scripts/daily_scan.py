#!/usr/bin/env python3
"""
Comprehensive daily scan
Runs at 2 AM daily via cron
More thorough than the 15-minute incremental scans
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.services.scraping.free_web_scraper import PublicContentScraper, MonitoringOrchestrator
from backend.services.ai_detection.free_ai_engine import FreeAIDetectionEngine
from backend.database.models import SessionLocal, MonitoredPerson, Alert, DailyReport
from sqlalchemy import select


async def run_daily_scan():
    """Run comprehensive daily scan"""
    
    print(f"[{datetime.now()}] Starting daily comprehensive scan...")
    
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
        
        for person in persons:
            try:
                print(f"\n{'='*60}")
                print(f"Daily Scan: {person.name}")
                print(f"{'='*60}")
                
                # More comprehensive search
                # Include variations of name, historical data, deep search
                
                # Scrape all platforms
                all_content = await orchestrator.monitor_person(
                    person_name=person.name,
                    aliases=person.aliases or [],
                    social_handles=person.social_handles or {},
                    keywords=person.keywords or [],
                    comprehensive=True  # Deep search mode
                )
                
                print(f"  Found {len(all_content)} total items")
                
                # Analyze all content
                fake_news_count = 0
                negative_sentiment_count = 0
                deepfake_count = 0
                alerts_created = 0
                
                for content in all_content:
                    # Run comprehensive AI detection
                    fake_news = await ai_engine.detect_fake_news(
                        content.text,
                        content.url
                    )
                    
                    sentiment = await ai_engine.detect_sentiment_threat(
                        content.text,
                        person.name
                    )
                    
                    # Check for deepfakes if image/video
                    if content.media_urls:
                        for media_url in content.media_urls:
                            if media_url.endswith(('.jpg', '.jpeg', '.png')):
                                deepfake = await ai_engine.detect_deepfake_image(media_url)
                                if deepfake.is_deepfake:
                                    deepfake_count += 1
                    
                    # Count threats
                    if fake_news.is_fake:
                        fake_news_count += 1
                    
                    if sentiment.severity in ['medium', 'high', 'critical']:
                        negative_sentiment_count += 1
                    
                    # Create alert for serious threats
                    if (sentiment.severity in ['high', 'critical'] or 
                        (fake_news.is_fake and fake_news.confidence > 0.8)):
                        
                        alert = Alert(
                            monitored_person_id=person.id,
                            severity=sentiment.severity,
                            alert_type='daily_scan_threat',
                            content=content.text,
                            source_url=content.url,
                            source_platform=content.platform,
                            confidence_score=max(fake_news.confidence, sentiment.confidence),
                            metadata={
                                'fake_news': fake_news.to_dict(),
                                'sentiment': sentiment.to_dict(),
                                'scan_type': 'daily_comprehensive'
                            }
                        )
                        
                        db.add(alert)
                        alerts_created += 1
                
                # Create daily report
                report = DailyReport(
                    monitored_person_id=person.id,
                    scan_date=datetime.now().date(),
                    total_mentions=len(all_content),
                    fake_news_count=fake_news_count,
                    negative_sentiment_count=negative_sentiment_count,
                    deepfake_count=deepfake_count,
                    alerts_created=alerts_created,
                    summary={
                        'platforms_scanned': list(set([c.platform for c in all_content])),
                        'top_keywords': person.keywords,
                        'scan_duration_seconds': 0  # TODO: track duration
                    }
                )
                
                db.add(report)
                db.commit()
                
                print(f"\nDaily Summary for {person.name}:")
                print(f"  Total mentions: {len(all_content)}")
                print(f"  Fake news detected: {fake_news_count}")
                print(f"  Negative sentiment: {negative_sentiment_count}")
                print(f"  Deepfakes: {deepfake_count}")
                print(f"  Alerts created: {alerts_created}")
                
                # TODO: Generate PDF report and email to client
                # await generate_daily_report_pdf(person, report)
                # await send_daily_report_email(person.client_email, report)
                
            except Exception as e:
                print(f"  ❌ Error scanning {person.name}: {e}")
                continue
        
        print(f"\n[{datetime.now()}] Daily scan complete")
        
    finally:
        db.close()


async def main():
    """Main entry point"""
    try:
        await run_daily_scan()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
