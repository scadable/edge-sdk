from dataclasses import dataclass
from .base import Protocol, SerialConnection


# Docs: https://docs.scadable.com/docs/edge/protocols#serial
@dataclass
class SerialDeviceConnection(SerialConnection):
    """
    Generic serial/UART device connection settings.

    Connects to any serial device (ESP32, Arduino, sensors, etc.)
    over USB or hardware UART.

    Attributes:
        serial_port: Serial port path (e.g. "/dev/ttyUSB0", "/dev/ttyACM0", "COM3").
        baudrate: Serial baud rate. Common values:
                  115200 (default for most devices),
                  921600 (fast, for image transfer),
                  9600 (legacy sensors).
        parity: Parity bit — "N" (none), "E" (even), "O" (odd).
        stopbits: Number of stop bits (1 or 2).
        bytesize: Data bits per byte (typically 8).
        timeout: Read timeout in seconds.
        retries: Number of retry attempts on failure.
    """
    serial_port: str = "/dev/ttyUSB0"
    baudrate: int = 115200
    parity: str = "N"
    stopbits: int = 1
    bytesize: int = 8


class SerialProtocol(Protocol):
    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError
