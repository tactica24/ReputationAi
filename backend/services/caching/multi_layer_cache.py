"""
Multi-Layer Caching Strategy
Redis L1, In-Memory L2, and CDN L3 caching for optimal performance
"""

from typing import Any, Optional, Dict, Callable
from datetime import datetime, timedelta
from enum import Enum
import json
import hashlib
import asyncio
from functools import wraps
import pickle


class CacheLayer(Enum):
    """Cache layer types"""
    L1_MEMORY = "l1_memory"  # In-memory (fastest, 100ms TTL)
    L2_REDIS = "l2_redis"  # Redis (fast, 1-60min TTL)
    L3_CDN = "l3_cdn"  # CDN (static content, 24h TTL)


class CacheStrategy(Enum):
    """Caching strategies"""
    WRITE_THROUGH = "write_through"  # Write to cache and DB simultaneously
    WRITE_BEHIND = "write_behind"  # Write to cache first, DB asynchronously
    WRITE_AROUND = "write_around"  # Write to DB, invalidate cache
    READ_THROUGH = "read_through"  # Read from cache, populate if miss


class InMemoryCache:
    """L1 In-memory cache with LRU eviction"""
    
    def __init__(self, max_size: int = 10000, default_ttl: int = 100):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.access_times: Dict[str, datetime] = {}
        self.max_size = max_size
        self.default_ttl = default_ttl  # seconds
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key not in self.cache:
            return None
        
        # Check expiration
        entry = self.cache[key]
        if datetime.utcnow() > entry["expires_at"]:
            await self.delete(key)
            return None
        
        # Update access time for LRU
        self.access_times[key] = datetime.utcnow()
        
        return entry["value"]
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ):
        """Set value in cache"""
        # Evict if at capacity
        if len(self.cache) >= self.max_size:
            await self._evict_lru()
        
        ttl = ttl or self.default_ttl
        
        self.cache[key] = {
            "value": value,
            "expires_at": datetime.utcnow() + timedelta(seconds=ttl),
            "created_at": datetime.utcnow()
        }
        self.access_times[key] = datetime.utcnow()
    
    async def delete(self, key: str):
        """Delete value from cache"""
        if key in self.cache:
            del self.cache[key]
        if key in self.access_times:
            del self.access_times[key]
    
    async def _evict_lru(self):
        """Evict least recently used entry"""
        if not self.access_times:
            return
        
        # Find LRU key
        lru_key = min(self.access_times, key=self.access_times.get)
        await self.delete(lru_key)
    
    async def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.access_times.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "utilization": len(self.cache) / self.max_size * 100,
            "default_ttl": self.default_ttl
        }


class RedisCache:
    """L2 Redis cache for distributed caching"""
    
    def __init__(self, redis_client=None):
        # In production, this would be actual Redis client
        # For now, simulating with in-memory dict
        self.redis = redis_client or {}
        self.default_ttl = 3600  # 1 hour
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        if isinstance(self.redis, dict):
            # Simulation mode
            if key in self.redis:
                entry = self.redis[key]
                if datetime.utcnow() > entry["expires_at"]:
                    await self.delete(key)
                    return None
                return entry["value"]
            return None
        else:
            # Real Redis mode
            value = await self.redis.get(key)
            if value:
                return json.loads(value)
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None
    ):
        """Set value in Redis"""
        ttl = ttl or self.default_ttl
        
        if isinstance(self.redis, dict):
            # Simulation mode
            self.redis[key] = {
                "value": value,
                "expires_at": datetime.utcnow() + timedelta(seconds=ttl)
            }
        else:
            # Real Redis mode
            await self.redis.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
    
    async def delete(self, key: str):
        """Delete value from Redis"""
        if isinstance(self.redis, dict):
            if key in self.redis:
                del self.redis[key]
        else:
            await self.redis.delete(key)
    
    async def clear_pattern(self, pattern: str):
        """Clear keys matching pattern"""
        if isinstance(self.redis, dict):
            keys_to_delete = [
                k for k in self.redis.keys()
                if pattern in k
            ]
            for key in keys_to_delete:
                del self.redis[key]
        else:
            keys = await self.redis.keys(pattern)
            if keys:
                await self.redis.delete(*keys)


class MultiLayerCache:
    """Multi-layer cache orchestrator"""
    
    def __init__(self, redis_client=None):
        self.l1_cache = InMemoryCache(max_size=10000, default_ttl=100)
        self.l2_cache = RedisCache(redis_client)
        
        # Cache statistics
        self.stats = {
            "l1_hits": 0,
            "l1_misses": 0,
            "l2_hits": 0,
            "l2_misses": 0,
            "total_requests": 0
        }
    
    def _generate_cache_key(
        self,
        namespace: str,
        identifier: str,
        **params
    ) -> str:
        """Generate cache key from parameters"""
        # Sort params for consistent keys
        sorted_params = sorted(params.items())
        param_str = "_".join(f"{k}={v}" for k, v in sorted_params)
        
        key_components = [namespace, identifier, param_str]
        key = ":".join(filter(None, key_components))
        
        # Hash if too long
        if len(key) > 200:
            key_hash = hashlib.md5(key.encode()).hexdigest()
            key = f"{namespace}:{key_hash}"
        
        return key
    
    async def get(
        self,
        namespace: str,
        identifier: str,
        **params
    ) -> Optional[Any]:
        """
        Get value from multi-layer cache
        Checks L1 -> L2 in order
        """
        self.stats["total_requests"] += 1
        
        key = self._generate_cache_key(namespace, identifier, **params)
        
        # Try L1 (in-memory)
        value = await self.l1_cache.get(key)
        if value is not None:
            self.stats["l1_hits"] += 1
            return value
        
        self.stats["l1_misses"] += 1
        
        # Try L2 (Redis)
        value = await self.l2_cache.get(key)
        if value is not None:
            self.stats["l2_hits"] += 1
            
            # Populate L1 for faster subsequent access
            await self.l1_cache.set(key, value, ttl=100)
            return value
        
        self.stats["l2_misses"] += 1
        return None
    
    async def set(
        self,
        namespace: str,
        identifier: str,
        value: Any,
        l1_ttl: int = 100,
        l2_ttl: int = 3600,
        **params
    ):
        """Set value in multi-layer cache"""
        key = self._generate_cache_key(namespace, identifier, **params)
        
        # Write to both layers
        await self.l1_cache.set(key, value, ttl=l1_ttl)
        await self.l2_cache.set(key, value, ttl=l2_ttl)
    
    async def delete(
        self,
        namespace: str,
        identifier: str,
        **params
    ):
        """Delete value from all cache layers"""
        key = self._generate_cache_key(namespace, identifier, **params)
        
        await self.l1_cache.delete(key)
        await self.l2_cache.delete(key)
    
    async def invalidate_namespace(self, namespace: str):
        """Invalidate all keys in namespace"""
        # L1 doesn't support pattern matching easily, so clear all
        await self.l1_cache.clear()
        
        # L2 supports pattern matching
        await self.l2_cache.clear_pattern(f"{namespace}:*")
    
    def cache_decorator(
        self,
        namespace: str,
        l1_ttl: int = 100,
        l2_ttl: int = 3600,
        key_generator: Optional[Callable] = None
    ):
        """
        Decorator for caching function results
        
        Usage:
            @cache.cache_decorator("user_profile", l1_ttl=60, l2_ttl=1800)
            async def get_user_profile(user_id: int):
                return await db.query(...)
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                if key_generator:
                    identifier = key_generator(*args, **kwargs)
                else:
                    # Use function name and args
                    identifier = func.__name__
                
                # Try to get from cache
                cached_value = await self.get(
                    namespace,
                    identifier,
                    args=str(args),
                    kwargs=str(kwargs)
                )
                
                if cached_value is not None:
                    return cached_value
                
                # Execute function
                result = await func(*args, **kwargs)
                
                # Store in cache
                await self.set(
                    namespace,
                    identifier,
                    result,
                    l1_ttl=l1_ttl,
                    l2_ttl=l2_ttl,
                    args=str(args),
                    kwargs=str(kwargs)
                )
                
                return result
            
            return wrapper
        
        return decorator
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total = self.stats["total_requests"]
        
        if total == 0:
            return {
                "total_requests": 0,
                "l1_hit_rate": 0.0,
                "l2_hit_rate": 0.0,
                "overall_hit_rate": 0.0
            }
        
        l1_hit_rate = (self.stats["l1_hits"] / total) * 100
        l2_hit_rate = (self.stats["l2_hits"] / total) * 100
        overall_hit_rate = ((self.stats["l1_hits"] + self.stats["l2_hits"]) / total) * 100
        
        return {
            "total_requests": total,
            "l1_hits": self.stats["l1_hits"],
            "l1_misses": self.stats["l1_misses"],
            "l1_hit_rate": round(l1_hit_rate, 2),
            "l2_hits": self.stats["l2_hits"],
            "l2_misses": self.stats["l2_misses"],
            "l2_hit_rate": round(l2_hit_rate, 2),
            "overall_hit_rate": round(overall_hit_rate, 2),
            "l1_stats": self.l1_cache.get_stats()
        }


# Global cache instance
cache = MultiLayerCache()


# Example usage patterns
class CachePatterns:
    """Common caching patterns for the application"""
    
    @staticmethod
    @cache.cache_decorator("entity_profile", l1_ttl=300, l2_ttl=1800)
    async def get_entity_profile(entity_id: int):
        """Cache entity profile for 30 minutes"""
        # Would fetch from database
        pass
    
    @staticmethod
    @cache.cache_decorator("reputation_score", l1_ttl=60, l2_ttl=600)
    async def get_reputation_score(entity_id: int):
        """Cache reputation score for 10 minutes"""
        # Would calculate from mentions
        pass
    
    @staticmethod
    @cache.cache_decorator("analytics_dashboard", l1_ttl=300, l2_ttl=3600)
    async def get_dashboard_data(user_id: int, date_range: str):
        """Cache dashboard data for 1 hour"""
        # Would aggregate analytics
        pass
    
    @staticmethod
    async def invalidate_entity_cache(entity_id: int):
        """Invalidate all cache related to an entity"""
        await cache.delete("entity_profile", str(entity_id))
        await cache.delete("reputation_score", str(entity_id))
        await cache.invalidate_namespace(f"entity_{entity_id}")
