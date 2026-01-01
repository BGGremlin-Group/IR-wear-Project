### Full Wiring Diagrams and Schematics

Detailed wiring diagrams and schematics for the IR LED setups in the project (e.g., hoodie with 20 LEDs, hat with 12, etc.). These are based on series-parallel configurations to efficiently manage voltage and current, using 940nm IR LEDs (~1.3V forward voltage, 20mA current).
ASCII representations for clarity, as well as references to visual Fritzing diagrams from online sources.
Since Fritzing files (.fzz) can be downloaded and opened in the free Fritzing software for interactive views, links to relevant projects with citations.
These can be adapted for your garments.

For all setups:
- Use current-limiting resistors per string to prevent burnout (calculated via Ohm's Law: R = (Supply V - Total LED V drop) / 0.02A).
- Safety: Add a 0.5A fuse in series with the battery positive for overload protection.
- Testing: Use a multimeter to verify ~20mA per LED string; view IR glow with a phone camera in night mode.

#### Hoodie/Pants Schematic (20 LEDs, 5 strings of 4 LEDs in series, 6V battery)
- **Configuration**: 5 parallel strings, each with 4 LEDs in series (total V drop ~5.2V). 40Ω resistor per string. Optional pulsing via 555 timer or microcontroller.
- **Why series-parallel?** Series matches battery voltage efficiently; parallel distributes current without overloading pins (total ~100mA).
- **ASCII Schematic**:
```
Battery Pack (4xAAA, 6V) [+] -- Toggle Switch -- + Bus (Distribute to 5 Resistors)
                                 |
                                 +-- 40Ω Res -- LED1 (A to C) -- LED2 (A to C) -- LED3 (A to C) -- LED4 (A to C) -- Common GND Bus (or Transistor Collector if Pulsing)
                                 +-- 40Ω Res -- [String 2: 4 LEDs Series]
                                 +-- 40Ω Res -- [String 3]
                                 +-- 40Ω Res -- [String 4]
                                 +-- 40Ω Res -- [String 5]
                                 |
Common GND Bus -- [-] Battery
```
- **Fritzing Visual**: Adapt from this multiple LED series project, which shows sequential LEDs (similar to strings) controlled by a sensor but modifiable for IR LEDs.
- Download the .fzz file for interactive wiring. Another example for IR-controlled LEDs (5 LEDs, adaptable to 20 by adding strings).

#### Hat Schematic (12 LEDs, 3 strings of 4 LEDs in series, 6V battery)
- **Configuration**: Similar to hoodie but scaled down (total ~60mA). Focus on brim for face obfuscation.
- **ASCII Schematic**:
```
Battery [+] -- Switch -- + Bus
                        |
                        +-- 40Ω -- LED1-4 Series -- GND Bus
                        +-- 40Ω -- LED5-8 Series -- GND Bus
                        +-- 40Ω -- LED9-12 Series -- GND Bus
                        |
Battery [-] -- GND Bus
```
- **Fritzing Visual**: Use this IR obstacle sensor diagram as a base (shows IR LED wiring; extend to multiple).
- For parallel LEDs: Reference this series-parallel explanation with diagrams.

#### Shoes Schematic (10 LEDs per shoe, 5 strings of 2 LEDs in series, 3V battery per shoe)
- **Configuration**: Independent per shoe for mobility (total ~100mA per shoe). 20Ω resistor per string (V drop ~2.6V).
- **ASCII Schematic** (Per Shoe):
```
Battery (2xAA, 3V) [+] -- Switch -- + Bus
                                  |
                                  +-- 20Ω -- LED1 (A-C) -- LED2 (A-C) -- GND Bus
                                  +-- 20Ω -- [String 2]
                                  +-- 20Ω -- [String 3]
                                  +-- 20Ω -- [String 4]
                                  +-- 20Ω -- [String 5]
                                  |
Battery [-] -- GND Bus
```
- **Fritzing Visual**: Based on this multiplexing LED setup (16 LEDs; scale down and adapt for series strings). For parallel wiring with microcontroller, see this guide:

For all: If using a transistor (e.g., 2N2222) for high current, connect the common cathode bus to the collector, emitter to GND, base to control pin via 1kΩ resistor.
Download Fritzing software (free) to import .fzz files from the linked projects and modify (e.g., replace visible LEDs with IR ones).

### Full Code to Induce Flicker (Half LEDs Flickering, Half Constant On)

This Arduino code is for the microcontroller version (e.g., Arduino Nano). It assumes two groups of LEDs:
- Group 1 (half, e.g., 10 LEDs in hoodie): Constant on (pin set HIGH).
- Group 2 (other half): Flickering via analogWrite for brightness variation (simulates flicker like candlelight).

Wire Group 1 directly to a digital pin (set HIGH; use transistor if >40mA total). Group 2 to a PWM pin (~) for fading.

**Assumptions**:
- Use PWM pin 9 for flickering group (via transistor for current).
- Constant group on pin 8.
- Add LDR on A0 for auto-activation in low light (optional).
- Adjust LED counts/resistors for your voltage (e.g., 5V Arduino).

**Full Arduino Code**:
```arduino
// IR LED Flicker Code: Half constant on, half flickering
// Adapt LED groups via transistors for current handling

const int constantPin = 8;    // Digital pin for constant ON group (half LEDs)
const int flickerPin = 9;     // PWM pin for flickering group (other half)
const int ldrPin = A0;        // LDR for low-light activation (optional)
int lightThreshold = 500;     // Adjust: Lower value = darker trigger

// Flicker pattern: Array of brightness values (0-255) for random flicker effect
byte flickerPattern[] = {180, 30, 89, 23, 255, 200, 90, 150, 60, 230, 180, 45, 90, 120, 210, 50, 170, 80, 240, 100};
const int patternSize = sizeof(flickerPattern) / sizeof(byte);

void setup() {
  pinMode(constantPin, OUTPUT);
  pinMode(flickerPin, OUTPUT);
  // No need for pinMode on analog A0
}

void loop() {
  int lightLevel = analogRead(ldrPin);  // Read ambient light
  
  if (lightLevel < lightThreshold) {    // Activate only in low light
    digitalWrite(constantPin, HIGH);    // Turn constant group ON
    
    // Flicker the other group
    for (int i = 0; i < patternSize; i++) {
      analogWrite(flickerPin, flickerPattern[i]);  // Set brightness
      delay(200);  // Adjust delay for flicker speed (200ms = slow flicker)
    }
  } else {
    digitalWrite(constantPin, LOW);       // Off in bright light
    analogWrite(flickerPin, 0);
  }
}
```

**Explanation**:
- **Constant Half**: Pin 8 is set HIGH, keeping those LEDs steadily on (full brightness).
- **Flickering Half**: Pin 9 uses analogWrite to cycle through brightness levels in the array, creating a flicker effect (e.g., dim to bright randomly). The array is from a tested flicker tutorial.
- **LDR Integration**: Auto-activates in low light to save battery and target night surveillance.
- **Customization**: For faster flicker, reduce delay(200) to 50-100ms. For random order, add random(i) in the loop. Upload via Arduino IDE; test on breadboard first.
- **Wiring for Code**: Connect constant group cathodes to transistor collector (base to pin 8 via 1kΩ). Flicker group to another transistor (base to pin 9). See ASCII above for LED strings.

### ***BGGG*** *Creating Unique Tools for Unique Individuals*
