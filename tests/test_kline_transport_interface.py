"""Tests for the K-Line transport interface."""

from unittest.mock import Mock

import pytest

from t3diag.kline import KLineConnectionError, KLineTransport
from t3diag.transports.serial_transport import (
    SerialTransport,
    SerialTransportError,
)


def create_serial_transport_mock() -> Mock:
    """Create a mock serial transport."""
    return Mock(spec=SerialTransport)


def test_transport_keeps_serial_transport_dependency() -> None:
    serial_transport = create_serial_transport_mock()

    transport = KLineTransport(serial_transport)

    assert transport.serial_transport is serial_transport


def test_is_open_returns_serial_transport_state() -> None:
    serial_transport = create_serial_transport_mock()
    serial_transport.is_open = True
    transport = KLineTransport(serial_transport)

    assert transport.is_open is True


def test_open_opens_serial_transport() -> None:
    serial_transport = create_serial_transport_mock()
    transport = KLineTransport(serial_transport)

    transport.open()

    serial_transport.open.assert_called_once_with()


def test_open_translates_serial_transport_error() -> None:
    serial_transport = create_serial_transport_mock()
    serial_transport.open.side_effect = SerialTransportError("Fehler")
    transport = KLineTransport(serial_transport)

    with pytest.raises(KLineConnectionError):
        transport.open()


def test_close_closes_serial_transport() -> None:
    serial_transport = create_serial_transport_mock()
    transport = KLineTransport(serial_transport)

    transport.close()

    serial_transport.close.assert_called_once_with()


def test_close_translates_serial_transport_error() -> None:
    serial_transport = create_serial_transport_mock()
    serial_transport.close.side_effect = SerialTransportError("Fehler")
    transport = KLineTransport(serial_transport)

    with pytest.raises(KLineConnectionError):
        transport.close()


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
