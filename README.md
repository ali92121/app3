# Enhanced Psychiatric Records Desktop App

This is a modern, efficient PyQt6 desktop application for psychiatric clinicians to capture comprehensive patient histories during live interviews. The app prioritizes speed, intuitive workflow, and beautiful UI while structuring data for future ML training.

## Core requirements
- PyQt6>=6.6.0
- SQLAlchemy>=2.0.0
- pysqlcipher3
- pandas>=2.0.0
- numpy>=1.24.0

## UI Enhancement
- qtawesome>=1.2.3
- qtmodern>=0.2.0
- pyqtdarktheme>=2.1.0

## Clinical Features
- SpeechRecognition>=3.10.0
- pyaudio>=0.2.11
- fuzzywuzzy>=0.18.0
- python-Levenshtein>=0.21.0

## Data Processing
- pydantic>=2.0.0
- python-dateutil>=2.8.0
- validators>=0.20.0

## How to run

1.  Install the required system dependencies:
    ```bash
    sudo apt-get update && sudo apt-get install -y build-essential libsqlcipher-dev portaudio19-dev libxcb-cursor0 qt6-wayland
    ```
2.  Install the required python packages:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python3 psychiatric_app/main.py
    ```
