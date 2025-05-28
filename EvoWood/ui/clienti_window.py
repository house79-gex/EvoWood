import os
import json
import csv
import re
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QLabel, QMessageBox, QDialog, QFormLayout, QFileDialog, QHeaderView,
    QTextEdit, QApplication, QTabWidget, QComboBox, QListWidget, QListWidgetItem, QInputDialog
)
from PyQt5.QtCore import Qt

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CLIENTI_PATH = os.path.join(DATA_DIR, "clienti.json")
ALLEGATI_DIR = os.path.join(DATA_DIR, "allegati")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(ALLEGATI_DIR):
        os.makedirs(ALLEGATI_DIR)
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
    return bool(re.fullmatch(r"[0-9+\- ]{6,20}", tel.strip()))

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

class ClienteDialog(QDialog):
    def __init__(self, parent=None, cliente=None):
        super().__init__(parent)
        self.setWindowTitle("Dettaglio Cliente")
        self.setMinimumWidth(500)

        self.cliente = dict(cliente) if cliente else None
        self.is_edit = cliente is not None

        self.tabs = QTabWidget()
        self.tab_dati = QWidget()
        self.tab_offerte = QWidget()
        self.tab_storico = QWidget()
        self.tab_allegati = QWidget()

        self.tabs.addTab(self.tab_dati, "Dati")
        self.tabs.addTab(self.tab_offerte, "Offerte")
        self.tabs.addTab(self.tab_storico, "Storico")
        self.tabs.addTab(self.tab_allegati, "Allegati")

        dlg_layout = QVBoxLayout(self)
        dlg_layout.addWidget(self.tabs)

        # --- TAB DATI ---
        dati_layout = QFormLayout()
        self.tipo_cliente = QComboBox()
        self.tipo_cliente.addItems(["Persona fisica", "Azienda/Ditta"])
        if cliente and cliente.get("tipo_cliente") == "azienda":
            self.tipo_cliente.setCurrentIndex(1)

        self.tipo_cliente.currentIndexChanged.connect(self.aggiorna_campi_visibili)

        self.nome = QLineEdit(cliente.get("nome") if cliente else "")
        self.cognome = QLineEdit(cliente.get("cognome") if cliente else "")
        self.ragione_sociale = QLineEdit(cliente.get("ragione_sociale") if cliente else "")
        self.referente_nome = QLineEdit(cliente.get("referente_nome") if cliente else "")
        self.referente_cognome = QLineEdit(cliente.get("referente_cognome") if cliente else "")
        self.telefono = QLineEdit(cliente.get("telefono") if cliente else "")
        self.email = QLineEdit(cliente.get("email") if cliente else "")
        self.indirizzo = QLineEdit(cliente.get("indirizzo") if cliente else "")
        self.codice_fiscale = QLineEdit(cliente.get("codice_fiscale") if cliente else "")
        self.partita_iva = QLineEdit(cliente.get("partita_iva") if cliente else "")
        self.note = QTextEdit(cliente.get("note") if cliente else "")

        dati_layout.addRow("Tipo Cliente:", self.tipo_cliente)
        dati_layout.addRow("Nome:", self.nome)
        dati_layout.addRow("Cognome:", self.cognome)
        dati_layout.addRow("Ragione Sociale:", self.ragione_sociale)
        dati_layout.addRow("Referente Nome:", self.referente_nome)
        dati_layout.addRow("Referente Cognome:", self.referente_cognome)
        dati_layout.addRow("Telefono:", self.telefono)
        dati_layout.addRow("Email:", self.email)
        dati_layout.addRow("Indirizzo:", self.indirizzo)
        dati_layout.addRow("Codice Fiscale:", self.codice_fiscale)
        dati_layout.addRow("Partita IVA:", self.partita_iva)
        dati_layout.addRow("Note:", self.note)
        self.tab_dati.setLayout(dati_layout)

        # --- TAB OFFERTE ---
        self.offerte_list = QListWidget()
        offerte = cliente.get("offerte", []) if cliente else []
        for off in offerte:
            item = QListWidgetItem(f"{off['data']} | {off['descrizione']} | {off['importo']} € | {off['stato']}")
            item.setData(Qt.UserRole, off)
            self.offerte_list.addItem(item)
        offerte_layout = QVBoxLayout()
        offerte_layout.addWidget(self.offerte_list)
        btn_off_layout = QHBoxLayout()
        btn_add_off = QPushButton("Aggiungi Offerta")
        btn_edit_off = QPushButton("Modifica Offerta")
        btn_del_off = QPushButton("Elimina Offerta")
        btn_off_layout.addWidget(btn_add_off)
        btn_off_layout.addWidget(btn_edit_off)
        btn_off_layout.addWidget(btn_del_off)
        offerte_layout.addLayout(btn_off_layout)
        self.tab_offerte.setLayout(offerte_layout)
        btn_add_off.clicked.connect(self.add_offerta)
        btn_edit_off.clicked.connect(self.edit_offerta)
        btn_del_off.clicked.connect(self.del_offerta)

        # --- TAB STORICO ---
        self.storico_list = QListWidget()
        storico = cliente.get("storico", []) if cliente else []
        for ev in storico:
            item = QListWidgetItem(f"{ev['data']} | {ev['tipo']} | {ev['descrizione']}")
            item.setData(Qt.UserRole, ev)
            self.storico_list.addItem(item)
        storico_layout = QVBoxLayout()
        storico_layout.addWidget(self.storico_list)
        btn_storico_layout = QHBoxLayout()
        btn_add_storico = QPushButton("Aggiungi Nota")
        btn_del_storico = QPushButton("Elimina Nota")
        btn_storico_layout.addWidget(btn_add_storico)
        btn_storico_layout.addWidget(btn_del_storico)
        storico_layout.addLayout(btn_storico_layout)
        self.tab_storico.setLayout(storico_layout)
        btn_add_storico.clicked.connect(self.add_storico)
        btn_del_storico.clicked.connect(self.del_storico)

        # --- TAB ALLEGATI ---
        self.allegati_list = QListWidget()
        allegati = cliente.get("allegati", []) if cliente else []
        for a in allegati:
            item = QListWidgetItem(f"{a['nome']} ({a['data']})")
            item.setData(Qt.UserRole, a)
            self.allegati_list.addItem(item)
        allegati_layout = QVBoxLayout()
        allegati_layout.addWidget(self.allegati_list)
        btn_allegati_layout = QHBoxLayout()
        btn_add_allegato = QPushButton("Aggiungi Allegato")
        btn_view_allegato = QPushButton("Apri Allegato")
        btn_del_allegato = QPushButton("Elimina Allegato")
        btn_allegati_layout.addWidget(btn_add_allegato)
        btn_allegati_layout.addWidget(btn_view_allegato)
        btn_allegati_layout.addWidget(btn_del_allegato)
        allegati_layout.addLayout(btn_allegati_layout)
        self.tab_allegati.setLayout(allegati_layout)
        btn_add_allegato.clicked.connect(self.add_allegato)
        btn_view_allegato.clicked.connect(self.open_allegato)
        btn_del_allegato.clicked.connect(self.del_allegato)

        # --- BOTTOM BUTTONS ---
        bottom_layout = QHBoxLayout()
        btn_save = QPushButton("Salva")
        btn_pdf = QPushButton("Stampa PDF")
        btn_cancel = QPushButton("Annulla")
        bottom_layout.addWidget(btn_save)
        bottom_layout.addWidget(btn_pdf)
        bottom_layout.addWidget(btn_cancel)
        dlg_layout.addLayout(bottom_layout)

        btn_save.clicked.connect(self.on_accept)
        btn_cancel.clicked.connect(self.reject)
        btn_pdf.clicked.connect(self.stampa_pdf)

        self.aggiorna_campi_visibili()

    def aggiorna_campi_visibili(self):
        tipo = self.tipo_cliente.currentIndex()
        self.nome.parentWidget().setVisible(tipo == 0)
        self.cognome.parentWidget().setVisible(tipo == 0)
        self.ragione_sociale.parentWidget().setVisible(tipo == 1)
        self.referente_nome.parentWidget().setVisible(tipo == 1)
        self.referente_cognome.parentWidget().setVisible(tipo == 1)

    def on_accept(self):
        errors = []
        tipo = self.tipo_cliente.currentIndex()
        if tipo == 0:
            if not self.nome.text().strip():
                errors.append("Il nome è obbligatorio.")
            if not self.cognome.text().strip():
                errors.append("Il cognome è obbligatorio.")
        else:
            if not self.ragione_sociale.text().strip():
                errors.append("La ragione sociale è obbligatoria.")
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
        tipo = self.tipo_cliente.currentIndex()
        base = {
            "tipo_cliente": "persona" if tipo == 0 else "azienda",
            "nome": self.nome.text().strip() if tipo == 0 else "",
            "cognome": self.cognome.text().strip() if tipo == 0 else "",
            "ragione_sociale": self.ragione_sociale.text().strip() if tipo == 1 else "",
            "referente_nome": self.referente_nome.text().strip() if tipo == 1 else "",
            "referente_cognome": self.referente_cognome.text().strip() if tipo == 1 else "",
            "telefono": self.telefono.text().strip(),
            "email": self.email.text().strip(),
            "indirizzo": self.indirizzo.text().strip(),
            "codice_fiscale": self.codice_fiscale.text().strip().upper(),
            "partita_iva": self.partita_iva.text().strip(),
            "note": self.note.toPlainText().strip(),
            "offerte": [],
            "storico": [],
            "allegati": []
        }
        base["offerte"] = []
        for i in range(self.offerte_list.count()):
            base["offerte"].append(self.offerte_list.item(i).data(Qt.UserRole))
        base["storico"] = []
        for i in range(self.storico_list.count()):
            base["storico"].append(self.storico_list.item(i).data(Qt.UserRole))
        base["allegati"] = []
        for i in range(self.allegati_list.count()):
            base["allegati"].append(self.allegati_list.item(i).data(Qt.UserRole))
        return base

    # --- GESTIONE OFFERTE ---
    def add_offerta(self):
        data, ok1 = QInputDialog.getText(self, "Data offerta", "Data (YYYY-MM-DD):", text=now_str().split()[0])
        if not ok1 or not data.strip():
            return
        descrizione, ok2 = QInputDialog.getText(self, "Descrizione offerta", "Descrizione:")
        if not ok2 or not descrizione.strip():
            return
        importo, ok3 = QInputDialog.getDouble(self, "Importo offerta", "Importo (€):", 0, 0, 1000000, 2)
        if not ok3:
            return
        stato, ok4 = QInputDialog.getItem(self, "Stato offerta", "Stato:", ["Inviata", "Accettata", "Rifiutata", "Scaduta"], 0, False)
        if not ok4:
            return
        off = {
            "data": data.strip(),
            "descrizione": descrizione.strip(),
            "importo": str(importo),
            "stato": stato
        }
        item = QListWidgetItem(f"{off['data']} | {off['descrizione']} | {off['importo']} € | {off['stato']}")
        item.setData(Qt.UserRole, off)
        self.offerte_list.addItem(item)
        ev = {
            "data": now_str(),
            "tipo": "offerta",
            "descrizione": f"Offerta '{descrizione.strip()}' inserita ({stato})."
        }
        item_ev = QListWidgetItem(f"{ev['data']} | {ev['tipo']} | {ev['descrizione']}")
        item_ev.setData(Qt.UserRole, ev)
        self.storico_list.addItem(item_ev)

    def edit_offerta(self):
        row = self.offerte_list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona un'offerta da modificare.")
            return
        off = self.offerte_list.item(row).data(Qt.UserRole)
        data, ok1 = QInputDialog.getText(self, "Data offerta", "Data (YYYY-MM-DD):", text=off["data"])
        if not ok1 or not data.strip():
            return
        descrizione, ok2 = QInputDialog.getText(self, "Descrizione offerta", "Descrizione:", text=off["descrizione"])
        if not ok2 or not descrizione.strip():
            return
        importo, ok3 = QInputDialog.getDouble(self, "Importo offerta", "Importo (€):", float(off["importo"]), 0, 1000000, 2)
        if not ok3:
            return
        stato, ok4 = QInputDialog.getItem(self, "Stato offerta", "Stato:", ["Inviata", "Accettata", "Rifiutata", "Scaduta"], ["Inviata", "Accettata", "Rifiutata", "Scaduta"].index(off["stato"]), False)
        if not ok4:
            return
        new_off = {
            "data": data.strip(),
            "descrizione": descrizione.strip(),
            "importo": str(importo),
            "stato": stato
        }
        item = QListWidgetItem(f"{new_off['data']} | {new_off['descrizione']} | {new_off['importo']} € | {new_off['stato']}")
        item.setData(Qt.UserRole, new_off)
        self.offerte_list.takeItem(row)
        self.offerte_list.insertItem(row, item)
        ev = {
            "data": now_str(),
            "tipo": "offerta",
            "descrizione": f"Offerta '{descrizione.strip()}' modificata ({stato})."
        }
        item_ev = QListWidgetItem(f"{ev['data']} | {ev['tipo']} | {ev['descrizione']}")
        item_ev.setData(Qt.UserRole, ev)
        self.storico_list.addItem(item_ev)

    def del_offerta(self):
        row = self.offerte_list.currentRow()
        if row < 0:
            return
        off = self.offerte_list.item(row).data(Qt.UserRole)
        descr = off["descrizione"]
        self.offerte_list.takeItem(row)
        ev = {
            "data": now_str(),
            "tipo": "offerta",
            "descrizione": f"Offerta '{descr}' eliminata."
        }
        item_ev = QListWidgetItem(f"{ev['data']} | {ev['tipo']} | {ev['descrizione']}")
        item_ev.setData(Qt.UserRole, ev)
        self.storico_list.addItem(item_ev)

    # --- GESTIONE STORICO ---
    def add_storico(self):
        testo, ok = QInputDialog.getMultiLineText(self, "Nota storico", "Descrizione:")
        if not ok or not testo.strip():
            return
        ev = {
            "data": now_str(),
            "tipo": "nota",
            "descrizione": testo.strip()
        }
        item = QListWidgetItem(f"{ev['data']} | {ev['tipo']} | {ev['descrizione']}")
        item.setData(Qt.UserRole, ev)
        self.storico_list.addItem(item)

    def del_storico(self):
        row = self.storico_list.currentRow()
        if row >= 0:
            self.storico_list.takeItem(row)

    # --- GESTIONE ALLEGATI ---
    def add_allegato(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleziona allegato", "", "Documenti (*.pdf *.doc *.docx *.jpg *.png *.jpeg *.txt);;Tutti i file (*)")
        if not path:
            return
        nome = os.path.basename(path)
        dest = os.path.join(ALLEGATI_DIR, f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{nome}")
        try:
            with open(path, "rb") as src, open(dest, "wb") as dst:
                dst.write(src.read())
            allegato = {
                "nome": nome,
                "percorso": dest,
                "data": now_str()
            }
            item = QListWidgetItem(f"{allegato['nome']} ({allegato['data']})")
            item.setData(Qt.UserRole, allegato)
            self.allegati_list.addItem(item)
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore nel salvataggio allegato: {e}")

    def open_allegato(self):
        row = self.allegati_list.currentRow()
        if row < 0:
            return
        allegato = self.allegati_list.item(row).data(Qt.UserRole)
        path = allegato["percorso"]
        if os.path.exists(path):
            os.startfile(path)
        else:
            QMessageBox.warning(self, "Errore", f"File non trovato: {path}")

    def del_allegato(self):
        row = self.allegati_list.currentRow()
        if row < 0:
            return
        allegato = self.allegati_list.item(row).data(Qt.UserRole)
        path = allegato["percorso"]
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass
        self.allegati_list.takeItem(row)

    # --- STAMPA PDF ---
    def stampa_pdf(self):
        try:
            from fpdf import FPDF
        except ImportError:
            QMessageBox.warning(self, "PDF", "Installare il modulo fpdf (`pip install fpdf`) per usare questa funzione.")
            return
        cliente = self.get_data()
        path, _ = QFileDialog.getSaveFileName(self, "Salva PDF scheda cliente", f"{cliente.get('ragione_sociale') or cliente.get('cognome') or 'cliente'}.pdf", "File PDF (*.pdf)")
        if not path:
            return
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "", 14)
        pdf.cell(0, 10, "Scheda Cliente", ln=1, align="C")
        pdf.set_font("Arial", "", 11)
        for key, label in [
            ("tipo_cliente", "Tipo Cliente"),
            ("nome", "Nome"),
            ("cognome", "Cognome"),
            ("ragione_sociale", "Ragione Sociale"),
            ("referente_nome", "Referente Nome"),
            ("referente_cognome", "Referente Cognome"),
            ("telefono", "Telefono"),
            ("email", "Email"),
            ("indirizzo", "Indirizzo"),
            ("codice_fiscale", "Codice Fiscale"),
            ("partita_iva", "Partita IVA"),
            ("note", "Note")
        ]:
            val = cliente.get(key, "")
            if val:
                pdf.cell(0, 7, f"{label}: {val}", ln=1)
        pdf.ln(3)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Offerte", ln=1)
        pdf.set_font("Arial", "", 10)
        for off in cliente.get("offerte", []):
            pdf.cell(0, 6, f"{off['data']} | {off['descrizione']} | {off['importo']} € | {off['stato']}", ln=1)
        pdf.ln(2)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Storico", ln=1)
        pdf.set_font("Arial", "", 10)
        for ev in cliente.get("storico", []):
            pdf.cell(0, 6, f"{ev['data']} | {ev['tipo']} | {ev['descrizione']}", ln=1)
        try:
            pdf.output(path)
            QMessageBox.information(self, "PDF", f"PDF creato:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "PDF", f"Errore nella creazione PDF: {e}")

class ClientiWindow(QWidget):
    COLS = [
        "Tipo", "Nome/Ragione Sociale", "Cognome", "Telefono", "Email", "Partita IVA", "Codice Fiscale", "Note"
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestione Clienti")
        self.resize(1150, 520)
        ensure_data_dir()
        self.clienti = self.load_clienti()
        self.filtrati = self.clienti.copy()

        main_layout = QVBoxLayout(self)

        # Barra di ricerca
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Cerca (nome, ragione sociale, cognome, email, CF, P.IVA, note)...")
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
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        main_layout.addWidget(self.table)

        # Pulsanti
        btn_layout = QHBoxLayout()
        self.btn_nuovo = QPushButton("Nuovo")
        self.btn_modifica = QPushButton("Modifica")
        self.btn_elimina = QPushButton("Elimina")
        self.btn_salva = QPushButton("Salva su file")
        self.btn_export = QPushButton("Esporta CSV")
        self.btn_copia = QPushButton("Copia dati cliente")
        btn_layout.addWidget(self.btn_nuovo)
        btn_layout.addWidget(self.btn_modifica)
        btn_layout.addWidget(self.btn_elimina)
        btn_layout.addWidget(self.btn_salva)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_copia)
        main_layout.addLayout(btn_layout)

        self.btn_nuovo.clicked.connect(self.nuovo_cliente)
        self.btn_modifica.clicked.connect(self.modifica_cliente)
        self.btn_elimina.clicked.connect(self.elimina_cliente)
        self.btn_salva.clicked.connect(self.salva_clienti)
        self.btn_export.clicked.connect(self.esporta_csv)
        self.btn_copia.clicked.connect(self.copia_dati_cliente)

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
        def testo_cliente(c):
            return " ".join([
                c.get("tipo_cliente", ""),
                c.get("nome", ""),
                c.get("ragione_sociale", ""),
                c.get("cognome", ""),
                c.get("telefono", ""),
                c.get("email", ""),
                c.get("indirizzo", ""),
                c.get("codice_fiscale", ""),
                c.get("partita_iva", ""),
                c.get("note", "")
            ]).lower()
        if filtro:
            self.filtrati = [c for c in self.clienti if filtro in testo_cliente(c)]
        else:
            self.filtrati = self.clienti.copy()
        self._aggiorna_tabella_filtrata()

    def _aggiorna_tabella_filtrata(self):
        self.table.setRowCount(len(self.filtrati))
        for row, c in enumerate(self.filtrati):
            tipo = "Azienda" if c.get("tipo_cliente") == "azienda" else "Persona"
            nome_rs = c.get("ragione_sociale") if c.get("tipo_cliente") == "azienda" else c.get("nome")
            self.table.setItem(row, 0, QTableWidgetItem(tipo))
            self.table.setItem(row, 1, QTableWidgetItem(nome_rs or ""))
            self.table.setItem(row, 2, QTableWidgetItem(c.get("cognome", "")))
            self.table.setItem(row, 3, QTableWidgetItem(c.get("telefono", "")))
            self.table.setItem(row, 4, QTableWidgetItem(c.get("email", "")))
            self.table.setItem(row, 5, QTableWidgetItem(c.get("partita_iva", "")))
            self.table.setItem(row, 6, QTableWidgetItem(c.get("codice_fiscale", "")))
            note = c.get("note", "").replace("\n", " | ")
            self.table.setItem(row, 7, QTableWidgetItem(note))

    def get_selected_cliente_global_index(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.filtrati):
            return None
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

    def esporta_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Esporta elenco clienti CSV", "", "CSV files (*.csv)")
        if not path:
            return
        try:
            with open(path, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.COLS)
                for c in self.filtrati:
                    tipo = "Azienda" if c.get("tipo_cliente") == "azienda" else "Persona"
                    nome_rs = c.get("ragione_sociale") if c.get("tipo_cliente") == "azienda" else c.get("nome")
                    writer.writerow([
                        tipo,
                        nome_rs or "",
                        c.get("cognome", ""),
                        c.get("telefono", ""),
                        c.get("email", ""),
                        c.get("partita_iva", ""),
                        c.get("codice_fiscale", ""),
                        c.get("note", "").replace("\n", " | ")
                    ])
            QMessageBox.information(self, "Esporta", f"Esportazione completata:\n{path}")
        except Exception as e:
            QMessageBox.warning(self, "Errore", f"Errore durante l'esportazione: {e}")

    def copia_dati_cliente(self):
        idx = self.get_selected_cliente_global_index()
        if idx is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona un cliente da copiare.")
            return
        c = self.clienti[idx]
        tipo = "Azienda" if c.get("tipo_cliente") == "azienda" else "Persona"
        nome_rs = c.get("ragione_sociale") if c.get("tipo_cliente") == "azienda" else c.get("nome")
        text = "\n".join([
            f"Tipo: {tipo}",
            f"Nome/Ragione Sociale: {nome_rs or ''}",
            f"Cognome: {c.get('cognome', '')}",
            f"Telefono: {c.get('telefono', '')}",
            f"Email: {c.get('email', '')}",
            f"Partita IVA: {c.get('partita_iva', '')}",
            f"Codice Fiscale: {c.get('codice_fiscale', '')}",
            f"Note: {c.get('note', '')}"
        ])
        clipboard = QApplication.instance().clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "Copia", "Dati cliente copiati negli appunti.")
