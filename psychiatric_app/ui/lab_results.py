"""
Lab results widget for managing laboratory test results
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QDialog, QFormLayout, QLineEdit, QComboBox, QDateTimeEdit,
    QDoubleSpinBox, QTextEdit, QLabel, QCheckBox, QHeaderView, QMessageBox,
    QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal
from datetime import datetime

class LabResultsWidget(QWidget):
    """Widget for managing laboratory test results"""
    
    data_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.lab_results = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI layout"""
        layout = QVBoxLayout(self)
        
        # Header with add button
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Laboratory Results")
        title_label.setProperty("class", "subtitle")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.add_result_btn = QPushButton("Add Lab Result")
        self.add_result_btn.setProperty("class", "primary")
        self.add_result_btn.clicked.connect(self.add_lab_result)
        header_layout.addWidget(self.add_result_btn)
        
        layout.addLayout(header_layout)
        
        # Lab results table
        self.results_table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.results_table)
        
        # Summary section
        self.create_summary_section()
        layout.addWidget(self.summary_section)
    
    def setup_table(self):
        """Setup the lab results table"""
        self.results_table.setColumnCount(9)
        self.results_table.setHorizontalHeaderLabels([
            "Test Name", "Result", "Reference Range", "Status", "Collection Date",
            "Category", "Physician", "Critical", "Actions"
        ])
        
        # Set column widths
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Test name
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
        
        # Set alternating row colors
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    
    def create_summary_section(self):
        """Create lab results summary section"""
        self.summary_section = QGroupBox("Lab Results Summary")
        layout = QHBoxLayout(self.summary_section)
        
        # Total results count
        self.total_count_label = QLabel("Total Results: 0")
        layout.addWidget(self.total_count_label)
        
        layout.addStretch()
        
        # Abnormal results count
        self.abnormal_count_label = QLabel("Abnormal: 0")
        layout.addWidget(self.abnormal_count_label)
        
        layout.addStretch()
        
        # Critical values count
        self.critical_count_label = QLabel("Critical: 0")
        layout.addWidget(self.critical_count_label)
        
        layout.addStretch()
        
        # Latest test date
        self.latest_date_label = QLabel("Latest Test: None")
        layout.addWidget(self.latest_date_label)
    
    def add_lab_result(self):
        """Add a new lab result"""
        dialog = LabResultDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            result_data = dialog.get_data()
            self.lab_results.append(result_data)
            self.refresh_table()
            self.update_summary()
            self.data_changed.emit()
    
    def edit_lab_result(self, index):
        """Edit an existing lab result"""
        if 0 <= index < len(self.lab_results):
            dialog = LabResultDialog(self.lab_results[index], self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.lab_results[index] = dialog.get_data()
                self.refresh_table()
                self.update_summary()
                self.data_changed.emit()
    
    def delete_lab_result(self, index):
        """Delete a lab result"""
        if 0 <= index < len(self.lab_results):
            result = self.lab_results[index]
            reply = QMessageBox.question(
                self,
                "Delete Lab Result",
                f"Are you sure you want to delete {result['test_name']}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.lab_results.pop(index)
                self.refresh_table()
                self.update_summary()
                self.data_changed.emit()
    
    def refresh_table(self):
        """Refresh the lab results table"""
        self.results_table.setRowCount(len(self.lab_results))
        
        for row, result in enumerate(self.lab_results):
            # Test name
            name_item = QTableWidgetItem(result.get('test_name', ''))
            self.results_table.setItem(row, 0, name_item)
            
            # Result value
            value = result.get('value')
            text_value = result.get('text_value', '')
            unit = result.get('unit', '')
            
            if text_value:
                result_display = text_value
            elif value is not None:
                result_display = f"{value} {unit}".strip()
            else:
                result_display = "No result"
            
            result_item = QTableWidgetItem(result_display)
            self.results_table.setItem(row, 1, result_item)
            
            # Reference range
            ref_range = result.get('reference_range', '')
            ref_item = QTableWidgetItem(ref_range)
            self.results_table.setItem(row, 2, ref_item)
            
            # Status
            is_abnormal = result.get('is_abnormal', False)
            abnormal_flag = result.get('abnormal_flag', '')
            
            if abnormal_flag:
                status_text = abnormal_flag
                status_color = "red" if abnormal_flag in ['H', 'HH', 'L', 'LL'] else "black"
            elif is_abnormal:
                status_text = "Abnormal"
                status_color = "orange"
            else:
                status_text = "Normal"
                status_color = "green"
            
            status_item = QTableWidgetItem(status_text)
            status_item.setForeground(Qt.GlobalColor.red if status_color == "red" else 
                                    Qt.GlobalColor.blue if status_color == "orange" else 
                                    Qt.GlobalColor.darkGreen)
            self.results_table.setItem(row, 3, status_item)
            
            # Collection date
            collection_date = result.get('collection_date', '')
            if collection_date:
                if isinstance(collection_date, str):
                    date_display = collection_date[:10]  # Just the date part
                else:
                    date_display = collection_date.strftime('%Y-%m-%d')
            else:
                date_display = ''
            
            date_item = QTableWidgetItem(date_display)
            self.results_table.setItem(row, 4, date_item)
            
            # Category
            category_item = QTableWidgetItem(result.get('test_category', ''))
            self.results_table.setItem(row, 5, category_item)
            
            # Physician
            physician_item = QTableWidgetItem(result.get('ordering_physician', ''))
            self.results_table.setItem(row, 6, physician_item)
            
            # Critical
            is_critical = result.get('is_critical', False)
            critical_item = QTableWidgetItem("Yes" if is_critical else "No")
            if is_critical:
                critical_item.setForeground(Qt.GlobalColor.red)
            self.results_table.setItem(row, 7, critical_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, idx=row: self.edit_lab_result(idx))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("Delete")
            delete_btn.setProperty("class", "danger")
            delete_btn.clicked.connect(lambda checked, idx=row: self.delete_lab_result(idx))
            actions_layout.addWidget(delete_btn)
            
            self.results_table.setCellWidget(row, 8, actions_widget)
    
    def update_summary(self):
        """Update the summary section"""
        total_results = len(self.lab_results)
        abnormal_results = len([r for r in self.lab_results if r.get('is_abnormal', False)])
        critical_results = len([r for r in self.lab_results if r.get('is_critical', False)])
        
        # Update counts
        self.total_count_label.setText(f"Total Results: {total_results}")
        
        self.abnormal_count_label.setText(f"Abnormal: {abnormal_results}")
        if abnormal_results > 0:
            self.abnormal_count_label.setStyleSheet("color: orange;")
        else:
            self.abnormal_count_label.setStyleSheet("")
        
        self.critical_count_label.setText(f"Critical: {critical_results}")
        if critical_results > 0:
            self.critical_count_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.critical_count_label.setStyleSheet("")
        
        # Latest test date
        if self.lab_results:
            latest_date = max(
                (r.get('collection_date') for r in self.lab_results if r.get('collection_date')),
                default=None
            )
            if latest_date:
                if isinstance(latest_date, str):
                    date_display = latest_date[:10]
                else:
                    date_display = latest_date.strftime('%Y-%m-%d')
                self.latest_date_label.setText(f"Latest Test: {date_display}")
            else:
                self.latest_date_label.setText("Latest Test: No dates recorded")
        else:
            self.latest_date_label.setText("Latest Test: None")
    
    def get_data(self):
        """Get all lab results data"""
        return self.lab_results.copy()
    
    def set_data(self, data):
        """Set lab results data"""
        self.lab_results = data.copy() if data else []
        self.refresh_table()
        self.update_summary()
    
    def clear_form(self):
        """Clear all lab results"""
        self.lab_results = []
        self.refresh_table()
        self.update_summary()

class LabResultDialog(QDialog):
    """Dialog for adding/editing lab results"""
    
    def __init__(self, result_data=None, parent=None):
        super().__init__(parent)
        self.result_data = result_data.copy() if result_data else {}
        self.setup_ui()
        self.populate_fields()
    
    def setup_ui(self):
        """Setup dialog UI"""
        title = "Edit Lab Result" if self.result_data else "Add Lab Result"
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(500, 700)
        
        layout = QVBoxLayout(self)
        
        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        
        # Test information
        test_group = QGroupBox("Test Information")
        test_layout = QFormLayout(test_group)
        
        self.test_name_input = QLineEdit()
        self.test_name_input.setPlaceholderText("e.g., Complete Blood Count")
        test_layout.addRow("Test Name *:", self.test_name_input)
        
        self.test_code_input = QLineEdit()
        self.test_code_input.setPlaceholderText("e.g., CBC")
        test_layout.addRow("Test Code:", self.test_code_input)
        
        self.test_category_combo = QComboBox()
        self.test_category_combo.addItems([
            "", "Chemistry", "Hematology", "Immunology", "Microbiology",
            "Endocrinology", "Cardiology", "Toxicology", "Other"
        ])
        self.test_category_combo.setEditable(True)
        test_layout.addRow("Category:", self.test_category_combo)
        
        self.test_panel_input = QLineEdit()
        self.test_panel_input.setPlaceholderText("e.g., Comprehensive Metabolic Panel")
        test_layout.addRow("Panel:", self.test_panel_input)
        
        form_layout.addRow(test_group)
        
        # Results
        results_group = QGroupBox("Results")
        results_layout = QFormLayout(results_group)
        
        # Numeric value
        value_layout = QHBoxLayout()
        self.value_spin = QDoubleSpinBox()
        self.value_spin.setRange(-999999, 999999)
        self.value_spin.setDecimals(3)
        value_layout.addWidget(self.value_spin)
        
        self.unit_combo = QComboBox()
        self.unit_combo.addItems([
            "", "mg/dL", "g/dL", "mmol/L", "U/L", "IU/L", "pg/mL", "ng/mL",
            "µg/dL", "mEq/L", "cells/µL", "10³/µL", "10⁶/µL", "%", "ratio", "other"
        ])
        self.unit_combo.setEditable(True)
        value_layout.addWidget(self.unit_combo)
        
        results_layout.addRow("Numeric Value:", value_layout)
        
        # Text value (for non-numeric results)
        self.text_value_input = QLineEdit()
        self.text_value_input.setPlaceholderText("e.g., Positive, Negative, Detected")
        results_layout.addRow("Text Result:", self.text_value_input)
        
        # Reference range
        self.reference_range_input = QLineEdit()
        self.reference_range_input.setPlaceholderText("e.g., 3.5-5.0 mg/dL")
        results_layout.addRow("Reference Range:", self.reference_range_input)
        
        # Reference min/max for calculations
        ref_layout = QHBoxLayout()
        self.reference_min_spin = QDoubleSpinBox()
        self.reference_min_spin.setRange(-999999, 999999)
        self.reference_min_spin.setDecimals(3)
        ref_layout.addWidget(QLabel("Min:"))
        ref_layout.addWidget(self.reference_min_spin)
        
        self.reference_max_spin = QDoubleSpinBox()
        self.reference_max_spin.setRange(-999999, 999999)
        self.reference_max_spin.setDecimals(3)
        ref_layout.addWidget(QLabel("Max:"))
        ref_layout.addWidget(self.reference_max_spin)
        
        results_layout.addRow("Reference Min/Max:", ref_layout)
        
        # Status
        self.is_abnormal_checkbox = QCheckBox("Abnormal result")
        results_layout.addRow("", self.is_abnormal_checkbox)
        
        self.abnormal_flag_combo = QComboBox()
        self.abnormal_flag_combo.addItems(["", "H", "L", "HH", "LL"])
        results_layout.addRow("Abnormal Flag:", self.abnormal_flag_combo)
        
        form_layout.addRow(results_group)
        
        # Dates
        dates_group = QGroupBox("Dates")
        dates_layout = QFormLayout(dates_group)
        
        self.collection_date_input = QDateTimeEdit()
        self.collection_date_input.setDateTime(QDateTime.currentDateTime())
        self.collection_date_input.setCalendarPopup(True)
        dates_layout.addRow("Collection Date:", self.collection_date_input)
        
        self.result_date_input = QDateTimeEdit()
        self.result_date_input.setDateTime(QDateTime.currentDateTime())
        self.result_date_input.setCalendarPopup(True)
        dates_layout.addRow("Result Date:", self.result_date_input)
        
        form_layout.addRow(dates_group)
        
        # Clinical context
        context_group = QGroupBox("Clinical Context")
        context_layout = QFormLayout(context_group)
        
        self.ordering_physician_input = QLineEdit()
        context_layout.addRow("Ordering Physician:", self.ordering_physician_input)
        
        self.lab_facility_input = QLineEdit()
        context_layout.addRow("Lab Facility:", self.lab_facility_input)
        
        self.specimen_type_combo = QComboBox()
        self.specimen_type_combo.addItems([
            "", "Blood", "Serum", "Plasma", "Urine", "Saliva", "CSF", "Other"
        ])
        self.specimen_type_combo.setEditable(True)
        context_layout.addRow("Specimen Type:", self.specimen_type_combo)
        
        self.fasting_checkbox = QCheckBox("Fasting specimen")
        context_layout.addRow("", self.fasting_checkbox)
        
        form_layout.addRow(context_group)
        
        # Notes
        notes_group = QGroupBox("Notes and Interpretation")
        notes_layout = QFormLayout(notes_group)
        
        self.interpretation_input = QTextEdit()
        self.interpretation_input.setMaximumHeight(80)
        self.interpretation_input.setPlaceholderText("Clinical interpretation...")
        notes_layout.addRow("Interpretation:", self.interpretation_input)
        
        self.physician_notes_input = QTextEdit()
        self.physician_notes_input.setMaximumHeight(80)
        self.physician_notes_input.setPlaceholderText("Physician notes...")
        notes_layout.addRow("Physician Notes:", self.physician_notes_input)
        
        form_layout.addRow(notes_group)
        
        # Critical values
        critical_group = QGroupBox("Critical Values")
        critical_layout = QFormLayout(critical_group)
        
        self.is_critical_checkbox = QCheckBox("Critical value")
        critical_layout.addRow("", self.is_critical_checkbox)
        
        self.critical_notified_checkbox = QCheckBox("Physician notified")
        critical_layout.addRow("", self.critical_notified_checkbox)
        
        form_layout.addRow(critical_group)
        
        scroll.setWidget(form_widget)
        layout.addWidget(scroll)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setProperty("class", "primary")
        save_btn.clicked.connect(self.save_result)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def populate_fields(self):
        """Populate form fields with existing data"""
        if not self.result_data:
            return
        
        data = self.result_data
        
        self.test_name_input.setText(data.get('test_name', ''))
        self.test_code_input.setText(data.get('test_code', ''))
        self.test_category_combo.setCurrentText(data.get('test_category', ''))
        self.test_panel_input.setText(data.get('test_panel', ''))
        
        if data.get('value') is not None:
            self.value_spin.setValue(data['value'])
        self.unit_combo.setCurrentText(data.get('unit', ''))
        self.text_value_input.setText(data.get('text_value', ''))
        
        self.reference_range_input.setText(data.get('reference_range', ''))
        if data.get('reference_min') is not None:
            self.reference_min_spin.setValue(data['reference_min'])
        if data.get('reference_max') is not None:
            self.reference_max_spin.setValue(data['reference_max'])
        
        self.is_abnormal_checkbox.setChecked(data.get('is_abnormal', False))
        self.abnormal_flag_combo.setCurrentText(data.get('abnormal_flag', ''))
        
        if data.get('collection_date'):
            if isinstance(data['collection_date'], str):
                self.collection_date_input.setDateTime(QDateTime.fromString(data['collection_date'], Qt.DateFormat.ISODate))
            else:
                self.collection_date_input.setDateTime(QDateTime(data['collection_date']))
        
        if data.get('result_date'):
            if isinstance(data['result_date'], str):
                self.result_date_input.setDateTime(QDateTime.fromString(data['result_date'], Qt.DateFormat.ISODate))
            else:
                self.result_date_input.setDateTime(QDateTime(data['result_date']))
        
        self.ordering_physician_input.setText(data.get('ordering_physician', ''))
        self.lab_facility_input.setText(data.get('lab_facility', ''))
        self.specimen_type_combo.setCurrentText(data.get('specimen_type', ''))
        self.fasting_checkbox.setChecked(data.get('fasting_status', False))
        
        self.interpretation_input.setPlainText(data.get('interpretation', ''))
        self.physician_notes_input.setPlainText(data.get('physician_notes', ''))
        
        self.is_critical_checkbox.setChecked(data.get('is_critical', False))
        self.critical_notified_checkbox.setChecked(data.get('critical_notified', False))
    
    def save_result(self):
        """Save lab result data"""
        # Validate required fields
        if not self.test_name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Test name is required.")
            return
        
        self.accept()
    
    def get_data(self):
        """Get lab result data from form"""
        return {
            'test_name': self.test_name_input.text().strip(),
            'test_code': self.test_code_input.text().strip(),
            'test_category': self.test_category_combo.currentText(),
            'test_panel': self.test_panel_input.text().strip(),
            'value': self.value_spin.value() if self.value_spin.value() != 0 else None,
            'text_value': self.text_value_input.text().strip(),
            'unit': self.unit_combo.currentText(),
            'reference_range': self.reference_range_input.text().strip(),
            'reference_min': self.reference_min_spin.value() if self.reference_min_spin.value() != 0 else None,
            'reference_max': self.reference_max_spin.value() if self.reference_max_spin.value() != 0 else None,
            'is_abnormal': self.is_abnormal_checkbox.isChecked(),
            'abnormal_flag': self.abnormal_flag_combo.currentText(),
            'collection_date': self.collection_date_input.dateTime().toPython(),
            'result_date': self.result_date_input.dateTime().toPython(),
            'ordering_physician': self.ordering_physician_input.text().strip(),
            'lab_facility': self.lab_facility_input.text().strip(),
            'specimen_type': self.specimen_type_combo.currentText(),
            'fasting_status': self.fasting_checkbox.isChecked(),
            'interpretation': self.interpretation_input.toPlainText().strip(),
            'physician_notes': self.physician_notes_input.toPlainText().strip(),
            'is_critical': self.is_critical_checkbox.isChecked(),
            'critical_notified': self.critical_notified_checkbox.isChecked(),
        }