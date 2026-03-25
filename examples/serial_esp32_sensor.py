"""
Example: Serial — ESP32 Sensor Hub

Receives structured sensor data from an ESP32 connected via USB.
The ESP32 reads multiple sensors (temperature, humidity, GPS, etc.)
and sends JSON-framed data over UART.
"""
from scadable.edge import Device, SerialDeviceConnection
from scadable.edge.constants import SERIAL, FIVE_SEC
from dataclasses import dataclass


@dataclass
class Connection(SerialDeviceConnection):
    serial_port: str = "/dev/ttyACM0"  # ESP32-S3 native USB shows up here
    baudrate: int = 115200
    parity: str = "N"
    stopbits: int = 1
    bytesize: int = 8


class Esp32SensorHub(Device):
    id = "esp32-sensors"
    protocol = SERIAL
    connection = Connection
    frequency = FIVE_SEC
    filter = ["temperature", "humidity"]  # only forward these fields
