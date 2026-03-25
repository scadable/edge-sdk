"""
Example: Modbus TCP PLC

Reads holding registers from a PLC over Modbus TCP.
Common for: Siemens, Allen-Bradley, Schneider PLCs, power meters, VFDs.
"""
from scadable.edge import Device, ModbusTCPConnection
from scadable.edge.constants import MODBUS_TCP, FIVE_SEC
from dataclasses import dataclass


@dataclass
class Connection(ModbusTCPConnection):
    host: str = "192.168.1.100"
    port: int = 502
    slave_id: int = 1


class MainPLC(Device):
    id = "main-plc"
    protocol = MODBUS_TCP
    connection = Connection
    frequency = FIVE_SEC
    filter = []  # pull all registers
