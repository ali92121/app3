"""
Symptom assessment widget with DSM-5 TR hierarchical structure
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QCheckBox, QComboBox, QLineEdit, QPushButton, QTextEdit, QDialog,
    QLabel, QScrollArea, QSplitter, QGroupBox, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from psychiatric_app.data.dsm5_hierarchy import DSM5_HIERARCHY

class SymptomAssessmentWidget(QWidget):
    """DSM-5 TR symptom assessment with hierarchical tree structure"""
    
    data_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.symptom_data = {}
        self.setup_ui()
        self.build_symptom_tree()
    
    def setup_ui(self):
        """Setup the main UI layout"""
        layout = QVBoxLayout(self)
        
        # Create splitter for tree and details
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel: Symptom tree
        tree_widget = QWidget()
        tree_layout = QVBoxLayout(tree_widget)
        
        tree_label = QLabel("DSM-5 TR Symptom Assessment")
        tree_label.setProperty("class", "subtitle")
        tree_layout.addWidget(tree_label)
        
        # Create hierarchical tree view
        self.symptom_tree = QTreeWidget()
        self.symptom_tree.setHeaderLabels([
            "Symptom", "Present", "Severity", "Duration", "Details"
        ])
        self.symptom_tree.setAlternatingRowColors(True)
        tree_layout.addWidget(self.symptom_tree)
        
        splitter.addWidget(tree_widget)
        
        # Right panel: Symptom details
        details_widget = self.create_details_panel()
        splitter.addWidget(details_widget)
        
        # Set splitter sizes (60% tree, 40% details)
        splitter.setSizes([600, 400])
        
        layout.addWidget(splitter)
    
    def create_details_panel(self):
        """Create details panel for selected symptom"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Details header
        header_label = QLabel("Symptom Details")
        header_label.setProperty("class", "subtitle")
        layout.addWidget(header_label)
        
        # Scroll area for details
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        details_content = QWidget()
        self.details_layout = QVBoxLayout(details_content)
        
        # Placeholder content
        placeholder = QLabel("Select a symptom from the tree to view details")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: gray; font-style: italic;")
        self.details_layout.addWidget(placeholder)
        
        scroll.setWidget(details_content)
        layout.addWidget(scroll)
        
        return widget
    
    def build_symptom_tree(self):
        """Build the DSM-5 symptom tree structure"""
        for category, disorders in DSM5_HIERARCHY.items():
            category_item = QTreeWidgetItem([category])
            category_item.setExpanded(False)
            category_item.setFlags(category_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            
            # Style category items
            font = category_item.font(0)
            font.setBold(True)
            category_item.setFont(0, font)
            
            for disorder, symptoms in disorders.items():
                disorder_item = QTreeWidgetItem([disorder])
                disorder_item.setExpanded(False)
                disorder_item.setFlags(disorder_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                
                # Add symptom groups
                for symptom_group, symptom_list in symptoms.items():
                    if isinstance(symptom_list, list):
                        group_item = QTreeWidgetItem([symptom_group.replace('_', ' ').title()])
                        group_item.setExpanded(False)
                        
                        for symptom in symptom_list:
                            symptom_item = QTreeWidgetItem([symptom['name']])
                            symptom_code = symptom.get('code', '')
                            
                            # Store symptom data
                            if symptom_code not in self.symptom_data:
                                self.symptom_data[symptom_code] = {
                                    'name': symptom['name'],
                                    'code': symptom_code,
                                    'category': category,
                                    'disorder': disorder,
                                    'group': symptom_group,
                                    'required': symptom.get('required', False),
                                    'present': False,
                                    'severity': 'None',
                                    'duration': '',
                                    'onset_date': '',
                                    'frequency': '',
                                    'triggers': '',
                                    'impact_functional': 0,
                                    'impact_occupational': 0,
                                    'impact_social': 0,
                                    'notes': ''
                                }
                            
                            # Add presence checkbox
                            checkbox = QCheckBox()
                            checkbox.toggled.connect(
                                lambda checked, code=symptom_code: self.on_symptom_present_changed(code, checked)
                            )
                            self.symptom_tree.setItemWidget(symptom_item, 1, checkbox)
                            
                            # Add severity dropdown
                            severity_combo = QComboBox()
                            severity_combo.addItems(["None", "Mild", "Moderate", "Severe"])
                            severity_combo.currentTextChanged.connect(
                                lambda text, code=symptom_code: self.on_severity_changed(code, text)
                            )
                            self.symptom_tree.setItemWidget(symptom_item, 2, severity_combo)
                            
                            # Add duration input
                            duration_input = QLineEdit()
                            duration_input.setPlaceholderText("e.g., 2 weeks")
                            duration_input.textChanged.connect(
                                lambda text, code=symptom_code: self.on_duration_changed(code, text)
                            )
                            self.symptom_tree.setItemWidget(symptom_item, 3, duration_input)
                            
                            # Add details button
                            details_btn = QPushButton("Details")
                            details_btn.clicked.connect(
                                lambda checked, code=symptom_code: self.show_symptom_details(code)
                            )
                            self.symptom_tree.setItemWidget(symptom_item, 4, details_btn)
                            
                            # Mark required symptoms
                            if symptom.get('required', False):
                                font = symptom_item.font(0)
                                font.setBold(True)
                                symptom_item.setFont(0, font)
                                symptom_item.setToolTip(0, "Required for diagnosis")
                            
                            group_item.addChild(symptom_item)
                        
                        disorder_item.addChild(group_item)
                
                category_item.addChild(disorder_item)
            
            self.symptom_tree.addTopLevelItem(category_item)
        
        # Connect tree selection
        self.symptom_tree.itemClicked.connect(self.on_tree_item_clicked)
    
    def on_symptom_present_changed(self, symptom_code, checked):
        """Handle symptom presence change"""
        if symptom_code in self.symptom_data:
            self.symptom_data[symptom_code]['present'] = checked
            self.data_changed.emit()
    
    def on_severity_changed(self, symptom_code, severity):
        """Handle severity change"""
        if symptom_code in self.symptom_data:
            self.symptom_data[symptom_code]['severity'] = severity
            self.data_changed.emit()
    
    def on_duration_changed(self, symptom_code, duration):
        """Handle duration change"""
        if symptom_code in self.symptom_data:
            self.symptom_data[symptom_code]['duration'] = duration
            self.data_changed.emit()
    
    def on_tree_item_clicked(self, item, column):
        """Handle tree item selection"""
        # Find the symptom code for this item
        symptom_code = None
        for code, data in self.symptom_data.items():
            if data['name'] == item.text(0):
                symptom_code = code
                break
        
        if symptom_code:
            self.show_symptom_details_panel(symptom_code)
    
    def show_symptom_details_panel(self, symptom_code):
        """Show symptom details in the right panel"""
        # Clear existing content
        for i in reversed(range(self.details_layout.count())):
            self.details_layout.itemAt(i).widget().setParent(None)
        
        symptom = self.symptom_data[symptom_code]
        
        # Create details form
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        
        # Symptom info
        info_group = QGroupBox("Symptom Information")
        info_layout = QFormLayout(info_group)
        
        name_label = QLabel(symptom['name'])
        name_label.setWordWrap(True)
        info_layout.addRow("Symptom:", name_label)
        
        category_label = QLabel(f"{symptom['category']} > {symptom['disorder']}")
        info_layout.addRow("Category:", category_label)
        
        if symptom['required']:
            required_label = QLabel("Yes")
            required_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            required_label = QLabel("No")
        info_layout.addRow("Required:", required_label)
        
        form_layout.addRow(info_group)
        
        # Clinical details
        clinical_group = QGroupBox("Clinical Assessment")
        clinical_layout = QFormLayout(clinical_group)
        
        # Onset date
        onset_input = QLineEdit(symptom.get('onset_date', ''))
        onset_input.setPlaceholderText("e.g., January 2024")
        onset_input.textChanged.connect(
            lambda text: self.update_symptom_field(symptom_code, 'onset_date', text)
        )
        clinical_layout.addRow("Onset Date:", onset_input)
        
        # Frequency
        frequency_combo = QComboBox()
        frequency_combo.addItems([
            "", "Daily", "Several times per day", "Weekly", "Several times per week",
            "Monthly", "Occasionally", "During episodes only"
        ])
        frequency_combo.setCurrentText(symptom.get('frequency', ''))
        frequency_combo.currentTextChanged.connect(
            lambda text: self.update_symptom_field(symptom_code, 'frequency', text)
        )
        clinical_layout.addRow("Frequency:", frequency_combo)
        
        # Triggers
        triggers_input = QTextEdit(symptom.get('triggers', ''))
        triggers_input.setMaximumHeight(60)
        triggers_input.setPlaceholderText("Environmental or situational triggers...")
        triggers_input.textChanged.connect(
            lambda: self.update_symptom_field(symptom_code, 'triggers', triggers_input.toPlainText())
        )
        clinical_layout.addRow("Triggers:", triggers_input)
        
        form_layout.addRow(clinical_group)
        
        # Functional impact
        impact_group = QGroupBox("Functional Impact (0-10 scale)")
        impact_layout = QFormLayout(impact_group)
        
        # Create impact sliders/spinboxes
        from PyQt6.QtWidgets import QSpinBox
        
        functional_spin = QSpinBox()
        functional_spin.setRange(0, 10)
        functional_spin.setValue(symptom.get('impact_functional', 0))
        functional_spin.valueChanged.connect(
            lambda value: self.update_symptom_field(symptom_code, 'impact_functional', value)
        )
        impact_layout.addRow("Daily Functioning:", functional_spin)
        
        occupational_spin = QSpinBox()
        occupational_spin.setRange(0, 10)
        occupational_spin.setValue(symptom.get('impact_occupational', 0))
        occupational_spin.valueChanged.connect(
            lambda value: self.update_symptom_field(symptom_code, 'impact_occupational', value)
        )
        impact_layout.addRow("Work/School:", occupational_spin)
        
        social_spin = QSpinBox()
        social_spin.setRange(0, 10)
        social_spin.setValue(symptom.get('impact_social', 0))
        social_spin.valueChanged.connect(
            lambda value: self.update_symptom_field(symptom_code, 'impact_social', value)
        )
        impact_layout.addRow("Social Relationships:", social_spin)
        
        form_layout.addRow(impact_group)
        
        # Clinical notes
        notes_group = QGroupBox("Clinical Notes")
        notes_layout = QVBoxLayout(notes_group)
        
        notes_text = QTextEdit(symptom.get('notes', ''))
        notes_text.setMaximumHeight(100)
        notes_text.setPlaceholderText("Additional clinical observations, patient descriptions, etc.")
        notes_text.textChanged.connect(
            lambda: self.update_symptom_field(symptom_code, 'notes', notes_text.toPlainText())
        )
        notes_layout.addWidget(notes_text)
        
        form_layout.addRow(notes_group)
        
        self.details_layout.addWidget(form_widget)
        self.details_layout.addStretch()
    
    def update_symptom_field(self, symptom_code, field, value):
        """Update a specific field in symptom data"""
        if symptom_code in self.symptom_data:
            self.symptom_data[symptom_code][field] = value
            self.data_changed.emit()
    
    def show_symptom_details(self, symptom_code):
        """Show detailed symptom dialog"""
        dialog = SymptomDetailsDialog(symptom_code, self.symptom_data[symptom_code], self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.symptom_data[symptom_code].update(dialog.get_data())
            self.data_changed.emit()
    
    def get_data(self):
        """Get all symptom assessment data"""
        return self.symptom_data
    
    def set_data(self, data):
        """Set symptom assessment data"""
        self.symptom_data.update(data)
        # TODO: Update UI widgets to reflect the data
    
    def clear_form(self):
        """Clear all symptom data"""
        for code in self.symptom_data:
            self.symptom_data[code].update({
                'present': False,
                'severity': 'None',
                'duration': '',
                'onset_date': '',
                'frequency': '',
                'triggers': '',
                'impact_functional': 0,
                'impact_occupational': 0,
                'impact_social': 0,
                'notes': ''
            })
        # TODO: Update UI widgets to reflect cleared data

class SymptomDetailsDialog(QDialog):
    """Dialog for detailed symptom information"""
    
    def __init__(self, symptom_code, symptom_data, parent=None):
        super().__init__(parent)
        self.symptom_code = symptom_code
        self.symptom_data = symptom_data.copy()
        self.setup_ui()
    
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle(f"Symptom Details: {self.symptom_data['name']}")
        self.setModal(True)
        self.resize(500, 600)
        
        layout = QVBoxLayout(self)
        
        # Main content in scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content_widget = QWidget()
        content_layout = QFormLayout(content_widget)
        
        # All the detailed form fields would go here
        # Similar to the panel version but in a dialog format
        
        # For now, just a placeholder
        placeholder = QLabel("Detailed symptom assessment form would go here")
        content_layout.addRow(placeholder)
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def get_data(self):
        """Get dialog data"""
        return self.symptom_data