"""
Application settings and configuration
"""

import os
from pathlib import Path

# Application settings
APP_NAME = "Enhanced Psychiatric Records"
APP_VERSION = "1.0.0"
ORGANIZATION = "Psychiatric Records Team"

# Database settings
DATABASE_NAME = "psychiatric_records.db"
DATABASE_PATH = Path.home() / ".psychiatric_records" / DATABASE_NAME

# Ensure data directory exists
DATABASE_PATH.parent.mkdir(exist_ok=True)

# Encryption settings (for SQLCipher)
DATABASE_KEY = os.environ.get('PSYCHIATRIC_DB_KEY', 'default_development_key_change_in_production')

# UI settings
DEFAULT_THEME = "dark"
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800
WINDOW_DEFAULT_WIDTH = 1400
WINDOW_DEFAULT_HEIGHT = 1000

# Clinical settings
AUTO_SAVE_INTERVAL = 30  # seconds
BACKUP_INTERVAL = 3600  # 1 hour in seconds
MAX_RECENT_PATIENTS = 10

# Data validation settings
MAX_TEXT_LENGTH = 5000
MAX_NAME_LENGTH = 100
MAX_PHONE_LENGTH = 20
MAX_EMAIL_LENGTH = 255

# Export settings
EXPORT_FORMAT = "json"
ANONYMIZE_EXPORTS = True

# Logging settings
LOG_LEVEL = "INFO"
LOG_FILE = DATABASE_PATH.parent / "app.log"