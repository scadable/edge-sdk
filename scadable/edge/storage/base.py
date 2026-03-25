from abc import ABC, abstractmethod


class Partition(ABC):
    """
    A namespaced view into a file storage backend.
    Data written to one partition is isolated from other partitions.
    """

    def __init__(self, storage: "Storage", name: str):
        self._storage = storage
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def write(self, key: str, data, metadata: dict = None) -> str:
        """Write data. Returns the full storage reference (partition/key)."""
        pass

    @abstractmethod
    def read(self, key: str) -> bytes:
        """Read data by key. Raises KeyError if not found."""
        pass

    @abstractmethod
    def list(self, prefix: str = None, limit: int = None) -> list:
        """List keys in this partition, optionally filtered by prefix."""
        pass

    @abstractmethod
    def delete(self, key: str):
        """Delete a key. No error if key doesn't exist."""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if a key exists in this partition."""
        pass

    @abstractmethod
    def metadata(self, key: str) -> dict:
        """Get metadata for a key. Returns empty dict if no metadata."""
        pass


class Query:
    """
    Chainable query builder for SQLite tables.

    Usage:
        rows = table.where(device_id="sensor-01").last(10)
        latest = table.where(device_id="sensor-01").latest()
        count = table.where("temperature > 30").count()
    """

    def __init__(self, table: "Table", filters: dict = None, raw_filter: str = None):
        self._table = table
        self._filters = filters or {}
        self._raw_filter = raw_filter

    def last(self, n: int) -> list:
        """Get the last N rows ordered by insertion time (newest first)."""
        raise NotImplementedError("last() is executed by the edge-main runtime")

    def latest(self) -> dict:
        """Get the most recent row. Returns empty dict if no match."""
        raise NotImplementedError("latest() is executed by the edge-main runtime")

    def first(self) -> dict:
        """Get the oldest row. Returns empty dict if no match."""
        raise NotImplementedError("first() is executed by the edge-main runtime")

    def all(self) -> list:
        """Get all matching rows."""
        raise NotImplementedError("all() is executed by the edge-main runtime")

    def count(self) -> int:
        """Count matching rows."""
        raise NotImplementedError("count() is executed by the edge-main runtime")


class Table:
    """
    A typed table in a SQLite storage backend.

    Usage:
        readings = db.table("readings", columns={
            "device_id": str,
            "temperature": float,
            "humidity": float,
            "timestamp": int,
        })

        readings.insert({"device_id": "sensor-01", "temperature": 23.5, ...})
        rows = readings.where(device_id="sensor-01").last(10)
    """

    def __init__(self, storage: "Storage", name: str, columns: dict):
        self._storage = storage
        self._name = name
        self._columns = columns

    @property
    def name(self) -> str:
        return self._name

    @property
    def columns(self) -> dict:
        return self._columns

    def insert(self, row: dict):
        """Insert a row. Keys must match column names."""
        raise NotImplementedError("insert() is executed by the edge-main runtime")

    def where(self, raw: str = None, **kwargs) -> Query:
        """
        Filter rows. Returns a chainable Query.

        Keyword args filter by exact match:
            table.where(device_id="sensor-01")

        String arg for expressions:
            table.where("temperature > 30")
        """
        return Query(self, filters=kwargs, raw_filter=raw)

    def all(self) -> list:
        """Get all rows in the table."""
        raise NotImplementedError("all() is executed by the edge-main runtime")

    def count(self) -> int:
        """Count all rows in the table."""
        raise NotImplementedError("count() is executed by the edge-main runtime")

    def delete_where(self, **kwargs):
        """Delete rows matching the given filters."""
        raise NotImplementedError("delete_where() is executed by the edge-main runtime")


class Storage:
    """
    Base class for all storage backends.

    Attributes:
        id: Unique identifier for this storage instance.
        path: Filesystem path (directory for File, .db file for SQLite).
        max_size: Maximum storage size in bytes. Use SIZE_* constants.
        warning_threshold: Percentage (1-100) at which the runtime logs a warning.
                           Default: 80 (warn when 80% full).
    """

    id: str = None
    path: str = None
    max_size: int = 512 * 1024 * 1024
    warning_threshold: int = 80

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.__name__ in ("Storage", "FileStorage", "SQLiteStorage"):
            return
        errors = []
        if not cls.id:
            errors.append(f"Storage '{cls.__name__}' must define 'id'")
        if not cls.path:
            errors.append(f"Storage '{cls.__name__}' must define 'path'")
        if cls.max_size is not None and (not isinstance(cls.max_size, int) or cls.max_size <= 0):
            errors.append(f"Storage '{cls.__name__}' — max_size must be a positive integer")
        if not isinstance(cls.warning_threshold, int) or not (1 <= cls.warning_threshold <= 100):
            errors.append(f"Storage '{cls.__name__}' — warning_threshold must be 1-100")
        if errors:
            raise TypeError("\n".join(errors))

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} id={self.id!r} path={self.path!r} "
            f"max_size={_format_size(self.max_size)} threshold={self.warning_threshold}%>"
        )

    def size(self) -> int:
        """Current storage usage in bytes."""
        raise NotImplementedError("size() is executed by the edge-main runtime")

    def cleanup(self, target_bytes: int = None):
        """Free space by removing oldest entries."""
        raise NotImplementedError("cleanup() is executed by the edge-main runtime")


def _format_size(size_bytes: int) -> str:
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024 * 1024):.0f}GB"
    elif size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.0f}MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f}KB"
    return f"{size_bytes}B"
