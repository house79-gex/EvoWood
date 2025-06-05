from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton
from utils.config import set_cloud_credentials, get_cloud_credentials

class CloudSettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Impostazioni Cloud MEGA")
        layout = QVBoxLayout()
        creds = get_cloud_credentials()
        self.username_edit = QLineEdit(creds.get('username', ''))
        self.password_edit = QLineEdit(creds.get('password', ''))
