"""Tests for the K-Line transport interface."""

from unittest.mock import Mock

from t3diag.kline import KLineTransport
from t3diag.transports.serial_transport import SerialTransport


def create_serial_transport_mock() -> SerialTransport:
    """Create a mock serial transport."""
    return Mock(spec=SerialTransport)


def test_transport_keeps_serial_transport_dependency() -> None:
    serial_transport = create_serial_transport_mock()

    transport = KLineTransport(serial_transport)

    assert transport.serial_transport is serial_transport


def test_transport_exposes_required_public_api() -> None:
    serial_transport = create_serial_transport_mock()
    transport = KLineTransport(serial_transport)

    assert callable(transport.open)
    assert callable(transport.close)
    assert callable(transport.send)
    assert callable(transport.receive)
    assert callable(transport.receive_exact)
    assert callable(transport.flush)
    assert callable(transport.initialize_5_baud)


def test_transport_does_not_expose_fast_initialization() -> None:
    serial_transport = create_serial_transport_mock()
    transport = KLineTransport(serial_transport)

    assert not hasattr(transport, "initialize_fast")
    assert not hasattr(transport, "fast_init")
