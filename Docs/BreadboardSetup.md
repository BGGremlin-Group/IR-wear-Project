### How-To: Breadboard Setup with Improved ASCII Diagrams (Including On-Off Switch and Battery Pack)

This how-to focuses on building the circuit on a breadboard for testing, with clear ASCII diagrams that include the on-off switch and battery pack. We've improved clarity by using labels, lines for connections, and separate sections for components. Diagrams represent a standard breadboard layout (rows 1-30 left/right, power rails).

**Step-by-Step Instructions:**
1. Set up power: Connect the battery pack (4xAAA for 6V) to the breadboard's power rails. Positive (+) to the red rail, negative (-) to the blue rail.
2. Add the toggle switch: Place it to control power flow from battery to the circuit.
3. Place the 555 timer IC and supporting components for pulsing.
4. Add the transistor for current handling.
5. Wire the LED strings in series-parallel.
6. Test with multimeter and IR camera app.

**Improved ASCII Diagram for Hoodie/Pants (20 LEDs, 5 strings of 4, 6V with Pulsing):**

```
Breadboard Layout (Left Side: Power and Timer; Right Side: LEDs)

+ Rail (Red) ----------------------------------------------------- +6V from Battery Pack (+)
|          Toggle Switch (SPST) - Breaks connection when off
|          |
555 IC (DIP-8): 
  Pin 1 (GND) ------------------ GND Rail (Blue) ---------------- - from Battery Pack (-)
  Pin 8 (VCC) --+ 
  Pin 4 (Reset) -| (Connected together to + Rail via Switch)
  Pin 7 -------- 10kΩ (R1) ------ Pin 6
  Pin 6 -------- 10kΩ (R2) ------ Pin 2
  Pin 2 -------- 10µF Cap (+ to Pin 2) -- GND Rail
  Pin 5 (optional) -- 0.01µF Cap -- GND Rail
  Pin 3 (Output) -- 1kΩ Resistor -- Base of 2N2222 Transistor

2N2222 Transistor:
  Base -- from Pin 3 via 1kΩ
  Emitter ----------------------- GND Rail
  Collector --------------------- Common Cathode Bus (for all LED strings)

LED Array (Right Side - 5 Parallel Strings):
String 1: + Rail -- 40Ω Res -- LED1 Anode -- Cathode -- LED2 Anode -- Cathode -- LED3 Anode -- Cathode -- LED4 Anode -- Cathode -- Collector
String 2: (Same as String 1, parallel from + Rail)
... (Repeat for Strings 3-5)

GND Rail --------------------------------------------------------- - Battery
```

**Explanation:** The diagram shows power flowing from battery through switch to + rail. The 555 creates a pulse signal amplified by the transistor, which switches the LEDs on/off. Each string has its resistor to limit current. This setup ensures even distribution and pulsing for efficiency. For hat, scale to 3 strings; for shoes, use 3V with 20Ω and 2-LED strings.

**Additional Diagram for Shoes (10 LEDs, 5 strings of 2, 3V - No Pulsing):**

```
Compact Breadboard Layout for One Shoe

+ Rail (Red) ---------------- Toggle Switch -- +3V Battery Pack (+)
|
LED Strings (5 Parallel):
String 1: + Rail -- 20Ω Res -- LED1 Anode -- Cathode -- LED2 Anode -- Cathode -- GND Rail
String 2: (Parallel from + Rail)
... (Strings 3-5)

GND Rail ------------------------------------- - Battery Pack (-)
```

**Explanation:** Simpler without timer; direct power through switch. Test by flipping switch and viewing LEDs via phone camera (they appear purple/white in IR mode).

**Additional Diagram for Hat (12 LEDs, 3 strings of 4, 6V with Pulsing):**

```
Breadboard Layout (Similar to Hoodie but Scaled)

+ Rail (Red) ----------------------------------------------------- +6V from Battery Pack (+)
|          Toggle Switch (SPST)
|          |
555 IC Setup (Identical to Hoodie Diagram Above)

Transistor Setup (Identical to Hoodie)

LED Array - 3 Parallel Strings:
String 1: + Rail -- 40Ω Res -- LED1 A-C -- LED2 A-C -- LED3 A-C -- LED4 A-C -- Collector
String 2: (Parallel)
String 3: (Parallel)

GND Rail --------------------------------------------------------- - Battery
```

**Explanation:** Reduced strings for compactness. Focus on brim placement during integration. Pulsing conserves power for longer wear.

**Additional Diagram for Pants (20 LEDs, 5 strings of 4, 6V with Pulsing):**

```
Extended Breadboard Layout (For Leg Simulation - Use Longer Jumpers)

+ Rail (Red) ----------------------------------------------------- +6V Belt-Mounted Battery (+)
|          Toggle Switch (Pocket-Accessible)
|          |
555 IC and Transistor (Identical to Hoodie)

LED Array - 5 Parallel Strings (Distribute Across Board to Mimic Legs):
Left Leg Strings 1-3: + Rail -- 40Ω -- LED Chain (4 Series) -- Collector
Right Leg Strings 4-5: (Parallel)

GND Rail --------------------------------------------------------- - Battery
```

**Explanation:** Use flexible wires to simulate movement. Bundle for harness during soldering. Ensures symmetry for gait disruption.

### How-To: Version with a Microcontroller

This how-to adds a microcontroller version using an Arduino Nano (compact, $5 on Amazon) for advanced control like pulsing, auto-activation via LDR, or Bluetooth. It replaces the 555 timer for programmability.

**Step-by-Step Instructions:**
1. Components: Arduino Nano, 940nm IR LEDs, resistors (as before), NPN transistor (or MOSFET like IRLZ44N for higher current), LDR (optional), battery pack (5V USB for Nano or 6V with regulator).
2. Wire: Power Nano from battery (VIN to +5-12V, GND to -). Use digital pin for PWM pulsing.
3. Code: Upload via Arduino IDE – simple blink or analogWrite for duty cycle.
4. Integrate: Solder after breadboard test; hide Nano in pocket.
5. For LDR: Connect to analog pin; activate LEDs if light < threshold.

**Arduino Code Example (for Pulsing with LDR):**
```arduino
const int ledPin = 9; // PWM to transistor
const int ldrPin = A0; // LDR input

void setup() {
  pinMode(ledPin, OUTPUT);
}

void loop() {
  int light = analogRead(ldrPin);
  if (light < 500) { // Threshold for low light
    analogWrite(ledPin, 128); // 50% duty
    delay(500);
    analogWrite(ledPin, 0);
    delay(500);
  } else {
    analogWrite(ledPin, 0); // Off in bright light
  }
}
```

**ASCII Diagram for Hoodie with Arduino (20 LEDs, 5V):**

```
Breadboard Layout

+ Rail (Red) -------------------------------- Toggle Switch -- +5V Battery/USB (+)
| 
Arduino Nano:
  VIN ------------------ + Rail (via Switch)
  GND ------------------ GND Rail (Blue) -- - Battery (-)
  D9 (PWM) -- 1kΩ Res -- Base of Transistor
  A0 --------------- LDR (Voltage Divider: + Rail -- LDR -- A0 -- 10kΩ -- GND)

Transistor (IRLZ44N MOSFET):
  Gate -- from D9
  Source --------------- GND Rail
  Drain ---------------- Common Cathode Bus

LED Array (Adjust for 5V: 3 LEDs/string, R=(5-3.9)/0.02=55Ω, ~7 strings for 21 LEDs):
String 1: + Rail -- 55Ω Res -- LED1 A-C -- LED2 A-C -- LED3 A-C -- Drain
(Parallel for others)

GND Rail ------------------------------------- - Battery
```

**Explanation:** Microcontroller allows software control – e.g., LDR reads light levels, activates pulsing only in low light to save battery. Code can vary frequency randomly to evade AI filters. PWM improves efficiency (50% duty ~ doubles runtime). Upgradable to Bluetooth (add HC-05 module to TX/RX pins) for app control via phone. For other garments, scale LED count and adjust voltage/resistors accordingly.

**Additional Diagram for Shoes with Microcontroller (10 LEDs, 3V - Use 3.3V Arduino like Nano Every):**

```
Compact Layout

+ Rail -------------------------------- Toggle -- +3.3V Battery (+)
| 
Nano:
  3.3V Out -- + Rail (or VIN if higher V)
  GND ------ GND Rail -- - Battery
  D9 ------- 1kΩ -- Transistor Gate
  A0 ------- LDR Divider

Transistor and LEDs (5 strings of 2, R=20Ω):
String 1: + -- 20Ω -- LED1 A-C -- LED2 A-C -- Drain
(Parallels)

GND ---------------------------------- - Battery
```

**Explanation:** Compact for shoes; LDR auto-activates for ground-level cams in dark.

### How-To: Bare Minimum Build (Twist and Tape/Glue)

This how-to is for a simple, no-solder build: Twist wires together, insulate with tape, glue battery pack. Ideal for quick prototypes, but less reliable (twists can loosen). No tools beyond wire strippers.

**Step-by-Step Instructions:**
1. Components: 940nm IR LEDs, resistors, battery pack, 22AWG wire, electrical tape, hot glue gun.
2. Cut/strip wires: 10-20cm segments, strip 1cm ends.
3. Twist connections: Clockwise for secure hold; anode (long leg) to cathode (short) for series.
4. Attach to battery: Twist + terminal to resistor/LED start, - to end cathodes.
5. Secure: Wrap each twist with tape to insulate/prevent shorts; hot glue LEDs to fabric, battery to pocket.
6. No switch: Direct connect for always-on; to add, twist switch in-line on + wire (break and reconnect via switch terminals).
7. Test: Connect battery, view with phone camera; if flickering/hot, check twists/resistors.

**ASCII Diagram for Basic Hoodie (20 LEDs, 5 strings of 4, 6V - No Pulsing):**

```
Battery Pack (4xAAA, + and - Terminals)

+ Terminal -- Twist -- Toggle Switch (Optional: Twist wires to switch terminals)
           |
           -- Twist to Parallel Bus: Split to 5 Resistors
              |
              String 1: -- 40Ω Res (Twist ends) -- LED1 Anode (Twist)
                                        -- LED1 Cathode -- Twist -- LED2 Anode
                                                          -- LED2 Cathode -- Twist -- LED3 Anode
                                                                            -- LED3 Cathode -- Twist -- LED4 Anode
                                                                                              -- LED4 Cathode -- Twist to Common - Bus
              Strings 2-5: (Same, twisted in parallel at + and - buses)

Common - Bus -- Twist -- - Terminal

Tape all twists. Glue LEDs outward on hood, wires inside seams, pack in pocket.
```

**Explanation:** Parallels at buses (twist all string starts together post-switch, ends to -). Resistor per string prevents overload. Simpler than solder but monitor for loose twists causing intermittence. Battery life ~10h; disconnect to turn off if no switch. For safety, tape exposed metal.

**Additional Diagram for Basic Shoes (10 LEDs/Shoe, 5 strings of 2, 3V):**

```
Per Shoe Battery (2xAA, +/-)

+ -- Twist -- (Switch) -- Parallel Bus to 5 Resistors
     |
     String 1: -- 20Ω -- LED1 A -- C -- LED2 A -- C -- Twist to - Bus
     Strings 2-5: (Parallel)

- Bus -- Twist -- - Terminal

Glue to insoles/edges; tape twists.
```

**Explanation:** Independent per shoe for mobility. Short wires reduce snags. Test one foot first.

**Additional Diagram for Basic Hat (12 LEDs, 3 strings of 4, 6V):**

```
Battery + -- Twist -- Switch -- Bus to 3 Resistors
           |
           String 1: -- 40Ω -- LED1-4 Series Chain -- - Bus
           Strings 2-3: (Parallel)

- Bus -- Twist -- Battery -

Glue to brim/crown; tape for sweat resistance.
```

**Explanation:** Compact twists for headwear. Emphasis on brim for face shielding.
