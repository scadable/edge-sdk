from dataclasses import dataclass
from .base import Protocol, TCPConnection, SerialConnection


# Docs: https://docs.scadable.com/docs/edge/protocols#modbus-tcp
@dataclass
class ModbusTCPConnection(TCPConnection):
    """
    Modbus TCP connection settings.

    Attributes:
        host: IP address or hostname of the Modbus device.
        port: TCP port number (default: 502).
        slave_id: Modbus slave/unit ID (1-247).
        timeout: Read timeout in seconds.
        retries: Number of retry attempts on failure.
    """
    host: str = ""
    port: int = 502
    slave_id: int = 1


# Docs: https://docs.scadable.com/docs/edge/protocols#modbus-rtu
@dataclass
class ModbusRTUConnection(SerialConnection):
    """
    Modbus RTU (serial) connection settings.

    Attributes:
        serial_port: Serial port path (e.g. "/dev/ttyUSB0", "COM3").
        slave_id: Modbus slave/unit ID (1-247).
        baudrate: Serial baud rate (common: 9600, 19200, 115200).
        parity: Parity bit — "N" (none), "E" (even), "O" (odd).
        stopbits: Number of stop bits (1 or 2).
        bytesize: Data bits per byte (typically 8).
    """
    serial_port: str = "/dev/ttyUSB0"
    slave_id: int = 1
    baudrate: int = 9600
    parity: str = "N"
    stopbits: int = 1
    bytesize: int = 8


class ModbusProtocol(Protocol):
    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError
