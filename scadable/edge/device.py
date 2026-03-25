PAYLOAD_SCHEMA = {
    "device_id": str,
    "protocol": str,
    "timestamp": int,
    "payload": dict,
}


class Device:
    """
    Base class for all gateway devices.
    Subclass this in your config.py to define a device.

    Required class variables:
        id         — unique identifier for this device
        protocol   — use a constant from scadable.edge.constants
        connection — subclass of a connection class (ModbusTCPConnection, etc.)
        frequency  — polling interval in seconds, use constants: FIVE_SEC, TEN_SEC etc

    Optional class variables:
        filter     — list of field names to pull (empty = pull all)

    Optional methods:
        decode(raw) — transform incoming data before forwarding to outbound.
                      Return a dict to forward, or None to drop the message.
        encode(cmd) — transform outgoing commands before sending to device.
                      Return a dict of raw values to write to the device.

    If decode/encode are not overridden, data passes through unchanged.
    """

    id: str = None
    protocol: str = None
    connection = None
    frequency: int = 10
    filter: list = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__name__ == "Device":
            return
        errors = []
        if not cls.id:
            errors.append(f"Device subclass '{cls.__name__}' must define 'id'")
        if not cls.protocol:
            errors.append(f"Device subclass '{cls.__name__}' must define 'protocol'")
        if cls.connection is None:
            errors.append(f"Device subclass '{cls.__name__}' must define 'connection'")
        if errors:
            raise TypeError("\n".join(errors))

    def __repr__(self):
        return (
            f"<Device id={self.id!r} protocol={self.protocol!r} "
            f"connection={self.connection.__name__} frequency={self.frequency}s>"
        )

    def decode(self, raw: dict):
        """
        Transform incoming device data before forwarding to outbound.

        Override this to convert raw protocol data into meaningful values.
        If not overridden, raw data passes through unchanged.

        Args:
            raw: dict matching PAYLOAD_SCHEMA:
                 {
                     "device_id": "my-plc",
                     "protocol": "modbus-tcp",
                     "timestamp": 1711234567,
                     "payload": {"reg_0": 2350, "reg_1": 10130, ...}
                 }

        Returns:
            dict — transformed data, forwarded to outbound
            None — drop this message (don't forward)
        """
        return raw

    def encode(self, command: dict) -> dict:
        """
        Transform outgoing commands before sending to the device.

        Override this to convert meaningful commands into raw protocol values.
        If not overridden, commands pass through unchanged.

        Args:
            command: dict from the API or controller, e.g.:
                     {"set_speed": 1500, "set_temp": 75.0}

        Returns:
            dict — raw values to write to the device, e.g.:
                   {"reg_10": 15000, "reg_11": 7500}
        """
        return command
