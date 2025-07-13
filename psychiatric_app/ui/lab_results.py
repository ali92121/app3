from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget

class LabResultsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        add_button = QPushButton("Add Lab Result")
        layout.addWidget(add_button)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Test Name", "Value", "Unit", "Reference Range", "Date"])
        layout.addWidget(self.table)

        self.setLayout(layout)
