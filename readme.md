# 🧠 PicoPySim – Virtual Raspberry Pi Pico Fault Simulator & Diagnostic Framework  

PicoPySim is a **Python-based simulation and testing framework** that mimics a Raspberry Pi Pico microcontroller.  
It lets you inject hardware-like faults (ADC drift, LED stuck, USB disconnect, etc.), run diagnostic routines, and verify that your fault-detection logic behaves correctly — all **without real hardware**.

---

## 🚀 Features

- 🧩 **Virtual Pico hardware** (`FaultyVirtualPico`) – simulates GPIOs, ADC, USB, and power metrics  
- ⚡ **Fault injection system** – add faults like drift, noise, stuck-at, delay, disconnect, and more  
- 🔎 **Fault detection logic** – identifies anomalies automatically  
- 🧪 **Scenario-based runner** – executes multiple test scenarios sequentially  
- 🟢 **"No-fault" baseline check** – confirms normal behavior when no faults are present  
- 🧾 **pytest integration** – supports automated testing for each simulated component  

---

## 📁 Project Structure

```
PicoPySim/
│
├── faulty_simulator.py     # Core simulator & fault injection engine
├── fault_detector.py       # Logic for detecting abnormal behavior
├── fault_scenarios.py      # Predefined test scenarios
├── test_runner.py          # Main diagnostic runner (entry point)
├── test_faults.py          # Unit tests (pytest)
├── config.py               # Mode configuration (SIM or HARDWARE)
├── requirements.txt        # Dependencies
└── README.md               # You are here
```

---

## ⚙️ Installation

1. Clone or download this repository.
2. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

### 🧪 Run Full Diagnostic Simulation

```bash
python test_runner.py
```

This will:

* Initialize a virtual Pico
* Run all predefined fault scenarios (including a normal "no-fault" run)
* Detect and classify each fault
* Print a summary table like:

```
📊 Fault Detection Summary:
• no_faults               → ALL NORMAL ✅
• adc_drift               → FAULT DETECTED ✅ ADC drift/offset
• led_stuck_high          → FAULT DETECTED ✅ LED stuck
• usb_disconnect          → FAULT DETECTED ✅ USB disconnect
• adc_noisy_and_led_delay → FAULT DETECTED ✅ ADC noisy
```

---

### 🧩 Run Individual Tests (using Pytest)

```bash
pytest -v -s
```

This runs the unit tests in `test_faults.py` and shows `[FAULT]` logs such as:

```
[FAULT] ADC26 stuck -> 40000
[FAULT] LED25 fault stuck enforced value=0
[FAULT] USB disconnect
```

---

### 🔧 Configuration

Edit **config.py** to switch between modes:

```python
MODE = "SIM"       # Run virtual simulator
# MODE = "HARDWARE"  # Reserved for future physical Pico tests
```

---

## 🧩 Fault Types Supported

| Fault Type   | Description                                    |
| ------------ | ---------------------------------------------- |
| `stuck`      | Keeps a pin or ADC at a constant value         |
| `drift`      | Gradually shifts ADC readings over time        |
| `noisy`      | Adds random variation around a value           |
| `delay`      | Adds latency to an operation (e.g. LED toggle) |
| `disconnect` | Simulates USB link loss                        |
| `offset`     | Adds bias to ADC reading                       |
| `brownout`   | Simulates low voltage (ADC undervalue)         |

---

## 📈 Example Output

```
=== PicoPySim Diagnostic Mode ===

🧪 Running scenario: adc_drift
[FAULT] ADC26 drift step 200 acc 200 -> 32968
🔎 Detected: ['ADC drift/offset']

🧪 Running scenario: no_faults
LED now 1
LED now 0
🔎 Detected: ['None']

📊 Fault Detection Summary:
• adc_drift     → FAULT DETECTED ✅ ADC drift/offset
• no_faults     → ALL NORMAL ✅
```

---

## 🧩 Future Enhancements

* 💾 Save results to CSV/JSON logs with timestamps
* 📊 Plot ADC drift and noise graphs using `matplotlib`
* 🤖 Add machine-learning-based fault classification
* 🧠 Extend support for real hardware (`MODE = "HARDWARE"`)

---

## 📜 License

MIT License © 2025 — Developed as an educational microcontroller-simulation toolkit.