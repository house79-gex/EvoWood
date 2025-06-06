from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class Materiale:
    nome: str
    codice: str
    descrizione: str
    prezzo: float
    finitura: Optional[str] = None
    colore: Optional[str] = None

@dataclass
class Componente:
    nome: str
    tipo: str  # esempio: anta, ripiano, cassetto, struttura, schiena, base, accessorio
    materiale: Materiale
    dimensioni: Dict[str, float]  # larghezza, altezza, profondità, spessore, etc.
    posizione: Dict[str, float] = field(default_factory=dict)  # x, y, z, angolo, etc.
    attributi: Dict[str, Any] = field(default_factory=dict)    # es: maniglia, cerniere, etc.

@dataclass
class FormaPersonalizzata:
    tipo: str  # esempio: "rettangolare", "angolo", "ponte", "trapezio", "su_misura"
    parametri: Dict[str, Any]  # punti, segmenti, angoli, curve, etc.

@dataclass
class Armadio:
    id: int
    nome: str
    cliente: Optional[str]
    progetto: Optional[str]
    forma: FormaPersonalizzata
    componenti: List[Componente] = field(default_factory=list)
    materiali: List[Materiale] = field(default_factory=list)
    accessori: List[str] = field(default_factory=list)
    note: Optional[str] = ""
    tags: List[str] = field(default_factory=list)
    descrizione_testuale: Optional[str] = ""
    extra: Dict[str, Any] = field(default_factory=dict)
