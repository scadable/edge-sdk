"""Modbus TCP temperature and pressure sensor."""
from scadable import Device, modbus_tcp, every, Register, Historian, SECONDS, MINUTES

class TempPressureSensor(Device):
    id = "line1-temp-pressure"
    name = "Main line sensor"

    connection = modbus_tcp(host="${SENSOR_HOST}", port=502, slave=1)
    poll = every(5, SECONDS)

    registers = [
        Register(40001, "temperature", unit="°C", scale=0.1),
        Register(40002, "pressure",    unit="bar", scale=0.01),
        Register(40003, "flow_rate",   unit="L/min", scale=0.1),
    ]

    # Store temperature and pressure every 5 minutes (flow_rate not stored)
    historian = Historian(
        fields=["temperature", "pressure"],
        interval=every(5, MINUTES),
    )
