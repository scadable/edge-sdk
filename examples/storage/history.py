"""SQLite storage for device reading history."""
from scadable import SQLiteStorage, MB_256

class DeviceHistory(SQLiteStorage):
    id = "device-history"
    path = "/var/data/history.db"
    max_size = MB_256
    warn_at = 80
