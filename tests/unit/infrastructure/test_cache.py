"""Tests for the caching infrastructure."""

import asyncio
import time
from unittest.mock import MagicMock

import pytest

from forge_llm.domain.entities import ChatResponse
from forge_llm.domain.value_objects import TokenUsage
from forge_llm.infrastructure.cache import (
    CacheConfig,
    CacheEntry,
    CacheKey,
    CacheStats,
    InMemoryCache,
    NoOpCache,
)


class TestCacheKey:
    """Tests for CacheKey."""

    def test_create_basic_key(self) -> None:
        """Test creating a basic cache key."""
        messages = [{"role": "user", "content": "Hello"}]
        key = CacheKey.create(
            provider="openai",
            model="gpt-4",
            messages=messages,
        )

        assert key.provider == "openai"
        assert key.model == "gpt-4"
        assert key.messages_hash is not None
        assert key.tools_hash is None
        assert key.response_format_hash is None

    def test_create_key_with_tools(self) -> None:
        """Test creating a cache key with tools."""
        messages = [{"role": "user", "content": "Hello"}]
        tools = [{"name": "get_weather", "parameters": {}}]
        key = CacheKey.create(
            provider="openai",
            model="gpt-4",
            messages=messages,
            tools=tools,
        )

        assert key.tools_hash is not None

    def test_create_key_with_response_format(self) -> None:
        """Test creating a cache key with response format."""
        messages = [{"role": "user", "content": "Hello"}]
        response_format = {"type": "json_object"}
        key = CacheKey.create(
            provider="openai",
            model="gpt-4",
            messages=messages,
            response_format=response_format,
        )

        assert key.response_format_hash is not None

    def test_same_inputs_same_hash(self) -> None:
        """Test that identical inputs produce the same hash."""
        messages = [{"role": "user", "content": "Hello"}]
        key1 = CacheKey.create("openai", "gpt-4", messages)
        key2 = CacheKey.create("openai", "gpt-4", messages)

        assert key1.messages_hash == key2.messages_hash
        assert key1.to_string() == key2.to_string()

    def test_different_inputs_different_hash(self) -> None:
        """Test that different inputs produce different hashes."""
        messages1 = [{"role": "user", "content": "Hello"}]
        messages2 = [{"role": "user", "content": "Hi"}]
        key1 = CacheKey.create("openai", "gpt-4", messages1)
        key2 = CacheKey.create("openai", "gpt-4", messages2)

        assert key1.messages_hash != key2.messages_hash

    def test_to_string(self) -> None:
        """Test key serialization."""
        messages = [{"role": "user", "content": "Hello"}]
        key = CacheKey.create("openai", "gpt-4", messages)
        key_str = key.to_string()

        assert "openai" in key_str
        assert "gpt-4" in key_str
        assert "|" in key_str

    def test_frozen(self) -> None:
        """Test that CacheKey is immutable."""
        messages = [{"role": "user", "content": "Hello"}]
        key = CacheKey.create("openai", "gpt-4", messages)

        with pytest.raises(AttributeError):
            key.provider = "anthropic"  # type: ignore[misc]


class TestCacheEntry:
    """Tests for CacheEntry."""

    def test_not_expired(self) -> None:
        """Test that new entry is not expired."""
        response = MagicMock(spec=ChatResponse)
        entry = CacheEntry(
            response=response,
            created_at=time.time(),
            ttl_seconds=300.0,
        )

        assert not entry.is_expired

    def test_expired(self) -> None:
        """Test that old entry is expired."""
        response = MagicMock(spec=ChatResponse)
        entry = CacheEntry(
            response=response,
            created_at=time.time() - 400,  # 400 seconds ago
            ttl_seconds=300.0,  # 5 minutes TTL
        )

        assert entry.is_expired

    def test_age_seconds(self) -> None:
        """Test age calculation."""
        response = MagicMock(spec=ChatResponse)
        entry = CacheEntry(
            response=response,
            created_at=time.time() - 100,
            ttl_seconds=300.0,
        )

        assert 99 <= entry.age_seconds <= 101


class TestCacheStats:
    """Tests for CacheStats."""

    def test_hit_rate_no_requests(self) -> None:
        """Test hit rate with no requests."""
        stats = CacheStats()
        assert stats.hit_rate == 0.0

    def test_hit_rate_calculation(self) -> None:
        """Test hit rate calculation."""
        stats = CacheStats(hits=80, misses=20)
        assert stats.hit_rate == 0.8


class TestInMemoryCache:
    """Tests for InMemoryCache."""

    @pytest.fixture
    def cache(self) -> InMemoryCache:
        """Create a cache instance."""
        return InMemoryCache(CacheConfig(default_ttl_seconds=60.0))

    @pytest.fixture
    def sample_response(self) -> ChatResponse:
        """Create a sample response."""
        return ChatResponse(
            content="Hello!",
            model="gpt-4",
            provider="openai",
            finish_reason="stop",
            usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )

    @pytest.fixture
    def sample_key(self) -> CacheKey:
        """Create a sample cache key."""
        return CacheKey.create(
            provider="openai",
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}],
        )

    @pytest.mark.asyncio
    async def test_set_and_get(
        self, cache: InMemoryCache, sample_key: CacheKey, sample_response: ChatResponse
    ) -> None:
        """Test basic set and get."""
        await cache.set(sample_key, sample_response)
        result = await cache.get(sample_key)

        assert result is not None
        assert result.content == sample_response.content

    @pytest.mark.asyncio
    async def test_cache_miss(self, cache: InMemoryCache) -> None:
        """Test cache miss."""
        key = CacheKey.create("openai", "gpt-4", [{"role": "user", "content": "Missing"}])
        result = await cache.get(key)

        assert result is None
        assert cache.stats().misses == 1

    @pytest.mark.asyncio
    async def test_cache_hit_stats(
        self, cache: InMemoryCache, sample_key: CacheKey, sample_response: ChatResponse
    ) -> None:
        """Test hit statistics."""
        await cache.set(sample_key, sample_response)
        await cache.get(sample_key)

        stats = cache.stats()
        assert stats.hits == 1
        assert stats.total_entries == 1

    @pytest.mark.asyncio
    async def test_disabled_cache(self, sample_key: CacheKey, sample_response: ChatResponse) -> None:
        """Test disabled cache."""
        cache = InMemoryCache(CacheConfig(enabled=False))
        await cache.set(sample_key, sample_response)
        result = await cache.get(sample_key)

        assert result is None

    @pytest.mark.asyncio
    async def test_expiration(self, sample_key: CacheKey, sample_response: ChatResponse) -> None:
        """Test cache expiration."""
        cache = InMemoryCache(CacheConfig(default_ttl_seconds=0.1))  # 100ms TTL
        await cache.set(sample_key, sample_response)

        # Wait for expiration
        await asyncio.sleep(0.15)

        result = await cache.get(sample_key)
        assert result is None
        assert cache.stats().expirations == 1

    @pytest.mark.asyncio
    async def test_delete(
        self, cache: InMemoryCache, sample_key: CacheKey, sample_response: ChatResponse
    ) -> None:
        """Test deleting a cache entry."""
        await cache.set(sample_key, sample_response)
        deleted = await cache.delete(sample_key)

        assert deleted
        result = await cache.get(sample_key)
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, cache: InMemoryCache) -> None:
        """Test deleting a nonexistent entry."""
        key = CacheKey.create("openai", "gpt-4", [{"role": "user", "content": "Missing"}])
        deleted = await cache.delete(key)

        assert not deleted

    @pytest.mark.asyncio
    async def test_clear(
        self, cache: InMemoryCache, sample_key: CacheKey, sample_response: ChatResponse
    ) -> None:
        """Test clearing the cache."""
        await cache.set(sample_key, sample_response)
        await cache.clear()

        result = await cache.get(sample_key)
        assert result is None
        assert cache.stats().total_entries == 0

    @pytest.mark.asyncio
    async def test_lru_eviction(self, sample_response: ChatResponse) -> None:
        """Test LRU eviction when at capacity."""
        cache = InMemoryCache(CacheConfig(max_entries=2))

        key1 = CacheKey.create("openai", "gpt-4", [{"role": "user", "content": "1"}])
        key2 = CacheKey.create("openai", "gpt-4", [{"role": "user", "content": "2"}])
        key3 = CacheKey.create("openai", "gpt-4", [{"role": "user", "content": "3"}])

        await cache.set(key1, sample_response)
        await cache.set(key2, sample_response)
        await cache.set(key3, sample_response)  # Should evict key1

        assert await cache.get(key1) is None
        assert await cache.get(key2) is not None
        assert await cache.get(key3) is not None
        assert cache.stats().evictions == 1

    @pytest.mark.asyncio
    async def test_dont_cache_tool_calls(self, cache: InMemoryCache, sample_key: CacheKey) -> None:
        """Test that responses with tool calls are not cached by default."""
        response = ChatResponse(
            content=None,
            model="gpt-4",
            provider="openai",
            finish_reason="tool_calls",
            tool_calls=[MagicMock()],
            usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )

        await cache.set(sample_key, response)
        result = await cache.get(sample_key)

        assert result is None

    @pytest.mark.asyncio
    async def test_cache_tool_calls_when_enabled(self, sample_key: CacheKey) -> None:
        """Test caching tool call responses when enabled."""
        cache = InMemoryCache(CacheConfig(cache_tool_calls=True))
        response = ChatResponse(
            content=None,
            model="gpt-4",
            provider="openai",
            finish_reason="tool_calls",
            tool_calls=[MagicMock()],
            usage=TokenUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        )

        await cache.set(sample_key, response)
        result = await cache.get(sample_key)

        assert result is not None


class TestNoOpCache:
    """Tests for NoOpCache."""

    @pytest.fixture
    def cache(self) -> NoOpCache:
        """Create a no-op cache."""
        return NoOpCache()

    @pytest.fixture
    def sample_key(self) -> CacheKey:
        """Create a sample cache key."""
        return CacheKey.create("openai", "gpt-4", [{"role": "user", "content": "Hello"}])

    @pytest.mark.asyncio
    async def test_get_always_none(self, cache: NoOpCache, sample_key: CacheKey) -> None:
        """Test that get always returns None."""
        result = await cache.get(sample_key)
        assert result is None

    @pytest.mark.asyncio
    async def test_set_does_nothing(
        self, cache: NoOpCache, sample_key: CacheKey
    ) -> None:
        """Test that set does nothing."""
        response = MagicMock(spec=ChatResponse)
        await cache.set(sample_key, response)
        result = await cache.get(sample_key)
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_always_false(self, cache: NoOpCache, sample_key: CacheKey) -> None:
        """Test that delete always returns False."""
        result = await cache.delete(sample_key)
        assert not result

    def test_stats_empty(self, cache: NoOpCache) -> None:
        """Test that stats are always empty."""
        stats = cache.stats()
        assert stats.hits == 0
        assert stats.misses == 0
