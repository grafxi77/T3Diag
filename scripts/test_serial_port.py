"""Hardwaretest für die serielle Transportschicht."""

from t3diag.transports.serial_transport import (
    SerialTransport,
    SerialTransportError,
)


def main() -> int:
    """Öffnet und schließt das USB-KKL-Interface."""
    transport = SerialTransport("/dev/ttyUSB0")

    try:
        with transport:
            print(f"Port geöffnet: {transport.port}")
            print(f"Portstatus: {transport.is_open}")

        print(f"Portstatus nach close: {transport.is_open}")
        return 0

    except SerialTransportError as error:
        print(f"Fehler: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
