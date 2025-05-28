import os
import shutil
import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
BACKUP_DIR = os.path.join(DATA_DIR, "backup")

def backup_files():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    files = ["clienti.json", "appuntamenti.json"]
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    for f in files:
        src = os.path.join(DATA_DIR, f)
        if os.path.exists(src):
            dest = os.path.join(BACKUP_DIR, f"{f}_{stamp}.bak")
            shutil.copy2(src, dest)
    # Include allegati, se vuoi
    return True

def restore_latest_backup(file):
    # Cerca il backup più recente per il file
    files = [f for f in os.listdir(BACKUP_DIR) if f.startswith(file)]
    if not files:
        return None
    files.sort(reverse=True)
    latest = files[0]
    shutil.copy2(os.path.join(BACKUP_DIR, latest), os.path.join(DATA_DIR, file))
    return latest

# Sincronizzazione Cloud (Dropbox, Google Drive)
# Qui puoi implementare il caricamento/scaricamento dei file data su cloud.
# Esempio: usa pydrive per Google Drive, dropbox per Dropbox.
# Puoi aggiungere funzioni tipo:
#   def sync_to_dropbox(): ...
#   def sync_to_gdrive(): ...
