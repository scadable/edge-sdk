"""MQTT outbound for all sensor telemetry."""
from scadable import MQTTOutbound

class SensorData(MQTTOutbound):
    id = "sensor-data"
    devices = []  # all devices
