from dataclasses import dataclass, field
from typing import List, Optional
from .base import Protocol, TCPConnection


@dataclass
class OPCUAConnection(TCPConnection):
    """
    OPC-UA client connection settings.

    Connects to an OPC-UA server (Ignition, Kepware, Siemens, etc.)
    and reads the specified node values.

    Attributes:
        host: OPC-UA server hostname or IP address.
        port: OPC-UA server port (default: 4840).
        node_ids: List of OPC-UA node IDs to read.
                  String format: "ns=2;s=Temperature"
                  Numeric format: "ns=2;i=1001"
        security_policy: OPC-UA security policy.
                         "None", "Basic256Sha256", "Basic128Rsa15".
        username: Username for authentication (leave empty for anonymous).
        password: Password for authentication.
        timeout: Connection timeout in seconds.
        retries: Number of retry attempts on failure.
    """
    host: str = ""
    port: int = 4840
    node_ids: List[str] = field(default_factory=list)
    security_policy: str = "None"
    username: str = ""
    password: str = ""


class OPCUAProtocol(Protocol):
    def read(self, *args, **kwargs):
        raise NotImplementedError

    def write(self, *args, **kwargs):
        raise NotImplementedError
