#!/usr/bin/env python3
"""
IRWP v2.5 Complete Controller
Entry point for multi-platform microcontroller application
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

def main():
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    Path("firmware").mkdir(exist_ok=True)
    Path("user_attacks").mkdir(exist_ok=True)
    
    app = QApplication(sys.argv)
    
    # Add tools to PATH if they exist locally
    if sys.platform != "win32":
        tools_dir = Path("tools")
        if tools_dir.exists():
            os.environ["PATH"] = str(tools_dir.absolute()) + os.pathsep + os.environ["PATH"]
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
