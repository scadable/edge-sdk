"""
Example: OPC-UA — Ignition SCADA Server

Reads tag values from an Ignition gateway via OPC-UA.
Works with: Ignition, Kepware, Siemens WinCC, Beckhoff TwinCAT, Prosys.
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
    security_policy: str = "None"  # or "Basic256Sha256" for encrypted
    username: str = ""             # leave empty for anonymous
    password: str = ""


class IgnitionServer(Device):
    id = "ignition-server"
    protocol = OPCUA
    connection = Connection
    frequency = FIVE_SEC
    filter = []  # read all configured node_ids
