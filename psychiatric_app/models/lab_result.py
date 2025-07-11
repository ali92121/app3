"""
Lab Result model for tracking laboratory test results with reference ranges and clinical interpretation.
Includes comprehensive lab data management for psychiatric practice monitoring.
"""

from datetime import datetime, date
from typing import Dict, Any, Optional, Tuple
from .base import BaseModel

class LabResult(BaseModel):
    """
    Comprehensive lab result model for tracking laboratory test results,
    including reference ranges, abnormal flagging, and clinical interpretation.
    """
    
    def __init__(self):
        super().__init__()
        
        # Foreign key reference (stored as string in this implementation)
        self.patient_id: str = ""
        
        # Test Identification
        self.test_name: str = ""
        self.test_code: Optional[str] = None  # e.g., CPT code, LOINC code
        self.test_category: Optional[str] = None  # Chemistry, Hematology, Toxicology, etc.
        self.test_panel: Optional[str] = None  # Comprehensive Metabolic Panel, Lipid Panel, etc.
        
        # Test Results
        self.value: Optional[float] = None
        self.value_text: Optional[str] = None  # For non-numeric results
        self.unit: Optional[str] = None
        self.reference_range_low: Optional[float] = None
        self.reference_range_high: Optional[float] = None
        self.reference_range_text: Optional[str] = None  # For text reference ranges
        
        # Result Status and Flags
        self.is_abnormal: bool = False
        self.abnormal_flag: Optional[str] = None  # H (High), L (Low), C (Critical), etc.
        self.is_critical: bool = False
        self.result_status: str = "Final"  # Final, Preliminary, Corrected, etc.
        
        # Dates and Timing
        self.collection_date: Optional[datetime] = None
        self.result_date: Optional[datetime] = None
        self.reported_date: Optional[datetime] = None
        
        # Clinical Context
        self.ordering_physician: Optional[str] = None
        self.ordering_reason: Optional[str] = None
        self.lab_facility: Optional[str] = None
        self.lab_facility_address: Optional[str] = None
        self.specimen_type: Optional[str] = None  # Serum, Plasma, Whole Blood, etc.
        self.collection_method: Optional[str] = None
        
        # Quality and Validation
        self.quality_flag: Optional[str] = None  # Hemolyzed, Lipemic, etc.
        self.delta_flag: Optional[str] = None  # Significant change from previous result
        self.verified_by: Optional[str] = None
        self.verified_date: Optional[datetime] = None
        
        # Clinical Interpretation
        self.clinical_significance: Optional[str] = None
        self.interpretation: Optional[str] = None
        self.follow_up_required: bool = False
        self.follow_up_instructions: Optional[str] = None
        
        # Notes and Comments
        self.lab_comments: Optional[str] = None
        self.clinician_notes: Optional[str] = None
        self.patient_notes: Optional[str] = None
    
    @property
    def display_name(self) -> str:
        """Get formatted test name for display."""
        if self.test_panel and self.test_name != self.test_panel:
            return f"{self.test_panel} - {self.test_name}"
        return self.test_name
    
    @property
    def formatted_value(self) -> str:
        """Get formatted value with unit for display."""
        if self.value_text:
            return self.value_text
        
        if self.value is not None:
            if self.unit:
                return f"{self.value} {self.unit}"
            else:
                return str(self.value)
        
        return "No result"
    
    @property
    def reference_range_display(self) -> str:
        """Get formatted reference range for display."""
        if self.reference_range_text:
            return self.reference_range_text
        
        if self.reference_range_low is not None and self.reference_range_high is not None:
            unit_str = f" {self.unit}" if self.unit else ""
            return f"{self.reference_range_low}-{self.reference_range_high}{unit_str}"
        elif self.reference_range_low is not None:
            unit_str = f" {self.unit}" if self.unit else ""
            return f"≥ {self.reference_range_low}{unit_str}"
        elif self.reference_range_high is not None:
            unit_str = f" {self.unit}" if self.unit else ""
            return f"≤ {self.reference_range_high}{unit_str}"
        
        return "Not established"
    
    @property
    def days_since_collection(self) -> Optional[int]:
        """Calculate days since specimen collection."""
        if not self.collection_date:
            return None
        
        return (datetime.now() - self.collection_date).days
    
    @property
    def turnaround_time_hours(self) -> Optional[float]:
        """Calculate turnaround time from collection to result in hours."""
        if not self.collection_date or not self.result_date:
            return None
        
        return (self.result_date - self.collection_date).total_seconds() / 3600
    
    def determine_abnormal_status(self) -> Tuple[bool, Optional[str]]:
        """
        Automatically determine if result is abnormal based on reference ranges.
        
        Returns:
            Tuple of (is_abnormal, abnormal_flag)
        """
        if self.value is None:
            return False, None
        
        # Check for critical values first
        if self.is_critical:
            return True, "C"
        
        # Check against reference ranges
        if self.reference_range_low is not None and self.value < self.reference_range_low:
            return True, "L"
        
        if self.reference_range_high is not None and self.value > self.reference_range_high:
            return True, "H"
        
        return False, None
    
    def update_abnormal_status(self):
        """Update abnormal status based on current values."""
        self.is_abnormal, self.abnormal_flag = self.determine_abnormal_status()
    
    @property
    def abnormal_description(self) -> str:
        """Get text description of abnormal status."""
        if not self.is_abnormal:
            return "Normal"
        
        flag_descriptions = {
            "H": "High",
            "L": "Low", 
            "C": "Critical",
            "HH": "Critical High",
            "LL": "Critical Low"
        }
        
        return flag_descriptions.get(self.abnormal_flag or "", "Abnormal")
    
    @property
    def requires_immediate_attention(self) -> bool:
        """Check if result requires immediate clinical attention."""
        return self.is_critical or self.abnormal_flag in ["C", "HH", "LL"]
    
    @property
    def is_psychiatric_relevant(self) -> bool:
        """Check if this lab test is relevant to psychiatric care."""
        psychiatric_tests = [
            "lithium", "valproic acid", "carbamazepine", "lamotrigine",
            "clozapine", "glucose", "hemoglobin a1c", "lipid panel",
            "liver function", "kidney function", "thyroid", "tsh",
            "vitamin b12", "folate", "vitamin d", "drug screen",
            "urine drug", "alcohol", "complete blood count", "cbc"
        ]
        
        test_name_lower = self.test_name.lower()
        return any(test in test_name_lower for test in psychiatric_tests)
    
    def get_trend_indication(self, previous_result: 'LabResult') -> Optional[str]:
        """
        Compare with previous result to determine trend.
        
        Args:
            previous_result: Previous lab result for the same test
            
        Returns:
            Trend indication string or None
        """
        if not previous_result or self.value is None or previous_result.value is None:
            return None
        
        if self.test_name != previous_result.test_name:
            return None
        
        current_val = self.value
        previous_val = previous_result.value
        
        # Calculate percentage change
        if previous_val != 0:
            percent_change = ((current_val - previous_val) / previous_val) * 100
        else:
            percent_change = 100 if current_val > 0 else -100
        
        # Determine significance threshold (could be test-specific)
        significance_threshold = 10  # 10% change
        
        if abs(percent_change) < significance_threshold:
            return "Stable"
        elif percent_change > 0:
            return f"Increased ({percent_change:.1f}%)"
        else:
            return f"Decreased ({abs(percent_change):.1f}%)"
    
    def validate(self) -> Dict[str, str]:
        """
        Validate lab result data and return any validation errors.
        
        Returns:
            Dictionary of field_name: error_message pairs
        """
        errors = super().validate()
        
        # Required fields validation
        if not self.test_name:
            errors["test_name"] = "Test name is required"
        
        if not self.patient_id:
            errors["patient_id"] = "Patient ID is required"
        
        # Date validation
        if self.collection_date and self.result_date:
            if self.result_date < self.collection_date:
                errors["result_date"] = "Result date cannot be before collection date"
        
        if self.collection_date and self.collection_date > datetime.now():
            errors["collection_date"] = "Collection date cannot be in the future"
        
        # Value validation
        if self.value is not None and self.value < 0:
            # Allow negative values for some tests (e.g., temperature changes)
            pass
        
        # Reference range validation
        if (self.reference_range_low is not None and 
            self.reference_range_high is not None and
            self.reference_range_low > self.reference_range_high):
            errors["reference_range"] = "Low reference range cannot be greater than high range"
        
        # Result status validation
        valid_statuses = ["Final", "Preliminary", "Corrected", "Cancelled", "Pending"]
        if self.result_status and self.result_status not in valid_statuses:
            errors["result_status"] = f"Result status must be one of: {', '.join(valid_statuses)}"
        
        return errors
    
    def set_critical_values(self, test_name: str):
        """
        Set critical value thresholds based on common test parameters.
        
        Args:
            test_name: Name of the test to set critical values for
        """
        # Common critical value thresholds (these should ideally come from a reference database)
        critical_values = {
            "glucose": {"low": 40, "high": 400},
            "potassium": {"low": 2.5, "high": 6.0},
            "sodium": {"low": 120, "high": 160},
            "creatinine": {"low": None, "high": 3.0},
            "hemoglobin": {"low": 7.0, "high": 20.0},
            "white blood cell count": {"low": 1.0, "high": 50.0},
            "platelet count": {"low": 20, "high": 1000},
            "lithium": {"low": None, "high": 1.5}
        }
        
        test_lower = test_name.lower()
        for test_key, values in critical_values.items():
            if test_key in test_lower:
                if values["low"] and self.value and self.value <= values["low"]:
                    self.is_critical = True
                    self.abnormal_flag = "LL"
                elif values["high"] and self.value and self.value >= values["high"]:
                    self.is_critical = True
                    self.abnormal_flag = "HH"
                break
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of lab result information."""
        return {
            "test": self.display_name,
            "value": self.formatted_value,
            "reference_range": self.reference_range_display,
            "status": self.abnormal_description,
            "is_critical": self.is_critical,
            "collection_date": self.collection_date.strftime("%Y-%m-%d") if self.collection_date else None,
            "result_date": self.result_date.strftime("%Y-%m-%d") if self.result_date else None,
            "days_old": self.days_since_collection,
            "psychiatric_relevant": self.is_psychiatric_relevant,
            "needs_attention": self.requires_immediate_attention
        }
    
    def __str__(self):
        """String representation for display purposes."""
        status = f" ({self.abnormal_description})" if self.is_abnormal else ""
        return f"{self.display_name}: {self.formatted_value}{status}"