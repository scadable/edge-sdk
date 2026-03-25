from .base import Storage, Partition


class FilePartition(Partition):
    """
    File-based partition. Each key is a file in a subdirectory.
    Metadata stored as JSON sidecar. Isolated from other partitions.

    On-disk structure (managed by runtime):
        {storage_path}/{partition}/{key}.dat
        {storage_path}/{partition}/{key}.meta.json
    """

    def write(self, key: str, data, metadata: dict = None) -> str:
        raise NotImplementedError("write() is executed by the edge-main runtime")

    def read(self, key: str) -> bytes:
        raise NotImplementedError("read() is executed by the edge-main runtime")

    def list(self, prefix: str = None, limit: int = None) -> list:
        raise NotImplementedError("list() is executed by the edge-main runtime")

    def delete(self, key: str):
        raise NotImplementedError("delete() is executed by the edge-main runtime")

    def exists(self, key: str) -> bool:
        raise NotImplementedError("exists() is executed by the edge-main runtime")

    def metadata(self, key: str) -> dict:
        raise NotImplementedError("metadata() is executed by the edge-main runtime")


# Docs: https://docs.scadable.com/docs/edge/storage#file-storage
class FileStorage(Storage):
    """
    File-based storage for blobs (images, binary data, raw files).

    Each partition is a subdirectory. Oldest files are evicted when
    max_size is reached. A warning is logged when usage exceeds
    warning_threshold % of max_size.

    Usage:
        class ImageStore(FileStorage):
            id = "image-store"
            path = "/var/scadable/storage/images"
            max_size = SIZE_1_GB
            warning_threshold = 80

        store = ImageStore()
        images = store.partition("camera")
        images.write("frame-001", jpeg_bytes, metadata={"type": "jpeg"})
        data = images.read("frame-001")
    """

    id: str = None
    path: str = None
    max_size: int = 512 * 1024 * 1024
    warning_threshold: int = 80

    def partition(self, name: str) -> FilePartition:
        raise NotImplementedError("partition() is executed by the edge-main runtime")
