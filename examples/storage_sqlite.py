"""
Example: SQLite-based local storage

Stores data in a SQLite database. Each partition gets its own table.
Good for: structured data, key-value cache, queryable state.
"""
from scadable.edge import SQLiteStorage
from scadable.edge.constants import SIZE_256_MB


class DeviceCache(SQLiteStorage):
    id = "device-cache"
    path = "/var/scadable/storage/device-cache.db"
    max_size = SIZE_256_MB


# Usage in a decoder or controller (executed by edge-main runtime):
#
#   store = storage("device-cache")
#
#   # Partitions keep data isolated
#   readings = store.partition("readings")
#   state    = store.partition("state")
#
#   # Write sensor data
#   import json
#   readings.write("sensor-01-latest", json.dumps({
#       "temperature": 23.5,
#       "humidity": 65.2,
#       "timestamp": 1711234567,
#   }).encode())
#
#   # Read it back
#   data = json.loads(readings.read("sensor-01-latest"))
#
#   # Store decoder state
#   state.write("calibration", json.dumps({
#       "offset": 0.3,
#       "last_calibrated": "2026-03-24",
#   }).encode())
#
#   # List keys with prefix
#   keys = readings.list(prefix="sensor-01")
#
#   # Check if exists
#   if readings.exists("sensor-01-latest"):
#       print("Got cached reading")
