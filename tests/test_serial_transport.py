"""Unit-Tests für die serielle Transportschicht."""

from unittest.mock import MagicMock, patch

import pytest

from t3diag.transports.serial_transport import (
    SerialTransport,
    SerialTransportError,
    SerialTransportTimeoutError,
)


@patch("t3diag.transports.serial_transport.serial.Serial")
def test_open_and_close(mock_serial: MagicMock) -> None:
    """Testet das Öffnen und Schließen der seriellen Verbindung."""
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
    """Testet das Schreiben von Bytes."""
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
    """Testet das Lesen von Bytes."""
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
    """read() lehnt ungültige Größen ab."""
    transport = SerialTransport("/dev/ttyUSB0")

    with pytest.raises(ValueError, match="mindestens 1"):
        transport.read(0)


def test_write_requires_open_connection() -> None:
    """write() benötigt eine geöffnete Verbindung."""
    transport = SerialTransport("/dev/ttyUSB0")

    with pytest.raises(SerialTransportError, match="nicht geöffnet"):
        transport.write(b"\x01")


@patch("t3diag.transports.serial_transport.serial.Serial")
def test_buffer_operations(mock_serial: MagicMock) -> None:
    """Testet Flush und Buffer-Funktionen."""
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


@patch("t3diag.transports.serial_transport.serial.Serial")
def test_read_exact(mock_serial: MagicMock) -> None:
    """Testet das Lesen einer exakten Anzahl Bytes."""
    connection = MagicMock()
    connection.is_open = True
    connection.read.side_effect = [b"\x01", b"\x02\x03"]
    mock_serial.return_value = connection

    transport = SerialTransport("/dev/ttyUSB0")
    transport.open()

    result = transport.read_exact(3)

    assert result == b"\x01\x02\x03"
    assert connection.read.call_count == 2


@patch("t3diag.transports.serial_transport.serial.Serial")
def test_read_exact_timeout(mock_serial: MagicMock) -> None:
    """Testet Timeout bei unvollständigen Daten."""
    connection = MagicMock()
    connection.is_open = True
    connection.read.side_effect = [b"\x01", b""]
    mock_serial.return_value = connection

    transport = SerialTransport("/dev/ttyUSB0")
    transport.open()

    with pytest.raises(
        SerialTransportTimeoutError,
        match="1 von 2 Bytes",
    ):
        transport.read_exact(2)


def test_read_exact_rejects_invalid_size() -> None:
    """read_exact() lehnt ungültige Größen ab."""
    transport = SerialTransport("/dev/ttyUSB0")

    with pytest.raises(ValueError, match="mindestens 1"):
        transport.read_exact(0)
