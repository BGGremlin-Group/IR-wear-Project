IRWP Flasher V2 README

What This Application Does

This is a Python GUI application that:
- Flashes firmware to ESP32, Pi Pico, Arduino Nano, and STM32 microcontrollers
- Orchestrates IR LED attack patterns against surveillance cameras
- Provides real-time control and monitoring via serial connection

File Structure

```
Flasher_v2/
├── main.py              # Main application
├── Requirements.txt     # Python dependencies
├── Firmware_Setup.md    # Firmware build instructions
└── README.md           # This file
```

Dependencies
- PyQt6
- pyserial
- esptool (for ESP32)
- picotool (for Pi Pico)
- avrdude (for Arduino Nano)
- st-flash (for STM32)

How to Run
1. Install dependencies: `pip install -r Requirements.txt`
2. Place firmware binaries in `firmware/` directory
3. Run: `python main.py`
4. Connect microcontroller via USB
5. Use GUI to flash and control

Attack Patterns
Patterns are loaded from `user_attacks/` directory as JSON files. The application includes:
- Built-in patterns: AGC_LOCK, SATURATION, FLICKER
- Custom patterns: Load from JSON files

Pattern format:

```json
{
  "name": "Pattern_Name",
  "sequence": [
    {"group": 0-4, "intensity": 0-255, "duration_ms": 1-60000}
  ],
  "repeat": 1-100
}
```

---

Version: Flasher V2
