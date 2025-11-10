# test_faults.py
import pytest
from faulty_simulator import FaultyVirtualPico, FaultSpec

def test_adc_stuck_detection():
    p = FaultyVirtualPico(seed=0)
    # ADC stuck at a fixed value (simulate failure)
    p.add_adc_fault(FaultSpec(kind="stuck", probability=1.0, params={"value": 40000}))
    val = p.read_adc()
    assert val == 40000, "ADC should be stuck at 40000"

def test_led_stuck_behavior():
    p = FaultyVirtualPico(seed=1)
    p.led.add_fault(FaultSpec(kind="stuck", probability=1.0, params={"value": 0}))
    p.led_toggle()  # toggle should enforce stuck=0
    assert p.led.read() == 0

def test_intermittent_usb_disconnect():
    p = FaultyVirtualPico(seed=2)
    p.add_usb_fault(FaultSpec(kind="disconnect", probability=1.0))
    p._apply_usb_faults()
    assert p.usb_connected is False
