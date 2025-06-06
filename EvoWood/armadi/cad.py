def esporta_per_cad(armadio, path="modello_armadio.dxf"):
    # Placeholder: salva dati armadio in formato compatibile con CAD
    with open(path, "w") as f:
        f.write(f"DXF di esempio per {armadio.nome}\n")
    print(f"Salvato file CAD in {path}.")
