"""
Database configuration and management for the Psychiatric Records System.
Uses SQLCipher for encrypted local database storage to ensure HIPAA compliance.
"""

import os
import logging
from pathlib import Path
from typing import Optional
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from cryptography.fernet import Fernet
import secrets

logger = logging.getLogger(__name__)

# Create base class for all models
Base = declarative_base()

class DatabaseManager:
    """
    Manages database connection, encryption, and session handling.
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager with optional custom database path.
        
        Args:
            db_path: Optional custom path for database file
        """
        self.app_dir = Path.home() / '.psychiatric_app'
        self.db_path = db_path or str(self.app_dir / 'data' / 'psychiatric_records.db')
        self.engine = None
        self.Session = None
        self._encryption_key = None
        
        # Ensure app directory exists
        self.app_dir.mkdir(parents=True, exist_ok=True)
        (self.app_dir / 'data').mkdir(parents=True, exist_ok=True)
        
    def _get_or_create_encryption_key(self) -> str:
        """
        Get existing encryption key or create a new one for database encryption.
        
        Returns:
            Database encryption key as string
        """
        key_file = self.app_dir / 'data' / '.db_key'
        
        if key_file.exists():
            try:
                with open(key_file, 'rb') as f:
                    key = f.read()
                logger.info("Loaded existing database encryption key")
                return key.decode('utf-8')
            except Exception as e:
                logger.warning(f"Failed to load existing key: {e}")
        
        # Generate new key
        key = secrets.token_urlsafe(32)
        try:
            with open(key_file, 'wb') as f:
                f.write(key.encode('utf-8'))
            # Set restrictive permissions (owner read/write only)
            os.chmod(key_file, 0o600)
            logger.info("Generated new database encryption key")
            return key
        except Exception as e:
            logger.error(f"Failed to save encryption key: {e}")
            raise
    
    def _create_engine(self):
        """
        Create SQLCipher encrypted database engine.
        
        Returns:
            SQLAlchemy engine with encryption enabled
        """
        try:
            # Get encryption key
            encryption_key = self._get_or_create_encryption_key()
            
            # Create SQLCipher connection string
            db_url = f"sqlite+pysqlcipher://:{encryption_key}@/{self.db_path}"
            
            # Create engine with optimizations
            engine = create_engine(
                db_url,
                echo=False,  # Set to True for SQL debugging
                pool_pre_ping=True,
                pool_recycle=300,
                connect_args={
                    'check_same_thread': False,
                    'timeout': 30
                }
            )
            
            # Set SQLCipher pragmas for security and performance
            @event.listens_for(engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                # Security settings
                cursor.execute("PRAGMA cipher_page_size = 4096")
                cursor.execute("PRAGMA kdf_iter = 256000")
                cursor.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA512")
                cursor.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA512")
                
                # Performance settings
                cursor.execute("PRAGMA journal_mode = WAL")
                cursor.execute("PRAGMA synchronous = NORMAL")
                cursor.execute("PRAGMA cache_size = 10000")
                cursor.execute("PRAGMA temp_store = memory")
                cursor.execute("PRAGMA mmap_size = 268435456")  # 256MB
                
                # Foreign key enforcement
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.close()
            
            logger.info(f"Created encrypted database engine for: {self.db_path}")
            return engine
            
        except Exception as e:
            logger.error(f"Failed to create database engine: {e}")
            raise
    
    def initialize_database(self):
        """
        Initialize database connection and create all tables.
        """
        try:
            # Create engine
            self.engine = self._create_engine()
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            
            # Create session factory
            self.Session = sessionmaker(bind=self.engine)
            
            # Import all models to ensure they're registered
            from ..models import patient, medication, lab_result, symptom_assessment
            
            # Create all tables
            Base.metadata.create_all(self.engine)
            
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def get_session(self):
        """
        Get a new database session.
        
        Returns:
            SQLAlchemy session instance
        """
        if not self.Session:
            raise RuntimeError("Database not initialized. Call initialize_database() first.")
        
        return self.Session()
    
    def close(self):
        """
        Close database connection and clean up resources.
        """
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")
    
    def backup_database(self, backup_path: str):
        """
        Create an encrypted backup of the database.
        
        Args:
            backup_path: Path where backup should be saved
        """
        try:
            import shutil
            
            # Ensure we have a valid session to close any transactions
            if self.engine:
                with self.engine.connect() as conn:
                    conn.execute("PRAGMA wal_checkpoint(FULL)")
            
            # Copy the database file
            shutil.copy2(self.db_path, backup_path)
            
            # Also backup the key file (to a separate location!)
            key_backup_path = f"{backup_path}.key"
            shutil.copy2(self.app_dir / 'data' / '.db_key', key_backup_path)
            
            logger.info(f"Database backed up to: {backup_path}")
            
        except Exception as e:
            logger.error(f"Failed to backup database: {e}")
            raise

# Global database manager instance
db_manager = None

def get_db_manager() -> DatabaseManager:
    """
    Get the global database manager instance.
    
    Returns:
        DatabaseManager instance
    """
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager

def get_db_session():
    """
    Convenience function to get a database session.
    
    Returns:
        SQLAlchemy session instance
    """
    return get_db_manager().get_session()

def init_db():
    """
    Initialize the database (convenience function).
    """
    get_db_manager().initialize_database()