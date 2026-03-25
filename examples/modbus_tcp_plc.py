"""
Example: Modbus TCP PLC with decode/encode

Reads holding registers from a PLC over Modbus TCP.
decode() converts raw register values to meaningful data.
encode() converts commands back to register values.
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
    filter = []

    def decode(self, raw: dict) -> dict:
        """
        Raw payload from driver:
            {"reg_0": 2350, "reg_1": 10130, "reg_2": 4200, "reg_3": 15678}

        Decoded output (forwarded to outbound):
            {"power_kw": 23.5, "voltage": 101.3, "current": 4.2, "energy_kwh": 15678}
        """
        regs = raw["payload"]
        return {
            "power_kw": regs.get("reg_0", 0) / 100.0,
            "voltage": regs.get("reg_1", 0) / 100.0,
            "current": regs.get("reg_2", 0) / 1000.0,
            "energy_kwh": regs.get("reg_3", 0),
        }

    def encode(self, command: dict) -> dict:
        """
        Command from API/controller:
            {"set_speed": 1500, "set_temp": 75.0}

        Encoded output (written to device registers):
            {"reg_10": 15000, "reg_11": 7500}
        """
        result = {}
        if "set_speed" in command:
            result["reg_10"] = int(command["set_speed"] * 10)
        if "set_temp" in command:
            result["reg_11"] = int(command["set_temp"] * 100)
        return result
