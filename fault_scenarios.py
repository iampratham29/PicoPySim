# fault_scenarios.py
from faulty_simulator import FaultSpec

def get_fault_scenarios():
    """Return a dictionary of named fault scenarios."""
    return {
        "no_faults": [],  # ✅ New baseline scenario
        "adc_drift": [
            ("adc", FaultSpec(kind="drift", probability=1.0, params={"step": 200}))
        ],
        "led_stuck_high": [
            ("led", FaultSpec(kind="stuck", probability=1.0, params={"value": 1}))
        ],
        "usb_disconnect": [
            ("usb", FaultSpec(kind="disconnect", probability=1.0))
        ],
        "adc_noisy_and_led_delay": [
            ("adc", FaultSpec(kind="noisy", probability=1.0, params={"amplitude": 3000})),
            ("led", FaultSpec(kind="delay", probability=1.0, params={"delay_s": 0.5}))
        ]
    }
