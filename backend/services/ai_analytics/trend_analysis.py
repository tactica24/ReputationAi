"""
Trend Analysis Engine
Detects spikes in mentions and provides early-warning signals for PR crises or opportunities
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
from enum import Enum
import statistics


class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    OPPORTUNITY = "opportunity"


class TrendType(Enum):
    """Types of trends"""
    SPIKE = "spike"
    DROP = "drop"
    STEADY_GROWTH = "steady_growth"
    STEADY_DECLINE = "steady_decline"
    STABLE = "stable"
    VIRAL = "viral"


@dataclass
class TrendAlert:
    """Alert for detected trend"""
    alert_id: str
    entity_id: str
    entity_name: str
    alert_level: AlertLevel
    trend_type: TrendType
    message: str
    current_value: float
    baseline_value: float
    change_percentage: float
    confidence: float
    timestamp: datetime
    recommendations: List[str]
    affected_sources: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "alert_id": self.alert_id,
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "alert_level": self.alert_level.value,
            "trend_type": self.trend_type.value,
            "message": self.message,
            "current_value": self.current_value,
            "baseline_value": self.baseline_value,
            "change_percentage": round(self.change_percentage, 2),
            "confidence": round(self.confidence, 2),
            "timestamp": self.timestamp.isoformat(),
            "recommendations": self.recommendations,
            "affected_sources": self.affected_sources
        }


class TrendAnalyzer:
    """
    Analyze trends and detect anomalies in reputation data
    Provides early-warning system for PR crises and opportunities
    """
    
    def __init__(self, sensitivity: float = 2.0):
        """
        Initialize trend analyzer
        
        Args:
            sensitivity: Multiplier for spike detection (lower = more sensitive)
        """
        self.sensitivity = sensitivity
        self.baseline_data: Dict[str, List] = defaultdict(list)
        self.alerts_history: List[TrendAlert] = []
    
    def analyze_mention_volume(
        self,
        entity_id: str,
        entity_name: str,
        mentions: List[Dict],
        time_window_hours: int = 24
    ) -> Optional[TrendAlert]:
        """
        Analyze mention volume for unusual spikes or drops
        
        Args:
            entity_id: Entity identifier
            entity_name: Entity name
            mentions: List of mentions
            time_window_hours: Time window for analysis
            
        Returns:
            TrendAlert if anomaly detected, None otherwise
        """
        # Group mentions by hour
        hourly_counts = self._group_by_hour(mentions, time_window_hours)
        
        if len(hourly_counts) < 6:  # Need minimum data for trend analysis
            return None
        
        # Calculate statistics
        counts = list(hourly_counts.values())
        baseline = statistics.mean(counts[:-2])  # Exclude last 2 hours
        current = statistics.mean(counts[-2:])   # Last 2 hours average
        std_dev = statistics.stdev(counts) if len(counts) > 1 else 0
        
        # Detect spike
        if current > baseline * self.sensitivity:
            change_pct = ((current - baseline) / baseline) * 100
            
            # Determine severity
            if change_pct > 300:  # 300% increase
                alert_level = AlertLevel.CRITICAL
                trend_type = TrendType.VIRAL if change_pct > 500 else TrendType.SPIKE
            elif change_pct > 150:
                alert_level = AlertLevel.WARNING
                trend_type = TrendType.SPIKE
            else:
                alert_level = AlertLevel.INFO
                trend_type = TrendType.STEADY_GROWTH
            
            # Generate recommendations
            recommendations = self._generate_spike_recommendations(
                mentions[-10:], 
                change_pct, 
                alert_level
            )
            
            # Get affected sources
            affected_sources = list(set(m.get('source', 'unknown') for m in mentions[-20:]))
            
            alert = TrendAlert(
                alert_id=f"alert_{entity_id}_{datetime.now().timestamp()}",
                entity_id=entity_id,
                entity_name=entity_name,
                alert_level=alert_level,
                trend_type=trend_type,
                message=f"Mention volume spike detected: {change_pct:.1f}% increase",
                current_value=current,
                baseline_value=baseline,
                change_percentage=change_pct,
                confidence=min((change_pct / 100), 1.0),
                timestamp=datetime.now(),
                recommendations=recommendations,
                affected_sources=affected_sources
            )
            
            self.alerts_history.append(alert)
            return alert
        
        # Detect drop
        elif current < baseline * 0.5:  # 50% drop
            change_pct = ((baseline - current) / baseline) * 100
            
            alert = TrendAlert(
                alert_id=f"alert_{entity_id}_{datetime.now().timestamp()}",
                entity_id=entity_id,
                entity_name=entity_name,
                alert_level=AlertLevel.INFO,
                trend_type=TrendType.DROP,
                message=f"Mention volume drop detected: {change_pct:.1f}% decrease",
                current_value=current,
                baseline_value=baseline,
                change_percentage=-change_pct,
                confidence=0.7,
                timestamp=datetime.now(),
                recommendations=["Consider increasing content output", "Check if monitoring is working correctly"],
                affected_sources=list(set(m.get('source') for m in mentions))
            )
            
            self.alerts_history.append(alert)
            return alert
        
        return None
    
    def analyze_sentiment_shift(
        self,
        entity_id: str,
        entity_name: str,
        mentions: List[Dict],
        time_window_hours: int = 24
    ) -> Optional[TrendAlert]:
        """
        Detect sudden shifts in sentiment that could indicate PR crisis
        
        Args:
            entity_id: Entity identifier
            entity_name: Entity name
            mentions: List of mentions with sentiment
            time_window_hours: Time window for analysis
            
        Returns:
            TrendAlert if significant shift detected
        """
        if len(mentions) < 10:
            return None
        
        # Split into baseline and recent periods
        split_point = len(mentions) * 2 // 3
        baseline_mentions = mentions[:split_point]
        recent_mentions = mentions[split_point:]
        
        # Calculate sentiment scores
        baseline_sentiment = self._calculate_avg_sentiment(baseline_mentions)
        current_sentiment = self._calculate_avg_sentiment(recent_mentions)
        
        sentiment_change = current_sentiment - baseline_sentiment
        
        # Detect negative sentiment shift (PR crisis warning)
        if sentiment_change < -15:  # Significant negative shift
            alert_level = AlertLevel.CRITICAL if sentiment_change < -30 else AlertLevel.WARNING
            
            # Find most common negative keywords
            negative_mentions = [m for m in recent_mentions if m.get('sentiment') == 'negative']
            common_themes = self._extract_common_themes(negative_mentions)
            
            recommendations = [
                "🚨 Immediate response recommended",
                "Analyze root cause of negative sentiment",
                f"Focus on addressing: {', '.join(common_themes[:3])}",
                "Prepare official statement",
                "Monitor social media channels closely"
            ]
            
            alert = TrendAlert(
                alert_id=f"alert_{entity_id}_{datetime.now().timestamp()}",
                entity_id=entity_id,
                entity_name=entity_name,
                alert_level=alert_level,
                trend_type=TrendType.STEADY_DECLINE,
                message=f"⚠️ Negative sentiment shift detected: {abs(sentiment_change):.1f} point drop",
                current_value=current_sentiment,
                baseline_value=baseline_sentiment,
                change_percentage=sentiment_change,
                confidence=0.85,
                timestamp=datetime.now(),
                recommendations=recommendations,
                affected_sources=list(set(m.get('source') for m in negative_mentions))
            )
            
            self.alerts_history.append(alert)
            return alert
        
        # Detect positive sentiment shift (opportunity)
        elif sentiment_change > 15:
            recommendations = [
                "✨ Capitalize on positive momentum",
                "Share positive feedback on social media",
                "Engage with satisfied customers",
                "Consider PR campaign to amplify success"
            ]
            
            alert = TrendAlert(
                alert_id=f"alert_{entity_id}_{datetime.now().timestamp()}",
                entity_id=entity_id,
                entity_name=entity_name,
                alert_level=AlertLevel.OPPORTUNITY,
                trend_type=TrendType.STEADY_GROWTH,
                message=f"✅ Positive sentiment shift detected: {sentiment_change:.1f} point increase",
                current_value=current_sentiment,
                baseline_value=baseline_sentiment,
                change_percentage=sentiment_change,
                confidence=0.80,
                timestamp=datetime.now(),
                recommendations=recommendations,
                affected_sources=list(set(m.get('source') for m in recent_mentions))
            )
            
            self.alerts_history.append(alert)
            return alert
        
        return None
    
    def predict_crisis_probability(
        self,
        entity_id: str,
        mentions: List[Dict],
        reputation_score: float
    ) -> Dict:
        """
        Use ML to predict probability of PR crisis in next 24-48 hours
        
        Args:
            entity_id: Entity identifier
            mentions: Recent mentions
            reputation_score: Current reputation score
            
        Returns:
            Crisis prediction with probability and risk factors
        """
        # Risk factors analysis
        risk_factors = []
        risk_score = 0.0
        
        # Factor 1: Negative mention ratio
        negative_count = sum(1 for m in mentions if m.get('sentiment') == 'negative')
        negative_ratio = negative_count / len(mentions) if mentions else 0
        
        if negative_ratio > 0.5:
            risk_score += 0.3
            risk_factors.append("High negative mention ratio")
        
        # Factor 2: Declining reputation score
        if reputation_score < 40:
            risk_score += 0.25
            risk_factors.append("Low reputation score")
        
        # Factor 3: High volume spike with negative sentiment
        recent_negative = [m for m in mentions[-20:] if m.get('sentiment') == 'negative']
        if len(recent_negative) > 10:
            risk_score += 0.25
            risk_factors.append("Spike in negative mentions")
        
        # Factor 4: Authoritative source mentions
        news_mentions = [m for m in mentions if m.get('source') in ['news', 'press_release']]
        negative_news = [m for m in news_mentions if m.get('sentiment') == 'negative']
        if negative_news:
            risk_score += 0.2
            risk_factors.append("Negative news coverage")
        
        # Determine crisis probability
        crisis_probability = min(risk_score, 1.0)
        
        if crisis_probability > 0.7:
            level = "HIGH"
            action = "Immediate action required"
        elif crisis_probability > 0.4:
            level = "MEDIUM"
            action = "Monitor closely and prepare response"
        else:
            level = "LOW"
            action = "Continue normal monitoring"
        
        return {
            "entity_id": entity_id,
            "crisis_probability": crisis_probability,
            "risk_level": level,
            "risk_factors": risk_factors,
            "recommended_action": action,
            "prediction_confidence": 0.75,
            "timestamp": datetime.now().isoformat()
        }
    
    def _group_by_hour(self, mentions: List[Dict], hours: int) -> Dict[datetime, int]:
        """Group mentions by hour"""
        hourly_counts = defaultdict(int)
        cutoff = datetime.now() - timedelta(hours=hours)
        
        for mention in mentions:
            timestamp = datetime.fromisoformat(mention.get('timestamp', datetime.now().isoformat()))
            if timestamp >= cutoff:
                hour_key = timestamp.replace(minute=0, second=0, microsecond=0)
                hourly_counts[hour_key] += 1
        
        return dict(sorted(hourly_counts.items()))
    
    def _calculate_avg_sentiment(self, mentions: List[Dict]) -> float:
        """Calculate average sentiment score (0-100)"""
        if not mentions:
            return 50.0
        
        sentiment_values = []
        for mention in mentions:
            sentiment = mention.get('sentiment', 'neutral')
            if sentiment == 'positive':
                sentiment_values.append(100.0)
            elif sentiment == 'negative':
                sentiment_values.append(0.0)
            else:
                sentiment_values.append(50.0)
        
        return statistics.mean(sentiment_values)
    
    def _extract_common_themes(self, mentions: List[Dict]) -> List[str]:
        """Extract common themes/keywords from mentions"""
        all_keywords = []
        for mention in mentions:
            keywords = mention.get('keywords', [])
            all_keywords.extend(keywords)
        
        # Count frequency
        keyword_counts = defaultdict(int)
        for keyword in all_keywords:
            keyword_counts[keyword] += 1
        
        # Sort by frequency
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [kw for kw, count in sorted_keywords[:5]]
    
    def _generate_spike_recommendations(
        self,
        recent_mentions: List[Dict],
        change_pct: float,
        alert_level: AlertLevel
    ) -> List[str]:
        """Generate recommendations based on spike analysis"""
        recommendations = []
        
        # Analyze sentiment of spike
        positive_count = sum(1 for m in recent_mentions if m.get('sentiment') == 'positive')
        negative_count = sum(1 for m in recent_mentions if m.get('sentiment') == 'negative')
        
        if negative_count > positive_count:
            recommendations.extend([
                "🚨 Investigate cause of negative spike",
                "Prepare crisis communication plan",
                "Monitor sentiment continuously",
                "Consider issuing official response"
            ])
        else:
            recommendations.extend([
                "✨ Positive momentum detected",
                "Amplify positive content",
                "Engage with audience",
                "Share success stories"
            ])
        
        if alert_level == AlertLevel.CRITICAL:
            recommendations.insert(0, "⚠️ URGENT: Executive notification required")
        
        return recommendations
    
    def get_trending_topics(
        self,
        entity_id: str,
        mentions: List[Dict],
        top_n: int = 10
    ) -> List[Dict]:
        """
        Identify trending topics/keywords associated with entity
        
        Args:
            entity_id: Entity identifier
            mentions: List of mentions
            top_n: Number of top topics to return
            
        Returns:
            List of trending topics with metrics
        """
        keyword_data = defaultdict(lambda: {
            'count': 0,
            'positive': 0,
            'negative': 0,
            'neutral': 0
        })
        
        for mention in mentions:
            keywords = mention.get('keywords', [])
            sentiment = mention.get('sentiment', 'neutral')
            
            for keyword in keywords:
                keyword_data[keyword]['count'] += 1
                keyword_data[keyword][sentiment] += 1
        
        # Create trending topics list
        trending = []
        for keyword, data in keyword_data.items():
            sentiment_score = (data['positive'] - data['negative']) / data['count'] if data['count'] > 0 else 0
            
            trending.append({
                'keyword': keyword,
                'mention_count': data['count'],
                'sentiment_score': sentiment_score,
                'positive_count': data['positive'],
                'negative_count': data['negative'],
                'neutral_count': data['neutral']
            })
        
        # Sort by mention count
        trending.sort(key=lambda x: x['mention_count'], reverse=True)
        
        return trending[:top_n]


# Example usage
if __name__ == "__main__":
    analyzer = TrendAnalyzer(sensitivity=2.0)
    
    # Sample data with spike
    sample_mentions = [
        {"timestamp": (datetime.now() - timedelta(hours=i)).isoformat(),
         "sentiment": "negative" if i < 3 else "neutral",
         "source": "twitter",
         "keywords": ["issue", "problem"] if i < 3 else ["update"]}
        for i in range(24)
    ]
    
    # Analyze
    alert = analyzer.analyze_mention_volume(
        entity_id="test_123",
        entity_name="Test Company",
        mentions=sample_mentions,
        time_window_hours=24
    )
    
    if alert:
        print("\n🚨 ALERT DETECTED")
        print(f"Level: {alert.alert_level.value}")
        print(f"Type: {alert.trend_type.value}")
        print(f"Message: {alert.message}")
        print(f"Recommendations:")
        for rec in alert.recommendations:
            print(f"  - {rec}")
