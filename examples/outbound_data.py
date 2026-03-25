"""
Example: Data outbound — stream telemetry to Scadable cloud

Sends structured device data (Modbus registers, OPC-UA node values,
sensor readings) via MQTT. The system handles endpoint, certificates,
and topic routing automatically. Zero configuration needed.
"""
from scadable.edge import OutboundData, Device
from scadable.edge.constants import MODBUS_TCP, FIVE_SEC


# ── Example device (normally imported from devices/ folder) ───────────────────

class MyPlc(Device):
    id = "my-plc"
    protocol = MODBUS_TCP
    connection = type("C", (), {"host": "192.168.1.100", "port": 502})
    frequency = FIVE_SEC


# ── Outbound definition ──────────────────────────────────────────────────────

class DefaultTelemetry(OutboundData):
    id = "default-telemetry"
    devices = [MyPlc]       # only this device's data goes here
    # devices = []          # uncomment for all devices (broadcast)
