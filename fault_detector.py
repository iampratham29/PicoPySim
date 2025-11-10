# fault_detector.py
import statistics

class FaultDetector:
    """Analyzes simulation results to flag abnormal behavior."""

    def detect_adc_fault(self, values):
        avg = statistics.mean(values)
        std = statistics.pstdev(values)
        if std > 1500:
            return "ADC noisy"
        elif abs(avg - 32768) > 5000:
            return "ADC drift/offset"
        return None

    def detect_led_fault(self, led_states):
        if len(set(led_states)) == 1:
            return "LED stuck"
        return None

    def detect_usb_fault(self, usb_states):
        if not all(usb_states):
            return "USB disconnect"
        return None
