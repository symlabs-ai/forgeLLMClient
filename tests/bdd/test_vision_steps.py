"""BDD steps for Vision/Image support."""

import asyncio

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from forge_llm.client import Client
from forge_llm.domain.exceptions import ValidationError
from forge_llm.domain.value_objects import ImageContent, Message

scenarios("../../specs/bdd/10_forge_core/vision.feature")


def run_async(coro):
    """Run async coroutine synchronously."""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)


@pytest.fixture
def vision_context():
    """Context for vision tests."""
    return {
        "client": None,
        "images": [],
        "response": None,
        "error": None,
        "last_message": None,
    }


@given('um cliente configurado com provider "mock"')
def client_configured(vision_context):
    """Configure client with mock provider."""
    vision_context["client"] = Client(provider="mock", api_key="test-key")


@given(parsers.parse('uma imagem com URL "{url}"'))
def image_with_url(vision_context, url):
    """Create image with URL."""
    image = ImageContent(url=url)
    vision_context["images"] = [image]


@given(parsers.parse('uma imagem em base64 com media type "{media_type}"'))
def image_with_base64(vision_context, media_type):
    """Create image with base64."""
    image = ImageContent(base64_data="dGVzdGltYWdlZGF0YQ==", media_type=media_type)
    vision_context["images"] = [image]


@given(parsers.parse('outra imagem com URL "{url}"'))
def another_image_with_url(vision_context, url):
    """Add another image with URL."""
    image = ImageContent(url=url)
    vision_context["images"].append(image)


@when(parsers.parse('eu envio a mensagem "{text}" com a imagem'))
def send_message_with_image(vision_context, text):
    """Send message with single image."""
    client = vision_context["client"]
    images = vision_context["images"]

    content = [text] + images
    message = Message(role="user", content=content)
    vision_context["last_message"] = message

    response = run_async(client.chat([message]))
    vision_context["response"] = response


@when(parsers.parse('eu envio a mensagem "{text}" com as imagens'))
def send_message_with_images(vision_context, text):
    """Send message with multiple images."""
    client = vision_context["client"]
    images = vision_context["images"]

    content = [text] + images
    message = Message(role="user", content=content)
    vision_context["last_message"] = message

    response = run_async(client.chat([message]))
    vision_context["response"] = response


@when("eu tento criar uma imagem sem URL e sem base64")
def create_image_without_url_or_base64(vision_context):
    """Try to create image without URL or base64."""
    try:
        ImageContent()
    except ValidationError as e:
        vision_context["error"] = e


@when("eu tento criar uma imagem com URL e base64")
def create_image_with_url_and_base64(vision_context):
    """Try to create image with both URL and base64."""
    try:
        ImageContent(url="https://example.com/img.jpg", base64_data="abc123")
    except ValidationError as e:
        vision_context["error"] = e


@then("a resposta deve conter conteudo")
def response_has_content(vision_context):
    """Check response has content."""
    response = vision_context["response"]
    assert response is not None
    assert response.content


@then("a mensagem enviada deve conter a imagem")
def message_contains_image(vision_context):
    """Check message contains image."""
    message = vision_context["last_message"]
    assert message.has_images
    assert len(message.images) == 1


@then("a mensagem enviada deve conter a imagem em base64")
def message_contains_base64_image(vision_context):
    """Check message contains base64 image."""
    message = vision_context["last_message"]
    assert message.has_images
    assert message.images[0].is_base64


@then(parsers.parse('deve lancar ValidationError com mensagem "{expected_msg}"'))
def should_raise_validation_error(vision_context, expected_msg):
    """Check ValidationError was raised with message."""
    error = vision_context["error"]
    assert error is not None
    assert isinstance(error, ValidationError)
    assert expected_msg in str(error)


@then(parsers.parse("a mensagem enviada deve conter {count:d} imagens"))
def message_contains_n_images(vision_context, count):
    """Check message contains N images."""
    message = vision_context["last_message"]
    assert message.has_images
    assert len(message.images) == count


@then(parsers.parse('a imagem deve ter media type "{expected_type}"'))
def image_has_media_type(vision_context, expected_type):
    """Check image has expected media type."""
    images = vision_context["images"]
    assert len(images) > 0
    assert images[0].media_type == expected_type
