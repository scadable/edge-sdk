"""
Multi-device temperature monitor.

Reads from a Modbus sensor and an OPC-UA server.
If temperature is high, triggers the camera and uploads the photo.
"""
from scadable import Controller, every, route, actuate, alert, SECONDS

from examples.devices.temp_pressure_sensor import TempPressureSensor
from examples.devices.ignition_scada import IgnitionSCADA
from examples.devices.factory_camera import FactoryCamera


class TempMonitor(Controller):
    id = "temp-monitor"
    run = every(5, SECONDS)
    uses = [TempPressureSensor, IgnitionSCADA, FactoryCamera]

    def execute(self, data):
        # Read from Modbus sensor
        temp = data.TempPressureSensor.temperature
        pressure = data.TempPressureSensor.pressure

        # Read from OPC-UA server
        tank_level = data.IgnitionSCADA.level

        # Always send readings to MQTT
        route("sensor-data", {
            "temperature": temp,
            "pressure": pressure,
            "tank_level": tank_level,
        })

        # High temperature: take photo and upload
        if temp > 75:
            actuate(FactoryCamera, action="capture")

            route("high-temp-photos", metadata={
                "temperature": temp,
                "reason": "high_temp",
            })

            alert("warning", f"High temperature detected: {temp}°C")

        # Critical: emergency stop
        if temp > 95:
            actuate(TempPressureSensor, register=40050, value=1)
            alert("critical", f"CRITICAL: {temp}°C, machine stopped")
