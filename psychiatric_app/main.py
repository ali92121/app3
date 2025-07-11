"""
Main entry point for the Enhanced Psychiatric Records Desktop Application
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import qdarktheme

# Add the parent directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from psychiatric_app.ui.main_window import MainWindow
from psychiatric_app.config.database import DatabaseManager
from psychiatric_app.ui.components.theme_manager import ThemeManager

class PsychiatricApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.setup_application()
        self.theme_manager = ThemeManager()
        self.db_manager = DatabaseManager()
        
    def setup_application(self):
        """Setup application-wide settings"""
        self.app.setApplicationName("Enhanced Psychiatric Records")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("Psychiatric Records Team")
        
        # Set application icon
        # self.app.setWindowIcon(QIcon("resources/icons/app_icon.png"))
        
        # Enable high DPI scaling
        self.app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        self.app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
    def initialize_database(self):
        """Initialize the database connection"""
        try:
            self.db_manager.initialize_database()
            return True
        except Exception as e:
            QMessageBox.critical(
                None,
                "Database Error",
                f"Failed to initialize database:\n{str(e)}\n\nThe application will exit."
            )
            return False
    
    def run(self):
        """Run the application"""
        # Initialize database
        if not self.initialize_database():
            return 1
        
        # Apply initial theme
        self.theme_manager.apply_theme("dark")
        
        # Create and show main window
        self.main_window = MainWindow()
        self.main_window.show()
        
        # Center the window on screen
        self.main_window.center_on_screen()
        
        return self.app.exec()

def main():
    """Main function to run the application"""
    try:
        app = PsychiatricApp()
        return app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())