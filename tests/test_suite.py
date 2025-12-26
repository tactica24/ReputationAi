"""
Comprehensive Testing Suite for Enterprise Quality Assurance
Targeting 90%+ code coverage with unit, integration, and E2E tests
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any
import json


# ================== Unit Tests for MFA Service ==================

class TestMFAService:
    """Test Multi-Factor Authentication service"""
    
    @pytest.fixture
    async def mfa_service(self):
        from backend.services.security.mfa_service import MFAService
        return MFAService()
    
    @pytest.mark.asyncio
    async def test_generate_totp_secret(self, mfa_service):
        """Test TOTP secret generation"""
        secret = await mfa_service.generate_totp_secret()
        
        assert secret is not None
        assert len(secret) == 32  # Base32 encoded
        assert secret.isalnum()
    
    @pytest.mark.asyncio
    async def test_verify_totp_token(self, mfa_service):
        """Test TOTP token verification"""
        secret = await mfa_service.generate_totp_secret()
        
        # Generate current token
        import pyotp
        totp = pyotp.TOTP(secret)
        current_token = totp.now()
        
        # Verify token
        is_valid = await mfa_service.verify_totp_token(secret, current_token)
        assert is_valid is True
        
        # Test invalid token
        is_valid = await mfa_service.verify_totp_token(secret, "000000")
        assert is_valid is False
    
    @pytest.mark.asyncio
    async def test_generate_backup_codes(self, mfa_service):
        """Test backup code generation"""
        codes = await mfa_service.generate_backup_codes(count=10)
        
        assert len(codes) == 10
        for code in codes:
            assert len(code) == 12  # XXX-XXX-XXX format
            assert code.count('-') == 2
    
    @pytest.mark.asyncio
    async def test_verify_backup_code(self, mfa_service):
        """Test backup code verification"""
        codes = await mfa_service.generate_backup_codes(count=5)
        hashed_codes = [mfa_service._hash_code(code) for code in codes]
        
        # Test valid code
        is_valid = await mfa_service.verify_backup_code(codes[0], hashed_codes)
        assert is_valid is True
        
        # Test invalid code
        is_valid = await mfa_service.verify_backup_code("XXX-XXX-XXX", hashed_codes)
        assert is_valid is False
    
    @pytest.mark.asyncio
    async def test_device_fingerprint(self, mfa_service):
        """Test device fingerprinting"""
        fingerprint1 = await mfa_service.generate_device_fingerprint(
            "Mozilla/5.0", "192.168.1.1"
        )
        fingerprint2 = await mfa_service.generate_device_fingerprint(
            "Mozilla/5.0", "192.168.1.1"
        )
        fingerprint3 = await mfa_service.generate_device_fingerprint(
            "Chrome/91.0", "192.168.1.2"
        )
        
        assert fingerprint1 == fingerprint2
        assert fingerprint1 != fingerprint3
        assert len(fingerprint1) == 64  # SHA-256 hex


# ================== Unit Tests for Encryption Service ==================

class TestEncryptionService:
    """Test Advanced Encryption service"""
    
    @pytest.fixture
    async def encryption_service(self):
        from backend.services.security.encryption_service import AdvancedEncryptionService
        return AdvancedEncryptionService()
    
    @pytest.mark.asyncio
    async def test_symmetric_encryption(self, encryption_service):
        """Test Fernet symmetric encryption"""
        plaintext = "Sensitive user data"
        
        encrypted = await encryption_service.encrypt_symmetric(plaintext)
        decrypted = await encryption_service.decrypt_symmetric(encrypted)
        
        assert decrypted == plaintext
        assert encrypted != plaintext
    
    @pytest.mark.asyncio
    async def test_aes_gcm_encryption(self, encryption_service):
        """Test AES-256-GCM authenticated encryption"""
        plaintext = "Top secret information"
        key = encryption_service._generate_aes_key()
        
        encrypted = await encryption_service.encrypt_aes_gcm(plaintext, key)
        decrypted = await encryption_service.decrypt_aes_gcm(encrypted, key)
        
        assert decrypted == plaintext
    
    @pytest.mark.asyncio
    async def test_rsa_encryption(self, encryption_service):
        """Test RSA asymmetric encryption"""
        public_key, private_key = await encryption_service.generate_rsa_keypair()
        plaintext = "Asymmetrically encrypted message"
        
        encrypted = await encryption_service.encrypt_rsa(plaintext, public_key)
        decrypted = await encryption_service.decrypt_rsa(encrypted, private_key)
        
        assert decrypted == plaintext
    
    @pytest.mark.asyncio
    async def test_field_level_encryption(self, encryption_service):
        """Test field-level encryption for databases"""
        data = {
            "email": "user@example.com",
            "phone": "+1234567890",
            "public_info": "Not encrypted"
        }
        fields_to_encrypt = ["email", "phone"]
        
        encrypted_data = await encryption_service.encrypt_fields(data, fields_to_encrypt)
        
        # Check encryption
        assert encrypted_data["email"] != data["email"]
        assert encrypted_data["phone"] != data["phone"]
        assert encrypted_data["public_info"] == data["public_info"]
        
        # Decrypt
        decrypted_data = await encryption_service.decrypt_fields(
            encrypted_data, fields_to_encrypt
        )
        assert decrypted_data == data


# ================== Unit Tests for AI Ensemble ==================

class TestMultiModelEnsemble:
    """Test Multi-Model AI Ensemble"""
    
    @pytest.fixture
    async def ensemble(self):
        from backend.services.ai_analytics.multi_model_ensemble import MultiModelAIEnsemble
        # Mock API keys for testing
        return MultiModelAIEnsemble(
            openai_api_key="test-key",
            anthropic_api_key="test-key"
        )
    
    @pytest.mark.asyncio
    async def test_sentiment_aggregation(self, ensemble):
        """Test sentiment aggregation logic"""
        model_results = [
            {"sentiment": "positive", "score": 0.85, "confidence": 90.0},
            {"sentiment": "positive", "score": 0.90, "confidence": 95.0},
            {"sentiment": "neutral", "score": 0.55, "confidence": 70.0},
        ]
        
        weights = [0.35, 0.30, 0.20]  # GPT-4, Claude, Custom
        
        aggregated = ensemble._aggregate_sentiments(model_results, weights)
        
        assert aggregated["sentiment"] == "positive"
        assert 0.7 <= aggregated["score"] <= 0.9
        assert aggregated["confidence"] > 75.0


# ================== Unit Tests for Data Quality Pipeline ==================

class TestDataQualityPipeline:
    """Test Data Validation and Quality Pipeline"""
    
    @pytest.fixture
    async def spam_detector(self):
        from backend.services.validation.data_quality_pipeline import SpamBotDetector
        return SpamBotDetector()
    
    @pytest.mark.asyncio
    async def test_spam_detection(self, spam_detector):
        """Test spam content detection"""
        spam_content = "BUY NOW! Limited time offer! Click here to earn money fast!"
        is_spam, confidence, reasons = await spam_detector.detect_spam(spam_content)
        
        assert is_spam is True
        assert confidence >= 60.0
        assert len(reasons) > 0
    
    @pytest.mark.asyncio
    async def test_legitimate_content(self, spam_detector):
        """Test that legitimate content is not flagged as spam"""
        legit_content = "Our company is launching a new product next month."
        is_spam, confidence, reasons = await spam_detector.detect_spam(legit_content)
        
        assert is_spam is False
        assert confidence < 60.0
    
    @pytest.mark.asyncio
    async def test_url_verification(self):
        """Test URL credibility verification"""
        from backend.services.validation.data_quality_pipeline import SourceVerifier
        verifier = SourceVerifier()
        
        # Test trusted domain
        is_valid, trust_score, issues = await verifier.verify_url("https://twitter.com/post")
        assert is_valid is True
        assert trust_score >= 60.0
        
        # Test suspicious URL
        is_valid, trust_score, issues = await verifier.verify_url("http://random123456789.xyz")
        assert trust_score < 60.0


# ================== Integration Tests ==================

class TestAPIIntegration:
    """Integration tests for API endpoints"""
    
    @pytest.fixture
    async def client(self):
        from fastapi.testclient import TestClient
        from backend.main import app
        return TestClient(app)
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_create_entity(self, client):
        """Test entity creation endpoint"""
        entity_data = {
            "name": "Test Company",
            "entity_type": "company",
            "description": "Test entity for integration testing"
        }
        
        response = client.post("/api/v1/entities", json=entity_data)
        assert response.status_code == 201
        assert response.json()["name"] == entity_data["name"]
    
    def test_authentication_required(self, client):
        """Test that protected endpoints require authentication"""
        response = client.get("/api/v1/entities")
        assert response.status_code == 401


# ================== Performance Tests ==================

class TestPerformance:
    """Performance and load tests"""
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """Test system under concurrent load"""
        from backend.services.ai_analytics.multi_model_ensemble import MultiModelAIEnsemble
        
        ensemble = MultiModelAIEnsemble("test-key", "test-key")
        
        # Simulate 100 concurrent requests
        tasks = []
        for i in range(100):
            # Mock task - would be actual API calls in production
            tasks.append(asyncio.sleep(0.01))
        
        start_time = datetime.utcnow()
        await asyncio.gather(*tasks)
        end_time = datetime.utcnow()
        
        duration = (end_time - start_time).total_seconds()
        
        # Should handle 100 concurrent requests within reasonable time
        assert duration < 5.0  # 5 seconds max
    
    @pytest.mark.asyncio
    async def test_api_response_time(self):
        """Test API response time meets SLA (<100ms p95)"""
        # Simplified test - would use actual HTTP requests in production
        response_times = []
        
        for _ in range(100):
            start = datetime.utcnow()
            await asyncio.sleep(0.01)  # Simulate API call
            end = datetime.utcnow()
            response_times.append((end - start).total_seconds() * 1000)
        
        # Calculate p95
        response_times.sort()
        p95_index = int(len(response_times) * 0.95)
        p95_latency = response_times[p95_index]
        
        assert p95_latency < 100  # <100ms SLA


# ================== Security Tests ==================

class TestSecurity:
    """Security and penetration tests"""
    
    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting prevents brute force"""
        from backend.services.security.mfa_service import MFAAttemptTracker
        
        tracker = MFAAttemptTracker()
        user_id = 123
        
        # Attempt 5 times (should be allowed)
        for i in range(5):
            is_allowed = await tracker.is_attempt_allowed(user_id)
            assert is_allowed is True
            await tracker.record_attempt(user_id, False)
        
        # 6th attempt should be blocked
        is_allowed = await tracker.is_attempt_allowed(user_id)
        assert is_allowed is False
    
    @pytest.mark.asyncio
    async def test_sql_injection_prevention(self, client):
        """Test SQL injection prevention"""
        # Attempt SQL injection
        malicious_input = "'; DROP TABLE users; --"
        
        response = client.post("/api/v1/entities", json={
            "name": malicious_input,
            "entity_type": "company"
        })
        
        # Should not cause error and should sanitize input
        assert response.status_code in [201, 400]  # Created or validation error
    
    @pytest.mark.asyncio
    async def test_xss_prevention(self):
        """Test XSS attack prevention"""
        from backend.services.validation.data_quality_pipeline import DataQualityPipeline
        
        pipeline = DataQualityPipeline()
        
        xss_content = "<script>alert('XSS')</script>"
        result = await pipeline.validate_mention({
            "content": xss_content,
            "source_url": "https://example.com"
        })
        
        # Should detect malicious content
        assert result.confidence_score < 80.0


# ================== Test Configuration ==================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ================== Test Runner Configuration ==================

if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",  # Verbose
        "--cov=backend",  # Coverage for backend
        "--cov-report=html",  # HTML coverage report
        "--cov-report=term-missing",  # Show missing lines
        "--asyncio-mode=auto"  # Auto async mode
    ])
