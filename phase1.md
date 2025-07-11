# 🚀 **Phase 1 Implementation Guide - Psychiatric Records App**

## 📋 **Phase 1 Core Components**

### 1. Modern UI Framework with Theming
### 2. Comprehensive Patient Demographics
### 3. DSM-5 TR Hierarchical Symptom Assessment
### 4. Basic Medication Tracking
### 5. Lab Results Entry

---

## 🎨 **1. Modern UI Framework Setup**

### **Required Libraries**
```python
# Core UI
PyQt6>=6.6.0
qtawesome>=1.2.3
qdarktheme>=2.1.0

# Database
SQLAlchemy>=2.0.0
sqlcipher3>=0.5.0

# Data Processing
pandas>=2.0.0
pydantic>=2.0.0
python-dateutil>=2.8.0
```

### **UI Theme System**
```python
# themes/theme_manager.py
class ThemeManager:
    def __init__(self):
        self.current_theme = "dark"
        self.themes = {
            "dark": {
                "primary": "#2196F3",
                "secondary": "#FF9800",
                "background": "#121212",
                "surface": "#1E1E1E",
                "text": "#FFFFFF",
                "error": "#F44336"
            },
            "light": {
                "primary": "#1976D2",
                "secondary": "#F57C00",
                "background": "#FAFAFA",
                "surface": "#FFFFFF",
                "text": "#212121",
                "error": "#D32F2F"
            }
        }
```

### **Modern Widget Components**
```python
# ui/components/modern_widgets.py
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import qtawesome as qta

class ModernButton(QPushButton):
    """
    Material Design button with hover effects and animations
    Usage: button = ModernButton("Save", button_type="primary")
    """
    def __init__(self, text="", button_type="primary", icon=None, parent=None):
        super().__init__(text, parent)
        self.button_type = button_type
        self.setup_style()
        self.setup_animations()
        if icon:
            self.setIcon(qta.icon(icon, color='white' if button_type == 'primary' else '#666'))
    
    def setup_style(self):
        styles = {
            "primary": """
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: 500;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                    transform: translateY(-1px);
                }
                QPushButton:pressed {
                    background-color: #1565C0;
                }
                QPushButton:disabled {
                    background-color: #BDBDBD;
                    color: #9E9E9E;
                }
            """,
            "secondary": """
                QPushButton {
                    background-color: transparent;
                    color: #2196F3;
                    border: 2px solid #2196F3;
                    border-radius: 8px;
                    padding: 10px 22px;
                    font-size: 14px;
                    font-weight: 500;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #E3F2FD;
                    border-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #BBDEFB;
                }
            """,
            "danger": """
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: 500;
                    min-width: 120px;
                }
                QPushButton:hover {
                    background-color: #D32F2F;
                }
            """,
            "icon": """
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 20px;
                    padding: 10px;
                    min-width: 40px;
                    max-width: 40px;
                    min-height: 40px;
                    max-height: 40px;
                }
                QPushButton:hover {
                    background-color: rgba(33, 150, 243, 0.1);
                }
            """
        }
        self.setStyleSheet(styles.get(self.button_type, styles["primary"]))
    
    def setup_animations(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

class ModernLineEdit(QLineEdit):
    """
    Material Design text input with floating labels and validation
    Usage: input_field = ModernLineEdit("Patient Name", required=True)
    """
    def __init__(self, placeholder="", required=False, validation_pattern=None, parent=None):
        super().__init__(parent)
        self.placeholder_text = placeholder
        self.required = required
        self.validation_pattern = validation_pattern
        self.is_valid = True
        self.setup_style()
        self.setup_validation()
        self.textChanged.connect(self.on_text_changed)
    
    def setup_style(self):
        self.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                padding: 12px 0px 8px 0px;
                font-size: 16px;
                color: #212121;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #2196F3;
            }
            QLineEdit[invalid="true"] {
                border-bottom: 2px solid #F44336;
            }
        """)
        self.setPlaceholderText(self.placeholder_text)
    
    def setup_validation(self):
        if self.validation_pattern:
            self.validator = QRegularExpressionValidator(
                QRegularExpression(self.validation_pattern)
            )
            self.setValidator(self.validator)
    
    def on_text_changed(self):
        self.validate_input()
    
    def validate_input(self):
        text = self.text().strip()
        self.is_valid = True
        
        if self.required and not text:
            self.is_valid = False
        elif self.validation_pattern and text:
            regex = QRegularExpression(self.validation_pattern)
            if not regex.match(text).hasMatch():
                self.is_valid = False
        
        self.setProperty("invalid", not self.is_valid)
        self.style().unpolish(self)
        self.style().polish(self)
        
        return self.is_valid

class ModernComboBox(QComboBox):
    """
    Searchable dropdown with icons and modern styling
    Usage: combo = ModernComboBox(["Option 1", "Option 2"], searchable=True)
    """
    def __init__(self, items=None, searchable=False, icons=None, parent=None):
        super().__init__(parent)
        self.searchable = searchable
        self.setup_style()
        if items:
            self.add_items(items, icons)
        if searchable:
            self.setEditable(True)
            self.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
            self.setup_search()
    
    def setup_style(self):
        self.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #212121;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #2196F3;
            }
            QComboBox:hover {
                border-color: #BDBDBD;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
                width: 0px;
                height: 0px;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 8px solid #757575;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 4px;
                selection-background-color: #E3F2FD;
                selection-color: #1976D2;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border: none;
                border-radius: 4px;
                margin: 1px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #F5F5F5;
            }
        """)
    
    def add_items(self, items, icons=None):
        for i, item in enumerate(items):
            if icons and i < len(icons):
                self.addItem(qta.icon(icons[i]), item)
            else:
                self.addItem(item)
    
    def setup_search(self):
        completer = QCompleter()
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.setCompleter(completer)

class ModernCheckBox(QCheckBox):
    """
    Material Design checkbox with smooth animations
    Usage: checkbox = ModernCheckBox("Enable notifications", checked=True)
    """
    def __init__(self, text="", checked=False, parent=None):
        super().__init__(text, parent)
        self.setChecked(checked)
        self.setup_style()
        self.setup_animations()
    
    def setup_style(self):
        self.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #212121;
                spacing: 12px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #757575;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox::indicator:hover {
                border-color: #2196F3;
                background-color: #E3F2FD;
            }
            QCheckBox::indicator:checked {
                background-color: #2196F3;
                border-color: #2196F3;
                image: url(:/icons/checkmark.png);
            }
            QCheckBox::indicator:checked:hover {
                background-color: #1976D2;
            }
            QCheckBox::indicator:disabled {
                border-color: #BDBDBD;
                background-color: #F5F5F5;
            }
        """)
    
    def setup_animations(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)

class ModernCard(QFrame):
    """
    Material Design card container with elevation shadow
    Usage: card = ModernCard(elevation=2)
    """
    def __init__(self, elevation=1, parent=None):
        super().__init__(parent)
        self.elevation = elevation
        self.setup_style()
    
    def setup_style(self):
        shadow_styles = {
            1: "box-shadow: 0 2px 4px rgba(0,0,0,0.1);",
            2: "box-shadow: 0 4px 8px rgba(0,0,0,0.12);",
            3: "box-shadow: 0 8px 16px rgba(0,0,0,0.15);",
            4: "box-shadow: 0 12px 24px rgba(0,0,0,0.18);"
        }
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
                {shadow_styles.get(self.elevation, shadow_styles[1])}
                padding: 16px;
            }}
        """)
        
        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(self.elevation * 4)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, self.elevation * 2)
        self.setGraphicsEffect(shadow)

class ModernSlider(QSlider):
    """
    Material Design slider with value display
    Usage: slider = ModernSlider(0, 100, 50, orientation=Qt.Orientation.Horizontal)
    """
    def __init__(self, min_val=0, max_val=100, current_val=50, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.setMinimum(min_val)
        self.setMaximum(max_val)
        self.setValue(current_val)
        self.setup_style()
        self.valueChanged.connect(self.on_value_changed)
    
    def setup_style(self):
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #E0E0E0;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                border: 2px solid #2196F3;
                width: 20px;
                height: 20px;
                margin: -7px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: #1976D2;
                border-color: #1976D2;
            }
            QSlider::sub-page:horizontal {
                background: #2196F3;
                border-radius: 3px;
            }
        """)
    
    def on_value_changed(self, value):
        # Show tooltip with current value
        QToolTip.showText(self.mapToGlobal(QPoint(0, 0)), str(value))

class ModernProgressBar(QProgressBar):
    """
    Material Design progress bar with smooth animations
    Usage: progress = ModernProgressBar(value=65, show_text=True)
    """
    def __init__(self, value=0, show_text=False, parent=None):
        super().__init__(parent)
        self.setValue(value)
        self.setTextVisible(show_text)
        self.setup_style()
        self.setup_animations()
    
    def setup_style(self):
        self.setStyleSheet("""
            QProgressBar {
                background-color: #E0E0E0;
                border-radius: 4px;
                height: 8px;
                text-align: center;
                font-size: 12px;
                color: #212121;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 4px;
            }
        """)
    
    def setup_animations(self):
        self.animation = QPropertyAnimation(self, b"value")
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def animate_to_value(self, target_value):
        self.animation.setStartValue(self.value())
        self.animation.setEndValue(target_value)
        self.animation.start()

class ModernTabWidget(QTabWidget):
    """
    Material Design tab widget with smooth transitions
    Usage: tabs = ModernTabWidget()
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_style()
    
    def setup_style(self):
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                background-color: white;
                padding: 16px;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: transparent;
                padding: 12px 24px;
                margin: 0 2px;
                border-bottom: 3px solid transparent;
                color: #757575;
                font-size: 14px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                color: #2196F3;
                border-bottom-color: #2196F3;
            }
            QTabBar::tab:hover {
                color: #1976D2;
                background-color: #E3F2FD;
            }
        """)

class ModernSearchBox(QLineEdit):
    """
    Search input with icon and clear button
    Usage: search = ModernSearchBox(placeholder="Search patients...")
    """
    def __init__(self, placeholder="Search...", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setup_style()
        self.setup_actions()
    
    def setup_style(self):
        self.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5;
                border: 2px solid transparent;
                border-radius: 20px;
                padding: 8px 40px 8px 40px;
                font-size: 14px;
                color: #212121;
            }
            QLineEdit:focus {
                background-color: white;
                border-color: #2196F3;
            }
        """)
    
    def setup_actions(self):
        # Search icon
        search_action = QAction(qta.icon('fa.search', color='#757575'), "", self)
        self.addAction(search_action, QLineEdit.ActionPosition.LeadingPosition)
        
        # Clear button
        clear_action = QAction(qta.icon('fa.times', color='#757575'), "", self)
        clear_action.triggered.connect(self.clear)
        self.addAction(clear_action, QLineEdit.ActionPosition.TrailingPosition)
        
        # Show/hide clear button based on text
        self.textChanged.connect(self.toggle_clear_button)
    
    def toggle_clear_button(self, text):
        actions = self.actions()
        if len(actions) > 1:
            actions[1].setVisible(bool(text))
```

### **Widget Usage Examples**
```python
# Example usage in main application
class PatientForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create modern card container
        card = ModernCard(elevation=2)
        card_layout = QVBoxLayout(card)
        
        # Modern input fields with validation
        self.name_input = ModernLineEdit(
            placeholder="Full Name",
            required=True,
            validation_pattern=r"^[A-Za-z\s]{2,50}$"
        )
        
        self.email_input = ModernLineEdit(
            placeholder="Email Address",
            validation_pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        )
        
        # Modern dropdown with search
        self.gender_combo = ModernComboBox(
            items=["Male", "Female", "Non-binary", "Other", "Prefer not to say"],
            searchable=True,
            icons=["fa.male", "fa.female", "fa.user", "fa.question", "fa.ban"]
        )
        
        # Modern checkbox
        self.consent_checkbox = ModernCheckBox("I consent to treatment")
        
        # Modern buttons
        button_layout = QHBoxLayout()
        cancel_btn = ModernButton("Cancel", button_type="secondary")
        save_btn = ModernButton("Save Patient", button_type="primary", icon="fa.save")
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        
        # Add to card
        card_layout.addWidget(self.name_input)
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(self.gender_combo)
        card_layout.addWidget(self.consent_checkbox)
        card_layout.addLayout(button_layout)
        
        layout.addWidget(card)
        self.setLayout(layout)
```

### **Performance Optimizations**
```python
# ui/components/optimized_widgets.py
class OptimizedTableWidget(QTableWidget):
    """
    High-performance table widget with virtual scrolling and lazy loading
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        
        # Enable virtual scrolling for large datasets
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        
        # Custom styling
        self.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                gridline-color: #F5F5F5;
                selection-background-color: #E3F2FD;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                border: none;
                padding: 12px 8px;
                font-weight: 600;
                color: #424242;
            }
        """)

class LazyLoadingListWidget(QListWidget):
    """
    List widget with lazy loading for large datasets
    """
    def __init__(self, data_loader_func, parent=None):
        super().__init__(parent)
        self.data_loader = data_loader_func
        self.current_page = 0
        self.page_size = 50
        self.loading = False
        
        # Connect scroll event
        self.verticalScrollBar().valueChanged.connect(self.on_scroll)
        
        # Initial load
        self.load_more_items()
    
    def load_more_items(self):
        if self.loading:
            return
        
        self.loading = True
        items = self.data_loader(self.current_page, self.page_size)
        
        for item_data in items:
            item = QListWidgetItem(item_data['text'])
            item.setData(Qt.ItemDataRole.UserRole, item_data)
            self.addItem(item)
        
        self.current_page += 1
        self.loading = False
    
    def on_scroll(self, value):
        if value == self.verticalScrollBar().maximum():
            self.load_more_items()
```

---

## 👤 **2. Comprehensive Patient Demographics**

### **Patient Model Structure**
```python
# models/patient.py
class Patient(Base):
    __tablename__ = 'patients'
    
    # Basic Identity
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    preferred_name = Column(String(100))
    date_of_birth = Column(Date, nullable=False)
    age = Column(Integer)  # Auto-calculated
    gender = Column(String(50))
    biological_sex = Column(String(20))
    sexual_orientation = Column(String(50))
    gender_identity = Column(String(100))
    
    # Contact Information
    phone_primary = Column(String(20))
    phone_secondary = Column(String(20))
    email = Column(String(255))
    address_street = Column(String(255))
    address_city = Column(String(100))
    address_state = Column(String(50))
    address_zip = Column(String(20))
    address_country = Column(String(100), default="USA")
    
    # Emergency Contact
    emergency_name = Column(String(200))
    emergency_relationship = Column(String(100))
    emergency_phone = Column(String(20))
    emergency_email = Column(String(255))
    
    # Demographics
    race = Column(String(100))
    ethnicity = Column(String(100))
    primary_language = Column(String(50), default="English")
    secondary_languages = Column(Text)  # JSON array
    interpreter_needed = Column(Boolean, default=False)
    
    # Social History
    marital_status = Column(String(50))
    children_count = Column(Integer)
    living_situation = Column(String(100))
    housing_stability = Column(String(100))
    
    # Education
    education_level = Column(String(100))
    education_details = Column(Text)
    current_student = Column(Boolean, default=False)
    
    # Employment
    employment_status = Column(String(100))
    job_title = Column(String(200))
    employer = Column(String(200))
    work_schedule = Column(String(100))
    income_range = Column(String(50))
    financial_stress = Column(String(100))
    
    # Legal
    legal_issues = Column(Text)
    legal_guardian = Column(String(200))
    
    # Insurance & Medical
    insurance_primary = Column(String(200))
    insurance_secondary = Column(String(200))
    insurance_id = Column(String(100))
    primary_care_physician = Column(String(200))
    referred_by = Column(String(200))
    
    # System Fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    is_active = Column(Boolean, default=True)
```

### **Demographics UI Component**
```python
# ui/demographics_form.py
class DemographicsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create tabbed interface for demographics
        tab_widget = QTabWidget()
        
        # Tab 1: Basic Information
        basic_tab = self.create_basic_info_tab()
        tab_widget.addTab(basic_tab, "Basic Info")
        
        # Tab 2: Contact & Emergency
        contact_tab = self.create_contact_tab()
        tab_widget.addTab(contact_tab, "Contact")
        
        # Tab 3: Social & Demographics
        social_tab = self.create_social_tab()
        tab_widget.addTab(social_tab, "Social")
        
        # Tab 4: Education & Employment
        education_tab = self.create_education_employment_tab()
        tab_widget.addTab(education_tab, "Education/Work")
        
        # Tab 5: Insurance & Medical
        insurance_tab = self.create_insurance_tab()
        tab_widget.addTab(insurance_tab, "Insurance")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)
```

---

## 🧠 **3. DSM-5 TR Hierarchical Symptom Assessment**

### **Symptom Hierarchy Structure**
```python
# data/dsm5_hierarchy.py
DSM5_HIERARCHY = {
    "Mood Disorders": {
        "Major Depressive Disorder": {
            "core_symptoms": [
                {"name": "Depressed mood", "code": "A1", "required": True},
                {"name": "Anhedonia", "code": "A2", "required": True},
            ],
            "additional_symptoms": [
                {"name": "Insomnia or hypersomnia", "code": "A3"},
                {"name": "Psychomotor agitation or retardation", "code": "A4"},
                {"name": "Fatigue or loss of energy", "code": "A5"},
                {"name": "Feelings of worthlessness or guilt", "code": "A6"},
                {"name": "Diminished concentration", "code": "A7"},
                {"name": "Recurrent thoughts of death", "code": "A8"},
                {"name": "Significant weight loss or gain", "code": "A9"},
            ],
            "severity_specifiers": ["Mild", "Moderate", "Severe"],
            "episode_specifiers": ["Single Episode", "Recurrent"],
            "features": ["With anxious distress", "With melancholic features", "With atypical features"]
        },
        "Bipolar I Disorder": {
            "manic_episode": [
                {"name": "Elevated, expansive, or irritable mood", "code": "B1", "required": True},
                {"name": "Increased goal-directed activity", "code": "B2", "required": True},
            ],
            "manic_symptoms": [
                {"name": "Inflated self-esteem or grandiosity", "code": "B3"},
                {"name": "Decreased need for sleep", "code": "B4"},
                {"name": "More talkative than usual", "code": "B5"},
                {"name": "Flight of ideas or racing thoughts", "code": "B6"},
                {"name": "Distractibility", "code": "B7"},
                {"name": "Increase in risky behavior", "code": "B8"},
            ]
        }
    },
    "Anxiety Disorders": {
        "Generalized Anxiety Disorder": {
            "core_symptoms": [
                {"name": "Excessive anxiety and worry", "code": "C1", "required": True},
                {"name": "Difficult to control worry", "code": "C2", "required": True},
            ],
            "associated_symptoms": [
                {"name": "Restlessness or feeling on edge", "code": "C3"},
                {"name": "Being easily fatigued", "code": "C4"},
                {"name": "Difficulty concentrating", "code": "C5"},
                {"name": "Irritability", "code": "C6"},
                {"name": "Muscle tension", "code": "C7"},
                {"name": "Sleep disturbance", "code": "C8"},
            ]
        },
        "Panic Disorder": {
            "panic_attacks": [
                {"name": "Palpitations or pounding heart", "code": "D1"},
                {"name": "Sweating", "code": "D2"},
                {"name": "Trembling or shaking", "code": "D3"},
                {"name": "Shortness of breath", "code": "D4"},
                {"name": "Feelings of choking", "code": "D5"},
                {"name": "Chest pain or discomfort", "code": "D6"},
                {"name": "Nausea or abdominal distress", "code": "D7"},
                {"name": "Dizziness or lightheadedness", "code": "D8"},
                {"name": "Chills or heat sensations", "code": "D9"},
                {"name": "Numbness or tingling", "code": "D10"},
                {"name": "Derealization or depersonalization", "code": "D11"},
                {"name": "Fear of losing control", "code": "D12"},
                {"name": "Fear of dying", "code": "D13"},
            ]
        }
    },
    "Trauma and Stressor-Related Disorders": {
        "PTSD": {
            "criterion_a": [
                {"name": "Exposure to actual or threatened death, serious injury, or sexual violence", "code": "E1", "required": True}
            ],
            "criterion_b": [
                {"name": "Recurrent, involuntary intrusive memories", "code": "E2"},
                {"name": "Recurrent distressing dreams", "code": "E3"},
                {"name": "Dissociative reactions (flashbacks)", "code": "E4"},
                {"name": "Intense psychological distress", "code": "E5"},
                {"name": "Marked physiological reactions", "code": "E6"},
            ]
        }
    }
}
```

### **Symptom Assessment UI**
```python
# ui/symptom_assessment.py
class SymptomAssessmentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.symptom_data = {}
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create hierarchical tree view
        self.symptom_tree = QTreeWidget()
        self.symptom_tree.setHeaderLabels(["Symptom", "Present", "Severity", "Duration", "Comments"])
        
        # Build DSM-5 tree structure
        self.build_symptom_tree()
        
        layout.addWidget(self.symptom_tree)
        self.setLayout(layout)
    
    def build_symptom_tree(self):
        for category, disorders in DSM5_HIERARCHY.items():
            category_item = QTreeWidgetItem([category])
            category_item.setExpanded(False)
            
            for disorder, symptoms in disorders.items():
                disorder_item = QTreeWidgetItem([disorder])
                disorder_item.setExpanded(False)
                
                # Add symptom items
                for symptom_group, symptom_list in symptoms.items():
                    if isinstance(symptom_list, list):
                        group_item = QTreeWidgetItem([symptom_group.replace('_', ' ').title()])
                        
                        for symptom in symptom_list:
                            symptom_item = QTreeWidgetItem([symptom['name']])
                            
                            # Add checkbox for presence
                            checkbox = QCheckBox()
                            self.symptom_tree.setItemWidget(symptom_item, 1, checkbox)
                            
                            # Add severity dropdown
                            severity_combo = QComboBox()
                            severity_combo.addItems(["None", "Mild", "Moderate", "Severe"])
                            self.symptom_tree.setItemWidget(symptom_item, 2, severity_combo)
                            
                            # Add duration input
                            duration_input = QLineEdit()
                            duration_input.setPlaceholderText("e.g., 2 weeks")
                            self.symptom_tree.setItemWidget(symptom_item, 3, duration_input)
                            
                            # Add comments button
                            comments_btn = QPushButton("Comments")
                            comments_btn.clicked.connect(lambda: self.open_comments_dialog(symptom['code']))
                            self.symptom_tree.setItemWidget(symptom_item, 4, comments_btn)
                            
                            group_item.addChild(symptom_item)
                        
                        disorder_item.addChild(group_item)
                
                category_item.addChild(disorder_item)
            
            self.symptom_tree.addTopLevelItem(category_item)
    
    def open_comments_dialog(self, symptom_code):
        dialog = QDialog(self)
        dialog.setWindowTitle("Additional Comments")
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        # Large text area for comments
        text_edit = QTextEdit()
        text_edit.setMinimumHeight(200)
        text_edit.setPlainText(self.symptom_data.get(symptom_code, {}).get('comments', ''))
        
        # Save button
        save_btn = QPushButton("Save Comments")
        save_btn.clicked.connect(lambda: self.save_comments(symptom_code, text_edit.toPlainText(), dialog))
        
        layout.addWidget(QLabel("Additional clinical notes and observations:"))
        layout.addWidget(text_edit)
        layout.addWidget(save_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def save_comments(self, symptom_code, comments, dialog):
        if symptom_code not in self.symptom_data:
            self.symptom_data[symptom_code] = {}
        self.symptom_data[symptom_code]['comments'] = comments
        dialog.accept()
```

---

## 💊 **4. Basic Medication Tracking**

### **Medication Model**
```python
# models/medication.py
class Medication(Base):
    __tablename__ = 'medications'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey('patients.id'), nullable=False)
    
    # Medication Details
    name = Column(String(200), nullable=False)
    generic_name = Column(String(200))
    brand_name = Column(String(200))
    medication_class = Column(String(100))
    
    # Dosage
    dose_amount = Column(Float)
    dose_unit = Column(String(50))  # mg, ml, etc.
    frequency = Column(String(100))  # BID, TID, etc.
    route = Column(String(50))  # PO, IM, etc.
    
    # Timing
    start_date = Column(Date)
    end_date = Column(Date)
    is_current = Column(Boolean, default=True)
    
    # Effectiveness & Side Effects
    effectiveness = Column(Integer)  # 0-100 scale
    side_effects = Column(Text)  # JSON array
    adherence = Column(Integer)  # 0-100 scale
    
    # Clinical Notes
    indication = Column(String(500))
    prescriber = Column(String(200))
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### **Medication UI Component**
```python
# ui/medication_manager.py
class MedicationManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Add medication button
        add_btn = QPushButton("Add Medication")
        add_btn.clicked.connect(self.add_medication)
        layout.addWidget(add_btn)
        
        # Medications table
        self.medications_table = QTableWidget()
        self.medications_table.setColumnCount(8)
        self.medications_table.setHorizontalHeaderLabels([
            "Name", "Dose", "Frequency", "Start Date", "Effectiveness", "Side Effects", "Current", "Actions"
        ])
        
        layout.addWidget(self.medications_table)
        self.setLayout(layout)
```

---

## 🔬 **5. Lab Results Entry**

### **Lab Result Model**
```python
# models/lab_result.py
class LabResult(Base):
    __tablename__ = 'lab_results'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String, ForeignKey('patients.id'), nullable=False)
    
    # Test Information
    test_name = Column(String(200), nullable=False)
    test_code = Column(String(50))
    test_category = Column(String(100))  # Chemistry, Hematology, etc.
    
    # Results
    value = Column(Float)
    unit = Column(String(50))
    reference_range = Column(String(100))
    is_abnormal = Column(Boolean, default=False)
    
    # Dates
    collection_date = Column(DateTime)
    result_date = Column(DateTime)
    
    # Clinical Context
    ordering_physician = Column(String(200))
    lab_facility = Column(String(200))
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

## 📁 **File Structure for Phase 1**

```
psychiatric_app/
├── main.py
├── config/
│   ├── __init__.py
│   ├── database.py
│   └── settings.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── patient.py
│   ├── medication.py
│   ├── lab_result.py
│   └── symptom_assessment.py
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── demographics_form.py
│   ├── symptom_assessment.py
│   ├── medication_manager.py
│   ├── lab_results.py
│   └── components/
│       ├── __init__.py
│       ├── modern_widgets.py
│       └── theme_manager.py
├── services/
│   ├── __init__.py
│   ├── database_service.py
│   ├── patient_service.py
│   └── validation_service.py
├── data/
│   ├── dsm5_hierarchy.py
│   ├── medications.json
│   └── lab_references.json
└── resources/
    ├── themes/
    │   ├── dark.qss
    │   └── light.qss
    └── icons/
```

---

## 🎯 **Phase 1 Success Criteria**

1. **Beautiful Modern UI** with dark/light theme switching
2. **Complete Demographics Collection** with all social determinants
3. **DSM-5 TR Hierarchical Symptom Assessment** with expandable tree view
4. **Basic Medication Tracking** with effectiveness rating
5. **Lab Results Entry** with reference ranges
6. **Local SQLCipher Database** with encryption
7. **Responsive Design** that works on different screen sizes
8. **Data Validation** with helpful error messages
9. **Auto-save Functionality** with visual indicators
10. **Smooth Performance** with lazy loading for large datasets

---

## 🚀 **Implementation Order**

### **Week 1: Foundation**
1. Set up project structure
2. Implement theme manager and modern widgets
3. Create database models and services
4. Build main window framework

### **Week 2: Demographics**
1. Complete demographics form with all tabs
2. Implement validation and auto-save
3. Add data persistence layer
4. Create patient search functionality

### **Week 3: Clinical Assessment**
1. Build DSM-5 TR hierarchical tree
2. Implement symptom tracking with comments
3. Add medication management interface
4. Create lab results entry system

### **Week 4: Polish & Testing**
1. Implement theme switching
2. Add keyboard shortcuts
3. Performance optimization
4. User testing and bug fixes

This Phase 1 implementation provides a solid foundation for a modern, efficient psychiatric records application with comprehensive data collection capabilities.