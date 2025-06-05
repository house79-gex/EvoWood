# Modulo Armadi - EvoWood (Versione Avanzata)

## Funzionalità
- Progettazione avanzata armadi modulari su misura
- Gestione multi-modulo, materiali, ante, cassetti e accessori
- Cataloghi materiali/accessori (estendibili, integrabili da altri moduli/cataloghi IA)
- Interfaccia grafica PyQt5 multi-tab (dati generali, moduli, accessori, anteprima)
- Output dettagliato della struttura armadio (pronto per export e integrazione con CAD/CAM/BOM)
- Pronto per estensione con:
    - Suggerimenti IA (accessori, configurazioni)
    - Collegamento modulo rilievo reale
    - Export avanzati (DXF, 3D, etc.)

## Struttura file
- `models.py` — Modelli dati estesi (Materiale, Modulo, Vano, Anta, Cassetto, Accessorio, Armadio)
- `ui_armadio.py` — Interfaccia grafica avanzata PyQt5
- `README.md` — Questa documentazione

## Esecuzione demo
```bash
python ui_armadio.py
```

## Estensioni consigliate
- Integrazione reale con rilievo e altri moduli verticali
- Importazione cataloghi ferramenta/accessori da file/fornitori/IA
- Editor grafico 2D/3D
- Anteprima rendering e simulazioni
- Pipeline suggerimenti IA/configurazioni automatiche
