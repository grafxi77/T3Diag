"""K-Line transport interface."""

from __future__ import annotations

from t3diag.kline.exceptions import (
    KLineConnectionError,
    KLineTimeoutError,
)
from t3diag.transports.serial_transport import (
    SerialTransport,
    SerialTransportError,
    SerialTransportTimeoutError,
)


class KLineTransport:
    """K-Line communication layer above SerialTransport."""

    def __init__(self, serial_transport: SerialTransport) -> None:
        """Create a K-Line transport."""
        self._serial_transport = serial_transport

    @property
    def serial_transport(self) -> SerialTransport:
        """Return the underlying serial transport."""
        return self._serial_transport

    @property
    def is_open(self) -> bool:
        """Return whether the transport is open."""
        return self._serial_transport.is_open

    def open(self) -> None:
        """Open the K-Line transport."""
        try:
            self._serial_transport.open()
        except SerialTransportError as error:
            raise KLineConnectionError(
                "K-Line transport could not be opened."
            ) from error

    def close(self) -> None:
        """Close the K-Line transport."""
        try:
            self._serial_transport.close()
        except SerialTransportError as error:
            raise KLineConnectionError(
                "K-Line transport could not be closed."
            ) from error

    def send(self, data: bytes) -> None:
        """Send raw bytes."""
        try:
            self._serial_transport.write(data)
        except SerialTransportError as error:
            raise KLineConnectionError("K-Line data could not be sent.") from error

    def receive(self, size: int) -> bytes:
        """Receive up to the requested number of bytes."""
        try:
            return self._serial_transport.read(size)
        except SerialTransportError as error:
            raise KLineConnectionError("K-Line data could not be received.") from error

    def receive_exact(self, size: int) -> bytes:
        """Receive exactly the requested number of bytes."""
        try:
            return self._serial_transport.read_exact(size)
        except SerialTransportTimeoutError as error:
            raise KLineTimeoutError("K-Line receive operation timed out.") from error
        except SerialTransportError as error:
            raise KLineConnectionError("K-Line data could not be received.") from error

    def flush(self) -> None:
        """Flush pending data and reset buffers."""
        try:
            self._serial_transport.flush()
            self._serial_transport.reset_input_buffer()
            self._serial_transport.reset_output_buffer()
        except SerialTransportError as error:
            raise KLineConnectionError(
                "K-Line buffers could not be flushed."
            ) from error

    def initialize_5_baud(self, address: int) -> None:
        """Perform the future 5-baud initialization."""
        raise NotImplementedError
