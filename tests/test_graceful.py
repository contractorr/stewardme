"""Tests for graceful degradation primitives."""

from unittest.mock import patch

import pytest

from graceful import graceful, graceful_context


class TestGracefulDecorator:
    def test_passes_through_on_success(self):
        @graceful("test.metric", fallback="fail")
        def add(a, b):
            return a + b

        assert add(1, 2) == 3

    def test_returns_fallback_on_exception(self):
        @graceful("test.metric", fallback=-1)
        def boom():
            raise ValueError("oops")

        assert boom() == -1

    def test_returns_none_fallback_by_default(self):
        @graceful("test.metric")
        def boom():
            raise RuntimeError("fail")

        assert boom() is None

    def test_increments_counter_on_exception(self):
        @graceful("test.dec.counter", fallback=None)
        def boom():
            raise ValueError("oops")

        with patch("graceful.metrics") as mock_metrics:
            boom()
            mock_metrics.counter.assert_called_once_with("test.dec.counter")

    def test_exc_types_narrowing_propagates(self):
        @graceful("test.metric", fallback=None, exc_types=(ValueError,))
        def boom():
            raise TypeError("wrong type")

        with pytest.raises(TypeError):
            boom()

    def test_exc_types_narrowing_catches(self):
        @graceful("test.metric", fallback="caught", exc_types=(ValueError,))
        def boom():
            raise ValueError("val")

        assert boom() == "caught"

    def test_preserves_function_name(self):
        @graceful("test.metric")
        def my_func():
            """My docstring."""

        assert my_func.__name__ == "my_func"
        assert my_func.__doc__ == "My docstring."

    def test_log_level_debug(self):
        @graceful("test.debug", fallback=None, log_level="debug")
        def boom():
            raise RuntimeError("fail")

        with patch("graceful.structlog") as mock_sl:
            mock_logger = mock_sl.get_logger.return_value
            boom()
            mock_logger.debug.assert_called_once()
            mock_logger.warning.assert_not_called()


class TestGracefulContext:
    def test_no_exception_runs_normally(self):
        result = []
        with graceful_context("test.ctx"):
            result.append(1)
        assert result == [1]

    def test_continues_after_exception(self):
        value = "default"
        with graceful_context("test.ctx"):
            raise RuntimeError("boom")
        # execution continues; value unchanged
        assert value == "default"

    def test_increments_counter_on_exception(self):
        with patch("graceful.metrics") as mock_metrics:
            with graceful_context("test.ctx.counter"):
                raise ValueError("oops")
            mock_metrics.counter.assert_called_once_with("test.ctx.counter")

    def test_preserves_default_on_exception_before_assignment(self):
        data = "original"
        with graceful_context("test.ctx"):
            data = 1 / 0  # ZeroDivisionError before assignment completes
        assert data == "original"

    def test_exc_types_narrowing_propagates(self):
        with pytest.raises(TypeError):
            with graceful_context("test.ctx", exc_types=(ValueError,)):
                raise TypeError("wrong")

    def test_exc_types_narrowing_catches(self):
        with graceful_context("test.ctx", exc_types=(ValueError,)):
            raise ValueError("caught")
        # no exception propagated

    def test_log_level_debug(self):
        with patch("graceful.structlog") as mock_sl:
            mock_logger = mock_sl.get_logger.return_value
            with graceful_context("test.ctx.debug", log_level="debug"):
                raise RuntimeError("fail")
            mock_logger.debug.assert_called_once()
            mock_logger.warning.assert_not_called()


class TestLastResortSafety:
    def test_log_and_count_never_raises(self):
        """Even if structlog + metrics both fail, decorator still returns fallback."""

        @graceful("test.broken", fallback="safe")
        def boom():
            raise RuntimeError("inner")

        with patch("graceful.structlog") as mock_sl, patch("graceful.metrics") as mock_m:
            mock_sl.get_logger.side_effect = Exception("structlog dead")
            mock_m.counter.side_effect = Exception("metrics dead")
            assert boom() == "safe"
