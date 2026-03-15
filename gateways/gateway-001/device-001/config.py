from scadable.edge import Device, ModbusConnection
from scadable.edge.constants import MODBUS_TCP, FIVE_SEC
from dataclasses import dataclass

@dataclass
class Connection(ModbusConnection):
    host: str = "${DEVICE_HOST}"
    port: int = 502
    slave_id: int = 1

class MainPLC(Device):
    id = "device-001"
    protocol = MODBUS_TCP
    connection = Connection
    frequency = FIVE_SEC
