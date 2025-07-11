#!/usr/bin/env python3
"""
Main application entry point for the Psychiatric Records System.
Handles application initialization, database setup, and UI launch.
"""

import sys
import os
import logging
import traceback
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QIcon

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('psychiatric_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_application_directories():
    """Create necessary application directories if they don't exist."""
    app_dir = Path.home() / '.psychiatric_app'
    data_dir = app_dir / 'data'
    logs_dir = app_dir / 'logs'
    
    for directory in [app_dir, data_dir, logs_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    
    return app_dir

def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler for uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    
    # Show error dialog to user
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    try:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle("Application Error")
        msg_box.setText("An unexpected error occurred. The application will close.")
        msg_box.setDetailedText(error_msg)
        msg_box.exec()
    except:
        # If Qt is not available, just print to console
        print(f"Critical error: {error_msg}")

def main():
    """Main application entry point."""
    try:
        # Set up application directories
        app_dir = setup_application_directories()
        logger.info(f"Application directory: {app_dir}")
        
        # Set up global exception handler
        sys.excepthook = handle_exception
        
        # Create QApplication instance
        app = QApplication(sys.argv)
        app.setApplicationName("Psychiatric Records System")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Psychiatric Records Team")
        
        # Set application icon
        app_icon = QIcon()
        if os.path.exists("resources/icons/app_icon.png"):
            app_icon.addFile("resources/icons/app_icon.png")
            app.setWindowIcon(app_icon)
        
        # Import and initialize database
        try:
            from config.database import DatabaseManager
            db_manager = DatabaseManager()
            db_manager.initialize_database()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            QMessageBox.critical(
                None, 
                "Database Error", 
                f"Failed to initialize database: {str(e)}\n\nThe application cannot start without a database connection."
            )
            return 1
        
        # Import and create main window
        try:
            from ui.main_window import MainWindow
            main_window = MainWindow()
            main_window.show()
            logger.info("Main window created and displayed")
        except Exception as e:
            logger.error(f"Failed to create main window: {e}")
            QMessageBox.critical(
                None,
                "UI Error",
                f"Failed to create the main window: {str(e)}"
            )
            return 1
        
        # Start application event loop
        logger.info("Starting application event loop")
        return app.exec()
        
    except Exception as e:
        logger.critical(f"Fatal error during application startup: {e}")
        try:
            QMessageBox.critical(
                None,
                "Startup Error",
                f"Failed to start the application: {str(e)}"
            )
        except:
            print(f"Fatal startup error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    logger.info(f"Application exiting with code: {exit_code}")
    sys.exit(exit_code)