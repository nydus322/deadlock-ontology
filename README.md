# Deadlock Ontology — Nydus

A knowledge graph viewer for Deadlock heroes, abilities, and stats. The project contains a Python data pipeline that builds a structured RDF graph from raw game files, and a Flutter web app (`nydus_flutter/`) that visualises it.

---

## Data Pipeline

```
game KV3 files
      │
      ▼  src/extract.py
  raw JSON per hero
      │
      ▼  src/build_graph.py
  Turtle (.ttl) RDF graph per hero
      │
      ▼  src/bundle.py
  assets/graphs.json   ← loaded by the Flutter app
```

`assets/graphs.json` contains a single JSON object keyed by hero code (e.g. `hero_inferno`). Each value is a Cytoscape.js-compatible graph with `nodes` and `edges` arrays.

---

## Flutter App — `nydus_flutter/`

### Running

```bash
cd nydus_flutter
flutter pub get
flutter run -d chrome
```

Targets Flutter web. Requires Flutter ≥ 3.22 / Dart ≥ 3.4.

### Tech stack

| Concern | Choice |
|---|---|
| State management | Riverpod 2.x (`flutter_riverpod`) |
| Fonts | Google Fonts — Cinzel (hero/ability names), Fira Code (stats/IRIs) |
| Graph rendering | `CustomPainter` + `InteractiveViewer` (no third-party graph package) |

---

## Architecture

### Directory layout

```
lib/
├── main.dart                    — ProviderScope + runApp
├── app.dart                     — MaterialApp + theme wiring
│
├── data/
│   ├── models/
│   │   ├── bundle_data.dart     — BundleData (lazy per-hero parse), HeroGraph, HeroEntry
│   │   ├── graph_elements.dart  — GraphNode, GraphEdge, NodeData, EdgeData; CLASS_ORDER
│   │   └── kit_data.dart        — KitData, SlotData, AbilityKitData, UpgradeData, StatEntry
│   ├── repository/
│   │   └── bundle_repository.dart — rootBundle.loadString → BundleData
│   ├── extractors/
│   │   ├── prop_formatter.dart  — spiritize, prettifyPropKey/Value, withUnit, stripParentName
│   │   ├── kit_extractor.dart   — port of extractKitData() + computeKitNodeIds()
│   │   └── topology.dart        — port of synthesizeKitTopology(); blank-node collapsing
│   └── graph/
│       ├── force_layout.dart    — ForceNode/ForceEdge types + radiusForClass(); ForceLayout (unused)
│       └── hierarchical_layout.dart — BFS static layout (HierarchicalLayout.compute)
│
├── state/
│   ├── app_state.dart           — AppViewMode enum (card | graph)
│   ├── app_providers.dart       — all Riverpod providers
│   └── graph_notifier.dart      — GraphNotifier + GraphState (filters, selection, kit mode)
│
├── theme/
│   ├── app_colors.dart          — all Color constants; AppColors.forNodeClass(cls)
│   ├── hero_accents.dart        — 38 per-hero accent colors; HeroAccents.forHero()
│   ├── app_text_styles.dart     — all TextStyle definitions
│   └── app_theme.dart           — HeroAccentTheme (ThemeExtension); buildAppTheme()
│
└── widgets/
    ├── shell/
    │   ├── app_shell.dart       — top-level layout; re-wraps Theme with per-hero accent
    │   ├── nydus_app_bar.dart
    │   ├── hero_picker.dart     — DropdownButton reading heroListProvider
    │   └── view_mode_toggle.dart — Card / Map segmented toggle
    ├── card_view/
    │   ├── hero_card_view.dart  — root layout (responsive 1/2-col)
    │   ├── hero_card_header.dart — hero name + tag chips (fade-in animation)
    │   ├── ability_grid.dart    — Wrap auto-fit columns
    │   ├── ability_card.dart    — per-ability card with hover lift animation
    │   ├── ability_stats_list.dart
    │   ├── tier_stamp.dart      — T1/T2/T3 upgrade box
    │   ├── upgrade_row.dart
    │   └── stats_spine.dart     — 220 px right sidebar: Core + Combat stat sections
    ├── graph_view/
    │   ├── graph_view.dart      — 3-column root layout
    │   ├── graph_canvas.dart    — pan/zoom canvas; tap + hover interaction
    │   ├── graph_painter.dart   — CustomPainter: nodes, edges, labels, glow
    │   ├── graph_left_sidebar.dart — class/edge filter chips, kit-mode toggle
    │   ├── graph_right_sidebar.dart — wraps InspectorPanel
    │   └── inspector_panel.dart — class tag, IRI, properties, edge lists
    └── shared/
        ├── tag_chip.dart
        ├── filter_chip_widget.dart
        ├── stat_row.dart
        └── section_header.dart
```

### Riverpod provider chain

```
bundleProvider  (FutureProvider<BundleData>)
  ├── heroListProvider          → List<HeroEntry>
  └── currentHeroCodeProvider   → StateProvider<String>
        ├── currentHeroGraphProvider  → Provider<HeroGraph?>
        │     ├── kitDataProvider         → Provider<KitData?>
        │     ├── synthesizedGraphProvider → Provider<SynthesizedGraph?>
        │     └── kitNodeIdsProvider       → Provider<Set<String>>
        └── heroAccentThemeProvider   → Provider<HeroAccentTheme>

viewModeProvider    (StateProvider<AppViewMode>)
graphNotifierProvider (NotifierProvider<GraphNotifier, GraphState>)
```

### Hero accent color system

`HeroAccentTheme` is a `ThemeExtension<HeroAccentTheme>`. `AppShell` rebuilds the `Theme` subtree each time `heroAccentThemeProvider` changes, so all descendants read `Theme.of(context).extension<HeroAccentTheme>()!.accent` without prop-drilling — the Flutter equivalent of a CSS custom property (`--hero-accent`).

---

## Card View

The default view. Activated by the **Card** toggle in the app bar.

- **Hero header** — Cinzel hero name with fade + slide animation; role/faction tag chips.
- **Ability grid** — responsive `Wrap`; each card shows slot label, ability name, stats list, and T1/T2/T3 upgrade rows. Weapon and aberrant slots use distinct accent colors.
- **Stats spine** — 220 px right sidebar with Core stats (health, speed, stamina) and Combat stats (melee damage, reload speed, etc.).

Data is extracted from the raw graph by `KitExtractor.extract()`, which walks the `Hero → hasAbilityInSlot → [blank node] → {slot, ability}` RDF pattern, formats values via `PropFormatter`, and returns a typed `KitData` tree.

---

## Graph View (Map)

Activated by the **Map** toggle. Shows the full RDF graph for the selected hero as an interactive node-link diagram.

### Layout

`HierarchicalLayout.compute()` runs a BFS from the Hero root node and assigns each node a depth level:

```
Level 0  Hero
Level 1  Slots
Level 2  Abilities
Level 3  Stats / Properties
Level 4  Upgrades / Scale functions
```

Nodes are distributed evenly across each level, with extra padding between sibling groups that have different parents (preserving slot-ability clustering). All node positions are static — no physics simulation.

### Rendering (`GraphPainter`)

Node shapes are mapped to ontology classes:

| Class | Shape |
|---|---|
| Hero | Circle |
| Ability | Rounded rectangle |
| Slot | Triangle |
| Stat | Diamond |
| AbilityUpgrade | Rounded rectangle (smaller) |
| Other | Circle |

Edge predicates are color-coded: `hasSlot`/`filledBy` → hero accent, `hasProperty` → muted fg, `hasUpgrade` → border, `scalesStat` → gold accent, `primaryCategory`/`secondaryCategory` → category color.

### Interaction

- **Pan / zoom** — `InteractiveViewer` with scale range 0.03–5×.
- **Tap node** — selects it; inspector panel on the right shows class, IRI, properties, and outgoing/incoming edges.
- **Hover edge** — highlights the edge and shows a predicate label.
- **Left sidebar** — toggle visibility by node class and edge predicate; **Kit mode** restricts the graph to the hero's signature kit (5 slots + abilities + their immediate properties/upgrades).

### Blank-node collapsing

`TopologyExtractor.synthesize()` pre-processes the raw Cytoscape graph before rendering. RDF reification blank nodes (intermediaries from `hasAbilityInSlot` triples) are collapsed into direct synthetic `hasSlot` (Hero→Slot) and `filledBy` (Slot→Ability) edges, removing them from the visible graph.

---

## PropFormatter

Static utility methods ported from the original JavaScript app:

| Method | Purpose |
|---|---|
| `spiritize(s)` | Replaces `Tech` → `Spirit` throughout (Deadlock in-game terminology) |
| `prettifyPropKey(k)` | camelCase → display label; strips `starting` prefix |
| `prettifyPropValue(k, v)` | Numeric rounding; Valve enum prefix stripping; scale function + modifies-property lookups |
| `unitFor(label)` | Returns `%`, `s`, `m`, or `''` based on label suffix |
| `withUnit(value, label)` | Appends unit if value doesn't already carry one |
| `stripParentName(child, parent)` | Removes parent name tokens from child labels to reduce redundancy |
| `classifyPropKey(k)` | Buckets hero stat keys into Core / Combat / Meta |
