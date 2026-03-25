"""Serial/UART air quality sensor (ESP32 or Arduino)."""
from scadable import Device, serial_uart, every, Field, SECONDS, FLOAT32, UINT16

class UartAirQualitySensor(Device):
    id = "uart-air-quality"
    name = "Air quality monitor"

    connection = serial_uart(port="/dev/ttyUSB0", baud=9600)
    poll = every(10, SECONDS)

    fields = [
        Field("temperature", start=0,  length=4, type=FLOAT32, scale=0.01, unit="°C"),
        Field("pressure",    start=4,  length=4, type=FLOAT32, scale=0.01, unit="bar"),
        Field("co2_ppm",     start=8,  length=2, type=UINT16,  unit="ppm"),
        Field("humidity",    start=10, length=2, type=UINT16,   scale=0.1, unit="%"),
    ]
