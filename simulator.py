# simulator.py
import random, time

class VirtualPin:
    def __init__(self, name):
        self.name = name
        self.state = 0
    def toggle(self):
        self.state ^= 1
        print(f"[SIM] {self.name} -> {'HIGH' if self.state else 'LOW'}")

class VirtualADC:
    def __init__(self, channel):
        self.channel = channel
    def read_u16(self):
        value = random.randint(20000, 60000)
        print(f"[SIM] ADC{self.channel} read: {value}")
        return value

class VirtualPico:
    def __init__(self):
        self.led = VirtualPin("LED25")
        self.adc = VirtualADC(26)
    def run_all_tests(self):
        print("[SIM] Running virtual Pico tests...")
        for _ in range(3):
            self.led.toggle()
            time.sleep(0.3)
        self.adc.read_u16()
        print("[SIM] Tests completed successfully.")
