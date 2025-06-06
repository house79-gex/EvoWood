def cerca_armadi_per_materiale(armadi, materiale_nome):
    return [a for a in armadi if any(c.materiale.nome == materiale_nome for c in a.componenti)]

def cerca_armadi_per_dimensione(armadi, larghezza_min=0, larghezza_max=9999):
    return [
        a for a in armadi
        if any(
            c.dimensioni.get("larghezza",0) >= larghezza_min and c.dimensioni.get("larghezza",0) <= larghezza_max
            for c in a.componenti
        )
    ]
