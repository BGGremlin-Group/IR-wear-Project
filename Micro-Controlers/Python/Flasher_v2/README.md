IRWP v2.5 Flasher V2! Read me

Multi-Platform Infrared Anti-Surveillance System Tools

---

Overview

IRWP is a python GUI application for testing surveillance system vulnerabilities and privacy Obfuscation via IR LED arrays.
Supports ESP32, Raspberry Pi Pico, Arduino Nano, and STM32 microcontrollers with integrated firmware flashing, attack orchestration, and real-time monitoring.

---

Features

✅ Core Functionality
- Multi-Platform Support: Auto-detect and flash ESP32, Pi Pico, Arduino Nano, STM32
- Real-Time Attack Orchestration: Thread-safe, non-blocking serial communication
- Hardware Safety Integration: Physical dead-man switch required for operation
- Attack Pattern Library: 12+ documented patterns with flip-flop orchestration
- Live Monitoring: Cycle counters, phase tracking, spectrum visualization
- Cryptographic Logging: Tamper-evident audit logs for authorized testing
- Emergency Stop: Instant hardware relay cutoff

🔥 Extreme Patterns (Deadly Defaults)
Located in `user_attacks/Deadly_Defaults/`:

---

Installation

System Requirements
- OS: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- Python: 3.8 or higher
- Hardware: USB port, 12V 3A power supply, 40x 5mm IR LED array

Quick Install

```bash
# Clone repository
git clone https://github.com/BGGremlin-Group/IR-wear-Project.git
cd IR-wear-Project/Micro-Controlers/Python

# Install dependencies
pip install -r requirements.txt

# For firmware flashing tools:
# ESP32: pip install esptool
# Pi Pico: Install picotool (system package)
# Arduino: Install avrdude (system package)
# STM32: Install st-flash (system package)
```

---

Quick Start

1. Connect Microcontroller
- Plug in ESP32/Pico/Nano/STM32 via USB
- Click "Auto-Detect & Connect" or select manual port

2. Flash Firmware (First Time Only)
- Select platform from dropdown
- Click "Flash Selected Platform"
- Wait for completion (progress bar will show 100%)

3. Configure Attack
- Select targets (Walmart, Target, etc.)
- Choose pattern from dropdown
- Set durations and max cycles


---

Usage Guide

Main Window Layout

Left Panel - Connection & Flashing
- Auto-detect/connect to microcontroller
- Manual port selection with refresh
- Multi-platform firmware flashing
- Hardware safety indicator

Center Panel - Attack Configuration
- Pattern selection (stable/experimental/deadly)
- Target store checkboxes
- Camera/Data injection duration sliders
- Jitter and max cycles configuration

Right Panel - Control & Monitoring
- Master arm/disarm switch
- Live cycle counter
- Real-time status feed (last 1000 lines)
- Emergency stop button

Pattern Types

Stable Patterns (✅ Should Work)
- `AGC_LOCK`: 5-30 second video blackout
- `SATURATION`: Full sensor whiteout
- `FLICKER`: Rolling shutter diagonal tearing
- `Dazzle`: Anti-facial recognition
- `PTZ_JAM`: Overflow PTZ tracking buffer
- `ALPR_CORRUPT`: OCR confidence drop

Experimental Patterns (⚠️ May Not Work)
- `EXPERIMENTAL-heat_map`: False analytics zones
- `EXPERIMENTAL-people_spoof`: Phantom people injection
- `EXPERIMENTAL-queue_manip`: Queue length spoofing

Deadly Defaults (🔴 Extreme)
Located in `user_attacks/Deadly_Defaults/`:
- D_Default1: All attacks max intensity, thermal warnings
- D_Default2: Deliberate thermal stress test
- D_Default3: Randomized chaos engine (defeats AI)
- D_Default4: Balanced 20-25 minute endurance

---

Building Firmware

Option 1: Automated (PlatformIO)

```bash
cd Firmware/
pip install platformio
pio run -e esp32dev  # or pico, nanoatmega328, bluepill_f103c8
# Binaries appear in .pio/build/
```

Option 2: Arduino IDE
1. Open `.ino` file in Arduino IDE
2. Select correct Tools → Board
3. Sketch → Export Compiled Binary
4. Rename and move to `firmware/` directory

   
---

Troubleshooting

Connection Issues
Problem: "No ports found"
- Solution: Install USB drivers (CP210x for ESP32, CH340 for Nano)

Problem: "Failed to open serial port"
- Solution: Close other serial monitor programs, check permissions (Linux: `sudo usermod -a -G dialout $USER`)

Flashing Failures
Problem: "Firmware not found"
- Solution: Build firmware first using instructions above

Problem: "Tool not found"
- Solution: Install platform-specific tools and add to PATH

Attack Not Working
Problem: No visible effect on camera
- Solution: 
  - Check distance (most effective <3m)
  - Verify line-of-sight to camera IR sensor
  - Increase intensity to 255
  - Try `SATURATION` pattern first (most reliable)

Problem: LEDs getting hot
- Solution: 
  - Reduce intensity to 180-200
  - Add micro-rests in pattern
  - Use `Deadly_Default4` for thermal management

---

Safety Guidelines

Pattern-Specific Warnings

Deadly Defaults:
- D_Default1: Thermal shutdown in 15-20 min
- D_Default2: Will damage LEDs with extended use
- D_Default3: Unpredictable power draw, not for battery
- D_Default4: Safe for 20-25 min continuous

Experimental Patterns:
- May not work at all
- Higher chance of detection in logs
- Wasted battery power

---

Adding New Patterns

1. Create JSON in `user_attacks/` folder
2. Use existing pattern as template
3. Follow format:

```json
{
  "name": "Your_Pattern_Name",
  "description": "What it does",
  "type": "camera_attack|data_injection",
  "severity": "low|medium|high|critical",
  "sequence": [
    {"group": 0-4, "intensity": 0-255, "duration_ms": 1-60000}
  ],
  "repeat": 1-100
}
```

4. Mark as `EXPERIMENTAL-` prefix until verified
5. Test on your own hardware before field use

---

License & Legal
MIT - Open Source Project
We are not your nanny. We neither endorse the use nor misuse of anything within this project or any of our products.
All code is presented as is.

---

Support & Contributions

- Issues: Report bugs via GitHub Issues
- Patterns: Submit verified patterns via Pull Request
- Documentation: Improve this project
- Firmware: Submit optimized builds for new boards

---

Document Version: 2.5.0

Last Updated: Jan 2026

Maintained by: BGGremlin Group - IR Wear Project Team
