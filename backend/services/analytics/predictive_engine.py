"""
Predictive Analytics Engine
ML-powered forecasting, trend prediction, and crisis detection
"""

from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
import numpy as np
from collections import defaultdict
import asyncio


class TrendDirection(Enum):
    """Trend direction types"""
    UPWARD = "upward"
    DOWNWARD = "downward"
    STABLE = "stable"
    VOLATILE = "volatile"


class CrisisLevel(Enum):
    """Crisis severity levels"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PredictionResult:
    """Prediction result with confidence"""
    predicted_value: float
    confidence: float
    trend_direction: TrendDirection
    prediction_date: datetime
    contributing_factors: List[str]
    metadata: Dict[str, Any]


@dataclass
class CrisisAlert:
    """Crisis detection alert"""
    level: CrisisLevel
    confidence: float
    risk_score: float
    triggers: List[str]
    recommended_actions: List[str]
    time_to_impact: timedelta
    affected_entities: List[int]


class TimeSeriesAnalyzer:
    """Analyze time series data for patterns and trends"""
    
    def __init__(self):
        self.min_data_points = 7  # Minimum points for prediction
    
    async def analyze_trend(
        self,
        time_series: List[Tuple[datetime, float]]
    ) -> Tuple[TrendDirection, float]:
        """
        Analyze trend in time series data
        
        Returns:
            (trend_direction, trend_strength)
        """
        if len(time_series) < 2:
            return TrendDirection.STABLE, 0.0
        
        # Sort by date
        sorted_series = sorted(time_series, key=lambda x: x[0])
        values = [val for _, val in sorted_series]
        
        # Calculate linear regression slope
        n = len(values)
        x = np.arange(n)
        y = np.array(values)
        
        # Simple linear regression
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)
        
        if denominator == 0:
            return TrendDirection.STABLE, 0.0
        
        slope = numerator / denominator
        
        # Calculate R-squared for trend strength
        y_pred = slope * x + (y_mean - slope * x_mean)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y_mean) ** 2)
        
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # Calculate volatility
        volatility = np.std(values) / np.mean(values) if np.mean(values) != 0 else 0
        
        # Determine trend direction
        if volatility > 0.3:  # High volatility
            return TrendDirection.VOLATILE, abs(slope)
        elif slope > 0.1:
            return TrendDirection.UPWARD, r_squared
        elif slope < -0.1:
            return TrendDirection.DOWNWARD, r_squared
        else:
            return TrendDirection.STABLE, r_squared
    
    async def detect_anomalies(
        self,
        time_series: List[Tuple[datetime, float]],
        threshold_std: float = 2.0
    ) -> List[Tuple[datetime, float, str]]:
        """
        Detect anomalies using statistical methods
        
        Returns:
            List of (date, value, reason) tuples
        """
        if len(time_series) < self.min_data_points:
            return []
        
        values = [val for _, val in time_series]
        mean = np.mean(values)
        std = np.std(values)
        
        anomalies = []
        for date, value in time_series:
            z_score = abs(value - mean) / std if std != 0 else 0
            
            if z_score > threshold_std:
                reason = "spike" if value > mean else "drop"
                anomalies.append((date, value, reason))
        
        return anomalies
    
    async def forecast_next_period(
        self,
        time_series: List[Tuple[datetime, float]],
        periods: int = 7
    ) -> List[Tuple[datetime, float, float]]:
        """
        Forecast future values using exponential smoothing
        
        Returns:
            List of (date, predicted_value, confidence) tuples
        """
        if len(time_series) < self.min_data_points:
            return []
        
        # Sort by date
        sorted_series = sorted(time_series, key=lambda x: x[0])
        values = [val for _, val in sorted_series]
        
        # Exponential smoothing parameters
        alpha = 0.3  # Smoothing factor for level
        beta = 0.1   # Smoothing factor for trend
        
        # Initialize
        level = values[0]
        trend = values[1] - values[0] if len(values) > 1 else 0
        
        # Calculate smoothed values
        for value in values[1:]:
            last_level = level
            level = alpha * value + (1 - alpha) * (level + trend)
            trend = beta * (level - last_level) + (1 - beta) * trend
        
        # Forecast
        forecasts = []
        last_date = sorted_series[-1][0]
        
        for i in range(1, periods + 1):
            forecast_date = last_date + timedelta(days=i)
            forecast_value = level + i * trend
            
            # Confidence decreases with distance
            confidence = max(0.5, 1.0 - (i * 0.05))
            
            forecasts.append((forecast_date, forecast_value, confidence))
        
        return forecasts


class ReputationPredictor:
    """Predict future reputation scores"""
    
    def __init__(self):
        self.analyzer = TimeSeriesAnalyzer()
    
    async def predict_reputation_score(
        self,
        entity_id: int,
        historical_scores: List[Tuple[datetime, float]],
        days_ahead: int = 7
    ) -> PredictionResult:
        """
        Predict future reputation score
        
        Args:
            entity_id: Entity ID
            historical_scores: Historical reputation scores
            days_ahead: Days to predict ahead
        
        Returns:
            PredictionResult with predicted score
        """
        # Analyze current trend
        trend_direction, trend_strength = await self.analyzer.analyze_trend(
            historical_scores
        )
        
        # Forecast future scores
        forecasts = await self.analyzer.forecast_next_period(
            historical_scores,
            periods=days_ahead
        )
        
        if not forecasts:
            # Not enough data
            current_score = historical_scores[-1][1] if historical_scores else 50.0
            return PredictionResult(
                predicted_value=current_score,
                confidence=0.3,
                trend_direction=TrendDirection.STABLE,
                prediction_date=datetime.utcnow() + timedelta(days=days_ahead),
                contributing_factors=["Insufficient historical data"],
                metadata={"days_ahead": days_ahead}
            )
        
        # Get prediction for target date
        target_date, predicted_score, confidence = forecasts[-1]
        
        # Identify contributing factors
        contributing_factors = []
        
        if trend_direction == TrendDirection.UPWARD:
            contributing_factors.append("Positive sentiment trend")
        elif trend_direction == TrendDirection.DOWNWARD:
            contributing_factors.append("Negative sentiment trend")
        
        # Check for anomalies
        anomalies = await self.analyzer.detect_anomalies(historical_scores)
        if anomalies:
            contributing_factors.append(f"Recent anomalies detected ({len(anomalies)})")
        
        # Calculate volatility
        values = [val for _, val in historical_scores]
        volatility = np.std(values) / np.mean(values) if np.mean(values) != 0 else 0
        
        if volatility > 0.2:
            contributing_factors.append("High volatility in recent scores")
            confidence *= 0.8  # Reduce confidence for volatile data
        
        return PredictionResult(
            predicted_value=predicted_score,
            confidence=confidence,
            trend_direction=trend_direction,
            prediction_date=target_date,
            contributing_factors=contributing_factors,
            metadata={
                "days_ahead": days_ahead,
                "trend_strength": trend_strength,
                "volatility": volatility,
                "data_points": len(historical_scores)
            }
        )


class CrisisDetector:
    """Detect potential reputation crises before they escalate"""
    
    def __init__(self):
        self.analyzer = TimeSeriesAnalyzer()
    
    async def detect_crisis(
        self,
        entity_id: int,
        recent_mentions: List[Dict[str, Any]],
        historical_data: Dict[str, Any]
    ) -> CrisisAlert:
        """
        Detect potential crisis situation
        
        Args:
            entity_id: Entity ID
            recent_mentions: Recent mentions (last 24-48 hours)
            historical_data: Historical metrics for comparison
        
        Returns:
            CrisisAlert with risk assessment
        """
        triggers = []
        risk_score = 0.0
        
        # 1. Check mention volume spike
        recent_volume = len(recent_mentions)
        avg_daily_volume = historical_data.get("avg_daily_mentions", 10)
        
        volume_ratio = recent_volume / avg_daily_volume if avg_daily_volume > 0 else 1
        
        if volume_ratio > 3:
            triggers.append(f"Mention volume spike: {volume_ratio:.1f}x normal")
            risk_score += 25
        elif volume_ratio > 2:
            triggers.append(f"Elevated mention volume: {volume_ratio:.1f}x normal")
            risk_score += 15
        
        # 2. Check sentiment shift
        recent_negative_ratio = sum(
            1 for m in recent_mentions 
            if m.get("sentiment", "neutral") == "negative"
        ) / len(recent_mentions) if recent_mentions else 0
        
        avg_negative_ratio = historical_data.get("avg_negative_ratio", 0.2)
        
        if recent_negative_ratio > 0.6:
            triggers.append(f"High negative sentiment: {recent_negative_ratio:.1%}")
            risk_score += 30
        elif recent_negative_ratio > avg_negative_ratio * 2:
            triggers.append(f"Sentiment deterioration: {recent_negative_ratio:.1%}")
            risk_score += 20
        
        # 3. Check source diversity
        sources = set(m.get("source_name") for m in recent_mentions if m.get("source_name"))
        
        if len(sources) > 10:
            triggers.append(f"Widespread coverage: {len(sources)} sources")
            risk_score += 15
        
        # 4. Check for viral potential
        high_engagement = [
            m for m in recent_mentions 
            if m.get("engagement_score", 0) > historical_data.get("avg_engagement", 100) * 3
        ]
        
        if high_engagement:
            triggers.append(f"High engagement content: {len(high_engagement)} mentions")
            risk_score += 20
        
        # 5. Check trending topics
        negative_keywords = ["scandal", "controversy", "lawsuit", "fraud", "failure", "crisis"]
        contains_negative_keywords = any(
            any(keyword in m.get("content", "").lower() for keyword in negative_keywords)
            for m in recent_mentions
        )
        
        if contains_negative_keywords:
            triggers.append("Crisis keywords detected")
            risk_score += 15
        
        # Determine crisis level
        if risk_score >= 80:
            level = CrisisLevel.CRITICAL
            time_to_impact = timedelta(hours=2)
        elif risk_score >= 60:
            level = CrisisLevel.HIGH
            time_to_impact = timedelta(hours=6)
        elif risk_score >= 40:
            level = CrisisLevel.MEDIUM
            time_to_impact = timedelta(hours=12)
        elif risk_score >= 20:
            level = CrisisLevel.LOW
            time_to_impact = timedelta(days=1)
        else:
            level = CrisisLevel.NONE
            time_to_impact = timedelta(days=7)
        
        # Calculate confidence
        confidence = min(risk_score / 100, 0.95)
        
        # Recommended actions
        recommended_actions = self._get_recommended_actions(level, triggers)
        
        return CrisisAlert(
            level=level,
            confidence=confidence,
            risk_score=risk_score,
            triggers=triggers,
            recommended_actions=recommended_actions,
            time_to_impact=time_to_impact,
            affected_entities=[entity_id]
        )
    
    def _get_recommended_actions(
        self,
        level: CrisisLevel,
        triggers: List[str]
    ) -> List[str]:
        """Get recommended actions based on crisis level"""
        actions = []
        
        if level == CrisisLevel.CRITICAL:
            actions.extend([
                "Activate crisis response team immediately",
                "Prepare official statement",
                "Monitor social media in real-time",
                "Notify senior leadership",
                "Engage legal/PR advisors"
            ])
        elif level == CrisisLevel.HIGH:
            actions.extend([
                "Alert crisis management team",
                "Draft response statement",
                "Increase monitoring frequency",
                "Review communication strategy",
                "Prepare FAQ for stakeholders"
            ])
        elif level == CrisisLevel.MEDIUM:
            actions.extend([
                "Notify relevant stakeholders",
                "Monitor situation closely",
                "Prepare contingency plans",
                "Review recent communications"
            ])
        elif level == CrisisLevel.LOW:
            actions.extend([
                "Continue monitoring",
                "Document situation",
                "Review if patterns emerge"
            ])
        
        return actions


class TrendForecaster:
    """Forecast emerging trends and topics"""
    
    def __init__(self):
        self.min_mentions = 5
    
    async def identify_emerging_trends(
        self,
        recent_mentions: List[Dict[str, Any]],
        timeframe_hours: int = 24
    ) -> List[Dict[str, Any]]:
        """
        Identify emerging trends from mentions
        
        Returns:
            List of trending topics with growth metrics
        """
        # Extract topics/keywords
        topic_counts = defaultdict(int)
        topic_timestamps = defaultdict(list)
        
        for mention in recent_mentions:
            content = mention.get("content", "").lower()
            timestamp = mention.get("created_at", datetime.utcnow())
            
            # Simple keyword extraction (would use NLP in production)
            words = content.split()
            significant_words = [
                w for w in words 
                if len(w) > 4 and w.isalpha()
            ]
            
            for word in significant_words[:5]:  # Top 5 words per mention
                topic_counts[word] += 1
                topic_timestamps[word].append(timestamp)
        
        # Calculate trend metrics
        trends = []
        
        for topic, count in topic_counts.items():
            if count < self.min_mentions:
                continue
            
            timestamps = topic_timestamps[topic]
            
            # Calculate velocity (mentions per hour)
            time_range = (max(timestamps) - min(timestamps)).total_seconds() / 3600
            velocity = count / time_range if time_range > 0 else count
            
            # Calculate acceleration (is it speeding up?)
            if len(timestamps) > 2:
                # Compare first half vs second half
                mid_point = len(timestamps) // 2
                first_half = timestamps[:mid_point]
                second_half = timestamps[mid_point:]
                
                first_rate = len(first_half) / timeframe_hours * 2
                second_rate = len(second_half) / timeframe_hours * 2
                
                acceleration = (second_rate - first_rate) / first_rate if first_rate > 0 else 0
            else:
                acceleration = 0
            
            trends.append({
                "topic": topic,
                "mention_count": count,
                "velocity": velocity,
                "acceleration": acceleration,
                "is_growing": acceleration > 0.2,
                "confidence": min(count / 20, 1.0)  # More mentions = higher confidence
            })
        
        # Sort by velocity (trending now)
        trends.sort(key=lambda x: x["velocity"], reverse=True)
        
        return trends[:10]  # Top 10 trends


class PredictiveAnalyticsEngine:
    """Main predictive analytics orchestrator"""
    
    def __init__(self):
        self.reputation_predictor = ReputationPredictor()
        self.crisis_detector = CrisisDetector()
        self.trend_forecaster = TrendForecaster()
    
    async def generate_insights(
        self,
        entity_id: int,
        historical_data: Dict[str, Any],
        recent_mentions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive predictive insights
        
        Returns:
            Dictionary with predictions, crisis alerts, and trends
        """
        # Run predictions in parallel
        tasks = [
            self.reputation_predictor.predict_reputation_score(
                entity_id,
                historical_data.get("reputation_scores", []),
                days_ahead=7
            ),
            self.crisis_detector.detect_crisis(
                entity_id,
                recent_mentions,
                historical_data
            ),
            self.trend_forecaster.identify_emerging_trends(
                recent_mentions,
                timeframe_hours=24
            )
        ]
        
        reputation_prediction, crisis_alert, emerging_trends = await asyncio.gather(*tasks)
        
        return {
            "prediction": {
                "reputation_score": {
                    "predicted_value": reputation_prediction.predicted_value,
                    "confidence": reputation_prediction.confidence,
                    "trend": reputation_prediction.trend_direction.value,
                    "prediction_date": reputation_prediction.prediction_date.isoformat(),
                    "factors": reputation_prediction.contributing_factors
                }
            },
            "crisis_assessment": {
                "level": crisis_alert.level.value,
                "risk_score": crisis_alert.risk_score,
                "confidence": crisis_alert.confidence,
                "triggers": crisis_alert.triggers,
                "recommended_actions": crisis_alert.recommended_actions,
                "time_to_impact_hours": crisis_alert.time_to_impact.total_seconds() / 3600
            },
            "emerging_trends": emerging_trends,
            "generated_at": datetime.utcnow().isoformat()
        }


# Global instance
predictive_engine = PredictiveAnalyticsEngine()
