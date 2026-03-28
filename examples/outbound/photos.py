"""S3 outbound for high-temperature photos."""
from scadable import S3Outbound

from examples.devices.factory_camera import FactoryCamera
from examples.storage.images import CameraImages

class HighTempPhotos(S3Outbound):
    id = "high-temp-photos"
    devices = [FactoryCamera]
    storage = CameraImages
    prefix = "images/{date}/{device_id}/"
    max_age = "30d"
