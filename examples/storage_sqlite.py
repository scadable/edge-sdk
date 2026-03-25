"""
Example: SQLite-based local storage

Stores structured data in tables with typed columns.
Supports insert, query, and delete operations.
Oldest rows are evicted when max_size is reached.
A warning is logged when usage exceeds warning_threshold%.
"""
from scadable.edge import SQLiteStorage
from scadable.edge.constants import SIZE_256_MB


class DeviceCache(SQLiteStorage):
    id = "device-cache"
    path = "/var/scadable/storage/device-cache.db"
    max_size = SIZE_256_MB
    warning_threshold = 80  # warn at 80% full


# Usage in a decoder or controller:
#
#   db = DeviceCache()
#
#   # Define a table with typed columns
#   readings = db.table("readings", columns={
#       "device_id": str,
#       "temperature": float,
#       "humidity": float,
#       "timestamp": int,
#   })
#
#   # Insert rows
#   readings.insert({
#       "device_id": "sensor-01",
#       "temperature": 23.5,
#       "humidity": 65.2,
#       "timestamp": 1711234567,
#   })
#
#   # Query with filters
#   rows = readings.where(device_id="sensor-01").last(10)    # last 10 readings
#   latest = readings.where(device_id="sensor-01").latest()  # most recent
#   first = readings.where(device_id="sensor-01").first()    # oldest
#   all_rows = readings.where(device_id="sensor-01").all()   # everything
#   count = readings.where(device_id="sensor-01").count()    # count matches
#
#   # Get all rows (no filter)
#   everything = readings.all()
#   total = readings.count()
#
#   # Delete matching rows
#   readings.delete_where(device_id="sensor-01")
#
#
#   # Another table for decoder state
#   state = db.table("state", columns={
#       "key": str,
#       "value": str,
#   })
#
#   state.insert({"key": "calibration_offset", "value": "0.3"})
#   offset = state.where(key="calibration_offset").latest()
