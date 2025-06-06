from .models import Armadio, Componente, Materiale

def aggiungi_componente(armadio: Armadio, componente: Componente):
    armadio.componenti.append(componente)

def rimuovi_componente(armadio: Armadio, nome_componente: str):
    armadio.componenti = [c for c in armadio.componenti if c.nome != nome_componente]

def aggiorna_componente(armadio: Armadio, componente_mod: Componente):
    for i, c in enumerate(armadio.componenti):
        if c.nome == componente_mod.nome:
            armadio.componenti[i] = componente_mod
