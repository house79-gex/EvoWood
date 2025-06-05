from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QCheckBox

class BackupSelector(QDialog):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleziona cosa includere nel backup")
        self.selected = []
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Seleziona i dati da includere:"))
        self.checkboxes = []
        for entry in items:
            cb = QCheckBox(entry)
            cb.setChecked(True)
            self.checkboxes.append(cb)
            layout.addWidget(cb)
        self.ok_btn = QPushButton("OK")
        self.ok_btn.clicked.connect(self.accept)
        layout.addWidget(self.ok_btn)
        self.setLayout(layout)

    def get_selected(self):
        return [cb.text() for cb in self.checkboxes if cb.isChecked()]
