"""
Main window for the Enhanced Psychiatric Records Application
"""

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QMenuBar, QStatusBar, QToolBar, QLabel, QPushButton, QMessageBox,
    QApplication, QSplitter, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QIcon, QKeySequence

from psychiatric_app.ui.components.theme_manager import ThemeManager
from psychiatric_app.ui.demographics_form import DemographicsForm
from psychiatric_app.ui.symptom_assessment import SymptomAssessmentWidget
from psychiatric_app.ui.medication_manager import MedicationManager
from psychiatric_app.ui.lab_results import LabResultsWidget
from psychiatric_app.config.settings import (
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT,
    AUTO_SAVE_INTERVAL
)

class MainWindow(QMainWindow):
    """Main application window with tabbed interface"""
    
    def __init__(self):
        super().__init__()
        self.current_patient_id = None
        self.unsaved_changes = False
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        
        # Setup UI
        self.setup_ui()
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()
        self.setup_auto_save()
        
        # Connect signals
        self.setup_connections()
        
        # Set window properties
        self.setWindowTitle("Enhanced Psychiatric Records")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
    
    def setup_ui(self):
        """Setup the main UI layout"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel for patient selection/search (optional for Phase 1)
        self.create_patient_panel()
        splitter.addWidget(self.patient_panel)
        
        # Main content area with tabs
        self.create_main_content()
        splitter.addWidget(self.main_content)
        
        # Set splitter sizes (25% left, 75% right)
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
    
    def create_patient_panel(self):
        """Create left panel for patient information"""
        self.patient_panel = QFrame()
        self.patient_panel.setMaximumWidth(350)
        self.patient_panel.setMinimumWidth(250)
        
        layout = QVBoxLayout(self.patient_panel)
        
        # Patient info header
        header_label = QLabel("Current Patient")
        header_label.setProperty("class", "title")
        layout.addWidget(header_label)
        
        # Patient details (will be populated when patient is selected)
        self.patient_info_label = QLabel("No patient selected")
        self.patient_info_label.setProperty("class", "subtitle")
        self.patient_info_label.setWordWrap(True)
        layout.addWidget(self.patient_info_label)
        
        # Quick actions
        actions_layout = QVBoxLayout()
        
        self.new_patient_btn = QPushButton("New Patient")
        self.new_patient_btn.setProperty("class", "primary")
        self.new_patient_btn.clicked.connect(self.new_patient)
        actions_layout.addWidget(self.new_patient_btn)
        
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setProperty("class", "primary")
        self.save_btn.clicked.connect(self.save_current_patient)
        self.save_btn.setEnabled(False)
        actions_layout.addWidget(self.save_btn)
        
        layout.addLayout(actions_layout)
        layout.addStretch()
    
    def create_main_content(self):
        """Create main content area with tabs"""
        self.main_content = QTabWidget()
        
        # Demographics tab
        self.demographics_form = DemographicsForm()
        self.main_content.addTab(self.demographics_form, "Demographics")
        
        # Symptom Assessment tab  
        self.symptom_assessment = SymptomAssessmentWidget()
        self.main_content.addTab(self.symptom_assessment, "Symptoms")
        
        # Medications tab
        self.medication_manager = MedicationManager()
        self.main_content.addTab(self.medication_manager, "Medications")
        
        # Lab Results tab
        self.lab_results = LabResultsWidget()
        self.main_content.addTab(self.lab_results, "Lab Results")
        
        # Connect tab change signal
        self.main_content.currentChanged.connect(self.on_tab_changed)
    
    def setup_menu_bar(self):
        """Setup application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Patient", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_patient)
        file_menu.addAction(new_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_current_patient)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        toggle_theme_action = QAction("Toggle Theme", self)
        toggle_theme_action.setShortcut("Ctrl+T")
        toggle_theme_action.triggered.connect(self.theme_manager.toggle_theme)
        view_menu.addAction(toggle_theme_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_toolbar(self):
        """Setup application toolbar"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # New patient button
        new_patient_action = QAction("New Patient", self)
        new_patient_action.triggered.connect(self.new_patient)
        toolbar.addAction(new_patient_action)
        
        # Save button
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_current_patient)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Theme toggle button
        theme_action = QAction("Toggle Theme", self)
        theme_action.triggered.connect(self.theme_manager.toggle_theme)
        toolbar.addAction(theme_action)
    
    def setup_status_bar(self):
        """Setup application status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status labels
        self.patient_status_label = QLabel("No patient selected")
        self.save_status_label = QLabel("Ready")
        self.auto_save_label = QLabel("Auto-save: ON")
        
        self.status_bar.addWidget(self.patient_status_label)
        self.status_bar.addPermanentWidget(self.save_status_label)
        self.status_bar.addPermanentWidget(self.auto_save_label)
    
    def setup_auto_save(self):
        """Setup auto-save functionality"""
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(AUTO_SAVE_INTERVAL * 1000)  # Convert to milliseconds
    
    def setup_connections(self):
        """Setup signal connections"""
        # Theme change connection
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # Data change connections (will be implemented when forms are ready)
        # self.demographics_form.data_changed.connect(self.on_data_changed)
        # self.symptom_assessment.data_changed.connect(self.on_data_changed)
        # self.medication_manager.data_changed.connect(self.on_data_changed)
        # self.lab_results.data_changed.connect(self.on_data_changed)
    
    def center_on_screen(self):
        """Center the window on the screen"""
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
    
    def new_patient(self):
        """Create a new patient record"""
        if self.unsaved_changes:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them first?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                if not self.save_current_patient():
                    return  # Save failed, don't proceed
            elif reply == QMessageBox.StandardButton.Cancel:
                return  # User cancelled
        
        # Clear all forms
        self.clear_all_forms()
        self.current_patient_id = None
        self.unsaved_changes = False
        
        # Update UI
        self.patient_info_label.setText("New Patient")
        self.patient_status_label.setText("Creating new patient")
        self.save_btn.setEnabled(False)
        
        # Focus on first tab
        self.main_content.setCurrentIndex(0)
    
    def save_current_patient(self):
        """Save the current patient data"""
        try:
            # Collect data from all forms
            patient_data = {
                'demographics': self.demographics_form.get_data(),
                'symptoms': self.symptom_assessment.get_data(),
                'medications': self.medication_manager.get_data(),
                'lab_results': self.lab_results.get_data()
            }
            
            # Validate required fields
            if not self.validate_patient_data(patient_data):
                return False
            
            # Save to database (will be implemented with database service)
            # success = self.patient_service.save_patient(self.current_patient_id, patient_data)
            success = True  # Placeholder
            
            if success:
                self.unsaved_changes = False
                self.save_status_label.setText("Saved successfully")
                self.save_btn.setEnabled(False)
                
                # Clear status after 3 seconds
                QTimer.singleShot(3000, lambda: self.save_status_label.setText("Ready"))
                return True
            else:
                QMessageBox.critical(self, "Save Error", "Failed to save patient data.")
                return False
                
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"An error occurred while saving: {str(e)}")
            return False
    
    def auto_save(self):
        """Auto-save current patient data if changes exist"""
        if self.unsaved_changes and self.current_patient_id:
            self.save_current_patient()
            self.auto_save_label.setText("Auto-saved")
            QTimer.singleShot(2000, lambda: self.auto_save_label.setText("Auto-save: ON"))
    
    def validate_patient_data(self, data):
        """Validate patient data before saving"""
        demographics = data.get('demographics', {})
        
        # Check required fields
        required_fields = ['first_name', 'last_name', 'date_of_birth']
        missing_fields = []
        
        for field in required_fields:
            if not demographics.get(field):
                missing_fields.append(field.replace('_', ' ').title())
        
        if missing_fields:
            QMessageBox.warning(
                self,
                "Missing Required Fields",
                f"Please fill in the following required fields:\n" + "\n".join(missing_fields)
            )
            return False
        
        return True
    
    def clear_all_forms(self):
        """Clear all form data"""
        self.demographics_form.clear_form()
        self.symptom_assessment.clear_form()
        self.medication_manager.clear_form()
        self.lab_results.clear_form()
    
    def on_data_changed(self):
        """Handle data change events"""
        self.unsaved_changes = True
        self.save_btn.setEnabled(True)
        self.save_status_label.setText("Unsaved changes")
    
    def on_tab_changed(self, index):
        """Handle tab change events"""
        tab_names = ["Demographics", "Symptoms", "Medications", "Lab Results"]
        if 0 <= index < len(tab_names):
            self.status_bar.showMessage(f"Viewing: {tab_names[index]}", 2000)
    
    def on_theme_changed(self, theme_name):
        """Handle theme change events"""
        self.status_bar.showMessage(f"Theme changed to: {theme_name.title()}", 2000)
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Enhanced Psychiatric Records",
            """
            <h3>Enhanced Psychiatric Records v1.0</h3>
            <p>A comprehensive desktop application for psychiatric patient record management.</p>
            <p><b>Features:</b></p>
            <ul>
                <li>Comprehensive patient demographics</li>
                <li>DSM-5 TR symptom assessment</li>
                <li>Medication tracking</li>
                <li>Lab results management</li>
                <li>Encrypted local database</li>
                <li>Modern dark/light themes</li>
            </ul>
            <p><b>Built with:</b> PyQt6, SQLAlchemy, SQLCipher</p>
            """
        )
    
    def closeEvent(self, event):
        """Handle application close event"""
        if self.unsaved_changes:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save them before exiting?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                if self.save_current_patient():
                    event.accept()
                else:
                    event.ignore()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()