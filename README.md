# Nydus — Deadlock Ontology Graph

A navigable knowledge graph of every active **Deadlock** hero's abilities, upgrades, and stat scaling — built directly from Valve's `.vdata` files.

**[Open Nydus in your browser →](outputs/nydus.html)** (single self-contained HTML, 3 MB)

![Nydus screenshot placeholder — open outputs/nydus.html](outputs/viewer/og-preview.png)

- 38 active heroes
- Ability → stat scaling paths (e.g. *Infernus's Afterburn → Spirit Power*)
- Tiered upgrades as first-class nodes
- Slot bindings (Primary Weapon, Ability 1..4, innate movement)
- Deep linkable: `nydus.html#hero/Yamato/node/ability/PowerSlash`

## Pipeline

```
Deadlock .vpk  →  Source2Viewer-CLI  →  .vdata
     |
     v
kv3_parser.py  (Valve KV3 / KV1 localization)
     |
     v
graph_builder.py  →  RDF / Turtle  →  SHACL validation
     |
     v
ttl_to_cytoscape.py  →  graphs.json
     |
     v
bundle.py  →  nydus.html  (inline JS libs + data + CSS)
```

Every typed resource carries `rdfs:label` resolved from Deadlock's English localization bundle, so the viewer surfaces "Spirit Power" instead of `TechPower`, "Primary Weapon" instead of `WeaponPrimary`, and so on.

## Regenerate from your own Deadlock install

1. Grab the Source2Viewer CLI from [ValveResourceFormat/releases](https://github.com/ValveResourceFormat/ValveResourceFormat/releases), unzip to `tools/vrf/`.
2. Extract the `.vdata` files:
   ```bash
   tools/vrf/Source2Viewer-CLI.exe \
     -i "<steam>/Deadlock/game/citadel/pak01_dir.vpk" \
     -o extracted/ --vpk_decompile \
     --vpk_filepath scripts/heroes.vdata_c,scripts/abilities.vdata_c,scripts/modifiers.vdata_c,scripts/npc_units.vdata_c
   ```
3. Build:
   ```bash
   pip install rdflib pyshacl
   PYTHONUTF8=1 python3 src/graph_builder.py
   PYTHONUTF8=1 python3 src/ttl_to_cytoscape.py --bundle outputs/heroes outputs/viewer/graphs.json
   PYTHONUTF8=1 python3 src/bundle.py
   ```
4. Open `outputs/nydus.html`.

## Repo layout

- `src/graph_builder.py` — emits per-hero `.ttl` + SHACL validates
- `src/nydus.shacl.ttl` — shape constraints
- `src/ttl_to_cytoscape.py` — converts to `graphs.json`
- `src/bundle.py` — inlines everything into `nydus.html`
- `outputs/heroes/*.ttl` — 38 hero Turtles (the canonical data)
- `outputs/nydus.html` — shipped single-file viewer
- `Knowledge/` — design notes and heuristics

## License

MIT for the code. Deadlock game data is © Valve; this project just parses what's locally installed.
