"""Tests for the K-Line exception hierarchy."""

from t3diag.kline import (
    KLineConnectionError,
    KLineError,
    KLineInitializationError,
    KLineTimeoutError,
)


def test_connection_error_inherits_from_kline_error() -> None:
    assert issubclass(KLineConnectionError, KLineError)


def test_timeout_error_inherits_from_kline_error() -> None:
    assert issubclass(KLineTimeoutError, KLineError)


def test_initialization_error_inherits_from_kline_error() -> None:
    assert issubclass(KLineInitializationError, KLineError)
