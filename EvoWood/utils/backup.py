import os
import zipfile
from datetime import datetime
from pathlib import Path

def create_backup(data_dirs, output_dir, backup_name=None):
    """
    Crea un archivio ZIP dei dati specificati.
    data_dirs: elenco di cartelle o file da includere (path assoluti o relativi)
    output_dir: cartella dove salvare il backup
    backup_name: nome file backup (se None viene generato con data/ora)
    Ritorna il path del file creato.
    """
    if not backup_name:
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    backup_path = Path(output_dir) / backup_name
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for item in data_dirs:
            p = Path(item)
            if p.is_dir():
                for root, dirs, files in os.walk(p):
                    for file in files:
                        full_path = Path(root) / file
                        arcname = full_path.relative_to(p.parent)
                        zf.write(full_path, arcname)
            elif p.is_file():
                zf.write(p, p.name)
    return str(backup_path)

def extract_backup(backup_path, dest_dir):
    """
    Estrae l'archivio ZIP nel percorso specificato.
    """
    with zipfile.ZipFile(backup_path, 'r') as zf:
        zf.extractall(dest_dir)
