from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QCheckBox, QComboBox, QLineEdit, QPushButton, QDialog, QTextEdit, QLabel
from psychiatric_app.data.dsm5_hierarchy import DSM5_HIERARCHY

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
