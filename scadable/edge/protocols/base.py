from abc import ABC, abstractmethod
from dataclasses import dataclass


class Protocol(ABC):
    @abstractmethod
    def read(self, *args, **kwargs):
        pass

    @abstractmethod
    def write(self, *args, **kwargs):
        pass


# ─── Base Connection Types ───────────────────────────────────────────────────


@dataclass
class TCPConnection:
    """
    Base class for TCP-based protocol connections.
    """
    host: str = ""
    port: int = 0
    timeout: float = 5.0
    retries: int = 3


@dataclass
class SerialConnection:
    """
    Base class for serial/UART-based protocol connections.
    """
    serial_port: str = "/dev/ttyUSB0"
    baudrate: int = 9600
    parity: str = "N"      # N=none, E=even, O=odd
    stopbits: int = 1
    bytesize: int = 8
    timeout: float = 5.0
    retries: int = 3
