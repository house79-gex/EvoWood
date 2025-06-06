from .models import Armadio, FormaPersonalizzata, Componente, Materiale
import random

def suggerisci_configurazione_armadio(descrizione_testuale: str) -> Armadio:
    """
    Riceve una descrizione testuale e genera una configurazione base di armadio.
    In futuro collegherà un modello IA evoluto.
    """
    # Esempio: generazione dummy, da sostituire con IA reale
    forma = FormaPersonalizzata(
        tipo="rettangolare" if "angolo" not in descrizione_testuale else "angolo",
        parametri={"larghezza": 300, "altezza": 260, "profondità": 60}
    )
    materiale = Materiale(nome="Melaminico", codice="MEL001", descrizione="Bianco", prezzo=25.0)
    componenti = [
        Componente(
            nome="Anta 1",
            tipo="anta",
            materiale=materiale,
            dimensioni={"larghezza": 60, "altezza": 260, "spessore": 2},
            posizione={"x": 0, "y": 0, "z": 0},
        ),
        Componente(
            nome="Ripiano base",
            tipo="ripiano",
            materiale=materiale,
            dimensioni={"larghezza": 300, "profondità": 60, "spessore": 2},
            posizione={"x": 0, "y": 0, "z": 0},
        ),
    ]
    armadio = Armadio(
        id=random.randint(1000, 9999),
        nome="Suggerito IA",
        cliente=None,
        progetto=None,
        forma=forma,
        componenti=componenti,
        materiali=[materiale],
        descrizione_testuale=descrizione_testuale,
        tags=["generato", "ia"],
    )
    return armadio
