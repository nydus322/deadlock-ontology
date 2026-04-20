# Nydus

A knowledge graph of every active **Deadlock** hero — abilities, tiered upgrades, scaling stats, and the engine relationships between them — built from Valve's `.vdata` files.

**[Open the viewer →](https://nydus322.github.io/deadlock-ontology/outputs/nydus.html)** · single self-contained HTML, ~3 MB

## What's in here

```
src/
  kv3_parser.py        Valve KV3 / KV1 localization parser
  graph_builder.py     Emits per-hero RDF/Turtle, validates against SHACL
  nydus.shacl.ttl      Shape constraints — the ontology's contract
  ttl_to_cytoscape.py  Bundles all hero TTLs into a single Cytoscape JSON
  bundle.py            Inlines libs + data + CSS into one HTML file

outputs/
  nydus.html           The shipped viewer (the thing GitHub Pages serves)
```

The intermediate per-hero TTLs (`outputs/heroes/`) and the dev viewer assets (`outputs/viewer/`) are not tracked — they regenerate from a local Deadlock install.

## Vocabulary

The ontology speaks Deadlock, not Source 2. Every property points at a canonical IRI in player vocabulary:

- `prop:Cooldown`, `prop:Damage`, `prop:Duration`, `prop:CastRange`, `prop:Charges`, `prop:Radius`, `prop:DPS`, …
- `sf:SpiritPower`, `sf:WeaponDamage`, `sf:SpiritDuration`, `sf:AbilityCharges`, …

So `"which abilities scale with Spirit Power?"` is one SPARQL hop, not a string match. SHACL validates that every reference resolves to a typed canonical IRI.

## Regenerate locally

```bash
# 1. Get the Source2Viewer CLI (https://github.com/ValveResourceFormat/ValveResourceFormat/releases)
#    Drop the binaries into tools/vrf/

# 2. Extract the .vdata files from your Deadlock install
tools/vrf/Source2Viewer-CLI.exe \
  -i "<steam>/Deadlock/game/citadel/pak01_dir.vpk" \
  -o extracted/ --vpk_decompile \
  --vpk_filepath scripts/heroes.vdata_c,scripts/abilities.vdata_c,scripts/modifiers.vdata_c,scripts/npc_units.vdata_c

# 3. Build
pip install rdflib pyshacl
PYTHONUTF8=1 python3 src/graph_builder.py                                    # 38/38 SHACL conform
PYTHONUTF8=1 python3 src/ttl_to_cytoscape.py --bundle outputs/heroes outputs/viewer/graphs.json
PYTHONUTF8=1 python3 src/bundle.py                                            # writes outputs/nydus.html

# 4. Open outputs/nydus.html in any browser
```

## License

MIT for the code. Deadlock and its data are © Valve; this repo redistributes none of it — it just parses what's already on your disk.
