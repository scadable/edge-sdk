from .base import Storage, Partition


class FilePartition(Partition):
    """
    File-based partition. Each key is stored as a file in a subdirectory.
    Metadata is stored as a JSON sidecar file alongside the data.

    Structure on disk (managed by the runtime):
        {storage_path}/{partition_name}/{key}.dat
        {storage_path}/{partition_name}/{key}.meta.json

    Note: All operations are executed by the edge-main runtime.
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


class FileStorage(Storage):
    """
    File-based storage backend.

    Stores data as files on disk. Each partition is a subdirectory.
    Oldest files are automatically evicted when max_size is reached.

    Usage:
        class LocalStore(FileStorage):
            id = "local-data"
            path = "/var/scadable/storage/local-data"
            max_size = SIZE_512_MB

    Then in a decoder or controller:
        store = storage("local-data")
        images = store.partition("images")
        images.write("frame-001", jpeg_bytes, metadata={"type": "jpeg"})
        data = images.read("frame-001")
    """

    id: str = None
    path: str = None
    max_size: int = 512 * 1024 * 1024

    def partition(self, name: str) -> FilePartition:
        raise NotImplementedError("partition() is executed by the edge-main runtime")

    def size(self) -> int:
        raise NotImplementedError("size() is executed by the edge-main runtime")

    def cleanup(self, target_bytes: int = None):
        raise NotImplementedError("cleanup() is executed by the edge-main runtime")
