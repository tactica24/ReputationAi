"""
Advanced API Gateway with Rate Limiting, Authentication, and Request Routing
Enterprise-grade API management and security
"""

from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import time
from dataclasses import dataclass
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import asyncio


class RateLimitStrategy(Enum):
    """Rate limiting strategies"""
    FIXED_WINDOW = "fixed_window"
    SLIDING_WINDOW = "sliding_window"
    TOKEN_BUCKET = "token_bucket"
    LEAKY_BUCKET = "leaky_bucket"


class RateLimitTier(Enum):
    """Rate limit tiers for different user types"""
    FREE = "free"  # 100 requests/hour
    BASIC = "basic"  # 1,000 requests/hour
    PROFESSIONAL = "professional"  # 10,000 requests/hour
    ENTERPRISE = "enterprise"  # 100,000 requests/hour
    UNLIMITED = "unlimited"  # No limits


@dataclass
class RateLimitConfig:
    """Rate limit configuration"""
    requests_per_hour: int
    requests_per_minute: int
    burst_size: int
    strategy: RateLimitStrategy


# Tier configurations
RATE_LIMIT_CONFIGS = {
    RateLimitTier.FREE: RateLimitConfig(
        requests_per_hour=100,
        requests_per_minute=10,
        burst_size=20,
        strategy=RateLimitStrategy.SLIDING_WINDOW
    ),
    RateLimitTier.BASIC: RateLimitConfig(
        requests_per_hour=1000,
        requests_per_minute=100,
        burst_size=200,
        strategy=RateLimitStrategy.SLIDING_WINDOW
    ),
    RateLimitTier.PROFESSIONAL: RateLimitConfig(
        requests_per_hour=10000,
        requests_per_minute=500,
        burst_size=1000,
        strategy=RateLimitStrategy.TOKEN_BUCKET
    ),
    RateLimitTier.ENTERPRISE: RateLimitConfig(
        requests_per_hour=100000,
        requests_per_minute=5000,
        burst_size=10000,
        strategy=RateLimitStrategy.TOKEN_BUCKET
    )
}


class RateLimiter:
    """Advanced rate limiting implementation"""
    
    def __init__(self):
        # Store request history: {client_id: [timestamps]}
        self.request_history: Dict[str, list] = {}
        
        # Token bucket states: {client_id: {tokens, last_refill}}
        self.token_buckets: Dict[str, Dict[str, Any]] = {}
    
    async def check_rate_limit(
        self,
        client_id: str,
        tier: RateLimitTier
    ) -> tuple[bool, Dict[str, Any]]:
        """
        Check if request is within rate limits
        
        Returns:
            (is_allowed, limit_info)
        """
        if tier == RateLimitTier.UNLIMITED:
            return True, {"allowed": True, "tier": "unlimited"}
        
        config = RATE_LIMIT_CONFIGS[tier]
        
        if config.strategy == RateLimitStrategy.SLIDING_WINDOW:
            return await self._check_sliding_window(client_id, config)
        elif config.strategy == RateLimitStrategy.TOKEN_BUCKET:
            return await self._check_token_bucket(client_id, config)
        else:
            return await self._check_fixed_window(client_id, config)
    
    async def _check_sliding_window(
        self,
        client_id: str,
        config: RateLimitConfig
    ) -> tuple[bool, Dict[str, Any]]:
        """Sliding window rate limit check"""
        now = time.time()
        hour_ago = now - 3600
        minute_ago = now - 60
        
        # Initialize history if needed
        if client_id not in self.request_history:
            self.request_history[client_id] = []
        
        # Remove old timestamps
        self.request_history[client_id] = [
            ts for ts in self.request_history[client_id]
            if ts > hour_ago
        ]
        
        # Count requests
        requests_last_hour = len(self.request_history[client_id])
        requests_last_minute = len([
            ts for ts in self.request_history[client_id]
            if ts > minute_ago
        ])
        
        # Check limits
        if requests_last_minute >= config.requests_per_minute:
            return False, {
                "allowed": False,
                "reason": "Per-minute limit exceeded",
                "limit": config.requests_per_minute,
                "current": requests_last_minute,
                "reset_in_seconds": 60 - int(now - minute_ago)
            }
        
        if requests_last_hour >= config.requests_per_hour:
            return False, {
                "allowed": False,
                "reason": "Per-hour limit exceeded",
                "limit": config.requests_per_hour,
                "current": requests_last_hour,
                "reset_in_seconds": 3600 - int(now - hour_ago)
            }
        
        # Add current request
        self.request_history[client_id].append(now)
        
        return True, {
            "allowed": True,
            "remaining_hour": config.requests_per_hour - requests_last_hour - 1,
            "remaining_minute": config.requests_per_minute - requests_last_minute - 1
        }
    
    async def _check_token_bucket(
        self,
        client_id: str,
        config: RateLimitConfig
    ) -> tuple[bool, Dict[str, Any]]:
        """Token bucket rate limit check"""
        now = time.time()
        
        # Initialize bucket if needed
        if client_id not in self.token_buckets:
            self.token_buckets[client_id] = {
                "tokens": config.burst_size,
                "last_refill": now
            }
        
        bucket = self.token_buckets[client_id]
        
        # Refill tokens based on time elapsed
        time_elapsed = now - bucket["last_refill"]
        refill_rate = config.requests_per_hour / 3600  # tokens per second
        new_tokens = time_elapsed * refill_rate
        
        bucket["tokens"] = min(
            bucket["tokens"] + new_tokens,
            config.burst_size
        )
        bucket["last_refill"] = now
        
        # Check if token available
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True, {
                "allowed": True,
                "remaining_tokens": int(bucket["tokens"])
            }
        else:
            # Calculate wait time
            wait_time = (1 - bucket["tokens"]) / refill_rate
            return False, {
                "allowed": False,
                "reason": "Token bucket empty",
                "retry_after_seconds": int(wait_time) + 1
            }
    
    async def _check_fixed_window(
        self,
        client_id: str,
        config: RateLimitConfig
    ) -> tuple[bool, Dict[str, Any]]:
        """Fixed window rate limit check"""
        now = time.time()
        current_window = int(now / 3600)  # Hour window
        
        # Initialize history if needed
        if client_id not in self.request_history:
            self.request_history[client_id] = []
        
        # Filter to current window
        self.request_history[client_id] = [
            ts for ts in self.request_history[client_id]
            if int(ts / 3600) == current_window
        ]
        
        requests_current_window = len(self.request_history[client_id])
        
        if requests_current_window >= config.requests_per_hour:
            next_window = (current_window + 1) * 3600
            return False, {
                "allowed": False,
                "reason": "Fixed window limit exceeded",
                "limit": config.requests_per_hour,
                "reset_at": next_window
            }
        
        self.request_history[client_id].append(now)
        
        return True, {
            "allowed": True,
            "remaining": config.requests_per_hour - requests_current_window - 1
        }


class APIKeyManager:
    """Manage API keys and authentication"""
    
    def __init__(self):
        # In production, this would be in database
        self.api_keys: Dict[str, Dict[str, Any]] = {}
    
    def generate_api_key(
        self,
        user_id: int,
        tier: RateLimitTier,
        name: str = None
    ) -> str:
        """Generate new API key"""
        import secrets
        
        # Generate secure random key
        key = f"sk_{'test' if tier == RateLimitTier.FREE else 'live'}_{secrets.token_urlsafe(32)}"
        
        self.api_keys[key] = {
            "user_id": user_id,
            "tier": tier.value,
            "name": name,
            "created_at": datetime.utcnow(),
            "last_used": None,
            "is_active": True,
            "usage_count": 0
        }
        
        return key
    
    async def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return associated data"""
        if api_key not in self.api_keys:
            return None
        
        key_data = self.api_keys[api_key]
        
        if not key_data["is_active"]:
            return None
        
        # Update usage
        key_data["last_used"] = datetime.utcnow()
        key_data["usage_count"] += 1
        
        return key_data
    
    def revoke_api_key(self, api_key: str):
        """Revoke an API key"""
        if api_key in self.api_keys:
            self.api_keys[api_key]["is_active"] = False


class RequestRouter:
    """Route requests based on patterns and rules"""
    
    def __init__(self):
        self.routes: Dict[str, Dict[str, Any]] = {}
    
    def add_route(
        self,
        pattern: str,
        backend_url: str,
        methods: list = None,
        rate_limit_override: RateLimitTier = None
    ):
        """Add a route pattern"""
        self.routes[pattern] = {
            "backend_url": backend_url,
            "methods": methods or ["GET", "POST", "PUT", "DELETE"],
            "rate_limit_override": rate_limit_override
        }
    
    def match_route(self, path: str, method: str) -> Optional[Dict[str, Any]]:
        """Match request to route"""
        for pattern, route_config in self.routes.items():
            # Simple pattern matching (would use regex in production)
            if path.startswith(pattern) and method in route_config["methods"]:
                return route_config
        
        return None


class APIGateway:
    """Main API Gateway orchestrating all components"""
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.api_key_manager = APIKeyManager()
        self.request_router = RequestRouter()
        
        # Setup default routes
        self._setup_default_routes()
    
    def _setup_default_routes(self):
        """Setup default API routes"""
        self.request_router.add_route(
            "/api/v1/entities",
            "http://backend:8000/api/v1/entities",
            methods=["GET", "POST", "PUT", "DELETE"]
        )
        
        self.request_router.add_route(
            "/api/v1/mentions",
            "http://backend:8000/api/v1/mentions",
            methods=["GET", "POST"]
        )
        
        self.request_router.add_route(
            "/api/v1/analytics",
            "http://backend:8000/api/v1/analytics",
            methods=["GET"],
            rate_limit_override=RateLimitTier.PROFESSIONAL  # Higher limits for analytics
        )
    
    async def process_request(self, request: Request) -> JSONResponse:
        """
        Process incoming request through gateway
        
        1. Extract API key
        2. Validate authentication
        3. Check rate limits
        4. Route to backend
        5. Return response
        """
        # Extract API key from header
        api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization", "").replace("Bearer ", "")
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key required"
            )
        
        # Validate API key
        key_data = await self.api_key_manager.validate_api_key(api_key)
        
        if not key_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or revoked API key"
            )
        
        # Get rate limit tier
        tier = RateLimitTier(key_data["tier"])
        
        # Check rate limits
        client_id = f"user_{key_data['user_id']}"
        is_allowed, limit_info = await self.rate_limiter.check_rate_limit(client_id, tier)
        
        if not is_allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=limit_info.get("reason", "Rate limit exceeded"),
                headers={
                    "X-RateLimit-Limit": str(limit_info.get("limit", 0)),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(limit_info.get("reset_in_seconds", 0)),
                    "Retry-After": str(limit_info.get("retry_after_seconds", 60))
                }
            )
        
        # Match route
        path = request.url.path
        method = request.method
        
        route = self.request_router.match_route(path, method)
        
        if not route:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Route not found"
            )
        
        # In production, forward request to backend using httpx
        # For now, return success with metadata
        return JSONResponse(
            content={
                "status": "success",
                "message": "Request processed through API Gateway",
                "route": route["backend_url"],
                "user_id": key_data["user_id"],
                "rate_limit": limit_info
            },
            headers={
                "X-RateLimit-Remaining": str(limit_info.get("remaining_hour", 0)),
                "X-User-Tier": tier.value
            }
        )


# Global gateway instance
gateway = APIGateway()
