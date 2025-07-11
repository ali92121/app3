"""psychiatric_app.models.substance_use
SQLAlchemy model representing a patient's substance-use history entry.
"""

from __future__ import annotations

from sqlalchemy import Column, String, Integer, Boolean, Text, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from psychiatric_app.models.base import BaseModel


class SubstanceUse(BaseModel):
    __tablename__ = "substance_use_records"

    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)

    # Substance details -------------------------------------------------
    substance_type = Column(String(100), nullable=False)  # Alcohol, Cannabis, etc.
    usage_pattern = Column(String(200))  # Daily, Weekends, Binge, etc.
    frequency = Column(String(100))  # e.g. "3 times/week"
    amount = Column(String(100))  # e.g. "2 drinks", "1g"
    route = Column(String(50))  # Oral, Inhalation, IV, etc.

    # Timeline ----------------------------------------------------------
    age_of_first_use = Column(Integer)
    years_of_use = Column(Float)
    last_use_date = Column(Date)
    periods_of_abstinence = Column(Text)  # JSON-encoded list of {start, end}

    # Treatment history & impact ---------------------------------------
    treatment_history = Column(Text)  # JSON-encoded list of programs / MAT
    current_status = Column(String(100))  # Active Use, In Remission, etc.
    motivation_level = Column(String(50))  # Pre-contemplation, Action, etc.
    consequences = Column(Text)  # Legal/social consequences

    # Severity metrics --------------------------------------------------
    severity_score = Column(Integer)  # 0-10 clinician rating
    craving_score = Column(Integer)  # 0-10 self-reported

    notes = Column(Text)

    # Relationships -----------------------------------------------------
    patient = relationship("Patient", back_populates="substance_use_records")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<SubstanceUse(id={self.id}, substance={self.substance_type}, patient={self.patient_id})>"


# Dynamically attach back-reference to Patient --------------------------------
from psychiatric_app.models.patient import Patient  # noqa: E402  pylint: disable=wrong-import-position

Patient.substance_use_records = relationship(
    "SubstanceUse",
    back_populates="patient",
    cascade="all, delete-orphan",
)