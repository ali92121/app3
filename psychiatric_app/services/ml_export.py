"""psychiatric_app.services.ml_export
Utility for exporting patient data sets for downstream ML pipelines.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd  # type: ignore
from sqlalchemy.orm import joinedload

from psychiatric_app.config.database import db_manager
from psychiatric_app.models.patient import Patient


class MLExportService:
    """Service class responsible for materialising ML-ready exports."""

    @staticmethod
    def export_patient(
        patient_id: str,
        destination: str | Path,
        *,
        format: str = "json",
        indent: int | None = 2,
    ) -> Path:
        """Export a single patient's complete record.

        Parameters
        ----------
        patient_id: str
            The primary-key UUID of the patient.
        destination: str | Path
            File-path (or directory if exporting to multiple CSVs).
        format: str
            'json' (single hierarchical JSON) or 'csv' (separate tables).
        indent: int | None
            JSON indent; pass None for minified.
        """
        session = db_manager.get_session()
        try:
            patient = (
                session.query(Patient)
                .options(
                    joinedload(Patient.medications),
                    joinedload(Patient.lab_results),
                    joinedload(Patient.symptom_assessments),
                    joinedload(Patient.substance_use_records),
                    joinedload(Patient.clinical_scale_results),
                )
                .filter(Patient.id == patient_id)
                .first()
            )
            if not patient:
                raise ValueError(f"Patient '{patient_id}' not found")

            out_path = Path(destination)
            if format.lower() == "json":
                data = MLExportService._patient_to_dict(patient)
                if out_path.is_dir():
                    out_path = out_path / f"{patient_id}.json"
                out_path.write_text(json.dumps(data, indent=indent, default=str))
            elif format.lower() == "csv":
                # When CSV, treat destination as directory
                out_path.mkdir(parents=True, exist_ok=True)
                MLExportService._export_patient_to_csv(patient, out_path)
            else:
                raise ValueError("format must be 'json' or 'csv'")
            return out_path
        finally:
            session.close()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _patient_to_dict(patient: Patient) -> Dict[str, Any]:
        d: Dict[str, Any] = patient.to_dict()
        d["medications"] = [m.to_dict() for m in getattr(patient, "medications", [])]
        d["lab_results"] = [l.to_dict() for l in getattr(patient, "lab_results", [])]
        d["symptom_assessments"] = [s.to_dict() for s in getattr(patient, "symptom_assessments", [])]
        d["substance_use"] = [s.to_dict() for s in getattr(patient, "substance_use_records", [])]
        d["clinical_scales"] = [c.to_dict() for c in getattr(patient, "clinical_scale_results", [])]
        return d

    @staticmethod
    def _export_patient_to_csv(patient: Patient, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)

        # Core patient demographics
        pd.DataFrame([patient.to_dict()]).to_csv(directory / "patient.csv", index=False)

        # Related tables
        for attr, filename in [
            ("medications", "medications.csv"),
            ("lab_results", "lab_results.csv"),
            ("symptom_assessments", "symptom_assessments.csv"),
            ("substance_use_records", "substance_use.csv"),
            ("clinical_scale_results", "clinical_scales.csv"),
        ]:
            items: List[Any] = getattr(patient, attr, [])  # type: ignore[arg-type]
            if items:
                pd.DataFrame([i.to_dict() for i in items]).to_csv(directory / filename, index=False)