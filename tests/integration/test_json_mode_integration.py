"""Integration tests for JSON mode / Structured Output."""

import json
import os

import pytest

from forge_llm import Client, ResponseFormat
from forge_llm.domain.value_objects import Message


def get_provider_and_key() -> tuple[str, str]:
    """Get first available provider and key."""
    if os.getenv("OPENAI_API_KEY"):
        return "openai", os.getenv("OPENAI_API_KEY", "")
    if os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic", os.getenv("ANTHROPIC_API_KEY", "")
    if os.getenv("OPENROUTER_API_KEY"):
        return "openrouter", os.getenv("OPENROUTER_API_KEY", "")
    return "", ""


has_any_key = pytest.mark.skipif(
    not (
        os.getenv("OPENAI_API_KEY")
        or os.getenv("ANTHROPIC_API_KEY")
        or os.getenv("OPENROUTER_API_KEY")
    ),
    reason="No API keys available",
)


@pytest.mark.integration
@pytest.mark.asyncio
class TestJSONModeIntegration:
    """Integration tests for JSON mode with real API calls."""

    @has_any_key
    async def test_json_object_mode(self):
        """Should return valid JSON with json_object mode."""
        provider, api_key = get_provider_and_key()
        if not provider:
            pytest.skip("No API keys available")

        client = Client(provider=provider, api_key=api_key)

        response = await client.chat(
            "List 3 colors as JSON with keys: colors (array of strings)",
            response_format=ResponseFormat.json(),
            max_tokens=100,
        )

        assert response.content is not None

        # Should be parseable JSON
        try:
            data = json.loads(response.content)
            assert isinstance(data, dict)
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {response.content}")

        await client.close()

    @has_any_key
    async def test_json_schema_mode(self):
        """Should return JSON matching schema."""
        provider, api_key = get_provider_and_key()
        if not provider:
            pytest.skip("No API keys available")

        client = Client(provider=provider, api_key=api_key)

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "capital": {"type": "string"},
            },
            "required": ["name", "capital"],
            "additionalProperties": False,
        }

        response = await client.chat(
            "Return info about Brazil",
            response_format=ResponseFormat.json_with_schema(schema, name="Country"),
            max_tokens=100,
        )

        assert response.content is not None

        # Should be parseable JSON matching schema
        try:
            data = json.loads(response.content)
            assert "name" in data or "capital" in data
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {response.content}")

        await client.close()

    @has_any_key
    async def test_text_mode_returns_normal_text(self):
        """Text mode should return normal text (default)."""
        provider, api_key = get_provider_and_key()
        if not provider:
            pytest.skip("No API keys available")

        client = Client(provider=provider, api_key=api_key)

        response = await client.chat(
            "Say hello",
            response_format=ResponseFormat.text(),
            max_tokens=50,
        )

        assert response.content is not None
        assert len(response.content) > 0

        await client.close()

    @has_any_key
    async def test_no_response_format_is_default_text(self):
        """No response_format should behave like text mode."""
        provider, api_key = get_provider_and_key()
        if not provider:
            pytest.skip("No API keys available")

        client = Client(provider=provider, api_key=api_key)

        response = await client.chat(
            "Say hello",
            max_tokens=50,
        )

        assert response.content is not None
        assert len(response.content) > 0

        await client.close()


@pytest.mark.integration
@pytest.mark.asyncio
class TestJSONModeWithPydantic:
    """Integration tests for JSON mode with Pydantic models."""

    @has_any_key
    async def test_pydantic_schema_mode(self):
        """Should work with Pydantic model schema."""
        from pydantic import BaseModel

        provider, api_key = get_provider_and_key()
        if not provider:
            pytest.skip("No API keys available")

        class Person(BaseModel):
            name: str
            occupation: str

        client = Client(provider=provider, api_key=api_key)

        response = await client.chat(
            "Create a fictional person",
            response_format=ResponseFormat.from_pydantic(Person),
            max_tokens=100,
        )

        assert response.content is not None

        # Should be valid JSON that can be parsed
        try:
            data = json.loads(response.content)
            assert isinstance(data, dict)
            # Note: actual validation against Pydantic schema is user's responsibility
        except json.JSONDecodeError:
            pytest.fail(f"Response is not valid JSON: {response.content}")

        await client.close()
