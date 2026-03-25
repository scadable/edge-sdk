from .device import Device, PAYLOAD_SCHEMA
from .protocols.base import Protocol, TCPConnection, SerialConnection
from .protocols.modbus import ModbusTCPConnection, ModbusRTUConnection, ModbusProtocol
from .protocols.opcua import OPCUAConnection, OPCUAProtocol
from .protocols.serial import SerialDeviceConnection, SerialProtocol
from .storage.base import Storage, Partition
from .storage.file import FileStorage
from .storage.sqlite import SQLiteStorage
from .constants import (
    MODBUS_TCP, MODBUS_RTU, OPCUA, SERIAL, MQTT,
    STORAGE_FILE, STORAGE_SQLITE,
    ONE_SEC, FIVE_SEC, TEN_SEC, THIRTY_SEC, ONE_MIN, FIVE_MIN,
    SIZE_64_MB, SIZE_128_MB, SIZE_256_MB, SIZE_512_MB,
    SIZE_1_GB, SIZE_2_GB, SIZE_5_GB,
)

# Backward compatibility
ModbusConnection = ModbusTCPConnection

__all__ = [
    "Device",
    "PAYLOAD_SCHEMA",
    # Base
    "Protocol",
    "TCPConnection",
    "SerialConnection",
    # Modbus
    "ModbusTCPConnection",
    "ModbusRTUConnection",
    "ModbusConnection",       # backward compat alias
    "ModbusProtocol",
    # OPC-UA
    "OPCUAConnection",
    "OPCUAProtocol",
    # Serial
    "SerialDeviceConnection",
    "SerialProtocol",
    # Storage
    "Storage",
    "Partition",
    "FileStorage",
    "SQLiteStorage",
    # Constants
    "MODBUS_TCP", "MODBUS_RTU", "OPCUA", "SERIAL", "MQTT",
    "STORAGE_FILE", "STORAGE_SQLITE",
    "ONE_SEC", "FIVE_SEC", "TEN_SEC", "THIRTY_SEC", "ONE_MIN", "FIVE_MIN",
    "SIZE_64_MB", "SIZE_128_MB", "SIZE_256_MB", "SIZE_512_MB",
    "SIZE_1_GB", "SIZE_2_GB", "SIZE_5_GB",
]
