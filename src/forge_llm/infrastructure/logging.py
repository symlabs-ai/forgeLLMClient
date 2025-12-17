"""
LogService - Structured logging for ForgeLLM.

Provides JSON-formatted structured logging with correlation IDs
and timing support for LLM provider calls.

Usage:
    from forge_llm.infrastructure.logging import LogService, get_logger

    logger = get_logger(__name__)
    logger.info("message", extra_field="value")

    # With correlation ID
    with LogService.correlation_context("request-123"):
        logger.info("processing request")

    # Timing provider calls
    with LogService.timed("anthropic_call"):
        response = client.messages.create(...)
"""
from __future__ import annotations

import contextlib
import logging
import sys
import time
import uuid
from collections.abc import Generator
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any

import structlog
from structlog.types import EventDict, Processor

if TYPE_CHECKING:
    pass

# Context variable for correlation ID
_correlation_id: ContextVar[str | None] = ContextVar("correlation_id", default=None)

# Flag to track if structlog has been configured
_configured = False


def _add_correlation_id(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Add correlation ID to log event if available."""
    correlation_id = _correlation_id.get()
    if correlation_id:
        event_dict["correlation_id"] = correlation_id
    return event_dict


def _add_timestamp(
    logger: logging.Logger, method_name: str, event_dict: EventDict
) -> EventDict:
    """Add ISO timestamp to log event."""
    event_dict["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    return event_dict


def configure_logging(
    json_output: bool = True,
    log_level: str = "INFO",
) -> None:
    """
    Configure structured logging for the application.

    Args:
        json_output: If True, output JSON format. If False, output console format.
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    """
    global _configured

    if _configured:
        return

    # Build processor chain
    processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        _add_timestamp,
        _add_correlation_id,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]

    if json_output:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure stdlib logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    _configured = True


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a configured structlog logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured structlog logger instance
    """
    configure_logging()
    logger: structlog.stdlib.BoundLogger = structlog.get_logger(name)
    return logger


class LogService:
    """
    Structured logging service with correlation ID and timing support.

    This class provides a structured logging interface with:
    - JSON output format
    - Correlation IDs for request tracing
    - Timing context for measuring operations
    - Structured context fields
    """

    def __init__(self, name: str) -> None:
        self._logger = get_logger(name)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message with structured context."""
        self._logger.info(message, **kwargs)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message with structured context."""
        self._logger.debug(message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message with structured context."""
        self._logger.warning(message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message with structured context."""
        self._logger.error(message, **kwargs)

    def exception(self, message: str, **kwargs: Any) -> None:
        """Log exception with traceback."""
        self._logger.exception(message, **kwargs)

    def bind(self, **kwargs: Any) -> LogService:
        """
        Create a new LogService with bound context.

        Args:
            **kwargs: Context fields to bind

        Returns:
            New LogService with bound context
        """
        new_service = LogService.__new__(LogService)
        new_service._logger = self._logger.bind(**kwargs)
        return new_service

    @staticmethod
    def generate_correlation_id() -> str:
        """Generate a new correlation ID."""
        return str(uuid.uuid4())

    @staticmethod
    @contextlib.contextmanager
    def correlation_context(correlation_id: str | None = None) -> Generator[str, None, None]:
        """
        Context manager for setting correlation ID.

        Args:
            correlation_id: Optional correlation ID. If None, generates a new one.

        Yields:
            The correlation ID being used
        """
        if correlation_id is None:
            correlation_id = LogService.generate_correlation_id()

        token = _correlation_id.set(correlation_id)
        try:
            yield correlation_id
        finally:
            _correlation_id.reset(token)

    @staticmethod
    def get_correlation_id() -> str | None:
        """Get the current correlation ID, if any."""
        return _correlation_id.get()

    @staticmethod
    @contextlib.contextmanager
    def timed(
        operation: str,
        logger: LogService | None = None,
        log_level: str = "debug",
        **extra_context: Any,
    ) -> Generator[dict[str, Any], None, None]:
        """
        Context manager for timing operations.

        Args:
            operation: Name of the operation being timed
            logger: Optional LogService to log timing. If None, uses module logger.
            log_level: Log level for timing messages (debug, info, etc.)
            **extra_context: Additional context to include in logs

        Yields:
            Dict that will contain timing info after context exits

        Example:
            with LogService.timed("anthropic_call", provider="anthropic", model="claude-3"):
                response = await client.messages.create(...)
        """
        timing_info: dict[str, Any] = {
            "operation": operation,
            "start_time": time.time(),
        }
        timing_info.update(extra_context)

        if logger is None:
            logger = LogService(__name__)

        log_method = getattr(logger, log_level, logger.debug)
        log_method(f"Starting {operation}", **extra_context)

        try:
            yield timing_info
        finally:
            elapsed = time.time() - timing_info["start_time"]
            timing_info["elapsed_seconds"] = elapsed
            timing_info["elapsed_ms"] = elapsed * 1000

            log_method(
                f"Completed {operation}",
                elapsed_ms=round(elapsed * 1000, 2),
                **extra_context,
            )


def reset_logging() -> None:
    """Reset logging configuration. Useful for testing."""
    global _configured
    _configured = False
    structlog.reset_defaults()
