"""
psychiatric_app.services - service layer package
"""

# Import core services so they can be accessed directly from the package
from importlib import import_module

# Lazy import to avoid heavy dependencies when not needed
try:
    VoiceService = import_module("psychiatric_app.services.voice_service").VoiceService
except Exception:  # pragma: no cover
    VoiceService = None

try:
    MLExportService = import_module("psychiatric_app.services.ml_export").MLExportService
except Exception:
    MLExportService = None