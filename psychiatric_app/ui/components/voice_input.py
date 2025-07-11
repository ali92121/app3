"""psychiatric_app.ui.components.voice_input
User-facing widget that provides microphone controls and live transcription display.
"""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
)
import qtawesome as qta

from psychiatric_app.services.voice_service import VoiceService


class VoiceInputWidget(QWidget):
    """A polished widget that lets the clinician dictate notes by voice."""

    # Emitted whenever the internal text buffer changes (e.g., new transcription)
    text_captured = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.voice_service = VoiceService()
        self._setup_ui()
        self._connect_signals()

    # ------------------------------------------------------------------
    # UI assembly
    # ------------------------------------------------------------------
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Control buttons ------------------------------------------------
        button_layout = QHBoxLayout()

        self.record_button = QPushButton("Start Recording")
        self.record_button.setCheckable(True)
        self.record_button.setIcon(qta.icon("fa5s.microphone"))
        self.record_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.clear_button = QPushButton("Clear")
        self.clear_button.setIcon(qta.icon("fa5s.trash"))
        self.clear_button.setCursor(Qt.CursorShape.PointingHandCursor)

        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()

        # Transcription view -------------------------------------------
        self.voice_text = QTextEdit()
        self.voice_text.setPlaceholderText("Voice recognition will appear here...")
        self.voice_text.setMaximumHeight(200)
        self.voice_text.setReadOnly(False)  # Allow manual edits if desired

        # Status label --------------------------------------------------
        self.status_label = QLabel("Ready to record")
        self.status_label.setProperty("class", "subtitle")

        # Assemble ------------------------------------------------------
        layout.addLayout(button_layout)
        layout.addWidget(self.voice_text)
        layout.addWidget(self.status_label)

    # ------------------------------------------------------------------
    # Signal wiring
    # ------------------------------------------------------------------
    def _connect_signals(self) -> None:
        self.record_button.clicked.connect(self._toggle_recording)  # type: ignore[arg-type]
        self.clear_button.clicked.connect(self._clear_text)  # type: ignore[arg-type]

        self.voice_service.text_recognized.connect(self._append_text)
        self.voice_service.listening_started.connect(self._on_listening_started)
        self.voice_service.listening_stopped.connect(self._on_listening_stopped)
        self.voice_service.error_occurred.connect(self._on_error)

    # ------------------------------------------------------------------
    # Voice-service slot handlers
    # ------------------------------------------------------------------
    def _toggle_recording(self) -> None:
        if self.record_button.isChecked():
            self.voice_service.start_listening()
        else:
            self.voice_service.stop_listening()

    def _append_text(self, text: str) -> None:  # pragma: no cover – GUI slot
        cursor = self.voice_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text + " ")
        self.voice_text.setTextCursor(cursor)
        self.text_captured.emit(self.voice_text.toPlainText())

    def _on_listening_started(self) -> None:
        self.status_label.setText("🎤 Listening…")
        self.record_button.setText("Stop Recording")
        self.record_button.setIcon(qta.icon("fa5s.stop"))

    def _on_listening_stopped(self) -> None:
        self.status_label.setText("Ready to record")
        self.record_button.setText("Start Recording")
        self.record_button.setIcon(qta.icon("fa5s.microphone"))
        self.record_button.setChecked(False)

    def _clear_text(self) -> None:  # pragma: no cover – GUI slot
        self.voice_text.clear()
        self.text_captured.emit("")

    def _on_error(self, message: str) -> None:  # pragma: no cover – GUI slot
        self.status_label.setText(f"Error: {message}")
        # Reset recording state to safe default
        self.record_button.setChecked(False)