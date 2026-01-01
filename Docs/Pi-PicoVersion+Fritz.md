### How-To: Version with Raspberry Pi Pico Microcontroller

This how-to adapts the microcontroller version to the Raspberry Pi Pico (the small, low-cost microcontroller board from Raspberry Pi, ideal for wearables due to its compact size ~2.1x5.1cm and low power).
It uses MicroPython for programming (firmware downloadable from official site). The Pico replaces the Arduino Nano, offering similar GPIO (26 pins) but with built-in PWM on all pins for easy brightness control.
We'll control 20 LEDs (e.g., for hoodie): half (10 LEDs) constant on, half flickering via random PWM for a dynamic disruption effect (harder for AI to filter).

**Step-by-Step Instructions:**
1. **Components**: Raspberry Pi Pico (~$4), 940nm IR LEDs, resistors (e.g., 40Ω for 6V strings; adjust for Pico's 3.3V logic but 5V-tolerant pins – use 5V battery with level shifting if needed, or 3.3V direct), N-channel MOSFET (e.g., IRLZ44N) for high current (Pico pins max 3mA direct; MOSFET handles 100mA+), LDR (optional for auto-activation), battery pack (3.7V LiPo or 5V USB for simplicity), jumper wires.
2. **Setup MicroPython**: Download MicroPython UF2 from https://micropython.org/download/rp2-pico/, hold BOOTSEL button on Pico while connecting USB, drag UF2 to RPI-RP2 drive. Use Thonny IDE to code/run.
3. **Wire**: Power Pico via VSYS (pin 39) for 1.8-5.5V battery. Use GPIO pins for control. Split LEDs into two groups: constant (GPIO 15), flickering (GPIO 14 with PWM).
4. **Code**: Save as main.py on Pico for auto-run. Upload via Thonny.
5. **Integrate**: Solder after breadboard; mount Pico in pocket with wires to LEDs. For low light auto-activation, add LDR to ADC pin.
6. **Power**: ~100mA total draw; use rechargeable battery for ~10h runtime.

**Full MicroPython Code (Half LEDs Constant On, Half Flickering):**
```python
from machine import Pin, PWM, ADC
import random
import time

# Pin assignments (adapt as needed)
constant_pin = Pin(15, Pin.OUT)  # Constant ON group (half LEDs, via MOSFET gate)
flicker_pwm = PWM(Pin(14))       # Flickering group (PWM for brightness, via MOSFET gate)
ldr = ADC(Pin(26))               # LDR on ADC0 (GP26) for light sensing
flicker_pwm.freq(1000)           # PWM frequency (1kHz smooth)

light_threshold = 30000          # Adjust: Higher ADC value = brighter light (0-65535 range)

# MOSFET wiring: Gate to pin, Source to GND, Drain to LED common cathode

def main():
    while True:
        light_level = ldr.read_u16()  # Read light (brighter = higher value)
        
        if light_level < light_threshold:  # Activate in low light
            constant_pin.value(1)  # Turn constant half ON
            
            # Flicker the other half with random brightness
            for _ in range(20):  # Loop for ~4s cycle; adjust
                brightness = random.randint(0, 65535)  # Random PWM duty (0-65535 = 0-100%)
                flicker_pwm.duty_u16(brightness)
                time.sleep(0.2)  # 200ms delay for visible flicker; reduce for faster
        else:
            constant_pin.value(0)  # Off in bright light
            flicker_pwm.duty_u16(0)

main()
```

**Explanation:** 
- **Constant Half**: GPIO 15 set high, keeping those LEDs steadily on (full brightness via MOSFET).
- **Flickering Half**: PWM on GPIO 14 cycles random duty cycles (0-100%), creating a flicker effect (e.g., dim to bright irregularly). Randomness from `random.randint` evades AI patterns.
- **LDR Integration**: ADC reads light; activates only in dark to save battery and target surveillance.
- **Customization**: For faster flicker, reduce `time.sleep(0.2)` to 0.05-0.1. Add more randomness by varying sleep time. Test in Thonny; LEDs appear pulsing in phone camera IR view.
- **Power Efficiency**: PWM at 50% average duty doubles battery life for flickering group.

**ASCII Diagram for Hoodie with Pico (20 LEDs, 5V Battery – Adjust for 3.3V if Direct):**
```
Battery (5V) [+] -- Toggle Switch -- Pico VSYS (Pin 39)
                                     Pico GND (Pin 38) -- [-] Battery

Pico:
  GP15 -- 1kΩ Res -- MOSFET1 Gate (Constant Group)
  GP14 -- 1kΩ Res -- MOSFET2 Gate (Flicker Group)
  GP26 -- LDR (to 3.3V via 10kΩ Divider: 3.3V -- LDR -- GP26 -- 10kΩ -- GND)

MOSFET1 (Constant):
  Gate -- GP15
  Source -- GND
  Drain -- Common Cathode Bus1 (10 LEDs: 3 strings of 3-4, R=(5-3.9/5.2)/0.02 ≈55/40Ω)

MOSFET2 (Flicker):
  Gate -- GP14
  Source -- GND
  Drain -- Common Cathode Bus2 (Other 10 LEDs, similar strings)

LED String Example: +5V Bus -- Res -- LED1 A-C -- LED2 A-C -- ... -- Drain
```

**Explanation:** Split LEDs into two buses for groups. MOSFETs amplify Pico's low-current signals. For 3.3V logic, use 3.3V battery or level shifter if LEDs need 5V. Bundle wires for garment integration.

**Full Wiring Diagrams and Schematics**
- **Configuration**: Series-parallel as before, but controlled via Pico GPIO through MOSFETs for current. Total V drop per string ~5.2V for 4 LEDs (use 3-LED strings at 3.9V for 5V supply to avoid dimming).
- **ASCII Schematic (General for Pico-Controlled LEDs)**:
```
Battery [+] -- Switch -- +5V Bus (to LED Anodes via Res) & Pico VSYS
                       Pico GND -- GND Bus -- Battery [-]

Group 1 (Constant 10 LEDs - 3 parallel strings of ~3 LEDs):
+5V -- 55Ω -- LED Chain (Series) -- MOSFET1 Drain
MOSFET1 Source -- GND
MOSFET1 Gate -- 1kΩ -- Pico GP15

Group 2 (Flicker 10 LEDs - Similar):
+5V -- 55Ω -- LED Chain -- MOSFET2 Drain
MOSFET2 Source -- GND
MOSFET2 Gate -- 1kΩ -- Pico GP14 (PWM)

LDR: Pico 3.3V -- LDR -- GP26 -- 10kΩ -- GND
```
- **Adaptations**: For hat (12 LEDs): Split 6 constant/6 flicker. For shoes (10/shoe): Use per-shoe Pico if independent, or wire to one. For pants: Extend wires for legs.

**Fritzing Visual Diagrams**
- Download official Pico Fritzing part from Raspberry Pi: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html (includes .fzpz file for import into Fritzing software – free at https://fritzing.org/). Use it to build your circuit visually.
- Example Blinking LED Fritzing: http://multiwingspan.co.uk/pico.php?page=blink – Shows basic Pico + LED + resistor on breadboard; extend to multiple LEDs by duplicating.
- LED Bar/Control Example: https://nerdcave.xyz/docs/sunfounder/tutorial-2-led-bar-graph/ – Fritzing for LED arrays; adapt for IR LEDs.
- Forum Project: https://forum.fritzing.org/t/new-project-with-raspberry-pi-pico/20270 – Includes Pico with LEDs/buttons; download shared .fzz files for interactive wiring.
- To visualize: Open Fritzing, import Pico part, add LEDs/resistors/MOSFETs, connect as per ASCII. For high-current, add transistor symbols.

For other garments, scale LED groups similarly. If needed, test code on Pico breadboard before soldering.
