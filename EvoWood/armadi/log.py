import datetime

LOG_PATH = "storico_armadi.log"

def registra_modifica(azione, armadio_id, dettaglio):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().isoformat()} | Armadio {armadio_id} | {azione} | {dettaglio}\n")
