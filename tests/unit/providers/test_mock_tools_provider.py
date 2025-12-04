"""Testes para MockToolsProvider - TDD RED phase."""

import pytest


class TestMockToolsProvider:
    """Testes para MockToolsProvider."""

    def test_mock_tools_provider_implements_provider_port(self):
        """MockToolsProvider deve implementar ProviderPort."""
        from forge_llm.application.ports import ProviderPort
        from forge_llm.providers import MockToolsProvider

        assert issubclass(MockToolsProvider, ProviderPort)

    def test_mock_tools_provider_creation(self):
        """MockToolsProvider deve ser criado sem erros."""
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        assert provider is not None

    def test_mock_tools_provider_name(self):
        """MockToolsProvider deve ter provider_name = 'mock-tools'."""
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        assert provider.provider_name == "mock-tools"

    def test_mock_tools_provider_supports_tool_calling(self):
        """MockToolsProvider deve suportar tool calling."""
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        assert provider.supports_tool_calling is True

    def test_mock_tools_provider_default_model(self):
        """MockToolsProvider deve ter modelo padrao."""
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        assert provider.default_model == "mock-tools-model"

    @pytest.mark.asyncio
    async def test_mock_tools_provider_chat_returns_tool_call(self):
        """MockToolsProvider.chat deve retornar tool_call quando tool registrada."""
        from forge_llm.domain.value_objects import Message, ToolDefinition
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        provider.register_tool(
            ToolDefinition(
                name="calculator",
                description="Does math",
                parameters={"type": "object", "properties": {}},
            )
        )

        messages = [Message(role="user", content="What is 2+2?")]
        response = await provider.chat(messages)

        assert response.has_tool_calls is True
        assert len(response.tool_calls) == 1
        assert response.tool_calls[0].name == "calculator"

    @pytest.mark.asyncio
    async def test_mock_tools_provider_chat_no_tool_call_without_tools(self):
        """MockToolsProvider.chat sem tools deve retornar resposta normal."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        messages = [Message(role="user", content="Hello")]
        response = await provider.chat(messages)

        assert response.has_tool_calls is False
        assert response.content != ""

    def test_mock_tools_provider_register_tool(self):
        """MockToolsProvider deve permitir registrar tools."""
        from forge_llm.domain.value_objects import ToolDefinition
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        tool = ToolDefinition(
            name="test_tool",
            description="Test",
            parameters={"type": "object"},
        )
        provider.register_tool(tool)

        assert len(provider.tools) == 1
        assert provider.tools[0].name == "test_tool"

    def test_mock_tools_provider_register_multiple_tools(self):
        """MockToolsProvider deve permitir registrar multiplas tools."""
        from forge_llm.domain.value_objects import ToolDefinition
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        provider.register_tool(
            ToolDefinition(name="tool1", description="T1", parameters={})
        )
        provider.register_tool(
            ToolDefinition(name="tool2", description="T2", parameters={})
        )

        assert len(provider.tools) == 2

    def test_mock_tools_provider_has_tool(self):
        """MockToolsProvider deve verificar se tool existe."""
        from forge_llm.domain.value_objects import ToolDefinition
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        provider.register_tool(
            ToolDefinition(name="calculator", description="Math", parameters={})
        )

        assert provider.has_tool("calculator") is True
        assert provider.has_tool("unknown") is False

    @pytest.mark.asyncio
    async def test_mock_tools_provider_multiple_tool_calls(self):
        """MockToolsProvider deve retornar multiplos tool_calls."""
        from forge_llm.domain.value_objects import Message, ToolDefinition
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        provider.register_tool(
            ToolDefinition(name="calculator", description="Math", parameters={})
        )
        provider.register_tool(
            ToolDefinition(name="weather", description="Weather", parameters={})
        )
        provider.set_next_tool_calls(["calculator", "weather"])

        messages = [Message(role="user", content="Math and weather")]
        response = await provider.chat(messages)

        assert len(response.tool_calls) == 2
        names = [tc.name for tc in response.tool_calls]
        assert "calculator" in names
        assert "weather" in names

    @pytest.mark.asyncio
    async def test_mock_tools_provider_tool_call_has_id(self):
        """Tool calls devem ter id unico."""
        from forge_llm.domain.value_objects import Message, ToolDefinition
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        provider.register_tool(
            ToolDefinition(name="calculator", description="Math", parameters={})
        )

        messages = [Message(role="user", content="2+2")]
        response = await provider.chat(messages)

        assert response.tool_calls[0].id is not None
        assert response.tool_calls[0].id.startswith("tc_")

    @pytest.mark.asyncio
    async def test_mock_tools_provider_tool_call_has_arguments(self):
        """Tool calls devem ter argumentos."""
        from forge_llm.domain.value_objects import Message, ToolDefinition
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        provider.register_tool(
            ToolDefinition(name="calculator", description="Math", parameters={})
        )
        provider.set_next_tool_arguments({"a": 2, "b": 2, "operation": "add"})

        messages = [Message(role="user", content="2+2")]
        response = await provider.chat(messages)

        assert isinstance(response.tool_calls[0].arguments, dict)
        assert response.tool_calls[0].arguments.get("operation") == "add"

    def test_mock_tools_provider_reset(self):
        """MockToolsProvider.reset deve limpar estado."""
        from forge_llm.domain.value_objects import ToolDefinition
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        provider.register_tool(
            ToolDefinition(name="calculator", description="Math", parameters={})
        )
        provider.set_next_tool_calls(["calculator"])
        provider.set_next_tool_arguments({"a": 1})

        assert len(provider.tools) == 1

        provider.reset()

        assert len(provider.tools) == 0
        assert provider.call_count == 0

    @pytest.mark.asyncio
    async def test_mock_tools_provider_reset_clears_call_count(self):
        """MockToolsProvider.reset deve zerar call_count."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        messages = [Message(role="user", content="Hello")]

        await provider.chat(messages)
        await provider.chat(messages)
        assert provider.call_count == 2

        provider.reset()
        assert provider.call_count == 0

    @pytest.mark.asyncio
    async def test_mock_tools_provider_chat_stream_yields_chunks(self):
        """MockToolsProvider.chat_stream deve retornar chunks."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        messages = [Message(role="user", content="Hello")]

        chunks = []
        async for chunk in provider.chat_stream(messages):
            chunks.append(chunk)

        assert len(chunks) > 0
        assert chunks[-1].get("finish_reason") == "stop"

    @pytest.mark.asyncio
    async def test_mock_tools_provider_chat_stream_increments_call_count(self):
        """MockToolsProvider.chat_stream deve incrementar call_count."""
        from forge_llm.domain.value_objects import Message
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        messages = [Message(role="user", content="Hello")]

        assert provider.call_count == 0
        async for _ in provider.chat_stream(messages):
            pass
        assert provider.call_count == 1

    def test_mock_tools_provider_supports_streaming(self):
        """MockToolsProvider deve suportar streaming."""
        from forge_llm.providers import MockToolsProvider

        provider = MockToolsProvider()
        assert provider.supports_streaming is True
