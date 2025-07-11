"""psychiatric_app.models.clinical_scale
Model for standardized clinical scale results (e.g., PHQ-9, GAD-7).
"""

from __future__ import annotations

from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship

from psychiatric_app.models.base import BaseModel


class ClinicalScaleResult(BaseModel):
    __tablename__ = "clinical_scale_results"

    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)

    scale_name = Column(String(100), nullable=False)  # PHQ-9, GAD-7, YMRS, etc.
    score = Column(Integer, nullable=False)
    severity = Column(String(50))  # Mild, Moderate, Severe, etc.
    administration_date = Column(Date)
    administered_by = Column(String(200))

    # Raw responses or additional metadata (JSON encoded)
    raw_data = Column(Text)

    interpretation = Column(Text)

    # Relationships -----------------------------------------------------
    patient = relationship("Patient", back_populates="clinical_scale_results")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<ClinicalScaleResult(id={self.id}, scale={self.scale_name}, score={self.score})>"


# Attach back-reference to Patient --------------------------------------------
from psychiatric_app.models.patient import Patient  # noqa: E402  pylint: disable=wrong-import-position

Patient.clinical_scale_results = relationship(
    "ClinicalScaleResult",
    back_populates="patient",
    cascade="all, delete-orphan",
)