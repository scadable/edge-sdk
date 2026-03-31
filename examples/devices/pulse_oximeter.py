"""BLE pulse oximeter for patient monitoring."""
from scadable import Device, ble, every, Characteristic, Historian, SECONDS


class PulseOximeter(Device):
    id = "pulse-ox"
    name = "Bedside pulse oximeter"
    connection = ble(
        mac="${PULSE_OX_MAC}",
        service="0x1822",  # Pulse Oximeter Service (IEEE 11073-10404)
        characteristics=[
            Characteristic("spo2", uuid="0x2A5E"),
            Characteristic("pulse_rate", uuid="0x2A37"),
            Characteristic("pleth_waveform", uuid="0x2A5F"),
        ],
    )
    poll = every(1, SECONDS)

    # Store SpO2 and pulse rate every reading, skip raw waveform
    historian = Historian(fields=["spo2", "pulse_rate"])
