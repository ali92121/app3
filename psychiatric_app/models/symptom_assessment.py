"""
Symptom assessment model for DSM-5 TR hierarchical symptom tracking
"""

from sqlalchemy import Column, String, Integer, Boolean, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from psychiatric_app.models.base import BaseModel

class SymptomAssessment(BaseModel):
    __tablename__ = 'symptom_assessments'
    
    patient_id = Column(String, ForeignKey('patients.id'), nullable=False)
    
    # DSM-5 Hierarchy
    category = Column(String(100), nullable=False)  # Mood Disorders, Anxiety Disorders, etc.
    disorder = Column(String(200), nullable=False)  # Major Depressive Disorder, etc.
    symptom_group = Column(String(200))  # core_symptoms, additional_symptoms, etc.
    symptom_name = Column(String(500), nullable=False)
    symptom_code = Column(String(20))  # A1, A2, etc.
    
    # Assessment Data
    is_present = Column(Boolean, default=False)
    severity = Column(String(50))  # None, Mild, Moderate, Severe
    severity_score = Column(Integer)  # 0-10 scale
    duration = Column(String(100))  # "2 weeks", "6 months", etc.
    onset_date = Column(Date)
    
    # Clinical Details
    frequency = Column(String(100))  # Daily, Weekly, etc.
    triggers = Column(Text)  # Environmental/situational triggers
    impact_functional = Column(Integer)  # 0-10 scale
    impact_occupational = Column(Integer)  # 0-10 scale
    impact_social = Column(Integer)  # 0-10 scale
    
    # Assessment Context
    assessment_date = Column(Date)
    assessed_by = Column(String(200))
    assessment_method = Column(String(100))  # Clinical interview, self-report, etc.
    
    # Notes and Comments
    clinical_notes = Column(Text)
    patient_description = Column(Text)
    collateral_information = Column(Text)
    
    # DSM-5 Criteria Tracking
    required_symptom = Column(Boolean, default=False)
    criteria_met = Column(Boolean, default=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="symptom_assessments")
    
    def get_severity_numeric(self):
        """Convert severity to numeric value for calculations"""
        severity_map = {
            "None": 0,
            "Mild": 1,
            "Moderate": 2,
            "Severe": 3
        }
        return severity_map.get(self.severity, 0)
    
    def __repr__(self):
        return f"<SymptomAssessment(id={self.id}, symptom={self.symptom_name}, present={self.is_present})>"

class DisorderDiagnosis(BaseModel):
    __tablename__ = 'disorder_diagnoses'
    
    patient_id = Column(String, ForeignKey('patients.id'), nullable=False)
    
    # Diagnosis Information
    disorder_category = Column(String(100), nullable=False)
    disorder_name = Column(String(200), nullable=False)
    icd_10_code = Column(String(20))
    dsm_5_code = Column(String(20))
    
    # Diagnosis Details
    diagnosis_date = Column(Date)
    diagnosed_by = Column(String(200))
    confidence_level = Column(String(50))  # Provisional, Confirmed, Rule Out
    
    # Severity and Specifiers
    severity = Column(String(50))  # Mild, Moderate, Severe
    episode_type = Column(String(100))  # Single Episode, Recurrent, etc.
    specifiers = Column(Text)  # JSON array of specifiers
    
    # Clinical Context
    criteria_met_count = Column(Integer)
    total_criteria = Column(Integer)
    onset_type = Column(String(100))  # Acute, Gradual, etc.
    
    # Treatment Planning
    treatment_priority = Column(Integer)  # 1-5 scale
    treatment_complexity = Column(String(50))  # Low, Moderate, High
    
    # Notes
    diagnostic_notes = Column(Text)
    differential_considerations = Column(Text)
    
    # Status
    is_primary_diagnosis = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    resolution_date = Column(Date)
    
    # Relationships
    patient = relationship("Patient", back_populates="diagnoses")
    
    def __repr__(self):
        return f"<DisorderDiagnosis(id={self.id}, disorder={self.disorder_name}, patient={self.patient_id})>"

# Add back references to Patient model
from psychiatric_app.models.patient import Patient
Patient.symptom_assessments = relationship("SymptomAssessment", back_populates="patient", cascade="all, delete-orphan")
Patient.diagnoses = relationship("DisorderDiagnosis", back_populates="patient", cascade="all, delete-orphan")