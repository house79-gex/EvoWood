import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QDialog, QFormLayout
)
from PyQt5.QtCore import Qt

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLIENTI_PATH = os.path.join(DATA_DIR, "clienti.json")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(CLIENTI_PATH):
        with open(CLIENTI_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)

class ClienteDialog(QDialog):
    def __init__(self, parent=None, cliente=None):
        super().__init__(parent)
        self.setWindowTitle("Dati Cliente")
        layout = QFormLayout()
        self.nome = QLineEdit(cliente["nome"] if cliente else "")
        self.cognome = QLineEdit(cliente["cognome"] if cliente else "")
        self.telefono = QLineEdit(cliente["telefono"] if cliente else "")
        self.email = QLineEdit(cliente["email"] if cliente else "")
        self.indirizzo = QLineEdit(cliente["indirizzo"] if cliente else "")
        layout.addRow("Nome:", self.nome)
        layout.addRow("Cognome:", self.cognome)
        layout.addRow("Telefono:", self.telefono)
        layout.addRow("Email:", self.email)
        layout.addRow("Indirizzo:", self.indirizzo)
        self.setLayout(layout)
        self.setMinimumWidth(300)
        self.result = None
        btn_box = QHBoxLayout()
        salva_btn = QPushButton("Salva")
        salva_btn.clicked.connect(self.accept)
        annulla_btn = QPushButton("Annulla")
        annulla_btn.clicked.connect(self.reject)
        btn_box.addWidget(salva_btn)
        btn_box.addWidget(annulla_btn)
        layout.addRow(btn_box)

    def get_data(self):
        return {
            "nome": self.nome.text(),
            "cognome": self.cognome.text(),
            "telefono": self.telefono.text(),
            "email": self.email.text(),
            "indirizzo": self.indirizzo.text()
        }

class ClientiWindow(QWidget):
    COLS = ["Nome", "Cognome", "Telefono", "Email", "Indirizzo"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestione Clienti")
        self.resize(700, 400)
        ensure_data_dir()
        self.clienti = self.load_clienti()

        main_layout = QVBoxLayout(self)

        # Tabella
        self.table = QTableWidget(0, len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        main_layout.addWidget(self.table)

        # Pulsanti
        btn_layout = QHBoxLayout()
        self.btn_nuovo = QPushButton("Nuovo")
        self.btn_modifica = QPushButton("Modifica")
        self.btn_elimina = QPushButton("Elimina")
        self.btn_salva = QPushButton("Salva su file")
        btn_layout.addWidget(self.btn_nuovo)
        btn_layout.addWidget(self.btn_modifica)
        btn_layout.addWidget(self.btn_elimina)
        btn_layout.addWidget(self.btn_salva)
        main_layout.addLayout(btn_layout)

        self.btn_nuovo.clicked.connect(self.nuovo_cliente)
        self.btn_modifica.clicked.connect(self.modifica_cliente)
        self.btn_elimina.clicked.connect(self.elimina_cliente)
        self.btn_salva.clicked.connect(self.salva_clienti)

        self.aggiorna_tabella()

    def load_clienti(self):
        try:
            with open(CLIENTI_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def salva_clienti(self):
        try:
            with open(CLIENTI_PATH, "w", encoding="utf-8") as f:
                json.dump(self.clienti, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Salvataggio", "Clienti salvati con successo!")
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore nel salvataggio: {e}")

    def aggiorna_tabella(self):
        self.table.setRowCount(len(self.clienti))
        for row, cliente in enumerate(self.clienti):
            for col, key in enumerate(["nome", "cognome", "telefono", "email", "indirizzo"]):
                self.table.setItem(row, col, QTableWidgetItem(cliente.get(key, "")))

    def nuovo_cliente(self):
        dialog = ClienteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.clienti.append(dialog.get_data())
            self.aggiorna_tabella()

    def modifica_cliente(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un cliente da modificare.")
            return
        cliente = self.clienti[row]
        dialog = ClienteDialog(self, cliente)
        if dialog.exec_() == QDialog.Accepted:
            self.clienti[row] = dialog.get_data()
            self.aggiorna_tabella()

    def elimina_cliente(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un cliente da eliminare.")
            return
        reply = QMessageBox.question(self, "Conferma", "Eliminare il cliente selezionato?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.clienti[row]
            self.aggiorna_tabella()
