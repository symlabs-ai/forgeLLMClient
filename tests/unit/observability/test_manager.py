"""Testes unitarios para ObservabilityManager."""

from datetime import datetime
from typing import Any

import pytest

from forge_llm.observability.events import ChatStartEvent
from forge_llm.observability.manager import ObservabilityConfig, ObservabilityManager
from forge_llm.observability.observer_port import ObserverPort


class MockObserver(ObserverPort):
    """Observer mock para testes."""

    def __init__(self) -> None:
        self.events: list[Any] = []

    async def on_event(self, event: Any) -> None:
        """Armazena evento recebido."""
        self.events.append(event)


class FailingObserver(ObserverPort):
    """Observer que sempre falha."""

    async def on_event(self, event: Any) -> None:
        """Sempre lanca excecao."""
        raise RuntimeError("Observer error")


class TestObservabilityConfig:
    """Testes para ObservabilityConfig."""

    def test_config_default(self) -> None:
        """Config padrao deve ter observability habilitado."""
        config = ObservabilityConfig()

        assert config.enabled is True
        assert config.capture_content is False

    def test_config_custom(self) -> None:
        """Deve aceitar valores customizados."""
        config = ObservabilityConfig(enabled=False, capture_content=True)

        assert config.enabled is False
        assert config.capture_content is True


class TestObservabilityManager:
    """Testes para ObservabilityManager."""

    def test_criar_manager_default(self) -> None:
        """Deve criar manager com config padrao."""
        manager = ObservabilityManager()

        assert manager._config.enabled is True
        assert len(manager._observers) == 0

    def test_criar_manager_com_config(self) -> None:
        """Deve criar manager com config customizada."""
        config = ObservabilityConfig(enabled=False)
        manager = ObservabilityManager(config=config)

        assert manager._config.enabled is False

    def test_add_observer(self) -> None:
        """Deve adicionar observer."""
        manager = ObservabilityManager()
        observer = MockObserver()

        manager.add_observer(observer)

        assert len(manager._observers) == 1
        assert observer in manager._observers

    def test_add_multiple_observers(self) -> None:
        """Deve adicionar multiplos observers."""
        manager = ObservabilityManager()
        obs1 = MockObserver()
        obs2 = MockObserver()

        manager.add_observer(obs1)
        manager.add_observer(obs2)

        assert len(manager._observers) == 2

    def test_remove_observer(self) -> None:
        """Deve remover observer."""
        manager = ObservabilityManager()
        observer = MockObserver()

        manager.add_observer(observer)
        manager.remove_observer(observer)

        assert len(manager._observers) == 0

    def test_remove_observer_nao_existente(self) -> None:
        """Deve ignorar remocao de observer nao existente."""
        manager = ObservabilityManager()
        observer = MockObserver()

        # Nao deve lancar excecao
        manager.remove_observer(observer)

        assert len(manager._observers) == 0

    @pytest.mark.asyncio
    async def test_emit_para_todos_observers(self) -> None:
        """Deve emitir evento para todos observers."""
        manager = ObservabilityManager()
        obs1 = MockObserver()
        obs2 = MockObserver()

        manager.add_observer(obs1)
        manager.add_observer(obs2)

        event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            message_count=1,
            has_tools=False,
        )

        await manager.emit(event)

        assert len(obs1.events) == 1
        assert len(obs2.events) == 1
        assert obs1.events[0] == event
        assert obs2.events[0] == event

    @pytest.mark.asyncio
    async def test_emit_desabilitado(self) -> None:
        """Nao deve emitir quando desabilitado."""
        config = ObservabilityConfig(enabled=False)
        manager = ObservabilityManager(config=config)
        observer = MockObserver()

        manager.add_observer(observer)

        event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            message_count=1,
            has_tools=False,
        )

        await manager.emit(event)

        assert len(observer.events) == 0

    @pytest.mark.asyncio
    async def test_emit_sem_observers(self) -> None:
        """Deve funcionar sem observers."""
        manager = ObservabilityManager()

        event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            message_count=1,
            has_tools=False,
        )

        # Nao deve lancar excecao
        await manager.emit(event)

    @pytest.mark.asyncio
    async def test_emit_continua_apos_falha_observer(self) -> None:
        """Deve continuar emitindo mesmo se um observer falhar."""
        manager = ObservabilityManager()
        obs1 = MockObserver()
        failing = FailingObserver()
        obs2 = MockObserver()

        manager.add_observer(obs1)
        manager.add_observer(failing)
        manager.add_observer(obs2)

        event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_abc123",
            provider="openai",
            model="gpt-4",
            message_count=1,
            has_tools=False,
        )

        # Nao deve lancar excecao
        await manager.emit(event)

        # Outros observers devem ter recebido o evento
        assert len(obs1.events) == 1
        assert len(obs2.events) == 1

    def test_generate_request_id(self) -> None:
        """Deve gerar request_id unico."""
        id1 = ObservabilityManager.generate_request_id()
        id2 = ObservabilityManager.generate_request_id()

        assert id1.startswith("req_")
        assert len(id1) == 16  # "req_" + 12 hex chars
        assert id1 != id2  # Deve ser unico
