"""Modbus RTU power meter on RS-485."""
from scadable import Device, modbus_rtu, every, Register, SECONDS

class PowerMeter(Device):
    id = "power-meter"
    name = "Main panel meter"

    connection = modbus_rtu(port="/dev/ttyUSB0", baud=9600, slave=1)
    poll = every(10, SECONDS)

    registers = [
        Register(30001, "voltage",   unit="V",   scale=0.1),
        Register(30002, "current",   unit="A",   scale=0.01),
        Register(30003, "power",     unit="kW",  scale=0.001),
        Register(30004, "energy",    unit="kWh"),
    ]
