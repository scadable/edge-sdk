from ..device import Device
from ..storage.base import Storage


# Docs: https://docs.scadable.com/docs/edge/outbound
class Outbound:
    """
    Base class for all outbound destinations.

    Outbounds define where device data goes. All outbounds are
    Scadable-managed — the system handles endpoints, credentials,
    and routing automatically.

    Attributes:
        id: Unique identifier for this outbound.
        devices: List of Device subclasses to route to this outbound.
                 Empty list = all devices (broadcast).
    """

    id: str = None
    devices: list = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__name__ in ("Outbound", "OutboundData", "OutboundUpload"):
            return
        errors = []
        if not cls.id:
            errors.append(f"Outbound '{cls.__name__}' must define 'id'")
        if not isinstance(cls.devices, list):
            errors.append(f"Outbound '{cls.__name__}' — devices must be a list")
        else:
            for i, dev in enumerate(cls.devices):
                if not (isinstance(dev, type) and issubclass(dev, Device)):
                    errors.append(
                        f"Outbound '{cls.__name__}' — devices[{i}] must be a Device subclass, "
                        f"got {dev!r}"
                    )
        # OutboundUpload: validate storage reference
        storage_ref = getattr(cls, "storage", None)
        if storage_ref is not None and not (isinstance(storage_ref, type) and issubclass(storage_ref, Storage)):
            errors.append(
                f"Outbound '{cls.__name__}' — storage must be a Storage subclass, "
                f"got {storage_ref!r}"
            )
        if errors:
            raise TypeError("\n".join(errors))

    def __repr__(self):
        dev_names = [d.__name__ for d in self.devices] if self.devices else ["all"]
        return f"<{self.__class__.__name__} id={self.id!r} devices={dev_names}>"


# Docs: https://docs.scadable.com/docs/edge/outbound#outbounddata
class OutboundData(Outbound):
    """
    Scadable-managed data outbound (MQTT telemetry stream).

    Sends structured device data (Modbus registers, OPC-UA node values,
    sensor readings) to the Scadable cloud. The system handles MQTT
    endpoint, certificates, and topic routing automatically.

    Usage:
        class DefaultTelemetry(OutboundData):
            id = "default-telemetry"
            devices = [MyPlc, IgnitionServer]  # empty = all devices
    """

    id: str = None
    devices: list = []


# Docs: https://docs.scadable.com/docs/edge/outbound#outboundupload
class OutboundUpload(Outbound):
    """
    Scadable-managed upload outbound (S3 file upload).

    Uploads files (images, binary data) from a local storage to the
    Scadable cloud. The system handles S3 bucket, presigned URLs,
    retry logic, and retention automatically.

    Attributes:
        storage: A Storage subclass to read files from. The outbound
                 watches this storage and uploads new files automatically.
                 Set to None if files are sent directly (not via storage).

    Usage:
        class ImageUpload(OutboundUpload):
            id = "image-upload"
            devices = [Esp32Camera]
            storage = ImageStore  # reads from this FileStorage
    """

    id: str = None
    devices: list = []
    storage = None  # Storage subclass reference (optional)
