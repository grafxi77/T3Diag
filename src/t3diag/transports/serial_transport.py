"""Serielle Transportschicht für T3Diag."""

from __future__ import annotations

import serial
from serial import SerialException


class SerialTransportError(Exception):
    """Basisklasse für Fehler der seriellen Transportschicht."""


class SerialTransportTimeoutError(SerialTransportError):
    """Timeout beim Lesen serieller Daten."""


class SerialTransport:
    """Abstraktion einer seriellen Verbindung.

    Diese Klasse kennt weder K-Line noch KWP1281.
    """

    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        timeout: float = 1.0,
    ) -> None:
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._connection: serial.Serial | None = None

    @property
    def port(self) -> str:
        """Gibt den Gerätenamen zurück."""
        return self._port

    @property
    def is_open(self) -> bool:
        """Gibt an, ob der Port geöffnet ist."""
        return self._connection is not None and self._connection.is_open

    def open(self) -> None:
        """Öffnet den seriellen Port."""
        if self.is_open:
            return

        try:
            self._connection = serial.Serial(
                port=self._port,
                baudrate=self._baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self._timeout,
                write_timeout=self._timeout,
            )
        except SerialException as error:
            self._connection = None
            raise SerialTransportError(
                f"Port {self._port} konnte nicht geöffnet werden."
            ) from error

    def close(self) -> None:
        """Schließt den seriellen Port."""
        if self._connection is None:
            return

        try:
            self._connection.close()
        except SerialException as error:
            raise SerialTransportError(
                f"Port {self._port} konnte nicht geschlossen werden."
            ) from error
        finally:
            self._connection = None

    def write(self, data: bytes) -> int:
        """Schreibt Bytes auf die Schnittstelle."""
        connection = self._require_connection()

        try:
            written = connection.write(data)

            if written is None:
                raise SerialTransportError(
                    "pySerial lieferte keine Anzahl geschriebener Bytes."
                )

            return written

        except SerialException as error:
            raise SerialTransportError(
                f"Schreiben auf {self._port} fehlgeschlagen."
            ) from error

    def read(self, size: int = 1) -> bytes:
        """Liest bis zu size Bytes."""
        if size < 1:
            raise ValueError("size muss mindestens 1 sein.")

        connection = self._require_connection()

        try:
            data = connection.read(size)
        except SerialException as error:
            raise SerialTransportError(
                f"Lesen von {self._port} fehlgeschlagen."
            ) from error

        return bytes(data)

    def read_exact(self, size: int) -> bytes:
        """Liest exakt size Bytes oder löst einen Timeout aus."""
        if size < 1:
            raise ValueError("size muss mindestens 1 sein.")

        received = bytearray()

        while len(received) < size:
            chunk = self.read(size - len(received))

            if not chunk:
                raise SerialTransportTimeoutError(
                    f"Timeout: {len(received)} von {size} Bytes empfangen."
                )

            received.extend(chunk)

        return bytes(received)

    def flush(self) -> None:
        """Wartet, bis alle Daten übertragen wurden."""
        self._require_connection().flush()

    def reset_input_buffer(self) -> None:
        """Leert den Eingabepuffer."""
        self._require_connection().reset_input_buffer()

    def reset_output_buffer(self) -> None:
        """Leert den Ausgabepuffer."""
        self._require_connection().reset_output_buffer()

    def set_break(self, enabled: bool) -> None:
        """Aktiviert oder deaktiviert den BREAK-Zustand."""
        connection = self._require_connection()
        connection.break_condition = enabled

    def _require_connection(self) -> serial.Serial:
        """Gibt eine geöffnete Verbindung zurück."""
        if self._connection is None or not self._connection.is_open:
            raise SerialTransportError(f"Port {self._port} ist nicht geöffnet.")

        return self._connection

    def __enter__(self) -> SerialTransport:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: object,
        exc_value: object,
        traceback: object,
    ) -> None:
        self.close()
