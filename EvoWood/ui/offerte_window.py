import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QHeaderView, QApplication
)
from PyQt5.QtCore import Qt

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLIENTI_PATH = os.path.join(DATA_DIR, "clienti.json")

def load_all_offerte():
    if not os.path.exists(CLIENTI_PATH):
        return []
    with open(CLIENTI_PATH, "r", encoding="utf-8") as f:
        clienti = json.load(f)
    offerte = []
    for c in clienti:
        for off in c.get("offerte", []):
            offerte.append({
                "cliente": c.get("ragione_sociale") or f"{c.get('nome','')} {c.get('cognome','')}".strip(),
                "cliente_tipo": c.get("tipo_cliente"),
                "descrizione": off["descrizione"],
                "importo": off["importo"],
                "stato": off["stato"],
                "data": off["data"],
                "cliente_ref": c  # riferimento al cliente per apertura/modifica
            })
    return offerte

class OfferteWindow(QWidget):
    COLS = ["Cliente", "Descrizione", "Importo (€)", "Stato", "Data"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestione Offerte (tutti i clienti)")
        self.resize(950, 500)
        self.offerte = load_all_offerte()
        self.filtered = self.offerte.copy()

        main_layout = QVBoxLayout(self)

        # Ricerca
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Cerca in tutte le offerte...")
        self.search_box.textChanged.connect(self.filter_offerte)
        search_layout.addWidget(QLabel("Ricerca:"))
        search_layout.addWidget(self.search_box)
        main_layout.addLayout(search_layout)

        # Tabella offerte
        self.table = QTableWidget(0, len(self.COLS))
        self.table.setHorizontalHeaderLabels(self.COLS)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)
        self.table.cellDoubleClicked.connect(self.show_cliente_details)

        # Pulsanti
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton("Aggiorna")
        self.btn_export = QPushButton("Esporta CSV")
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_export)
        main_layout.addLayout(btn_layout)

        self.btn_refresh.clicked.connect(self.aggiorna_offerte)
        self.btn_export.clicked.connect(self.esporta_csv)

        self.aggiorna_tabella()

    def aggiorna_offerte(self):
        self.offerte = load_all_offerte()
        self.filter_offerte(self.search_box.text())

    def filter_offerte(self, filtro):
        filtro = filtro.lower().strip()
        if filtro:
            self.filtered = [o for o in self.offerte if
                filtro in (o["cliente"] or "").lower() or
                filtro in (o["descrizione"] or "").lower() or
                filtro in (o["stato"] or "").lower() or
                filtro in (o["data"] or "").lower()
            ]
        else:
            self.filtered = self.offerte.copy()
        self.aggiorna_tabella()

    def aggiorna_tabella(self):
        self.table.setRowCount(len(self.filtered))
        for row, o in enumerate(self.filtered):
            self.table.setItem(row, 0, QTableWidgetItem(o["cliente"]))
            self.table.setItem(row, 1, QTableWidgetItem(o["descrizione"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(o["importo"])))
            self.table.setItem(row, 3, QTableWidgetItem(o["stato"]))
            self.table.setItem(row, 4, QTableWidgetItem(o["data"]))

    def show_cliente_details(self, row, col):
        # Opzionale: apri la finestra dettaglio cliente su questa offerta.
        o = self.filtered[row]
        QMessageBox.information(self, "Cliente", f"Cliente: {o['cliente']}\nDescrizione offerta: {o['descrizione']}")

    def esporta_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Esporta offerte CSV", "", "CSV files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", newline='', encoding="utf-8") as f:
                import csv
                writer = csv.writer(f)
                writer.writerow(self.COLS)
                for o in self.filtered:
                    writer.writerow([
                        o["cliente"], o["descrizione"], o["importo"], o["stato"], o["data"]
                    ])
            QMessageBox.information(self, "Esporta", f"Esportazione completata:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore durante l'esportazione: {e}")
