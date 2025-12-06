"""Response caching for LLM API calls."""

from __future__ import annotations

import asyncio
import hashlib
import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from forge_llm.domain.entities import ChatResponse


@dataclass(frozen=True)
class CacheKey:
    """Immutable cache key for LLM requests."""

    provider: str
    model: str
    messages_hash: str
    tools_hash: str | None
    response_format_hash: str | None

    @classmethod
    def create(
        cls,
        provider: str,
        model: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> CacheKey:
        """Create a cache key from request parameters."""
        messages_hash = cls._hash_data(messages)
        tools_hash = cls._hash_data(tools) if tools else None
        response_format_hash = cls._hash_data(response_format) if response_format else None

        return cls(
            provider=provider,
            model=model,
            messages_hash=messages_hash,
            tools_hash=tools_hash,
            response_format_hash=response_format_hash,
        )

    @staticmethod
    def _hash_data(data: Any) -> str:
        """Create a hash from JSON-serializable data."""
        json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(json_str.encode()).hexdigest()[:16]

    def to_string(self) -> str:
        """Convert to string representation for storage."""
        parts = [self.provider, self.model, self.messages_hash]
        if self.tools_hash:
            parts.append(f"t:{self.tools_hash}")
        if self.response_format_hash:
            parts.append(f"rf:{self.response_format_hash}")
        return "|".join(parts)


@dataclass
class CacheEntry:
    """A cached response with metadata."""

    response: ChatResponse
    created_at: float
    ttl_seconds: float
    hit_count: int = 0

    @property
    def is_expired(self) -> bool:
        """Check if the entry has expired."""
        return time.time() > self.created_at + self.ttl_seconds

    @property
    def age_seconds(self) -> float:
        """Get the age of the entry in seconds."""
        return time.time() - self.created_at


@dataclass
class CacheConfig:
    """Configuration for the response cache."""

    enabled: bool = True
    default_ttl_seconds: float = 300.0  # 5 minutes default
    max_entries: int = 1000
    # Don't cache responses with tool calls by default
    cache_tool_calls: bool = False
    # Only cache deterministic requests (temperature=0)
    require_deterministic: bool = True


@dataclass
class CacheStats:
    """Statistics about cache usage."""

    hits: int = 0
    misses: int = 0
    evictions: int = 0
    expirations: int = 0
    total_entries: int = 0

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0


class CachePort(ABC):
    """Abstract interface for response caching."""

    @abstractmethod
    async def get(self, key: CacheKey) -> ChatResponse | None:
        """Get a cached response if it exists and is not expired."""
        ...

    @abstractmethod
    async def set(
        self,
        key: CacheKey,
        response: ChatResponse,
        ttl_seconds: float | None = None,
    ) -> None:
        """Store a response in the cache."""
        ...

    @abstractmethod
    async def delete(self, key: CacheKey) -> bool:
        """Delete a cached entry."""
        ...

    @abstractmethod
    async def clear(self) -> None:
        """Clear all cached entries."""
        ...

    @abstractmethod
    def stats(self) -> CacheStats:
        """Get cache statistics."""
        ...


class InMemoryCache(CachePort):
    """In-memory LRU cache implementation."""

    def __init__(self, config: CacheConfig | None = None) -> None:
        self._config = config or CacheConfig()
        self._cache: dict[str, CacheEntry] = {}
        self._access_order: list[str] = []
        self._stats = CacheStats()
        self._lock = asyncio.Lock()

    async def get(self, key: CacheKey) -> ChatResponse | None:
        """Get a cached response."""
        if not self._config.enabled:
            return None

        key_str = key.to_string()

        async with self._lock:
            entry = self._cache.get(key_str)

            if entry is None:
                self._stats.misses += 1
                return None

            if entry.is_expired:
                # Remove expired entry
                del self._cache[key_str]
                if key_str in self._access_order:
                    self._access_order.remove(key_str)
                self._stats.expirations += 1
                self._stats.misses += 1
                self._stats.total_entries = len(self._cache)
                return None

            # Update access order for LRU
            if key_str in self._access_order:
                self._access_order.remove(key_str)
            self._access_order.append(key_str)

            entry.hit_count += 1
            self._stats.hits += 1
            return entry.response

    async def set(
        self,
        key: CacheKey,
        response: ChatResponse,
        ttl_seconds: float | None = None,
    ) -> None:
        """Store a response in the cache."""
        if not self._config.enabled:
            return

        # Don't cache responses with tool calls if configured
        if not self._config.cache_tool_calls and response.tool_calls:
            return

        key_str = key.to_string()
        ttl = ttl_seconds if ttl_seconds is not None else self._config.default_ttl_seconds

        async with self._lock:
            # Evict if at capacity
            while len(self._cache) >= self._config.max_entries:
                self._evict_oldest()

            self._cache[key_str] = CacheEntry(
                response=response,
                created_at=time.time(),
                ttl_seconds=ttl,
            )

            # Update access order
            if key_str in self._access_order:
                self._access_order.remove(key_str)
            self._access_order.append(key_str)

            self._stats.total_entries = len(self._cache)

    def _evict_oldest(self) -> None:
        """Evict the least recently used entry."""
        if self._access_order:
            oldest_key = self._access_order.pop(0)
            if oldest_key in self._cache:
                del self._cache[oldest_key]
                self._stats.evictions += 1

    async def delete(self, key: CacheKey) -> bool:
        """Delete a cached entry."""
        key_str = key.to_string()

        async with self._lock:
            if key_str in self._cache:
                del self._cache[key_str]
                if key_str in self._access_order:
                    self._access_order.remove(key_str)
                self._stats.total_entries = len(self._cache)
                return True
            return False

    async def clear(self) -> None:
        """Clear all cached entries."""
        async with self._lock:
            self._cache.clear()
            self._access_order.clear()
            self._stats.total_entries = 0

    def stats(self) -> CacheStats:
        """Get cache statistics."""
        return CacheStats(
            hits=self._stats.hits,
            misses=self._stats.misses,
            evictions=self._stats.evictions,
            expirations=self._stats.expirations,
            total_entries=len(self._cache),
        )


class NoOpCache(CachePort):
    """A cache implementation that does nothing (for disabled caching)."""

    def __init__(self) -> None:
        self._stats = CacheStats()

    async def get(self, key: CacheKey) -> ChatResponse | None:
        """Always returns None."""
        return None

    async def set(
        self,
        key: CacheKey,
        response: ChatResponse,
        ttl_seconds: float | None = None,
    ) -> None:
        """Does nothing."""
        pass

    async def delete(self, key: CacheKey) -> bool:
        """Always returns False."""
        return False

    async def clear(self) -> None:
        """Does nothing."""
        pass

    def stats(self) -> CacheStats:
        """Returns empty stats."""
        return self._stats
