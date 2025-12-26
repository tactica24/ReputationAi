"""
Sentiment Analysis Engine
Monitors social media, forums, blogs, news for mentions and classifies sentiment
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re


class SentimentType(Enum):
    """Sentiment classification types"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class SentimentResult:
    """Result from sentiment analysis"""
    text: str
    sentiment: SentimentType
    confidence_score: float
    timestamp: datetime
    source: str
    entity_mentioned: str
    keywords: List[str]
    influence_score: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "text": self.text,
            "sentiment": self.sentiment.value,
            "confidence_score": self.confidence_score,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "entity_mentioned": self.entity_mentioned,
            "keywords": self.keywords,
            "influence_score": self.influence_score
        }


class SentimentAnalyzer:
    """
    Advanced sentiment analysis engine with multi-model support
    Supports: Rule-based, ML-based, and Transformer-based models
    """
    
    def __init__(self, model_type: str = "transformer"):
        """
        Initialize sentiment analyzer
        
        Args:
            model_type: Type of model to use (transformer, ml, rule_based)
        """
        self.model_type = model_type
        self._load_model()
        
    def _load_model(self):
        """Load the sentiment analysis model"""
        # Placeholder for model loading
        # In production: Load pre-trained models (BERT, RoBERTa, etc.)
        self.model = None
        self.tokenizer = None
        
    def analyze(
        self, 
        text: str, 
        source: str, 
        entity: str
    ) -> SentimentResult:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            source: Source of the text (twitter, news, etc.)
            entity: Entity being mentioned
            
        Returns:
            SentimentResult with classification and confidence
        """
        # Clean and preprocess text
        cleaned_text = self._preprocess_text(text)
        
        # Extract keywords
        keywords = self._extract_keywords(cleaned_text, entity)
        
        # Perform sentiment analysis
        sentiment, confidence = self._classify_sentiment(cleaned_text)
        
        # Calculate influence score based on source
        influence = self._calculate_influence_score(source, len(text))
        
        return SentimentResult(
            text=text,
            sentiment=sentiment,
            confidence_score=confidence,
            timestamp=datetime.now(),
            source=source,
            entity_mentioned=entity,
            keywords=keywords,
            influence_score=influence
        )
    
    def batch_analyze(
        self, 
        texts: List[Tuple[str, str, str]]
    ) -> List[SentimentResult]:
        """
        Analyze multiple texts in batch for efficiency
        
        Args:
            texts: List of (text, source, entity) tuples
            
        Returns:
            List of SentimentResult objects
        """
        results = []
        for text, source, entity in texts:
            result = self.analyze(text, source, entity)
            results.append(result)
        return results
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove mentions and hashtags (keep the text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _extract_keywords(self, text: str, entity: str) -> List[str]:
        """Extract relevant keywords from text"""
        # Simple keyword extraction (in production: use TF-IDF, RAKE, etc.)
        words = text.lower().split()
        
        # Filter common words (simplified stopwords)
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        keywords = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Return top keywords
        return list(set(keywords))[:10]
    
    def _classify_sentiment(self, text: str) -> Tuple[SentimentType, float]:
        """
        Classify sentiment using the loaded model
        
        Returns:
            Tuple of (sentiment_type, confidence_score)
        """
        # Placeholder implementation
        # In production: Use actual ML model for classification
        
        # Simple rule-based sentiment for demo
        positive_words = {'good', 'great', 'excellent', 'amazing', 'wonderful', 
                         'fantastic', 'love', 'best', 'outstanding', 'perfect'}
        negative_words = {'bad', 'terrible', 'awful', 'horrible', 'worst', 
                         'hate', 'disgusting', 'poor', 'disappointing', 'scam'}
        
        text_lower = text.lower()
        words = set(text_lower.split())
        
        positive_count = len(words.intersection(positive_words))
        negative_count = len(words.intersection(negative_words))
        
        if positive_count > negative_count:
            confidence = min(0.6 + (positive_count * 0.1), 0.95)
            return SentimentType.POSITIVE, confidence
        elif negative_count > positive_count:
            confidence = min(0.6 + (negative_count * 0.1), 0.95)
            return SentimentType.NEGATIVE, confidence
        else:
            return SentimentType.NEUTRAL, 0.5
    
    def _calculate_influence_score(self, source: str, text_length: int) -> float:
        """
        Calculate influence score based on source and content
        
        Args:
            source: Source platform
            text_length: Length of the text
            
        Returns:
            Influence score (0.0 - 1.0)
        """
        # Base scores by source type
        source_weights = {
            'news': 0.9,
            'twitter': 0.7,
            'linkedin': 0.8,
            'facebook': 0.6,
            'instagram': 0.5,
            'reddit': 0.6,
            'blog': 0.7,
            'forum': 0.5,
            'review': 0.8
        }
        
        base_score = source_weights.get(source.lower(), 0.5)
        
        # Adjust based on text length (longer posts may be more influential)
        length_factor = min(text_length / 500, 1.0) * 0.2
        
        return min(base_score + length_factor, 1.0)


class SentimentAggregator:
    """Aggregate and analyze sentiment results over time"""
    
    def __init__(self):
        self.results_cache: List[SentimentResult] = []
    
    def add_result(self, result: SentimentResult):
        """Add a sentiment result to the cache"""
        self.results_cache.append(result)
    
    def get_average_sentiment(
        self, 
        entity: str, 
        time_window_hours: int = 24
    ) -> Dict:
        """
        Calculate average sentiment for an entity in a time window
        
        Args:
            entity: Entity to analyze
            time_window_hours: Hours to look back
            
        Returns:
            Dictionary with sentiment statistics
        """
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
        
        # Filter results
        relevant_results = [
            r for r in self.results_cache 
            if r.entity_mentioned == entity and r.timestamp >= cutoff_time
        ]
        
        if not relevant_results:
            return {
                "entity": entity,
                "count": 0,
                "average_sentiment": "neutral",
                "confidence": 0.0,
                "positive_percentage": 0.0,
                "negative_percentage": 0.0,
                "neutral_percentage": 0.0
            }
        
        # Calculate statistics
        total = len(relevant_results)
        positive = sum(1 for r in relevant_results if r.sentiment == SentimentType.POSITIVE)
        negative = sum(1 for r in relevant_results if r.sentiment == SentimentType.NEGATIVE)
        neutral = sum(1 for r in relevant_results if r.sentiment == SentimentType.NEUTRAL)
        
        avg_confidence = sum(r.confidence_score for r in relevant_results) / total
        
        # Determine overall sentiment
        if positive > negative and positive > neutral:
            overall = "positive"
        elif negative > positive and negative > neutral:
            overall = "negative"
        else:
            overall = "neutral"
        
        return {
            "entity": entity,
            "count": total,
            "average_sentiment": overall,
            "confidence": avg_confidence,
            "positive_percentage": (positive / total) * 100,
            "negative_percentage": (negative / total) * 100,
            "neutral_percentage": (neutral / total) * 100,
            "time_window_hours": time_window_hours
        }
    
    def detect_sentiment_spike(
        self, 
        entity: str, 
        threshold: float = 2.0
    ) -> Optional[Dict]:
        """
        Detect unusual spikes in sentiment mentions
        
        Args:
            entity: Entity to monitor
            threshold: Multiplier for detecting spikes
            
        Returns:
            Spike information if detected, None otherwise
        """
        from collections import defaultdict
        
        # Group by hour
        hourly_counts = defaultdict(int)
        
        for result in self.results_cache:
            if result.entity_mentioned == entity:
                hour_key = result.timestamp.replace(minute=0, second=0, microsecond=0)
                hourly_counts[hour_key] += 1
        
        if len(hourly_counts) < 2:
            return None
        
        # Calculate average and check for spikes
        counts = list(hourly_counts.values())
        average = sum(counts) / len(counts)
        max_count = max(counts)
        
        if max_count > average * threshold:
            return {
                "spike_detected": True,
                "max_mentions": max_count,
                "average_mentions": average,
                "spike_ratio": max_count / average,
                "entity": entity
            }
        
        return None


# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = SentimentAnalyzer(model_type="rule_based")
    
    # Test data
    test_texts = [
        ("This product is absolutely amazing! Best purchase ever.", "review", "Product X"),
        ("Terrible customer service, very disappointing experience.", "twitter", "Company Y"),
        ("The new update has some interesting features.", "blog", "Software Z")
    ]
    
    # Analyze sentiments
    results = analyzer.batch_analyze(test_texts)
    
    for result in results:
        print(f"\nText: {result.text[:50]}...")
        print(f"Sentiment: {result.sentiment.value}")
        print(f"Confidence: {result.confidence_score:.2f}")
        print(f"Keywords: {', '.join(result.keywords[:5])}")
