# main.py (MicroPython on Pico)
from machine import Pin, ADC
import time, sys

led = Pin(25, Pin.OUT)
adc = ADC(26)

def led_test():
    for _ in range(3):
        led.toggle()
        time.sleep(0.3)
    return "LED OK"

def adc_test():
    val = adc.read_u16()
    return f"ADC: {val}"

def sleep_test():
    time.sleep(1)
    return "SLEEP OK"

def echo(msg):
    return f"ECHO: {msg}"

while True:
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline().strip()
        if line == "LED":
            print(led_test())
        elif line == "ADC":
            print(adc_test())
        elif line == "SLEEP":
            print(sleep_test())
        elif line.startswith("ECHO"):
            print(echo(line.split(" ", 1)[1]))
