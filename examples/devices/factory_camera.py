"""Factory camera that can capture images on demand."""
from scadable import Device, serial_uart, every, SECONDS

class FactoryCamera(Device):
    id = "factory-camera"
    name = "Production line camera"

    connection = serial_uart(port="/dev/ttyACM0", baud=921600)
    poll = every(30, SECONDS)
