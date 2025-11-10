# hardware_test.py
import serial, time

class PicoHardwareTester:
    def __init__(self, port, baudrate, timeout):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # wait for connection
        print("[HW] Connected to Pico")

    def send_command(self, cmd):
        self.ser.write((cmd + "\n").encode())
        time.sleep(0.5)
        return self.ser.readline().decode().strip()

    def run_all_tests(self):
        print("[HW] Running hardware tests...")
        print("→ LED Blink Test:", self.send_command("LED"))
        print("→ ADC Test:", self.send_command("ADC"))
        print("→ Sleep Mode Test:", self.send_command("SLEEP"))
        print("→ USB Echo Test:", self.send_command("ECHO hello"))
        print("[HW] Tests completed.")
