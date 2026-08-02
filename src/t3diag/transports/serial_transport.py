"""Serielle Transportschicht für T3Diag."""

from __future__ import annotations

import serial
from serial import SerialException


class SerialTransportError(Exception):
    """Fehler innerhalb der seriellen Transportschicht."""


class SerialTransport:
    """Verwaltet eine serielle Verbindung.

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
        """Gibt den konfigurierten Gerätenamen zurück."""
        return self._port

    @property
    def is_open(self) -> bool:
        """Gibt an, ob die Schnittstelle geöffnet ist."""
        return self._connection is not None and self._connection.is_open

    def open(self) -> None:
        """Öffnet die serielle Schnittstelle."""
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
                f"Serieller Port {self._port} konnte nicht geöffnet werden"
            ) from error

    def close(self) -> None:
        """Schließt die serielle Schnittstelle."""
        if self._connection is None:
            return

        try:
            self._connection.close()
        except SerialException as error:
            raise SerialTransportError(
                f"Serieller Port {self._port} konnte nicht geschlossen werden"
            ) from error
        finally:
            self._connection = None

    def write(self, data: bytes) -> int:
        """Schreibt Bytes auf die serielle Schnittstelle."""
        connection = self._require_connection()

        try:
            written = connection.write(data)

            if written is None:
                raise SerialTransportError(
                    f"Schreiben auf {self._port} lieferte kein Ergebnis"
                )

            return written

        except SerialException as error:
            raise SerialTransportError(
                f"Schreiben auf {self._port} fehlgeschlagen"
            ) from error

    def read(self, size: int = 1) -> bytes:
        """Liest eine festgelegte Anzahl Bytes."""
        if size < 1:
            raise ValueError("size muss mindestens 1 sein")

        connection = self._require_connection()

        try:
            return connection.read(size)
        except SerialException as error:
            raise SerialTransportError(
                f"Lesen von {self._port} fehlgeschlagen"
            ) from error

    def flush(self) -> None:
        """Wartet, bis ausstehende Schreibdaten übertragen wurden."""
        connection = self._require_connection()

        try:
            connection.flush()
        except SerialException as error:
            raise SerialTransportError(
                f"Flush auf {self._port} fehlgeschlagen"
            ) from error

    def reset_input_buffer(self) -> None:
        """Verwirft ungelesene Eingangsdaten."""
        connection = self._require_connection()

        try:
            connection.reset_input_buffer()
        except SerialException as error:
            raise SerialTransportError(
                f"Eingangspuffer von {self._port} konnte nicht geleert werden"
            ) from error

    def reset_output_buffer(self) -> None:
        """Verwirft noch nicht übertragene Ausgangsdaten."""
        connection = self._require_connection()

        try:
            connection.reset_output_buffer()
        except SerialException as error:
            raise SerialTransportError(
                f"Ausgangspuffer von {self._port} konnte nicht geleert werden"
            ) from error

    def _require_connection(self) -> serial.Serial:
        """Gibt die offene Verbindung zurück."""
        if self._connection is None or not self._connection.is_open:
            raise SerialTransportError(
                f"Serieller Port {self._port} ist nicht geöffnet"
            )

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
