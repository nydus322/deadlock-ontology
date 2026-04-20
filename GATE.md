# Nydus Gate — LLM entry point (planned, not built)

The visual layer is an **LLM + plugin dyad**, not a viewer this repo ships. The repo's deliverable is the **canonical graph** and **the gate** an LLM uses to query it. This file is the design constraint that future implementation has to satisfy. No code in this file is wired up yet.

## Premise

- The graph (`outputs/heroes/*.ttl`) is the source of truth.
- 38/38 SHACL conform; 0 dangling refs; every IRI typed and labelled.
- An LLM (Claude, GPT, etc.) reads this graph through the gate and renders memetic responses (game iconography, hero portraits, ability glyphs, soul-item sprites). Text labels are second-tier.
- The operator can swap data sources or asset providers later without touching the gate's tool surface.

## Gate shape

Single MCP server. Tools below are the closed surface the LLM is given. Each tool returns structured payloads keyed by canonical Nydus IRIs — never engine-internal strings. The LLM is expected to render assets keyed off those IRIs (the gate doesn't ship pixels).

### Tools

| Tool | Args | Returns |
|---|---|---|
| `find_heroes(filter?)` | `{ scales_with?: sf:IRI, has_property?: prop:IRI, role?: role:IRI, has_keyword?: keyword:IRI }` | list of `{ hero_iri, label, codename, hero_id }` |
| `get_hero_kit(hero_iri)` | `{ hero_iri }` | `{ hero, slots: [{ slot_iri, ability_iri, abilityType }], properties: [...], upgrades: [...] }` keyed by canonical IRIs |
| `get_ability(ability_iri)` | `{ ability_iri }` | full per-ability payload: properties (each with propertyType + scaleFunction + baseValue), upgrades (each with modifiesPropertyType + bonusValue + tier) |
| `compare_heroes(hero_iris[])` | `{ hero_iris }` | per-IRI overlap matrix: which prop:* and sf:* IRIs are shared, which are unique |
| `who_scales_with(stat_or_sf_iri)` | `{ iri }` | every ability whose properties scale with that stat/function, grouped by hero |
| `vocabulary(class)` | `{ class: "PropertyType" \| "ScaleFunction" \| "Role" \| "Keyword" \| "DamageClass" }` | the full canonical IRI list with labels — the LLM uses this to plan queries |
| `describe(iri)` | `{ iri }` | the full subgraph rooted at `iri` (BFS depth ≤ 3), as a JSON tree |

### What the LLM does NOT get

- No SPARQL endpoint exposed directly. SPARQL is internal to the gate; the tool surface is curated.
- No raw blank-node IDs. Tools always return canonical IRIs and let the LLM compose follow-ups by IRI.
- No text descriptions pre-rendered. Labels are returned alongside IRIs but the LLM decides whether to use them at all.

### Asset path (operator-provided)

Each canonical IRI has an optional `nydus:assetURI` slot in the data. Empty by default. When the operator wires a hero portrait CDN / ability icon source, every gate response carries `asset_uri` next to `label` and the LLM can render memetically. Until then, the gate returns `asset_uri: null` and the LLM falls back to text — explicitly second-tier.

## What the ontology has to keep providing

The gate is only as useful as the canonical vocabulary it can query against. Active maintenance debt:

1. **PropertyType** (`prop:`) — done. 14 curated + synthetic fallbacks. Closed-world enforceable.
2. **ScaleFunction** (`sf:`) — done. 14 curated, all in player vocabulary.
3. **Role** (`role:`) — **not built yet**. Heroes need 1-N canonical roles (Initiator, Carry, Burst, Sustain, Support, CC, Mobility) — derivable from kit composition. Without this, `find_heroes(role: ...)` is dead.
4. **Keyword / status effect** (`keyword:`) — **not built yet**. Slow, Stun, Silence, Root, Burn, Pull. Per-ability `nydus:appliesKeyword`. Without this, "find me CC heroes" requires string sniffing.
5. **DamageClass** (`damage:`) — **not built yet**. Spirit / Weapon / Light / True / Burn. Per-property `nydus:damageClass`. Promotes the Tech-vs-Weapon distinction from string heuristics to typed IRIs.

These three (Role, Keyword, DamageClass) are the next ontology pass. They're insight-empowering bridges with weak connections elsewhere — they don't duplicate existing data, they expose latent structure that's currently locked inside flavor strings or implied by property names.

## Closure properties the gate counts on

These are SHACL-enforced as of the last referential-integrity pass:

- Every `nydus:Hero` has a label, an internalKey, ≥1 `hasAbilityInSlot`.
- Every full `nydus:Ability` (one with `abilityType`) has `internalKey`, `activationType`, `prov:wasDerivedFrom`.
- Every `nydus:AbilityProperty` has a `propertyType` IRI (typed `nydus:PropertyType`) and a `baseValue`.
- Every `nydus:AbilityUpgrade` has `upgradeLevel ∈ {1,2,3}`, a `modifiesPropertyType` IRI, a `bonusValue`.
- Every `nydus:scaleFunction` reference points to a typed `nydus:ScaleFunction`.
- Zero dangling IRIs across the corpus. Zero untyped declared resources.

Any future ontology change must preserve these closures or the gate's tool surface degrades gracefully (returns `null` rather than half-broken structures).
