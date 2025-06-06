import json
from .models import Armadio

class ArmadioCRUD:
    def __init__(self, storage_path="armadi.json"):
        self.storage_path = storage_path
        self.armadi = self.carica()

    def carica(self):
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Armadio(**a) for a in data]
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

    def elimina(self, armadio_id: int):
        self.armadi = [a for a in self.armadi if a.id != armadio_id]
        self.salva()

    def aggiorna(self, armadio_mod: Armadio):
        for idx, a in enumerate(self.armadi):
            if a.id == armadio_mod.id:
                self.armadi[idx] = armadio_mod
                self.salva()
                return

    def cerca(self, keyword: str):
        return [a for a in self.armadi if keyword.lower() in a.nome.lower()]
