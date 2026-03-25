"""
Example: File-based local storage

Stores data as files on disk. Each partition gets its own subdirectory.
Good for: images, binary blobs, large payloads.
"""
from scadable.edge import FileStorage
from scadable.edge.constants import SIZE_1_GB


class ImageStore(FileStorage):
    id = "image-store"
    path = "/var/scadable/storage/image-store"
    max_size = SIZE_1_GB


# Usage in a decoder or controller (executed by edge-main runtime):
#
#   store = storage("image-store")
#
#   # Partitions keep data isolated
#   images = store.partition("camera")
#   cache  = store.partition("decoder")
#
#   # Write an image
#   images.write("frame-001", jpeg_bytes, metadata={
#       "device_id": "esp32-cam-01",
#       "content_type": "image/jpeg",
#       "resolution": "640x480",
#   })
#
#   # Read it back
#   data = images.read("frame-001")
#   meta = images.metadata("frame-001")
#
#   # List all images
#   keys = images.list()          # ["frame-001", "frame-002", ...]
#   keys = images.list(limit=10)  # first 10
#
#   # Delete
#   images.delete("frame-001")
