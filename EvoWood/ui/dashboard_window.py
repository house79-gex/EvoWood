from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt
import os, json, datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLIENTI_PATH = os.path.join(DATA_DIR, "clienti.json")
APPUNTAMENTI_PATH = os.path.join(DATA_DIR, "appuntamenti.json")

def _count_offerte():
    if not os.path.exists(CLIENTI_PATH):
        return 0
    with open(CLIENTI_PATH, "r", encoding="utf-8") as f:
        clienti = json.load(f)
    return sum(len(c.get("offerte", [])) for c in clienti)

def _count_clienti():
    if not os.path.exists(CLIENTI_PATH):
        return 0
    with open(CLIENTI_PATH, "r", encoding="utf-8") as f:
        clienti = json.load(f)
    return len(clienti)

def _count_appuntamenti():
    if not os.path.exists(APPUNTAMENTI_PATH):
        return 0
    with open(APPUNTAMENTI_PATH, "r", encoding="utf-8") as f:
        appuntamenti = json.load(f)
    return len(appuntamenti)

def _get_next_appuntamenti(n=5):
    if not os.path.exists(APPUNTAMENTI_PATH):
        return []
    with open(APPUNTAMENTI_PATH, "r", encoding="utf-8") as f:
        appuntamenti = json.load(f)
    oggi = datetime.datetime.now().strftime("%Y-%m-%d")
    futuri = [a for a in appuntamenti if a.get("dataora","") >= oggi]
    futuri = sorted(futuri, key=lambda a: a["dataora"])
    return futuri[:n]

class DashboardWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dashboard")
        self.resize(900, 400)
        layout = QVBoxLayout(self)

        # Statistiche
        stats_group = QGroupBox("Statistiche rapide")
        stats_layout = QHBoxLayout()
        self.lbl_clienti = QLabel()
        self.lbl_offerte = QLabel()
        self.lbl_appuntamenti = QLabel()
        stats_layout.addWidget(self.lbl_clienti)
        stats_layout.addWidget(self.lbl_offerte)
        stats_layout.addWidget(self.lbl_appuntamenti)
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # Prossimi appuntamenti
        appunt_group = QGroupBox("Prossimi appuntamenti")
        appunt_layout = QVBoxLayout()
        self.lbl_next_appunt = QLabel()
        appunt_layout.addWidget(self.lbl_next_appunt)
        appunt_group.setLayout(appunt_layout)
        layout.addWidget(appunt_group)

        # Pulsanti rapidi
        btn_layout = QHBoxLayout()
        self.btn_clienti = QPushButton("Gestione Clienti")
        self.btn_offerte = QPushButton("Gestione Offerte")
        self.btn_appuntamenti = QPushButton("Gestione Appuntamenti")
        btn_layout.addWidget(self.btn_clienti)
        btn_layout.addWidget(self.btn_offerte)
        btn_layout.addWidget(self.btn_appuntamenti)
        layout.addLayout(btn_layout)

        self.refresh_dashboard()

    def refresh_dashboard(self):
        self.lbl_clienti.setText(f"Clienti totali: <b>{_count_clienti()}</b>")
        self.lbl_offerte.setText(f"Offerte totali: <b>{_count_offerte()}</b>")
        self.lbl_appuntamenti.setText(f"Appuntamenti totali: <b>{_count_appuntamenti()}</b>")
        # Prossimi appuntamenti
        rows = []
        for a in _get_next_appuntamenti(5):
            rows.append(f"{a['dataora']} - {a.get('cliente_nome','')} - {a['titolo']}")
        if not rows:
            rows.append("Nessun appuntamento futuro.")
        self.lbl_next_appunt.setText("<br>".join(rows))
