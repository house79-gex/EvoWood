# Servizi aggiuntivi per armadi: esportazione, filtri, logica business

def esporta_armadi_csv(armadi, path="armadi.csv"):
    import csv
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Nome", "Cliente", "Progetto", "Finiture", "Note"])
        for a in armadi:
            writer.writerow([a.id, a.nome, a.cliente, a.progetto, a.finiture, a.note])

def filtra_armadi_per_cliente(armadi, cliente):
    return [a for a in armadi if a.cliente == cliente]
