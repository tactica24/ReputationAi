"""
Celery configuration and background tasks.
"""

from celery import Celery
from celery.schedules import crontab
import os
from datetime import datetime

# Initialize Celery
celery_app = Celery(
    'reputation_ai',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Periodic task schedule
celery_app.conf.beat_schedule = {
    # Monitor entities every 15 minutes
    'monitor-entities': {
        'task': 'backend.tasks.tasks.monitor_all_entities',
        'schedule': crontab(minute='*/15'),
    },
    # Update reputation scores hourly
    'update-reputation-scores': {
        'task': 'backend.tasks.tasks.update_reputation_scores',
        'schedule': crontab(minute=0),
    },
    # Check for alerts every 5 minutes
    'check-alerts': {
        'task': 'backend.tasks.tasks.check_and_send_alerts',
        'schedule': crontab(minute='*/5'),
    },
    # Send daily digest at 9 AM
    'daily-digest': {
        'task': 'backend.tasks.tasks.send_daily_digest',
        'schedule': crontab(hour=9, minute=0),
    },
    # Send weekly report every Monday at 10 AM
    'weekly-report': {
        'task': 'backend.tasks.tasks.send_weekly_report',
        'schedule': crontab(day_of_week=1, hour=10, minute=0),
    },
    # Cleanup old data every night at 2 AM
    'cleanup-old-data': {
        'task': 'backend.tasks.tasks.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),
    },
}
