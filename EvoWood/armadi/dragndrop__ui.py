import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QColorDialog, QPushButton, QHBoxLayout,
    QInputDialog, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QColor, QBrush

from .models import Armadio, Componente, Materiale, FormaPersonalizzata
from .crud import ArmadioCRUD

COMPONENTI_COLORI = {
    "Fianco": "#F6B26B",
    "Fondo": "#B6D7A8",
    "Zoccolo": "#A4C2F4",
    "Anta": "#FFD966",
    "Ripiano": "#D9D2E9",
}

class ComponentiPalette(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(120)
        for nome in COMPONENTI_COLORI.keys():
            item = QListWidgetItem(nome)
            item.setData(Qt.UserRole, nome)
            self.addItem(item)
        self.setStyleSheet("background: #FDEEC6; border-radius: 7px; font-weight: bold;")

class ComponentGraphicsItem(QGraphicsRectItem):
    def __init__(self, comp: Componente):
        super().__init__(0, 0, comp.dimensioni.get("larghezza", 40), comp.dimensioni.get("altezza", 100))
        self.componente = comp
        self.setBrush(QBrush(QColor(COMPONENTI_COLORI.get(comp.tipo, "#FFF"))))
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.setToolTip(f"{comp.nome} ({comp.tipo})")

    def aggiorna_dimensioni(self):
        self.setRect(0, 0, self.componente.dimensioni.get("larghezza", 40), self.componente.dimensioni.get("altezza", 100))
        self.update()

class ArmadioScene(QGraphicsScene):
    def __init__(self, armadio: Armadio):
        super().__init__()
        self.armadio = armadio
        self.setBackgroundBrush(QColor("#FFF5E0"))  # Colore caldo chiaro
        self.sync_grafica()

    def sync_grafica(self):
        self.clear()
        for comp in self.armadio.componenti:
            item = ComponentGraphicsItem(comp)
            pos = comp.posizione or {}
            item.setPos(pos.get("x", 0), pos.get("y", 0))
            self.addItem(item)

    def aggiungi_componente(self, nome, pos_scene: QPointF = None):
        idx = len(self.armadio.componenti) + 1
        materiale = Materiale(nome="Melaminico", codice="MEL001", descrizione="Bianco", prezzo=25)
        comp = Componente(
            nome=f"{nome} {idx}",
            tipo=nome,
            materiale=materiale,
            dimensioni={"larghezza": 40, "altezza": 100, "spessore": 2},
            posizione={}
        )
        if pos_scene:
            comp.posizione = {"x": pos_scene.x(), "y": pos_scene.y()}
        self.armadio.componenti.append(comp)
        item = ComponentGraphicsItem(comp)
        if pos_scene:
            item.setPos(pos_scene)
        self.addItem(item)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # Aggiorna posizione componente dopo spostamento
        for item in self.selectedItems():
            if isinstance(item, ComponentGraphicsItem):
                pos = item.scenePos()
                item.componente.posizione = {"x": pos.x(), "y": pos.y()}

    def dragEnterEvent(self, event): event.accept()
    def dragMoveEvent(self, event): event.accept()
    def dropEvent(self, event):
        nome = event.mimeData().text()
        if nome:
            pos = self.views()[0].mapToScene(event.pos())
            self.aggiungi_componente(nome, pos)
        event.accept()

class ArmadioView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setAcceptDrops(True)
        self.setStyleSheet("border: 2px solid #BB7539; background: #FFF5E0;")

    def dragEnterEvent(self, event): event.accept()
    def dragMoveEvent(self, event): event.accept()
    def dropEvent(self, event): self.scene().dropEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progetta Armadio - EvoWood")
        self.setStyleSheet("background: #FFF5E0; color: #6C3D12; font-family: Segoe UI; font-size: 12pt;")
        self.resize(1100, 650)
        central = QWidget()
        layout = QHBoxLayout(central)

        # Dati armadio corrente
        self.crud = ArmadioCRUD()
        if self.crud.armadi:
            self.armadio = self.crud.armadi[-1]
        else:
            forma = FormaPersonalizzata("rettangolare", {"larghezza": 300, "altezza": 260, "profondità": 60})
            self.armadio = Armadio(id=1, nome="Armadio Drag&Drop", cliente=None, progetto=None, forma=forma)

        self.palette = ComponentiPalette()
        layout.addWidget(self.palette)

        self.scene = ArmadioScene(self.armadio)
        self.view = ArmadioView(self.scene)
        layout.addWidget(self.view, stretch=1)

        prop_panel = QVBoxLayout()
        self.btn_colore = QPushButton("Cambia colore selezione")
        self.btn_colore.setStyleSheet("background: #F6B26B; border-radius: 7px; padding: 7px;")
        self.btn_colore.clicked.connect(self.cambia_colore_selezione)
        prop_panel.addWidget(self.btn_colore)

        self.btn_dim = QPushButton("Cambia dimensioni selezione")
        self.btn_dim.setStyleSheet("background: #FFE599; border-radius: 7px; padding: 7px;")
        self.btn_dim.clicked.connect(self.cambia_dimensioni_selezione)
        prop_panel.addWidget(self.btn_dim)

        self.btn_salva = QPushButton("Salva armadio")
        self.btn_salva.setStyleSheet("background: #B6D7A8; border-radius: 7px; padding: 7px;")
        self.btn_salva.clicked.connect(self.salva_armadio)
        prop_panel.addWidget(self.btn_salva)

        self.btn_carica = QPushButton("Carica armadio")
        self.btn_carica.setStyleSheet("background: #A4C2F4; border-radius: 7px; padding: 7px;")
        self.btn_carica.clicked.connect(self.carica_armadio)
        prop_panel.addWidget(self.btn_carica)

        prop_panel.addStretch()
        layout.addLayout(prop_panel)

        self.setCentralWidget(central)
        self.palette.itemPressed.connect(self.drag_start)

    def drag_start(self, item):
        from PyQt5.QtCore import QMimeData
        from PyQt5.QtGui import QDrag
        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(item.text())
        drag.setMimeData(mime)
        drag.exec_(Qt.MoveAction)

    def cambia_colore_selezione(self):
        items = self.scene.selectedItems()
        if not items:
            return
        color = QColorDialog.getColor()
        if color.isValid():
            for item in items:
                item.setBrush(QBrush(color))

    def cambia_dimensioni_selezione(self):
        items = self.scene.selectedItems()
        if not items:
            return
        for item in items:
            if isinstance(item, ComponentGraphicsItem):
                larghezza, ok1 = QInputDialog.getInt(self, "Larghezza", "Larghezza (cm):", int(item.rect().width()), 1, 500)
                if not ok1: continue
                altezza, ok2 = QInputDialog.getInt(self, "Altezza", "Altezza (cm):", int(item.rect().height()), 1, 500)
                if not ok2: continue
                item.componente.dimensioni["larghezza"] = larghezza
                item.componente.dimensioni["altezza"] = altezza
                item.aggiorna_dimensioni()

    def salva_armadio(self):
        # Aggiorna tutte le posizioni dei componenti prima di salvare
        for item in self.scene.items():
            if isinstance(item, ComponentGraphicsItem):
                pos = item.scenePos()
                item.componente.posizione = {"x": pos.x(), "y": pos.y()}
        # Salva l'armadio
        self.crud.aggiungi(self.armadio)
        QMessageBox.information(self, "Salvataggio", "Armadio salvato!")

    def carica_armadio(self):
        path, _ = QFileDialog.getOpenFileName(self, "Carica armadio", "", "Armadi JSON (*.json)")
        if not path:
            return
        # Ricarica da file usando CRUD
        vecchio_path = self.crud.storage_path
        self.crud.storage_path = path
        self.crud.armadi = self.crud.carica()
        if self.crud.armadi:
            self.armadio = self.crud.armadi[-1]
            self.scene.armadio = self.armadio
            self.scene.sync_grafica()
            QMessageBox.information(self, "Caricamento", "Armadio caricato!")
        self.crud.storage_path = vecchio_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
