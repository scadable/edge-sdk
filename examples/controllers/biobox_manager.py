"""BioBox lifecycle manager for Verdant Metrics deployments.

Demonstrates startup/shutdown hooks and command handling for
devices that power on/off on a schedule.
"""
from scadable import (
    Controller, every, on_startup, on_shutdown, on_message,
    system, alert, broadcast, MINUTES, HOURS,
)
from devices.esp32_sensors import ESP32Sensors


class BioBoxManager(Controller):
    id = "biobox-manager"
    run = every(1, MINUTES)
    uses = [ESP32Sensors]

    @on_startup
    def boot(self):
        broadcast("BioBox online, starting data collection")

    @on_shutdown
    def goodbye(self):
        system.shutdown(duration=2, HOURS)

    @on_message("halt")
    def handle_halt(self, message):
        alert("info", "Halt command received")
        duration = message.get("duration", 2) if isinstance(message, dict) else 2
        system.shutdown(duration=duration, unit=HOURS)

    def execute(self, data):
        temp = data.ESP32Sensors.soil_temp
        if temp > 45:
            alert("warning", f"High soil temperature: {temp}C")
