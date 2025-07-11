"""
Lab result model for tracking laboratory tests and values
"""

from sqlalchemy import Column, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from psychiatric_app.models.base import BaseModel

class LabResult(BaseModel):
    __tablename__ = 'lab_results'
    
    patient_id = Column(String, ForeignKey('patients.id'), nullable=False)
    
    # Test Information
    test_name = Column(String(200), nullable=False)
    test_code = Column(String(50))  # CPT code or lab code
    test_category = Column(String(100))  # Chemistry, Hematology, etc.
    test_panel = Column(String(100))  # CMP, CBC, etc.
    
    # Results
    value = Column(Float)
    text_value = Column(String(500))  # For non-numeric results
    unit = Column(String(50))
    reference_range = Column(String(100))
    reference_min = Column(Float)
    reference_max = Column(Float)
    is_abnormal = Column(Boolean, default=False)
    abnormal_flag = Column(String(10))  # H, L, HH, LL
    
    # Dates and Context
    collection_date = Column(DateTime)
    result_date = Column(DateTime)
    report_date = Column(DateTime)
    
    # Clinical Context
    ordering_physician = Column(String(200))
    lab_facility = Column(String(200))
    specimen_type = Column(String(100))  # Blood, Urine, etc.
    fasting_status = Column(Boolean)
    
    # Notes and Comments
    interpretation = Column(Text)
    technician_notes = Column(Text)
    physician_notes = Column(Text)
    
    # Critical Values
    is_critical = Column(Boolean, default=False)
    critical_notified = Column(Boolean, default=False)
    critical_notify_date = Column(DateTime)
    
    # Relationships
    patient = relationship("Patient", back_populates="lab_results")
    
    @property
    def formatted_value(self):
        """Get formatted value with unit"""
        if self.text_value:
            return self.text_value
        elif self.value is not None:
            if self.unit:
                return f"{self.value} {self.unit}"
            return str(self.value)
        return "No result"
    
    @property
    def is_within_range(self):
        """Check if numeric value is within reference range"""
        if self.value is None or (self.reference_min is None and self.reference_max is None):
            return None
        
        within_range = True
        if self.reference_min is not None and self.value < self.reference_min:
            within_range = False
        if self.reference_max is not None and self.value > self.reference_max:
            within_range = False
        
        return within_range
    
    def determine_abnormal_flag(self):
        """Automatically determine abnormal flag based on reference ranges"""
        if self.value is None:
            return None
            
        if self.reference_min is not None and self.value < self.reference_min:
            # Significantly low
            if self.reference_min > 0 and self.value < (self.reference_min * 0.5):
                return "LL"
            return "L"
        elif self.reference_max is not None and self.value > self.reference_max:
            # Significantly high
            if self.value > (self.reference_max * 2):
                return "HH"
            return "H"
        
        return None
    
    def __repr__(self):
        return f"<LabResult(id={self.id}, test={self.test_name}, value={self.formatted_value})>"

# Add back reference to Patient model
from psychiatric_app.models.patient import Patient
Patient.lab_results = relationship("LabResult", back_populates="patient", cascade="all, delete-orphan")