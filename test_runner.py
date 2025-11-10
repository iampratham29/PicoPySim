# test_runner.py
from config import MODE, SERIAL_PORT, BAUDRATE, TIMEOUT
from simulator import VirtualPico
from hardware_test import PicoHardwareTester

if __name__ == "__main__":
    print(f"=== Raspberry Pi Pico Test Suite ({MODE}) ===")
    if MODE == "SIM":
        pico = VirtualPico()
        pico.run_all_tests()
    elif MODE == "HARDWARE":
        tester = PicoHardwareTester(SERIAL_PORT, BAUDRATE, TIMEOUT)
        tester.run_all_tests()
    else:
        print("Invalid MODE in config.py (use 'SIM' or 'HARDWARE')")
