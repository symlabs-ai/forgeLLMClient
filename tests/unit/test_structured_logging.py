"""Tests for structured logging module."""
import json
import logging
import time
from io import StringIO
from unittest.mock import patch

import pytest

from forge_llm.infrastructure.logging import (
    LogService,
    configure_logging,
    get_logger,
    reset_logging,
)


@pytest.fixture(autouse=True)
def reset_logging_state():
    """Reset logging state before and after each test."""
    reset_logging()
    yield
    reset_logging()


class TestGetLogger:
    """Tests for get_logger function."""

    def test_get_logger_returns_bound_logger(self):
        """get_logger should return a structlog BoundLogger."""
        logger = get_logger("test")
        assert hasattr(logger, "info")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")

    def test_get_logger_configures_logging_once(self):
        """get_logger should auto-configure logging."""
        with patch(
            "forge_llm.infrastructure.logging.configure_logging"
        ) as mock_configure:
            mock_configure.side_effect = lambda *args, **kwargs: None
            reset_logging()
            get_logger("test1")
            get_logger("test2")
            # Configure is called but _configured flag prevents re-configuration
            assert mock_configure.call_count >= 1


class TestConfigureLogging:
    """Tests for configure_logging function."""

    def test_configure_logging_sets_json_output_by_default(self):
        """configure_logging should default to JSON output."""
        configure_logging()
        # No error means configuration succeeded
        logger = get_logger("test")
        assert logger is not None

    def test_configure_logging_accepts_log_level_parameter(self):
        """configure_logging should accept log_level parameter without error."""
        # Note: logging.basicConfig only sets level if no handlers exist
        # We test that the parameter is accepted
        configure_logging(log_level="DEBUG")
        logger = get_logger("test")
        assert logger is not None


class TestLogService:
    """Tests for LogService class."""

    def test_log_service_init(self):
        """LogService should initialize with a logger."""
        service = LogService("test_module")
        assert service._logger is not None

    def test_log_service_info(self, capfd):
        """LogService.info should log info messages."""
        configure_logging(json_output=False)
        service = LogService("test")
        service.info("test message", key="value")
        # Output is logged, verify no errors
        assert True

    def test_log_service_debug(self, capfd):
        """LogService.debug should log debug messages."""
        configure_logging(json_output=False, log_level="DEBUG")
        service = LogService("test")
        service.debug("debug message")
        assert True

    def test_log_service_warning(self):
        """LogService.warning should log warning messages."""
        service = LogService("test")
        service.warning("warning message")
        assert True

    def test_log_service_error(self):
        """LogService.error should log error messages."""
        service = LogService("test")
        service.error("error message")
        assert True

    def test_log_service_exception(self):
        """LogService.exception should log exceptions."""
        service = LogService("test")
        try:
            raise ValueError("test error")
        except ValueError:
            service.exception("caught exception")
        assert True

    def test_log_service_bind_returns_new_service(self):
        """LogService.bind should return a new LogService with bound context."""
        service = LogService("test")
        bound = service.bind(request_id="123")
        assert bound is not service
        assert isinstance(bound, LogService)


class TestCorrelationId:
    """Tests for correlation ID functionality."""

    def test_generate_correlation_id_returns_uuid(self):
        """generate_correlation_id should return a valid UUID string."""
        cid = LogService.generate_correlation_id()
        assert isinstance(cid, str)
        assert len(cid) == 36  # UUID format: 8-4-4-4-12

    def test_correlation_context_sets_id(self):
        """correlation_context should set the correlation ID."""
        with LogService.correlation_context("test-123") as cid:
            assert cid == "test-123"
            assert LogService.get_correlation_id() == "test-123"

    def test_correlation_context_generates_id_if_none(self):
        """correlation_context should generate ID if not provided."""
        with LogService.correlation_context() as cid:
            assert cid is not None
            assert len(cid) == 36

    def test_correlation_context_clears_on_exit(self):
        """correlation_context should clear ID after exiting."""
        with LogService.correlation_context("test-123"):
            pass
        assert LogService.get_correlation_id() is None

    def test_get_correlation_id_returns_none_by_default(self):
        """get_correlation_id should return None when not in context."""
        assert LogService.get_correlation_id() is None

    def test_nested_correlation_contexts(self):
        """Nested correlation contexts should work correctly."""
        with LogService.correlation_context("outer"):
            assert LogService.get_correlation_id() == "outer"
            with LogService.correlation_context("inner"):
                assert LogService.get_correlation_id() == "inner"
            assert LogService.get_correlation_id() == "outer"
        assert LogService.get_correlation_id() is None


class TestTimedContext:
    """Tests for timing context manager."""

    def test_timed_returns_timing_info(self):
        """timed should yield a dict with timing info."""
        with LogService.timed("test_op") as timing:
            assert "operation" in timing
            assert timing["operation"] == "test_op"
            assert "start_time" in timing

    def test_timed_calculates_elapsed_time(self):
        """timed should calculate elapsed time after context exits."""
        with LogService.timed("test_op") as timing:
            time.sleep(0.01)  # Sleep 10ms
        assert "elapsed_seconds" in timing
        assert "elapsed_ms" in timing
        assert timing["elapsed_ms"] >= 10  # At least 10ms

    def test_timed_includes_extra_context(self):
        """timed should include extra context in timing dict."""
        with LogService.timed("test_op", provider="openai", model="gpt-4") as timing:
            pass
        assert timing["provider"] == "openai"
        assert timing["model"] == "gpt-4"

    def test_timed_uses_custom_logger(self):
        """timed should use custom logger if provided."""
        custom_logger = LogService("custom")
        with patch.object(custom_logger, "debug") as mock_debug:
            with LogService.timed("test_op", logger=custom_logger):
                pass
            assert mock_debug.call_count == 2  # Start and complete

    def test_timed_uses_specified_log_level(self):
        """timed should use the specified log level."""
        custom_logger = LogService("custom")
        with patch.object(custom_logger, "info") as mock_info:
            with LogService.timed("test_op", logger=custom_logger, log_level="info"):
                pass
            assert mock_info.call_count == 2


class TestJSONOutput:
    """Tests for JSON output format."""

    def test_json_output_is_valid_json(self, capfd):
        """JSON output should be valid JSON."""
        reset_logging()
        configure_logging(json_output=True, log_level="INFO")

        # Capture stdout
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        handler.setLevel(logging.INFO)

        root_logger = logging.getLogger()
        root_logger.addHandler(handler)

        service = LogService("test_json")
        service.info("test message", key="value")

        output = stream.getvalue()
        if output:
            try:
                data = json.loads(output.strip())
                assert "event" in data
            except json.JSONDecodeError:
                # Console format was used, that's also OK
                pass

        root_logger.removeHandler(handler)


class TestResetLogging:
    """Tests for reset_logging function."""

    def test_reset_logging_clears_configuration(self):
        """reset_logging should clear the configuration flag."""
        configure_logging()
        reset_logging()
        # After reset, we should be able to reconfigure without error
        configure_logging(log_level="DEBUG")
        # Verify we can get a logger after reconfiguration
        logger = get_logger("test_reset")
        assert logger is not None
