from .base import Storage, Table


class SQLiteStorage(Storage):
    """
    SQLite-based storage for structured data (tables, rows, queries).

    Each table is a named collection of typed columns. WAL mode is
    enabled for performance. Oldest rows are evicted when max_size
    is reached. A warning is logged when usage exceeds
    warning_threshold % of max_size.

    Usage:
        class DeviceCache(SQLiteStorage):
            id = "device-cache"
            path = "/var/scadable/storage/cache.db"
            max_size = SIZE_256_MB
            warning_threshold = 80

        db = DeviceCache()
        readings = db.table("readings", columns={
            "device_id": str,
            "temperature": float,
            "humidity": float,
            "timestamp": int,
        })

        readings.insert({"device_id": "sensor-01", "temperature": 23.5, ...})
        rows = readings.where(device_id="sensor-01").last(10)
        latest = readings.where(device_id="sensor-01").latest()
        count = readings.count()
    """

    id: str = None
    path: str = None
    max_size: int = 256 * 1024 * 1024
    warning_threshold: int = 80

    def table(self, name: str, columns: dict) -> Table:
        """
        Get or create a named table with typed columns.

        Args:
            name: Table name.
            columns: Dict of column_name → type.
                     Supported types: str, int, float, bool, bytes.

        Returns:
            A Table instance for insert/query/delete operations.
        """
        return Table(self, name, columns)
