# Psychiatric Records Desktop Application - Phase 1

A comprehensive, modern psychiatric records management system built with PyQt6. This Phase 1 implementation provides the foundational components for secure patient data management, clinical assessment, and treatment tracking.

## 🎯 Features Implemented

### ✅ Modern UI Framework
- **Dark/Light Theme Support** - Material Design-inspired themes with comprehensive styling
- **Responsive Design** - Modern PyQt6 interface optimized for clinical workflows
- **Theme Manager** - Seamless switching between dark and light themes
- **Custom Components** - Material Design buttons, inputs, cards, and navigation

### ✅ Comprehensive Patient Demographics
- **Complete Patient Profiles** - 60+ demographic and social determinant fields
- **6-Tab Interface** - Organized data collection across:
  - Basic Information (identity, demographics)
  - Contact & Emergency details
  - Social & Cultural information
  - Education & Employment history
  - Insurance & Medical information
- **Data Validation** - Real-time validation with helpful error messages
- **Auto-calculations** - Automatic age calculation and data consistency checks

### ✅ DSM-5 TR Symptom Assessment
- **Hierarchical Structure** - Complete DSM-5 TR disorder categories including:
  - Mood Disorders (Depression, Bipolar I/II, Dysthymia)
  - Anxiety Disorders (GAD, Panic, Social Anxiety, Phobias)
  - Trauma Disorders (PTSD, Acute Stress Disorder)
  - ADHD (Combined, Inattentive, Hyperactive presentations)
  - Substance Use Disorders (Alcohol, Cannabis)
  - Psychotic Disorders (Schizophrenia, Brief Psychotic Disorder)
- **Clinical Assessment Tools** - Integrated rating scales (PHQ-9, GAD-7, PCL-5, ADHD-RS)
- **Symptom Tracking** - Severity ratings, duration tracking, functional impairment assessment
- **Progress Monitoring** - Baseline comparisons and improvement tracking

### ✅ Medication Management
- **Comprehensive Tracking** - Full medication profiles with:
  - Dosage and administration details
  - Effectiveness rating (0-100 scale)
  - Side effect monitoring
  - Adherence tracking
  - Lab monitoring requirements
- **Psychiatric Focus** - Specialized features for psychiatric medications
- **Clinical Context** - Indication tracking, prescriber information, treatment goals
- **Progress Notes** - Timestamped clinical observations and adjustments

### ✅ Laboratory Results Management
- **Complete Lab Tracking** - Test results with reference ranges and abnormal flagging
- **Clinical Interpretation** - Automatic abnormal value detection with severity classification
- **Psychiatric Relevance** - Specialized handling for psychiatry-relevant labs
- **Trend Analysis** - Comparison with previous results and improvement tracking
- **Quality Control** - Specimen tracking, verification status, and quality flags

### ✅ Secure Data Architecture
- **Encrypted Storage** - Database encryption ready (SQLCipher integration prepared)
- **Audit Trails** - Comprehensive logging of all data changes
- **Data Validation** - Multi-level validation for data integrity
- **Auto-save** - Automatic data persistence with visual indicators

## 🏗️ Technical Architecture

### Database Models
- **SQLAlchemy ORM** - Modern database abstraction with relationship management
- **Encrypted Storage Ready** - Architecture prepared for SQLCipher integration
- **Audit Fields** - Created/updated timestamps, user tracking, soft delete support
- **Data Validation** - Model-level validation with comprehensive error handling

### UI Components
- **PyQt6 Framework** - Latest Qt6 bindings for Python
- **Material Design** - Modern, accessible interface following Material Design principles
- **Theme System** - Comprehensive theming with color palette management
- **Responsive Layout** - Adaptive layouts for different screen sizes

### Data Structures
- **DSM-5 TR Compliance** - Accurate implementation of diagnostic criteria
- **Clinical Scales** - Integrated standardized assessment tools
- **Reference Data** - Comprehensive clinical reference databases

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Virtual environment (recommended)
- SQLCipher development libraries (for encryption - see Known Issues)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd psychiatric-records-app
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python -m psychiatric_app.main
   ```

### Development Setup

For development with full encryption support:

1. **Install SQLCipher system libraries**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install libsqlcipher-dev libsqlcipher0
   
   # macOS with Homebrew
   brew install sqlcipher
   
   # CentOS/RHEL
   sudo yum install sqlcipher-devel
   ```

2. **Enable encrypted database**
   ```bash
   pip install pysqlcipher3
   ```

## 📁 Project Structure

```
psychiatric_app/
├── main.py                 # Application entry point
├── config/                 # Configuration and database setup
│   ├── database.py        # SQLCipher database configuration
│   └── settings.py        # Application settings management
├── models/                 # SQLAlchemy database models
│   ├── base.py           # Base model with audit fields
│   ├── patient.py        # Patient demographics model
│   ├── medication.py     # Medication tracking model
│   ├── lab_result.py     # Laboratory results model
│   └── symptom_assessment.py # DSM-5 symptom tracking
├── ui/                    # User interface components
│   ├── main_window.py    # Main application window
│   ├── demographics_form.py # Patient demographics interface
│   ├── symptom_assessment.py # DSM-5 assessment interface
│   ├── medication_manager.py # Medication management UI
│   ├── lab_results.py    # Lab results interface
│   └── components/       # Reusable UI components
│       └── theme_manager.py # Theme management system
└── data/                  # Clinical reference data
    └── dsm5_hierarchy.py # DSM-5 TR diagnostic structure
```

## 🎨 UI Themes

The application supports both dark and light themes with Material Design principles:

### Dark Theme
- Optimized for extended clinical use
- Reduced eye strain in low-light environments
- Modern color palette with excellent contrast

### Light Theme  
- Clean, professional appearance
- High contrast for detailed data review
- Accessibility-focused design

**Theme Switching**: Use Ctrl+T or the theme toggle in the menu bar.

## 📊 Clinical Features

### DSM-5 TR Assessment
- **Complete Diagnostic Criteria** - All major psychiatric disorder categories
- **Severity Ratings** - Standardized severity assessment (0-10 scale)
- **Duration Tracking** - Onset dates and symptom duration monitoring
- **Functional Impairment** - Multi-domain functional assessment
- **Treatment Planning** - Priority setting and goal tracking

### Medication Monitoring
- **Effectiveness Tracking** - Quantitative effectiveness ratings
- **Side Effect Management** - Comprehensive adverse event tracking
- **Adherence Monitoring** - Compliance assessment and intervention planning
- **Drug Interactions** - Interaction checking and contraindication alerts
- **Lab Monitoring** - Required lab work tracking and reminders

### Laboratory Integration
- **Reference Ranges** - Age and gender-appropriate normal values
- **Critical Values** - Automatic flagging of life-threatening results
- **Trend Analysis** - Graphical representation of lab trends over time
- **Clinical Correlation** - Medication and symptom correlation with lab results

## ⚠️ Known Issues

### SQLCipher Dependency
**Issue**: Database encryption requires SQLCipher system libraries that are not available in all environments.

**Temporary Solution**: The application currently runs with standard SQLite (unencrypted) for compatibility.

**Resolution**: To enable full encryption:
1. Install SQLCipher development libraries for your system
2. Uncomment the `pysqlcipher3>=0.5.0` line in `requirements.txt`
3. Reinstall dependencies: `pip install -r requirements.txt`

### Display Issues
**Note**: The application requires a graphical desktop environment. Remote or headless servers will need X11 forwarding or VNC.

## 🚦 Current Status

### ✅ Completed (Phase 1)
- Modern UI framework with theming
- Complete patient demographics system
- DSM-5 TR symptom assessment framework
- Medication tracking and management
- Laboratory results system
- Database architecture and models
- Data validation and security framework

### 🔄 In Progress
- Database encryption integration
- Advanced clinical reporting
- Data export/import functionality

### 📋 Planned (Future Phases)
- Treatment planning module
- Progress note templates
- Clinical decision support
- Integration with external systems
- Advanced analytics and reporting

## 🔒 Security & Compliance

### Data Protection
- **Encryption Ready** - Database encryption architecture implemented
- **Audit Logging** - Comprehensive change tracking
- **Access Controls** - User authentication framework prepared
- **Data Validation** - Multi-level input validation and sanitization

### HIPAA Considerations
- **Local Storage** - Data remains on local systems
- **Encryption** - Database encryption ready for deployment
- **Audit Trails** - Complete activity logging
- **Access Controls** - Role-based access framework

**Note**: This is a development version. Production deployment requires additional security hardening and compliance review.

## 🤝 Contributing

This project follows modern Python development practices:

- **Code Style** - PEP 8 compliance with type hints
- **Architecture** - Clean separation of concerns (MVC pattern)
- **Documentation** - Comprehensive docstrings and comments
- **Testing** - Framework prepared for unit and integration tests

## 📄 License

This psychiatric records application is developed for clinical and educational use. Please review licensing terms before deployment in production environments.

## 📞 Support

For technical support or clinical feature requests, please refer to the project documentation or contact the development team.

---

**Version**: 1.0.0 (Phase 1)  
**Last Updated**: January 2025  
**Python Version**: 3.11+  
**Framework**: PyQt6 6.6.0+
