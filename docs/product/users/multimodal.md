# Multimodal Support

ForgeLLM supports multimodal inputs including images and audio for compatible models.

## Overview

| Content Type | Providers | Formats | Models |
|--------------|-----------|---------|--------|
| Images | OpenAI, Anthropic | URL, Base64 | gpt-4o, gpt-4-turbo, claude-3-* |
| Audio | OpenAI only | WAV, MP3 (Base64) | gpt-4o-audio-preview |

## Images

### Creating Image Content

```python
from forge_llm import ImageContent

# From URL
img = ImageContent.from_url("https://example.com/image.png")

# From URL with detail level (OpenAI-specific)
img = ImageContent.from_url("https://example.com/image.png", detail="high")
# detail options: "auto" (default), "low", "high"

# From Base64
import base64
with open("photo.jpg", "rb") as f:
    data = base64.b64encode(f.read()).decode()

img = ImageContent.from_base64(
    data=data,
    media_type="image/jpeg",  # image/png, image/gif, image/webp
    detail="auto"
)
```

### Sending Images in Messages

```python
from forge_llm import ChatAgent, ChatMessage, ImageContent

agent = ChatAgent(provider="openai", model="gpt-4o")

# Single image
img = ImageContent.from_url("https://example.com/cat.jpg")
msg = ChatMessage.user_with_image("What animal is this?", img)
response = agent.chat([msg])
print(response.content)

# Multiple images
images = [
    ImageContent.from_url("https://example.com/before.png"),
    ImageContent.from_url("https://example.com/after.png"),
]
msg = ChatMessage.user_with_images("What changed between these images?", images)
response = agent.chat([msg])
```

### Checking for Images

```python
msg = ChatMessage.user_with_image("Describe this", img)
print(msg.has_images)  # True

msg = ChatMessage.user("Hello")
print(msg.has_images)  # False
```

### Provider Support

**OpenAI:**
- Converts to `image_url` format
- Supports `detail` parameter (auto, low, high)
- Base64 images sent as data URLs

**Anthropic:**
- Converts to native `image` format with `source` object
- Supports URL and Base64
- `detail` parameter is ignored

## Audio

### Creating Audio Content

```python
from forge_llm import AudioContent

# From file (recommended)
audio = AudioContent.from_file("recording.wav")  # or .mp3

# From Base64
import base64
with open("speech.mp3", "rb") as f:
    data = base64.b64encode(f.read()).decode()

audio = AudioContent.from_base64(data=data, format="mp3")
# format options: "wav", "mp3"
```

### Sending Audio in Messages

```python
from forge_llm import ChatAgent, ChatMessage, AudioContent

# Audio ONLY works with OpenAI gpt-4o-audio-preview
agent = ChatAgent(provider="openai", model="gpt-4o-audio-preview")

# Single audio
audio = AudioContent.from_file("question.wav")
msg = ChatMessage.user_with_audio("What is being said?", audio)
response = agent.chat([msg])

# Multiple audio files
audios = [
    AudioContent.from_file("speaker1.wav"),
    AudioContent.from_file("speaker2.wav"),
]
msg = ChatMessage.user_with_audios("Who sounds more confident?", audios)
response = agent.chat([msg])
```

### Checking for Audio

```python
msg = ChatMessage.user_with_audio("Transcribe", audio)
print(msg.has_audio)  # True

msg = ChatMessage.user("Hello")
print(msg.has_audio)  # False
```

### Provider Support

**OpenAI:**
- Converts to `input_audio` format
- Only supported by `gpt-4o-audio-preview` model

**Anthropic:**
- **NOT SUPPORTED** - Raises `UnsupportedFeatureError`

```python
from forge_llm import ChatAgent, ChatMessage, AudioContent
from forge_llm.domain import UnsupportedFeatureError

agent = ChatAgent(provider="anthropic", model="claude-3-sonnet")
audio = AudioContent.from_file("speech.wav")
msg = ChatMessage.user_with_audio("Transcribe", audio)

try:
    response = agent.chat([msg])
except UnsupportedFeatureError as e:
    print(f"{e.feature} is not supported by {e.provider}")
    # Output: Audio input is not supported by anthropic
```

## Combining Text, Images, and Audio

You can create messages with mixed content manually:

```python
from forge_llm import ChatMessage, TextContent, ImageContent, AudioContent

# Custom multimodal content
content = [
    TextContent(text="Here's an image and audio:"),
    ImageContent.from_url("https://example.com/chart.png"),
    AudioContent.from_file("explanation.wav"),
]

msg = ChatMessage(role="user", content=content)
```

## Serialization

Multimodal messages serialize to a canonical format:

```python
msg = ChatMessage.user_with_image("Describe", img)
data = msg.to_dict()

# data = {
#     "role": "user",
#     "content": [
#         {"type": "text", "text": "Describe"},
#         {"type": "image", "source_type": "url", "url": "https://..."}
#     ]
# }

# Reconstruct from dict
msg2 = ChatMessage.from_dict(data)
```

## Best Practices

1. **Use appropriate models**: Vision requires gpt-4o/gpt-4-turbo/claude-3-*, audio requires gpt-4o-audio-preview
2. **Handle unsupported features**: Wrap audio calls in try/except for provider portability
3. **Optimize image size**: Use `detail="low"` for thumbnails, `detail="high"` for detailed analysis
4. **Prefer from_file() for audio**: Automatically handles Base64 encoding and format detection
