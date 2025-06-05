from mega import Mega
from pathlib import Path

class MegaAdapter:
    def __init__(self, username, password):
        self.mega = Mega()
        self.m = self.mega.login(username, password)

    def upload(self, file_path, remote_folder=None):
        if remote_folder:
            folder = self.m.find(remote_folder)
            self.m.upload(file_path, folder[0])
        else:
            self.m.upload(file_path)

    def list_backups(self, remote_folder=None):
        files = self.m.get_files()
        backup_files = []
        for file_id, file_info in files.items():
            name = file_info['a']['n']
            if name.endswith(".zip"):
                backup_files.append(name)
        backup_files.sort()
        return backup_files

    def download(self, file_name, dest_path):
        files = self.m.get_files()
        for file_id, file_info in files.items():
            if file_info['a']['n'] == file_name:
                self.m.download(file_info, dest_path)
                return True
        return False
