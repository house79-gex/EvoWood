import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView, QDialog, QFormLayout, QDateTimeEdit, QTextEdit, QComboBox, QFileDialog
)
from PyQt5.QtCore import Qt, QDateTime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
APPUNTAMENTI_PATH = os.path.join(DATA_DIR, "appuntamenti.json")
CLIENTI_PATH = os.path.join(DATA_DIR, "clienti.json")

def ensure_appuntamenti_file():
    if not os.path.exists(APPUNTAMENTI_PATH):
        with open(APPUNTAMENTI_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)

def load_clienti_for_combo():
    if not os.path.exists(CLIENTI_PATH):
        return []
    with open(CLIENTI_PATH, "r", encoding="utf-8") as f:
        clienti = json.load(f)
    return [
        (c.get("ragione_sociale") or f"{c.get('nome','')} {c.get('cognome','')}".strip(), c)
        for c in clienti
    ]

class AppuntamentoDialog(QDialog):
    def __init__(self, parent=None, appuntamento=None):
        super().__init__(parent)
        self.setWindowTitle("Appuntamento")
        self.setMinimumWidth(350)
        layout = QFormLayout()
        self.cliente_combo = QComboBox()
        self.clienti = load_clienti_for_combo()
        self.cliente_combo.addItem("(Nessun cliente collegato)", None)
        for nome, c in self.clienti:
            self.cliente_combo.addItem(nome, c)
        if appuntamento and appuntamento.get("cliente_nome"):
            idx = self.cliente_combo.findText(appuntamento["cliente_nome"])
            if idx >= 0:
                self.cliente_combo.setCurrentIndex(idx)
        self.titolo = QLineEdit(appuntamento.get("titolo","") if appuntamento else "")
        self.dataora = QDateTimeEdit()
        self.dataora.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.dataora.setCalendarPopup(True)
        if appuntamento and appuntamento.get("dataora"):
            self.dataora.setDateTime(QDateTime.fromString(appuntamento["dataora"], "yyyy-MM-dd HH:mm"))
        else:
            self.dataora.setDateTime(QDateTime.currentDateTime())
        self.note = QTextEdit(appuntamento.get("note","") if appuntamento else "")
        layout.addRow("Cliente:", self.cliente_combo)
        layout.addRow("Titolo:", self.titolo)
        layout.addRow("Data/Ora:", self.dataora)
        layout.addRow("Note:", self.note)
        self.setLayout(layout)
        btn_box = QHBoxLayout()
        salva_btn = QPushButton("Salva")
        salva_btn.clicked.connect(self.accept)
        annulla_btn = QPushButton("Annulla")
        annulla_btn.clicked.connect(self.reject)
        btn_box.addWidget(salva_btn)
        btn_box.addWidget(annulla_btn)
        layout.addRow(btn_box)

    def get_data(self):
        idx = self.cliente_combo.currentIndex()
        cliente = self.cliente_combo.itemData(idx)
        return {
            "cliente_nome": self.cliente_combo.currentText() if idx > 0 else "",
            "cliente_tipo": cliente.get("tipo_cliente") if cliente else "",
            "titolo": self.titolo.text().strip(),
            "dataora": self.dataora.dateTime().toString("yyyy-MM-dd HH:mm"),
            "note": self.note.toPlainText().strip()
        }

class AppuntamentiWindow(QWidget):
    COLS = ["Cliente", "Titolo", "Data/Ora", "Note"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Appuntamenti")
        self.resize(800, 500)
        ensure_appuntamenti_file()
        self.appuntamenti = self.load_appuntamenti()
        self.filtered = self.appuntamenti.copy()

        main_layout = QVBoxLayout(self)

        # Ricerca
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Cerca appuntamenti...")
        self.search_box.textChanged.connect(self.filter_appuntamenti)
        search_layout.addWidget(QLabel("Ricerca:"))
        search_layout.addWidget(self.search_box)
        main_layout.addLayout(search_layout)

        # Tabella appuntamenti
        self.table = QTableWidget(0, len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        # Pulsanti
        btn_layout = QHBoxLayout()
        self.btn_nuovo = QPushButton("Nuovo")
        self.btn_modifica = QPushButton("Modifica")
        self.btn_elimina = QPushButton("Elimina")
        self.btn_export = QPushButton("Esporta CSV")
        btn_layout.addWidget(self.btn_nuovo)
        btn_layout.addWidget(self.btn_modifica)
        btn_layout.addWidget(self.btn_elimina)
        btn_layout.addWidget(self.btn_export)
        main_layout.addLayout(btn_layout)

        self.btn_nuovo.clicked.connect(self.nuovo_appuntamento)
        self.btn_modifica.clicked.connect(self.modifica_appuntamento)
        self.btn_elimina.clicked.connect(self.elimina_appuntamento)
        self.btn_export.clicked.connect(self.esporta_csv)

        self.aggiorna_tabella()

    def load_appuntamenti(self):
        try:
            with open(APPUNTAMENTI_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def salva_appuntamenti(self):
        try:
            with open(APPUNTAMENTI_PATH, "w", encoding="utf-8") as f:
                json.dump(self.appuntamenti, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Salvataggio", "Appuntamenti salvati con successo!")
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore nel salvataggio: {e}")

    def aggiorna_tabella(self):
        self.filter_appuntamenti(self.search_box.text())

    def filter_appuntamenti(self, filtro):
        filtro = filtro.lower().strip()
        if filtro:
            self.filtered = [a for a in self.appuntamenti if
                filtro in (a.get("cliente_nome","").lower()) or
                filtro in (a.get("titolo","").lower()) or
                filtro in (a.get("dataora","").lower()) or
                filtro in (a.get("note","").lower())
            ]
        else:
            self.filtered = self.appuntamenti.copy()
        self._aggiorna_tabella_filtrata()

    def _aggiorna_tabella_filtrata(self):
        self.table.setRowCount(len(self.filtered))
        for row, a in enumerate(self.filtered):
            self.table.setItem(row, 0, QTableWidgetItem(a.get("cliente_nome","")))
            self.table.setItem(row, 1, QTableWidgetItem(a.get("titolo","")))
            self.table.setItem(row, 2, QTableWidgetItem(a.get("dataora","")))
            self.table.setItem(row, 3, QTableWidgetItem(a.get("note","")))

    def get_selected_appuntamento_index(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.filtered):
            return None
        app_sel = self.filtered[row]
        for idx, a in enumerate(self.appuntamenti):
            if a == app_sel:
                return idx
        return None

    def nuovo_appuntamento(self):
        dialog = AppuntamentoDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.appuntamenti.append(dialog.get_data())
            self.salva_appuntamenti()
            self.aggiorna_tabella()

    def modifica_appuntamento(self):
        idx = self.get_selected_appuntamento_index()
        if idx is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona un appuntamento da modificare.")
            return
        appuntamento = self.appuntamenti[idx]
        dialog = AppuntamentoDialog(self, appuntamento)
        if dialog.exec_() == QDialog.Accepted:
            self.appuntamenti[idx] = dialog.get_data()
            self.salva_appuntamenti()
            self.aggiorna_tabella()

    def elimina_appuntamento(self):
        idx = self.get_selected_appuntamento_index()
        if idx is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona un appuntamento da eliminare.")
            return
        reply = QMessageBox.question(self, "Conferma", "Eliminare l'appuntamento selezionato?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.appuntamenti[idx]
            self.salva_appuntamenti()
            self.aggiorna_tabella()

    def esporta_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Esporta appuntamenti CSV", "", "CSV files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.COLS)
                for a in self.filtered:
                    writer.writerow([
                        a.get("cliente_nome",""),
                        a.get("titolo",""),
                        a.get("dataora",""),
                        a.get("note","")
                    ])
            QMessageBox.information(self, "Esporta", f"Esportazione completata:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore durante l'esportazione: {e}")
