import time
import random
import queue
from PyQt6.QtCore import QThread, pyqtSignal
from utils.logger import SimpleLogger

class AttackOrchestrator(QThread):
    status_signal = pyqtSignal(str)
    cycle_signal = pyqtSignal(int)
    phase_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)
    
    def __init__(self, arduino, pattern_loader):
        super().__init__()
        self.arduino = arduino
        self.patterns = pattern_loader
        self.logger = SimpleLogger("logs/attacks.log")
        
        self.running = False
        self.safety_engaged = False
        self.config_queue = queue.Queue()
        self.pattern_queue = queue.Queue()
        
        self.config = {
            "targets": [],
            "camera_duration": 5000,
            "injection_duration": 3000,
            "jitter_range": 0.2,
            "max_cycles": 100,
            "pattern_name": "AGC_LOCK"
        }
        
        self.current_cycle = 0
        self.attack_queue = []
    
    def engage_safety(self):
        self.safety_engaged = True
        self.status_signal.emit("SAFETY ENGAGED")
        self.logger.log("SAFETY", {"state": "ENGAGED"})
    
    def disengage_safety(self):
        self.safety_engaged = False
        self.status_signal.emit("SAFETY DISENGAGED")
        self.logger.log("SAFETY", {"state": "DISENGAGED"})
        if self.running:
            self.stop_cycling()
    
    def update_config(self, config: dict):
        self.config_queue.put(config)
        self.logger.log("CONFIG_UPDATE", config)
    
    def load_pattern(self, pattern_name: str):
        self.pattern_queue.put(pattern_name)
        self.logger.log("PATTERN_REQUEST", {"name": pattern_name})
    
    def start_cycling(self):
        if not self.arduino.connected:
            self.error_signal.emit("Arduino not connected")
            return
        
        if not self.safety_engaged:
            self.error_signal.emit("Safety not engaged")
            return
        
        if not self.config["targets"]:
            self.error_signal.emit("No targets configured")
            return
        
        self.running = True
        self.current_cycle = 0
        self.start()
        self.status_signal.emit("ATTACK CYCLING STARTED")
        self.logger.log("CYCLING_START", self.config)
    
    def stop_cycling(self):
        self.running = False
        self.arduino.send_command("DISARM")
        self.status_signal.emit("ATTACK CYCLING STOPPED")
        self.logger.log("CYCLING_STOP", {"cycles": self.current_cycle})
    
    def run(self):
        self.build_attack_queue()
        
        while self.running:
            # Process config updates
            try:
                while True:
                    new_config = self.config_queue.get_nowait()
                    self.config.update(new_config)
                    self.build_attack_queue()
                    self.status_signal.emit("Config updated")
            except queue.Empty:
                pass
            
            # Process pattern changes
            try:
                while True:
                    pattern_name = self.pattern_queue.get_nowait()
                    if self.patterns.get_pattern(pattern_name):
                        self.config["pattern_name"] = pattern_name
                        self.build_attack_queue()
                        self.status_signal.emit(f"Pattern: {pattern_name}")
            except queue.Empty:
                pass
            
            # Check safety
            if not self.safety_engaged:
                self.error_signal.emit("SAFETY BREACH - ABORTING")
                self.running = False
                break
            
            # Execute attack queue
            for attack in self.attack_queue:
                if not self.running:
                    break
                
                self.execute_attack(attack)
                
                jitter = random.uniform(
                    1 - self.config["jitter_range"],
                    1 + self.config["jitter_range"]
                )
                sleep_time = attack["duration"] / 1000 * jitter
                time.sleep(sleep_time)
                
                time.sleep(0.5)
                
                self.current_cycle += 1
                self.cycle_signal.emit(self.current_cycle)
                
                if self.current_cycle >= self.config["max_cycles"]:
                    self.status_signal.emit("MAX CYCLES REACHED")
                    self.running = False
                    break
            
            if self.running:
                self.build_attack_queue()
        
        self.arduino.send_command("ALL_OFF")
        self.status_signal.emit("ORCHESTRATOR STOPPED")
        self.logger.log("ORCHESTRATOR_STOP", {})
    
    def build_attack_queue(self):
        pattern = self.patterns.get_pattern(self.config["pattern_name"])
        if not pattern:
            self.error_signal.emit(f"Pattern not found: {self.config['pattern_name']}")
            return
        
        self.attack_queue = []
        for target in self.config["targets"]:
            for repeat in range(pattern.get("repeat", 1)):
                for phase in pattern["sequence"]:
                    self.attack_queue.append({
                        "target": target,
                        "group": phase["group"],
                        "intensity": phase["intensity"],
                        "duration": phase.get("duration_ms", 1000),
                        "name": f"{target}_{pattern['name']}"
                    })
        
        random.shuffle(self.attack_queue)
        self.status_signal.emit(f"Queue: {len(self.attack_queue)} attacks")
    
    def execute_attack(self, attack: dict):
        self.phase_signal.emit(attack)
        self.status_signal.emit(f"[C{self.current_cycle}] {attack['name']}")
        self.logger.log("PHASE_EXEC", attack)
        
        self.arduino.send_command("SET_GROUP", {
            "group": attack["group"],
            "intensity": attack["intensity"]
        })
