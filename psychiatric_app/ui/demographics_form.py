"""
Demographics form for comprehensive patient information collection
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QFormLayout,
    QLineEdit, QComboBox, QDateEdit, QSpinBox, QCheckBox, QTextEdit,
    QLabel, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

class DemographicsForm(QWidget):
    """Comprehensive demographics form with multiple tabs"""
    
    data_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_validation()
        self.connect_signals()
    
    def setup_ui(self):
        """Setup the main UI layout"""
        layout = QVBoxLayout(self)
        
        # Create tabbed interface for demographics
        self.tab_widget = QTabWidget()
        
        # Tab 1: Basic Information
        self.basic_tab = self.create_basic_info_tab()
        self.tab_widget.addTab(self.basic_tab, "Basic Info")
        
        # Tab 2: Contact & Emergency
        self.contact_tab = self.create_contact_tab()
        self.tab_widget.addTab(self.contact_tab, "Contact")
        
        # Tab 3: Demographics & Cultural
        self.demographics_tab = self.create_demographics_tab()
        self.tab_widget.addTab(self.demographics_tab, "Demographics")
        
        # Tab 4: Social History
        self.social_tab = self.create_social_tab()
        self.tab_widget.addTab(self.social_tab, "Social")
        
        # Tab 5: Education & Employment
        self.education_tab = self.create_education_employment_tab()
        self.tab_widget.addTab(self.education_tab, "Education/Work")
        
        # Tab 6: Insurance & Medical
        self.insurance_tab = self.create_insurance_tab()
        self.tab_widget.addTab(self.insurance_tab, "Insurance")
        
        layout.addWidget(self.tab_widget)
    
    def create_basic_info_tab(self):
        """Create basic information tab"""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        
        layout = QFormLayout(widget)
        
        # Name fields
        name_group = QGroupBox("Name Information")
        name_layout = QFormLayout(name_group)
        
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("Required")
        name_layout.addRow("First Name *:", self.first_name)
        
        self.middle_name = QLineEdit()
        name_layout.addRow("Middle Name:", self.middle_name)
        
        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Required")
        name_layout.addRow("Last Name *:", self.last_name)
        
        self.preferred_name = QLineEdit()
        name_layout.addRow("Preferred Name:", self.preferred_name)
        
        layout.addRow(name_group)
        
        # Birth and demographics
        birth_group = QGroupBox("Birth Information")
        birth_layout = QFormLayout(birth_group)
        
        self.date_of_birth = QDateEdit()
        self.date_of_birth.setDate(QDate.currentDate().addYears(-30))
        self.date_of_birth.setMaximumDate(QDate.currentDate())
        self.date_of_birth.setCalendarPopup(True)
        birth_layout.addRow("Date of Birth *:", self.date_of_birth)
        
        self.age = QSpinBox()
        self.age.setRange(0, 150)
        self.age.setReadOnly(True)
        birth_layout.addRow("Age:", self.age)
        
        layout.addRow(birth_group)
        
        # Gender and identity
        identity_group = QGroupBox("Gender & Identity")
        identity_layout = QFormLayout(identity_group)
        
        self.gender = QComboBox()
        self.gender.addItems([
            "", "Male", "Female", "Non-binary", "Transgender Male", 
            "Transgender Female", "Other", "Prefer not to say"
        ])
        identity_layout.addRow("Gender:", self.gender)
        
        self.biological_sex = QComboBox()
        self.biological_sex.addItems(["", "Male", "Female", "Intersex"])
        identity_layout.addRow("Biological Sex:", self.biological_sex)
        
        self.sexual_orientation = QComboBox()
        self.sexual_orientation.addItems([
            "", "Heterosexual", "Homosexual", "Bisexual", "Pansexual", 
            "Asexual", "Other", "Prefer not to say"
        ])
        identity_layout.addRow("Sexual Orientation:", self.sexual_orientation)
        
        self.gender_identity = QLineEdit()
        identity_layout.addRow("Gender Identity (details):", self.gender_identity)
        
        layout.addRow(identity_group)
        
        return scroll
    
    def create_contact_tab(self):
        """Create contact information tab"""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        
        layout = QFormLayout(widget)
        
        # Contact information
        contact_group = QGroupBox("Contact Information")
        contact_layout = QFormLayout(contact_group)
        
        self.phone_primary = QLineEdit()
        self.phone_primary.setPlaceholderText("(555) 123-4567")
        contact_layout.addRow("Primary Phone:", self.phone_primary)
        
        self.phone_secondary = QLineEdit()
        contact_layout.addRow("Secondary Phone:", self.phone_secondary)
        
        self.email = QLineEdit()
        self.email.setPlaceholderText("patient@email.com")
        contact_layout.addRow("Email:", self.email)
        
        layout.addRow(contact_group)
        
        # Address
        address_group = QGroupBox("Address")
        address_layout = QFormLayout(address_group)
        
        self.address_street = QLineEdit()
        address_layout.addRow("Street Address:", self.address_street)
        
        self.address_city = QLineEdit()
        address_layout.addRow("City:", self.address_city)
        
        self.address_state = QComboBox()
        self.address_state.addItems([
            "", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ])
        self.address_state.setEditable(True)
        address_layout.addRow("State:", self.address_state)
        
        self.address_zip = QLineEdit()
        self.address_zip.setPlaceholderText("12345 or 12345-6789")
        address_layout.addRow("ZIP Code:", self.address_zip)
        
        self.address_country = QLineEdit()
        self.address_country.setText("USA")
        address_layout.addRow("Country:", self.address_country)
        
        layout.addRow(address_group)
        
        # Emergency contact
        emergency_group = QGroupBox("Emergency Contact")
        emergency_layout = QFormLayout(emergency_group)
        
        self.emergency_name = QLineEdit()
        emergency_layout.addRow("Name:", self.emergency_name)
        
        self.emergency_relationship = QComboBox()
        self.emergency_relationship.addItems([
            "", "Spouse", "Parent", "Child", "Sibling", "Friend", 
            "Other Family", "Other"
        ])
        self.emergency_relationship.setEditable(True)
        emergency_layout.addRow("Relationship:", self.emergency_relationship)
        
        self.emergency_phone = QLineEdit()
        emergency_layout.addRow("Phone:", self.emergency_phone)
        
        self.emergency_email = QLineEdit()
        emergency_layout.addRow("Email:", self.emergency_email)
        
        layout.addRow(emergency_group)
        
        return scroll
    
    def create_demographics_tab(self):
        """Create demographics and cultural information tab"""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        
        layout = QFormLayout(widget)
        
        # Race and ethnicity
        race_group = QGroupBox("Race & Ethnicity")
        race_layout = QFormLayout(race_group)
        
        self.race = QComboBox()
        self.race.addItems([
            "", "American Indian or Alaska Native", "Asian", "Black or African American",
            "Native Hawaiian or Other Pacific Islander", "White", "Multiple races", "Other"
        ])
        self.race.setEditable(True)
        race_layout.addRow("Race:", self.race)
        
        self.ethnicity = QComboBox()
        self.ethnicity.addItems([
            "", "Hispanic or Latino", "Not Hispanic or Latino", "Unknown"
        ])
        race_layout.addRow("Ethnicity:", self.ethnicity)
        
        layout.addRow(race_group)
        
        # Language preferences
        language_group = QGroupBox("Language Preferences")
        language_layout = QFormLayout(language_group)
        
        self.primary_language = QComboBox()
        self.primary_language.addItems([
            "English", "Spanish", "Chinese", "French", "German", "Italian",
            "Portuguese", "Russian", "Arabic", "Japanese", "Korean", "Other"
        ])
        self.primary_language.setEditable(True)
        language_layout.addRow("Primary Language:", self.primary_language)
        
        self.secondary_languages = QLineEdit()
        self.secondary_languages.setPlaceholderText("Comma-separated list")
        language_layout.addRow("Other Languages:", self.secondary_languages)
        
        self.interpreter_needed = QCheckBox("Interpreter services needed")
        language_layout.addRow("", self.interpreter_needed)
        
        layout.addRow(language_group)
        
        return scroll
    
    def create_social_tab(self):
        """Create social history tab"""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        
        layout = QFormLayout(widget)
        
        # Marital and family
        family_group = QGroupBox("Family & Relationships")
        family_layout = QFormLayout(family_group)
        
        self.marital_status = QComboBox()
        self.marital_status.addItems([
            "", "Single", "Married", "Divorced", "Separated", "Widowed",
            "Domestic Partnership", "Other"
        ])
        family_layout.addRow("Marital Status:", self.marital_status)
        
        self.children_count = QSpinBox()
        self.children_count.setRange(0, 20)
        family_layout.addRow("Number of Children:", self.children_count)
        
        layout.addRow(family_group)
        
        # Living situation
        living_group = QGroupBox("Living Situation")
        living_layout = QFormLayout(living_group)
        
        self.living_situation = QComboBox()
        self.living_situation.addItems([
            "", "Lives alone", "Lives with family", "Lives with roommates",
            "Assisted living", "Group home", "Homeless", "Other"
        ])
        self.living_situation.setEditable(True)
        living_layout.addRow("Living Situation:", self.living_situation)
        
        self.housing_stability = QComboBox()
        self.housing_stability.addItems([
            "", "Stable", "Unstable", "Temporary", "At risk"
        ])
        living_layout.addRow("Housing Stability:", self.housing_stability)
        
        layout.addRow(living_group)
        
        # Legal issues
        legal_group = QGroupBox("Legal Information")
        legal_layout = QFormLayout(legal_group)
        
        self.legal_guardian = QLineEdit()
        legal_layout.addRow("Legal Guardian:", self.legal_guardian)
        
        self.legal_issues = QTextEdit()
        self.legal_issues.setMaximumHeight(80)
        self.legal_issues.setPlaceholderText("Any legal issues or restrictions...")
        legal_layout.addRow("Legal Issues:", self.legal_issues)
        
        layout.addRow(legal_group)
        
        return scroll
    
    def create_education_employment_tab(self):
        """Create education and employment tab"""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        
        layout = QFormLayout(widget)
        
        # Education
        education_group = QGroupBox("Education")
        education_layout = QFormLayout(education_group)
        
        self.education_level = QComboBox()
        self.education_level.addItems([
            "", "Some high school", "High school diploma/GED", 
            "Some college", "Associate degree", "Bachelor's degree",
            "Master's degree", "Doctoral degree", "Professional degree"
        ])
        education_layout.addRow("Education Level:", self.education_level)
        
        self.current_student = QCheckBox("Currently enrolled in school")
        education_layout.addRow("", self.current_student)
        
        self.education_details = QTextEdit()
        self.education_details.setMaximumHeight(60)
        self.education_details.setPlaceholderText("School name, field of study, etc.")
        education_layout.addRow("Education Details:", self.education_details)
        
        layout.addRow(education_group)
        
        # Employment
        employment_group = QGroupBox("Employment")
        employment_layout = QFormLayout(employment_group)
        
        self.employment_status = QComboBox()
        self.employment_status.addItems([
            "", "Employed full-time", "Employed part-time", "Self-employed",
            "Unemployed", "Retired", "Student", "Disabled", "Homemaker"
        ])
        employment_layout.addRow("Employment Status:", self.employment_status)
        
        self.job_title = QLineEdit()
        employment_layout.addRow("Job Title:", self.job_title)
        
        self.employer = QLineEdit()
        employment_layout.addRow("Employer:", self.employer)
        
        self.work_schedule = QComboBox()
        self.work_schedule.addItems([
            "", "Day shift", "Evening shift", "Night shift", "Rotating shifts",
            "Flexible", "Remote", "Other"
        ])
        employment_layout.addRow("Work Schedule:", self.work_schedule)
        
        self.income_range = QComboBox()
        self.income_range.addItems([
            "", "Under $25,000", "$25,000-$49,999", "$50,000-$74,999",
            "$75,000-$99,999", "$100,000-$149,999", "$150,000+", "Prefer not to say"
        ])
        employment_layout.addRow("Income Range:", self.income_range)
        
        self.financial_stress = QComboBox()
        self.financial_stress.addItems([
            "", "None", "Mild", "Moderate", "Severe"
        ])
        employment_layout.addRow("Financial Stress:", self.financial_stress)
        
        layout.addRow(employment_group)
        
        return scroll
    
    def create_insurance_tab(self):
        """Create insurance and medical information tab"""
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        
        layout = QFormLayout(widget)
        
        # Insurance
        insurance_group = QGroupBox("Insurance Information")
        insurance_layout = QFormLayout(insurance_group)
        
        self.insurance_primary = QLineEdit()
        insurance_layout.addRow("Primary Insurance:", self.insurance_primary)
        
        self.insurance_secondary = QLineEdit()
        insurance_layout.addRow("Secondary Insurance:", self.insurance_secondary)
        
        self.insurance_id = QLineEdit()
        insurance_layout.addRow("Insurance ID:", self.insurance_id)
        
        layout.addRow(insurance_group)
        
        # Medical information
        medical_group = QGroupBox("Medical Information")
        medical_layout = QFormLayout(medical_group)
        
        self.primary_care_physician = QLineEdit()
        medical_layout.addRow("Primary Care Physician:", self.primary_care_physician)
        
        self.referred_by = QLineEdit()
        medical_layout.addRow("Referred By:", self.referred_by)
        
        layout.addRow(medical_group)
        
        return scroll
    
    def setup_validation(self):
        """Setup input validation"""
        # Phone number validation
        phone_regex = QRegularExpression(r"^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$")
        phone_validator = QRegularExpressionValidator(phone_regex)
        self.phone_primary.setValidator(phone_validator)
        self.phone_secondary.setValidator(phone_validator)
        self.emergency_phone.setValidator(phone_validator)
        
        # Email validation
        email_regex = QRegularExpression(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        email_validator = QRegularExpressionValidator(email_regex)
        self.email.setValidator(email_validator)
        self.emergency_email.setValidator(email_validator)
        
        # ZIP code validation
        zip_regex = QRegularExpression(r"^\d{5}(-\d{4})?$")
        zip_validator = QRegularExpressionValidator(zip_regex)
        self.address_zip.setValidator(zip_validator)
        
        # Connect date of birth to age calculation
        self.date_of_birth.dateChanged.connect(self.calculate_age)
    
    def connect_signals(self):
        """Connect all signals to data_changed"""
        # Text fields
        for widget in self.findChildren(QLineEdit):
            widget.textChanged.connect(self.data_changed.emit)
        
        # Combo boxes
        for widget in self.findChildren(QComboBox):
            widget.currentTextChanged.connect(self.data_changed.emit)
        
        # Date edit
        for widget in self.findChildren(QDateEdit):
            widget.dateChanged.connect(self.data_changed.emit)
        
        # Spin boxes
        for widget in self.findChildren(QSpinBox):
            widget.valueChanged.connect(self.data_changed.emit)
        
        # Check boxes
        for widget in self.findChildren(QCheckBox):
            widget.toggled.connect(self.data_changed.emit)
        
        # Text edits
        for widget in self.findChildren(QTextEdit):
            widget.textChanged.connect(self.data_changed.emit)
    
    def calculate_age(self, birth_date):
        """Calculate age from birth date"""
        today = QDate.currentDate()
        age = today.year() - birth_date.year()
        if today.dayOfYear() < birth_date.dayOfYear():
            age -= 1
        self.age.setValue(age)
    
    def get_data(self):
        """Get all form data as dictionary"""
        return {
            # Basic info
            'first_name': self.first_name.text().strip(),
            'middle_name': self.middle_name.text().strip(),
            'last_name': self.last_name.text().strip(),
            'preferred_name': self.preferred_name.text().strip(),
            'date_of_birth': self.date_of_birth.date().toPython(),
            'age': self.age.value(),
            'gender': self.gender.currentText(),
            'biological_sex': self.biological_sex.currentText(),
            'sexual_orientation': self.sexual_orientation.currentText(),
            'gender_identity': self.gender_identity.text().strip(),
            
            # Contact
            'phone_primary': self.phone_primary.text().strip(),
            'phone_secondary': self.phone_secondary.text().strip(),
            'email': self.email.text().strip(),
            'address_street': self.address_street.text().strip(),
            'address_city': self.address_city.text().strip(),
            'address_state': self.address_state.currentText(),
            'address_zip': self.address_zip.text().strip(),
            'address_country': self.address_country.text().strip(),
            
            # Emergency contact
            'emergency_name': self.emergency_name.text().strip(),
            'emergency_relationship': self.emergency_relationship.currentText(),
            'emergency_phone': self.emergency_phone.text().strip(),
            'emergency_email': self.emergency_email.text().strip(),
            
            # Demographics
            'race': self.race.currentText(),
            'ethnicity': self.ethnicity.currentText(),
            'primary_language': self.primary_language.currentText(),
            'secondary_languages': self.secondary_languages.text().strip(),
            'interpreter_needed': self.interpreter_needed.isChecked(),
            
            # Social
            'marital_status': self.marital_status.currentText(),
            'children_count': self.children_count.value(),
            'living_situation': self.living_situation.currentText(),
            'housing_stability': self.housing_stability.currentText(),
            'legal_guardian': self.legal_guardian.text().strip(),
            'legal_issues': self.legal_issues.toPlainText().strip(),
            
            # Education/Employment
            'education_level': self.education_level.currentText(),
            'current_student': self.current_student.isChecked(),
            'education_details': self.education_details.toPlainText().strip(),
            'employment_status': self.employment_status.currentText(),
            'job_title': self.job_title.text().strip(),
            'employer': self.employer.text().strip(),
            'work_schedule': self.work_schedule.currentText(),
            'income_range': self.income_range.currentText(),
            'financial_stress': self.financial_stress.currentText(),
            
            # Insurance
            'insurance_primary': self.insurance_primary.text().strip(),
            'insurance_secondary': self.insurance_secondary.text().strip(),
            'insurance_id': self.insurance_id.text().strip(),
            'primary_care_physician': self.primary_care_physician.text().strip(),
            'referred_by': self.referred_by.text().strip(),
        }
    
    def set_data(self, data):
        """Set form data from dictionary"""
        # Block signals temporarily to avoid triggering data_changed
        self.blockSignals(True)
        
        # Basic info
        self.first_name.setText(data.get('first_name', ''))
        self.middle_name.setText(data.get('middle_name', ''))
        self.last_name.setText(data.get('last_name', ''))
        self.preferred_name.setText(data.get('preferred_name', ''))
        
        if data.get('date_of_birth'):
            self.date_of_birth.setDate(QDate.fromString(str(data['date_of_birth']), Qt.DateFormat.ISODate))
        
        # Set other fields...
        # (Similar pattern for all fields)
        
        self.blockSignals(False)
    
    def clear_form(self):
        """Clear all form fields"""
        self.blockSignals(True)
        
        # Clear all text fields
        for widget in self.findChildren(QLineEdit):
            widget.clear()
        
        # Reset combo boxes
        for widget in self.findChildren(QComboBox):
            widget.setCurrentIndex(0)
        
        # Reset date to default
        self.date_of_birth.setDate(QDate.currentDate().addYears(-30))
        
        # Reset spin boxes
        for widget in self.findChildren(QSpinBox):
            widget.setValue(0)
        
        # Uncheck checkboxes
        for widget in self.findChildren(QCheckBox):
            widget.setChecked(False)
        
        # Clear text edits
        for widget in self.findChildren(QTextEdit):
            widget.clear()
        
        # Set defaults
        self.primary_language.setCurrentText("English")
        self.address_country.setText("USA")
        
        self.blockSignals(False)