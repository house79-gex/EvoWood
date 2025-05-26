import os
import json
import re
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

def valida_codice_fiscale(cf):
    return bool(re.fullmatch(r"[A-Z0-9]{16}", cf.upper()))

def valida_partita_iva(pi):
    return bool(re.fullmatch(r"\d{11}", pi))

def valida_email(email):
    return "@" in email and "." in email

def valida_telefono(tel):
    # Accetta cifre, +, -, spazi
    return bool(re.fullmatch(r"[0-9+\- ]{6,20}", tel.strip()))

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
        self.codice_fiscale = QLineEdit(cliente["codice_fiscale"] if cliente and "codice_fiscale" in cliente else "")
        self.partita_iva = QLineEdit(cliente["partita_iva"] if cliente and "partita_iva" in cliente else "")
        layout.addRow("Nome:", self.nome)
        layout.addRow("Cognome:", self.cognome)
        layout.addRow("Telefono:", self.telefono)
        layout.addRow("Email:", self.email)
        layout.addRow("Indirizzo:", self.indirizzo)
        layout.addRow("Codice Fiscale:", self.codice_fiscale)
        layout.addRow("Partita IVA:", self.partita_iva)
        self.setLayout(layout)
        self.setMinimumWidth(350)
        self.result = None
        btn_box = QHBoxLayout()
        salva_btn = QPushButton("Salva")
        salva_btn.clicked.connect(self.on_accept)
        annulla_btn = QPushButton("Annulla")
        annulla_btn.clicked.connect(self.reject)
        btn_box.addWidget(salva_btn)
        btn_box.addWidget(annulla_btn)
        layout.addRow(btn_box)

    def on_accept(self):
        errors = []
        if not self.nome.text().strip():
            errors.append("Il nome è obbligatorio.")
        if not self.cognome.text().strip():
            errors.append("Il cognome è obbligatorio.")
        if self.email.text().strip() and not valida_email(self.email.text().strip()):
            errors.append("Email non valida.")
        if self.telefono.text().strip() and not valida_telefono(self.telefono.text().strip()):
            errors.append("Telefono non valido (solo cifre, +, - e spazi).")
        cf = self.codice_fiscale.text().strip().upper()
        if cf and not valida_codice_fiscale(cf):
            errors.append("Codice fiscale non valido (16 caratteri, lettere e numeri).")
        pi = self.partita_iva.text().strip()
        if pi and not valida_partita_iva(pi):
            errors.append("Partita IVA non valida (11 cifre).")
        if errors:
            QMessageBox.warning(self, "Dati non validi", "\n".join(errors))
            return
        self.accept()

    def get_data(self):
        return {
            "nome": self.nome.text().strip(),
            "cognome": self.cognome.text().strip(),
            "telefono": self.telefono.text().strip(),
            "email": self.email.text().strip(),
            "indirizzo": self.indirizzo.text().strip(),
            "codice_fiscale": self.codice_fiscale.text().strip().upper(),
            "partita_iva": self.partita_iva.text().strip()
        }

class ClientiWindow(QWidget):
    COLS = [
        "Nome", "Cognome", "Telefono", "Email", "Indirizzo", "Codice Fiscale", "Partita IVA"
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestione Clienti")
        self.resize(950, 500)
        ensure_data_dir()
        self.clienti = self.load_clienti()
        self.filtrati = self.clienti.copy()

        main_layout = QVBoxLayout(self)

        # Barra di ricerca
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Cerca (nome, cognome, email, CF, P.IVA)...")
        self.search_box.textChanged.connect(self.filter_clienti)
        search_layout.addWidget(QLabel("Ricerca:"))
        search_layout.addWidget(self.search_box)
        main_layout.addLayout(search_layout)

        # Tabella
        self.table = QTableWidget(0, len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setSortingEnabled(True)
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
        self.filter_clienti(self.search_box.text())

    def filter_clienti(self, filtro):
        filtro = filtro.lower().strip()
        if filtro:
            self.filtrati = [c for c in self.clienti if
                filtro in c.get("nome", "").lower() or
                filtro in c.get("cognome", "").lower() or
                filtro in c.get("email", "").lower() or
                filtro in c.get("codice_fiscale", "").lower() or
                filtro in c.get("partita_iva", "").lower()
            ]
        else:
            self.filtrati = self.clienti.copy()
        self._aggiorna_tabella_filtrata()

    def _aggiorna_tabella_filtrata(self):
        self.table.setRowCount(len(self.filtrati))
        for row, cliente in enumerate(self.filtrati):
            for col, key in enumerate([
                "nome", "cognome", "telefono", "email", "indirizzo", "codice_fiscale", "partita_iva"
            ]):
                self.table.setItem(row, col, QTableWidgetItem(cliente.get(key, "")))

    def get_selected_cliente_global_index(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.filtrati):
            return None
        # Ricava l'indice del cliente selezionato nella lista globale
        cliente_selezionato = self.filtrati[row]
        for idx, c in enumerate(self.clienti):
            if c == cliente_selezionato:
                return idx
        return None

    def nuovo_cliente(self):
        dialog = ClienteDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.clienti.append(dialog.get_data())
            self.aggiorna_tabella()

    def modifica_cliente(self):
        idx = self.get_selected_cliente_global_index()
        if idx is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona un cliente da modificare.")
            return
        cliente = self.clienti[idx]
        dialog = ClienteDialog(self, cliente)
        if dialog.exec_() == QDialog.Accepted:
            self.clienti[idx] = dialog.get_data()
            self.aggiorna_tabella()

    def elimina_cliente(self):
        idx = self.get_selected_cliente_global_index()
        if idx is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona un cliente da eliminare.")
            return
        reply = QMessageBox.question(self, "Conferma", "Eliminare il cliente selezionato?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.clienti[idx]
            self.aggiorna_tabella()
