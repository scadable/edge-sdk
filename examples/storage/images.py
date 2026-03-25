"""File storage for camera images."""
from scadable import FileStorage, GB_1

class CameraImages(FileStorage):
    id = "camera-images"
    path = "/var/data/images"
    max_size = GB_1
    warn_at = 80
