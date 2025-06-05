import os
from pathlib import Path
import shutil

def sync_local_to_cloud(local_backup_path, cloud_adapter):
    """
    Carica il backup locale sul cloud tramite l'adapter passato.
    """
    cloud_adapter.upload(local_backup_path)

def sync_cloud_to_local(cloud_adapter, dest_dir, latest_only=True):
    """
    Scarica l'ultimo backup dal cloud e lo salva in dest_dir.
    """
    backups = cloud_adapter.list_backups()
    if not backups:
        return None
    backup_to_download = backups[-1] if latest_only else backups
    local_path = Path(dest_dir) / Path(backup_to_download).name
    cloud_adapter.download(backup_to_download, str(local_path))
    return str(local_path)
