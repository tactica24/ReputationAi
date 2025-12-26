"""
GraphQL API Layer
Flexible data querying with schema, resolvers, and subscriptions
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
import asyncio


# ==================== Enums ====================

@strawberry.enum
class EntityType(Enum):
    PERSON = "person"
    COMPANY = "company"
    BRAND = "brand"
    PRODUCT = "product"


@strawberry.enum
class SentimentType(Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@strawberry.enum
class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ==================== Types ====================

@strawberry.type
class User:
    id: int
    email: str
    name: str
    tier: str
    created_at: datetime
    is_active: bool


@strawberry.type
class Entity:
    id: int
    name: str
    entity_type: EntityType
    description: Optional[str]
    reputation_score: float
    created_at: datetime
    updated_at: datetime
    user_id: int


@strawberry.type
class Mention:
    id: int
    entity_id: int
    content: str
    source_name: str
    source_url: str
    author: Optional[str]
    sentiment: SentimentType
    sentiment_score: float
    language: str
    engagement_score: int
    published_at: datetime
    created_at: datetime


@strawberry.type
class Alert:
    id: int
    entity_id: int
    severity: AlertSeverity
    title: str
    description: str
    is_read: bool
    created_at: datetime
    
    @strawberry.field
    async def entity(self, info: Info) -> Optional[Entity]:
        """Resolve entity for this alert"""
        # Would query database in production
        return None


@strawberry.type
class ReputationTrend:
    date: datetime
    score: float
    mention_count: int
    sentiment_distribution: str  # JSON string


@strawberry.type
class Analytics:
    entity_id: int
    total_mentions: int
    positive_mentions: int
    neutral_mentions: int
    negative_mentions: int
    average_sentiment: float
    reputation_score: float
    trend_direction: str
    
    @strawberry.field
    async def reputation_history(
        self,
        days: int = 30
    ) -> List[ReputationTrend]:
        """Get reputation history for specified days"""
        # Would query database in production
        return []


@strawberry.type
class PredictiveInsight:
    entity_id: int
    predicted_score: float
    confidence: float
    trend: str
    crisis_level: str
    risk_score: float
    emerging_trends: str  # JSON string
    generated_at: datetime


@strawberry.type
class SearchResult:
    entities: List[Entity]
    mentions: List[Mention]
    total_count: int


# ==================== Input Types ====================

@strawberry.input
class CreateEntityInput:
    name: str
    entity_type: EntityType
    description: Optional[str] = None


@strawberry.input
class UpdateEntityInput:
    id: int
    name: Optional[str] = None
    description: Optional[str] = None


@strawberry.input
class MentionFilterInput:
    entity_id: Optional[int] = None
    sentiment: Optional[SentimentType] = None
    source_name: Optional[str] = None
    language: Optional[str] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None


@strawberry.input
class AlertFilterInput:
    entity_id: Optional[int] = None
    severity: Optional[AlertSeverity] = None
    is_read: Optional[bool] = None


# ==================== Queries ====================

@strawberry.type
class Query:
    """GraphQL Query root"""
    
    @strawberry.field
    async def me(self, info: Info) -> Optional[User]:
        """Get current authenticated user"""
        # Would get from context/JWT in production
        return User(
            id=1,
            email="user@example.com",
            name="Demo User",
            tier="professional",
            created_at=datetime.utcnow(),
            is_active=True
        )
    
    @strawberry.field
    async def entity(
        self,
        id: int,
        info: Info
    ) -> Optional[Entity]:
        """Get entity by ID"""
        # Would query database in production
        return Entity(
            id=id,
            name="Demo Entity",
            entity_type=EntityType.COMPANY,
            description="Example entity",
            reputation_score=75.5,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            user_id=1
        )
    
    @strawberry.field
    async def entities(
        self,
        limit: int = 10,
        offset: int = 0,
        info: Info
    ) -> List[Entity]:
        """Get list of entities"""
        # Would query database in production
        return []
    
    @strawberry.field
    async def mentions(
        self,
        filter: Optional[MentionFilterInput] = None,
        limit: int = 20,
        offset: int = 0,
        info: Info
    ) -> List[Mention]:
        """Get mentions with optional filters"""
        # Would query database with filters in production
        return []
    
    @strawberry.field
    async def alerts(
        self,
        filter: Optional[AlertFilterInput] = None,
        limit: int = 20,
        offset: int = 0,
        info: Info
    ) -> List[Alert]:
        """Get alerts with optional filters"""
        # Would query database in production
        return []
    
    @strawberry.field
    async def analytics(
        self,
        entity_id: int,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        info: Info
    ) -> Optional[Analytics]:
        """Get analytics for entity"""
        # Would calculate from database in production
        return Analytics(
            entity_id=entity_id,
            total_mentions=150,
            positive_mentions=80,
            neutral_mentions=50,
            negative_mentions=20,
            average_sentiment=0.72,
            reputation_score=75.5,
            trend_direction="upward"
        )
    
    @strawberry.field
    async def predictive_insights(
        self,
        entity_id: int,
        info: Info
    ) -> Optional[PredictiveInsight]:
        """Get predictive insights for entity"""
        # Would call predictive engine in production
        return PredictiveInsight(
            entity_id=entity_id,
            predicted_score=78.2,
            confidence=0.85,
            trend="upward",
            crisis_level="low",
            risk_score=15.0,
            emerging_trends='["topic1", "topic2"]',
            generated_at=datetime.utcnow()
        )
    
    @strawberry.field
    async def search(
        self,
        query: str,
        limit: int = 10,
        info: Info
    ) -> SearchResult:
        """Search across entities and mentions"""
        # Would perform full-text search in production
        return SearchResult(
            entities=[],
            mentions=[],
            total_count=0
        )


# ==================== Mutations ====================

@strawberry.type
class Mutation:
    """GraphQL Mutation root"""
    
    @strawberry.mutation
    async def create_entity(
        self,
        input: CreateEntityInput,
        info: Info
    ) -> Entity:
        """Create new entity"""
        # Would insert into database in production
        return Entity(
            id=1,
            name=input.name,
            entity_type=input.entity_type,
            description=input.description,
            reputation_score=50.0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            user_id=1
        )
    
    @strawberry.mutation
    async def update_entity(
        self,
        input: UpdateEntityInput,
        info: Info
    ) -> Optional[Entity]:
        """Update existing entity"""
        # Would update database in production
        return None
    
    @strawberry.mutation
    async def delete_entity(
        self,
        id: int,
        info: Info
    ) -> bool:
        """Delete entity"""
        # Would delete from database in production
        return True
    
    @strawberry.mutation
    async def mark_alert_read(
        self,
        id: int,
        info: Info
    ) -> Optional[Alert]:
        """Mark alert as read"""
        # Would update database in production
        return None
    
    @strawberry.mutation
    async def mark_all_alerts_read(
        self,
        entity_id: Optional[int] = None,
        info: Info
    ) -> int:
        """Mark all alerts as read, optionally filtered by entity"""
        # Would update database in production
        return 0


# ==================== Subscriptions ====================

@strawberry.type
class Subscription:
    """GraphQL Subscription root for real-time updates"""
    
    @strawberry.subscription
    async def mention_added(
        self,
        entity_id: Optional[int] = None,
        info: Info
    ) -> Mention:
        """Subscribe to new mentions"""
        # Simulate real-time updates
        while True:
            await asyncio.sleep(5)  # Poll every 5 seconds
            
            # Would use WebSocket/PubSub in production
            yield Mention(
                id=1,
                entity_id=entity_id or 1,
                content="New mention detected",
                source_name="Twitter",
                source_url="https://twitter.com/example",
                author="@user",
                sentiment=SentimentType.POSITIVE,
                sentiment_score=0.85,
                language="en",
                engagement_score=100,
                published_at=datetime.utcnow(),
                created_at=datetime.utcnow()
            )
    
    @strawberry.subscription
    async def alert_created(
        self,
        entity_id: Optional[int] = None,
        min_severity: Optional[AlertSeverity] = None,
        info: Info
    ) -> Alert:
        """Subscribe to new alerts"""
        while True:
            await asyncio.sleep(10)
            
            # Would use WebSocket/PubSub in production
            yield Alert(
                id=1,
                entity_id=entity_id or 1,
                severity=AlertSeverity.MEDIUM,
                title="New alert",
                description="Alert description",
                is_read=False,
                created_at=datetime.utcnow()
            )
    
    @strawberry.subscription
    async def reputation_updated(
        self,
        entity_id: int,
        info: Info
    ) -> ReputationTrend:
        """Subscribe to reputation score updates"""
        while True:
            await asyncio.sleep(60)  # Update every minute
            
            # Would use WebSocket/PubSub in production
            yield ReputationTrend(
                date=datetime.utcnow(),
                score=75.5,
                mention_count=10,
                sentiment_distribution='{"positive": 60, "neutral": 30, "negative": 10}'
            )


# ==================== Schema ====================

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)


# ==================== GraphQL Router ====================

def create_graphql_router() -> GraphQLRouter:
    """Create GraphQL router for FastAPI"""
    return GraphQLRouter(
        schema,
        graphiql=True,  # Enable GraphiQL IDE
        path="/graphql"
    )


# ==================== Example Queries ====================

EXAMPLE_QUERIES = """
# Get current user
query GetMe {
  me {
    id
    email
    name
    tier
  }
}

# Get entity with analytics
query GetEntity($id: Int!) {
  entity(id: $id) {
    id
    name
    entityType
    reputationScore
  }
  analytics(entityId: $id) {
    totalMentions
    positiveMentions
    negativeMentions
    averageSentiment
    trendDirection
  }
}

# Search mentions with filters
query SearchMentions($filter: MentionFilterInput, $limit: Int) {
  mentions(filter: $filter, limit: $limit) {
    id
    content
    sentiment
    sentimentScore
    sourceName
    publishedAt
  }
}

# Get predictive insights
query GetPredictions($entityId: Int!) {
  predictiveInsights(entityId: $entityId) {
    predictedScore
    confidence
    trend
    crisisLevel
    riskScore
  }
}

# Create entity
mutation CreateEntity($input: CreateEntityInput!) {
  createEntity(input: $input) {
    id
    name
    entityType
    reputationScore
  }
}

# Subscribe to new mentions
subscription OnMentionAdded($entityId: Int) {
  mentionAdded(entityId: $entityId) {
    id
    content
    sentiment
    sourceName
    publishedAt
  }
}

# Subscribe to alerts
subscription OnAlertCreated($entityId: Int, $minSeverity: AlertSeverity) {
  alertCreated(entityId: $entityId, minSeverity: $minSeverity) {
    id
    severity
    title
    description
    createdAt
  }
}
"""
