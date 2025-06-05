from typing import List, Optional

class Materiale:
    def __init__(self, nome: str, descrizione: str = "", codice: Optional[str] = None):
        self.nome = nome
        self.descrizione = descrizione
        self.codice = codice

class Accessorio:
    def __init__(self, nome: str, categoria: str, codice: Optional[str] = None):
        self.nome = nome
        self.categoria = categoria
        self.codice = codice

class Anta:
    def __init__(self, tipo: str, materiale: Materiale, altezza: int, larghezza: int, apertura: str = "battente"):
        self.tipo = tipo  # es: battente, scorrevole
        self.materiale = materiale
        self.altezza = altezza
        self.larghezza = larghezza
        self.apertura = apertura

class Cassetto:
    def __init__(self, larghezza: int, altezza: int, profondita: int, materiale: Materiale):
        self.larghezza = larghezza
        self.altezza = altezza
        self.profondita = profondita
        self.materiale = materiale

class Vano:
    def __init__(self, larghezza: int, altezza: int, profondita: int, tipo: str = "ripiano", n_ripiani: int = 0):
        self.larghezza = larghezza
        self.altezza = altezza
        self.profondita = profondita
        self.tipo = tipo  # es: ripiano, vano vuoto, appendiabiti
        self.n_ripiani = n_ripiani

class Modulo:
    def __init__(self, larghezza: int, altezza: int, profondita: int,
                 vani: List[Vano], ante: List[Anta], cassetti: List[Cassetto], materiale: Materiale, nome: str = ""):
        self.nome = nome or "Modulo"
        self.larghezza = larghezza
        self.altezza = altezza
        self.profondita = profondita
        self.vani = vani
        self.ante = ante
        self.cassetti = cassetti
        self.materiale = materiale

class Armadio:
    def __init__(self, nome: str, moduli: List[Modulo], accessori: Optional[List[Accessorio]] = None, note: str = ""):
        self.nome = nome
        self.moduli = moduli
        self.accessori = accessori or []
        self.note = note

    def descrizione_dettagliata(self):
        desc = f"Armadio: {self.nome}\nNote: {self.note}\n"
        for i, modulo in enumerate(self.moduli):
            desc += f"\nModulo {i+1} - {modulo.nome}: {modulo.larghezza}x{modulo.altezza}x{modulo.profondita}cm\n"
            desc += f"  Materiale: {modulo.materiale.nome}\n"
            for j, vano in enumerate(modulo.vani):
                desc += f"    Vano {j+1}: {vano.tipo}, {vano.larghezza}x{vano.altezza}x{vano.profondita}cm, Ripiani: {vano.n_ripiani}\n"
            for j, anta in enumerate(modulo.ante):
                desc += f"    Anta {j+1}: {anta.tipo} {anta.apertura}, {anta.larghezza}x{anta.altezza}cm, Materiale: {anta.materiale.nome}\n"
            for j, cass in enumerate(modulo.cassetti):
                desc += f"    Cassetto {j+1}: {cass.larghezza}x{cass.altezza}x{cass.profondita}cm, Materiale: {cass.materiale.nome}\n"
        if self.accessori:
            desc += "\nAccessori:\n"
            for acc in self.accessori:
                desc += f"  - {acc.nome} ({acc.categoria})\n"
        return desc
