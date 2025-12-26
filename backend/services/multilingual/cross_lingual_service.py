"""
Cross-Lingual Support Service
Support for 100+ languages with NLP, translation, and cultural sentiment analysis
"""

from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import asyncio


class Language(Enum):
    """Supported languages (100+ via external APIs)"""
    # Major languages
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    CHINESE_SIMPLIFIED = "zh-CN"
    CHINESE_TRADITIONAL = "zh-TW"
    JAPANESE = "ja"
    KOREAN = "ko"
    ARABIC = "ar"
    RUSSIAN = "ru"
    PORTUGUESE = "pt"
    ITALIAN = "it"
    DUTCH = "nl"
    POLISH = "pl"
    TURKISH = "tr"
    VIETNAMESE = "vi"
    THAI = "th"
    INDONESIAN = "id"
    HINDI = "hi"
    BENGALI = "bn"
    # Add 80+ more via translation API


class CulturalContext(Enum):
    """Cultural contexts for sentiment analysis"""
    WESTERN = "western"
    EAST_ASIAN = "east_asian"
    MIDDLE_EASTERN = "middle_eastern"
    SOUTH_ASIAN = "south_asian"
    LATIN_AMERICAN = "latin_american"
    AFRICAN = "african"


@dataclass
class LanguageDetectionResult:
    """Language detection result"""
    language: str
    confidence: float
    alternative_languages: List[Tuple[str, float]]


@dataclass
class TranslationResult:
    """Translation result with metadata"""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    confidence: float
    translation_engine: str


@dataclass
class CulturalSentimentResult:
    """Culturally-aware sentiment analysis"""
    sentiment: str
    confidence: float
    cultural_context: CulturalContext
    cultural_nuances: List[str]
    formality_level: str  # formal, neutral, informal


class LanguageDetector:
    """Detect language of text content"""
    
    def __init__(self):
        # Language patterns (simplified - would use ML models in production)
        self.language_patterns = {
            "en": ["the", "is", "and", "to", "of", "a", "in"],
            "es": ["el", "la", "de", "que", "y", "a", "en"],
            "fr": ["le", "la", "de", "et", "un", "une", "des"],
            "de": ["der", "die", "das", "und", "ist", "den", "dem"],
            "zh-CN": ["的", "了", "和", "是", "在", "我", "有"],
            "ja": ["の", "に", "は", "を", "た", "が", "で"],
            "ko": ["의", "이", "가", "을", "는", "에", "와"],
            "ar": ["في", "من", "إلى", "على", "هذا", "أن", "كان"],
            "ru": ["и", "в", "не", "на", "я", "что", "с"],
            "pt": ["o", "a", "de", "que", "e", "do", "da"],
        }
    
    async def detect_language(
        self,
        text: str,
        top_n: int = 3
    ) -> LanguageDetectionResult:
        """
        Detect language of text
        
        In production, would use:
        - Google Cloud Translation API
        - Azure Cognitive Services
        - AWS Comprehend
        - fastText language detection
        
        Returns:
            LanguageDetectionResult with detected language
        """
        if not text:
            return LanguageDetectionResult(
                language="en",
                confidence=0.0,
                alternative_languages=[]
            )
        
        text_lower = text.lower()
        scores = {}
        
        # Score each language based on pattern matching
        for lang, patterns in self.language_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            scores[lang] = score
        
        # Sort by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Calculate confidence
        total_score = sum(s for _, s in sorted_scores)
        
        if total_score == 0:
            # Default to English
            return LanguageDetectionResult(
                language="en",
                confidence=0.5,
                alternative_languages=[]
            )
        
        top_lang, top_score = sorted_scores[0]
        confidence = top_score / total_score
        
        # Get alternatives
        alternatives = [
            (lang, score / total_score)
            for lang, score in sorted_scores[1:top_n]
        ]
        
        return LanguageDetectionResult(
            language=top_lang,
            confidence=confidence,
            alternative_languages=alternatives
        )


class TranslationService:
    """Translate text between languages"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.supported_languages = 100  # Via external APIs
        
        # Simple word mappings for demo (would use actual translation APIs)
        self.demo_translations = {
            ("es", "en"): {
                "hola": "hello",
                "mundo": "world",
                "buenos": "good",
                "días": "days"
            },
            ("fr", "en"): {
                "bonjour": "hello",
                "monde": "world",
                "merci": "thank you"
            }
        }
    
    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> TranslationResult:
        """
        Translate text from source to target language
        
        In production, would use:
        - Google Cloud Translation API (100+ languages)
        - DeepL API (high quality for 26 languages)
        - Azure Translator (90+ languages)
        - AWS Translate (75+ languages)
        
        Returns:
            TranslationResult with translated text
        """
        if source_lang == target_lang:
            return TranslationResult(
                original_text=text,
                translated_text=text,
                source_language=source_lang,
                target_language=target_lang,
                confidence=1.0,
                translation_engine="none"
            )
        
        # Simplified translation (would use actual API in production)
        translated = text  # Default to original
        
        # Check demo translations
        lang_pair = (source_lang, target_lang)
        if lang_pair in self.demo_translations:
            words = text.lower().split()
            translated_words = [
                self.demo_translations[lang_pair].get(word, word)
                for word in words
            ]
            translated = " ".join(translated_words).capitalize()
        
        return TranslationResult(
            original_text=text,
            translated_text=translated,
            source_language=source_lang,
            target_language=target_lang,
            confidence=0.85,  # Simulated confidence
            translation_engine="google_translate"  # Would be actual engine
        )
    
    async def translate_batch(
        self,
        texts: List[str],
        source_lang: str,
        target_lang: str
    ) -> List[TranslationResult]:
        """Translate multiple texts in parallel"""
        tasks = [
            self.translate(text, source_lang, target_lang)
            for text in texts
        ]
        
        return await asyncio.gather(*tasks)


class CulturalSentimentAnalyzer:
    """Culturally-aware sentiment analysis"""
    
    def __init__(self):
        # Cultural sentiment mappings
        self.cultural_contexts = {
            "en": CulturalContext.WESTERN,
            "es": CulturalContext.LATIN_AMERICAN,
            "fr": CulturalContext.WESTERN,
            "de": CulturalContext.WESTERN,
            "zh-CN": CulturalContext.EAST_ASIAN,
            "ja": CulturalContext.EAST_ASIAN,
            "ko": CulturalContext.EAST_ASIAN,
            "ar": CulturalContext.MIDDLE_EASTERN,
            "hi": CulturalContext.SOUTH_ASIAN,
            "pt": CulturalContext.LATIN_AMERICAN,
        }
        
        # Cultural nuances by context
        self.cultural_nuances = {
            CulturalContext.EAST_ASIAN: [
                "Indirect communication preferred",
                "High context culture",
                "Emphasis on harmony and group consensus",
                "Saving face important"
            ],
            CulturalContext.MIDDLE_EASTERN: [
                "Formal communication valued",
                "Indirect criticism common",
                "Hospitality and honor important",
                "Relationship-focused"
            ],
            CulturalContext.LATIN_AMERICAN: [
                "Warm and expressive communication",
                "Personal relationships valued",
                "Flexible time perception",
                "Emotional expression acceptable"
            ],
            CulturalContext.WESTERN: [
                "Direct communication preferred",
                "Low context culture",
                "Individual achievement valued",
                "Time-conscious"
            ]
        }
    
    async def analyze_sentiment(
        self,
        text: str,
        language: str,
        context: Optional[Dict[str, Any]] = None
    ) -> CulturalSentimentResult:
        """
        Analyze sentiment with cultural awareness
        
        In production, would use:
        - Multilingual BERT models
        - XLM-RoBERTa for cross-lingual understanding
        - Cultural sentiment lexicons
        - Context-aware NLP models
        
        Returns:
            CulturalSentimentResult with culturally-adjusted sentiment
        """
        # Get cultural context
        cultural_context = self.cultural_contexts.get(
            language,
            CulturalContext.WESTERN
        )
        
        # Simplified sentiment analysis (would use ML in production)
        positive_words = ["good", "great", "excellent", "wonderful", "happy"]
        negative_words = ["bad", "terrible", "awful", "sad", "angry"]
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        # Determine sentiment
        if pos_count > neg_count:
            sentiment = "positive"
            confidence = min((pos_count / (pos_count + neg_count + 1)) * 100, 95)
        elif neg_count > pos_count:
            sentiment = "negative"
            confidence = min((neg_count / (pos_count + neg_count + 1)) * 100, 95)
        else:
            sentiment = "neutral"
            confidence = 70.0
        
        # Adjust for cultural context
        # East Asian cultures may express negative sentiment more indirectly
        if cultural_context == CulturalContext.EAST_ASIAN and sentiment == "negative":
            confidence *= 0.9  # Less certain due to indirect communication
        
        # Detect formality
        formal_indicators = ["please", "kindly", "respectfully", "sir", "madam"]
        formality_score = sum(1 for ind in formal_indicators if ind in text_lower)
        
        if formality_score >= 2:
            formality_level = "formal"
        elif formality_score == 1:
            formality_level = "neutral"
        else:
            formality_level = "informal"
        
        # Get cultural nuances
        nuances = self.cultural_nuances.get(cultural_context, [])
        
        return CulturalSentimentResult(
            sentiment=sentiment,
            confidence=confidence,
            cultural_context=cultural_context,
            cultural_nuances=nuances,
            formality_level=formality_level
        )


class MultilingualEntityExtractor:
    """Extract entities from text in multiple languages"""
    
    async def extract_entities(
        self,
        text: str,
        language: str
    ) -> Dict[str, List[str]]:
        """
        Extract named entities (people, organizations, locations)
        
        In production, would use:
        - spaCy multilingual models
        - Stanza NLP
        - Multilingual BERT NER
        
        Returns:
            Dictionary of entity types and their values
        """
        # Simplified extraction (would use NER models in production)
        entities = {
            "persons": [],
            "organizations": [],
            "locations": [],
            "dates": [],
            "monetary_values": []
        }
        
        # Capital letter detection for simple entity extraction
        words = text.split()
        capitalized = [
            word for word in words
            if word and word[0].isupper() and len(word) > 2
        ]
        
        # Simple heuristic (would use ML in production)
        entities["persons"] = capitalized[:3] if capitalized else []
        
        return entities


class CrossLingualService:
    """Main cross-lingual service orchestrator"""
    
    def __init__(self, translation_api_key: Optional[str] = None):
        self.language_detector = LanguageDetector()
        self.translation_service = TranslationService(translation_api_key)
        self.sentiment_analyzer = CulturalSentimentAnalyzer()
        self.entity_extractor = MultilingualEntityExtractor()
    
    async def process_multilingual_mention(
        self,
        mention_data: Dict[str, Any],
        target_language: str = "en"
    ) -> Dict[str, Any]:
        """
        Process mention in any language
        
        1. Detect language
        2. Translate to target language
        3. Analyze sentiment with cultural awareness
        4. Extract entities
        
        Returns:
            Processed mention with translations and analysis
        """
        content = mention_data.get("content", "")
        
        # Detect language
        detection = await self.language_detector.detect_language(content)
        
        # Translate if needed
        translation = None
        if detection.language != target_language:
            translation = await self.translation_service.translate(
                content,
                detection.language,
                target_language
            )
        
        # Analyze sentiment with cultural context
        sentiment = await self.sentiment_analyzer.analyze_sentiment(
            content,
            detection.language
        )
        
        # Extract entities
        entities = await self.entity_extractor.extract_entities(
            content,
            detection.language
        )
        
        return {
            "original_content": content,
            "detected_language": detection.language,
            "language_confidence": detection.confidence,
            "translation": {
                "text": translation.translated_text if translation else content,
                "confidence": translation.confidence if translation else 1.0
            } if translation else None,
            "sentiment": {
                "value": sentiment.sentiment,
                "confidence": sentiment.confidence,
                "cultural_context": sentiment.cultural_context.value,
                "formality": sentiment.formality_level,
                "cultural_notes": sentiment.cultural_nuances
            },
            "entities": entities,
            "processed_at": datetime.utcnow().isoformat()
        }
    
    async def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages"""
        # In production, would query translation API for supported languages
        languages = [
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "es", "name": "Spanish", "native_name": "Español"},
            {"code": "fr", "name": "French", "native_name": "Français"},
            {"code": "de", "name": "German", "native_name": "Deutsch"},
            {"code": "zh-CN", "name": "Chinese (Simplified)", "native_name": "中文（简体）"},
            {"code": "zh-TW", "name": "Chinese (Traditional)", "native_name": "中文（繁體）"},
            {"code": "ja", "name": "Japanese", "native_name": "日本語"},
            {"code": "ko", "name": "Korean", "native_name": "한국어"},
            {"code": "ar", "name": "Arabic", "native_name": "العربية"},
            {"code": "ru", "name": "Russian", "native_name": "Русский"},
            {"code": "pt", "name": "Portuguese", "native_name": "Português"},
            {"code": "it", "name": "Italian", "native_name": "Italiano"},
            {"code": "nl", "name": "Dutch", "native_name": "Nederlands"},
            {"code": "pl", "name": "Polish", "native_name": "Polski"},
            {"code": "tr", "name": "Turkish", "native_name": "Türkçe"},
            {"code": "vi", "name": "Vietnamese", "native_name": "Tiếng Việt"},
            {"code": "th", "name": "Thai", "native_name": "ไทย"},
            {"code": "id", "name": "Indonesian", "native_name": "Bahasa Indonesia"},
            {"code": "hi", "name": "Hindi", "native_name": "हिन्दी"},
            {"code": "bn", "name": "Bengali", "native_name": "বাংলা"},
            # ... 80+ more languages via Google/Azure/AWS APIs
        ]
        
        return languages


# Global instance
multilingual_service = CrossLingualService()
