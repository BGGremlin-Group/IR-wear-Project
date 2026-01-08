import time
import json
import serial
import serial.tools.list_ports
from PyQt6.QtCore import QObject, pyqtSignal
from gui.serial_worker import SerialWorker
from utils.logger import SimpleLogger

class ArduinoInterface(QObject):
    connected = pyqtSignal(str)
    disconnected = pyqtSignal()
    response_received = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.logger = SimpleLogger("logs/arduino.log")
        self.worker = None
        self.platform = "unknown"
        self._connected = False
    
    @property
    def connected(self) -> bool:
        return self._connected
    
    def detect_and_connect(self) -> bool:
        """Auto-detect and connect to microcontroller by VID/PID"""
        self.logger.log("AUTOCONNECT_START", {})
        
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            self.logger.log("NO_PORTS_FOUND", {})
            return False
        
        for port in ports:
            platform = self._detect_platform(port)
            if platform != "UNKNOWN":
                try:
                    self.worker = SerialWorker(port.device)
                    self.worker.data_received.connect(self._handle_response)
                    self.worker.error_occurred.connect(self._handle_error)
                    self.worker.disconnected.connect(self._handle_disconnect)
                    self.worker.start()
                    
                    self.platform = platform
                    self._connected = True
                    self.connected.emit(platform)
                    self.logger.log("CONNECTED", {"platform": platform, "port": port.device})
                    self.send_command("IDENTIFY")
                    return True
                    
                except Exception as e:
                    self.logger.log("CONNECTION_FAILED", {"error": str(e)})
        
        return False
    
    def _detect_platform(self, port) -> str:
        """Detect microcontroller platform from USB VID/PID"""
        if port.vid == 0x10C4 or "CP210" in port.description:
            return "ESP32"
        elif port.vid == 0x2E8A or "Pico" in port.description:
            return "PICO"
        elif port.vid in [0x2341, 0x2A03] or "Arduino" in port.description:
            return "ARDUINO"
        elif port.vid == 0x0483 or "STM32" in port.description:
            return "STM32"
        return "UNKNOWN"
    
    def connect_manual(self, port: str, baud: int = 115200) -> bool:
        """Manual connection to specific port"""
        try:
            self.worker = SerialWorker(port, baud)
            self.worker.data_received.connect(self._handle_response)
            self.worker.error_occurred.connect(self._handle_error)
            self.worker.disconnected.connect(self._handle_disconnect)
            self.worker.start()
            
            self._connected = True
            self.connected.emit("MANUAL")
            self.logger.log("MANUAL_CONNECTED", {"port": port, "baud": baud})
            return True
        except Exception as e:
            self.logger.log("MANUAL_CONNECTION_FAILED", {"error": str(e)})
            return False
    
    def _handle_response(self, data: dict):
        self.response_received.emit(data)
    
    def _handle_error(self, error: str):
        self.logger.log("SERIAL_ERROR", {"error": error})
    
    def _handle_disconnect(self):
        self._connected = False
        self.worker = None
        self.disconnected.emit()
        self.logger.log("DISCONNECTED", {})
    
    def send_command(self, cmd: str, params: dict = None):
        """Send command to microcontroller"""
        if self.worker and self._connected:
            payload = {"cmd": cmd, "params": params or {}}
            self.worker.send_command(payload)
            self.logger.log("COMMAND_SENT", payload)
        else:
            self.logger.log("COMMAND_FAILED", {"cmd": cmd, "reason": "not_connected"})
    
    def disconnect(self):
        """Disconnect from microcontroller"""
        if self.worker:
            self.worker.stop()
            self.worker = None
        self._connected = False
        self.logger.log("DISCONNECTED_MANUAL", {})
