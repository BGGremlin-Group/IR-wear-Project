import time
import json
import serial
from PyQt6.QtCore import QThread, pyqtSignal
from utils.logger import SimpleLogger

class SerialWorker(QThread):
    data_received = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    disconnected = pyqtSignal()
    
    def __init__(self, port: str, baud_rate: int = 115200):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.serial = None
        self.running = False
        self.command_queue = []
        self.logger = SimpleLogger("logs/serial.log")
    
    def run(self):
        try:
            self.serial = serial.Serial(self.port, self.baud_rate, timeout=0.1)
            time.sleep(2)  # Arduino reset
            
            if not self.serial.is_open:
                self.error_occurred.emit("Failed to open serial port")
                return
            
            self.running = True
            self.logger.log("SERIAL_OPEN", {"port": self.port, "baud": self.baud_rate})
            
            while self.running:
                # Send queued commands
                while self.command_queue:
                    cmd = self.command_queue.pop(0)
                    self.serial.write(json.dumps(cmd).encode() + b'\n')
                    self.logger.log("SERIAL_WRITE", cmd)
                
                # Read responses
                if self.serial.in_waiting:
                    try:
                        line = self.serial.readline()
                        if line:
                            data = json.loads(line.decode().strip())
                            self.data_received.emit(data)
                            self.logger.log("SERIAL_READ", data)
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        self.error_occurred.emit(f"Parse error: {e}")
                
                # Check disconnect
                if not self.serial.is_open:
                    self.disconnected.emit()
                    break
                
                time.sleep(0.01)
                
        except serial.SerialException as e:
            self.error_occurred.emit(f"Serial error: {e}")
        finally:
            if self.serial and self.serial.is_open:
                self.serial.close()
                self.logger.log("SERIAL_CLOSED", {})
    
    def send_command(self, cmd: dict):
        self.command_queue.append(cmd)
    
    def stop(self):
        self.running = False
        self.wait()
