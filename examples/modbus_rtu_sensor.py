"""
Example: Modbus RTU Sensor

Reads data from a sensor connected via RS-485 serial.
Common for: temperature/humidity sensors, energy meters, flow meters.
"""
from scadable.edge import Device, ModbusRTUConnection
from scadable.edge.constants import MODBUS_RTU, TEN_SEC
from dataclasses import dataclass


@dataclass
class Connection(ModbusRTUConnection):
    serial_port: str = "/dev/ttyUSB0"
    slave_id: int = 1
    baudrate: int = 9600
    parity: str = "N"
    stopbits: int = 1
    bytesize: int = 8


class TempSensor(Device):
    id = "temp-sensor"
    protocol = MODBUS_RTU
    connection = Connection
    frequency = TEN_SEC
    filter = ["reg_0", "reg_1"]  # only read temperature and humidity registers
