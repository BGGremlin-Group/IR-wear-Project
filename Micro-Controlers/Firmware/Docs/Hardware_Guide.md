# IRWP v1.5 Hardware Assembly Guide
## Wearable IR Countermeasure System

**Document Version:** 1.5  
**Last Updated:** 2024  
**Safety Classification:** HIGH VOLTAGE / THERMAL HAZARD

---

## 1. Bill of Materials (BOM)

### 1.1 Core Electronics
| Qty | Component | Specification | Part Number | Critical |
|-----|-----------|---------------|-------------|----------|
| 1 | Microcontroller | ESP32 DevKit C / Pico / Nano / STM32 | ESP32-WROOM-32 | Yes |
| 40 | IR LED 5mm | 850nm or 940nm, 100mA max | OSRAM SFH 4547 | Yes |
| 4 | N-Channel MOSFET | 30V, 5A min, Logic Level | IRLZ44N | Yes |
| 4 | Current Limit Resistor | 150Ω 1W (for 12V, 50mA) | CFR-25JB-150R | Yes |
| 1 | Power Relay | 5V coil, 5A contacts | SRD-05VDC-SL-C | Yes |
| 1 | Temperature Sensor | TMP36 analog | TMP36GT9Z | No |
| 1 | IMU | MPU6050 6-DOF | GY-521 | No |
| 1 | Safety Switch | SPST Toggle, 5A rating | MC0002 | Yes |
| 1 | Test Button | Momentary, normally open | TL1105 | No |

### 1.2 Power System
| Qty | Component | Specification | Notes |
|-----|-----------|---------------|-------|
| 1 | Battery | 3S LiPo 11.1V 2200mAh | Or 12V DC supply |
| 1 | Buck Converter | 12V → 5V 3A | LM2596 module |
| 1 | Power Jack | DC 5.5/2.1mm barrel | Panel mount |
| 1 | Fuse | 2A fast-blow inline | REQUIRED |

### 1.3 Garment Integration
| Qty | Component | Specification |
|-----|-----------|---------------|
| 1 | Base Garment | Hoodie + pants (dark color) |
| 1 | Hat/Headgear | Baseball cap or beanie |
| 1 | Wiring Harness | 22 AWG stranded silicone wire |
| 40 | LED Holders | 5mm panel mount clips |
| 1 | Project Box | 100x60x25mm ABS |
| 1 | Velcro Tape | 3M adhesive backed |
| 1 | Thermal Paste | For LED cooling (optional |

---

## 2. Schematic Diagrams

### 2.1 High-Level System Architecture
```

[11.1V Battery] → [2A Fuse] → [Master Switch] → [Buck Converter] → [5V Rail]
↓
[Relay Common]
↓
[MCU GPIO] → [Relay Coil] → [GND]
[25,26,27,14] → [MOSFET Gates] → [LED Groups] → [Relay NO] → [12V Rail]

```

### 2.2 LED Group Driver (Per-Zone, Replicate 4x)
```

GPIO_PIN (3.3V) → 100Ω → MOSFET Gate
MOSFET Drain → LED Anode (+)
MOSFET Source → GND
LED Cathode (-) → 150Ω Resistor → GND

```

**Note:** For 12V operation with 50mA current:
- Forward voltage: 1.5V (IR LED)
- Resistor value: (12V - 1.5V) / 0.05A = **210Ω** (use 220Ω standard)

### 2.3 Microcontroller Connections

| MCU Pin | Connection | Direction | Protection |
|---------|------------|-----------|------------|
| GPIO 25 | MOSFET Gate (Hat) | Output | 100Ω series |
| GPIO 26 | MOSFET Gate (Hoodie) | Output | 100Ω series |
| GPIO 27 | MOSFET Gate (Pants) | Output | 100Ω series |
| GPIO 14 | MOSFET Gate (Shoes) | Output | 100Ω series |
| GPIO 12 | Safety Switch | Input | Internal pullup |
| GPIO 13 | Test Button | Input | Internal pullup |
| GPIO 10 | Relay Coil | Output | Flyback diode REQUIRED |
| GPIO 2 | Status LED | Output | 220Ω series |
| A0 (36) | TMP36 | Input | Direct |
| SDA | MPU6050 SDA | Bidir | 4.7kΩ pullup |
| SCL | MPU6050 SCL | Bidir | 4.7kΩ pullup |

---

## 3. LED Layout & Garment Integration

### 3.1 Recommended Spatial Distribution

**Hat Zone (8 LEDs):**
- **Position:** Front-facing arc, 45° spacing
- **Wavelength:** 850nm (semi-covert, longer range)
- **Pattern:** `H H H H H H H H` (continuous arc)
- **Angle:** 15° downward tilt
- **Mounting:** Sewn through cap brim

**Hoodie Zone (16 LEDs):**
- **Position:** 360° perimeter at chest/shoulder level
- **Wavelength:** 940nm (fully covert)
- **Pattern:** 4 clusters of 4 LEDs, 90° spacing
- **Angle:** Horizontal, slight outward tilt (10°)
- **Mounting:** Mounted on velcro strips for adjustability

**Pants Zone (12 LEDs):**
- **Position:** Knee to ankle, front-facing
- **Wavelength:** 850nm (ground reflection)
- **Pattern:** 2 columns of 6 LEDs per leg
- **Angle:** 30° downward (low-angle attack)
- **Spacing:** 100mm vertical gap

**Shoes Zone (4 LEDs):**
- **Position:** Toe caps
- **Wavelength:** 940nm (short-range dazzle)
- **Pattern:** 2 per shoe, forward-facing
- **Mounting:** Integrated into shoe tongue

### 3.2 Wiring Harness Design

**Zone Bundles:** Use 4-conductor ribbon cable per zone
- **Colors:** Red (12V+), Black (GND), White (Signal), Green (Signal GND)
- **Length:** Hat (500mm), Hoodie (800mm), Pants (1200mm), Shoes (1500mm)
- **Connectors:** JST-XH 4-pin at MCU box, soldered at LED end

---

## 4. Thermal Management

### 4.1 LED Thermal Calculations
```

Power per LED: 1.5V × 0.05A = 0.075W
Total power: 40 × 0.075W = 3W
Heat per LED: 60% of power = 0.045W per LED
Concentrated zones: Hoodie cluster = 16 × 0.045W = 0.72W

```

### 4.2 Garment Material Requirements
- **Outer layer:** Cotton or polyester (natural IR reflectivity)
- **Underlayer:** Heat-resistant fabric (Nomex recommended for 850nm)
- **Ventilation:** Mesh backing behind LED clusters
- **Duty Cycle:** Limit to 80% at ambient >30°C

---

## 5. Assembly Step-by-Step

### Step 1: Prepare LED Modules
1. Solder 150Ω resistor to cathode (short leg)
2. Solder 100mm wire to anode (long leg)
3. Heat-shrink all connections
4. Test each LED: 12V → resistor → LED → GND (verify 50mA)

### Step 2: Mount LEDs on Garment
1. Mark positions with fabric marker
2. Punch 5mm holes through garment
3. Insert LED holders from front
4. Snap LEDs into holders from rear
5. Route wires to central spine (main harness)

### Step 3: Build Driver Board
1. Solder 4x MOSFETs to prototyping PCB
2. Add gate resistors (100Ω) to each MOSFET
3. Solder relay with flyback diode (1N4007)
4. Add screw terminals for zone connections
5. Mount in project box with ventilation slots

### Step 4: Connect MCU
1. Solder header pins to MCU board
2. Connect SDA/SCL to MPU6050 (4.7kΩ pullups)
3. Wire all GPIOs to driver board
4. Connect TMP36 to A0
5. Install master switch on battery positive line

### Step 5: System Integration
1. Connect zone bundles to driver board
2. Route main harness to back pocket/belt
3. Install project box at lower back position
4. Velcro battery pack to opposite side
5. **CRITICAL:** Verify NO shorts before power-on

---

## 6. Safety Warnings & Hazards

### ⚠️ EYE SAFETY (CRITICAL)
- **850nm LEDs:** Semi-visible, direct exposure causes retinal damage
- **940nm LEDs:** Covert but equally dangerous

### ⚠️ THERMAL HAZARDS
- **Garment Temperature:** Can reach 50°C+ during extended use
- **Skin Contact Risk:** Wear undershirt, limit continuous operation(when/if able)
- **Battery Heat:** LiPo can swell above 60°C, monitor during use

### ⚠️ ELECTRICAL SAFARDS
- **12V @ 2A:** Can cause burns if shorted
- **Wire Routing:** Avoid pinch points (joints, seams)
- **Fuse:** **MANDATORY** - prevents battery fire
- **Water Resistance:** Not waterproof. High humidity can short 12V rail.

---

## 7. Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| All LEDs dim | Low battery voltage | Charge/replace 3S LiPo |
| One zone dead | MOSFET failure | Replace IRLZ44N |
| Flickering | Loose ground connection | Check harness continuity |
| MPU not detected | I2C pullup missing | Add 4.7kΩ to SDA/SCL |
| Overheat warnings | Ambient >35°C | Reduce duty cycle to 60% |
| Bluetooth not pairing | ESP32 only | Ensure `#define ESP32` present |
| EEPROM corruption | Power loss during write | Add 100µF cap to 5V rail |

---

## 8. Bill of Materials (Complete Kit)

**Total Cost Estimate:** $85-$120 USD (single unit)

- [ ] ESP32 DevKit C: $8
- [ ] 40x IR LEDs: $12
- [ ] 4x IRLZ44N: $4
- [ ] Resistors (assorted): $3
- [ ] 5V Relay: $2
- [ ] TMP36: $2
- [ ] MPU6050: $5
- [ ] Safety Switch: $3
- [ ] Test Button: $1
- [ ] Project Box: $4
- [ ] Battery + Charger: $25
- [ ] Wiring + Connectors: $10
- [ ] Dark Hoodie/Pants: $20

---

## 9. Scalability Notes

**LED Count Modification:**
- Change `#define LED_COUNT_*` values at top of firmware
- Recalculate resistor values: `R = (12V - 1.5V) / (LED_CURRENT_MA / 1000)`
- **Do not exceed 100mA per LED** (thermal limit)
- **Do not exceed 5A total** (relay/MOSFET limit)

**Zone Expansion:**
- Add GPIO defines for new zones
- Replicate MOSFET driver circuit
- Update `setLEDGroup()` switch statement
- Add new pattern definitions

---

**Document Author:** BG GREMLIN GROUP 
**Repository:** `[https://github.com/BGGremlin-Group/IR-wear-Project/main/Micro-Controlers/Firmware]
**License:** MIT (Hardware designs public domain)
