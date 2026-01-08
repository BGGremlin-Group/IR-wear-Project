/*
 * esp32_firmware.ino
 * IRWP v2.5 - ESP32 Version
 * Compile with Arduino IDE (select ESP32 Dev Module) or PlatformIO
 */

#include <Arduino.h>
#include <WiFi.h>
#include <BluetoothSerial.h>
#include <esp32-hal-ledc.h>
#include <EEPROM.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>

// Pin Definitions
#define HAT_PIN     25
#define HOODIE_PIN  26
#define PANTS_PIN   27
#define SHOES_PIN   14
#define SAFETY_PIN  12
#define EMERGENCY_PIN 13
#define RELAY_PIN   10
#define STATUS_LED_PIN 2

// LED Specifications (5mm LEDs)
#define LED_COUNT_TOTAL 40
#define LED_CURRENT_MA  30  // Derated for thermal management

// System States
enum SystemState {
  STATE_IDLE = 0,
  STATE_ARMED = 1,
  STATE_CYCLING = 2,
  STATE_EMERGENCY = 99
};

SystemState currentState = STATE_IDLE;
bool safetyEngaged = false;
volatile bool emergencyTriggered = false;

// Attack Structures
struct AttackPhase {
  uint8_t ledGroup;
  uint16_t durationMs;
  uint8_t intensity;
};

struct AttackPattern {
  char name[48];
  uint8_t phaseCount;
  AttackPhase phases[20];
  uint8_t repeatCount;
};

// Built-in Attack Patterns
const AttackPattern PROVEN_PATTERNS[] = {
  {
    "AGC_Lock_5_Second", 9,
    {{4,50,255},{4,50,0},{4,50,255},{4,50,0},
     {4,50,255},{4,50,0},{4,50,255},{4,50,0},
     {4,5000,255}}, 1
  },
  {
    "Sensor_Saturation_Blast", 1,
    {{4,5000,255}}, 1
  },
  {
    "Rolling_Shutter_Flicker", 1,
    {{5,100,200}}, 3, true
  },
  {
    "Face_Dazzle_Anti_Biometric", 1,
    {{1,3000,255}}, 5, true
  }
};

#define PATTERN_COUNT (sizeof(PROVEN_PATTERNS) / sizeof(AttackPattern))

// Target Storage
struct TargetStore {
  char name[32];
  uint8_t cameraModels[15];
  bool hasALPR;
  bool hasAnalytics;
  bool isWireless;
};

TargetStore currentTarget;
AttackPattern currentPattern;
uint8_t currentPhaseIndex = 0;
uint32_t cycleStartTime = 0;
uint32_t globalCycleCount = 0;

// Hardware Interfaces
Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Serial.println("\nIRWP v2.5 ESP32 Firmware");
  
  // Safety pins
  pinMode(SAFETY_PIN, INPUT_PULLUP);
  pinMode(EMERGENCY_PIN, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
  attachInterrupt(digitalPinToInterrupt(EMERGENCY_PIN), emergencyISR, FALLING);
  
  // LED pins
  pinMode(HAT_PIN, OUTPUT);
  pinMode(HOODIE_PIN, OUTPUT);
  pinMode(PANTS_PIN, OUTPUT);
  pinMode(SHOES_PIN, OUTPUT);
  pinMode(STATUS_LED_PIN, OUTPUT);
  
  // ESP32-specific setup
  ledcSetup(0, 38000, 8);  // 38kHz PWM
  EEPROM.begin(512);
  
  // Disable WiFi/BT for power saving
  WiFi.mode(WIFI_OFF);
  btStop();
  
  // Initialize MPU6050
  if (mpu.begin()) {
    mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
    mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  }
  
  // Load last configuration
  EEPROM.get(0, currentTarget);
  EEPROM.get(128, currentPattern);
  
  digitalWrite(STATUS_LED_PIN, LOW);
  Serial.println("Firmware Initialized");
  Serial.print("LEDs: "); Serial.println(LED_COUNT_TOTAL);
}

void loop() {
  safetyEngaged = (digitalRead(SAFETY_PIN) == LOW);
  
  if (emergencyTriggered || !safetyEngaged) {
    if (currentState != STATE_IDLE) emergencyHandler();
    return;
  }
  
  processSerialCommand();
  processAutonomousCycle();
  
  // Bluetooth command processing (if enabled)
  // if (SerialBT.available()) { ... }
  
  delay(1);
}

void processSerialCommand() {
  if (!Serial.available()) return;
  
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  processCommand(cmd);
}

void processCommand(String cmd) {
  if (cmd == "ARM") {
    currentState = STATE_ARMED;
    Serial.println("ACK_ARMED");
  } else if (cmd == "DISARM") {
    currentState = STATE_IDLE;
    allLEDsOff();
    Serial.println("ACK_DISARMED");
  } else if (cmd == "START_CYCLE") {
    if (currentState == STATE_ARMED) {
      currentState = STATE_CYCLING;
      currentPhaseIndex = 0;
      cycleStartTime = millis();
      Serial.println("CYCLE_STARTED");
    }
  } else if (cmd == "STOP_CYCLE") {
    currentState = STATE_ARMED;
    Serial.println("CYCLE_STOPPED");
  } else if (cmd.startsWith("LOAD_PATTERN:")) {
    uint8_t idx = cmd.substring(13).toInt();
    if (idx < PATTERN_COUNT) {
      memcpy_P(&currentPattern, &PROVEN_PATTERNS[idx], sizeof(AttackPattern));
      Serial.print("PATTERN_LOADED:"); Serial.println(currentPattern.name);
    }
  } else if (cmd.startsWith("SET_GROUP:")) {
    // Parse: SET_GROUP:{group,intensity}
    int group = cmd.substring(10).toInt();
    int intensity = cmd.substring(cmd.indexOf(',') + 1).toInt();
    setLEDGroup(group, intensity);
    Serial.println("GROUP_SET");
  } else if (cmd == "EMERGENCY") {
    emergencyHandler();
  } else if (cmd == "GET_STATUS") {
    sendStatusJson();
  } else if (cmd == "IDENTIFY") {
    Serial.println("IRWP_ESP32_v2.5");
  }
}

void processAutonomousCycle() {
  if (currentState != STATE_CYCLING) return;
  
  unsigned long now = millis();
  if (now - cycleStartTime >= currentPattern.phases[currentPhaseIndex].durationMs) {
    executeCurrentPhase();
    currentPhaseIndex++;
    
    if (currentPhaseIndex >= currentPattern.phaseCount) {
      currentPhaseIndex = 0;
      globalCycleCount++;
      Serial.print("CYCLE_COMPLETE:"); Serial.println(globalCycleCount);
    }
    
    cycleStartTime = now;
  }
}

void executeCurrentPhase() {
  AttackPhase phase = currentPattern.phases[currentPhaseIndex];
  setLEDGroup(phase.ledGroup, phase.intensity);
}

void setLEDGroup(uint8_t group, uint8_t intensity) {
  digitalWrite(RELAY_PIN, HIGH); // Enable power relay
  
  // ESP32 PWM
  switch(group) {
    case 0: 
      ledcAttachPin(HAT_PIN, 0);
      ledcWrite(0, intensity);
      break;
    case 1:
      ledcAttachPin(HOODIE_PIN, 0);
      ledcWrite(0, intensity);
      break;
    case 2:
      ledcAttachPin(PANTS_PIN, 0);
      ledcWrite(0, intensity);
      break;
    case 3:
      ledcAttachPin(SHOES_PIN, 0);
      ledcWrite(0, intensity);
      break;
    case 4:
      ledcAttachPin(HAT_PIN, 0);
      ledcAttachPin(HOODIE_PIN, 0);
      ledcAttachPin(PANTS_PIN, 0);
      ledcAttachPin(SHOES_PIN, 0);
      ledcWrite(0, intensity);
      break;
    case 5:
      flickerAll(intensity);
      break;
  }
}

void flickerAll(uint8_t intensity) {
  for(uint8_t i = 0; i < 50; i++) {
    digitalWrite(HAT_PIN, (i % 2) * intensity);
    digitalWrite(HOODIE_PIN, ((i + 1) % 2) * intensity);
    digitalWrite(PANTS_PIN, ((i + 2) % 2) * intensity);
    digitalWrite(SHOES_PIN, ((i + 3) % 2) * intensity);
    delayMicroseconds(500);
  }
}

void allLEDsOff() {
  ledcDetachPin(HAT_PIN);
  ledcDetachPin(HOODIE_PIN);
  ledcDetachPin(PANTS_PIN);
  ledcDetachPin(SHOES_PIN);
  digitalWrite(HAT_PIN, LOW);
  digitalWrite(HOODIE_PIN, LOW);
  digitalWrite(PANTS_PIN, LOW);
  digitalWrite(SHOES_PIN, LOW);
  digitalWrite(RELAY_PIN, LOW);
}

void emergencyHandler() {
  emergencyTriggered = true;
  currentState = STATE_EMERGENCY;
  allLEDsOff();
  
  Serial.println("EMERGENCY_STOPPED");
  digitalWrite(STATUS_LED_PIN, HIGH);
  
  while(1) {
    digitalWrite(STATUS_LED_PIN, !digitalRead(STATUS_LED_PIN));
    delay(100);
  }
}

void emergencyISR() {
  emergencyTriggered = true;
}

void sendStatusJson() {
  Serial.print("{\"state\":");
  Serial.print(currentState);
  Serial.print(",\"safety\":");
  Serial.print(safetyEngaged);
  Serial.print(",\"armed\":");
  Serial.print(currentState != STATE_IDLE);
  Serial.print(",\"cycle\":");
  Serial.print(globalCycleCount);
  Serial.print(",\"platform\":\"ESP32\"}\n");
}
