"""
Example: Serial — ESP32 Camera

Receives images from an ESP32-CAM connected via USB serial.
The ESP32 sends framed binary data (images) over UART.

Flow: ESP32-CAM → ESP-NOW LR → ESP32 Bridge → USB → Pi → Scadable Cloud
"""
from scadable.edge import Device, SerialDeviceConnection
from scadable.edge.constants import SERIAL, ONE_SEC
from dataclasses import dataclass


@dataclass
class Connection(SerialDeviceConnection):
    serial_port: str = "/dev/ttyUSB0"  # CP2102/CH340 shows up here
    baudrate: int = 921600             # fast baud for image transfer
    parity: str = "N"
    stopbits: int = 1
    bytesize: int = 8


class Esp32Camera(Device):
    id = "esp32-cam-01"
    protocol = SERIAL
    connection = Connection
    frequency = ONE_SEC  # real-time — process frames as they arrive
    filter = []          # forward all data
