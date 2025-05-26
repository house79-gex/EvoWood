from PyQt5.QtWidgets import QMainWindow, QAction, QLabel, QVBoxLayout, QWidget, QStatusBar
from .clienti_window import ClientiWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EvoWood - Progettazione Arredi su Misura")
        self.setGeometry(100, 100, 1000, 700)

        # Menu
        self.create_menu()

        # Widget centrale vuoto (placeholder)
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Benvenuto in EvoWood!"))
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Barra di stato
        self.setStatusBar(QStatusBar())

    def create_menu(self):
        menubar = self.menuBar()

        # File
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Esci", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Moduli
        modules_menu = menubar.addMenu("Moduli")
        rilievo_action = QAction("Rilievo Misure", self)
        modules_menu.addAction(rilievo_action)
        cad_action = QAction("CAD", self)
        modules_menu.addAction(cad_action)
        clienti_action = QAction("Gestione Clienti", self)
        clienti_action.triggered.connect(self.open_clienti_window)
        modules_menu.addAction(clienti_action)

        # Help
        help_menu = menubar.addMenu("Aiuto")
        about_action = QAction("Info su EvoWood", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def open_clienti_window(self):
        self.clienti_window = ClientiWindow()
        self.clienti_window.show()

    def show_about(self):
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Info", "EvoWood\nProgettazione e gestione arredi su misura.\nBy house79-gex")
