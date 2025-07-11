# 🧠 **Phase 2: Advanced Features Implementation - Psychiatric Records App**

## 🎯 **Phase 2 Objectives**

Enhance the core psychiatric records application with advanced clinical features including voice input, comprehensive substance use tracking, clinical assessment scales, and ML-ready data export capabilities.

---

## 🚀 **Phase 2 Features Overview**

### 1. **Voice Input Integration** 🎤
### 2. **Substance Use Tracking System** 💊
### 3. **Clinical Scales Integration** 📊
### 4. **ML Export Functionality** 🤖

---

## 🎤 **1. Voice Input Integration**

### **Core Voice Service Implementation**
```python
# services/voice_service.py
import speech_recognition as sr
import threading
import queue
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import QWidget, QPushButton, QTextEdit, QVBoxLayout
import pyaudio

class VoiceService(QObject):
    """
    Real-time voice recognition service for clinical note-taking
    """
    text_recognized = pyqtSignal(str)
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.audio_queue = queue.Queue()
        
        # Optimize recognition settings for clinical environment
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.operation_timeout = None
        
    def start_listening(self):
        """Start continuous voice recognition"""
        if not self.listening:
            self.listening = True
            self.listening_started.emit()
            threading.Thread(target=self._listen_continuously, daemon=True).start()
    
    def stop_listening(self):
        """Stop voice recognition"""
        self.listening = False
        self.listening_stopped.emit()
    
    def _listen_continuously(self):
        """Continuous listening loop with error handling"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        while self.listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Process audio in background thread
                threading.Thread(target=self._process_audio, args=(audio,), daemon=True).start()
                
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                self.error_occurred.emit(f"Voice recognition error: {str(e)}")
                break
    
    def _process_audio(self, audio):
        """Process audio and emit recognized text"""
        try:
            text = self.recognizer.recognize_google(audio)
            if text:
                self.text_recognized.emit(text)
        except sr.UnknownValueError:
            pass  # No speech detected
        except sr.RequestError as e:
            self.error_occurred.emit(f"Recognition service error: {str(e)}")
```

### **Voice Input Widget Component**
```python
# ui/components/voice_input.py
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import qtawesome as qta

class VoiceInputWidget(QWidget):
    """
    Modern voice input widget with visual feedback
    """
    text_captured = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.voice_service = VoiceService()
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Voice control buttons
        button_layout = QHBoxLayout()
        
        self.record_button = QPushButton()
        self.record_button.setIcon(qta.icon('fa5s.microphone'))
        self.record_button.setText("Start Recording")
        self.record_button.setCheckable(True)
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #f44336;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.clear_button = QPushButton()
        self.clear_button.setIcon(qta.icon('fa5s.trash'))
        self.clear_button.setText("Clear")
        
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        
        # Voice feedback display
        self.voice_text = QTextEdit()
        self.voice_text.setPlaceholderText("Voice recognition will appear here...")
        self.voice_text.setMaximumHeight(200)
        
        # Status indicator
        self.status_label = QLabel("Ready to record")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        
        layout.addLayout(button_layout)
        layout.addWidget(self.voice_text)
        layout.addWidget(self.status_label)
        
    def connect_signals(self):
        self.record_button.clicked.connect(self.toggle_recording)
        self.clear_button.clicked.connect(self.clear_text)
        
        self.voice_service.text_recognized.connect(self.append_text)
        self.voice_service.listening_started.connect(self.on_listening_started)
        self.voice_service.listening_stopped.connect(self.on_listening_stopped)
        self.voice_service.error_occurred.connect(self.on_error)
    
    def toggle_recording(self):
        if self.record_button.isChecked():
            self.voice_service.start_listening()
        else:
            self.voice_service.stop_listening()
    
    def append_text(self, text):
        cursor = self.voice_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text + " ")
        self.voice_text.setTextCursor(cursor)
        self.text_captured.emit(self.voice_text.toPlainText())
    
    def on_listening_started(self):
        self.status_label.setText("🎤 Listening...")
        self.record_button.setText("Stop Recording")
        self.record_button.setIcon(qta.icon('fa5s.stop'))
    
    def on_listening_stopped(self):
        self.status_label.setText("Ready to record")
        self.record_button.setText("Start Recording")
        self.record_button.setIcon(qta.icon('fa5s.microphone'))
        self.record_button.setChecked(False)
    
    def clear_text(self):
        self.voice_text.clear()
        self.text_captured.emit("")
    
    def on_error(self, error_message):
        self.status_label.setText(f"Error: {error_message}")
        self.record_button.setChecked(False)
```

---

## 💊 **2. Substance Use Tracking System**

### **Enhanced Substance Use Model**
```python
# models/substance_use.py
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class SubstanceType(Base):
    __tablename__ = 'substance_types'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # Alcohol, Cannabis, Cocaine, etc.
    category = Column(String(50))  # Depressant, Stimulant, Hallucinogen
    risk_level = Column(String(20))  # Low, Medium, High
    withdrawal_symptoms = Column(Text)
    
class SubstanceUse(Base):
    __tablename__ = 'substance_use'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    substance_type_id = Column(Integer, ForeignKey('substance_types.id'))
    
    # Usage Pattern
    frequency = Column(String(50))  # Daily, Weekly, Monthly, Occasional
    amount = Column(String(100))  # Specific amounts/units
    route = Column(String(50))  # Oral, Inhalation, Injection, etc.
    
    # Timeline
    age_first_use = Column(Integer)
    duration_use = Column(String(100))  # "5 years", "6 months"
    last_use_date = Column(DateTime)
    
    # Current Status
    current_use = Column(Boolean, default=True)
    abstinence_date = Column(DateTime)
    longest_abstinence = Column(String(100))
    
    # Impact Assessment
    impact_work = Column(Integer)  # 1-10 scale
    impact_relationships = Column(Integer)
    impact_mental_health = Column(Integer)
    impact_physical_health = Column(Integer)
    
    # Treatment History
    treatment_attempts = Column(Text)
    support_groups = Column(Text)
    medication_assisted = Column(Boolean)
    
    # Risk Factors
    craving_level = Column(Integer)  # 1-10 scale
    trigger_situations = Column(Text)
    relapse_risk = Column(String(20))  # Low, Medium, High
    
    # Relationships
    patient = relationship("Patient", back_populates="substance_use")
    substance_type = relationship("SubstanceType")
    
class SubstanceUseLog(Base):
    __tablename__ = 'substance_use_logs'
    
    id = Column(Integer, primary_key=True)
    substance_use_id = Column(Integer, ForeignKey('substance_use.id'))
    log_date = Column(DateTime, default=datetime.utcnow)
    
    # Daily tracking
    used_today = Column(Boolean)
    amount_used = Column(String(100))
    craving_level = Column(Integer)
    mood_rating = Column(Integer)
    notes = Column(Text)
    
    substance_use = relationship("SubstanceUse")
```

### **Substance Use Tracking Interface**
```python
# ui/substance_tracker.py
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import qtawesome as qta
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SubstanceTracker(QWidget):
    """
    Comprehensive substance use tracking and assessment
    """
    
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header with patient info
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Substance Use Assessment"))
        header_layout.addStretch()
        
        add_button = QPushButton("Add Substance")
        add_button.setIcon(qta.icon('fa5s.plus'))
        add_button.clicked.connect(self.add_substance)
        header_layout.addWidget(add_button)
        
        layout.addLayout(header_layout)
        
        # Tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Current substances tab
        self.current_tab = self.create_current_substances_tab()
        self.tab_widget.addTab(self.current_tab, "Current Use")
        
        # History timeline tab
        self.timeline_tab = self.create_timeline_tab()
        self.tab_widget.addTab(self.timeline_tab, "Usage Timeline")
        
        # Assessment scores tab
        self.assessment_tab = self.create_assessment_tab()
        self.tab_widget.addTab(self.assessment_tab, "Risk Assessment")
        
        # Treatment history tab
        self.treatment_tab = self.create_treatment_tab()
        self.tab_widget.addTab(self.treatment_tab, "Treatment History")
        
        layout.addWidget(self.tab_widget)
        
    def create_current_substances_tab(self):
        """Create tab for current substance use"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Substance list
        self.substance_list = QListWidget()
        self.substance_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
            }
        """)
        
        # Substance details panel
        self.details_panel = self.create_substance_details_panel()
        
        # Split layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.substance_list)
        splitter.addWidget(self.details_panel)
        splitter.setSizes([300, 500])
        
        layout.addWidget(splitter)
        
        return widget
    
    def create_substance_details_panel(self):
        """Create detailed substance information panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Substance info form
        form_layout = QFormLayout()
        
        self.substance_name = QLineEdit()
        self.frequency = QComboBox()
        self.frequency.addItems(["Daily", "Weekly", "Monthly", "Occasional", "Former use"])
        
        self.amount = QLineEdit()
        self.amount.setPlaceholderText("e.g., 2-3 drinks, 1 joint, etc.")
        
        self.route = QComboBox()
        self.route.addItems(["Oral", "Inhalation", "Injection", "Nasal", "Other"])
        
        self.age_first_use = QSpinBox()
        self.age_first_use.setRange(5, 80)
        
        self.last_use = QDateEdit()
        self.last_use.setDate(QDate.currentDate())
        
        form_layout.addRow("Substance:", self.substance_name)
        form_layout.addRow("Frequency:", self.frequency)
        form_layout.addRow("Typical Amount:", self.amount)
        form_layout.addRow("Route:", self.route)
        form_layout.addRow("Age First Use:", self.age_first_use)
        form_layout.addRow("Last Use:", self.last_use)
        
        layout.addLayout(form_layout)
        
        # Impact assessment sliders
        layout.addWidget(QLabel("Impact Assessment (1-10 scale):"))
        
        self.impact_sliders = {}
        impacts = ["Work/School", "Relationships", "Mental Health", "Physical Health"]
        
        for impact in impacts:
            slider_layout = QHBoxLayout()
            label = QLabel(impact)
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(1, 10)
            slider.setValue(5)
            value_label = QLabel("5")
            
            slider.valueChanged.connect(lambda v, lbl=value_label: lbl.setText(str(v)))
            
            slider_layout.addWidget(label)
            slider_layout.addWidget(slider)
            slider_layout.addWidget(value_label)
            
            self.impact_sliders[impact] = slider
            layout.addLayout(slider_layout)
        
        # Treatment section
        layout.addWidget(QLabel("Treatment History:"))
        self.treatment_history = QTextEdit()
        self.treatment_history.setMaximumHeight(100)
        layout.addWidget(self.treatment_history)
        
        # Save button
        save_button = QPushButton("Save Changes")
        save_button.setIcon(qta.icon('fa5s.save'))
        save_button.clicked.connect(self.save_substance_details)
        layout.addWidget(save_button)
        
        return widget
    
    def create_timeline_tab(self):
        """Create visual timeline of substance use"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Timeline chart
        self.timeline_figure = Figure(figsize=(12, 6))
        self.timeline_canvas = FigureCanvas(self.timeline_figure)
        layout.addWidget(self.timeline_canvas)
        
        # Update timeline
        self.update_timeline_chart()
        
        return widget
    
    def create_assessment_tab(self):
        """Create standardized assessment tools"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Assessment tools
        assessment_layout = QHBoxLayout()
        
        # AUDIT for alcohol
        audit_button = QPushButton("AUDIT Assessment")
        audit_button.clicked.connect(self.run_audit_assessment)
        assessment_layout.addWidget(audit_button)
        
        # DAST for drugs
        dast_button = QPushButton("DAST Assessment")
        dast_button.clicked.connect(self.run_dast_assessment)
        assessment_layout.addWidget(dast_button)
        
        # CAGE screening
        cage_button = QPushButton("CAGE Screening")
        cage_button.clicked.connect(self.run_cage_screening)
        assessment_layout.addWidget(cage_button)
        
        layout.addLayout(assessment_layout)
        
        # Results display
        self.assessment_results = QTextEdit()
        self.assessment_results.setReadOnly(True)
        layout.addWidget(self.assessment_results)
        
        return widget
    
    def create_treatment_tab(self):
        """Create treatment history and planning"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Treatment history
        layout.addWidget(QLabel("Treatment History:"))
        self.treatment_table = QTableWidget()
        self.treatment_table.setColumnCount(4)
        self.treatment_table.setHorizontalHeaderLabels(["Date", "Type", "Duration", "Outcome"])
        layout.addWidget(self.treatment_table)
        
        # Add treatment button
        add_treatment_button = QPushButton("Add Treatment Episode")
        add_treatment_button.clicked.connect(self.add_treatment_episode)
        layout.addWidget(add_treatment_button)
        
        # Current treatment plan
        layout.addWidget(QLabel("Current Treatment Plan:"))
        self.current_plan = QTextEdit()
        layout.addWidget(self.current_plan)
        
        return widget
```

---

## 📊 **3. Clinical Scales Integration**

### **Clinical Scales Model**
```python
# models/clinical_scales.py
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class ClinicalScale(Base):
    __tablename__ = 'clinical_scales'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # PHQ-9, GAD-7, etc.
    description = Column(Text)
    category = Column(String(50))  # Depression, Anxiety, etc.
    questions = Column(JSON)  # Store questions and scoring
    scoring_info = Column(JSON)  # Scoring rules and interpretations
    
class ScaleAssessment(Base):
    __tablename__ = 'scale_assessments'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    scale_id = Column(Integer, ForeignKey('clinical_scales.id'))
    assessment_date = Column(DateTime, default=datetime.utcnow)
    
    responses = Column(JSON)  # Store individual responses
    total_score = Column(Integer)
    severity_level = Column(String(50))
    interpretation = Column(Text)
    
    # Relationships
    patient = relationship("Patient")
    scale = relationship("ClinicalScale")
```

### **Clinical Scales Interface**
```python
# ui/clinical_scales.py
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import qtawesome as qta
import json
from datetime import datetime

class ClinicalScalesWidget(QWidget):
    """
    Standardized clinical assessment scales interface
    """
    
    def __init__(self, patient_id, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.current_scale = None
        self.current_responses = {}
        self.setup_ui()
        self.load_scales()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Clinical Assessment Scales"))
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Scale selection
        selection_layout = QHBoxLayout()
        selection_layout.addWidget(QLabel("Select Scale:"))
        
        self.scale_combo = QComboBox()
        self.scale_combo.currentTextChanged.connect(self.scale_changed)
        selection_layout.addWidget(self.scale_combo)
        
        self.start_assessment_button = QPushButton("Start Assessment")
        self.start_assessment_button.clicked.connect(self.start_assessment)
        selection_layout.addWidget(self.start_assessment_button)
        
        selection_layout.addStretch()
        layout.addLayout(selection_layout)
        
        # Assessment area
        self.assessment_area = QStackedWidget()
        
        # Welcome screen
        self.welcome_screen = self.create_welcome_screen()
        self.assessment_area.addWidget(self.welcome_screen)
        
        # Assessment screen
        self.assessment_screen = self.create_assessment_screen()
        self.assessment_area.addWidget(self.assessment_screen)
        
        # Results screen
        self.results_screen = self.create_results_screen()
        self.assessment_area.addWidget(self.results_screen)
        
        layout.addWidget(self.assessment_area)
        
    def create_welcome_screen(self):
        """Create welcome/instruction screen"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        welcome_label = QLabel("Welcome to Clinical Assessment Scales")
        welcome_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(welcome_label)
        
        instructions = QLabel("""
        This module provides standardized clinical assessment tools including:
        
        • PHQ-9 (Patient Health Questionnaire - Depression)
        • GAD-7 (General Anxiety Disorder Scale)
        • AUDIT (Alcohol Use Disorders Identification Test)
        • DAST (Drug Abuse Screening Test)
        • CAGE (Alcohol Screening)
        • Beck Depression Inventory
        • Hamilton Anxiety Rating Scale
        
        Select a scale from the dropdown above and click "Start Assessment" to begin.
        """)
        instructions.setWordWrap(True)
        instructions.setStyleSheet("margin: 20px; line-height: 1.4;")
        layout.addWidget(instructions)
        
        layout.addStretch()
        
        return widget
    
    def create_assessment_screen(self):
        """Create assessment questionnaire screen"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Scale title and description
        self.scale_title = QLabel()
        self.scale_title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.scale_title)
        
        self.scale_description = QLabel()
        self.scale_description.setWordWrap(True)
        self.scale_description.setStyleSheet("margin: 10px; color: #666;")
        layout.addWidget(self.scale_description)
        
        # Questions area
        self.questions_widget = QScrollArea()
        self.questions_widget.setWidgetResizable(True)
        layout.addWidget(self.questions_widget)
        
        # Progress and navigation
        nav_layout = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        nav_layout.addWidget(self.progress_bar)
        
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_question)
        nav_layout.addWidget(self.prev_button)
        
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_question)
        nav_layout.addWidget(self.next_button)
        
        self.finish_button = QPushButton("Finish Assessment")
        self.finish_button.clicked.connect(self.finish_assessment)
        self.finish_button.setVisible(False)
        nav_layout.addWidget(self.finish_button)
        
        layout.addLayout(nav_layout)
        
        return widget
    
    def create_results_screen(self):
        """Create results display screen"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Results header
        self.results_title = QLabel("Assessment Results")
        self.results_title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(self.results_title)
        
        # Score display
        self.score_widget = QWidget()
        self.score_layout = QVBoxLayout(self.score_widget)
        layout.addWidget(self.score_widget)
        
        # Interpretation
        self.interpretation_text = QTextEdit()
        self.interpretation_text.setReadOnly(True)
        self.interpretation_text.setMaximumHeight(200)
        layout.addWidget(self.interpretation_text)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save Results")
        save_button.clicked.connect(self.save_results)
        button_layout.addWidget(save_button)
        
        print_button = QPushButton("Print Report")
        print_button.clicked.connect(self.print_results)
        button_layout.addWidget(print_button)
        
        new_assessment_button = QPushButton("New Assessment")
        new_assessment_button.clicked.connect(self.new_assessment)
        button_layout.addWidget(new_assessment_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return widget
    
    def load_scales(self):
        """Load available clinical scales"""
        scales = [
            "PHQ-9 (Depression)",
            "GAD-7 (Anxiety)",
            "AUDIT (Alcohol)",
            "DAST (Drug Use)",
            "CAGE (Alcohol Screening)",
            "Beck Depression Inventory",
            "Hamilton Anxiety Scale"
        ]
        
        self.scale_combo.addItems(scales)
        
    def start_assessment(self):
        """Start the selected assessment"""
        scale_name = self.scale_combo.currentText()
        
        if scale_name.startswith("PHQ-9"):
            self.load_phq9_scale()
        elif scale_name.startswith("GAD-7"):
            self.load_gad7_scale()
        # Add other scales...
        
        self.assessment_area.setCurrentIndex(1)
        
    def load_phq9_scale(self):
        """Load PHQ-9 Depression Scale"""
        self.current_scale = {
            "name": "PHQ-9",
            "title": "Patient Health Questionnaire-9 (PHQ-9)",
            "description": "Over the last 2 weeks, how often have you been bothered by any of the following problems?",
            "questions": [
                "Little interest or pleasure in doing things",
                "Feeling down, depressed, or hopeless",
                "Trouble falling or staying asleep, or sleeping too much",
                "Feeling tired or having little energy",
                "Poor appetite or overeating",
                "Feeling bad about yourself or that you are a failure or have let yourself or your family down",
                "Trouble concentrating on things, such as reading the newspaper or watching television",
                "Moving or speaking so slowly that other people could have noticed. Or the opposite being so fidgety or restless that you have been moving around a lot more than usual",
                "Thoughts that you would be better off dead, or of hurting yourself in some way"
            ],
            "options": [
                "Not at all (0)",
                "Several days (1)",
                "More than half the days (2)",
                "Nearly every day (3)"
            ],
            "scoring": {
                "ranges": [
                    (0, 4, "Minimal depression"),
                    (5, 9, "Mild depression"),
                    (10, 14, "Moderate depression"),
                    (15, 19, "Moderately severe depression"),
                    (20, 27, "Severe depression")
                ]
            }
        }
        
        self.create_questionnaire()
        
    def create_questionnaire(self):
        """Create the questionnaire interface"""
        questions_content = QWidget()
        layout = QVBoxLayout(questions_content)
        
        self.scale_title.setText(self.current_scale["title"])
        self.scale_description.setText(self.current_scale["description"])
        
        self.question_widgets = []
        
        for i, question in enumerate(self.current_scale["questions"]):
            question_widget = QWidget()
            question_layout = QVBoxLayout(question_widget)
            
            # Question text
            question_label = QLabel(f"{i+1}. {question}")
            question_label.setWordWrap(True)
            question_label.setStyleSheet("font-weight: bold; margin: 10px 0;")
            question_layout.addWidget(question_label)
            
            # Options
            options_widget = QWidget()
            options_layout = QVBoxLayout(options_widget)
            
            button_group = QButtonGroup()
            option_buttons = []
            
            for j, option in enumerate(self.current_scale["options"]):
                radio_button = QRadioButton(option)
                radio_button.toggled.connect(lambda checked, q=i, opt=j: self.answer_changed(q, opt, checked))
                button_group.addButton(radio_button)
                option_buttons.append(radio_button)
                options_layout.addWidget(radio_button)
            
            question_layout.addWidget(options_widget)
            layout.addWidget(question_widget)
            
            self.question_widgets.append({
                'question': question,
                'buttons': option_buttons,
                'group': button_group
            })
        
        self.questions_widget.setWidget(questions_content)
        self.current_responses = {}
        self.update_progress()
    
    def answer_changed(self, question_idx, option_idx, checked):
        """Handle answer selection"""
        if checked:
            self.current_responses[question_idx] = option_idx
            self.update_progress()
    
    def update_progress(self):
        """Update progress bar and navigation"""
        completed = len(self.current_responses)
        total = len(self.current_scale["questions"])
        
        self.progress_bar.setMaximum(total)
        self.progress_bar.setValue(completed)
        
        if completed == total:
            self.finish_button.setVisible(True)
            self.next_button.setVisible(False)
        else:
            self.finish_button.setVisible(False)
            self.next_button.setVisible(True)
    
    def finish_assessment(self):
        """Complete assessment and show results"""
        if len(self.current_responses) != len(self.current_scale["questions"]):
            QMessageBox.warning(self, "Incomplete Assessment", "Please answer all questions before finishing.")
            return
        
        # Calculate score
        total_score = sum(self.current_responses.values())
        
        # Get interpretation
        interpretation = self.get_interpretation(total_score)
        
        # Display results
        self.show_results(total_score, interpretation)
        self.assessment_area.setCurrentIndex(2)
    
    def get_interpretation(self, score):
        """Get score interpretation"""
        for min_score, max_score, interpretation in self.current_scale["scoring"]["ranges"]:
            if min_score <= score <= max_score:
                return interpretation
        return "Score out of range"
    
    def show_results(self, score, interpretation):
        """Display assessment results"""
        self.results_title.setText(f"{self.current_scale['name']} Results")
        
        # Clear previous results
        for i in reversed(range(self.score_layout.count())):
            self.score_layout.itemAt(i).widget().setParent(None)
        
        # Score display
        score_label = QLabel(f"Total Score: {score}")
        score_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2196F3; margin: 20px;")
        self.score_layout.addWidget(score_label)
        
        severity_label = QLabel(f"Severity: {interpretation}")
        severity_label.setStyleSheet("font-size: 16px; margin: 10px;")
        self.score_layout.addWidget(severity_label)
        
        # Detailed interpretation
        detailed_interpretation = self.get_detailed_interpretation(score, interpretation)
        self.interpretation_text.setHtml(detailed_interpretation)
    
    def get_detailed_interpretation(self, score, interpretation):
        """Get detailed clinical interpretation"""
        if self.current_scale["name"] == "PHQ-9":
            interpretations = {
                "Minimal depression": """
                <h3>Minimal Depression (0-4)</h3>
                <p>The patient shows minimal signs of depression. This score suggests:</p>
                <ul>
                <li>Little to no functional impairment</li>
                <li>Routine monitoring may be sufficient</li>
                <li>Focus on prevention and wellness</li>
                </ul>
                """,
                "Mild depression": """
                <h3>Mild Depression (5-9)</h3>
                <p>The patient shows mild depressive symptoms. Consider:</p>
                <ul>
                <li>Watchful waiting or counseling</li>
                <li>Lifestyle modifications</li>
                <li>Regular follow-up in 2-4 weeks</li>
                </ul>
                """,
                "Moderate depression": """
                <h3>Moderate Depression (10-14)</h3>
                <p>The patient shows moderate depressive symptoms. Treatment recommendations:</p>
                <ul>
                <li>Counseling and/or medication</li>
                <li>Close monitoring</li>
                <li>Consider psychotherapy</li>
                </ul>
                """,
                "Moderately severe depression": """
                <h3>Moderately Severe Depression (15-19)</h3>
                <p>The patient shows moderately severe symptoms. Immediate action needed:</p>
                <ul>
                <li>Active treatment with medication and/or psychotherapy</li>
                <li>Weekly follow-up</li>
                <li>Consider psychiatric referral</li>
                </ul>
                """,
                "Severe depression": """
                <h3>Severe Depression (20-27)</h3>
                <p>The patient shows severe depressive symptoms. Urgent intervention required:</p>
                <ul>
                <li>Immediate psychiatric evaluation</li>
                <li>Medication and intensive psychotherapy</li>
                <li>Consider hospitalization if suicidal</li>
                <li>Daily monitoring may be needed</li>
                </ul>
                """
            }
            return interpretations.get(interpretation, "No interpretation available")
        
        return f"<h3>{interpretation}</h3><p>Score: {score}</p>"
```

---

## 🤖 **4. ML Export Functionality**

### **ML Data Export Service**
```python
# services/ml_export.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from typing import Dict, List, Optional
import json
import hashlib

class MLDataExporter:
    """
    Export psychiatric data in ML-ready format with proper anonymization
    """
    
    def __init__(self, session):
        self.session = session
        
    def export_comprehensive_dataset(self, 
                                   start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None,
                                   anonymize: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Export comprehensive dataset for ML training
        """
        
        datasets = {
            'patient_features': self.export_patient_features(anonymize),
            'medication_responses': self.export_medication_responses(anonymize),
            'symptom_trajectories': self.export_symptom_trajectories(anonymize),
            'substance_use_patterns': self.export_substance_patterns(anonymize),
            'lab_trends': self.export_lab_trends(anonymize),
            'assessment_scores': self.export_assessment_scores(anonymize),
            'treatment_outcomes': self.export_treatment_outcomes(anonymize)
        }
        
        return datasets
    
    def export_patient_features(self, anonymize: bool = True) -> pd.DataFrame:
        """Export patient demographic and clinical features"""
        
        query = """
        SELECT 
            p.id,
            p.age,
            p.gender,
            p.ethnicity,
            p.education_level,
            p.employment_status,
            p.insurance_type,
            COUNT(DISTINCT ph.id) as psychiatric_episodes,
            COUNT(DISTINCT m.id) as medication_count,
            COUNT(DISTINCT su.id) as substance_use_count,
            MIN(ph.created_at) as first_episode_date,
            MAX(ph.created_at) as last_episode_date
        FROM patients p
        LEFT JOIN psychiatric_history ph ON p.id = ph.patient_id
        LEFT JOIN medications m ON p.id = m.patient_id
        LEFT JOIN substance_use su ON p.id = su.patient_id
        GROUP BY p.id
        """
        
        df = pd.read_sql_query(query, self.session.bind)
        
        if anonymize:
            df['patient_id'] = df['id'].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16])
            df = df.drop('id', axis=1)
        
        # Feature engineering
        df['episodes_per_year'] = df.apply(
            lambda row: self._calculate_episodes_per_year(row), axis=1
        )
        
        # Encode categorical variables
        df = pd.get_dummies(df, columns=['gender', 'ethnicity', 'education_level', 
                                       'employment_status', 'insurance_type'])
        
        return df
    
    def export_medication_responses(self, anonymize: bool = True) -> pd.DataFrame:
        """Export medication effectiveness and side effects"""
        
        query = """
        SELECT 
            m.patient_id,
            m.medication_name,
            m.dosage,
            m.frequency,
            m.start_date,
            m.end_date,
            m.effectiveness_rating,
            m.side_effects,
            m.adherence_rating,
            m.discontinuation_reason,
            mc.category as medication_category,
            mc.mechanism as medication_mechanism
        FROM medications m
        LEFT JOIN medication_categories mc ON m.medication_name = mc.name
        WHERE m.effectiveness_rating IS NOT NULL
        """
        
        df = pd.read_sql_query(query, self.session.bind)
        
        if anonymize:
            df['patient_id'] = df['patient_id'].apply(
                lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
            )
        
        # Calculate treatment duration
        df['treatment_duration_days'] = (
            pd.to_datetime(df['end_date']) - pd.to_datetime(df['start_date'])
        ).dt.days
        
        # Parse side effects
        df['side_effect_count'] = df['side_effects'].apply(
            lambda x: len(x.split(',')) if x else 0
        )
        
        return df
    
    def export_symptom_trajectories(self, anonymize: bool = True) -> pd.DataFrame:
        """Export symptom progression over time"""
        
        query = """
        SELECT 
            sa.patient_id,
            sa.assessment_date,
            cs.name as scale_name,
            cs.category as symptom_category,
            sa.total_score,
            sa.severity_level,
            sa.responses
        FROM scale_assessments sa
        JOIN clinical_scales cs ON sa.scale_id = cs.id
        ORDER BY sa.patient_id, sa.assessment_date
        """
        
        df = pd.read_sql_query(query, self.session.bind)
        
        if anonymize:
            df['patient_id'] = df['patient_id'].apply(
                lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
            )
        
        # Calculate score changes over time
        df['score_change'] = df.groupby(['patient_id', 'scale_name'])['total_score'].diff()
        df['days_since_last_assessment'] = df.groupby(['patient_id', 'scale_name'])['assessment_date'].diff().dt.days
        
        # Create trajectory features
        df['improvement_rate'] = df['score_change'] / df['days_since_last_assessment']
        
        return df
    
    def export_substance_patterns(self, anonymize: bool = True) -> pd.DataFrame:
        """Export substance use patterns"""
        
        query = """
        SELECT 
            su.patient_id,
            st.name as substance_name,
            st.category as substance_category,
            su.frequency,
            su.amount,
            su.age_first_use,
            su.current_use,
            su.impact_work,
            su.impact_relationships,
            su.impact_mental_health,
            su.impact_physical_health,
            su.craving_level,
            su.relapse_risk
        FROM substance_use su
        JOIN substance_types st ON su.substance_type_id = st.id
        """
        
        df = pd.read_sql_query(query, self.session.bind)
        
        if anonymize:
            df['patient_id'] = df['patient_id'].apply(
                lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
            )
        
        # Calculate composite impact score
        impact_cols = ['impact_work', 'impact_relationships', 'impact_mental_health', 'impact_physical_health']
        df['total_impact_score'] = df[impact_cols].sum(axis=1)
        
        return df
    
    def export_lab_trends(self, anonymize: bool = True) -> pd.DataFrame:
        """Export laboratory results with trends"""
        
        query = """
        SELECT 
            lr.patient_id,
            lr.test_date,
            lr.test_name,
            lr.test_value,
            lr.reference_range,
            lr.abnormal_flag,
            lr.test_category
        FROM lab_results lr
        ORDER BY lr.patient_id, lr.test_name, lr.test_date
        """
        
        df = pd.read_sql_query(query, self.session.bind)
        
        if anonymize:
            df['patient_id'] = df['patient_id'].apply(
                lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
            )
        
        # Calculate trends
        df['value_change'] = df.groupby(['patient_id', 'test_name'])['test_value'].diff()
        df['days_between_tests'] = df.groupby(['patient_id', 'test_name'])['test_date'].diff().dt.days
        
        return df
    
    def create_ml_features(self, datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Create comprehensive feature matrix for ML training
        """
        
        # Start with patient features
        features = datasets['patient_features'].copy()
        
        # Add medication features
        med_features = self._create_medication_features(datasets['medication_responses'])
        features = features.merge(med_features, on='patient_id', how='left')
        
        # Add symptom trajectory features
        symptom_features = self._create_symptom_features(datasets['symptom_trajectories'])
        features = features.merge(symptom_features, on='patient_id', how='left')
        
        # Add substance use features
        substance_features = self._create_substance_features(datasets['substance_use_patterns'])
        features = features.merge(substance_features, on='patient_id', how='left')
        
        # Add lab features
        lab_features = self._create_lab_features(datasets['lab_trends'])
        features = features.merge(lab_features, on='patient_id', how='left')
        
        return features
    
    def _create_medication_features(self, med_df: pd.DataFrame) -> pd.DataFrame:
        """Create medication-based features"""
        
        features = med_df.groupby('patient_id').agg({
            'effectiveness_rating': ['mean', 'std', 'count'],
            'adherence_rating': ['mean', 'std'],
            'treatment_duration_days': ['mean', 'sum'],
            'side_effect_count': ['mean', 'sum']
        }).reset_index()
        
        # Flatten column names
        features.columns = ['patient_id'] + [f'med_{col[0]}_{col[1]}' for col in features.columns[1:]]
        
        return features
    
    def export_training_dataset(self, target_variable: str, 
                              prediction_horizon_days: int = 30) -> Dict[str, pd.DataFrame]:
        """
        Export dataset specifically formatted for ML training
        """
        
        # Get comprehensive dataset
        datasets = self.export_comprehensive_dataset()
        
        # Create feature matrix
        features = self.create_ml_features(datasets)
        
        # Create target variable based on prediction task
        if target_variable == 'treatment_response':
            targets = self._create_treatment_response_target(datasets, prediction_horizon_days)
        elif target_variable == 'relapse_risk':
            targets = self._create_relapse_risk_target(datasets, prediction_horizon_days)
        elif target_variable == 'hospitalization_risk':
            targets = self._create_hospitalization_target(datasets, prediction_horizon_days)
        
        # Merge features and targets
        training_data = features.merge(targets, on='patient_id', how='inner')
        
        # Split features and targets
        feature_cols = [col for col in training_data.columns if col not in ['patient_id', 'target']]
        
        return {
            'features': training_data[feature_cols],
            'targets': training_data['target'],
            'patient_ids': training_data['patient_id'],
            'feature_names': feature_cols
        }

# Export interface widget
class MLExportWidget(QWidget):
    """
    Interface for ML data export
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Export options
        options_group = QGroupBox("Export Options")
        options_layout = QFormLayout(options_group)
        
        self.anonymize_checkbox = QCheckBox("Anonymize patient data")
        self.anonymize_checkbox.setChecked(True)
        
        self.date_range_checkbox = QCheckBox("Use date range")
        self.start_date = QDateEdit()
        self.end_date = QDateEdit()
        
        self.export_format = QComboBox()
        self.export_format.addItems(["CSV", "JSON", "Parquet", "Excel"])
        
        options_layout.addRow("Anonymize:", self.anonymize_checkbox)
        options_layout.addRow("Date Range:", self.date_range_checkbox)
        options_layout.addRow("Start Date:", self.start_date)
        options_layout.addRow("End Date:", self.end_date)
        options_layout.addRow("Format:", self.export_format)
        
        layout.addWidget(options_group)
        
        # Dataset selection
        datasets_group = QGroupBox("Datasets to Export")
        datasets_layout = QVBoxLayout(datasets_group)
        
        self.dataset_checkboxes = {}
        datasets = [
            "Patient Features",
            "Medication Responses", 
            "Symptom Trajectories",
            "Substance Use Patterns",
            "Lab Trends",
            "Assessment Scores",
            "Treatment Outcomes"
        ]
        
        for dataset in datasets:
            checkbox = QCheckBox(dataset)
            checkbox.setChecked(True)
            self.dataset_checkboxes[dataset] = checkbox
            datasets_layout.addWidget(checkbox)
        
        layout.addWidget(datasets_group)
        
        # Export buttons
        button_layout = QHBoxLayout()
        
        export_button = QPushButton("Export Selected Datasets")
        export_button.clicked.connect(self.export_datasets)
        button_layout.addWidget(export_button)
        
        export_ml_button = QPushButton("Export ML Training Set")
        export_ml_button.clicked.connect(self.export_ml_training)
        button_layout.addWidget(export_ml_button)
        
        layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
    def export_datasets(self):
        """Export selected datasets"""
        # Implementation for dataset export
        pass
        
    def export_ml_training(self):
        """Export ML training dataset"""
        # Implementation for ML training export
        pass
```

---

## 🔧 **Phase 2 Integration Requirements**

### **Updated Main Application Structure**
```python
# Add to main_window.py
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_phase2_features()
        
    def setup_phase2_features(self):
        """Add Phase 2 features to main window"""
        
        # Add voice input to toolbar
        self.voice_action = QAction(qta.icon('fa5s.microphone'), 'Voice Input', self)
        self.voice_action.triggered.connect(self.toggle_voice_input)
        self.toolbar.addAction(self.voice_action)
        
        # Add substance tracking tab
        self.substance_tab = SubstanceTracker(self.current_patient_id)
        self.tab_widget.addTab(self.substance_tab, "Substance Use")
        
        # Add clinical scales tab
        self.scales_tab = ClinicalScalesWidget(self.current_patient_id)
        self.tab_widget.addTab(self.scales_tab, "Clinical Scales")
        
        # Add ML export to menu
        ml_menu = self.menuBar().addMenu('ML Export')
        export_action = QAction('Export Training Data', self)
        export_action.triggered.connect(self.show_ml_export)
        ml_menu.addAction(export_action)
```

### **Updated Dependencies for Phase 2**
```python
# Additional requirements for Phase 2
SpeechRecognition>=3.10.0
pyaudio>=0.2.11
matplotlib>=3.5.0
scikit-learn>=1.3.0
seaborn>=0.11.0
plotly>=5.0.0
```

### **Database Migrations for Phase 2**
```python
# Add to models/migrations.py
def create_phase2_tables(engine):
    """Create Phase 2 database tables"""
    
    # Create substance use tables
    SubstanceType.__table__.create(engine, checkfirst=True)
    SubstanceUse.__table__.create(engine, checkfirst=True)
    SubstanceUseLog.__table__.create(engine, checkfirst=True)
    
    # Create clinical scales tables
    ClinicalScale.__table__.create(engine, checkfirst=True)
    ScaleAssessment.__table__.create(engine, checkfirst=True)
    
    # Populate default data
    populate_substance_types(engine)
    populate_clinical_scales(engine)
```

---

## 🎯 **Phase 2 Implementation Timeline**

### **Week 1-2: Voice Input Integration**
- Implement VoiceService with real-time recognition
- Create VoiceInputWidget components
- Integrate with existing forms
- Add voice command shortcuts

### **Week 3-4: Substance Use Tracking**
- Create substance use models and database tables
- Build comprehensive substance tracking interface
- Implement usage timeline visualization
- Add standardized assessment tools (AUDIT, DAST, CAGE)

### **Week 5-6: Clinical Scales Integration**
- Implement clinical scales database structure
- Create assessment interface with common scales
- Add scoring algorithms and interpretations
- Build results visualization and reporting

### **Week 7-8: ML Export Functionality**
- Develop ML data export service
- Create feature engineering pipeline
- Build export interface with format options
- Add data validation and quality checks

---

## 📊 **Phase 2 Success Metrics**

- **Voice Recognition Accuracy**: >95% for clinical terminology
- **Assessment Completion Time**: <10 minutes for comprehensive substance assessment
- **Clinical Scale Implementation**: 7+ standardized scales with automated scoring
- **ML Export Quality**: 100% structured data with <5% missing values
- **User Workflow Efficiency**: 30% reduction in data entry time

---

*This Phase 2 implementation will transform the basic psychiatric records app into a comprehensive clinical assessment platform with advanced features for modern psychiatric practice and ML training data collection.*