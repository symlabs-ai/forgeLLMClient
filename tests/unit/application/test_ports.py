"""Testes para Ports (interfaces) - TDD RED phase."""

from abc import ABC

import pytest


class TestProviderPort:
    """Testes para ProviderPort interface."""

    def test_provider_port_is_abstract(self):
        """ProviderPort deve ser uma ABC."""
        from forge_llm.application.ports import ProviderPort

        assert issubclass(ProviderPort, ABC)

    def test_provider_port_has_chat_method(self):
        """ProviderPort deve ter metodo abstrato chat."""
        from forge_llm.application.ports import ProviderPort

        assert hasattr(ProviderPort, "chat")
        assert getattr(ProviderPort.chat, "__isabstractmethod__", False)

    def test_provider_port_has_chat_stream_method(self):
        """ProviderPort deve ter metodo abstrato chat_stream."""
        from forge_llm.application.ports import ProviderPort

        assert hasattr(ProviderPort, "chat_stream")
        assert getattr(ProviderPort.chat_stream, "__isabstractmethod__", False)

    def test_provider_port_has_provider_name_property(self):
        """ProviderPort deve ter property abstrata provider_name."""
        from forge_llm.application.ports import ProviderPort

        assert hasattr(ProviderPort, "provider_name")

    def test_provider_port_has_supports_streaming_property(self):
        """ProviderPort deve ter property abstrata supports_streaming."""
        from forge_llm.application.ports import ProviderPort

        assert hasattr(ProviderPort, "supports_streaming")

    def test_provider_port_has_supports_tool_calling_property(self):
        """ProviderPort deve ter property abstrata supports_tool_calling."""
        from forge_llm.application.ports import ProviderPort

        assert hasattr(ProviderPort, "supports_tool_calling")

    def test_provider_port_has_default_model_property(self):
        """ProviderPort deve ter property abstrata default_model."""
        from forge_llm.application.ports import ProviderPort

        assert hasattr(ProviderPort, "default_model")

    def test_provider_port_cannot_be_instantiated(self):
        """ProviderPort nao pode ser instanciado diretamente."""
        from forge_llm.application.ports import ProviderPort

        with pytest.raises(TypeError):
            ProviderPort()  # type: ignore
