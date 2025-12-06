"""Tests for CLI module."""

import os
from argparse import Namespace
from unittest.mock import AsyncMock, patch

import pytest

from forge_llm.cli import (
    create_parser,
    get_api_key,
    main,
    run_models,
    run_providers,
)


class TestGetApiKey:
    """Tests for get_api_key function."""

    def test_returns_provided_api_key(self):
        """Should return the provided API key."""
        result = get_api_key("openai", "sk-test-key")
        assert result == "sk-test-key"

    def test_returns_env_var_for_openai(self):
        """Should return OPENAI_API_KEY from environment."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-env-key"}):
            result = get_api_key("openai", None)
            assert result == "sk-env-key"

    def test_returns_env_var_for_anthropic(self):
        """Should return ANTHROPIC_API_KEY from environment."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "sk-ant-key"}):
            result = get_api_key("anthropic", None)
            assert result == "sk-ant-key"

    def test_returns_env_var_for_openrouter(self):
        """Should return OPENROUTER_API_KEY from environment."""
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "sk-or-key"}):
            result = get_api_key("openrouter", None)
            assert result == "sk-or-key"

    def test_returns_none_when_no_key_available(self):
        """Should return None when no key is provided or in env."""
        with patch.dict(os.environ, {}, clear=True):
            # Clear specific keys
            for key in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OPENROUTER_API_KEY"]:
                os.environ.pop(key, None)
            result = get_api_key("openai", None)
            assert result is None

    def test_returns_generic_env_var_for_unknown_provider(self):
        """Should construct env var name for unknown providers."""
        with patch.dict(os.environ, {"CUSTOM_API_KEY": "custom-key"}):
            result = get_api_key("custom", None)
            assert result == "custom-key"


class TestCreateParser:
    """Tests for create_parser function."""

    def test_creates_parser_with_version(self):
        """Should create parser with version argument."""
        parser = create_parser()
        assert parser.prog == "forge-llm"

    def test_parser_has_chat_subcommand(self):
        """Should have chat subcommand."""
        parser = create_parser()
        args = parser.parse_args(["chat", "Hello"])
        assert args.command == "chat"
        assert args.message == "Hello"

    def test_parser_has_providers_subcommand(self):
        """Should have providers subcommand."""
        parser = create_parser()
        args = parser.parse_args(["providers"])
        assert args.command == "providers"

    def test_parser_has_models_subcommand(self):
        """Should have models subcommand."""
        parser = create_parser()
        args = parser.parse_args(["models", "openai"])
        assert args.command == "models"
        assert args.provider == "openai"

    def test_chat_default_provider_is_openai(self):
        """Chat should default to openai provider."""
        parser = create_parser()
        args = parser.parse_args(["chat", "Hello"])
        assert args.provider == "openai"

    def test_chat_accepts_provider_flag(self):
        """Chat should accept provider flag."""
        parser = create_parser()
        args = parser.parse_args(["chat", "-p", "anthropic", "Hello"])
        assert args.provider == "anthropic"

    def test_chat_accepts_model_flag(self):
        """Chat should accept model flag."""
        parser = create_parser()
        args = parser.parse_args(["chat", "-m", "gpt-4o", "Hello"])
        assert args.model == "gpt-4o"

    def test_chat_accepts_stream_flag(self):
        """Chat should accept stream flag."""
        parser = create_parser()
        args = parser.parse_args(["chat", "-s", "Hello"])
        assert args.stream is True

    def test_chat_accepts_verbose_flag(self):
        """Chat should accept verbose flag."""
        parser = create_parser()
        args = parser.parse_args(["chat", "-v", "Hello"])
        assert args.verbose is True


class TestRunProviders:
    """Tests for run_providers function."""

    @pytest.mark.asyncio
    async def test_lists_providers(self, capsys):
        """Should list available providers."""
        args = Namespace()
        result = await run_providers(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "Available providers:" in captured.out
        assert "openai" in captured.out
        assert "anthropic" in captured.out


class TestRunModels:
    """Tests for run_models function."""

    @pytest.mark.asyncio
    async def test_lists_openai_models(self, capsys):
        """Should list OpenAI models."""
        args = Namespace(provider="openai")
        result = await run_models(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "gpt-4o" in captured.out

    @pytest.mark.asyncio
    async def test_lists_anthropic_models(self, capsys):
        """Should list Anthropic models."""
        args = Namespace(provider="anthropic")
        result = await run_models(args)

        assert result == 0
        captured = capsys.readouterr()
        assert "claude-3-5-sonnet-latest" in captured.out

    @pytest.mark.asyncio
    async def test_returns_error_for_unknown_provider(self, capsys):
        """Should return error for unknown provider."""
        args = Namespace(provider="unknown")
        result = await run_models(args)

        assert result == 1
        captured = capsys.readouterr()
        assert "Unknown provider" in captured.out


class TestMain:
    """Tests for main function."""

    def test_shows_help_without_command(self, capsys):
        """Should show help when no command provided."""
        with patch("sys.argv", ["forge-llm"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "usage:" in captured.out.lower() or "forge-llm" in captured.out

    def test_runs_providers_command(self, capsys):
        """Should run providers command."""
        with patch("sys.argv", ["forge-llm", "providers"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "openai" in captured.out

    def test_runs_models_command(self, capsys):
        """Should run models command."""
        with patch("sys.argv", ["forge-llm", "models", "openai"]):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "gpt-4o" in captured.out

    def test_chat_fails_without_api_key(self, capsys):
        """Should fail chat without API key."""
        # Clear env vars
        env = {k: v for k, v in os.environ.items() if not k.endswith("_API_KEY")}
        with (
            patch.dict(os.environ, env, clear=True),
            patch("sys.argv", ["forge-llm", "chat", "Hello"]),
        ):
            result = main()

        assert result == 1
        captured = capsys.readouterr()
        assert "No API key" in captured.out or "Error" in captured.out

    def test_chat_with_mock_client(self, capsys):
        """Should run chat with mocked client."""
        mock_response = AsyncMock()
        mock_response.content = "Mocked response"
        mock_response.model = "gpt-4o-mini"
        mock_response.provider = "openai"
        mock_response.usage = None

        mock_client = AsyncMock()
        mock_client.chat = AsyncMock(return_value=mock_response)

        # Patch at the module where Client is imported, not where it's defined
        with (
            patch("sys.argv", ["forge-llm", "chat", "-k", "test-key", "Hello"]),
            patch("forge_llm.Client", return_value=mock_client),
        ):
            result = main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Mocked response" in captured.out
