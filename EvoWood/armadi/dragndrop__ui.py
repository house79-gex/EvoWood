import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QGraphicsView, QGraphicsScene, QGraphicsRectItem, QColorDialog, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QBrush

class ComponentiPalette(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(120)
        for nome in ["Fianco", "Fondo", "Zoccolo", "Anta", "Ripiano"]:
            item = QListWidgetItem(nome)
            item.setData(Qt.UserRole, nome)
            self.addItem(item)
        self.setStyleSheet("background: #FDEEC6; border-radius: 7px; font-weight: bold;")

class ArmadioScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setBackgroundBrush(QColor("#FFF5E0"))  # Colore caldo chiaro
        self.base_width = 300
        self.base_height = 260

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        nome = event.mimeData().text()
        if nome:
            rect = QGraphicsRectItem(0, 0, 40, 100)
            rect.setBrush(QBrush(QColor("#F6B26B")))  # Arancio caldo
            rect.setFlag(QGraphicsRectItem.ItemIsMovable, True)
            rect.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
            rect.setToolTip(nome)
            self.addItem(rect)
            rect.setPos(self.views()[0].mapToScene(event.pos()))
        event.accept()

class ArmadioView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setAcceptDrops(True)
        self.setStyleSheet("border: 2px solid #BB7539; background: #FFF5E0;")

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        self.scene().dropEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progetta Armadio - EvoWood")
        self.setStyleSheet("background: #FFF5E0; color: #6C3D12; font-family: Segoe UI; font-size: 12pt;")
        self.resize(900, 600)
        central = QWidget()
        layout = QHBoxLayout(central)

        self.palette = ComponentiPalette()
        layout.addWidget(self.palette)

        self.scene = ArmadioScene()
        self.view = ArmadioView(self.scene)
        layout.addWidget(self.view, stretch=1)

        # Palette colori e proprietà
        prop_panel = QVBoxLayout()
        self.btn_colore = QPushButton("Cambia colore selezione")
        self.btn_colore.setStyleSheet("background: #F6B26B; border-radius: 7px; padding: 7px;")
        self.btn_colore.clicked.connect(self.cambia_colore_selezione)
        prop_panel.addWidget(self.btn_colore)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
