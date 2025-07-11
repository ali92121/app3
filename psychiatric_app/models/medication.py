"""
Medication model for tracking patient medications, dosages, effectiveness, and side effects.
Includes comprehensive medication management for psychiatric practice.
"""

from datetime import datetime, date
from typing import Dict, Any, Optional, List
from .base import BaseModel
import json

class Medication(BaseModel):
    """
    Comprehensive medication model for tracking patient medications,
    including dosage, effectiveness, side effects, and clinical context.
    """
    
    def __init__(self):
        super().__init__()
        
        # Foreign key reference (stored as string in this implementation)
        self.patient_id: str = ""
        
        # Medication Details
        self.name: str = ""
        self.generic_name: Optional[str] = None
        self.brand_name: Optional[str] = None
        self.medication_class: Optional[str] = None
        self.drug_category: Optional[str] = None  # e.g., "Antidepressant", "Antipsychotic"
        
        # Dosage Information
        self.dose_amount: Optional[float] = None
        self.dose_unit: Optional[str] = None  # mg, ml, etc.
        self.frequency: Optional[str] = None  # BID, TID, QD, etc.
        self.route: str = "PO"  # PO, IM, IV, etc.
        self.instructions: Optional[str] = None  # Special instructions
        
        # Timing and Status
        self.start_date: Optional[date] = None
        self.end_date: Optional[date] = None
        self.is_current: bool = True
        self.discontinuation_reason: Optional[str] = None
        
        # Effectiveness and Monitoring
        self.effectiveness: Optional[int] = None  # 0-100 scale
        self.effectiveness_notes: Optional[str] = None
        self.side_effects: Optional[str] = None  # JSON array as string
        self.side_effects_severity: Optional[str] = None  # Mild, Moderate, Severe
        self.adherence: Optional[int] = None  # 0-100 scale
        self.adherence_notes: Optional[str] = None
        
        # Clinical Context
        self.indication: Optional[str] = None  # What condition this treats
        self.target_symptoms: Optional[str] = None  # JSON array as string
        self.prescriber: Optional[str] = None
        self.prescriber_contact: Optional[str] = None
        self.pharmacy: Optional[str] = None
        self.pharmacy_contact: Optional[str] = None
        
        # Monitoring and Lab Requirements
        self.requires_monitoring: bool = False
        self.monitoring_frequency: Optional[str] = None
        self.last_lab_check: Optional[date] = None
        self.next_lab_due: Optional[date] = None
        
        # Drug Interactions and Allergies
        self.known_interactions: Optional[str] = None  # JSON array as string
        self.contraindications: Optional[str] = None
        
        # Cost and Insurance
        self.cost_per_month: Optional[float] = None
        self.insurance_coverage: Optional[str] = None
        self.prior_authorization_required: bool = False
        
        # Clinical Notes
        self.clinical_notes: Optional[str] = None
        self.progress_notes: Optional[str] = None  # JSON array as string
    
    @property
    def display_name(self) -> str:
        """Get formatted medication name for display."""
        if self.brand_name and self.generic_name:
            return f"{self.brand_name} ({self.generic_name})"
        elif self.brand_name:
            return self.brand_name
        elif self.generic_name:
            return self.generic_name
        else:
            return self.name
    
    @property
    def dosage_display(self) -> str:
        """Get formatted dosage string."""
        parts = []
        
        if self.dose_amount and self.dose_unit:
            parts.append(f"{self.dose_amount} {self.dose_unit}")
        
        if self.frequency:
            parts.append(self.frequency)
        
        if self.route and self.route != "PO":
            parts.append(f"({self.route})")
        
        return " ".join(parts) if parts else "Dosage not specified"
    
    @property
    def duration_days(self) -> Optional[int]:
        """Calculate duration of medication use in days."""
        if not self.start_date:
            return None
        
        end_date = self.end_date or date.today()
        return (end_date - self.start_date).days
    
    @property
    def is_psychiatric_medication(self) -> bool:
        """Check if this is likely a psychiatric medication."""
        psychiatric_classes = [
            "antidepressant", "antipsychotic", "mood stabilizer", "anxiolytic",
            "stimulant", "anticonvulsant", "hypnotic", "sedative",
            "ssri", "snri", "maoi", "tricyclic", "benzodiazepine",
            "atypical antipsychotic", "typical antipsychotic"
        ]
        
        if self.medication_class:
            return any(pc in self.medication_class.lower() for pc in psychiatric_classes)
        
        if self.drug_category:
            return any(pc in self.drug_category.lower() for pc in psychiatric_classes)
        
        return False
    
    def get_side_effects_list(self) -> List[str]:
        """Get list of side effects from JSON string."""
        if not self.side_effects:
            return []
        
        try:
            return json.loads(self.side_effects)
        except (json.JSONDecodeError, TypeError):
            # If not JSON, treat as comma-separated string
            return [effect.strip() for effect in self.side_effects.split(",") if effect.strip()]
    
    def set_side_effects_list(self, side_effects: List[str]):
        """Set side effects from list."""
        self.side_effects = json.dumps(side_effects)
    
    def add_side_effect(self, side_effect: str):
        """Add a new side effect."""
        current_effects = self.get_side_effects_list()
        if side_effect not in current_effects:
            current_effects.append(side_effect)
            self.set_side_effects_list(current_effects)
    
    def remove_side_effect(self, side_effect: str):
        """Remove a side effect."""
        current_effects = self.get_side_effects_list()
        if side_effect in current_effects:
            current_effects.remove(side_effect)
            self.set_side_effects_list(current_effects)
    
    def get_target_symptoms_list(self) -> List[str]:
        """Get list of target symptoms from JSON string."""
        if not self.target_symptoms:
            return []
        
        try:
            return json.loads(self.target_symptoms)
        except (json.JSONDecodeError, TypeError):
            return [symptom.strip() for symptom in self.target_symptoms.split(",") if symptom.strip()]
    
    def set_target_symptoms_list(self, symptoms: List[str]):
        """Set target symptoms from list."""
        self.target_symptoms = json.dumps(symptoms)
    
    def get_known_interactions_list(self) -> List[str]:
        """Get list of known drug interactions."""
        if not self.known_interactions:
            return []
        
        try:
            return json.loads(self.known_interactions)
        except (json.JSONDecodeError, TypeError):
            return [interaction.strip() for interaction in self.known_interactions.split(",") if interaction.strip()]
    
    def get_progress_notes_list(self) -> List[Dict[str, Any]]:
        """Get list of progress notes with timestamps."""
        if not self.progress_notes:
            return []
        
        try:
            return json.loads(self.progress_notes)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def add_progress_note(self, note: str, user: str = "system"):
        """Add a new progress note with timestamp."""
        current_notes = self.get_progress_notes_list()
        new_note = {
            "timestamp": datetime.utcnow().isoformat(),
            "user": user,
            "note": note
        }
        current_notes.append(new_note)
        self.progress_notes = json.dumps(current_notes)
    
    @property
    def needs_lab_monitoring(self) -> bool:
        """Check if medication requires lab monitoring."""
        return self.requires_monitoring and self.next_lab_due is not None
    
    @property
    def is_lab_overdue(self) -> bool:
        """Check if lab monitoring is overdue."""
        if not self.next_lab_due:
            return False
        return self.next_lab_due < date.today()
    
    @property
    def effectiveness_rating(self) -> str:
        """Get text description of effectiveness rating."""
        if self.effectiveness is None:
            return "Not rated"
        elif self.effectiveness >= 80:
            return "Excellent"
        elif self.effectiveness >= 60:
            return "Good"
        elif self.effectiveness >= 40:
            return "Moderate"
        elif self.effectiveness >= 20:
            return "Poor"
        else:
            return "Ineffective"
    
    @property
    def adherence_rating(self) -> str:
        """Get text description of adherence rating."""
        if self.adherence is None:
            return "Not assessed"
        elif self.adherence >= 90:
            return "Excellent"
        elif self.adherence >= 75:
            return "Good"
        elif self.adherence >= 50:
            return "Fair"
        else:
            return "Poor"
    
    def validate(self) -> Dict[str, str]:
        """
        Validate medication data and return any validation errors.
        
        Returns:
            Dictionary of field_name: error_message pairs
        """
        errors = super().validate()
        
        # Required fields validation
        if not self.name:
            errors["name"] = "Medication name is required"
        
        if not self.patient_id:
            errors["patient_id"] = "Patient ID is required"
        
        # Date validation
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                errors["end_date"] = "End date cannot be before start date"
        
        if self.start_date and self.start_date > date.today():
            errors["start_date"] = "Start date cannot be in the future"
        
        # Dosage validation
        if self.dose_amount is not None and self.dose_amount <= 0:
            errors["dose_amount"] = "Dose amount must be greater than 0"
        
        # Effectiveness and adherence validation
        for field in ["effectiveness", "adherence"]:
            value = getattr(self, field)
            if value is not None and (value < 0 or value > 100):
                errors[field] = f"{field.title()} must be between 0 and 100"
        
        # Cost validation
        if self.cost_per_month is not None and self.cost_per_month < 0:
            errors["cost_per_month"] = "Cost cannot be negative"
        
        return errors
    
    def discontinue(self, reason: str, discontinued_by: str = "system"):
        """
        Discontinue the medication with reason.
        
        Args:
            reason: Reason for discontinuation
            discontinued_by: User or system discontinuing the medication
        """
        self.is_current = False
        self.end_date = date.today()
        self.discontinuation_reason = reason
        self.updated_by = discontinued_by
        self.updated_at = datetime.utcnow()
        
        # Add progress note
        self.add_progress_note(f"Medication discontinued: {reason}", discontinued_by)
    
    def restart(self, restarted_by: str = "system"):
        """
        Restart a discontinued medication.
        
        Args:
            restarted_by: User or system restarting the medication
        """
        self.is_current = True
        self.end_date = None
        self.discontinuation_reason = None
        self.updated_by = restarted_by
        self.updated_at = datetime.utcnow()
        
        # Add progress note
        self.add_progress_note("Medication restarted", restarted_by)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of medication information."""
        return {
            "name": self.display_name,
            "dosage": self.dosage_display,
            "indication": self.indication,
            "effectiveness": self.effectiveness_rating,
            "adherence": self.adherence_rating,
            "side_effects": self.get_side_effects_list(),
            "is_current": self.is_current,
            "duration_days": self.duration_days,
            "is_psychiatric": self.is_psychiatric_medication,
            "needs_monitoring": self.needs_lab_monitoring,
            "lab_overdue": self.is_lab_overdue
        }
    
    def __str__(self):
        """String representation for display purposes."""
        return f"{self.display_name} - {self.dosage_display} ({'Current' if self.is_current else 'Discontinued'})"