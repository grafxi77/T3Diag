"""Exceptions raised by the K-Line transport layer."""


class KLineError(Exception):
    """Base exception for all K-Line transport errors."""


class KLineConnectionError(KLineError):
    """Raised when the K-Line connection cannot be opened or used."""


class KLineTimeoutError(KLineError):
    """Raised when a K-Line operation exceeds the configured timeout."""


class KLineInitializationError(KLineError):
    """Raised when K-Line initialization fails."""
