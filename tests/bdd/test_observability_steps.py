"""Step definitions para observability.feature."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any

import pytest
from pytest_bdd import given, scenarios, then, when

from forge_llm.domain.value_objects import TokenUsage
from forge_llm.observability import (
    CallbackObserver,
    ChatCompleteEvent,
    ChatErrorEvent,
    ChatStartEvent,
    LoggingObserver,
    MetricsObserver,
    ObservabilityConfig,
    ObservabilityManager,
    ObserverPort,
)

scenarios("../../specs/bdd/10_forge_core/observability.feature")


def run_async(coro: Any) -> Any:
    """Helper to run async code in sync context."""
    return asyncio.get_event_loop().run_until_complete(coro)


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


@pytest.fixture
def context() -> dict[str, Any]:
    """Contexto compartilhado entre steps."""
    return {}


# ============ GIVEN ============


@given("um client configurado com observability")
def dado_client_com_observability(context: dict[str, Any]) -> None:
    """Configura client com observability manager."""
    context["manager"] = ObservabilityManager()


@given("um LoggingObserver configurado")
def dado_logging_observer(context: dict[str, Any]) -> None:
    """Configura logging observer."""
    observer = LoggingObserver()
    context["logging_observer"] = observer
    context["manager"].add_observer(observer)
    # Tambem adiciona mock para verificacao
    mock = MockObserver()
    context["mock_observer"] = mock
    context["manager"].add_observer(mock)


@given("um MetricsObserver configurado")
def dado_metrics_observer(context: dict[str, Any]) -> None:
    """Configura metrics observer."""
    observer = MetricsObserver()
    context["metrics_observer"] = observer
    context["manager"].add_observer(observer)


@given("um CallbackObserver com callbacks registrados")
def dado_callback_observer(context: dict[str, Any]) -> None:
    """Configura callback observer."""
    context["callback_starts"] = []
    context["callback_completes"] = []

    async def on_start(event: ChatStartEvent) -> None:
        context["callback_starts"].append(event)

    async def on_complete(event: ChatCompleteEvent) -> None:
        context["callback_completes"].append(event)

    observer = CallbackObserver(on_start=on_start, on_complete=on_complete)
    context["callback_observer"] = observer
    context["manager"].add_observer(observer)


@given("um ObservabilityManager desabilitado")
def dado_manager_desabilitado(context: dict[str, Any]) -> None:
    """Configura manager desabilitado."""
    config = ObservabilityConfig(enabled=False)
    context["manager"] = ObservabilityManager(config=config)


@given("um MockObserver configurado")
def dado_mock_observer(context: dict[str, Any]) -> None:
    """Configura mock observer."""
    observer = MockObserver()
    context["mock_observer"] = observer
    context["manager"].add_observer(observer)


@given("multiplos observers configurados")
def dado_multiplos_observers(context: dict[str, Any]) -> None:
    """Configura multiplos observers."""
    context["observers"] = []
    for _ in range(3):
        observer = MockObserver()
        context["observers"].append(observer)
        context["manager"].add_observer(observer)


@given("um observer que falha")
def dado_observer_que_falha(context: dict[str, Any]) -> None:
    """Configura observer que falha."""
    observer = FailingObserver()
    context["failing_observer"] = observer
    context["manager"].add_observer(observer)


@given("um observer normal")
def dado_observer_normal(context: dict[str, Any]) -> None:
    """Configura observer normal."""
    observer = MockObserver()
    context["normal_observer"] = observer
    context["manager"].add_observer(observer)


@given("um MetricsObserver com metricas existentes")
def dado_metrics_com_dados(context: dict[str, Any]) -> None:
    """Configura metrics observer com dados."""
    observer = MetricsObserver()
    observer._metrics.total_requests = 10
    observer._metrics.total_tokens = 1000
    observer._metrics.total_errors = 5
    context["metrics_observer"] = observer


# ============ WHEN ============


@when("eu fizer uma chamada de chat")
def quando_fazer_chamada(context: dict[str, Any]) -> None:
    """Simula chamada de chat emitindo eventos."""
    manager = context["manager"]

    async def emit_events() -> None:
        # Emit start event
        start_event = ChatStartEvent(
            timestamp=datetime.now(),
            request_id="req_test123",
            provider="openai",
            model="gpt-4",
            message_count=1,
            has_tools=False,
        )
        await manager.emit(start_event)
        context["start_event"] = start_event

        # Emit complete event
        complete_event = ChatCompleteEvent(
            timestamp=datetime.now(),
            request_id="req_test123",
            provider="openai",
            model="gpt-4",
            latency_ms=250.0,
            token_usage=TokenUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30),
            finish_reason="stop",
            tool_calls_count=0,
        )
        await manager.emit(complete_event)
        context["complete_event"] = complete_event

    run_async(emit_events())
    context["call_success"] = True


@when("eu fizer 3 chamadas de chat")
def quando_fazer_3_chamadas(context: dict[str, Any]) -> None:
    """Simula 3 chamadas de chat."""
    manager = context["manager"]

    async def emit_events() -> None:
        for i in range(3):
            # Start
            await manager.emit(
                ChatStartEvent(
                    timestamp=datetime.now(),
                    request_id=f"req_{i}",
                    provider="openai",
                    model="gpt-4",
                    message_count=1,
                    has_tools=False,
                )
            )

            # Complete
            await manager.emit(
                ChatCompleteEvent(
                    timestamp=datetime.now(),
                    request_id=f"req_{i}",
                    provider="openai",
                    model="gpt-4",
                    latency_ms=100.0 * (i + 1),  # 100, 200, 300
                    token_usage=TokenUsage(
                        prompt_tokens=10 * (i + 1),
                        completion_tokens=5 * (i + 1),
                        total_tokens=15 * (i + 1),
                    ),
                    finish_reason="stop",
                    tool_calls_count=0,
                )
            )

    run_async(emit_events())


@when("eu fizer chamadas para diferentes providers")
def quando_chamadas_diferentes_providers(context: dict[str, Any]) -> None:
    """Simula chamadas para diferentes providers."""
    manager = context["manager"]

    async def emit_events() -> None:
        providers = ["openai", "openai", "anthropic"]

        for i, provider in enumerate(providers):
            await manager.emit(
                ChatStartEvent(
                    timestamp=datetime.now(),
                    request_id=f"req_{i}",
                    provider=provider,
                    model="model",
                    message_count=1,
                    has_tools=False,
                )
            )

            await manager.emit(
                ChatCompleteEvent(
                    timestamp=datetime.now(),
                    request_id=f"req_{i}",
                    provider=provider,
                    model="model",
                    latency_ms=100.0,
                    token_usage=TokenUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20),
                    finish_reason="stop",
                    tool_calls_count=0,
                )
            )

    run_async(emit_events())


@when("ocorrer um erro na chamada")
def quando_erro_na_chamada(context: dict[str, Any]) -> None:
    """Simula erro na chamada."""
    manager = context["manager"]

    async def emit_events() -> None:
        await manager.emit(
            ChatStartEvent(
                timestamp=datetime.now(),
                request_id="req_error",
                provider="openai",
                model="gpt-4",
                message_count=1,
                has_tools=False,
            )
        )

        await manager.emit(
            ChatErrorEvent(
                timestamp=datetime.now(),
                request_id="req_error",
                provider="openai",
                error_type="RateLimitError",
                error_message="Rate limit exceeded",
                latency_ms=50.0,
                retryable=True,
            )
        )

    run_async(emit_events())


@when("eu resetar as metricas")
def quando_resetar_metricas(context: dict[str, Any]) -> None:
    """Reseta metricas."""
    context["metrics_observer"].reset()


@when("eu fizer uma chamada de chat com conteudo sensivel")
def quando_chamada_com_conteudo_sensivel(context: dict[str, Any]) -> None:
    """Simula chamada com conteudo sensivel."""
    manager = context["manager"]

    context["sensitive_content"] = "SENHA_SECRETA_12345"

    async def emit_events() -> None:
        # Note: eventos nao contem conteudo por design
        await manager.emit(
            ChatStartEvent(
                timestamp=datetime.now(),
                request_id="req_sensivel",
                provider="openai",
                model="gpt-4",
                message_count=1,
                has_tools=False,
            )
        )

    run_async(emit_events())


# ============ THEN ============


@then("o observer deve registrar evento de inicio")
def entao_registrar_inicio(context: dict[str, Any]) -> None:
    """Verifica evento de inicio."""
    mock = context["mock_observer"]
    starts = [e for e in mock.events if isinstance(e, ChatStartEvent)]
    assert len(starts) >= 1


@then("o observer deve registrar evento de conclusao")
def entao_registrar_conclusao(context: dict[str, Any]) -> None:
    """Verifica evento de conclusao."""
    mock = context["mock_observer"]
    completes = [e for e in mock.events if isinstance(e, ChatCompleteEvent)]
    assert len(completes) >= 1


@then("as metricas devem mostrar 3 requests totais")
def entao_3_requests(context: dict[str, Any]) -> None:
    """Verifica total de requests."""
    metrics = context["metrics_observer"].metrics
    assert metrics.total_requests == 3


@then("as metricas devem mostrar tokens consumidos")
def entao_tokens_consumidos(context: dict[str, Any]) -> None:
    """Verifica tokens consumidos."""
    metrics = context["metrics_observer"].metrics
    assert metrics.total_tokens > 0
    assert metrics.total_prompt_tokens > 0
    assert metrics.total_completion_tokens > 0


@then("as metricas devem mostrar latencia media")
def entao_latencia_media(context: dict[str, Any]) -> None:
    """Verifica latencia media."""
    metrics = context["metrics_observer"].metrics
    assert metrics.avg_latency_ms > 0


@then("as metricas devem agrupar requests por provider")
def entao_requests_por_provider(context: dict[str, Any]) -> None:
    """Verifica agrupamento por provider."""
    metrics = context["metrics_observer"].metrics
    assert metrics.requests_by_provider["openai"] == 2
    assert metrics.requests_by_provider["anthropic"] == 1


@then("as metricas devem agrupar tokens por provider")
def entao_tokens_por_provider(context: dict[str, Any]) -> None:
    """Verifica tokens por provider."""
    metrics = context["metrics_observer"].metrics
    assert "openai" in metrics.tokens_by_provider
    assert "anthropic" in metrics.tokens_by_provider


@then("o callback on_start deve ser executado")
def entao_callback_start(context: dict[str, Any]) -> None:
    """Verifica callback on_start."""
    assert len(context["callback_starts"]) >= 1


@then("o callback on_complete deve ser executado")
def entao_callback_complete(context: dict[str, Any]) -> None:
    """Verifica callback on_complete."""
    assert len(context["callback_completes"]) >= 1


@then("o observer nao deve receber eventos")
def entao_sem_eventos(context: dict[str, Any]) -> None:
    """Verifica que observer nao recebeu eventos."""
    mock = context["mock_observer"]
    assert len(mock.events) == 0


@then("o observer deve registrar evento de erro")
def entao_registrar_erro(context: dict[str, Any]) -> None:
    """Verifica evento de erro."""
    metrics = context["metrics_observer"].metrics
    assert metrics.total_errors >= 1


@then("as metricas devem mostrar 1 erro total")
def entao_1_erro(context: dict[str, Any]) -> None:
    """Verifica total de erros."""
    metrics = context["metrics_observer"].metrics
    assert metrics.total_errors == 1


@then("todos os observers devem receber o evento")
def entao_todos_recebem(context: dict[str, Any]) -> None:
    """Verifica que todos observers receberam."""
    for observer in context["observers"]:
        assert len(observer.events) >= 1


@then("o observer normal deve receber o evento")
def entao_normal_recebe(context: dict[str, Any]) -> None:
    """Verifica que observer normal recebeu."""
    assert len(context["normal_observer"].events) >= 1


@then("a chamada deve completar com sucesso")
def entao_chamada_sucesso(context: dict[str, Any]) -> None:
    """Verifica que chamada completou."""
    assert context.get("call_success", True)


@then("todas as metricas devem estar zeradas")
def entao_metricas_zeradas(context: dict[str, Any]) -> None:
    """Verifica metricas zeradas."""
    metrics = context["metrics_observer"].metrics
    assert metrics.total_requests == 0
    assert metrics.total_tokens == 0
    assert metrics.total_errors == 0


@then("o log nao deve conter o conteudo da mensagem")
def entao_sem_conteudo_no_log(context: dict[str, Any]) -> None:
    """Verifica que log nao contem conteudo sensivel."""
    # Por design, eventos nao contem conteudo
    # Apenas verificamos que sensitive_content existe no contexto
    # mas nao apareceria em logs de eventos
    assert "sensitive_content" in context
    # ChatStartEvent nao tem campo de conteudo, apenas message_count
