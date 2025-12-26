"""
Database models for the Reputation AI platform.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime,
    ForeignKey, JSON, Text, Index, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class UserRole(str, Enum):
    """User role enumeration for RBAC"""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MANAGER = "manager"
    ANALYST = "analyst"
    VIEWER = "viewer"


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class SentimentType(str, Enum):
    """Sentiment classification"""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    MIXED = "mixed"


class User(Base):
    """User model for authentication and authorization"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # GDPR
    gdpr_consent = Column(Boolean, default=False)
    data_retention_days = Column(Integer, default=365)
    
    # Relationships
    entities = relationship("Entity", back_populates="owner", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")

    __table_args__ = (
        Index('idx_user_email_active', 'email', 'is_active'),
    )


class Entity(Base):
    """Monitored entity (person, brand, organization)"""
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False)  # person, brand, organization
    description = Column(Text)
    
    # Owner
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Reputation metrics
    current_score = Column(Float, default=50.0)
    previous_score = Column(Float, default=50.0)
    score_trend = Column(String(20))  # up, down, stable
    
    # Monitoring settings
    keywords = Column(JSON, default=list)  # List of keywords to track
    excluded_keywords = Column(JSON, default=list)
    monitored_sources = Column(JSON, default=list)  # twitter, linkedin, news, etc.
    monitoring_enabled = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_monitored = Column(DateTime(timezone=True))
    
    # Relationships
    owner = relationship("User", back_populates="entities")
    mentions = relationship("Mention", back_populates="entity", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="entity", cascade="all, delete-orphan")
    reputation_history = relationship("ReputationHistory", back_populates="entity", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_entity_owner_active', 'owner_id', 'monitoring_enabled'),
    )


class Mention(Base):
    """Individual mention/reference to an entity"""
    __tablename__ = "mentions"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    
    # Source information
    source = Column(String(50), nullable=False, index=True)  # twitter, linkedin, news, reddit
    source_id = Column(String(255))  # External ID from source
    source_url = Column(String(1000))
    
    # Content
    content = Column(Text, nullable=False)
    author = Column(String(255))
    author_followers = Column(Integer, default=0)
    author_influence_score = Column(Float, default=0.0)
    
    # Sentiment analysis
    sentiment = Column(SQLEnum(SentimentType), nullable=False)
    sentiment_score = Column(Float, default=0.0)  # -1 to 1
    sentiment_confidence = Column(Float, default=0.0)
    
    # Engagement metrics
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    views = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)
    
    # AI analysis
    keywords_found = Column(JSON, default=list)
    topics = Column(JSON, default=list)
    entities_mentioned = Column(JSON, default=list)
    language = Column(String(10), default="en")
    
    # Timestamps
    published_at = Column(DateTime(timezone=True))
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Flags
    is_verified_author = Column(Boolean, default=False)
    is_influencer = Column(Boolean, default=False)
    requires_review = Column(Boolean, default=False)
    
    # Relationship
    entity = relationship("Entity", back_populates="mentions")

    __table_args__ = (
        Index('idx_mention_entity_date', 'entity_id', 'published_at'),
        Index('idx_mention_source_sentiment', 'source', 'sentiment'),
    )


class Alert(Base):
    """Alerts and notifications for significant events"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Alert details
    alert_type = Column(String(50), nullable=False)  # spike, sentiment_drop, crisis, trend
    severity = Column(SQLEnum(AlertSeverity), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    
    # Metadata
    data = Column(JSON)  # Additional context data
    threshold_value = Column(Float)
    actual_value = Column(Float)
    
    # Status
    is_read = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    entity = relationship("Entity", back_populates="alerts")
    user = relationship("User", back_populates="alerts", foreign_keys=[user_id])

    __table_args__ = (
        Index('idx_alert_user_read', 'user_id', 'is_read'),
        Index('idx_alert_severity_created', 'severity', 'created_at'),
    )


class ReputationHistory(Base):
    """Historical reputation scores for trend analysis"""
    __tablename__ = "reputation_history"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    
    # Score components
    overall_score = Column(Float, nullable=False)
    sentiment_score = Column(Float, nullable=False)
    volume_score = Column(Float, nullable=False)
    engagement_score = Column(Float, nullable=False)
    authority_score = Column(Float, nullable=False)
    
    # Metrics
    total_mentions = Column(Integer, default=0)
    positive_mentions = Column(Integer, default=0)
    neutral_mentions = Column(Integer, default=0)
    negative_mentions = Column(Integer, default=0)
    
    # Timestamp
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    entity = relationship("Entity", back_populates="reputation_history")

    __table_args__ = (
        Index('idx_reputation_entity_date', 'entity_id', 'recorded_at'),
    )


class AuditLog(Base):
    """Audit trail for compliance and security"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Action details
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50))
    resource_id = Column(Integer)
    
    # Context
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    details = Column(JSON)
    
    # Status
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", back_populates="audit_logs")

    __table_args__ = (
        Index('idx_audit_user_action_date', 'user_id', 'action', 'created_at'),
    )


class NotificationPreference(Base):
    """User notification preferences"""
    __tablename__ = "notification_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Channel preferences
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    push_enabled = Column(Boolean, default=True)
    slack_enabled = Column(Boolean, default=False)
    teams_enabled = Column(Boolean, default=False)
    
    # Alert preferences
    critical_alerts = Column(Boolean, default=True)
    high_alerts = Column(Boolean, default=True)
    medium_alerts = Column(Boolean, default=True)
    low_alerts = Column(Boolean, default=False)
    
    # Quiet hours
    quiet_hours_enabled = Column(Boolean, default=False)
    quiet_hours_start = Column(String(5))  # HH:MM format
    quiet_hours_end = Column(String(5))
    
    # Digest settings
    daily_digest = Column(Boolean, default=True)
    weekly_digest = Column(Boolean, default=True)
    
    # Contact info
    phone_number = Column(String(20))
    slack_webhook = Column(String(500))
    teams_webhook = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class APIKey(Base):
    """API keys for programmatic access"""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Key details
    key_hash = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    prefix = Column(String(10), nullable=False)
    
    # Permissions
    scopes = Column(JSON, default=list)  # List of allowed operations
    
    # Status
    is_active = Column(Boolean, default=True)
    last_used = Column(DateTime(timezone=True))
    usage_count = Column(Integer, default=0)
    
    # Expiration
    expires_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index('idx_apikey_user_active', 'user_id', 'is_active'),
    )
