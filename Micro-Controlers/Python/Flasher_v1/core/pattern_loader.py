import json
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal
from utils.logger import SimpleLogger

class PatternLoader(QObject):
    pattern_loaded = pyqtSignal(str, dict)
    pattern_error = pyqtSignal(str)
    
    def __init__(self, patterns_dir="user_attacks"):
        super().__init__()
        self.patterns_dir = Path(patterns_dir)
        self.patterns = {}
        self.logger = SimpleLogger("logs/patterns.log")
        self.load_patterns()
    
    def load_patterns(self):
        """Load built-in and custom attack patterns"""
        self.patterns_dir.mkdir(exist_ok=True)
        
        # Built-in patterns (embedded)
        self.patterns = {
            "AGC_LOCK": {
                "name": "AGC Lock 5-Second",
                "sequence": [
                    {"group": 4, "intensity": 255, "duration_ms": 50},
                    {"group": 4, "intensity": 0, "duration_ms": 50},
                    {"group": 4, "intensity": 255, "duration_ms": 50},
                    {"group": 4, "intensity": 0, "duration_ms": 50},
                    {"group": 4, "intensity": 255, "duration_ms": 50},
                    {"group": 4, "intensity": 0, "duration_ms": 50},
                    {"group": 4, "intensity": 255, "duration_ms": 50},
                    {"group": 4, "intensity": 0, "duration_ms": 50},
                    {"group": 4, "intensity": 255, "duration_ms": 5000}
                ],
                "repeat": 1
            },
            "SATURATION": {
                "name": "Sensor Saturation",
                "sequence": [{"group": 4, "intensity": 255, "duration_ms": 5000}],
                "repeat": 1
            },
            "FLICKER": {
                "name": "Rolling Shutter Flicker",
                "sequence": [{"group": 5, "intensity": 200, "duration_ms": 100}],
                "repeat": 3
            },
            "DAZZLE": {
                "name": "Face Dazzle",
                "sequence": [{"group": 1, "intensity": 255, "duration_ms": 3000}],
                "repeat": 5
            },
            "PTZ_JAM": {
                "name": "PTZ Tracking Jam",
                "sequence": [
                    {"group": i, "intensity": 200, "duration_ms": 100}
                    for i in range(4)
                ] * 20,
                "repeat": 1
            }
        }
        
        # Load custom patterns from user_attacks/
        for file in self.patterns_dir.glob("*.json"):
            try:
                with open(file) as f:
                    data = json.load(f)
                    if self._validate_pattern(data):
                        self.patterns[file.stem.upper()] = data
                        self.logger.log("PATTERN_LOADED", {"name": file.stem})
                    else:
                        self.logger.log("PATTERN_INVALID", {"file": str(file)})
                        self.pattern_error.emit(f"Invalid pattern: {file.name}")
            except Exception as e:
                self.logger.log("PATTERN_LOAD_ERROR", {"file": str(file), "error": str(e)})
                self.pattern_error.emit(f"Failed to load {file.name}: {e}")
    
    def _validate_pattern(self, pattern: dict) -> bool:
        """Validate pattern structure"""
        try:
            if "sequence" not in pattern or not isinstance(pattern["sequence"], list):
                return False
            for phase in pattern["sequence"]:
                if not all(k in phase for k in ["group", "intensity", "duration_ms"]):
                    return False
                if not (0 <= phase["intensity"] <= 255):
                    return False
            return True
        except:
            return False
    
    def get_pattern(self, name: str) -> dict:
        """Get pattern by name (case-insensitive)"""
        return self.patterns.get(name.upper(), {})
    
    def list_patterns(self) -> list:
        """List all available pattern names"""
        return sorted(self.patterns.keys())
