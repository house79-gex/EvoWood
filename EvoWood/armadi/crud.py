from .models import Armadio
import json

class ArmadioCRUD:
    def __init__(self, storage_path="armadi.json"):
        self.storage_path = storage_path
        self.armadi = self.carica()

    def carica(self):
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Serve un parser custom per ricostruire oggetti complessi se usi dataclass
                return []
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Errore caricamento dati: {e}")
            return []

    def salva(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump([a.__dict__ for a in self.armadi], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Errore salvataggio dati: {e}")

    def aggiungi(self, armadio: Armadio):
        self.armadi.append(armadio)
        self.salva()
