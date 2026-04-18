# Deadlock VPK and KV3 conventions for static data ETL

**Deadlock's data layer sits on Source 2's VData system — KV3-encoded, schema-typed, and fully flattened at decompile time, meaning preprocessor resolution is a non-issue but class discrimination and chaff filtering are the real ETL challenges.** The tooling ecosystem is mature enough for reliable batch extraction. ValveResourceFormat (VRF) handles all six binary KV3 versions including v5, which was added specifically for Deadlock in December 2024. The canonical extraction pipeline is DepotDownloader → VRF CLI (`--vpk_decompile`) → KV3 text → application-specific parser. Below is the deep dive across all eight areas.

---

## 1. The VRF-centered tooling ecosystem is production-ready for Deadlock

ValveResourceFormat (VRF, aka Source2Viewer) at `github.com/ValveResourceFormat/ValveResourceFormat` is the single authoritative decompiler for Deadlock VPKs. Maintained by **xPaw (Pavel Djundik)** — who also runs SteamDB — it ships as a .NET library, a GUI browser (S2V), and a CLI tool called **Decompiler**. The project recently moved from `SteamDatabase/ValveResourceFormat` to the `ValveResourceFormat` GitHub org. Key contributor **kristiker** also maintains the Python `keyvalues3` library on PyPI. As of **v19.1 (April 9, 2026, commit `c350f81`)**, KV3 text parsing was extracted to the separate **ValveKeyValue** library (`github.com/ValveResourceFormat/ValveKeyValue`, NuGet `ValveKeyValue` v0.20.0), which now handles KV3 text serialization. Binary KV3 parsing remains in VRF's `BinaryKV3` class.

The **CLI invocation** the community has converged on — used verbatim by `SteamDatabase/GameTracking-Deadlock`'s `update.sh` — is:

```bash
Decompiler \
  --input "game/citadel/pak01_dir.vpk" \
  --output "pak01_dir/" \
  --vpk_cache \
  --vpk_decompile \
  --vpk_extensions "txt,lua,kv3,db,gameevents,vcss_c,vjs_c,vts_c,vxml_c,vsndevts_c,vsndstck_c,vpulse_c,vdata_c"
```

The `--vpk_cache` flag enables incremental extraction (only re-extracts changed files), and `--vpk_extensions` filters to the extensions relevant for data extraction. The `_c` suffix denotes compiled resources that VRF decompiles back to text KV3.

**Known Deadlock-specific VRF issues** (from the issue tracker):
- **#849** (closed): `EntityLump.ReadValues()` threw `NotImplementedException` on Deadlock map `dl_streets_vmap_c` after a game update. Fixed.
- **#878** (open): Cloth bone animations don't export to GLB for Deadlock hero models like `models/heroes_staging/engineer/engineer.vmdl_c`. Rendering works, export doesn't.
- **#982** (open): SVG export from Deadlock `vsvg_c` files produces aliasing artifacts.
- **#672** (closed, not Deadlock-specific): `UnexpectedMagicException` on zero-magic KV3 files — corrupt/zeroed signature bytes.

**Community tools layered on VRF:**

| Tool | Language | Role | Wraps VRF? |
|------|----------|------|------------|
| `SteamDatabase/GameTracking-Deadlock` | Bash | Auto-extracts VPKs on every game update, commits diffs | Yes — CLI |
| `deadlock-wiki/deadbot` | Python | Parses decompiled VData → JSON/CSV for wiki upload | Yes — CLI |
| `deadlock-api/deadlock-api-assets` | Python/Bash | DepotDownloader + VRF → FastAPI serving parsed game data | Yes — CLI |
| `Zehmosu/kv3parser` | Python | Pure-Python KV3 text → JSON, no VRF dependency | No — direct parse |
| `ouwou/deadlock-data-tracking` | C#/.NET | Tracks VData changes across patches as JSON | Yes — library |
| `STmihan/deadlock-data-extractor` | Python + C# | Extracts heroes.json, items.json, images | Indirectly (via deadlockery) |
| `dougwithseismic/dezlock-dump` | C++ + TypeScript | Runtime schema/RTTI injection, dumps 23k+ classes with field offsets | No — process injection |
| `kristiker/keyvalues3` | Python | General KV3 read/write with encoding metadata | No — direct parse |

The **deadlock-api** GitHub org (`github.com/deadlock-api`, 17 repos) provides the most comprehensive API infrastructure, including `haste` — a Rust replay parser that handles a 31-minute match in ~660ms.

**Concrete actions for the normalizer:**
- (a) **Hardcode** the VRF CLI invocation pattern above as the extraction step. The `--vpk_extensions` list is the definitive filter for data-relevant files.
- (b) **Lookup table**: Map file extensions to content types: `vdata_c` → game data, `vsndevts_c` → sound events, `vxml_c` → Panorama UI, `vcss_c` → CSS, `vjs_c` → JS, `vpulse_c` → Pulse logic.
- (c) **Parser config**: For text KV3 parsing without VRF, use `Zehmosu/kv3parser` or `kristiker/keyvalues3` (Python), or `ValveKeyValue` v0.20.0+ (.NET). Binary KV3 requires VRF's `BinaryKV3` class — no standalone alternative exists.

---

## 2. Six binary KV3 versions exist, and VRF handles all of them

VRF's `BinaryKV3` class (at `ValveResourceFormat/Resource/ResourceTypes/BinaryKV3.cs`) defines six magic number constants:

| Constant | Hex Value | ASCII | Notes |
|----------|-----------|-------|-------|
| `MAGIC0` | `0x03564B56` | `VKV\x03` | Legacy format, basic compression |
| `MAGIC1` | `0x4B563301` | `KV3\x01` | LZ4 compression, single buffer |
| `MAGIC2` | `0x4B563302` | `KV3\x02` | ZSTD compression, improved blocks |
| `MAGIC3` | `0x4B563303` | `KV3\x03` | Binary blob blocks |
| `MAGIC4` | `0x4B563304` | `KV3\x04` | Mature format, serialization target |
| `MAGIC5` | `0x4B563305` | `KV3\x05` | **Dual-buffer architecture**, added for Deadlock |

**MAGIC5 was the headline feature of VRF v11.0 (December 2024)**, whose release notes explicitly state: *"This update was released to support new binary keyvalues 3 version added in Deadlock."* Version 5 introduces an auxiliary buffer for strings/metadata and optimized object length storage. Current Deadlock builds primarily emit v4 and v5 binary KV3.

Detection uses `BinaryKV3.IsBinaryKV3(uint magic)`, which checks the first 4 bytes against all six constants. Compression method is encoded as: **0** = uncompressed, **1** = LZ4, **2** = ZSTD. VRF v15.0 added **write-back serialization** to v4 format via `resource.Serialize(stream)`.

**No known parsing failures** exist for any KV3 version in current Deadlock builds. The only documented failure (#672) involved a corrupt file with zeroed magic bytes — not a format version issue.

**Concrete actions for the normalizer:**
- (a) **Hardcode** the six magic numbers as the KV3 detection table. Any file not matching one of these six 4-byte prefixes is not binary KV3.
- (c) **Parser config**: If building a custom binary parser, the v5 dual-buffer layout is the critical path. For ETL purposes, rely on VRF for binary → text conversion and parse only text KV3 downstream.

---

## 3. The CCitadel class hierarchy branches from three VData base classes

The class hierarchy is observable through three sources: the **s2v.app SchemaExplorer** (`s2v.app/SchemaExplorer/deadlock/`), the **DumpSource2/schemas/** directory in `SteamTracking/GameTracking-Deadlock`, and `dezlock-dump`'s RTTI extraction. The naming conventions are **inconsistent** — some classes use `CCitadel_` prefix, others `CCitadel` without underscore, and VData classes mix `CAbility*VData` with `CCitadelAbility*VData`.

### VData hierarchy (data definition classes)

```
CEntitySubclassVDataBase                         ← root of ALL VData
  ├── CitadelAbilityVData                        ← base for all abilities (100+ fields)
  │     ├── CAbilityMeleeVData
  │     ├── CAbilityJumpVData / CAbilityDashVData / CAbilityMantleVData
  │     ├── CBaseDashCastAbilityVData
  │     ├── CBaseLockonAbilityVData / CBaseTriggerAbilityVData
  │     ├── CCitadelAbilityChargedBombVData
  │     ├── CCitadelAbilityFlyingStrikeVData
  │     ├── CCitadelAbilityDruidBasePlantVData
  │     │     ├── CCitadelAbilityDruidPlantBranchWallVData
  │     │     ├── CCitadelAbilityDruidPlantHealingTreeVData
  │     │     └── CCitadelAbilityDruidPlantInvisBushVData
  │     ├── CAbilityLash[VData|DownStrike|Flog|Ultimate]VData
  │     ├── CAbilityHornet[Snipe|Chain|Leap|Sting]VData
  │     ├── CAbilityCadence[Anthem|Crescendo|GrandFinale|Lullaby|PrimaryWeapon|SilenceContraptions]VData
  │     └── ... (hundreds more, one per ability)
  │
  ├── CCitadelModifierVData                      ← base for all modifiers
  │     ├── CCitadelModifierAuraVData
  │     │     └── CCitadelModifierAura_ConeVData
  │     ├── CCitadelModifierAerialAssaultVData
  │     ├── CCitadelModifierCadenceGunSpikesVData
  │     ├── CCitadelModifer_Viscous_Goo_Aura_VData   ← note typo "Modifer"
  │     └── ... (extensive modifier list)
  │
  ├── CAI_BaseNPCVData
  │     └── CAI_CitadelNPCVData
  │           ├── CAI_NPC_TrooperVData (49 own fields)
  │           └── CAI_NPC_NecroSkeleVData
  │
  └── CBasePlayerVData                           ← base for player/hero VData
```

### Runtime entity hierarchy (server/client)

```
CEntityInstance → CBaseEntity → CBaseModelEntity → CBaseFlex → CBaseCombatCharacter
  ├── CBasePlayerPawn → CCitadelPlayerPawn
  └── CCitadelBaseAbility → [per-ability runtime classes]
```

The **`subclass` flag** is the polymorphic mechanism: a field declared as `CEntitySubclassVDataBase*` resolves at runtime to the full derived type. For example, `dezlock-dump` shows that such a pointer resolves to `CitadelAbilityVData` with 100+ fields. The `generic_data_type` key at the root of VData files declares the C++ struct type for all entries (e.g., `"generic_data_type": "PingWheelMessage_t"`).

**Concrete actions for the normalizer:**
- (b) **Lookup table**: Map VData class names to categories: `CitadelAbilityVData` and all `CAbility*VData`/`CCitadelAbility*VData` → "ability"; `CCitadelModifierVData` and subclasses → "modifier"; `CAI_*VData` → "npc"; `CBasePlayerVData` → "hero". Use suffix `VData` as the discriminator — any class ending in `VData` is a data definition.
- (a) **Hardcode** the known typo: `CCitadelModifer_Viscous_Goo_Aura_VData` (single 'i' in "Modifer"). This is not a pattern — it's a one-off misspelling in the source.
- (b) **Lookup table**: Build the base class → category mapping from the hierarchy above. Key discriminant: `generic_data_type` at VData root level tells you what struct type the file describes.

---

## 4. KV3 has no preprocessor directives — inheritance is schema-level, not file-level

This is the most important clarification for the normalizer: **`#base`, `#include`, and `@base` do not exist in KV3.** These are exclusively KeyValues1 (KV1) features. There is no file-level include or template system in KV3/VData.

`#base` (KV1 only) performs a recursive merge where the base file's keys are appended only if they don't already exist in the current file. `#include` (KV1 only) appends all keys including duplicates. Neither applies to `.vdata` files.

**What KV3 does have** is five **value flags** that annotate data:

- **`resource:`** — string is a resource path (e.g., `resource:"particles/items3_fx/star_emblem.vpcf"`)
- **`resourcename:`** — string is a resource name
- **`panorama:`** — Panorama UI reference
- **`soundevent:`** — sound event reference
- **`subclass:`** — marks a value as a polymorphic subclass type reference

The `subclass` flag is how the engine resolves polymorphic VData types. A hero's ability slot might contain `subclass:"citadel_ability_infernal_resilience"`, which the engine resolves to the corresponding C++ VData class at load time.

**Critically for ETL**: by the time VRF decompiles a `.vdata_c` file to text KV3, **all data is fully flattened and self-contained**. There are no cross-file references to resolve. Each entry includes all inherited fields with their values populated. The `deadlock-wiki/deadbot` parser confirms this — it does not handle any include resolution because none is needed post-decompilation.

The `gameinfo.gi` file (which *is* KV1 format) is the one file where `#base`-style mechanics could appear, but the current Deadlock `gameinfo.gi` does not use them.

**Concrete actions for the normalizer:**
- (c) **Parser config**: Do not implement `#base`, `#include`, or `@base` resolution for KV3 parsing. These features do not exist in the format.
- (c) **Parser config**: Implement the five KV3 value flags as annotations on parsed values. The `resource` and `subclass` flags are the ones most relevant for classification — `resource:` values are asset paths (filterable as chaff for stat extraction), and `subclass:` values identify the C++ type for polymorphic resolution.
- (a) **Hardcode**: The KV3 text header GUID pair `encoding:text:version{e21c7f3c-8a33-41c5-9977-a76d3a32aa0d} format:generic:version{7412167c-06e9-4698-aff2-e63eb59037e7}` is universal across all Deadlock VData files. Strip it during parsing.

---

## 5. Four monolithic VData files serve as de facto manifests

Deadlock does **not** have a `generic_data.vdata`, `hero_list.vdata`, or Dota-style `npc_heroes.txt` registry file. Instead, four large monolithic VData files under `game/citadel/pak01_dir/scripts/` serve as the canonical data sources:

- **`scripts/heroes.vdata`** — All hero definitions. Each hero entry contains `m_mapAbilities` (ability slot assignments keyed by `ESlot_Weapon`, `ESlot_Ability1`–`ESlot_Ability4`), `m_mapStartingStats`, `m_heroStatsUI`, and model references.
- **`scripts/abilities.vdata`** — All ability AND item definitions. This is the largest file and changes in nearly every patch.
- **`scripts/modifiers.vdata`** — All modifier/buff/debuff definitions.
- **`scripts/npc_units.vdata`** — NPC and unit definitions (troopers, bosses, etc.).

Additional minor VData files include `scripts/nav_hulls.vdata`, `scripts/nav_hulls_presets.vdata`, and `ping_wheel_messages.vdata`.

Each VData file uses a root-level `generic_data_type` key that declares the C++ struct type for its entries. Entity names within the file serve as dictionary keys at the top level — the file structure is essentially `{ "Root": { "generic_data_type": "TypeName", "EntityName1": { fields... }, "EntityName2": { fields... } } }`.

The **VPK manifest** (`pak01_dir.txt`, tracked by GameTracking-Deadlock) lists all files in the archive and can serve as a file-level index, though it's not semantically typed.

The `gameinfo.gi` contains a `VDataLocalization` block that configures auto-generated localization:
```
VDataLocalization {
    GameOutputPath  "resource/localization/citadel_vdata"
    TokenPrefix     "Citadel_VData_"
}
```

**Concrete actions for the normalizer:**
- (a) **Hardcode** the four canonical VData paths as the input file set: `scripts/heroes.vdata`, `scripts/abilities.vdata`, `scripts/modifiers.vdata`, `scripts/npc_units.vdata`.
- (b) **Lookup table**: Map `generic_data_type` values to data categories. The type declared at the root of each file is the authoritative type discriminator.
- (c) **Parser config**: Parse VData files as dictionaries keyed by entity name. Top-level keys (excluding `generic_data_type`) are entity identifiers. The hero file's `m_mapAbilities` field provides the authoritative hero → ability mapping.

---

## 6. Localization lives in five KV1 subdirectories with deterministic token joins

Localization files are **KeyValues1 format** (not KV3), located under `game/citadel/resource/localization/` inside the VPK. Five subdirectories exist:

| Directory | File Example | Content |
|-----------|-------------|---------|
| `citadel_attributes/` | `citadel_attributes_english.txt` | Attribute/stat names |
| `citadel_gc/` | `citadel_gc_english.txt` | Game coordinator strings |
| `citadel_heroes/` | `citadel_heroes_english.txt` (~214 KB) | Hero names, ability names, descriptions |
| `citadel_main/` | `citadel_main_english.txt` | Primary UI, HUD, menus |
| `citadel_mods/` | `citadel_mods_english.txt` | Mod-related strings |

Plus the auto-generated `citadel_vdata/` directory from the `VDataLocalization` gameinfo config, with prefix `Citadel_VData_`.

**Supported languages** (from `gameinfo.gi`): brazilian, czech, english, french, german, italian, indonesian, japanese, koreana, latam, polish, russian, schinese, spanish, thai, turkish, ukrainian.

**Token namespace conventions** are case-inconsistent but follow recognizable patterns:

- `#Citadel_` / `#citadel_` — general UI and game concepts
- `#Citadel_Hud_` — HUD elements
- `#Citadel_Settings_` — settings menu
- `#MODIFIER_CITADEL_` — modifier display names (uppercased)
- `#citadel_chatwheel_label_` / `#citadel_chatwheel_message_` — ping wheel
- `Citadel_VData_` — auto-generated VData localization (no `#` prefix)
- `modifier_citadel_` — modifier localization names in VData (lowercased, no `#`)

**Joins are deterministic.** VData fields reference localization tokens directly: `m_strLabelToken = "#citadel_chatwheel_label_GoingIn"` maps to the token `citadel_chatwheel_label_GoingIn` in the localization file. For modifiers, `m_sLocalizationName = "modifier_citadel_stunned"` gets uppercased and `#`-prefixed to `#MODIFIER_CITADEL_STUNNED` for lookup. The `#` prefix in VData values signals "this is a localization reference, not a literal string."

**Concrete actions for the normalizer:**
- (b) **Lookup table**: Map VData field names to localization join behavior: `m_strLabelToken`, `m_strMessageToken` → direct lookup (strip `#` prefix, find in `.txt` files); `m_sLocalizationName` → uppercase, prepend `#`, then lookup.
- (a) **Hardcode** the five localization subdirectory names and the `_english.txt` suffix as the canonical source paths.
- (c) **Parser config**: Use a KV1 parser (not KV3) for localization files. The format is `"lang" { "Language" "English" "Tokens" { "key" "value" } }`. ValveKeyValue's `KVSerializationFormat.KeyValues1Text` handles this natively.

---

## 7. Chaff patterns cluster around resource handles, editor metadata, and engine plumbing

No official chaff list exists. The following patterns are empirically derived from community parsing tools (`deadbot`, `deadlock-data-extractor`, `dezlock-dump` schema output) and Source 2 engine conventions. All VData fields use **Hungarian notation with `m_` prefix**.

### High-confidence denylist (engine plumbing, never gameplay-relevant)

- **Editor metadata**: `m_nEditorNode*`, `m_editorNode*`, `m_sComment` — editor positioning and annotations
- **Debug/test flags**: `m_bDebug*`, `m_bIsTestOnly`, `m_bTest*`
- **Entity identity**: `m_pEntity` (pointer), `m_name` (CUtlSymbolLarge internal name)
- **Network replication markers**: Fields with `[MNetworkEnable]` metadata — these are networking annotations, not data values

### Medium-confidence denylist (asset references, typically not wanted for stat extraction)

- **Particle handles**: `m_hParticle*`, `m_vecParticleSystems`
- **Model handles**: `m_hModel*`
- **Sound references**: `m_hSound*`, `m_strSound*`
- **Texture handles**: `m_hTexture*`
- **Animation handles**: `m_hCastAnimGraphAsset`, `m_hGlobalAnim*`, `m_fl*AnimGraph*`
- **Icon/image paths**: `m_strIcon` (values like `file://{images}/hud/ping/ping_icon_going_in.svg`), `m_strAbilityImage`

### Context-dependent fields (may be wanted depending on use case)

- **State machine fields**: `m_bitsPostCastEnabledStateMask`, `m_bitsInterruptingStates`, `m_nAbilityBehaviors` — bitmask flags encoding ability behavior rules
- **Type enums**: `m_eAbilityActivation`, `m_nAbilityTargetTypes`, `m_eAbilityType` — useful for classification but not stat display
- **Schema type fields**: `generic_data_type`, `_class`, `subclass`, `_type` — needed for type discrimination, not for output data
- **Empty defaults**: `[]` (empty arrays), `""` (empty strings), `0.0`/`0`/`false` — contextual; some zeros are meaningful balance values

### Prefix-based filter patterns

Fields starting with `m_h` are overwhelmingly resource handles (particle, model, sound, texture references). The prefix `m_str` requires disambiguation: `m_strLabelToken` is localization-relevant, but `m_strSound*` and `m_strIcon` are asset references.

**Evidence quality**: Thin. No community project publishes a canonical allow/deny list. The `deadbot` project performs field filtering in its Python parsing layer, but the specific filter logic would require reading its source code in detail. The patterns above are inferred from schema dumps and VData file inspection across multiple repos.

**Concrete actions for the normalizer:**
- (a) **Hardcode denylist**: `m_nEditorNode*`, `m_editorNode*`, `m_sComment`, `m_bDebug*`, `m_bIsTestOnly`, `m_pEntity`, `m_name` (CUtlSymbolLarge type only).
- (a) **Hardcode prefix denylist** (for stat extraction): `m_hParticle*`, `m_hModel*`, `m_hSound*`, `m_hTexture*`, `m_hCastAnimGraph*`, `m_hGlobalAnim*`, `m_vecParticle*`.
- (b) **Lookup table**: Classify `m_str*` fields: `m_strLabelToken`, `m_strMessageToken`, `m_strAbilityName` → keep (localization); `m_strSound*`, `m_strIcon`, `m_strAbilityImage` → filter for stat extraction, keep for asset extraction.
- (c) **Parser config**: Make the denylist configurable rather than absolute. Several "chaff" fields (state masks, behavior bitmasks) encode gameplay-relevant information that advanced consumers may want.

---

## 8. Ability values churn constantly, but file structure and class hierarchy are stable

**SteamDatabase/GameTracking-Deadlock** (689 commits, all from the `SteamDB-Tracker` bot) provides the definitive patch diff history. The `deadlock-wiki/deadbot` runs **hourly** CI checks for game updates via its `auto-deploy.yaml` workflow.

### Extreme volatility (changes nearly every patch, multiple times per week)

**`abilities.vdata`** and **`npc_units.vdata`** are modified in the vast majority of commits. The March 6, 2026 gameplay update alone contained ~**900 changes** to ability/item values. Typical balance patches touch damage numbers, cooldowns, heal amounts, and resistance percentages. Example from March 25, 2026: Bebop health regen 1.5→2.5, Calico Leaping Slash damage 50→60, Doorman Call Bell slow 30%→35%.

**Localization strings** (`client_strings.txt`, `server_strings.txt`, localization `.txt` files) change in most patches as ability descriptions are reworded.

### High volatility (changes with major updates)

**Schema classes** (`DumpSource2/schemas/`) — one observed commit changed **1,019 files** in the schemas directory when new fields were added across VData classes. New hero releases (6 heroes added in Jan 2026 "Old Gods, New Blood", 6 in Aug 2025) create entirely new `CAbility*VData` classes.

**Item shop structure** gets periodic reworks. Item tier structure (T1–T5 across Weapon/Vitality/Spirit categories) has been present throughout, but items are added, removed, and reclassified.

### Stable (rarely or never changes)

**Directory structure**: `game/citadel/` root, `pak01_dir/scripts/` for VData files, `resource/localization/` for strings — unchanged since tracking began. **VPK format** is Source 2 standard, stable. **`gameinfo.gi` structure** including SearchPaths is stable. **Class naming convention** (`CCitadel*`, `CAbility*VData`, `CCitadelModifier*VData`) is architecturally fixed. The internal codename **"citadel"** is permanently embedded in file paths.

### Known breaking changes for tooling

The binary KV3 v5 format (December 2024) broke all parsers that hadn't added MAGIC5 support. Major UI overhauls (January 2026 reactive portraits) broke UI mods. The February 2025 lane count change (4→3) broke map-related data assumptions. Valve does not guarantee mod stability — *"New game updates almost always break old mods"* (deadlockmods.app documentation).

**Undocumented changes are routine.** The community discovers balance changes not listed in patch notes via GameTracking diffs. Example: Celeste Light Eater target limit changed from 1 to 100 without any patch note.

**Concrete actions for the normalizer:**
- (a) **Hardcode** the stable paths: `game/citadel/pak01_dir/scripts/{heroes,abilities,modifiers,npc_units}.vdata` and `game/citadel/resource/localization/citadel_{attributes,gc,heroes,main,mods}/`. These are safe to rely on.
- (c) **Parser config**: Implement schema-tolerant parsing — accept unknown fields gracefully, since new fields are added with every hero release. Never fail on an unrecognized key.
- (c) **Parser config**: Use `SteamDatabase/GameTracking-Deadlock` commit history as the canonical diff source. The `--vpk_cache` flag in the extraction CLI enables efficient incremental re-extraction after patches.
- (b) **Lookup table**: Hero internal codenames → public names (volatile — new mappings added with each hero release): `werewolf`→Silver, `necro`→Graves, `familiar`→Rem, `unicorn`→Celeste, `fencer`→Apollo, `priest`→Venator. This table will grow and should be derived from the localization files rather than hardcoded.

---

## Conclusion

The Deadlock data extraction landscape is more mature than its "closed playtest" status might suggest. **VRF handles all binary KV3 versions including the Deadlock-specific v5**, and the GameTracking pipeline provides automated, commit-level diffs. The key insight for ETL design is that **KV3/VData files are fully flattened at decompile time** — there are no includes, no templates, and no cross-file references to resolve. The real engineering challenge is type discrimination (using `generic_data_type` and the VData class hierarchy as a lookup table) and chaff filtering (using the prefix-based patterns documented above). The most underappreciated resource is the `s2v.app/SchemaExplorer/deadlock/` — it provides browsable, typed class hierarchies directly from the game's schema system, making it possible to build an authoritative field allow-list per VData type rather than relying on empirical pattern matching.