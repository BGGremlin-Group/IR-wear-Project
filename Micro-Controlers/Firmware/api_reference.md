# IRWP - Infrared Wear Project

**Wearable IR LED countermeasure system. NEVER SHUTS DOWN.**  
Multi-platform firmware for ESP32, Raspberry Pi Pico, Arduino Nano, STM32.

## ⚠️ CRITICAL SAFETY WARNING
**HIGH VOLTAGE | THERMAL HAZARD | EYE SAFETY RISK**  
This device emits high-power infrared radiation that can cause permanent eye damage.
Wear IR-blocking safety glasses (OD 3+) during operation.
User assumes full legal responsibility.

---

## Quick Start

### Hardware Assembly
See [docs/hardware_guide.md](docs/hardware_guide.md) for complete BOM, schematics, and garment integration.

### Firmware Installation

**Arduino IDE:**
1. Install board packages for your platform
2. Install libraries: `Adafruit MPU6050`, `ArduinoJson`
3. Open `irwp_v15_firmware.ino`
4. **Edit LED counts** at top of file to match your hardware
5. Upload

**PlatformIO:**
```bash
pio run -e [esp32dev|pico|nano|stm32_bluepill] -t upload
```

3. Serial Commands (115200 baud)
- `ARM` / `DISARM` - Enable/disable patterns
- `START_CYCLE` - Begin autonomous attack
- `LOAD_PATTERN:0` - Load "AGC_Lock_5_Second"
- `GET_STATUS` - JSON system report
- `PING` - Health check

Full API: [docs/api_reference.md](docs/api_reference.md)

---

Project Structure

- `irwp_v15_firmware.ino` - Main firmware (monolithic, never shuts down)
- `platformio.ini` - Multi-platform build configuration
- `docs/hardware_guide.md` - Complete assembly instructions
- `docs/led_layout_diagram.png` - LED positioning visual guide
- `releases/` - Pre-compiled binaries

---

Legal
MIT License | Use at your own risk

Surveillance countermeasures are illegal in many regions. Educational/research purposes only.

```

---

## **docs/api_reference.md:**

```markdown
# IRWP v1.5 API Reference

## Serial Interface (115200 baud, 8N1)

### Commands
| Command | Response | Description |
|---------|----------|-------------|
| `ARM` | `ACK_ARMED` | Enable system (safety switch must be active) |
| `DISARM` | `ACK_DISARMED` | Stop all LEDs, return to idle |
| `START_CYCLE` | `CYCLE_STARTED` | Begin autonomous attack pattern |
| `STOP_CYCLE` | `CYCLE_STOPPED` | Halt cycle, remain armed |
| `LOAD_PATTERN:X` | `PATTERN_LOADED:name` | Load pattern 0-11 from library |
| `SET_TARGET:name` | `TARGET_SET:name` | Store target profile in EEPROM |
| `GET_STATUS` | JSON (see below) | Full system status report |
| `EMERGENCY` | `EMERGENCY_STOPPED` | Manual emergency halt (informational only) |
| `FACTORY_RESET` | `EEPROM_CLEARED` | Clear all stored configuration |
| `PING` | `PONG` | Health check |

### Status JSON Format
```json
{
  "version": "1.5",
  "state": 0,            // 0=IDLE, 1=ARMED, 2=CYCLING, 3=TESTMODE
  "safety": true,        // Safety switch state
  "armed": false,        // System active
  "cycle": 0,            // Global cycle counter
  "platform": "ESP32",   // Hardware platform
  "overheating": false,  // Thermal warning (>60°C)
  "temperature_c": 25.3, // TMP36 reading
  "led_power_w": 14.4,   // Calculated LED power
  "test_mode": false     // Test mode active
}
```

Error Messages
- `ERROR_SAFETY_DISABLED` - Safety switch is open
- `ERROR_NOT_ARMED` - Must ARM before START_CYCLE
- `ERROR_INVALID_PATTERN` - Pattern index out of range

Bluetooth (ESP32 only)
- Same commands/responses over BT
- Auto-discovery as "IRWP_v15"
