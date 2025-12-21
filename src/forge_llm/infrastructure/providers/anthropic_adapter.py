"""
AnthropicAdapter - Adapter for Anthropic API.

Implements ILLMProviderPort for Anthropic Claude models.
"""
from __future__ import annotations

from collections.abc import Generator
from typing import TYPE_CHECKING, Any

from forge_llm.domain import ProviderNotConfiguredError
from forge_llm.domain.entities import ProviderConfig
from forge_llm.infrastructure.logging import LogService

if TYPE_CHECKING:
    from anthropic import Anthropic


class AnthropicAdapter:
    """
    Adapter for Anthropic Claude API.

    Implements ILLMProviderPort interface for Anthropic.

    Usage:
        config = ProviderConfig(provider="anthropic", api_key="sk-...", model="claude-3-sonnet")
        adapter = AnthropicAdapter(config)

        response = adapter.send([{"role": "user", "content": "Hello"}])
    """

    SUPPORTED_MODELS = [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
    ]

    def __init__(self, config: ProviderConfig) -> None:
        self._config = config
        self._client: Anthropic | None = None
        self._logger = LogService(__name__)

    @property
    def name(self) -> str:
        """Provider name."""
        return "anthropic"

    @property
    def config(self) -> ProviderConfig:
        """Provider configuration."""
        return self._config

    def validate(self) -> bool:
        """
        Validate provider configuration.

        Returns:
            True if configuration is valid

        Raises:
            ProviderNotConfiguredError: If API key is missing
        """
        if not self._config.is_configured:
            raise ProviderNotConfiguredError("anthropic")
        return True

    def send(
        self,
        messages: list[dict[str, Any]],
        config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Send messages to Anthropic and get response.

        Args:
            messages: List of message dicts with role and content
            config: Optional request-specific configuration

        Returns:
            Response dict with content, role, model, and usage
        """
        self.validate()
        client = self._get_client()

        model = (config or {}).get("model") or self._config.model or "claude-3-sonnet-20240229"
        max_tokens = (config or {}).get("max_tokens", 4096)

        # Extract system messages and non-system messages
        system_prompt, filtered_messages = self._extract_system_prompt(messages)

        self._logger.debug(
            "Sending request to Anthropic",
            model=model,
            message_count=len(filtered_messages),
            has_system=system_prompt is not None,
        )

        # Build request params
        request_params: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": filtered_messages,
        }
        if system_prompt:
            request_params["system"] = system_prompt

        response = client.messages.create(**request_params)

        content = ""
        if response.content and hasattr(response.content[0], "text"):
            content = response.content[0].text
        return {
            "content": content,
            "role": response.role,
            "model": response.model,
            "provider": "anthropic",
            "usage": {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
            },
        }

    def stream(
        self,
        messages: list[dict[str, Any]],
        config: dict[str, Any] | None = None,
    ) -> Generator[dict[str, Any], None, None]:
        """
        Send messages and stream response chunks.

        Supports tool calls - when tools are provided in config, tool call
        events are yielded with 'tool_calls' key.

        Args:
            messages: List of message dicts
            config: Optional request-specific configuration (may include 'tools')

        Yields:
            Response chunks with partial content or tool_calls
        """
        self.validate()
        client = self._get_client()

        model = (config or {}).get("model") or self._config.model or "claude-3-sonnet-20240229"
        max_tokens = (config or {}).get("max_tokens", 4096)
        tools = (config or {}).get("tools")

        # Extract system messages and non-system messages
        system_prompt, filtered_messages = self._extract_system_prompt(messages)

        self._logger.debug(
            "Starting stream from Anthropic",
            model=model,
            message_count=len(filtered_messages),
            has_tools=tools is not None,
            has_system=system_prompt is not None,
        )

        # Build request params
        request_params: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": filtered_messages,
        }
        if system_prompt:
            request_params["system"] = system_prompt
        if tools:
            # Convert OpenAI format tools to Anthropic format
            request_params["tools"] = self._convert_tools_to_anthropic(tools)

        # Track tool use blocks being assembled
        current_tool_use: dict[str, Any] | None = None
        tool_calls: list[dict[str, Any]] = []

        with client.messages.stream(**request_params) as stream:
            for event in stream:
                # Handle text content
                if event.type == "content_block_delta":
                    if hasattr(event.delta, "text"):
                        yield {
                            "content": event.delta.text,
                            "provider": "anthropic",
                        }
                    # Handle tool use input JSON delta
                    elif hasattr(event.delta, "partial_json") and current_tool_use:
                        current_tool_use["input_json"] += event.delta.partial_json

                # Handle content block start (for tool_use)
                elif event.type == "content_block_start":
                    if (
                        hasattr(event.content_block, "type")
                        and event.content_block.type == "tool_use"
                    ):
                        current_tool_use = {
                            "id": event.content_block.id,
                            "name": event.content_block.name,
                            "input_json": "",
                        }

                # Handle content block stop
                elif event.type == "content_block_stop":
                    if current_tool_use:
                        # Convert to OpenAI-compatible format
                        tool_calls.append({
                            "id": current_tool_use["id"],
                            "type": "function",
                            "function": {
                                "name": current_tool_use["name"],
                                "arguments": current_tool_use["input_json"],
                            },
                        })
                        current_tool_use = None

                # Handle message stop
                elif event.type == "message_stop":
                    if tool_calls:
                        yield {
                            "content": "",
                            "provider": "anthropic",
                            "tool_calls": tool_calls,
                            "finish_reason": "tool_calls",
                        }
                    else:
                        yield {
                            "content": "",
                            "provider": "anthropic",
                            "finish_reason": "stop",
                        }

    def _extract_system_prompt(
        self, messages: list[dict[str, Any]]
    ) -> tuple[str | None, list[dict[str, Any]]]:
        """
        Extract system messages from message list.

        Anthropic API requires system prompt as separate parameter,
        not as a message with role "system".

        Args:
            messages: List of messages with roles

        Returns:
            Tuple of (system_prompt, filtered_messages)
        """
        system_parts = []
        filtered = []

        for msg in messages:
            if msg.get("role") == "system":
                content = msg.get("content", "")
                if content:
                    system_parts.append(content)
            else:
                filtered.append(msg)

        system_prompt = "\n\n".join(system_parts) if system_parts else None
        return system_prompt, filtered

    def _convert_tools_to_anthropic(
        self, tools: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Convert OpenAI format tools to Anthropic format."""
        anthropic_tools = []
        for tool in tools:
            if tool.get("type") == "function":
                func = tool.get("function", {})
                anthropic_tools.append({
                    "name": func.get("name", ""),
                    "description": func.get("description", ""),
                    "input_schema": func.get("parameters", {"type": "object"}),
                })
        return anthropic_tools

    def _get_client(self) -> Anthropic:
        """Get or create Anthropic client."""
        if self._client is None:
            from anthropic import Anthropic

            self._client = Anthropic(api_key=self._config.api_key)
        return self._client
