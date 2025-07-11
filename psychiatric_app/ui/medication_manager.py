"""
Medication manager widget for tracking patient medications
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit,
    QSpinBox, QTextEdit, QLabel, QCheckBox, QHeaderView, QMessageBox,
    QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from datetime import datetime

class MedicationManagerWidget(QWidget):
    """Widget for managing patient medications"""
    
    data_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.medications = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI layout"""
        layout = QVBoxLayout(self)
        
        # Header with add button
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Medication Management")
        title_label.setProperty("class", "subtitle")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.add_medication_btn = QPushButton("Add Medication")
        self.add_medication_btn.setProperty("class", "primary")
        self.add_medication_btn.clicked.connect(self.add_medication)
        header_layout.addWidget(self.add_medication_btn)
        
        layout.addLayout(header_layout)
        
        # Medications table
        self.medications_table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.medications_table)
        
        # Summary section
        self.create_summary_section()
        layout.addWidget(self.summary_section)
    
    def setup_table(self):
        """Setup the medications table"""
        self.medications_table.setColumnCount(9)
        self.medications_table.setHorizontalHeaderLabels([
            "Medication", "Dose", "Frequency", "Route", "Start Date", 
            "Effectiveness", "Side Effects", "Current", "Actions"
        ])
        
        # Set column widths
        header = self.medications_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Medication name
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
        
        # Set alternating row colors
        self.medications_table.setAlternatingRowColors(True)
        self.medications_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    
    def create_summary_section(self):
        """Create medication summary section"""
        self.summary_section = QGroupBox("Medication Summary")
        layout = QHBoxLayout(self.summary_section)
        
        # Current medications count
        self.current_count_label = QLabel("Current Medications: 0")
        layout.addWidget(self.current_count_label)
        
        layout.addStretch()
        
        # Psychiatric medications count
        self.psychiatric_count_label = QLabel("Psychiatric: 0")
        layout.addWidget(self.psychiatric_count_label)
        
        layout.addStretch()
        
        # Side effects alert
        self.side_effects_label = QLabel("Side Effects: None reported")
        layout.addWidget(self.side_effects_label)
    
    def add_medication(self):
        """Add a new medication"""
        dialog = MedicationDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            medication_data = dialog.get_data()
            self.medications.append(medication_data)
            self.refresh_table()
            self.update_summary()
            self.data_changed.emit()
    
    def edit_medication(self, index):
        """Edit an existing medication"""
        if 0 <= index < len(self.medications):
            dialog = MedicationDialog(self.medications[index], self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.medications[index] = dialog.get_data()
                self.refresh_table()
                self.update_summary()
                self.data_changed.emit()
    
    def delete_medication(self, index):
        """Delete a medication"""
        if 0 <= index < len(self.medications):
            medication = self.medications[index]
            reply = QMessageBox.question(
                self,
                "Delete Medication",
                f"Are you sure you want to delete {medication['name']}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.medications.pop(index)
                self.refresh_table()
                self.update_summary()
                self.data_changed.emit()
    
    def refresh_table(self):
        """Refresh the medications table"""
        self.medications_table.setRowCount(len(self.medications))
        
        for row, medication in enumerate(self.medications):
            # Medication name
            name_item = QTableWidgetItem(medication.get('name', ''))
            self.medications_table.setItem(row, 0, name_item)
            
            # Dose
            dose = f"{medication.get('dose_amount', '')} {medication.get('dose_unit', '')}"
            dose_item = QTableWidgetItem(dose.strip())
            self.medications_table.setItem(row, 1, dose_item)
            
            # Frequency
            frequency_item = QTableWidgetItem(medication.get('frequency', ''))
            self.medications_table.setItem(row, 2, frequency_item)
            
            # Route
            route_item = QTableWidgetItem(medication.get('route', ''))
            self.medications_table.setItem(row, 3, route_item)
            
            # Start date
            start_date = medication.get('start_date', '')
            if start_date:
                start_date_item = QTableWidgetItem(str(start_date))
            else:
                start_date_item = QTableWidgetItem('')
            self.medications_table.setItem(row, 4, start_date_item)
            
            # Effectiveness
            effectiveness = medication.get('effectiveness', 0)
            effectiveness_item = QTableWidgetItem(f"{effectiveness}%" if effectiveness else '')
            self.medications_table.setItem(row, 5, effectiveness_item)
            
            # Side effects
            side_effects = medication.get('side_effects', '')
            side_effects_item = QTableWidgetItem(side_effects[:50] + "..." if len(side_effects) > 50 else side_effects)
            self.medications_table.setItem(row, 6, side_effects_item)
            
            # Current status
            is_current = medication.get('is_current', True)
            current_item = QTableWidgetItem("Yes" if is_current else "No")
            self.medications_table.setItem(row, 7, current_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, idx=row: self.edit_medication(idx))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("Delete")
            delete_btn.setProperty("class", "danger")
            delete_btn.clicked.connect(lambda checked, idx=row: self.delete_medication(idx))
            actions_layout.addWidget(delete_btn)
            
            self.medications_table.setCellWidget(row, 8, actions_widget)
    
    def update_summary(self):
        """Update the summary section"""
        current_meds = [med for med in self.medications if med.get('is_current', True)]
        psychiatric_meds = [med for med in current_meds if self.is_psychiatric_medication(med)]
        
        # Update counts
        self.current_count_label.setText(f"Current Medications: {len(current_meds)}")
        self.psychiatric_count_label.setText(f"Psychiatric: {len(psychiatric_meds)}")
        
        # Check for side effects
        side_effects = []
        for med in current_meds:
            if med.get('side_effects'):
                side_effects.append(med['name'])
        
        if side_effects:
            self.side_effects_label.setText(f"Side Effects: {len(side_effects)} medication(s)")
            self.side_effects_label.setStyleSheet("color: orange;")
        else:
            self.side_effects_label.setText("Side Effects: None reported")
            self.side_effects_label.setStyleSheet("")
    
    def is_psychiatric_medication(self, medication):
        """Check if medication is psychiatric"""
        psychiatric_classes = [
            'antidepressant', 'antipsychotic', 'anxiolytic', 'mood stabilizer',
            'stimulant', 'sedative', 'hypnotic', 'anticonvulsant'
        ]
        medication_class = medication.get('medication_class', '').lower()
        return any(cls in medication_class for cls in psychiatric_classes)
    
    def get_data(self):
        """Get all medication data"""
        return self.medications.copy()
    
    def set_data(self, data):
        """Set medication data"""
        self.medications = data.copy() if data else []
        self.refresh_table()
        self.update_summary()
    
    def clear_form(self):
        """Clear all medications"""
        self.medications = []
        self.refresh_table()
        self.update_summary()

class MedicationDialog(QDialog):
    """Dialog for adding/editing medications"""
    
    def __init__(self, medication_data=None, parent=None):
        super().__init__(parent)
        self.medication_data = medication_data.copy() if medication_data else {}
        self.setup_ui()
        self.populate_fields()
    
    def setup_ui(self):
        """Setup dialog UI"""
        title = "Edit Medication" if self.medication_data else "Add Medication"
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 700)
        
        layout = QVBoxLayout(self)
        
        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        
        # Basic medication info
        basic_group = QGroupBox("Basic Information")
        basic_layout = QFormLayout(basic_group)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Sertraline")
        basic_layout.addRow("Medication Name *:", self.name_input)
        
        self.generic_name_input = QLineEdit()
        basic_layout.addRow("Generic Name:", self.generic_name_input)
        
        self.brand_name_input = QLineEdit()
        self.brand_name_input.setPlaceholderText("e.g., Zoloft")
        basic_layout.addRow("Brand Name:", self.brand_name_input)
        
        self.medication_class_combo = QComboBox()
        self.medication_class_combo.addItems([
            "", "Antidepressant", "Antipsychotic", "Anxiolytic", "Mood Stabilizer",
            "Stimulant", "Sedative", "Hypnotic", "Anticonvulsant", "Antihypertensive",
            "Diabetes Medication", "Pain Medication", "Other"
        ])
        self.medication_class_combo.setEditable(True)
        basic_layout.addRow("Medication Class:", self.medication_class_combo)
        
        form_layout.addRow(basic_group)
        
        # Dosage information
        dosage_group = QGroupBox("Dosage Information")
        dosage_layout = QFormLayout(dosage_group)
        
        dose_layout = QHBoxLayout()
        self.dose_amount_input = QLineEdit()
        self.dose_amount_input.setPlaceholderText("50")
        dose_layout.addWidget(self.dose_amount_input)
        
        self.dose_unit_combo = QComboBox()
        self.dose_unit_combo.addItems(["mg", "g", "ml", "units", "mcg", "other"])
        self.dose_unit_combo.setEditable(True)
        dose_layout.addWidget(self.dose_unit_combo)
        
        dosage_layout.addRow("Dose:", dose_layout)
        
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItems([
            "", "Once daily (QD)", "Twice daily (BID)", "Three times daily (TID)",
            "Four times daily (QID)", "Every other day", "At bedtime (QHS)",
            "As needed (PRN)", "Weekly", "Other"
        ])
        self.frequency_combo.setEditable(True)
        dosage_layout.addRow("Frequency:", self.frequency_combo)
        
        self.route_combo = QComboBox()
        self.route_combo.addItems([
            "", "Oral (PO)", "Intramuscular (IM)", "Intravenous (IV)",
            "Subcutaneous (SQ)", "Topical", "Sublingual", "Other"
        ])
        self.route_combo.setEditable(True)
        dosage_layout.addRow("Route:", self.route_combo)
        
        self.instructions_input = QTextEdit()
        self.instructions_input.setMaximumHeight(60)
        self.instructions_input.setPlaceholderText("Special instructions...")
        dosage_layout.addRow("Instructions:", self.instructions_input)
        
        form_layout.addRow(dosage_group)
        
        # Timing
        timing_group = QGroupBox("Timing")
        timing_layout = QFormLayout(timing_group)
        
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        timing_layout.addRow("Start Date:", self.start_date_input)
        
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate())
        self.end_date_input.setCalendarPopup(True)
        timing_layout.addRow("End Date:", self.end_date_input)
        
        self.is_current_checkbox = QCheckBox("Currently taking")
        self.is_current_checkbox.setChecked(True)
        timing_layout.addRow("", self.is_current_checkbox)
        
        form_layout.addRow(timing_group)
        
        # Clinical response
        response_group = QGroupBox("Clinical Response")
        response_layout = QFormLayout(response_group)
        
        self.effectiveness_spin = QSpinBox()
        self.effectiveness_spin.setRange(0, 100)
        self.effectiveness_spin.setSuffix("%")
        response_layout.addRow("Effectiveness (0-100%):", self.effectiveness_spin)
        
        self.adherence_spin = QSpinBox()
        self.adherence_spin.setRange(0, 100)
        self.adherence_spin.setSuffix("%")
        self.adherence_spin.setValue(100)
        response_layout.addRow("Adherence (0-100%):", self.adherence_spin)
        
        self.side_effects_input = QTextEdit()
        self.side_effects_input.setMaximumHeight(80)
        self.side_effects_input.setPlaceholderText("Any side effects experienced...")
        response_layout.addRow("Side Effects:", self.side_effects_input)
        
        form_layout.addRow(response_group)
        
        # Clinical context
        context_group = QGroupBox("Clinical Context")
        context_layout = QFormLayout(context_group)
        
        self.indication_input = QLineEdit()
        self.indication_input.setPlaceholderText("e.g., Major Depressive Disorder")
        context_layout.addRow("Indication:", self.indication_input)
        
        self.prescriber_input = QLineEdit()
        context_layout.addRow("Prescriber:", self.prescriber_input)
        
        self.pharmacy_input = QLineEdit()
        context_layout.addRow("Pharmacy:", self.pharmacy_input)
        
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("Additional notes...")
        context_layout.addRow("Notes:", self.notes_input)
        
        form_layout.addRow(context_group)
        
        scroll.setWidget(form_widget)
        layout.addWidget(scroll)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setProperty("class", "primary")
        save_btn.clicked.connect(self.save_medication)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def populate_fields(self):
        """Populate form fields with existing data"""
        if not self.medication_data:
            return
        
        data = self.medication_data
        
        self.name_input.setText(data.get('name', ''))
        self.generic_name_input.setText(data.get('generic_name', ''))
        self.brand_name_input.setText(data.get('brand_name', ''))
        self.medication_class_combo.setCurrentText(data.get('medication_class', ''))
        
        self.dose_amount_input.setText(str(data.get('dose_amount', '')))
        self.dose_unit_combo.setCurrentText(data.get('dose_unit', ''))
        self.frequency_combo.setCurrentText(data.get('frequency', ''))
        self.route_combo.setCurrentText(data.get('route', ''))
        self.instructions_input.setPlainText(data.get('instructions', ''))
        
        if data.get('start_date'):
            if isinstance(data['start_date'], str):
                self.start_date_input.setDate(QDate.fromString(data['start_date'], Qt.DateFormat.ISODate))
            else:
                self.start_date_input.setDate(QDate(data['start_date']))
        
        if data.get('end_date'):
            if isinstance(data['end_date'], str):
                self.end_date_input.setDate(QDate.fromString(data['end_date'], Qt.DateFormat.ISODate))
            else:
                self.end_date_input.setDate(QDate(data['end_date']))
        
        self.is_current_checkbox.setChecked(data.get('is_current', True))
        self.effectiveness_spin.setValue(data.get('effectiveness', 0))
        self.adherence_spin.setValue(data.get('adherence', 100))
        self.side_effects_input.setPlainText(data.get('side_effects', ''))
        
        self.indication_input.setText(data.get('indication', ''))
        self.prescriber_input.setText(data.get('prescriber', ''))
        self.pharmacy_input.setText(data.get('pharmacy', ''))
        self.notes_input.setPlainText(data.get('notes', ''))
    
    def save_medication(self):
        """Save medication data"""
        # Validate required fields
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Medication name is required.")
            return
        
        self.accept()
    
    def get_data(self):
        """Get medication data from form"""
        return {
            'name': self.name_input.text().strip(),
            'generic_name': self.generic_name_input.text().strip(),
            'brand_name': self.brand_name_input.text().strip(),
            'medication_class': self.medication_class_combo.currentText(),
            'dose_amount': float(self.dose_amount_input.text()) if self.dose_amount_input.text().strip() else None,
            'dose_unit': self.dose_unit_combo.currentText(),
            'frequency': self.frequency_combo.currentText(),
            'route': self.route_combo.currentText(),
            'instructions': self.instructions_input.toPlainText().strip(),
            'start_date': self.start_date_input.date().toPython(),
            'end_date': self.end_date_input.date().toPython(),
            'is_current': self.is_current_checkbox.isChecked(),
            'effectiveness': self.effectiveness_spin.value(),
            'adherence': self.adherence_spin.value(),
            'side_effects': self.side_effects_input.toPlainText().strip(),
            'indication': self.indication_input.text().strip(),
            'prescriber': self.prescriber_input.text().strip(),
            'pharmacy': self.pharmacy_input.text().strip(),
            'notes': self.notes_input.toPlainText().strip(),
        }