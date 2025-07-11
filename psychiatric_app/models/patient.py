"""
Patient model with comprehensive demographics and contact information
"""

from sqlalchemy import Column, String, Date, Integer, Boolean, Text
from psychiatric_app.models.base import BaseModel

class Patient(BaseModel):
    __tablename__ = 'patients'
    
    # Basic Identity
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    preferred_name = Column(String(100))
    date_of_birth = Column(Date, nullable=False)
    age = Column(Integer)  # Auto-calculated
    gender = Column(String(50))
    biological_sex = Column(String(20))
    sexual_orientation = Column(String(50))
    gender_identity = Column(String(100))
    
    # Contact Information
    phone_primary = Column(String(20))
    phone_secondary = Column(String(20))
    email = Column(String(255))
    address_street = Column(String(255))
    address_city = Column(String(100))
    address_state = Column(String(50))
    address_zip = Column(String(20))
    address_country = Column(String(100), default="USA")
    
    # Emergency Contact
    emergency_name = Column(String(200))
    emergency_relationship = Column(String(100))
    emergency_phone = Column(String(20))
    emergency_email = Column(String(255))
    
    # Demographics
    race = Column(String(100))
    ethnicity = Column(String(100))
    primary_language = Column(String(50), default="English")
    secondary_languages = Column(Text)  # JSON array
    interpreter_needed = Column(Boolean, default=False)
    
    # Social History
    marital_status = Column(String(50))
    children_count = Column(Integer)
    living_situation = Column(String(100))
    housing_stability = Column(String(100))
    
    # Education
    education_level = Column(String(100))
    education_details = Column(Text)
    current_student = Column(Boolean, default=False)
    
    # Employment
    employment_status = Column(String(100))
    job_title = Column(String(200))
    employer = Column(String(200))
    work_schedule = Column(String(100))
    income_range = Column(String(50))
    financial_stress = Column(String(100))
    
    # Legal
    legal_issues = Column(Text)
    legal_guardian = Column(String(200))
    
    # Insurance & Medical
    insurance_primary = Column(String(200))
    insurance_secondary = Column(String(200))
    insurance_id = Column(String(100))
    primary_care_physician = Column(String(200))
    referred_by = Column(String(200))
    
    # System Fields
    created_by = Column(String(100))
    
    @property
    def full_name(self):
        """Get patient's full name"""
        name_parts = [self.first_name]
        if self.middle_name:
            name_parts.append(self.middle_name)
        name_parts.append(self.last_name)
        return " ".join(name_parts)
    
    @property
    def display_name(self):
        """Get patient's display name (preferred if available)"""
        return self.preferred_name or self.full_name
    
    def __repr__(self):
        return f"<Patient(id={self.id}, name={self.full_name})>"