# 🧠 **Enhanced Psychiatric Records Desktop App - Production Prompt for Cursor AI**

## 🎯 **Project Vision**

Build a **modern, efficient PyQt6 desktop application** for psychiatric clinicians to capture comprehensive patient histories during live interviews. The app prioritizes **speed, intuitive workflow, and beautiful UI** while structuring data for future ML training.

---

## 🚀 **Key Requirements**

### 🎨 **1. Modern UI/UX Design**
- **Dark/Light theme support** with smooth transitions
- **Material Design-inspired** components using `qtawesome` icons
- **Responsive layout** that adapts to different screen sizes
- **Keyboard shortcuts** for rapid data entry (Tab navigation, Ctrl+S save, etc.)
- **Auto-save** functionality with visual save indicators
- **Smooth animations** for tab transitions and form interactions
- **Progress indicators** showing completion status of history sections

### ⚡ **2. Clinical Workflow Optimization**
- **Quick-access toolbar** with frequently used actions
- **Smart autocomplete** for medications, diagnoses, and lab tests
- **Voice-to-text integration** for notes (using `speech_recognition`)
- **Real-time validation** with helpful error messages
- **Undo/Redo** functionality for all data entry
- **Template-based entry** for common psychiatric assessments
- **Bulk operations** for multiple medications/diagnoses

### 📋 **3. Comprehensive Data Collection**

#### **Patient Demographics & Contact**
```python
# Enhanced patient model with comprehensive fields
class Patient:
    - Basic info (name, DOB, gender, contact)
    - Emergency contact details
    - Insurance information
    - Preferred communication method
    - Cultural/language preferences
```

#### **Psychiatric History (Structured)**
```python
class PsychiatricHistory:
    - Previous hospitalizations (dates, facilities, reasons)
    - Suicide attempts/ideation history
    - Self-harm behaviors
    - Previous therapy/counseling
    - Family psychiatric history
    - Trauma history (with sensitivity handling)
    - Current symptoms with severity scales
    - Functional assessment scores
```

#### **Medication Management**
```python
class Medication:
    - Current medications (psychiatric + medical)
    - Dosage with frequency and timing
    - Treatment response tracking (effectiveness 0-100)
    - Side effects (structured + free text)
    - Adherence patterns
    - Previous medication trials and outcomes
    - Allergies and contraindications
    - Drug interaction warnings
```

#### **Substance Use History**
```python
class SubstanceUse:
    - Substance types (alcohol, cannabis, stimulants, etc.)
    - Usage patterns (frequency, amount, route)
    - Timeline of use (onset, periods of abstinence)
    - Treatment history (rehab, AA/NA, MAT)
    - Current status and motivation for change
    - Impact on psychiatric symptoms
    - Legal/social consequences
```

#### **Laboratory & Medical Data**
```python
class LabResult:
    - Comprehensive lab panels (CBC, CMP, lipids, thyroid)
    - Psychiatric-specific tests (lithium levels, etc.)
    - Vital signs and physical measurements
    - EKG results for medication monitoring
    - Imaging results when relevant
    - Trend analysis and alerts for abnormal values
```

---

## 🛠 **Technical Implementation**

### 📦 **Enhanced Dependencies**
```python
# Core requirements
PyQt6>=6.6.0
SQLAlchemy>=2.0.0
pysqlcipher3
pandas>=2.0.0
numpy>=1.24.0

# UI Enhancement
qtawesome>=1.2.3
qtmodern>=0.2.0
pyqtdarktheme>=2.1.0

# Clinical Features
SpeechRecognition>=3.10.0
pyaudio>=0.2.11
fuzzywuzzy>=0.18.0
python-Levenshtein>=0.21.0

# Data Processing
pydantic>=2.0.0
python-dateutil>=2.8.0
validators>=0.20.0
```

### 🏗 **Enhanced Architecture**
```
psychiatric_app/
├── main.py
├── models/
│   ├── base.py
│   ├── patient.py
│   ├── psychiatric_history.py
│   ├── medication.py
│   ├── substance_use.py
│   ├── lab_result.py
│   └── clinical_scales.py
├── ui/
│   ├── main_window.py
│   ├── patient_dashboard.py
│   ├── history_wizard.py
│   ├── medication_manager.py
│   ├── substance_tracker.py
│   ├── lab_monitor.py
│   └── components/
│       ├── modern_widgets.py
│       ├── autocomplete.py
│       └── voice_input.py
├── services/
│   ├── database.py
│   ├── ml_export.py
│   ├── clinical_data.py
│   ├── voice_service.py
│   └── validation.py
├── data/
│   ├── medications.json
│   ├── diagnoses.json
│   ├── lab_references.json
│   └── clinical_scales.json
└── resources/
    ├── themes/
    ├── icons/
    └── templates/
```

---

## 🎨 **UI Components to Build**

### 1. **Main Dashboard**
- **Patient search** with fuzzy matching
- **Recent patients** quick access
- **Appointment schedule** integration
- **Statistics overview** (completion rates, alerts)

### 2. **Patient History Wizard**
- **Step-by-step guided interview** flow
- **Progress tracking** with visual indicators
- **Smart branching** based on responses
- **Voice note recording** with transcription
- **Image attachment** for documents

### 3. **Medication Management Interface**
- **Interactive medication timeline**
- **Dosage calculator** with warnings
- **Side effect tracker** with severity scales
- **Adherence monitoring** with reminders
- **Drug interaction checker**

### 4. **Substance Use Assessment**
- **Visual usage timeline**
- **Severity scoring** with standardized scales
- **Treatment history tracking**
- **Relapse risk assessment**
- **Motivation tracking**

### 5. **Lab Results Dashboard**
- **Trending graphs** for key values
- **Reference range indicators**
- **Alert system** for critical values
- **Medication monitoring** specific tests
- **Export to EMR** functionality

---

## 🧠 **ML-Ready Data Structure**

### **Export Features**
```python
def export_ml_dataset(session, anonymize=True):
    """
    Export structured data for ML training including:
    - Patient demographics (anonymized)
    - Symptom severity scores over time
    - Medication response patterns
    - Lab value trends
    - Substance use patterns
    - Treatment outcomes
    """
    return {
        'patient_features': pd.DataFrame,
        'medication_responses': pd.DataFrame,
        'lab_trends': pd.DataFrame,
        'substance_patterns': pd.DataFrame,
        'clinical_outcomes': pd.DataFrame
    }
```

---

## ⚡ **Performance & Workflow Features**

### **Speed Optimizations (LOCAL ONLY)**
- **Lazy loading** for large datasets
- **Background saving** with progress indicators
- **Local caching** for frequently accessed data
- **Offline-only mode** with no sync requirements
- **Batch operations** for bulk updates
- **Local database optimization** with proper indexing

### **Clinical Workflow Features**
- **Template library** for common assessments
- **Clinical decision support** alerts
- **Standardized scales** integration (PHQ-9, GAD-7, etc.)
- **Appointment scheduling** integration
- **Report generation** for referrals
- **Backup and restore** functionality

---

## 🔒 **Security & Compliance (LOCAL ONLY)**

### **Data Protection**
- **AES-256 encryption** for all patient data (local SQLCipher database)
- **Local key management** with secure password-based encryption
- **Audit logging** stored locally for all data access
- **HIPAA compliance** features for local data handling
- **Local data retention policies**
- **Secure local export** with de-identification
- **NO CLOUD CONNECTIVITY** - All data remains on local machine
- **Offline-first architecture** with no internet dependencies

---

## 📝 **Implementation Priority**

### **Phase 1: Core Functionality**
1. Modern UI framework with theming
2. Basic patient management
3. Medication tracking
4. Lab results entry

### **Phase 2: Advanced Features**
1. Voice input integration
2. Substance use tracking
3. Clinical scales integration
4. ML export functionality

### **Phase 3: Clinical Integration**
1. EMR integration
2. Decision support
3. Reporting system
4. Multi-user support

---

## 🎯 **Success Metrics**

- **Data entry time**: < 15 minutes for comprehensive history
- **User satisfaction**: Intuitive workflow requiring minimal training
- **Data quality**: 95%+ complete records with validation
- **ML readiness**: Structured data suitable for predictive modeling

---

## 🚀 **Getting Started Command**

```bash
# For Cursor AI with Task Master MCP
Create a psychiatric records desktop app with:
- Modern PyQt6 UI with dark/light themes
- Efficient clinical workflow for live patient interviews
- Comprehensive data collection for ML training
- Voice input and smart autocomplete
- Secure encrypted database
- Beautiful, responsive design
```

---

*This prompt provides a complete roadmap for building a production-ready psychiatric records application optimized for clinical efficiency and ML training data collection.*