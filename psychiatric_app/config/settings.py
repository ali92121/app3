"""
Application settings and configuration for the Psychiatric Records System.
Handles default values, environment variables, and user preferences.
"""

import os
from pathlib import Path
from typing import Dict, Any

# Application Information
APP_NAME = "Psychiatric Records System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Psychiatric Records Team"

# File Paths
HOME_DIR = Path.home()
APP_DIR = HOME_DIR / '.psychiatric_app'
DATA_DIR = APP_DIR / 'data'
LOGS_DIR = APP_DIR / 'logs'
CONFIG_DIR = APP_DIR / 'config'

# Database Configuration
DATABASE_PATH = DATA_DIR / 'psychiatric_records.db'
BACKUP_DIR = DATA_DIR / 'backups'

# UI Configuration
DEFAULT_THEME = "dark"
AVAILABLE_THEMES = ["dark", "light"]
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 800
WINDOW_DEFAULT_WIDTH = 1400
WINDOW_DEFAULT_HEIGHT = 900

# Auto-save Configuration
AUTO_SAVE_ENABLED = True
AUTO_SAVE_INTERVAL = 30  # seconds

# Validation Settings
VALIDATION_ENABLED = True
STRICT_VALIDATION = False

# Performance Settings
MAX_RECENT_PATIENTS = 20
LAZY_LOADING_THRESHOLD = 100

# Security Settings
SESSION_TIMEOUT = 3600  # 1 hour in seconds
REQUIRE_PASSWORD = False  # Can be enabled for additional security

# Clinical Settings
DSM5_VERSION = "DSM-5-TR"
MEDICATION_SEARCH_LIMIT = 50
LAB_REFERENCE_RANGES_ENABLED = True

# Export Settings
EXPORT_FORMATS = ["pdf", "csv", "json"]
DEFAULT_EXPORT_FORMAT = "pdf"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE_SIZE = 10 * 1024 * 1024  # 10MB
LOG_BACKUP_COUNT = 5

class Settings:
    """
    Application settings manager with support for user preferences and environment variables.
    """
    
    def __init__(self):
        """Initialize settings with default values."""
        self._settings = self._load_default_settings()
        self._user_settings_file = CONFIG_DIR / 'user_settings.json'
        self._load_user_settings()
    
    def _load_default_settings(self) -> Dict[str, Any]:
        """Load default application settings."""
        return {
            "theme": DEFAULT_THEME,
            "window_geometry": {
                "width": WINDOW_DEFAULT_WIDTH,
                "height": WINDOW_DEFAULT_HEIGHT,
                "maximized": False
            },
            "auto_save": {
                "enabled": AUTO_SAVE_ENABLED,
                "interval": AUTO_SAVE_INTERVAL
            },
            "validation": {
                "enabled": VALIDATION_ENABLED,
                "strict": STRICT_VALIDATION
            },
            "performance": {
                "max_recent_patients": MAX_RECENT_PATIENTS,
                "lazy_loading_threshold": LAZY_LOADING_THRESHOLD
            },
            "clinical": {
                "dsm5_version": DSM5_VERSION,
                "medication_search_limit": MEDICATION_SEARCH_LIMIT,
                "lab_reference_ranges": LAB_REFERENCE_RANGES_ENABLED
            },
            "export": {
                "default_format": DEFAULT_EXPORT_FORMAT,
                "available_formats": EXPORT_FORMATS
            },
            "security": {
                "session_timeout": SESSION_TIMEOUT,
                "require_password": REQUIRE_PASSWORD
            },
            "logging": {
                "level": LOG_LEVEL,
                "file_size": LOG_FILE_SIZE,
                "backup_count": LOG_BACKUP_COUNT
            }
        }
    
    def _load_user_settings(self):
        """Load user-specific settings from file."""
        if self._user_settings_file.exists():
            try:
                import json
                with open(self._user_settings_file, 'r') as f:
                    user_settings = json.load(f)
                self._merge_settings(user_settings)
            except Exception as e:
                print(f"Warning: Failed to load user settings: {e}")
    
    def _merge_settings(self, user_settings: Dict[str, Any]):
        """Merge user settings with default settings."""
        def merge_dict(default: Dict, user: Dict) -> Dict:
            result = default.copy()
            for key, value in user.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dict(result[key], value)
                else:
                    result[key] = value
            return result
        
        self._settings = merge_dict(self._settings, user_settings)
    
    def get(self, key: str, default=None):
        """
        Get a setting value using dot notation.
        
        Args:
            key: Setting key (e.g., 'window_geometry.width')
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        keys = key.split('.')
        value = self._settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set a setting value using dot notation.
        
        Args:
            key: Setting key (e.g., 'window_geometry.width')
            value: Value to set
        """
        keys = key.split('.')
        setting = self._settings
        
        for k in keys[:-1]:
            if k not in setting:
                setting[k] = {}
            setting = setting[k]
        
        setting[keys[-1]] = value
    
    def save_user_settings(self):
        """Save current settings to user settings file."""
        try:
            import json
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            
            with open(self._user_settings_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save user settings: {e}")
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self._settings = self._load_default_settings()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all current settings."""
        return self._settings.copy()

# Global settings instance
_settings = None

def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings

def get_setting(key: str, default=None):
    """Convenience function to get a setting value."""
    return get_settings().get(key, default)

def set_setting(key: str, value: Any):
    """Convenience function to set a setting value."""
    get_settings().set(key, value)

def save_settings():
    """Convenience function to save settings."""
    get_settings().save_user_settings()

# Environment variable overrides
def load_env_overrides():
    """Load settings from environment variables."""
    settings = get_settings()
    
    # Database path override
    if 'PSYCHIATRIC_DB_PATH' in os.environ:
        settings.set('database.path', os.environ['PSYCHIATRIC_DB_PATH'])
    
    # Theme override
    if 'PSYCHIATRIC_THEME' in os.environ:
        theme = os.environ['PSYCHIATRIC_THEME']
        if theme in AVAILABLE_THEMES:
            settings.set('theme', theme)
    
    # Debug mode
    if 'PSYCHIATRIC_DEBUG' in os.environ:
        settings.set('logging.level', 'DEBUG')
    
    # Auto-save interval
    if 'PSYCHIATRIC_AUTOSAVE' in os.environ:
        try:
            interval = int(os.environ['PSYCHIATRIC_AUTOSAVE'])
            settings.set('auto_save.interval', interval)
        except ValueError:
            pass

# Load environment overrides on import
load_env_overrides()