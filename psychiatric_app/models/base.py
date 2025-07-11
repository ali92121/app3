"""
Base model class with common fields and functionality for all database models.
Provides audit fields, common utilities, and base configuration.
"""

import uuid
from datetime import datetime
from typing import Dict, Any

# We'll define Base here and import it in database.py to avoid circular imports
class BaseModel:
    """
    Abstract base model with common fields and methods for all database entities.
    Provides audit fields, timestamps, and common utilities.
    """
    
    def __init__(self):
        # Primary key (UUID)
        self.id = str(uuid.uuid4())
        
        # Audit fields
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.created_by = "system"
        self.updated_by = "system"
        
        # Soft delete support
        self.is_active = True
        self.deleted_at = None
    
    def __repr__(self):
        """String representation of the model."""
        return f"<{self.__class__.__name__}(id={self.id})>"
    
    def to_dict(self, include_relationships: bool = False) -> Dict[str, Any]:
        """
        Convert model instance to dictionary.
        
        Args:
            include_relationships: Whether to include relationship data
            
        Returns:
            Dictionary representation of the model
        """
        result = {}
        
        # Get all attributes that don't start with _
        for attr_name in dir(self):
            if not attr_name.startswith('_') and not callable(getattr(self, attr_name)):
                value = getattr(self, attr_name)
                
                # Handle datetime serialization
                if isinstance(value, datetime):
                    result[attr_name] = value.isoformat()
                else:
                    result[attr_name] = value
        
        return result
    
    def update_from_dict(self, data: Dict[str, Any], exclude_fields: list = None):
        """
        Update model instance from dictionary data.
        
        Args:
            data: Dictionary containing field values
            exclude_fields: List of fields to exclude from update
        """
        if exclude_fields is None:
            exclude_fields = ['id', 'created_at', 'created_by']
        
        for key, value in data.items():
            if key not in exclude_fields and hasattr(self, key):
                setattr(self, key, value)
        
        # Update the updated_at timestamp
        self.updated_at = datetime.utcnow()
    
    def soft_delete(self, deleted_by: str = "system"):
        """
        Perform soft delete by setting is_active to False.
        
        Args:
            deleted_by: User or system that performed the deletion
        """
        self.is_active = False
        self.deleted_at = datetime.utcnow()
        self.updated_by = deleted_by
        self.updated_at = datetime.utcnow()
    
    def restore(self, restored_by: str = "system"):
        """
        Restore a soft-deleted record.
        
        Args:
            restored_by: User or system that performed the restoration
        """
        self.is_active = True
        self.deleted_at = None
        self.updated_by = restored_by
        self.updated_at = datetime.utcnow()
    
    def validate(self) -> Dict[str, str]:
        """
        Validate the model instance and return any validation errors.
        
        Returns:
            Dictionary of field_name: error_message pairs
        """
        errors = {}
        
        # Basic validation - subclasses should override this method
        # to add specific validation rules
        
        return errors
    
    def is_valid(self) -> bool:
        """
        Check if the model instance is valid.
        
        Returns:
            True if valid, False otherwise
        """
        return len(self.validate()) == 0
    
    @property
    def age_in_days(self) -> int:
        """
        Calculate age in days since creation.
        
        Returns:
            Number of days since record was created
        """
        return (datetime.utcnow() - self.created_at).days
    
    @property
    def is_recently_updated(self) -> bool:
        """
        Check if record was updated in the last 24 hours.
        
        Returns:
            True if updated within 24 hours, False otherwise
        """
        time_diff = datetime.utcnow() - self.updated_at
        return time_diff.total_seconds() < 86400  # 24 hours in seconds

# This will be set by the database configuration
Base = None