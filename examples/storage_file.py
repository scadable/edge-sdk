"""
Example: File-based local storage

Stores blobs (images, binary data, files) on disk.
Each partition gets its own subdirectory — data is isolated.
Oldest files are evicted when max_size is reached.
A warning is logged when usage exceeds warning_threshold%.
"""
from scadable.edge import FileStorage
from scadable.edge.constants import SIZE_1_GB


class ImageStore(FileStorage):
    id = "image-store"
    path = "/var/scadable/storage/image-store"
    max_size = SIZE_1_GB
    warning_threshold = 80  # warn at 80% full


# Usage in a decoder or controller:
#
#   store = ImageStore()
#
#   # Partitions keep data isolated
#   images = store.partition("camera")
#   cache  = store.partition("thumbnails")
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
#   keys = images.list()            # ["frame-001", "frame-002", ...]
#   keys = images.list(limit=10)    # first 10
#   keys = images.list(prefix="frame-00")  # filtered
#
#   # Check existence
#   if images.exists("frame-001"):
#       print("Image found")
#
#   # Delete
#   images.delete("frame-001")
