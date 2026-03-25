"""
Example: OPC-UA — Kepware Server with Authentication

Reads tags from a Kepware KEPServerEX with username/password authentication
and Basic256Sha256 security.
"""
from scadable.edge import Device, OPCUAConnection
from scadable.edge.constants import OPCUA, ONE_SEC
from dataclasses import dataclass, field
from typing import List


@dataclass
class Connection(OPCUAConnection):
    host: str = "10.0.1.100"
    port: int = 49320              # Kepware default OPC-UA port
    node_ids: List[str] = field(default_factory=lambda: [
        "ns=2;s=Channel1.Device1.Tag1",
        "ns=2;s=Channel1.Device1.Tag2",
        "ns=2;s=Channel1.Device1.Tag3",
    ])
    security_policy: str = "Basic256Sha256"
    username: str = "opcua_user"
    password: str = "${KEPWARE_PASSWORD}"  # env var injection


class KepwareServer(Device):
    id = "kepware-plc"
    protocol = OPCUA
    connection = Connection
    frequency = ONE_SEC
    filter = []
