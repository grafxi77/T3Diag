"""Tests für die serielle Transportschicht."""

from unittest.mock import Mock, patch

import pytest

from t3diag.transports.serial_transport import (
    SerialTransport,
    SerialTransportError,
    SerialTransportTimeoutError,
)


@patch("serial.Serial")
def test_open_and_close(mock_serial: Mock) -> None:
    connection = Mock()
    connection.is_open = True
    mock_serial.return_value = connection

    transport = SerialTransport("/dev/ttyUSB0")

    transport.open()
    assert transport.is_open

    transport.close()
    connection.close.assert_called_once()


@patch("serial.Serial")
def test_write(mock_serial: Mock) -> None:
    connection = Mock()
    connection.is_open = True
    connection.write.return_value = 2
    mock_serial.return_value = connection

    transport = SerialTransport("/dev/ttyUSB0")
    transport.open()

    written = transport.write(b"\x01\x02")

    assert written == 2
    connection.write.assert_called_once_with(b"\x01\x02")


@patch("serial.Serial")
def test_read(mock_serial: Mock) -> None:
    connection = Mock()
    connection.is_open = True
    connection.read.return_value = b"\x55"
    mock_serial.return_value = connection

    transport = SerialTransport("/dev/ttyUSB0")
    transport.open()

    data = transport.read(1)

    assert data == b"\x55"


def test_read_rejects_invalid_size() -> None:
    transport = SerialTransport("/dev/ttyUSB0")

    with pytest.raises(ValueError):
        transport.read(0)


def test_write_requires_open_connection() -> None:
    transport = SerialTransport("/dev/ttyUSB0")

    with pytest.raises(SerialTransportError):
        transport.write(b"\x01")


def test_buffer_operations() -> None:
    transport = SerialTransport("/dev/ttyUSB0")

    connection = Mock()
    connection.is_open = True
    transport._connection = connection

    transport.flush()
    transport.reset_input_buffer()
    transport.reset_output_buffer()

    connection.flush.assert_called_once()
    connection.reset_input_buffer.assert_called_once()
    connection.reset_output_buffer.assert_called_once()


def test_read_exact() -> None:
    transport = SerialTransport("/dev/ttyUSB0")

    connection = Mock()
    connection.is_open = True
    connection.read.side_effect = [b"\x55", b"\x01"]
    transport._connection = connection

    assert transport.read_exact(2) == b"\x55\x01"


def test_read_exact_timeout() -> None:
    transport = SerialTransport("/dev/ttyUSB0")

    connection = Mock()
    connection.is_open = True
    connection.read.side_effect = [b"\x55", b""]
    transport._connection = connection

    with pytest.raises(SerialTransportTimeoutError):
        transport.read_exact(2)


def test_read_exact_rejects_invalid_size() -> None:
    transport = SerialTransport("/dev/ttyUSB0")

    with pytest.raises(ValueError):
        transport.read_exact(0)


def test_set_break_controls_serial_break() -> None:
    transport = SerialTransport("/dev/ttyUSB0")

    connection = Mock()
    connection.is_open = True
    transport._connection = connection

    transport.set_break(True)
    assert connection.break_condition is True

    transport.set_break(False)
    assert connection.break_condition is False


@patch("serial.Serial")
def test_context_manager(mock_serial: Mock) -> None:
    connection = Mock()
    connection.is_open = True
    mock_serial.return_value = connection

    with SerialTransport("/dev/ttyUSB0") as transport:
        assert transport.is_open

    connection.close.assert_called_once()
