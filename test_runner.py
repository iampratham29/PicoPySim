# test_runner.py
from faulty_simulator import FaultyVirtualPico
from fault_scenarios import get_fault_scenarios
from fault_detector import FaultDetector
from config import MODE
import time

def run_fault_diagnostics():
    scenarios = get_fault_scenarios()
    detector = FaultDetector()
    results = []

    for name, faults in scenarios.items():
        print(f"\n🧪 Running scenario: {name}")
        pico = FaultyVirtualPico(seed=42)

        # --- Inject faults ---
        for target, fault in faults:
            if target == "adc":
                pico.add_adc_fault(fault)
            elif target == "led":
                pico.led.add_fault(fault)
            elif target == "usb":
                pico.add_usb_fault(fault)

        # --- Run the simulation ---
        adc_vals, led_states, usb_states = [], [], []
        for _ in range(5):
            pico.led_toggle()
            led_states.append(pico.led.read())
            adc_vals.append(pico.read_adc())
            pico._apply_usb_faults()
            usb_states.append(pico.usb_connected)
            time.sleep(0.1)

        # --- Fault detection phase ---
        detected = []
        if f := detector.detect_adc_fault(adc_vals):
            detected.append(f)
        if f := detector.detect_led_fault(led_states):
            detected.append(f)
        if f := detector.detect_usb_fault(usb_states):
            detected.append(f)

        # --- Reporting ---
        if not faults and not detected:
            status = "ALL NORMAL ✅"
        elif faults and not detected:
            status = "⚠️ FAULT MISSED (should have been detected)"
        elif detected:
            status = "FAULT DETECTED ✅"
        else:
            status = "UNKNOWN ⚠️"

        print(f"🔎 Detected: {detected or ['None']}")
        results.append((name, status, detected))

    # --- Summary ---
    print("\n📊 Fault Detection Summary:")
    for name, status, detected in results:
        print(f"• {name:<25} → {status:<30} {', '.join(detected) if detected else ''}")

if __name__ == "__main__":
    if MODE == "SIM":
        print("=== PicoPySim Diagnostic Mode ===")
        run_fault_diagnostics()
    else:
        print("Hardware mode not implemented yet. Set MODE='SIM' in config.py.")
