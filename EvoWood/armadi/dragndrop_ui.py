import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QColorDialog, QPushButton, QHBoxLayout,
    QInputDialog, QFileDialog, QMessageBox, QComboBox, QFrame, QListView
)
from PyQt5.QtCore import Qt, QRectF, QPointF, QSize
from PyQt5.QtGui import QColor, QBrush, QPen, QIcon, QPixmap

from .models import Armadio, Componente, Materiale, FormaPersonalizzata
from .crud import ArmadioCRUD
from .ia import suggerisci_configurazione_armadio

COMPONENTI_COLORI = {
    "Fianco": "#F6B26B",
    "Fondo": "#B6D7A8",
    "Zoccolo": "#A4C2F4",
    "Anta": "#FFD966",
    "Ripiano": "#D9D2E9",
}

FORME_PRESET = [
    ("Rettangolare", {"larghezza": 300, "altezza": 260, "profondità": 60}),
    ("Ad Angolo", {"larghezza_1": 150, "larghezza_2": 150, "altezza": 260, "profondità": 60}),
    ("Trapezio", {"base_maggiore": 200, "base_minore": 120, "altezza": 260, "profondità": 60}),
    ("Su misura", {}),
]

def palette_calda():
    return {
        "bg": "#FFF5E0",
        "panel": "#FDEEC6",
        "accent1": "#F6B26B",
        "accent2": "#FFD966",
        "accent3": "#A4C2F4",
        "accent4": "#B6D7A8",
        "accent5": "#D9D2E9",
        "text": "#6C3D12",
        "border": "#BB7539"
    }

class ComponentiPalette(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(120)
        for nome in COMPONENTI_COLORI.keys():
            item = QListWidgetItem(nome)
            item.setData(Qt.UserRole, nome)
            icon = QPixmap(24, 24)
            icon.fill(QColor(COMPONENTI_COLORI[nome]))
            item.setIcon(QIcon(icon))
            self.addItem(item)
        self.setStyleSheet("background: {}; border-radius: 7px; font-weight: bold;".format(palette_calda()["panel"]))

class ComponentGraphicsItem(QGraphicsRectItem):
    def __init__(self, comp: Componente, grid_size=10):
        super().__init__(0, 0, comp.dimensioni.get("larghezza", 40), comp.dimensioni.get("altezza", 100))
        self.componente = comp
        self.setBrush(QBrush(QColor(COMPONENTI_COLORI.get(comp.tipo, "#FFF"))))
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.setToolTip(f"{comp.nome} ({comp.tipo})")
        self.grid_size = grid_size

    def mouseReleaseEvent(self, event):
        # Snap a griglia alla fine del drag
        pos = self.scenePos()
        gs = self.grid_size
        snapped = QPointF(round(pos.x() / gs) * gs, round(pos.y() / gs) * gs)
        self.setPos(snapped)
        self.componente.posizione = {"x": snapped.x(), "y": snapped.y()}
        super().mouseReleaseEvent(event)

    def aggiorna_dimensioni(self):
        self.setRect(0, 0, self.componente.dimensioni.get("larghezza", 40), self.componente.dimensioni.get("altezza", 100))
        self.update()

class ArmadioScene(QGraphicsScene):
    def __init__(self, armadio: Armadio, grid_size=10):
        super().__init__()
        self.armadio = armadio
        self.grid_size = grid_size
        self.setBackgroundBrush(QColor(palette_calda()["bg"]))
        self.sync_grafica()

    def drawBackground(self, painter, rect):
        # Griglia
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        right = int(rect.right())
        bottom = int(rect.bottom())
        painter.save()
        pen = QPen(QColor("#F9D7B0"))
        pen.setWidth(1)
        painter.setPen(pen)
        for x in range(left, right, self.grid_size):
            painter.drawLine(x, top, x, bottom)
        for y in range(top, bottom, self.grid_size):
            painter.drawLine(left, y, right, y)
        painter.restore()

    def sync_grafica(self):
        self.clear()
        for comp in self.armadio.componenti:
            item = ComponentGraphicsItem(comp, self.grid_size)
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
        item = ComponentGraphicsItem(comp, self.grid_size)
        if pos_scene:
            item.setPos(pos_scene)
        self.addItem(item)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
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
            # Snap a griglia in drop
            gs = self.grid_size
            snapped = QPointF(round(pos.x() / gs) * gs, round(pos.y() / gs) * gs)
            self.aggiungi_componente(nome, snapped)
        event.accept()

class ArmadioView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setAcceptDrops(True)
        self.setStyleSheet("border: 2px solid {}; background: {};".format(palette_calda()["border"], palette_calda()["bg"]))

    def dragEnterEvent(self, event): event.accept()
    def dragMoveEvent(self, event): event.accept()
    def dropEvent(self, event): self.scene().dropEvent(event)

class ListaArmadiView(QListWidget):
    def __init__(self, crud: ArmadioCRUD):
        super().__init__()
        self.crud = crud
        self.setMinimumWidth(200)
        self.setViewMode(QListView.ListMode)
        self.refresh()

    def refresh(self):
        self.clear()
        for a in self.crud.armadi:
            item = QListWidgetItem(f"{a.id} - {a.nome} [{a.forma.tipo}]")
            self.addItem(item)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progetta Armadio - EvoWood")
        pal = palette_calda()
        self.setStyleSheet(f"background: {pal['bg']}; color: {pal['text']}; font-family: Segoe UI; font-size: 12pt;")
        self.resize(1100, 700)
        central = QWidget()
        layout = QHBoxLayout(central)

        # CRUD e lista armadi
        self.crud = ArmadioCRUD()
        if self.crud.armadi:
            self.armadio = self.crud.armadi[-1]
        else:
            forma = FormaPersonalizzata("rettangolare", {"larghezza": 300, "altezza": 260, "profondità": 60})
            self.armadio = Armadio(id=1, nome="Armadio Drag&Drop", cliente=None, progetto=None, forma=forma)
            self.crud.aggiungi(self.armadio)

        self.lista_armadi = ListaArmadiView(self.crud)
        self.lista_armadi.currentRowChanged.connect(self.cambia_armadio)
        layout.addWidget(self.lista_armadi)

        # Palette componenti
        palette_panel = QVBoxLayout()
        self.palette = ComponentiPalette()
        palette_panel.addWidget(QLabel("Componenti", alignment=Qt.AlignCenter))
        palette_panel.addWidget(self.palette)
        layout.addLayout(palette_panel)

        # Area lavoro 2D
        self.scene = ArmadioScene(self.armadio, grid_size=10)
        self.view = ArmadioView(self.scene)
        self.view.setFixedSize(600, 600)
        area_layout = QVBoxLayout()
        area_layout.addWidget(QLabel("Area di lavoro 2D", alignment=Qt.AlignCenter))
        area_layout.addWidget(self.view)
        area_layout.addWidget(QLabel("Modulo 3D non disponibile", alignment=Qt.AlignCenter))
        layout.addLayout(area_layout)

        # Pannello proprietà e azioni
        prop_panel = QVBoxLayout()
        prop_panel.addWidget(QLabel("Proprietà armadio", alignment=Qt.AlignCenter))
        self.combo_forma = QComboBox()
        for nome, _ in FORME_PRESET:
            self.combo_forma.addItem(nome)
        self.combo_forma.currentIndexChanged.connect(self.cambia_forma)
        prop_panel.addWidget(self.combo_forma)

        self.btn_colore = QPushButton("Cambia colore selezione")
        self.btn_colore.setStyleSheet(f"background: {pal['accent1']}; border-radius: 7px; padding: 7px;")
        self.btn_colore.clicked.connect(self.cambia_colore_selezione)
        prop_panel.addWidget(self.btn_colore)

        self.btn_dim = QPushButton("Cambia dimensioni selezione")
        self.btn_dim.setStyleSheet(f"background: {pal['accent2']}; border-radius: 7px; padding: 7px;")
        self.btn_dim.clicked.connect(self.cambia_dimensioni_selezione)
        prop_panel.addWidget(self.btn_dim)

        self.btn_ia = QPushButton("Suggerimento IA")
        self.btn_ia.setStyleSheet(f"background: {pal['accent4']}; border-radius: 7px; padding: 7px;")
        self.btn_ia.clicked.connect(self.suggerimento_ia)
        prop_panel.addWidget(self.btn_ia)

        self.btn_salva = QPushButton("Salva armadio")
        self.btn_salva.setStyleSheet(f"background: {pal['accent3']}; border-radius: 7px; padding: 7px;")
        self.btn_salva.clicked.connect(self.salva_armadio)
        prop_panel.addWidget(self.btn_salva)

        self.btn_nuovo = QPushButton("Nuovo armadio")
        self.btn_nuovo.setStyleSheet(f"background: {pal['accent5']}; border-radius: 7px; padding: 7px;")
        self.btn_nuovo.clicked.connect(self.nuovo_armadio)
        prop_panel.addWidget(self.btn_nuovo)

        self.btn_elimina = QPushButton("Elimina armadio")
        self.btn_elimina.setStyleSheet("background: #F08080; border-radius: 7px; padding: 7px; color: white;")
        self.btn_elimina.clicked.connect(self.elimina_armadio)
        prop_panel.addWidget(self.btn_elimina)

        prop_panel.addStretch()
        layout.addLayout(prop_panel)
        self.setCentralWidget(central)
        self.palette.itemPressed.connect(self.drag_start)
        self.lista_armadi.setCurrentRow(len(self.crud.armadi)-1)

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
        self.lista_armadi.refresh()
        QMessageBox.information(self, "Salvataggio", "Armadio salvato!")

    def carica_armadio(self):
        path, _ = QFileDialog.getOpenFileName(self, "Carica armadio", "", "Armadi JSON (*.json)")
        if not path:
            return
        vecchio_path = self.crud.storage_path
        self.crud.storage_path = path
        self.crud.armadi = self.crud.carica()
        if self.crud.armadi:
            self.armadio = self.crud.armadi[-1]
            self.scene.armadio = self.armadio
            self.scene.sync_grafica()
            self.lista_armadi.refresh()
            QMessageBox.information(self, "Caricamento", "Armadio caricato!")
        self.crud.storage_path = vecchio_path

    def nuovo_armadio(self):
        nome, ok = QInputDialog.getText(self, "Nuovo Armadio", "Nome:")
        if not (ok and nome): return
        idx = max([a.id for a in self.crud.armadi]+[0]) + 1
        forma = FormaPersonalizzata("rettangolare", {"larghezza": 300, "altezza": 260, "profondità": 60})
        armadio = Armadio(id=idx, nome=nome, cliente=None, progetto=None, forma=forma)
        self.crud.aggiungi(armadio)
        self.armadio = armadio
        self.scene.armadio = self.armadio
        self.scene.sync_grafica()
        self.lista_armadi.refresh()
        self.lista_armadi.setCurrentRow(self.lista_armadi.count()-1)

    def elimina_armadio(self):
        index = self.lista_armadi.currentRow()
        if index < 0 or self.lista_armadi.count() <= 1:
            QMessageBox.warning(self, "Elimina", "Seleziona un armadio diverso dall'ultimo rimasto.")
            return
        armadio = self.crud.armadi[index]
        self.crud.elimina(armadio.id)
        self.lista_armadi.refresh()
        self.lista_armadi.setCurrentRow(0)

    def cambia_armadio(self, idx):
        if idx < 0 or idx >= len(self.crud.armadi):
            return
        self.armadio = self.crud.armadi[idx]
        self.scene.armadio = self.armadio
        self.scene.sync_grafica()

    def cambia_forma(self, idx):
        nome, param = FORME_PRESET[idx]
        self.armadio.forma = FormaPersonalizzata(nome.lower().replace(" ", "_"), param)

    def suggerimento_ia(self):
        desc, ok = QInputDialog.getText(self, "Suggerimento IA", "Descrivi l'armadio desiderato:")
        if not (ok and desc): return
        armadio_ia = suggerisci_configurazione_armadio(desc)
        idx = max([a.id for a in self.crud.armadi]+[0]) + 1
        armadio_ia.id = idx
        self.crud.aggiungi(armadio_ia)
        self.armadio = armadio_ia
        self.scene.armadio = self.armadio
        self.scene.sync_grafica()
        self.lista_armadi.refresh()
        self.lista_armadi.setCurrentRow(self.lista_armadi.count()-1)
        QMessageBox.information(self, "Suggerimento IA", "Armadio generato dalla descrizione!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
