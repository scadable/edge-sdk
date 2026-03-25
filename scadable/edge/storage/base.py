from abc import ABC, abstractmethod


class Partition(ABC):
    """
    A namespaced view into a storage backend.
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
        """
        Write data to storage.

        Args:
            key: Unique key within this partition.
            data: Bytes or string to store.
            metadata: Optional metadata dict (stored alongside data).

        Returns:
            The full storage reference (partition/key).
        """
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


class Storage:
    """
    Base class for all storage backends.

    Subclass this to define a storage instance in your project.
    Each storage has an id, a path, and a max size limit.
    Data is organized into partitions to prevent mixing between
    different consumers (outbound, decoder, controller, etc).

    Usage:
        class MyStore(FileStorage):
            id = "local-data"
            path = "/var/scadable/storage/local-data"
            max_size = SIZE_512_MB
    """

    id: str = None
    path: str = None
    max_size: int = 512 * 1024 * 1024  # default 512MB

    _partitions: dict = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Skip validation for intermediate base classes
        if cls.__name__ in ("Storage", "FileStorage", "SQLiteStorage"):
            return
        errors = []
        if not cls.id:
            errors.append(f"Storage subclass '{cls.__name__}' must define 'id'")
        if not cls.path:
            errors.append(f"Storage subclass '{cls.__name__}' must define 'path'")
        if cls.max_size is not None and (not isinstance(cls.max_size, int) or cls.max_size <= 0):
            errors.append(f"Storage subclass '{cls.__name__}' — max_size must be a positive integer")
        if errors:
            raise TypeError("\n".join(errors))

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} id={self.id!r} "
            f"path={self.path!r} max_size={_format_size(self.max_size)}>"
        )

    @abstractmethod
    def partition(self, name: str) -> Partition:
        """
        Get a namespaced partition.

        Args:
            name: Partition name (e.g. "outbound", "decoder", "controller").

        Returns:
            A Partition instance scoped to this namespace.
        """
        pass

    @abstractmethod
    def size(self) -> int:
        """Current total storage usage in bytes across all partitions."""
        pass

    @abstractmethod
    def cleanup(self, target_bytes: int = None):
        """
        Free space by removing oldest entries.

        Args:
            target_bytes: Free space until usage is below this.
                          Defaults to max_size * 0.8.
        """
        pass


def _format_size(size_bytes: int) -> str:
    """Format bytes into human-readable string."""
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024 * 1024):.0f}GB"
    elif size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.0f}MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.0f}KB"
    return f"{size_bytes}B"
