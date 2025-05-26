import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.themes import apply_dark_theme

def main():
    app = QApplication(sys.argv)
    apply_dark_theme(app)  # Applica il tema scuro
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
