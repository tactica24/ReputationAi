"""
Reputation Scoring System
Dynamic reputation score that updates in real-time based on AI-monitored data
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json


class ScoreCategory(Enum):
    """Categories for reputation scoring"""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    CRITICAL = "critical"


@dataclass
class ReputationScore:
    """Reputation score for an entity"""
    entity_id: str
    entity_name: str
    overall_score: float  # 0-100
    category: ScoreCategory
    sentiment_score: float
    volume_score: float
    engagement_score: float
    authority_score: float
    trend_direction: str  # "up", "down", "stable"
    last_updated: datetime
    historical_scores: List[float]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "overall_score": round(self.overall_score, 2),
            "category": self.category.value,
            "sentiment_score": round(self.sentiment_score, 2),
            "volume_score": round(self.volume_score, 2),
            "engagement_score": round(self.engagement_score, 2),
            "authority_score": round(self.authority_score, 2),
            "trend_direction": self.trend_direction,
            "last_updated": self.last_updated.isoformat(),
            "change_24h": self._calculate_change_24h()
        }
    
    def _calculate_change_24h(self) -> float:
        """Calculate score change in last 24 hours"""
        if len(self.historical_scores) < 2:
            return 0.0
        return self.overall_score - self.historical_scores[-2]


class ReputationScorer:
    """
    Calculate and maintain reputation scores with weighted components
    """
    
    # Weighted importance of different sources (news > social > forums)
    SOURCE_WEIGHTS = {
        'news': 1.0,
        'press_release': 0.95,
        'major_blog': 0.85,
        'linkedin': 0.75,
        'twitter': 0.70,
        'facebook': 0.65,
        'instagram': 0.60,
        'reddit': 0.55,
        'forum': 0.50,
        'review_site': 0.80,
        'blog': 0.60
    }
    
    # Component weights for overall score
    COMPONENT_WEIGHTS = {
        'sentiment': 0.40,      # 40% weight
        'volume': 0.25,         # 25% weight
        'engagement': 0.20,     # 20% weight
        'authority': 0.15       # 15% weight
    }
    
    def __init__(self):
        self.scores_cache: Dict[str, ReputationScore] = {}
        self.mention_history: Dict[str, List] = {}
    
    def calculate_score(
        self,
        entity_id: str,
        entity_name: str,
        mentions: List[Dict],
        time_window_hours: int = 24
    ) -> ReputationScore:
        """
        Calculate comprehensive reputation score for an entity
        
        Args:
            entity_id: Unique identifier for entity
            entity_name: Name of the entity
            mentions: List of mentions with sentiment data
            time_window_hours: Time window to consider
            
        Returns:
            ReputationScore object
        """
        # Filter mentions by time window
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        recent_mentions = [
            m for m in mentions 
            if datetime.fromisoformat(m.get('timestamp', datetime.now().isoformat())) >= cutoff_time
        ]
        
        if not recent_mentions:
            # Return default score
            return self._create_default_score(entity_id, entity_name)
        
        # Calculate component scores
        sentiment_score = self._calculate_sentiment_score(recent_mentions)
        volume_score = self._calculate_volume_score(recent_mentions, time_window_hours)
        engagement_score = self._calculate_engagement_score(recent_mentions)
        authority_score = self._calculate_authority_score(recent_mentions)
        
        # Calculate weighted overall score
        overall_score = (
            sentiment_score * self.COMPONENT_WEIGHTS['sentiment'] +
            volume_score * self.COMPONENT_WEIGHTS['volume'] +
            engagement_score * self.COMPONENT_WEIGHTS['engagement'] +
            authority_score * self.COMPONENT_WEIGHTS['authority']
        )
        
        # Determine category
        category = self._get_score_category(overall_score)
        
        # Determine trend
        trend = self._determine_trend(entity_id, overall_score)
        
        # Get historical scores
        historical = self._get_historical_scores(entity_id)
        historical.append(overall_score)
        
        # Create score object
        score = ReputationScore(
            entity_id=entity_id,
            entity_name=entity_name,
            overall_score=overall_score,
            category=category,
            sentiment_score=sentiment_score,
            volume_score=volume_score,
            engagement_score=engagement_score,
            authority_score=authority_score,
            trend_direction=trend,
            last_updated=datetime.now(),
            historical_scores=historical[-30:]  # Keep last 30 scores
        )
        
        # Cache the score
        self.scores_cache[entity_id] = score
        
        return score
    
    def _calculate_sentiment_score(self, mentions: List[Dict]) -> float:
        """
        Calculate sentiment component score (0-100)
        Weighted by source importance
        """
        if not mentions:
            return 50.0
        
        weighted_sentiment_sum = 0.0
        total_weight = 0.0
        
        for mention in mentions:
            sentiment = mention.get('sentiment', 'neutral')
            confidence = mention.get('confidence_score', 0.5)
            source = mention.get('source', 'unknown')
            
            # Get source weight
            source_weight = self.SOURCE_WEIGHTS.get(source.lower(), 0.5)
            
            # Convert sentiment to numeric value
            if sentiment == 'positive':
                sentiment_value = 100.0
            elif sentiment == 'negative':
                sentiment_value = 0.0
            else:
                sentiment_value = 50.0
            
            # Weight by confidence and source importance
            weight = confidence * source_weight
            weighted_sentiment_sum += sentiment_value * weight
            total_weight += weight
        
        if total_weight == 0:
            return 50.0
        
        return weighted_sentiment_sum / total_weight
    
    def _calculate_volume_score(self, mentions: List[Dict], time_window: int) -> float:
        """
        Calculate volume component score based on mention frequency
        More mentions = higher visibility/importance
        """
        mention_count = len(mentions)
        
        # Normalize based on time window
        mentions_per_hour = mention_count / time_window
        
        # Scale: 0-1 mentions/hour = 0-20 points
        #        1-5 mentions/hour = 20-60 points
        #        5-10 mentions/hour = 60-80 points
        #        10+ mentions/hour = 80-100 points
        
        if mentions_per_hour <= 1:
            return mentions_per_hour * 20
        elif mentions_per_hour <= 5:
            return 20 + ((mentions_per_hour - 1) / 4) * 40
        elif mentions_per_hour <= 10:
            return 60 + ((mentions_per_hour - 5) / 5) * 20
        else:
            return min(80 + (mentions_per_hour - 10) * 2, 100)
    
    def _calculate_engagement_score(self, mentions: List[Dict]) -> float:
        """
        Calculate engagement score based on interactions
        (likes, shares, comments, etc.)
        """
        if not mentions:
            return 0.0
        
        total_engagement = 0
        for mention in mentions:
            engagement = (
                mention.get('likes', 0) +
                mention.get('shares', 0) * 2 +  # Shares worth more
                mention.get('comments', 0) * 1.5
            )
            total_engagement += engagement
        
        # Average engagement per mention
        avg_engagement = total_engagement / len(mentions)
        
        # Scale logarithmically (engagement can vary widely)
        if avg_engagement <= 10:
            return avg_engagement * 5
        elif avg_engagement <= 100:
            return 50 + ((avg_engagement - 10) / 90) * 30
        else:
            return min(80 + (avg_engagement - 100) / 50, 100)
    
    def _calculate_authority_score(self, mentions: List[Dict]) -> float:
        """
        Calculate authority score based on source credibility
        and influencer mentions
        """
        if not mentions:
            return 50.0
        
        authority_sum = 0.0
        
        for mention in mentions:
            source = mention.get('source', 'unknown')
            influence_score = mention.get('influence_score', 0.5)
            
            # Base authority from source type
            base_authority = self.SOURCE_WEIGHTS.get(source.lower(), 0.5) * 100
            
            # Adjust by influence score
            authority_sum += base_authority * influence_score
        
        return authority_sum / len(mentions)
    
    def _get_score_category(self, score: float) -> ScoreCategory:
        """Determine category based on score"""
        if score >= 80:
            return ScoreCategory.EXCELLENT
        elif score >= 65:
            return ScoreCategory.GOOD
        elif score >= 45:
            return ScoreCategory.FAIR
        elif score >= 25:
            return ScoreCategory.POOR
        else:
            return ScoreCategory.CRITICAL
    
    def _determine_trend(self, entity_id: str, current_score: float) -> str:
        """Determine if reputation is trending up, down, or stable"""
        if entity_id not in self.scores_cache:
            return "stable"
        
        previous_score = self.scores_cache[entity_id].overall_score
        difference = current_score - previous_score
        
        if difference > 2:
            return "up"
        elif difference < -2:
            return "down"
        else:
            return "stable"
    
    def _get_historical_scores(self, entity_id: str) -> List[float]:
        """Get historical scores for an entity"""
        if entity_id in self.scores_cache:
            return self.scores_cache[entity_id].historical_scores.copy()
        return []
    
    def _create_default_score(self, entity_id: str, entity_name: str) -> ReputationScore:
        """Create a default score when no data available"""
        return ReputationScore(
            entity_id=entity_id,
            entity_name=entity_name,
            overall_score=50.0,
            category=ScoreCategory.FAIR,
            sentiment_score=50.0,
            volume_score=0.0,
            engagement_score=0.0,
            authority_score=50.0,
            trend_direction="stable",
            last_updated=datetime.now(),
            historical_scores=[50.0]
        )
    
    def get_score(self, entity_id: str) -> Optional[ReputationScore]:
        """Retrieve cached score for an entity"""
        return self.scores_cache.get(entity_id)
    
    def compare_entities(
        self,
        entity_ids: List[str]
    ) -> List[Dict]:
        """
        Compare reputation scores across multiple entities
        
        Args:
            entity_ids: List of entity IDs to compare
            
        Returns:
            List of entity comparisons with rankings
        """
        comparisons = []
        
        for entity_id in entity_ids:
            if entity_id in self.scores_cache:
                score = self.scores_cache[entity_id]
                comparisons.append({
                    "entity_id": entity_id,
                    "entity_name": score.entity_name,
                    "overall_score": score.overall_score,
                    "category": score.category.value,
                    "trend": score.trend_direction
                })
        
        # Sort by overall score (descending)
        comparisons.sort(key=lambda x: x['overall_score'], reverse=True)
        
        # Add ranking
        for i, comp in enumerate(comparisons, 1):
            comp['rank'] = i
        
        return comparisons
    
    def export_scores(self, entity_id: str, filepath: str):
        """Export score history to JSON file"""
        if entity_id not in self.scores_cache:
            return
        
        score = self.scores_cache[entity_id]
        data = score.to_dict()
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


# Example usage
if __name__ == "__main__":
    scorer = ReputationScorer()
    
    # Sample mentions data
    sample_mentions = [
        {
            "text": "Great product!",
            "sentiment": "positive",
            "confidence_score": 0.9,
            "source": "twitter",
            "timestamp": datetime.now().isoformat(),
            "likes": 50,
            "shares": 10,
            "comments": 5,
            "influence_score": 0.7
        },
        {
            "text": "Excellent service",
            "sentiment": "positive",
            "confidence_score": 0.85,
            "source": "news",
            "timestamp": datetime.now().isoformat(),
            "likes": 200,
            "shares": 50,
            "comments": 30,
            "influence_score": 0.9
        }
    ]
    
    # Calculate score
    score = scorer.calculate_score(
        entity_id="company_123",
        entity_name="Example Corp",
        mentions=sample_mentions,
        time_window_hours=24
    )
    
    print(f"\nReputation Score for {score.entity_name}")
    print(f"Overall Score: {score.overall_score:.2f}/100")
    print(f"Category: {score.category.value}")
    print(f"Trend: {score.trend_direction}")
    print(f"\nComponent Scores:")
    print(f"  Sentiment: {score.sentiment_score:.2f}")
    print(f"  Volume: {score.volume_score:.2f}")
    print(f"  Engagement: {score.engagement_score:.2f}")
    print(f"  Authority: {score.authority_score:.2f}")
