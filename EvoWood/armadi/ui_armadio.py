import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QComboBox,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QSpinBox, QFormLayout, QDialog, QDialogButtonBox
)
from .models import Armadio, Modulo, Vano, Anta, Materiale, Cassetto, Accessorio

# Catalogo fittizio materiali e accessori (demo)
MATERIALI = [
    Materiale("Melaminico Bianco", "Pannello nobilitato bianco"),
    Materiale("Rovere Naturale", "Imitazione legno rovere"),
    Materiale("Vetro Satinato", "Vetro per ante scorrevoli"),
]
ACCESSORI = [
    Accessorio("Maniglia Inox", "maniglia"),
    Accessorio("Appendiabiti Estraibile", "ferramenta"),
    Accessorio("Luce LED interna", "elettrico"),
]

class ModuloDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aggiungi Modulo")
        self.setMinimumWidth(400)
        self.nome = QLineEdit("Modulo")
        self.larghezza = QSpinBox()
        self.larghezza.setRange(20, 120)
        self.larghezza.setValue(60)
        self.altezza = QSpinBox()
        self.altezza.setRange(120, 300)
        self.altezza.setValue(250)
        self.profondita = QSpinBox()
        self.profondita.setRange(30, 80)
        self.profondita.setValue(60)
        self.materiale = QComboBox()
        for m in MATERIALI:
            self.materiale.addItem(m.nome)
        # Vani, ante, cassetti
        self.n_vani = QSpinBox(); self.n_vani.setRange(1, 5); self.n_vani.setValue(1)
        self.n_ante = QSpinBox(); self.n_ante.setRange(0, 4); self.n_ante.setValue(1)
        self.n_cassetti = QSpinBox(); self.n_cassetti.setRange(0, 5); self.n_cassetti.setValue(0)
        form = QFormLayout()
        form.addRow("Nome modulo:", self.nome)
        form.addRow("Larghezza (cm):", self.larghezza)
        form.addRow("Altezza (cm):", self.altezza)
        form.addRow("Profondità (cm):", self.profondita)
        form.addRow("Materiale:", self.materiale)
        form.addRow("N° Vani:", self.n_vani)
        form.addRow("N° Ante:", self.n_ante)
        form.addRow("N° Cassetti:", self.n_cassetti)
        self.btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.btns)
        self.setLayout(layout)

    def get_modulo(self):
        mat = MATERIALI[self.materiale.currentIndex()]
        vani = [Vano(self.larghezza.value(), self.altezza.value(), self.profondita.value()) for _ in range(self.n_vani.value())]
        ante = [Anta("piena", mat, self.altezza.value(), self.larghezza.value() // max(1, self.n_ante.value())) for _ in range(self.n_ante.value())]
        cassetti = [Cassetto(self.larghezza.value(), 20, self.profondita.value(), mat) for _ in range(self.n_cassetti.value())]
        return Modulo(
            larghezza=self.larghezza.value(),
            altezza=self.altezza.value(),
            profondita=self.profondita.value(),
            vani=vani, ante=ante, cassetti=cassetti,
            materiale=mat, nome=self.nome.text() or "Modulo"
        )

class AccessorioDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aggiungi Accessorio")
        self.combo = QComboBox()
        for acc in ACCESSORI:
            self.combo.addItem(f"{acc.nome} ({acc.categoria})")
        self.btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addWidget(self.combo)
        layout.addWidget(self.btns)
        self.setLayout(layout)
    def get_accessorio(self):
        return ACCESSORI[self.combo.currentIndex()]

class ArmadioDesigner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progettazione Armadio Avanzata - EvoWood")
        self.setMinimumSize(700, 500)
        self.armadio = None
        self.moduli = []
        self.accessori = []

        self.tabs = QTabWidget()
        # Tab Dati Generali
        self.tab_generali = QWidget()
        gen_layout = QFormLayout()
        self.nome = QLineEdit("Armadio su misura")
        self.note = QTextEdit()
        gen_layout.addRow("Nome Armadio:", self.nome)
        gen_layout.addRow("Note:", self.note)
        self.tab_generali.setLayout(gen_layout)
        # Tab Moduli
        self.tab_moduli = QWidget()
        mod_layout = QVBoxLayout()
        self.lista_moduli = QListWidget()
        self.btn_aggiungi_modulo = QPushButton("Aggiungi Modulo")
        self.btn_rimuovi_modulo = QPushButton("Rimuovi Modulo selezionato")
        self.btn_aggiungi_modulo.clicked.connect(self.add_modulo)
        self.btn_rimuovi_modulo.clicked.connect(self.remove_modulo)
        btns_mod = QHBoxLayout()
        btns_mod.addWidget(self.btn_aggiungi_modulo)
        btns_mod.addWidget(self.btn_rimuovi_modulo)
        mod_layout.addWidget(self.lista_moduli)
        mod_layout.addLayout(btns_mod)
        self.tab_moduli.setLayout(mod_layout)
        # Tab Accessori
        self.tab_accessori = QWidget()
        acc_layout = QVBoxLayout()
        self.lista_accessori = QListWidget()
        self.btn_aggiungi_acc = QPushButton("Aggiungi Accessorio")
        self.btn_rimuovi_acc = QPushButton("Rimuovi Accessorio selezionato")
        self.btn_aggiungi_acc.clicked.connect(self.add_accessorio)
        self.btn_rimuovi_acc.clicked.connect(self.remove_accessorio)
        btns_acc = QHBoxLayout()
        btns_acc.addWidget(self.btn_aggiungi_acc)
        btns_acc.addWidget(self.btn_rimuovi_acc)
        acc_layout.addWidget(self.lista_accessori)
        acc_layout.addLayout(btns_acc)
        self.tab_accessori.setLayout(acc_layout)
        # Tab Anteprima
        self.tab_anteprima = QWidget()
        ante_layout = QVBoxLayout()
        self.btn_aggiorna = QPushButton("Aggiorna Anteprima")
        self.ante_box = QTextEdit()
        self.ante_box.setReadOnly(True)
        ante_layout.addWidget(self.btn_aggiorna)
        ante_layout.addWidget(self.ante_box)
        self.btn_aggiorna.clicked.connect(self.aggiorna_anteprima)
        self.tab_anteprima.setLayout(ante_layout)
        # Aggiungi tabs
        self.tabs.addTab(self.tab_generali, "Dati Generali")
        self.tabs.addTab(self.tab_moduli, "Moduli")
        self.tabs.addTab(self.tab_accessori, "Accessori")
        self.tabs.addTab(self.tab_anteprima, "Anteprima")
        # Layout principale
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def add_modulo(self):
        dlg = ModuloDialog(self)
        if dlg.exec_():
            modulo = dlg.get_modulo()
            self.moduli.append(modulo)
            self.lista_moduli.addItem(f"{modulo.nome} ({modulo.larghezza}x{modulo.altezza}x{modulo.profondita})")

    def remove_modulo(self):
        row = self.lista_moduli.currentRow()
        if row >= 0:
            self.moduli.pop(row)
            self.lista_moduli.takeItem(row)

    def add_accessorio(self):
        dlg = AccessorioDialog(self)
        if dlg.exec_():
            acc = dlg.get_accessorio()
            self.accessori.append(acc)
            self.lista_accessori.addItem(f"{acc.nome} ({acc.categoria})")

    def remove_accessorio(self):
        row = self.lista_accessori.currentRow()
        if row >= 0:
            self.accessori.pop(row)
            self.lista_accessori.takeItem(row)

    def aggiorna_anteprima(self):
        nome = self.nome.text().strip()
        note = self.note.toPlainText().strip()
        if not self.moduli:
            self.ante_box.setPlainText("Aggiungi almeno un modulo.")
            return
        self.armadio = Armadio(nome, self.moduli, self.accessori, note)
        # Placeholder IA: qui puoi aggiungere suggerimenti automatici o verifica errori
        self.ante_box.setPlainText(self.armadio.descrizione_dettagliata())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    aw = ArmadioDesigner()
    aw.show()
    sys.exit(app.exec_())
