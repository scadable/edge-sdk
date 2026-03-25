"""OPC-UA connection to Ignition SCADA."""
from scadable import Device, opcua, every, SECONDS

class IgnitionSCADA(Device):
    id = "ignition-scada"
    name = "Ignition gateway"

    connection = opcua(
        host="${IGNITION_HOST}",
        port=4840,
        nodes=[
            ("temperature", "ns=2;s=Tank/Temperature"),
            ("pressure",    "ns=2;s=Tank/Pressure"),
            ("level",       "ns=2;s=Tank/Level"),
            ("pump_status", "ns=2;s=Pump/Status"),
            ("pump_speed",  "ns=2;s=Pump/Speed"),
        ]
    )
    poll = every(5, SECONDS)
