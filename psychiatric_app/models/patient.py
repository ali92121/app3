"""
Patient model for comprehensive patient demographics and information.
Includes all fields required for psychiatric practice documentation and compliance.
"""

from datetime import datetime, date
from typing import Dict, Any, Optional
from .base import BaseModel

class Patient(BaseModel):
    """
    Comprehensive patient model with demographics, contact, social, educational, 
    employment, and insurance information for psychiatric practice.
    """
    
    def __init__(self):
        super().__init__()
        
        # Basic Identity Information
        self.first_name: str = ""
        self.last_name: str = ""
        self.middle_name: Optional[str] = None
        self.preferred_name: Optional[str] = None
        self.date_of_birth: Optional[date] = None
        self.age: Optional[int] = None  # Auto-calculated
        self.gender: Optional[str] = None
        self.biological_sex: Optional[str] = None
        self.sexual_orientation: Optional[str] = None
        self.gender_identity: Optional[str] = None
        
        # Contact Information
        self.phone_primary: Optional[str] = None
        self.phone_secondary: Optional[str] = None
        self.email: Optional[str] = None
        self.address_street: Optional[str] = None
        self.address_city: Optional[str] = None
        self.address_state: Optional[str] = None
        self.address_zip: Optional[str] = None
        self.address_country: str = "USA"
        
        # Emergency Contact
        self.emergency_name: Optional[str] = None
        self.emergency_relationship: Optional[str] = None
        self.emergency_phone: Optional[str] = None
        self.emergency_email: Optional[str] = None
        
        # Demographics
        self.race: Optional[str] = None
        self.ethnicity: Optional[str] = None
        self.primary_language: str = "English"
        self.secondary_languages: Optional[str] = None  # JSON array as string
        self.interpreter_needed: bool = False
        
        # Social History
        self.marital_status: Optional[str] = None
        self.children_count: Optional[int] = None
        self.living_situation: Optional[str] = None
        self.housing_stability: Optional[str] = None
        
        # Education
        self.education_level: Optional[str] = None
        self.education_details: Optional[str] = None
        self.current_student: bool = False
        
        # Employment
        self.employment_status: Optional[str] = None
        self.job_title: Optional[str] = None
        self.employer: Optional[str] = None
        self.work_schedule: Optional[str] = None
        self.income_range: Optional[str] = None
        self.financial_stress: Optional[str] = None
        
        # Legal
        self.legal_issues: Optional[str] = None
        self.legal_guardian: Optional[str] = None
        
        # Insurance & Medical
        self.insurance_primary: Optional[str] = None
        self.insurance_secondary: Optional[str] = None
        self.insurance_id: Optional[str] = None
        self.primary_care_physician: Optional[str] = None
        self.referred_by: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        """Get formatted full name."""
        names = [self.first_name, self.middle_name, self.last_name]
        return " ".join(name for name in names if name)
    
    @property
    def display_name(self) -> str:
        """Get display name (preferred name if available, otherwise full name)."""
        if self.preferred_name:
            return f"{self.preferred_name} ({self.full_name})"
        return self.full_name
    
    @property
    def calculated_age(self) -> Optional[int]:
        """Calculate current age from date of birth."""
        if not self.date_of_birth:
            return None
        
        today = date.today()
        age = today.year - self.date_of_birth.year
        
        # Adjust if birthday hasn't occurred this year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        
        return age
    
    def update_age(self):
        """Update the age field based on date of birth."""
        self.age = self.calculated_age
    
    @property
    def formatted_address(self) -> str:
        """Get formatted address string."""
        address_parts = []
        
        if self.address_street:
            address_parts.append(self.address_street)
        
        city_state_zip = []
        if self.address_city:
            city_state_zip.append(self.address_city)
        if self.address_state:
            city_state_zip.append(self.address_state)
        if self.address_zip:
            city_state_zip.append(self.address_zip)
        
        if city_state_zip:
            address_parts.append(", ".join(city_state_zip))
        
        if self.address_country and self.address_country != "USA":
            address_parts.append(self.address_country)
        
        return "\n".join(address_parts)
    
    @property
    def contact_methods(self) -> Dict[str, str]:
        """Get available contact methods."""
        methods = {}
        
        if self.phone_primary:
            methods["Primary Phone"] = self.phone_primary
        if self.phone_secondary:
            methods["Secondary Phone"] = self.phone_secondary
        if self.email:
            methods["Email"] = self.email
        
        return methods
    
    @property
    def emergency_contact_info(self) -> Optional[Dict[str, str]]:
        """Get emergency contact information."""
        if not self.emergency_name:
            return None
        
        info = {"Name": self.emergency_name}
        
        if self.emergency_relationship:
            info["Relationship"] = self.emergency_relationship
        if self.emergency_phone:
            info["Phone"] = self.emergency_phone
        if self.emergency_email:
            info["Email"] = self.emergency_email
        
        return info
    
    def validate(self) -> Dict[str, str]:
        """
        Validate patient data and return any validation errors.
        
        Returns:
            Dictionary of field_name: error_message pairs
        """
        errors = super().validate()
        
        # Required fields validation
        if not self.first_name:
            errors["first_name"] = "First name is required"
        elif len(self.first_name) > 100:
            errors["first_name"] = "First name must be 100 characters or less"
        
        if not self.last_name:
            errors["last_name"] = "Last name is required"
        elif len(self.last_name) > 100:
            errors["last_name"] = "Last name must be 100 characters or less"
        
        # Date of birth validation
        if self.date_of_birth:
            if self.date_of_birth > date.today():
                errors["date_of_birth"] = "Date of birth cannot be in the future"
            elif self.date_of_birth.year < 1900:
                errors["date_of_birth"] = "Invalid date of birth"
        
        # Email validation (basic)
        if self.email:
            if "@" not in self.email or "." not in self.email:
                errors["email"] = "Invalid email format"
        
        # Phone number validation (basic)
        for phone_field in ["phone_primary", "phone_secondary", "emergency_phone"]:
            phone_value = getattr(self, phone_field)
            if phone_value:
                # Remove common formatting characters
                clean_phone = "".join(c for c in phone_value if c.isdigit())
                if len(clean_phone) < 10:
                    errors[phone_field] = "Phone number must be at least 10 digits"
        
        # Age consistency validation
        if self.date_of_birth and self.age:
            calculated_age = self.calculated_age
            if calculated_age and abs(self.age - calculated_age) > 1:
                errors["age"] = "Age does not match date of birth"
        
        return errors
    
    def get_demographics_summary(self) -> Dict[str, Any]:
        """Get a summary of key demographic information."""
        return {
            "name": self.display_name,
            "age": self.calculated_age or self.age,
            "gender": self.gender,
            "race": self.race,
            "ethnicity": self.ethnicity,
            "primary_language": self.primary_language,
            "marital_status": self.marital_status,
            "employment": self.employment_status,
            "education": self.education_level
        }
    
    def get_contact_summary(self) -> Dict[str, Any]:
        """Get a summary of contact information."""
        return {
            "phone": self.phone_primary,
            "email": self.email,
            "address": self.formatted_address.replace("\n", ", ") if self.formatted_address else None,
            "emergency_contact": self.emergency_contact_info
        }
    
    def update_from_form_data(self, form_data: Dict[str, Any]):
        """
        Update patient from form data with specific handling for special fields.
        
        Args:
            form_data: Dictionary containing form field values
        """
        # Handle date of birth conversion
        if "date_of_birth" in form_data and form_data["date_of_birth"]:
            if isinstance(form_data["date_of_birth"], str):
                try:
                    form_data["date_of_birth"] = datetime.strptime(
                        form_data["date_of_birth"], "%Y-%m-%d"
                    ).date()
                except ValueError:
                    # Remove invalid date
                    del form_data["date_of_birth"]
        
        # Handle boolean fields
        boolean_fields = ["interpreter_needed", "current_student"]
        for field in boolean_fields:
            if field in form_data:
                if isinstance(form_data[field], str):
                    form_data[field] = form_data[field].lower() in ["true", "1", "yes", "on"]
        
        # Handle integer fields
        integer_fields = ["children_count", "age"]
        for field in integer_fields:
            if field in form_data and form_data[field]:
                try:
                    form_data[field] = int(form_data[field])
                except (ValueError, TypeError):
                    form_data[field] = None
        
        # Update using base method
        self.update_from_dict(form_data)
        
        # Auto-update age if date of birth was provided
        if "date_of_birth" in form_data:
            self.update_age()
    
    def __str__(self):
        """String representation for display purposes."""
        return f"{self.display_name} (ID: {self.id[:8]}...)"