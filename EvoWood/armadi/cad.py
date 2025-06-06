def apri_in_cad(armadio):
    """
    Stub per integrazione CAD.
    In futuro aprirà il progetto armadio nel CAD integrato.
    """
    print(f"Apro l'armadio '{armadio.nome}' nel CAD (funzione stub).")

def esporta_per_cad(armadio, path="modello_armadio.dxf"):
    """
    Stub di esportazione.
    In futuro esporterà i dati dell'armadio in un formato compatibile con CAD (es. DXF).
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"DXF di esempio per {armadio.nome}\n")
        f.write("...qui andrà la geometria generata...\n")
    print(f"Salvato file CAD in {path}.")
