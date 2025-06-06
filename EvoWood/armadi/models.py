from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Materiale:
    nome: str
    codice: str
    descrizione: str
    prezzo: float

@dataclass
class Componente:
    nome: str
    tipo: str
    materiale: Materiale
    dimensioni: dict  # es: {"larghezza": 80, "altezza": 200, "profondità": 60}

@dataclass
class Armadio:
    id: int
    nome: str
    cliente: Optional[str]
    progetto: Optional[str]
    componenti: List[Componente] = field(default_factory=list)
    finiture: Optional[str] = ""
    note: Optional[str] = ""
