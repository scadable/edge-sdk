"""OPC-UA connection to Ignition SCADA server."""
from scadable import Device, opcua, every, Node, SECONDS, SECURITY_NONE


class IgnitionSCADA(Device):
    id = "ignition-scada"
    name = "Ignition SCADA server"
    connection = opcua(
        host="${OPCUA_HOST}",
        port=4840,
        security=SECURITY_NONE,
        nodes=[
            Node("temperature", namespace=2, path="Tank/Temperature"),
            Node("pressure", namespace=2, path="Tank/Pressure"),
            Node("level", namespace=2, path="Tank/Level"),
            Node("pump_status", namespace=2, path="Pump/Status"),
            Node("pump_speed", namespace=2, identifier=1001),
        ],
    )
    poll = every(5, SECONDS)
