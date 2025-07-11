"""
Medication model for tracking patient medications
"""

from sqlalchemy import Column, String, Float, Integer, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from psychiatric_app.models.base import BaseModel

class Medication(BaseModel):
    __tablename__ = 'medications'
    
    patient_id = Column(String, ForeignKey('patients.id'), nullable=False)
    
    # Medication Details
    name = Column(String(200), nullable=False)
    generic_name = Column(String(200))
    brand_name = Column(String(200))
    medication_class = Column(String(100))
    ndc_number = Column(String(50))  # National Drug Code
    
    # Dosage
    dose_amount = Column(Float)
    dose_unit = Column(String(50))  # mg, ml, etc.
    frequency = Column(String(100))  # BID, TID, QHS, etc.
    route = Column(String(50))  # PO, IM, IV, etc.
    instructions = Column(Text)  # Special instructions
    
    # Timing
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=True)
    
    # Clinical Response
    effectiveness = Column(Integer)  # 0-100 scale
    side_effects = Column(Text)  # JSON array
    adherence = Column(Integer)  # 0-100 scale
    
    # Clinical Context
    indication = Column(String(500))
    prescriber = Column(String(200))
    pharmacy = Column(String(200))
    notes = Column(Text)
    
    # Relationships
    patient = relationship("Patient", back_populates="medications")
    
    @property
    def dose_display(self):
        """Get formatted dose display"""
        if self.dose_amount and self.dose_unit:
            return f"{self.dose_amount} {self.dose_unit}"
        return "Dose not specified"
    
    @property
    def is_psychiatric(self):
        """Check if medication is psychiatric"""
        psychiatric_classes = [
            'antidepressant', 'antipsychotic', 'anxiolytic', 'mood stabilizer',
            'stimulant', 'sedative', 'hypnotic', 'anticonvulsant'
        ]
        if self.medication_class:
            return any(cls in self.medication_class.lower() for cls in psychiatric_classes)
        return False
    
    def __repr__(self):
        return f"<Medication(id={self.id}, name={self.name}, patient={self.patient_id})>"

# Add back reference to Patient model
from psychiatric_app.models.patient import Patient
Patient.medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")