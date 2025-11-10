# faulty_simulator.py
import random
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Optional

# --- fault definitions ---
@dataclass
class FaultSpec:
    """Describe one fault with parameters."""
    kind: str                       # "stuck", "noisy", "drift", "intermittent", "delay", "corrupt", "brownout"
    probability: float = 1.0        # for probabilistic faults (0.0-1.0)
    params: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True

    def trigger(self) -> bool:
        if not self.enabled: return False
        return random.random() <= self.probability

# --- basic virtual peripherals (from earlier simulator, extended) ---
class VirtualPin:
    def __init__(self, name):
        self.name = name
        self.state = 0
        self.faults: list[FaultSpec] = []

    def add_fault(self, fault: FaultSpec):
        self.faults.append(fault)

    def _apply_faults(self):
        # evaluate faults in order; first applicable wins
        for f in self.faults:
            if not f.trigger(): 
                continue
            if f.kind == "stuck":
                stuck_val = f.params.get("value", 1)
                return stuck_val, f
            if f.kind == "flip":
                # flip state once when triggered
                self.state ^= 1
                return self.state, f
            if f.kind == "intermittent":
                # probabilistic random noise on reads
                val = f.params.get("value_on", 1) if random.random() < f.params.get("p_on", 0.5) else f.params.get("value_off", 0)
                return val, f
        return None, None

    def write(self, v):
        stuck_result, fault = self._apply_faults()
        if stuck_result is not None:
            # if the fault forces a value, honour it
            print(f"[FAULT] {self.name} fault {fault.kind} enforced value={stuck_result}")
            self.state = stuck_result
            return
        self.state = 1 if v else 0

    def read(self):
        stuck_result, fault = self._apply_faults()
        if stuck_result is not None:
            print(f"[FAULT] {self.name} fault {fault.kind} read value={stuck_result}")
            return stuck_result
        return self.state

class VirtualADC:
    def __init__(self, channel):
        self.channel = channel
        self._base = 32768
        self.faults: list[FaultSpec] = []
        self._drift_acc = 0

    def add_fault(self, fault: FaultSpec):
        self.faults.append(fault)

    def read_u16(self):
        # base reading
        val = self._base
        # apply faults
        for f in self.faults:
            if not f.trigger():
                continue
            if f.kind == "noisy":
                amp = f.params.get("amplitude", 1000)
                val = int(val + random.randint(-amp, amp))
                print(f"[FAULT] ADC{self.channel} noisy (+/-{amp}) -> {val}")
            elif f.kind == "offset":
                off = f.params.get("offset", 2000)
                val = int(val + off)
                print(f"[FAULT] ADC{self.channel} offset {off} -> {val}")
            elif f.kind == "drift":
                step = f.params.get("step", 50)
                self._drift_acc += step
                val = int(val + self._drift_acc)
                print(f"[FAULT] ADC{self.channel} drift step {step} acc {self._drift_acc} -> {val}")
            elif f.kind == "stuck":
                stuck_val = f.params.get("value", val)
                val = int(stuck_val)
                print(f"[FAULT] ADC{self.channel} stuck -> {val}")
            elif f.kind == "brownout":
                # emulate brownout by returning very low VSYS reading
                val = int(f.params.get("value", 5000))
                print(f"[FAULT] ADC{self.channel} brownout -> {val}")
        # clamp to valid range
        val = max(0, min(65535, val))
        return val

# --- Virtual Pico with faults ---
class FaultyVirtualPico:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
        self.led = VirtualPin("LED25")
        self.gp0 = VirtualPin("GP0")
        self.adc26 = VirtualADC(26)
        self.usb_connected = True
        self.usb_faults: list[FaultSpec] = []
        self.metrics = {"power_mA": 50}

    def add_pin_fault(self, pin_name: str, fault: FaultSpec):
        getattr(self, pin_name).add_fault(fault)

    def add_adc_fault(self, fault: FaultSpec):
        self.adc26.add_fault(fault)

    def add_usb_fault(self, fault: FaultSpec):
        self.usb_faults.append(fault)

    def _apply_usb_faults(self):
        for f in self.usb_faults:
            if not f.trigger(): continue
            if f.kind == "disconnect":
                print("[FAULT] USB disconnect")
                self.usb_connected = False
            if f.kind == "packet_loss":
                # we will simulate packet loss by returning False on a chance
                pass

    def led_toggle(self):
        # simulate latency faults
        # check for delay fault on LED pin
        for f in self.led.faults:
            if f.kind == "delay" and f.trigger():
                delay_s = f.params.get("delay_s", 0.5)
                print(f"[FAULT] LED toggle delayed by {delay_s}s")
                time.sleep(delay_s)
        # write normally (write respects stuck/intermittent faults)
        prev = self.led.read()
        self.led.write(0 if prev else 1)
        print(f"LED now {self.led.read()}")

    def read_adc(self):
        return self.adc26.read_u16()

    def run_scenario(self):
        print("Starting FaultyVirtualPico scenario run")
        # 1. LED test
        self.led_toggle()
        self.led_toggle()
        # 2. ADC test
        val = self.read_adc()
        print("ADC read:", val)
        # 3. USB check
        self._apply_usb_faults()
        print("USB connected:", self.usb_connected)
        # 4. power metric
        for f in getattr(self, "power_faults", []):
            if f.kind == "high_current" and f.trigger():
                self.metrics["power_mA"] = f.params.get("value", 200)
                print("[FAULT] high current draw ->", self.metrics["power_mA"])
        print("Metrics:", self.metrics)
