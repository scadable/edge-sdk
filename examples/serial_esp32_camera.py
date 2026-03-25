"""
Example: Serial — ESP32 Camera with decode

Receives complete image frames from an ESP32-CAM over USB serial.
The ESP32 reassembles chunks from ESP-NOW and sends complete frames.

decode() filters image frames and passes them to the outbound.
The OutboundUpload handles storage and S3 upload automatically.

Flow: ESP32-CAM → ESP-NOW LR → ESP32 Bridge → USB serial → Pi → decode → outbound → S3
"""
from scadable.edge import Device, SerialDeviceConnection
from scadable.edge.constants import SERIAL, ONE_SEC
from dataclasses import dataclass


@dataclass
class Connection(SerialDeviceConnection):
    serial_port: str = "/dev/ttyUSB0"
    baudrate: int = 921600


class Esp32Camera(Device):
    id = "esp32-cam-01"
    protocol = SERIAL
    connection = Connection
    frequency = ONE_SEC
    filter = []

    def decode(self, raw: dict):
        """
        Raw payload from serial driver:
            {
                "frame_type": 1,          # 1=image, 2=telemetry, 3=event
                "content_type": "jpeg",
                "data": <bytes>,
                "size": 102400,
            }

        For image frames: return the image data — outbound uploads it.
        For non-image frames: return None to drop.
        """
        payload = raw["payload"]

        if payload.get("frame_type") != 1:
            return None  # drop non-image frames

        return {
            "type": "image",
            "content_type": "image/jpeg",
            "data": payload["data"],
        }
