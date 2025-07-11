"""psychiatric_app.services.voice_service
Real-time voice recognition service used by the UI voice input widget.
"""

from __future__ import annotations

import queue
import threading
from typing import Optional

import speech_recognition as sr  # type: ignore
from PyQt6.QtCore import QObject, pyqtSignal


class VoiceService(QObject):
    """High-level wrapper around SpeechRecognition for continuous voice capture."""

    # ----- Qt Signals -----------------------------------------------------
    text_recognized = pyqtSignal(str)
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, *, energy_threshold: int = 4000, pause_threshold: float = 0.8):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone: Optional[sr.Microphone] = None
        try:
            self.microphone = sr.Microphone()
        except Exception as exc:  # pragma: no cover – hardware-dependent
            self.error_occurred.emit(f"Microphone init failed: {exc}")

        # Recognition tuning for clinical environment
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = pause_threshold
        self.recognizer.operation_timeout = None

        self._listening = False
        self._audio_queue: queue.Queue[sr.AudioData] = queue.Queue()

    # ------------------------------------------------------------------
    # Public control API
    # ------------------------------------------------------------------
    def start_listening(self) -> None:
        """Start asynchronous continuous listening."""
        if self._listening or self.microphone is None:
            return
        self._listening = True
        self.listening_started.emit()
        threading.Thread(target=self._listen_loop, daemon=True).start()
        # Spawn audio processor consumer thread
        threading.Thread(target=self._process_audio_loop, daemon=True).start()

    def stop_listening(self) -> None:
        """Stop listening loop gracefully."""
        if not self._listening:
            return
        self._listening = False
        self.listening_stopped.emit()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _listen_loop(self) -> None:
        if self.microphone is None:
            return
        # Calibrate for ambient noise once before entering loop
        with self.microphone as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source)
            except Exception as exc:  # pragma: no cover
                self.error_occurred.emit(str(exc))
                return

        while self._listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                # Push audio to queue for background processing
                self._audio_queue.put(audio)
            except sr.WaitTimeoutError:
                continue  # Just loop again ‑ no speech detected within timeout
            except Exception as exc:  # pragma: no cover
                self.error_occurred.emit(f"Voice recognition error: {exc}")
                break

    def _process_audio_loop(self) -> None:
        """Continuously consume audio from the queue and transcribe."""
        while self._listening or not self._audio_queue.empty():
            try:
                audio = self._audio_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            try:
                text = self.recognizer.recognize_google(audio)
                if text:
                    self.text_recognized.emit(text)
            except sr.UnknownValueError:
                # No discernible speech – ignore silently
                pass
            except sr.RequestError as exc:
                self.error_occurred.emit(f"Recognition service error: {exc}")
            except Exception as exc:  # pragma: no cover
                self.error_occurred.emit(str(exc))