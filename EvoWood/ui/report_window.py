import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QTextEdit
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLIENTI_PATH = os.path.join(DATA_DIR, "clienti.json")
APPUNTAMENTI_PATH = os.path.join(DATA_DIR, "appuntamenti.json")

class ReportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reportistica avanzata")
        self.resize(800, 500)
        layout = QVBoxLayout(self)
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)
        btn_layout = QVBoxLayout()
        btn_estrai = QPushButton("Estrai report (testuale)")
        btn_export = QPushButton("Esporta report CSV")
        btn_layout.addWidget(btn_estrai)
        btn_layout.addWidget(btn_export)
        layout.addLayout(btn_layout)
        btn_estrai.clicked.connect(self.estrai_report)
        btn_export.clicked.connect(self.export_csv)

    def estrai_report(self):
        s = []
        # Statistiche clienti/offerte/appuntamenti
        with open(CLIENTI_PATH, "r", encoding="utf-8") as f:
            clienti = json.load(f)
        with open(APPUNTAMENTI_PATH, "r", encoding="utf-8") as f:
            appuntamenti = json.load(f)
        s.append(f"Totale clienti: {len(clienti)}")
        offerte = sum(len(c.get("offerte",[])) for c in clienti)
        s.append(f"Totale offerte: {offerte}")
        s.append(f"Totale appuntamenti: {len(appuntamenti)}")
        # Offerte per stato
        stati = {}
        for c in clienti:
            for o in c.get("offerte",[]):
                stato = o["stato"]
                stati[stato] = stati.get(stato,0)+1
        s.append("Offerte per stato:")
        for stato, n in stati.items():
            s.append(f" - {stato}: {n}")
        # Appuntamenti futuri
        oggi = datetime.now().strftime("%Y-%m-%d %H:%M")
        futuri = [a for a in appuntamenti if a.get("dataora","") >= oggi]
        s.append(f"Appuntamenti futuri: {len(futuri)}")
        self.text.setText("\n".join(s))

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Esporta report CSV", "", "CSV files (*.csv)")
        if not path:
            return
        try:
            with open(CLIENTI_PATH, "r", encoding="utf-8") as f:
                clienti = json.load(f)
            with open(APPUNTAMENTI_PATH, "r", encoding="utf-8") as f:
                appuntamenti = json.load(f)
            with open(path, "w", encoding="utf-8") as f:
                f.write("Tipo,Valore\n")
                f.write(f"Clienti,{len(clienti)}\n")
                offerte = sum(len(c.get('offerte',[])) for c in clienti)
                f.write(f"Offerte,{offerte}\n")
                f.write(f"Appuntamenti,{len(appuntamenti)}\n")
            QMessageBox.information(self, "Esporta", f"Report CSV esportato:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore durante l'esportazione: {e}")
