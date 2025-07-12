from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget

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

    def add_medication(self):
        pass
