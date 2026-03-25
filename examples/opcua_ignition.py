"""
Example: OPC-UA — Ignition SCADA Server

Reads tag values from an Ignition gateway via OPC-UA.
Works with: Ignition, Kepware, Siemens WinCC, Beckhoff TwinCAT, Prosys.

OPC-UA data is already named and typed — no decode() needed
unless you want to rename fields or convert units.
"""
from scadable.edge import Device, OPCUAConnection
from scadable.edge.constants import OPCUA, FIVE_SEC
from dataclasses import dataclass, field
from typing import List


@dataclass
class Connection(OPCUAConnection):
    host: str = "192.168.1.50"
    port: int = 4840
    node_ids: List[str] = field(default_factory=lambda: [
        "ns=2;s=Tank/Temperature",
        "ns=2;s=Tank/Pressure",
        "ns=2;s=Tank/Level",
        "ns=2;s=Pump/Speed",
        "ns=2;s=Pump/Status",
    ])
    security_policy: str = "None"
    username: str = ""
    password: str = ""


class IgnitionServer(Device):
    id = "ignition-server"
    protocol = OPCUA
    connection = Connection
    frequency = FIVE_SEC
    filter = []

    # No decode() needed — OPC-UA nodes are already named:
    # {"Tank/Temperature": 23.5, "Tank/Pressure": 101.3, ...}
    #
    # But you CAN add one to rename or convert:
    #
    # def decode(self, raw: dict) -> dict:
    #     p = raw["payload"]
    #     return {
    #         "temp_celsius": p.get("Tank/Temperature", 0),
    #         "temp_fahrenheit": p.get("Tank/Temperature", 0) * 9/5 + 32,
    #         "pressure_psi": p.get("Tank/Pressure", 0) * 14.696,
    #     }
