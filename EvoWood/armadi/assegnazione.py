from .models import Armadio

def assegna_cliente(armadio: Armadio, cliente: str):
    armadio.cliente = cliente

def assegna_progetto(armadio: Armadio, progetto: str):
    armadio.progetto = progetto
