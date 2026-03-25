from .device import Device, PAYLOAD_SCHEMA
from .protocols.base import Protocol, TCPConnection, SerialConnection
from .protocols.modbus import ModbusTCPConnection, ModbusRTUConnection, ModbusProtocol
from .protocols.opcua import OPCUAConnection, OPCUAProtocol
from .protocols.serial import SerialDeviceConnection, SerialProtocol
from .constants import (
    MODBUS_TCP, MODBUS_RTU, OPCUA, SERIAL, MQTT,
    ONE_SEC, FIVE_SEC, TEN_SEC, THIRTY_SEC, ONE_MIN, FIVE_MIN,
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
    # Constants
    "MODBUS_TCP", "MODBUS_RTU", "OPCUA", "SERIAL", "MQTT",
    "ONE_SEC", "FIVE_SEC", "TEN_SEC", "THIRTY_SEC", "ONE_MIN", "FIVE_MIN",
]
