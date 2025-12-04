"""Unit tests for Vision/Image support."""

import pytest

from forge_llm.domain.exceptions import ValidationError
from forge_llm.domain.value_objects import ImageContent, Message
from forge_llm.providers.anthropic_provider import AnthropicProvider
from forge_llm.providers.openai_provider import OpenAIProvider


class TestImageContent:
    """Tests for ImageContent value object."""

    def test_image_with_url(self):
        """ImageContent with URL."""
        img = ImageContent(url="https://example.com/img.jpg")

        assert img.url == "https://example.com/img.jpg"
        assert img.base64_data is None
        assert img.is_url is True
        assert img.is_base64 is False

    def test_image_with_base64(self):
        """ImageContent with base64."""
        img = ImageContent(base64_data="abc123", media_type="image/png")

        assert img.url is None
        assert img.base64_data == "abc123"
        assert img.media_type == "image/png"
        assert img.is_url is False
        assert img.is_base64 is True

    def test_image_requires_url_or_base64(self):
        """ImageContent requires URL or base64."""
        with pytest.raises(ValidationError, match="URL ou base64_data obrigatorio"):
            ImageContent()

    def test_image_cannot_have_both_url_and_base64(self):
        """ImageContent cannot have both URL and base64."""
        with pytest.raises(ValidationError, match="Usar URL ou base64_data, nao ambos"):
            ImageContent(url="https://example.com/img.jpg", base64_data="abc123")

    def test_image_validates_media_type(self):
        """ImageContent validates media type."""
        with pytest.raises(ValidationError, match="Media type invalido"):
            ImageContent(base64_data="abc", media_type="invalid/type")

    def test_valid_media_types(self):
        """ImageContent accepts valid media types."""
        for media_type in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
            img = ImageContent(base64_data="abc", media_type=media_type)
            assert img.media_type == media_type

    def test_to_dict_url(self):
        """ImageContent.to_dict() for URL."""
        img = ImageContent(url="https://example.com/img.jpg")
        d = img.to_dict()

        assert d["type"] == "url"
        assert d["url"] == "https://example.com/img.jpg"

    def test_to_dict_base64(self):
        """ImageContent.to_dict() for base64."""
        img = ImageContent(base64_data="abc123", media_type="image/png")
        d = img.to_dict()

        assert d["type"] == "base64"
        assert d["data"] == "abc123"
        assert d["media_type"] == "image/png"

    def test_base64_size_limit(self):
        """ImageContent validates base64 size."""
        from forge_llm.domain.value_objects import MAX_BASE64_SIZE

        # Create data larger than limit
        large_data = "x" * (MAX_BASE64_SIZE + 1)

        with pytest.raises(ValidationError, match="excede limite"):
            ImageContent(base64_data=large_data)


class TestMessageWithImages:
    """Tests for Message with image content."""

    def test_message_simple_content(self):
        """Message with simple string content."""
        msg = Message(role="user", content="Hello")

        assert msg.has_images is False
        assert msg.images == []
        assert msg.text_content == "Hello"

    def test_message_with_image(self):
        """Message with image content."""
        img = ImageContent(url="https://example.com/img.jpg")
        msg = Message(role="user", content=["Describe this", img])

        assert msg.has_images is True
        assert len(msg.images) == 1
        assert msg.images[0] == img
        assert msg.text_content == "Describe this"

    def test_message_with_multiple_images(self):
        """Message with multiple images."""
        img1 = ImageContent(url="https://example.com/img1.jpg")
        img2 = ImageContent(url="https://example.com/img2.jpg")
        msg = Message(role="user", content=["Compare", img1, img2])

        assert msg.has_images is True
        assert len(msg.images) == 2
        assert msg.text_content == "Compare"


class TestOpenAIProviderImageFormatting:
    """Tests for OpenAI provider image formatting."""

    @pytest.fixture
    def provider(self):
        """Create OpenAI provider."""
        return OpenAIProvider(api_key="test-key")

    def test_format_image_url(self, provider):
        """OpenAI provider formats URL image correctly."""
        img = ImageContent(url="https://example.com/img.jpg")
        result = provider._format_image_for_openai(img)

        assert result["type"] == "input_image"
        assert result["image_url"] == "https://example.com/img.jpg"

    def test_format_image_base64(self, provider):
        """OpenAI provider formats base64 image correctly."""
        img = ImageContent(base64_data="abc123", media_type="image/png")
        result = provider._format_image_for_openai(img)

        assert result["type"] == "input_image"
        assert result["image_url"] == "data:image/png;base64,abc123"

    def test_convert_message_with_image(self, provider):
        """OpenAI provider converts message with image."""
        img = ImageContent(url="https://example.com/img.jpg")
        msg = Message(role="user", content=["Describe", img])

        result = provider._convert_messages_to_input([msg])

        assert len(result) == 1
        assert result[0]["role"] == "user"
        content = result[0]["content"]
        assert len(content) == 2
        assert content[0]["type"] == "input_text"
        assert content[0]["text"] == "Describe"
        assert content[1]["type"] == "input_image"


class TestAnthropicProviderImageFormatting:
    """Tests for Anthropic provider image formatting."""

    @pytest.fixture
    def provider(self):
        """Create Anthropic provider."""
        return AnthropicProvider(api_key="test-key")

    def test_format_image_url(self, provider):
        """Anthropic provider formats URL image correctly."""
        img = ImageContent(url="https://example.com/img.jpg")
        result = provider._format_image_for_anthropic(img)

        assert result["type"] == "image"
        assert result["source"]["type"] == "url"
        assert result["source"]["url"] == "https://example.com/img.jpg"

    def test_format_image_base64(self, provider):
        """Anthropic provider formats base64 image correctly."""
        img = ImageContent(base64_data="abc123", media_type="image/png")
        result = provider._format_image_for_anthropic(img)

        assert result["type"] == "image"
        assert result["source"]["type"] == "base64"
        assert result["source"]["media_type"] == "image/png"
        assert result["source"]["data"] == "abc123"

    def test_convert_message_with_image(self, provider):
        """Anthropic provider converts message with image."""
        img = ImageContent(url="https://example.com/img.jpg")
        msg = Message(role="user", content=["Describe", img])

        system, messages = provider._convert_messages([msg])

        assert system is None
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        content = messages[0]["content"]
        assert len(content) == 2
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "Describe"
        assert content[1]["type"] == "image"
