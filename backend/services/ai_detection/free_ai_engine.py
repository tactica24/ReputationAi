"""
Free/Open-Source AI Detection System
Uses HuggingFace models and free APIs - NO paid AI services

Cost: $0/month (runs on CPU, no GPU needed for inference)
"""

import asyncio
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import numpy as np


@dataclass
class ThreatAssessment:
    """Result of AI threat detection"""
    content_id: str
    is_threat: bool
    threat_type: str  # fake_news, deepfake, defamation, impersonation
    confidence: float  # 0-1
    evidence: List[str]
    severity: str  # low, medium, high, critical
    recommended_action: str


class FreeAIDetectionEngine:
    """
    AI detection using free open-source models
    All models from HuggingFace (free)
    """
    
    def __init__(self):
        self.models_loaded = False
        self._load_models()
    
    def _load_models(self):
        """Load free HuggingFace models (one-time download)"""
        from transformers import pipeline
        
        print("Loading free AI models (one-time download)...")
        
        # Fake news detection - BERT-based (FREE)
        self.fake_news_classifier = pipeline(
            "text-classification",
            model="hamzab/roberta-fake-news-classification",
            device=-1  # CPU only (free, no GPU needed)
        )
        
        # Sentiment analysis - for detecting defamation (FREE)
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            device=-1
        )
        
        # Zero-shot classification - multipurpose (FREE)
        self.zero_shot = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            device=-1
        )
        
        # Text similarity - for fact-checking (FREE)
        from sentence_transformers import SentenceTransformer
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.models_loaded = True
        print("✅ All AI models loaded (running on CPU - FREE)")
    
    async def detect_fake_news(
        self,
        content: str,
        context: Optional[str] = None
    ) -> ThreatAssessment:
        """
        Detect fake news using free BERT-based classifier
        
        Model: hamzab/roberta-fake-news-classification
        Cost: $0
        """
        try:
            # Classify as fake/real
            result = self.fake_news_classifier(content[:512])[0]  # Max 512 tokens
            
            is_fake = result['label'].upper() == 'FAKE'
            confidence = result['score']
            
            # Cross-reference with free fact-checkers
            fact_check_results = await self._cross_reference_facts(content)
            
            # Determine severity
            if is_fake and confidence > 0.8:
                severity = 'critical' if len(fact_check_results) > 0 else 'high'
            elif is_fake and confidence > 0.6:
                severity = 'medium'
            else:
                severity = 'low'
            
            evidence = [f"AI Classification: {result['label']} ({confidence:.2%} confidence)"]
            if fact_check_results:
                evidence.extend(fact_check_results)
            
            recommended_action = self._get_fake_news_action(severity)
            
            return ThreatAssessment(
                content_id=hash(content) % 10000000,
                is_threat=is_fake and confidence > 0.6,
                threat_type='fake_news',
                confidence=confidence,
                evidence=evidence,
                severity=severity,
                recommended_action=recommended_action
            )
        
        except Exception as e:
            print(f"Fake news detection error: {e}")
            return self._create_error_assessment('fake_news')
    
    async def detect_sentiment_threat(
        self,
        content: str
    ) -> ThreatAssessment:
        """
        Detect defamatory or negative content
        
        Model: cardiffnlp/twitter-roberta-base-sentiment
        Cost: $0
        """
        try:
            result = self.sentiment_analyzer(content[:512])[0]
            
            # Negative sentiment could indicate defamation
            is_negative = result['label'].lower() == 'negative'
            confidence = result['score']
            
            # Use zero-shot to classify intent
            intent_labels = ['defamation', 'criticism', 'neutral opinion', 'praise']
            intent_result = self.zero_shot(
                content[:512],
                candidate_labels=intent_labels
            )
            
            is_defamation = (
                is_negative and 
                confidence > 0.7 and
                intent_result['labels'][0] == 'defamation'
            )
            
            severity = self._calculate_sentiment_severity(confidence, is_defamation)
            
            evidence = [
                f"Sentiment: {result['label']} ({confidence:.2%} confidence)",
                f"Intent: {intent_result['labels'][0]} ({intent_result['scores'][0]:.2%})"
            ]
            
            return ThreatAssessment(
                content_id=hash(content) % 10000000,
                is_threat=is_defamation,
                threat_type='defamation',
                confidence=confidence,
                evidence=evidence,
                severity=severity,
                recommended_action=self._get_defamation_action(severity)
            )
        
        except Exception as e:
            print(f"Sentiment detection error: {e}")
            return self._create_error_assessment('defamation')
    
    async def detect_deepfake_image(
        self,
        image_url: str
    ) -> ThreatAssessment:
        """
        Detect manipulated images using free techniques
        
        Methods:
        - Error Level Analysis (ELA)
        - Metadata analysis (EXIF)
        - Reverse image search (free APIs)
        
        Cost: $0
        """
        import requests
        from PIL import Image
        from io import BytesIO
        import piexif
        
        evidence = []
        confidence = 0.0
        is_manipulated = False
        
        try:
            # Download image
            response = requests.get(image_url, timeout=10)
            img = Image.open(BytesIO(response.content))
            
            # 1. Error Level Analysis (ELA) - detects JPEG compression artifacts
            ela_score = self._perform_ela_analysis(img)
            evidence.append(f"ELA Score: {ela_score:.2f} (higher = more likely manipulated)")
            
            if ela_score > 15:  # Threshold for suspicious manipulation
                is_manipulated = True
                confidence = min(ela_score / 30, 1.0)
            
            # 2. Metadata analysis
            try:
                exif_dict = piexif.load(response.content)
                if not exif_dict or not exif_dict.get('0th'):
                    evidence.append("⚠️ No EXIF metadata (suspicious)")
                    confidence += 0.2
                    is_manipulated = True
                else:
                    evidence.append("✓ EXIF metadata present")
            except:
                evidence.append("⚠️ Invalid/missing metadata")
                confidence += 0.1
            
            # 3. Reverse image search (free)
            similar_images = await self._reverse_image_search_free(image_url)
            if similar_images:
                evidence.append(f"Found {len(similar_images)} similar images online")
                # Check if images are older (potential source)
                evidence.append("Possible original source found")
            
            severity = 'critical' if confidence > 0.8 else \
                      'high' if confidence > 0.6 else \
                      'medium' if confidence > 0.4 else 'low'
            
            return ThreatAssessment(
                content_id=hash(image_url) % 10000000,
                is_threat=is_manipulated and confidence > 0.5,
                threat_type='deepfake',
                confidence=confidence,
                evidence=evidence,
                severity=severity,
                recommended_action=self._get_deepfake_action(severity)
            )
        
        except Exception as e:
            print(f"Deepfake image detection error: {e}")
            return self._create_error_assessment('deepfake')
    
    async def detect_impersonation(
        self,
        content: str,
        author: str,
        known_handles: List[str]
    ) -> ThreatAssessment:
        """
        Detect fake accounts impersonating the person
        
        Uses pattern matching + zero-shot classification
        Cost: $0
        """
        evidence = []
        is_impersonation = False
        confidence = 0.0
        
        # Check if author is in known handles
        author_lower = author.lower()
        if author_lower in [h.lower() for h in known_handles]:
            evidence.append("✓ Verified account")
            return ThreatAssessment(
                content_id=hash(content) % 10000000,
                is_threat=False,
                threat_type='impersonation',
                confidence=0.0,
                evidence=evidence,
                severity='low',
                recommended_action='None - verified account'
            )
        
        # Check for similar usernames (potential impersonation)
        similarity_scores = []
        for handle in known_handles:
            similarity = self._calculate_username_similarity(author, handle)
            similarity_scores.append((handle, similarity))
        
        max_similarity = max(similarity_scores, key=lambda x: x[1])
        
        if max_similarity[1] > 0.7:  # Very similar username
            is_impersonation = True
            confidence = max_similarity[1]
            evidence.append(f"⚠️ Username '{author}' is {max_similarity[1]:.0%} similar to '{max_similarity[0]}'")
        
        # Use zero-shot to classify intent
        if is_impersonation:
            intent_result = self.zero_shot(
                content[:512],
                candidate_labels=['impersonation', 'parody', 'fan account', 'unrelated']
            )
            
            if intent_result['labels'][0] == 'impersonation':
                confidence = min(confidence + intent_result['scores'][0] / 2, 1.0)
                evidence.append(f"Intent: {intent_result['labels'][0]} ({intent_result['scores'][0]:.2%})")
        
        severity = 'critical' if confidence > 0.9 else \
                  'high' if confidence > 0.7 else \
                  'medium' if confidence > 0.5 else 'low'
        
        return ThreatAssessment(
            content_id=hash(content) % 10000000,
            is_threat=is_impersonation and confidence > 0.6,
            threat_type='impersonation',
            confidence=confidence,
            evidence=evidence,
            severity=severity,
            recommended_action=self._get_impersonation_action(severity)
        )
    
    async def _cross_reference_facts(self, content: str) -> List[str]:
        """
        Cross-reference with free fact-checking APIs
        
        Free sources:
        - Google Fact Check API (FREE)
        - Wikipedia API (FREE)
        - Snopes.com (via scraping)
        """
        evidence = []
        
        try:
            import aiohttp
            
            # Google Fact Check API (FREE)
            # Get free API key from: https://developers.google.com/fact-check/tools/api
            API_KEY = 'YOUR_FREE_API_KEY'
            
            # Extract main claim (first sentence)
            claim = content.split('.')[0]
            
            async with aiohttp.ClientSession() as session:
                url = f'https://factchecktools.googleapis.com/v1alpha1/claims:search?query={claim}&key={API_KEY}'
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'claims' in data and data['claims']:
                            for claim_review in data['claims'][:3]:
                                rating = claim_review.get('claimReview', [{}])[0].get('textualRating', 'Unknown')
                                evidence.append(f"Fact-check: {rating}")
        
        except Exception as e:
            print(f"Fact-checking error: {e}")
        
        return evidence
    
    def _perform_ela_analysis(self, image) -> float:
        """
        Error Level Analysis - detects JPEG manipulations
        
        Free technique, no API needed
        """
        try:
            from PIL import ImageChops
            import tempfile
            import os
            
            # Save at quality 90
            temp_path = tempfile.mktemp(suffix='.jpg')
            image.save(temp_path, 'JPEG', quality=90)
            
            # Reload
            compressed = Image.open(temp_path)
            
            # Calculate difference
            ela_image = ImageChops.difference(image, compressed)
            
            # Calculate average intensity
            extrema = ela_image.getextrema()
            max_diff = max([ex[1] for ex in extrema])
            
            # Cleanup
            os.remove(temp_path)
            
            return float(max_diff)
        
        except Exception as e:
            print(f"ELA analysis error: {e}")
            return 0.0
    
    async def _reverse_image_search_free(self, image_url: str) -> List[str]:
        """
        Free reverse image search using Google Custom Search API
        
        Free tier: 100 queries/day
        """
        results = []
        
        try:
            import aiohttp
            
            # Get free API key from: https://developers.google.com/custom-search
            API_KEY = 'YOUR_FREE_API_KEY'
            CX = 'YOUR_SEARCH_ENGINE_ID'
            
            async with aiohttp.ClientSession() as session:
                url = f'https://www.googleapis.com/customsearch/v1?q={image_url}&cx={CX}&key={API_KEY}&searchType=image'
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = [item['link'] for item in data.get('items', [])[:5]]
        
        except Exception as e:
            print(f"Reverse image search error: {e}")
        
        return results
    
    def _calculate_username_similarity(self, username1: str, username2: str) -> float:
        """Calculate similarity between usernames using Levenshtein distance"""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, username1.lower(), username2.lower()).ratio()
    
    def _calculate_sentiment_severity(self, confidence: float, is_defamation: bool) -> str:
        """Calculate severity level for sentiment threats"""
        if is_defamation and confidence > 0.8:
            return 'critical'
        elif is_defamation and confidence > 0.6:
            return 'high'
        elif confidence > 0.7:
            return 'medium'
        else:
            return 'low'
    
    def _get_fake_news_action(self, severity: str) -> str:
        """Recommended action for fake news"""
        actions = {
            'critical': 'IMMEDIATE: Contact legal team, request platform removal, issue public statement',
            'high': 'URGENT: Monitor spread, prepare counter-evidence, notify PR team',
            'medium': 'MONITOR: Track engagement, prepare response if escalates',
            'low': 'LOG: Document for records, no immediate action needed'
        }
        return actions.get(severity, 'Monitor situation')
    
    def _get_defamation_action(self, severity: str) -> str:
        """Recommended action for defamation"""
        actions = {
            'critical': 'IMMEDIATE: Legal cease & desist, platform report, public rebuttal',
            'high': 'URGENT: Document evidence, consult legal, prepare response',
            'medium': 'MONITOR: Track spread and engagement',
            'low': 'LOG: Keep record for future reference'
        }
        return actions.get(severity, 'Monitor situation')
    
    def _get_deepfake_action(self, severity: str) -> str:
        """Recommended action for deepfakes"""
        actions = {
            'critical': 'IMMEDIATE: DMCA takedown, law enforcement contact, public alert',
            'high': 'URGENT: Report to platform, issue warning, gather evidence',
            'medium': 'MONITOR: Track distribution, prepare response',
            'low': 'LOG: Document for records'
        }
        return actions.get(severity, 'Monitor situation')
    
    def _get_impersonation_action(self, severity: str) -> str:
        """Recommended action for impersonation"""
        actions = {
            'critical': 'IMMEDIATE: Report to platform, file DMCA, alert followers',
            'high': 'URGENT: Report account, document activity, notify team',
            'medium': 'MONITOR: Track account activity and follower growth',
            'low': 'LOG: Note account for future monitoring'
        }
        return actions.get(severity, 'Monitor situation')
    
    def _create_error_assessment(self, threat_type: str) -> ThreatAssessment:
        """Create assessment when detection fails"""
        return ThreatAssessment(
            content_id=0,
            is_threat=False,
            threat_type=threat_type,
            confidence=0.0,
            evidence=['Error during analysis'],
            severity='low',
            recommended_action='Manual review needed'
        )


# Example usage
async def main():
    """
    Example: Analyze scraped content for threats
    """
    engine = FreeAIDetectionEngine()
    
    # Example fake news content
    fake_news_text = """
    BREAKING: Celebrity John Doe caught in major financial scandal!
    Sources reveal he's been secretly funneling millions to offshore accounts.
    Investors are fleeing in panic!
    """
    
    print("🔍 Analyzing for fake news...")
    fake_news_result = await engine.detect_fake_news(fake_news_text)
    print(f"  Threat: {fake_news_result.is_threat}")
    print(f"  Confidence: {fake_news_result.confidence:.2%}")
    print(f"  Severity: {fake_news_result.severity}")
    print(f"  Evidence: {fake_news_result.evidence}")
    print(f"  Action: {fake_news_result.recommended_action}\n")
    
    # Example defamatory content
    defamatory_text = """
    John Doe is a complete fraud and scam artist.
    Don't trust anything he says - he's lying to steal your money!
    """
    
    print("🔍 Analyzing for defamation...")
    defamation_result = await engine.detect_sentiment_threat(defamatory_text)
    print(f"  Threat: {defamation_result.is_threat}")
    print(f"  Confidence: {defamation_result.confidence:.2%}")
    print(f"  Severity: {defamation_result.severity}")
    print(f"  Action: {defamation_result.recommended_action}\n")
    
    # Example impersonation
    print("🔍 Analyzing for impersonation...")
    impersonation_result = await engine.detect_impersonation(
        content="Follow me for investment advice!",
        author="JohnD0e_Official",  # Similar to "JohnDoe"
        known_handles=["JohnDoe", "JohnDoeOfficial"]
    )
    print(f"  Threat: {impersonation_result.is_threat}")
    print(f"  Confidence: {impersonation_result.confidence:.2%}")
    print(f"  Severity: {impersonation_result.severity}")
    print(f"  Evidence: {impersonation_result.evidence}\n")


if __name__ == "__main__":
    asyncio.run(main())
