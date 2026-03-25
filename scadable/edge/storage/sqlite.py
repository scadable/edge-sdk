from .base import Storage, Partition


class SQLitePartition(Partition):
    """
    SQLite-based partition. Each partition is a separate table.
    Data is stored as BLOBs with a JSON metadata column.

    Table structure (managed by the runtime):
        CREATE TABLE p_{name} (
            key TEXT PRIMARY KEY,
            data BLOB NOT NULL,
            metadata TEXT DEFAULT '{}',
            created_at REAL NOT NULL,
            size INTEGER NOT NULL
        )

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


class SQLiteStorage(Storage):
    """
    SQLite-based storage backend.

    Stores data in a SQLite database with WAL mode for performance.
    Each partition is a separate table. Good for structured/queryable
    data and key-value storage.

    Usage:
        class DeviceCache(SQLiteStorage):
            id = "device-cache"
            path = "/var/scadable/storage/device-cache.db"
            max_size = SIZE_256_MB

    Then in a decoder or controller:
        store = storage("device-cache")
        cache = store.partition("readings")
        cache.write("sensor-01", json.dumps(reading).encode())
        data = cache.read("sensor-01")
    """

    id: str = None
    path: str = None
    max_size: int = 256 * 1024 * 1024

    def partition(self, name: str) -> SQLitePartition:
        raise NotImplementedError("partition() is executed by the edge-main runtime")

    def size(self) -> int:
        raise NotImplementedError("size() is executed by the edge-main runtime")

    def cleanup(self, target_bytes: int = None):
        raise NotImplementedError("cleanup() is executed by the edge-main runtime")
