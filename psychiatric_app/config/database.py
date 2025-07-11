"""
Database configuration and connection management using SQLAlchemy with SQLCipher
"""

import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from pathlib import Path
from psychiatric_app.config.settings import DATABASE_PATH, DATABASE_KEY

# Create base class for all models
Base = declarative_base()

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self.logger = logging.getLogger(__name__)
        
    def get_database_url(self):
        """Get SQLCipher database URL"""
        return f"sqlite+pysqlcipher://:{DATABASE_KEY}@/{DATABASE_PATH}"
    
    def initialize_database(self):
        """Initialize database connection and create tables"""
        try:
            # Create SQLCipher engine
            self.engine = create_engine(
                self.get_database_url(),
                poolclass=StaticPool,
                pool_pre_ping=True,
                echo=False  # Set to True for SQL debugging
            )
            
            # Set SQLCipher specific pragmas
            @event.listens_for(self.engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                # Enable foreign key constraints
                cursor.execute("PRAGMA foreign_keys=ON")
                # Set journal mode for better performance
                cursor.execute("PRAGMA journal_mode=WAL")
                # Set synchronous mode
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.close()
            
            # Create session factory
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Import all models to ensure they're registered
            from psychiatric_app.models import patient, medication, lab_result, symptom_assessment
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            
            self.logger.info(f"Database initialized successfully at {DATABASE_PATH}")
            return True
            
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise
    
    def get_session(self):
        """Get a new database session"""
        if self.SessionLocal is None:
            raise RuntimeError("Database not initialized. Call initialize_database() first.")
        return self.SessionLocal()
    
    def close_connection(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            self.logger.info("Database connection closed")

# Global database manager instance
db_manager = DatabaseManager()

def get_db():
    """Dependency to get database session"""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()