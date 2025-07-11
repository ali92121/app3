"""
Symptom Assessment model for DSM-5 TR hierarchical symptom tracking and clinical assessment.
Includes comprehensive mental health symptom documentation and diagnosis support.
"""

from datetime import datetime, date
from typing import Dict, Any, Optional, List
from .base import BaseModel
import json

class SymptomAssessment(BaseModel):
    """
    Comprehensive symptom assessment model for tracking DSM-5 TR symptoms,
    including hierarchical organization, severity ratings, and clinical notes.
    """
    
    def __init__(self):
        super().__init__()
        
        # Foreign key reference (stored as string in this implementation)
        self.patient_id: str = ""
        
        # Assessment Session Information
        self.assessment_date: Optional[date] = None
        self.assessment_type: str = "Initial"  # Initial, Follow-up, Crisis, etc.
        self.assessor: Optional[str] = None
        self.session_duration: Optional[int] = None  # Duration in minutes
        
        # DSM-5 TR Hierarchy Information
        self.category: str = ""  # e.g., "Mood Disorders"
        self.disorder: str = ""  # e.g., "Major Depressive Disorder"
        self.symptom_group: Optional[str] = None  # e.g., "core_symptoms"
        self.symptom_code: str = ""  # e.g., "A1"
        self.symptom_name: str = ""  # e.g., "Depressed mood"
        
        # Symptom Presence and Characteristics
        self.is_present: bool = False
        self.is_required: bool = False  # Whether this is a required symptom for diagnosis
        self.severity: Optional[str] = None  # None, Mild, Moderate, Severe
        self.severity_score: Optional[int] = None  # 0-10 scale
        self.frequency: Optional[str] = None  # Daily, Weekly, Intermittent, etc.
        self.duration: Optional[str] = None  # e.g., "2 weeks", "6 months"
        self.duration_weeks: Optional[int] = None  # Numeric duration in weeks
        
        # Clinical Context
        self.onset_date: Optional[date] = None
        self.onset_description: Optional[str] = None  # Gradual, Sudden, etc.
        self.triggers: Optional[str] = None  # JSON array as string
        self.precipitating_factors: Optional[str] = None
        self.alleviating_factors: Optional[str] = None
        self.impact_level: Optional[str] = None  # Minimal, Mild, Moderate, Severe
        
        # Functional Impairment
        self.functional_impairment: bool = False
        self.work_impairment: Optional[str] = None
        self.social_impairment: Optional[str] = None
        self.relationship_impairment: Optional[str] = None
        self.daily_living_impairment: Optional[str] = None
        
        # Associated Features
        self.associated_symptoms: Optional[str] = None  # JSON array as string
        self.comorbid_conditions: Optional[str] = None
        self.substance_related: bool = False
        self.medical_condition_related: bool = False
        
        # Assessment Tools and Scales
        self.assessment_scale: Optional[str] = None  # PHQ-9, GAD-7, etc.
        self.scale_score: Optional[int] = None
        self.scale_interpretation: Optional[str] = None
        
        # Clinical Notes and Observations
        self.clinical_notes: Optional[str] = None
        self.behavioral_observations: Optional[str] = None
        self.patient_report: Optional[str] = None
        self.collateral_information: Optional[str] = None
        
        # Treatment Planning
        self.treatment_target: bool = False
        self.treatment_priority: Optional[int] = None  # 1 (highest) to 10 (lowest)
        self.treatment_approach: Optional[str] = None
        self.treatment_goals: Optional[str] = None
        
        # Progress Tracking
        self.baseline_severity: Optional[int] = None
        self.previous_severity: Optional[int] = None
        self.improvement_percentage: Optional[float] = None
        self.response_to_treatment: Optional[str] = None  # Excellent, Good, Partial, Poor, None
    
    @property
    def symptom_hierarchy_path(self) -> str:
        """Get the full hierarchical path of the symptom."""
        path_parts = [self.category, self.disorder]
        if self.symptom_group:
            path_parts.append(self.symptom_group)
        path_parts.append(self.symptom_name)
        return " > ".join(path_parts)
    
    @property
    def display_name(self) -> str:
        """Get formatted symptom name for display."""
        if self.symptom_code:
            return f"{self.symptom_code}: {self.symptom_name}"
        return self.symptom_name
    
    @property
    def severity_description(self) -> str:
        """Get text description of severity."""
        if self.severity:
            return self.severity
        elif self.severity_score is not None:
            if self.severity_score <= 2:
                return "Minimal"
            elif self.severity_score <= 4:
                return "Mild"
            elif self.severity_score <= 6:
                return "Moderate"
            elif self.severity_score <= 8:
                return "Severe"
            else:
                return "Extreme"
        return "Not rated"
    
    @property
    def days_since_onset(self) -> Optional[int]:
        """Calculate days since symptom onset."""
        if not self.onset_date:
            return None
        return (date.today() - self.onset_date).days
    
    @property
    def weeks_since_onset(self) -> Optional[float]:
        """Calculate weeks since symptom onset."""
        days = self.days_since_onset
        return round(days / 7, 1) if days is not None else None
    
    @property
    def is_chronic(self) -> bool:
        """Check if symptom is considered chronic (>6 months)."""
        weeks = self.weeks_since_onset
        return weeks is not None and weeks >= 26
    
    @property
    def requires_attention(self) -> bool:
        """Check if symptom requires immediate clinical attention."""
        return (
            self.is_present and 
            (self.severity in ["Severe", "Extreme"] or 
             (self.severity_score is not None and self.severity_score >= 7) or
             self.functional_impairment)
        )
    
    def get_triggers_list(self) -> List[str]:
        """Get list of triggers from JSON string."""
        if not self.triggers:
            return []
        
        try:
            return json.loads(self.triggers)
        except (json.JSONDecodeError, TypeError):
            return [trigger.strip() for trigger in self.triggers.split(",") if trigger.strip()]
    
    def set_triggers_list(self, triggers: List[str]):
        """Set triggers from list."""
        self.triggers = json.dumps(triggers)
    
    def get_associated_symptoms_list(self) -> List[str]:
        """Get list of associated symptoms from JSON string."""
        if not self.associated_symptoms:
            return []
        
        try:
            return json.loads(self.associated_symptoms)
        except (json.JSONDecodeError, TypeError):
            return [symptom.strip() for symptom in self.associated_symptoms.split(",") if symptom.strip()]
    
    def set_associated_symptoms_list(self, symptoms: List[str]):
        """Set associated symptoms from list."""
        self.associated_symptoms = json.dumps(symptoms)
    
    def calculate_improvement(self) -> Optional[float]:
        """Calculate improvement percentage from baseline."""
        if self.baseline_severity is None or self.severity_score is None:
            return None
        
        if self.baseline_severity == 0:
            return 0.0
        
        improvement = ((self.baseline_severity - self.severity_score) / self.baseline_severity) * 100
        self.improvement_percentage = round(improvement, 1)
        return self.improvement_percentage
    
    def update_severity_trend(self, new_severity: int):
        """Update severity with trend tracking."""
        self.previous_severity = self.severity_score
        self.severity_score = new_severity
        
        # Update text severity based on score
        if new_severity <= 2:
            self.severity = "Minimal"
        elif new_severity <= 4:
            self.severity = "Mild"
        elif new_severity <= 6:
            self.severity = "Moderate"
        elif new_severity <= 8:
            self.severity = "Severe"
        else:
            self.severity = "Extreme"
        
        # Calculate improvement
        self.calculate_improvement()
    
    @property
    def severity_trend(self) -> Optional[str]:
        """Get trend description compared to previous assessment."""
        if self.previous_severity is None or self.severity_score is None:
            return None
        
        diff = self.severity_score - self.previous_severity
        
        if abs(diff) <= 1:
            return "Stable"
        elif diff > 0:
            return f"Worsened ({diff:+d})"
        else:
            return f"Improved ({diff:+d})"
    
    def meets_dsm5_criteria(self, disorder_criteria: Dict[str, Any]) -> bool:
        """
        Check if symptom meets DSM-5 criteria for a specific disorder.
        
        Args:
            disorder_criteria: Dictionary containing DSM-5 criteria for the disorder
            
        Returns:
            True if criteria are met, False otherwise
        """
        # This is a simplified version - full implementation would need comprehensive DSM-5 criteria
        if not self.is_present:
            return False
        
        # Check duration requirements
        if "min_duration_weeks" in disorder_criteria:
            if self.duration_weeks is None or self.duration_weeks < disorder_criteria["min_duration_weeks"]:
                return False
        
        # Check severity requirements
        if "min_severity" in disorder_criteria:
            severity_map = {"Minimal": 1, "Mild": 2, "Moderate": 3, "Severe": 4, "Extreme": 5}
            current_severity = severity_map.get(self.severity or "", 0)
            required_severity = severity_map.get(disorder_criteria["min_severity"], 0)
            
            if current_severity < required_severity:
                return False
        
        # Check impairment requirements
        if disorder_criteria.get("requires_impairment", False) and not self.functional_impairment:
            return False
        
        return True
    
    def validate(self) -> Dict[str, str]:
        """
        Validate symptom assessment data and return any validation errors.
        
        Returns:
            Dictionary of field_name: error_message pairs
        """
        errors = super().validate()
        
        # Required fields validation
        if not self.patient_id:
            errors["patient_id"] = "Patient ID is required"
        
        if not self.category:
            errors["category"] = "DSM-5 category is required"
        
        if not self.disorder:
            errors["disorder"] = "Disorder name is required"
        
        if not self.symptom_name:
            errors["symptom_name"] = "Symptom name is required"
        
        # Date validation
        if self.onset_date and self.onset_date > date.today():
            errors["onset_date"] = "Onset date cannot be in the future"
        
        if self.assessment_date and self.assessment_date > date.today():
            errors["assessment_date"] = "Assessment date cannot be in the future"
        
        # Severity validation
        if self.severity_score is not None and (self.severity_score < 0 or self.severity_score > 10):
            errors["severity_score"] = "Severity score must be between 0 and 10"
        
        # Duration validation
        if self.duration_weeks is not None and self.duration_weeks < 0:
            errors["duration_weeks"] = "Duration cannot be negative"
        
        # Treatment priority validation
        if self.treatment_priority is not None and (self.treatment_priority < 1 or self.treatment_priority > 10):
            errors["treatment_priority"] = "Treatment priority must be between 1 and 10"
        
        return errors
    
    def get_functional_impairment_summary(self) -> Dict[str, str]:
        """Get summary of functional impairment across domains."""
        return {
            "work": self.work_impairment or "None reported",
            "social": self.social_impairment or "None reported",
            "relationships": self.relationship_impairment or "None reported",
            "daily_living": self.daily_living_impairment or "None reported"
        }
    
    def get_assessment_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of the symptom assessment."""
        return {
            "symptom": self.display_name,
            "hierarchy": self.symptom_hierarchy_path,
            "present": self.is_present,
            "severity": self.severity_description,
            "duration": self.duration or f"{self.duration_weeks} weeks" if self.duration_weeks else "Not specified",
            "onset": self.onset_date.strftime("%Y-%m-%d") if self.onset_date else "Unknown",
            "functional_impairment": self.functional_impairment,
            "treatment_target": self.treatment_target,
            "requires_attention": self.requires_attention,
            "improvement": f"{self.improvement_percentage}%" if self.improvement_percentage else "Not calculated",
            "trend": self.severity_trend
        }
    
    def __str__(self):
        """String representation for display purposes."""
        status = "Present" if self.is_present else "Absent"
        severity = f" ({self.severity_description})" if self.is_present and self.severity_description != "Not rated" else ""
        return f"{self.display_name}: {status}{severity}"