"""
Example: Upload outbound — send files to Scadable cloud via S3

Uploads files (images, binary data) from a local FileStorage to the
Scadable cloud. The system handles S3 bucket, presigned URLs, retry
logic, and retention automatically. Zero configuration needed.
"""
from scadable.edge import OutboundUpload, FileStorage, Device
from scadable.edge.constants import SERIAL, ONE_SEC, SIZE_1_GB


# ── Example device (normally imported from devices/ folder) ───────────────────

class Esp32Camera(Device):
    id = "esp32-cam-01"
    protocol = SERIAL
    connection = type("C", (), {"serial_port": "/dev/ttyUSB0", "baudrate": 921600})
    frequency = ONE_SEC


# ── Example storage (normally imported from storage/ folder) ──────────────────

class ImageStore(FileStorage):
    id = "image-store"
    path = "/var/scadable/storage/images"
    max_size = SIZE_1_GB
    warning_threshold = 80


# ── Outbound definition ──────────────────────────────────────────────────────

class ImageUpload(OutboundUpload):
    id = "image-upload"
    devices = [Esp32Camera]     # only upload this device's files
    storage = ImageStore        # read files from this storage
