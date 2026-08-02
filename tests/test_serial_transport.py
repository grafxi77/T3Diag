from unittest.mock import MagicMock, patch

import pytest

from t3diag.transports.serial_transport import (
    SerialTransport,
    SerialTransportError,
)


@patch("t3diag.transports.serial_transport.serial.Serial")
def test_open_and_close(mock_serial: MagicMock) -> None:
    connection = MagicMock()
    connection.is_open = True
    mock_serial.return_value = connection

    transport = SerialTransport("/dev/ttyUSB0")

    transport.open()

    assert transport.is_open is True

    transport.close()

    connection.close.assert_called_once()
    assert transport.is_open is False


@patch("t3diag.transports.serial_transport.serial.Serial")
def test_write(mock_serial: MagicMock) -> None:
    connection = MagicMock()
    connection.is_open = True
    connection.write.return_value = 3
    mock_serial.return_value = connection

    transport = SerialTransport("/dev/ttyUSB0")
    transport.open()

    written = transport.write(b"\x01\x02\x03")

    assert written == 3
    connection.write.assert_called_once_with(b"\x01\x02\x03")


@patch("t3diag.transports.serial_transport.serial.Serial")
def test_read(mock_serial: MagicMock) -> None:
    connection = MagicMock()
    connection.is_open = True
    connection.read.return_value = b"\x55\xaa"
    mock_serial.return_value = connection

    transport = SerialTransport("/dev/ttyUSB0")
    transport.open()

    result = transport.read(2)

    assert result == b"\x55\xaa"
    connection.read.assert_called_once_with(2)


def test_read_rejects_invalid_size() -> None:
    transport = SerialTransport("/dev/ttyUSB0")

    with pytest.raises(ValueError, match="mindestens 1"):
        transport.read(0)


def test_write_requires_open_connection() -> None:
    transport = SerialTransport("/dev/ttyUSB0")

    with pytest.raises(SerialTransportError, match="nicht geöffnet"):
        transport.write(b"\x01")


@patch("t3diag.transports.serial_transport.serial.Serial")
def test_buffer_operations(mock_serial: MagicMock) -> None:
    connection = MagicMock()
    connection.is_open = True
    mock_serial.return_value = connection

    transport = SerialTransport("/dev/ttyUSB0")
    transport.open()

    transport.flush()
    transport.reset_input_buffer()
    transport.reset_output_buffer()

    connection.flush.assert_called_once()
    connection.reset_input_buffer.assert_called_once()
    connection.reset_output_buffer.assert_called_once()
