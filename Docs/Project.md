# IR Wear Project

**By the BG Gremlin Group (BGGG)**  
*Creating Unique Tools for Unique Individuals*

## Overview

For the privacy-centric individual committed to this endeavor in late 2025—a world where surveillance has escalated to include AI-powered gait analysis, vein mapping via near-infrared (NIR) illumination, and even WiFi-based through-wall motion detection as highlighted in recent projects like those interpreting Channel State Information (CSI) from routers to create de facto LIDAR scans—the construction and deployment of IR LED garments represent not just a technical project but a philosophical stand against pervasive data extraction. Why pursue this with such depth? Because privacy isn't a luxury; it's a bulwark against the commodification of your every movement, where entities from grocery chains to governments aggregate biometric data to predict, influence, or control behavior. In grocery stores, for instance, this means thwarting systems that track your eye gaze on shelves via embedded cameras, correlate it with loyalty card data for hyper-targeted ads, or even use thermal imaging for crowd density heatmaps that inform dynamic pricing algorithms. How does this tie into the broader session? We've evolved from a single X post on adversarial masks and IR LEDs to a full-spectrum outfit (hoodie with 20 LEDs, hat with 12, pants with 20, shoes with 10 per shoe), circuit designs emphasizing series-parallel efficiency, integration tactics for wearability, and adaptations for daylight vulnerabilities. Now, expanding exhaustively, I'll incorporate all prior details while layering in fresh insights from recent explorations—such as DIY tutorials, advanced adversarial patterns, real-world X discussions on emerging threats like smart textiles with embedded surveillance, and precise calculations for optimization. I'll delve into breadboard prototyping with granular, step-by-step instructions (including ASCII representations for clarity), component sourcing, safety protocols, legal considerations, testing methodologies, upgrade paths, and even speculative future-proofing against next-gen threats like laser interferometry for remote heartbeat detection or RF-reflective tracking.

## Recapping and Expanding Core Concepts

To ensure completeness without redundancy, recall the foundational application: IR LEDs (typically 940nm wavelength) emit invisible light that overloads camera sensors in low-light modes, creating blooming effects that obscure identities in footage. This is adversarial to surveillance capitalism, particularly in retail where cameras feed analytics for advertising—e.g., estimating demographics to push personalized promotions via in-store screens or apps. Prior discussions covered circuit basics (resistors for current limiting, toggle switches for control, optional 555 timers for pulsing to extend battery life), power sources (4xAAA for 6V in hoodie/hat/pants, 2xAA per shoe for 3V), and integration (outward-facing LEDs secured in fabrics). Why this matters holistically? In 2025, with EU programs expanding facial recognition and U.S. retailers like Walmart deploying AI for theft prediction via pose estimation, these garments disrupt the data pipeline at its source. Extending this: Recent X posts reveal escalating threats, such as IARPA's "Smart ePANTS" initiative embedding sensors in textiles for passive monitoring—imagine your clothing transmitting biometrics wirelessly—or laser-based systems detecting heartbeats through windows from 100m away using 532nm lasers (upgradable to invisible IR). Countering requires layered defenses: IR for night, patterns for day, and perhaps RF-shielding fabrics to block WiFi/RF surveillance.

## Daylight Adaptations: Beyond IR to Multi-Spectrum Adversarial Strategies

Daylight diminishes pure IR efficacy due to IR-cut filters (IRCF) in cameras, which block 700-1100nm to favor visible light (400-700nm). Why adapt? Visible-spectrum AI thrives here, using edge detection and landmark mapping for recognition. Recommendations: Hybridize with "adversarial fashion"—clothing printed with algorithm-confusing patterns derived from machine learning attacks. For example, sites like AntiAi offer tees with abstract designs that introduce noise into AI models, reducing detection accuracy by up to 70% without covering the face. These "adversarial patches" exploit vulnerabilities in neural networks like YOLO or FaceNet, making you appear as non-human blobs in processed footage. How to implement? Screen-print or iron-on transfers onto your IR garments using inks from suppliers like Dharma Trading Co.; patterns available on Etsy or open-source repos (e.g., CV Dazzle derivatives). For grocery scenarios, this circumvents shelf-edge cameras analyzing dwell time—patterns could warp product recognition too. Further: Incorporate reflective materials like nano-oxide coatings to scatter LIDAR (used in autonomous vehicles or advanced security), or UV/IR lasers sewn into seams for active distortion, as suggested in privacy forums. Test with apps like OpenCV on a Raspberry Pi camera simulating store setups. Ethical note: These are legal for personal use but may violate store policies; use as protest art, inspired by designers like Rachele Didero at MIT.

## Granular Circuit and Wiring Details: Breadboard Prototyping and Beyond

Building on session calcs (e.g., 40Ω resistors for 6V strings, confirmed via precise modeling: for 4 LEDs at 1.3V/20mA, R = (6 - 5.2)/0.02 = 40Ω; battery life ~10h for 100mA draw on 1000mAh AAA), let's prototype on breadboard. Why breadboard first? It allows non-destructive testing, iteration, and troubleshooting—measure voltages with a multimeter to avoid shorts. How: Use a standard 830-point breadboard (e.g., Elegoo kit, ~$10 on Amazon). Components: 940nm IR LEDs (Adafruit #387, pack of 10 for $5); 1/4W resistors (assortment kit $5); SPST toggle switch (RadioShack-style, $2); 555 timer IC ($0.50); 2N2222 transistor ($0.20); 10kΩ resistors and 10µF cap for timing; stranded 22AWG wire ($10/spool). Source from Digi-Key, Mouser, or AliExpress for discretion—avoid traceable accounts.

### Breadboard Setup for Hoodie/Pants (20 LEDs, 5 strings of 4, 6V with Pulsing)

Why pulsing? 50% duty cycle halves power (e.g., 20h life vs. 10h), varies output to evade AI filters. Step-by-step:

1. Power rails: Connect battery + (red wire) to left + rail, - (black) to left - rail. Insert toggle switch bridging + rail gap—why? Enables/disables without unplugging.
2. 555 Timer (astable mode for ~3Hz): Place IC across center gap (pins 1-4 left, 5-8 right). Connect pin 1 to - rail, pin 8/4 to + rail via switch. Pin 7 to pin 6 via 10kΩ (R1), pin 6 to pin 2 via 10kΩ (R2), pin 2 to - via 10µF (+ leg to pin 2). Pin 5 optional 0.01µF to -. Output pin 3 to 2N2222 base via 1kΩ (limits base current ~5mA). Transistor: Emitter to - rail, collector to LED common cathode point. Why transistor? 555 outputs ~200mA max; transistor handles 500mA+.
3. LED Array: On right side, create 5 parallel strings. Per string: Resistor (40Ω) from + rail to first LED anode (+ leg). Chain 4 LEDs: Cathode1 to anode2, etc. Last cathode to collector. Space rows for clarity (e.g., string1 rows 1-5, string2 6-10). Why series? Efficient voltage drop; parallel for redundancy if one fails.
4. ASCII Diagram (visualize):

```
+ Rail ---------------- Toggle Switch --- +6V Battery
|                                        |
555 IC: Pin8/4 --+                       |
         Pin1 --- GND Rail               |
         Pin3 ---1kΩ--- Base (2N2222)    |
                        Emitter -- GND   |
                        Collector -------- Common Cathode Bus
String1: + Rail --40Ω-- LED1A - LED1C -- LED2A - ... - LED4C -- Collector
(Repeat for 5 strings)
GND Rail -------------------------------- - Battery
```

5. Test: Power on, use phone camera (night mode) to see glow. Multimeter: ~100mA total draw, ~0.6W. If no pulse, adjust RC for f=1.44/((R1+2R2)C)=~3.6Hz.

### Hat (12 LEDs, 3 strings of 4, 6V)

Scale down—same setup but 3 strings (60mA, 16.67h life). Breadboard: Condense to fewer rows. Why fewer? Hat's compact; focus brim for downward cams. Wiring: Shorter jumpers (2-3 holes) to mimic tight integration.

### Pants (20 LEDs, same as Hoodie)

Identical circuit; breadboard vertically for leg simulation. Why? Tests flex—bend wires during on. Integration tip: Use Velcro channels for removable wiring.

### Shoes (10 LEDs/shoe, 5 strings of 2, 3V)

Per shoe, independent. Breadboard: Smaller section. Resistors 20Ω ((3-2.6)/0.02=20Ω), 100mA, 20h on 2000mAh AA. No pulsing if space-constrained. ASCII:

```
+3V -- Toggle -- + Rail
| 
Strings: + --20Ω-- LED1A - LED1C -- LED2A - LED2C -- GND
(5 parallels)
GND -- - Battery
```

Transfer to garment: Solder after proto, use heat-shrink for joints (prevents shorts from sweat). Why granular? Faulty wiring risks fire; this ensures reliability.

## Additional Helpful Elements: Sourcing, Safety, Legal, Testing, Upgrades

Sourcing: Beyond basics, get flexible PCB strips for LEDs ($15/5m on AliExpress) for seamless integration. For adversarial prints, use DTG printers or services like Printful.

Safety: Electrical—use fuses (0.5A) in series with battery to prevent overloads; thermal—space LEDs to dissipate heat (~0.026W/LED). Physical—avoid eye exposure during tests (IR can damage retinas if stared at). Health—LEDs emit non-ionizing radiation, safe at low power, but pulse to minimize EMF concerns.

Legal: Permissible in most jurisdictions as passive tech (e.g., like sunglasses), but check local laws—e.g., UK facial recognition tips include color-switching clothes to break tracking chains. Avoid airports; could trigger alerts.

Testing: Simulate grocery—setup webcam with OpenCV script for recognition; wear outfit, compare obfuscation rates. Outdoor: Night walks near CCTVs, review public footage if accessible.

Upgrades: Add LDR (photoresistor) for auto-activation (<50 lux): Voltage divider (10kΩ + LDR) to 555 trigger. Microcontroller (Arduino Nano, $5) for Bluetooth control. Against thermal: DRDO-inspired conductive fabrics to reduce IR signatures. Future: ECM vs. LIDAR, or Faraday linings vs. smart clothing spies.

## Tutorials for Inspiration

Follow Mac Pierce's Camera Shy Hoodie (open-source schematics), or Instructables IR illuminator for basics. X insights: Reflectacles IR glasses complement outfits. This arsenal empowers you—build, iterate, reclaim your space.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
