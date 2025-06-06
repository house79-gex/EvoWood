import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel,
    QMessageBox, QInputDialog, QHBoxLayout
)
from .models import Armadio, FormaPersonalizzata
from .crud import ArmadioCRUD
from .cad import apri_in_cad
from .ia import suggerisci_configurazione_armadio
from .componenti import aggiungi_componente
from .services import esporta_armadi_csv

class ArmadiWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestione Armadi")
        self.crud = ArmadioCRUD()
        self.init_ui()
        self.aggiorna_lista()

    def init_ui(self):
        layout = QVBoxLayout()
        self.lista = QListWidget()
        layout.addWidget(QLabel("Lista Armadi"))
        layout.addWidget(self.lista)

        btn_layout = QHBoxLayout()
        btn_nuovo = QPushButton("Nuovo parametrico")
        btn_nuovo_ia = QPushButton("Nuovo da descrizione (IA)")
        btn_elimina = QPushButton("Elimina Armadio")
        btn_cad = QPushButton("Apri in CAD")
        btn_csv = QPushButton("Esporta CSV")
        btn_componenti = QPushButton("Componenti")

        btn_nuovo.clicked.connect(self.nuovo_armadio_parametrico)
        btn_nuovo_ia.clicked.connect(self.nuovo_armadio_da_descrizione)
        btn_elimina.clicked.connect(self.elimina_armadio)
        btn_cad.clicked.connect(self.apri_cad)
        btn_csv.clicked.connect(self.esporta_csv)
        btn_componenti.clicked.connect(self.mostra_componenti)

        btn_layout.addWidget(btn_nuovo)
        btn_layout.addWidget(btn_nuovo_ia)
        btn_layout.addWidget(btn_elimina)
        btn_layout.addWidget(btn_cad)
        btn_layout.addWidget(btn_csv)
        btn_layout.addWidget(btn_componenti)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def aggiorna_lista(self):
        self.lista.clear()
        for a in self.crud.armadi:
            forma_str = f" ({a.forma.tipo})"
            self.lista.addItem(f"{a.id} - {a.nome}{forma_str}")

    def nuovo_armadio_parametrico(self):
        nome, ok = QInputDialog.getText(self, "Nuovo Parametrico", "Nome:")
        if not (ok and nome): return
        # Parametri base, in futuro dialog avanzato
        larghezza, ok1 = QInputDialog.getInt(self, "Larghezza", "Larghezza (cm):", 250, 40, 1000)
        if not ok1: return
        altezza, ok2 = QInputDialog.getInt(self, "Altezza", "Altezza (cm):", 260, 180, 350)
        if not ok2: return
        profondita, ok3 = QInputDialog.getInt(self, "Profondità", "Profondità (cm):", 60, 20, 120)
        if not ok3: return
        forma = FormaPersonalizzata("rettangolare", {"larghezza": larghezza, "altezza": altezza, "profondità": profondita})
        armadio = Armadio(
            id=len(self.crud.armadi)+1,
            nome=nome,
            cliente=None,
            progetto=None,
            forma=forma,
        )
        self.crud.aggiungi(armadio)
        self.aggiorna_lista()

    def nuovo_armadio_da_descrizione(self):
        desc, ok = QInputDialog.getText(self, "Nuovo Armadio da Descrizione", "Descrizione:")
        if ok and desc:
            armadio_ia = suggerisci_configurazione_armadio(desc)
            self.crud.aggiungi(armadio_ia)
            self.aggiorna_lista()

    def elimina_armadio(self):
        selected = self.lista.currentRow()
        if selected >= 0:
            armadio = self.crud.armadi[selected]
            self.crud.elimina(armadio.id)
            self.aggiorna_lista()
        else:
            QMessageBox.warning(self, "Seleziona", "Seleziona un armadio da eliminare.")

    def apri_cad(self):
        selected = self.lista.currentRow()
        if selected >= 0:
            armadio = self.crud.armadi[selected]
            apri_in_cad(armadio)
        else:
            QMessageBox.warning(self, "Seleziona", "Seleziona un armadio per aprirlo nel CAD.")

    def esporta_csv(self):
        esporta_armadi_csv(self.crud.armadi)
        QMessageBox.information(self, "Esportazione CSV", "Esportazione completata.")

    def mostra_componenti(self):
        selected = self.lista.currentRow()
        if selected >= 0:
            armadio = self.crud.armadi[selected]
            if not armadio.componenti:
                msg = "Nessun componente."
            else:
                msg = "\n".join([f"{c.nome} ({c.tipo})" for c in armadio.componenti])
            QMessageBox.information(self, "Componenti", msg)
        else:
            QMessageBox.warning(self, "Seleziona", "Seleziona un armadio per vedere i componenti.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ArmadiWindow()
    win.show()
    sys.exit(app.exec_())
