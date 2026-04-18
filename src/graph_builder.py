#!/usr/bin/env python3
"""
Nydus graph_builder.py  —  Phase C -> B -> A in one pass.

Outputs (all to outputs/):
  stat_bridge.jsonl        C: every (ability, property, MODIFIER_VALUE, scale_stat) edge
  stat_bridge_summary.md   C: frequency tables + scale function inventory
  roster.jsonl             B: canonical hero identity map with status
  roster_intelligence.md   B: annotated roster markdown
  abrams.ttl               A: Abrams vertical slice in Turtle
  wander_questions.md      +: minimum calibration deck for human expert

Usage:
  PYTHONUTF8=1 python3 src/graph_builder.py
"""

import sys
import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from typing import Any, Optional

# Reuse parser + localization from Phase 1
sys.path.insert(0, str(Path(__file__).parent))
from kv3_parser import KV3TextParser, LOC_BASE, LOC_SUBDIRS, parse_kv1_localization

BASE_DIR      = Path(__file__).resolve().parent.parent
EXTRACTED_DIR = BASE_DIR / "extracted" / "scripts"
OUTPUTS_DIR   = BASE_DIR / "outputs"

# =============================================================================
# IDENTITY LAYER
# Codename -> public name, sourced from:
#   - model path directory name (developer name)
#   - tagged_sounds filenames (public names)
# "?" prefix = uncertain, auto-added to Wander deck
# =============================================================================

CODENAME_TO_PUBLIC: dict[str, str] = {
    # Confirmed via model path + tagged_sounds cross-reference
    "hero_atlas":      "Abrams",
    "hero_inferno":    "Infernus",
    "hero_ghost":      "Lady Geist",
    "hero_orion":      "Grey Talon",
    "hero_tengu":      "Ivy",
    "hero_synth":      "Pocket",
    "hero_krill":      "Mo & Krill",
    "hero_nano":       "Seven",
    "hero_dynamo":     "Dynamo",
    "hero_forge":      "McGinnis",
    "hero_chrono":     "Paradox",
    "hero_bebop":      "Bebop",
    "hero_haze":       "Haze",
    "hero_kelvin":     "Kelvin",
    "hero_lash":       "Lash",
    "hero_mirage":     "Mirage",
    "hero_shiv":       "Shiv",
    "hero_viper":      "Vindicta",
    "hero_viscous":    "Viscous",
    "hero_warden":     "Warden",
    "hero_wraith":     "Wraith",
    "hero_yamato":     "Yamato",
    "hero_drifter":    "Drifter",
    "hero_frank":      "Frank",
    "hero_bookworm":   "Bookworm",
    "hero_doorman":    "Holliday",      # holliday_anim_sounds
    "hero_priest":     "Priest",
    "hero_familiar":   "Familiar",
    "hero_fencer":     "Fencer",
    "hero_necro":      "Necro",
    "hero_punkgoat":   "Punkgoat",
    "hero_werewolf":   "Wrecker",       # wrecker_anim_sounds - confirm with Wander
    "hero_vampirebat": "Calico",        # calico_anim_sounds  - confirm with Wander
    "hero_unicorn":    "Sinclair",      # sinclair_anim_sounds
    # Uncertain — no tagged_sounds entry, model path is the only clue
    "hero_astro":      "?Astro",
    "hero_magician":   "?Magician",
    "hero_gigawatt":   "?Gigawatt",
    "hero_hornet":     "?Hornet",
    "hero_boho":       "?Boho",
    "hero_druid":      "?Druid",
    "hero_graf":       "?GraffitiGirl",
    "hero_fortuna":    "?Fortuna",
    "hero_swan":       "?Swan",
    "hero_skyrunner":  "?Skyrunner",
    "hero_airheart":   "?Airheart",
    "hero_opera":      "?Opera",
}

# Hero IDs confirmed allocated then deleted (entire entry removed)
DELETED_IDS = [5, 9, 22, 23, 24, 26, 28, 29, 30, 32, 33, 34, 36, 37, 40, 41, 42, 43, 44, 45]

# =============================================================================
# IRI UTILITIES
# =============================================================================

def hero_iri(codename: str) -> str:
    public = CODENAME_TO_PUBLIC.get(codename, "")
    name = public.lstrip("?") if public else codename.replace("hero_", "").title()
    slug = re.sub(r"[^A-Za-z0-9]", "", name)
    return f"hero:{slug}"

def ability_iri(key: str) -> str:
    slug = key.replace("citadel_ability_", "").replace("citadel_weapon_", "weapon_")
    if slug.startswith("ability_"):
        slug = slug[len("ability_"):]
    slug = "".join(w.title() for w in slug.split("_"))
    return f"ability:{slug}"

def stat_iri(e_key: str) -> str:
    return f"stat:{e_key.lstrip('E')}"

def mv_iri(mv: str) -> str:
    slug = mv.replace("MODIFIER_VALUE_", "").replace("_", " ").title().replace(" ", "")
    return f"mv:{slug}"

def slot_iri(slot: str) -> str:
    slug = slot.replace("ESlot_", "").replace("_", "")
    return f"slot:{slug}"

def sf_iri(sf: str) -> str:
    slug = sf.replace("scale_function_", "").replace("_", " ").title().replace(" ", "")
    return f"sf:{slug}"

# =============================================================================
# PARSING HELPERS
# =============================================================================

def load_vdata(name: str) -> dict:
    path = EXTRACTED_DIR / name
    kb = path.stat().st_size // 1024
    print(f"  Parsing {name} ({kb} KB)...")
    text = path.read_text(encoding="utf-8")
    return KV3TextParser(text).parse()

def load_loc() -> dict[str, str]:
    loc: dict[str, str] = {}
    for subdir in LOC_SUBDIRS:
        p = LOC_BASE / subdir
        if not p.exists():
            continue
        for f in sorted(p.glob("*_english.txt")):
            try:
                loc.update(parse_kv1_localization(f.read_text(encoding="utf-8-sig")))
            except Exception:
                pass
    return loc

def resolve_loc(token: str, loc: dict) -> Optional[str]:
    if not token or not str(token).startswith("#"):
        return None
    return loc.get(str(token)[1:].lower())

def unwrap_flag(val: Any) -> Any:
    """Unwrap KV3 flagged value {'_flag': X, '_value': Y} -> Y."""
    if isinstance(val, dict) and "_flag" in val:
        return val.get("_value", val)
    return val

def get_str(d: dict, key: str) -> Optional[str]:
    v = d.get(key)
    v = unwrap_flag(v)
    return str(v) if v is not None else None

# =============================================================================
# PHASE B — ROSTER INTELLIGENCE
# =============================================================================

def build_roster(heroes_data: dict) -> list[dict]:
    skip = {"generic_data_type", "_include", "hero_base"}
    roster = []

    for key, val in heroes_data.items():
        if key in skip or not isinstance(val, dict):
            continue

        raw_model = get_str(val, "m_strModelName") or ""
        if "heroes_wip"     in raw_model: stage = "WIP"
        elif "heroes_staging" in raw_model: stage = "STAGING"
        elif "gen_man"       in raw_model: stage = "PLACEHOLDER"
        else:                              stage = "UNKNOWN"

        model_dir = raw_model.split("/")[-2] if "/" in raw_model else ""

        sel   = bool(val.get("m_bPlayerSelectable", False))
        dis   = bool(val.get("m_bDisabled", False))
        indev = bool(val.get("m_bInDevelopment", False))

        if   sel and not dis and not indev: status = "ACTIVE"
        elif sel and dis and indev:         status = "PIPELINE"
        elif not sel and dis and indev:     status = "TOMBSTONE"
        elif not sel and not dis:           status = "NPC_OR_STUB"
        else:                               status = "AMBIGUOUS"

        public = CODENAME_TO_PUBLIC.get(key, f"?{model_dir}")

        roster.append({
            "codename":    key,
            "hero_id":     int(val.get("m_HeroID", -1)),
            "public_name": public,
            "uncertain":   public.startswith("?"),
            "status":      status,
            "stage":       stage,
            "model_dir":   model_dir,
            "selectable":  sel,
            "disabled":    dis,
            "indev":       indev,
        })

    roster.sort(key=lambda r: r["hero_id"])
    return roster


def render_roster_md(roster: list[dict]) -> str:
    deleted_str = ", ".join(str(x) for x in DELETED_IDS)
    lines = [
        "# Nydus Roster Intelligence",
        "",
        f"> Source: `heroes.vdata`  |  Entities: {len(roster)}  |  Deleted IDs: {len(DELETED_IDS)}",
        "",
        "## Active Released",
        "",
        "| ID | Codename | Public Name | Stage |",
        "|---|---|---|---|",
    ]
    for r in roster:
        if r["status"] == "ACTIVE":
            flag = " ?" if r["uncertain"] else ""
            lines.append(f"| {r['hero_id']} | `{r['codename']}` | {r['public_name'].lstrip('?')}{flag} | {r['stage']} |")

    lines += ["", "## Pipeline Queue  *(sel=T, dis=T, indev=T)*", "",
              "| ID | Codename | Model Hint | Stage |", "|---|---|---|---|"]
    for r in roster:
        if r["status"] == "PIPELINE":
            lines.append(f"| {r['hero_id']} | `{r['codename']}` | `{r['model_dir']}` | {r['stage']} |")

    lines += ["", "## Tombstones  *(disabled, own model, no active successor)*", "",
              "| ID | Codename | Model Hint |", "|---|---|---|"]
    for r in roster:
        if r["status"] == "TOMBSTONE":
            lines.append(f"| {r['hero_id']} | `{r['codename']}` | `{r['model_dir']}` |")

    lines += ["", "## NPCs / Stubs", "",
              "| ID | Codename | Status |", "|---|---|---|"]
    for r in roster:
        if r["status"] in ("NPC_OR_STUB", "AMBIGUOUS"):
            lines.append(f"| {r['hero_id']} | `{r['codename']}` | {r['status']} |")

    lines += [
        "",
        "## Deleted Hero IDs (entries fully removed, not tombstoned)",
        "",
        f"`{deleted_str}`",
        "",
        f"20 heroes were allocated IDs and subsequently deleted from the data entirely.",
        "The gap cluster at IDs 22-45 suggests a single large design purge event.",
    ]
    return "\n".join(lines)

# =============================================================================
# PHASE C — STAT BRIDGE
# =============================================================================

def build_hero_bindings(heroes_data: dict) -> dict[str, dict[str, str]]:
    """hero_key -> {slot: ability_key}"""
    out: dict[str, dict[str, str]] = {}
    for key, val in heroes_data.items():
        if not isinstance(val, dict):
            continue
        bound = val.get("m_mapBoundAbilities", {})
        if isinstance(bound, dict) and bound:
            out[key] = {k: str(unwrap_flag(v)) for k, v in bound.items()}
    return out


def extract_stat_bridge(abilities_data: dict,
                        hero_bindings: dict[str, dict[str, str]]) -> list[dict]:
    """
    Walk every ability's m_mapAbilityProperties.
    Emit one edge per property that has either:
      - m_eProvidedPropertyType   (MODIFIER_VALUE_* edge)
      - m_subclassScaleFunction   (scaling stat edge)
    """
    # Invert: ability_key -> [(hero_key, slot)]
    ab_to_heroes: dict[str, list] = defaultdict(list)
    for hero_key, slots in hero_bindings.items():
        for slot, ab_key in slots.items():
            ab_to_heroes[ab_key].append((hero_key, slot))

    edges: list[dict] = []

    for ab_key, ab_val in abilities_data.items():
        if ab_key in ("generic_data_type", "_include") or not isinstance(ab_val, dict):
            continue

        props = ab_val.get("m_mapAbilityProperties", {})
        if not isinstance(props, dict):
            continue

        ab_class    = str(ab_val.get("_class", ab_key))
        hero_refs   = ab_to_heroes.get(ab_key) or [("(shared)", "(shared)")]

        for prop_name, prop_val in props.items():
            if not isinstance(prop_val, dict):
                continue

            raw_val   = prop_val.get("m_strValue")
            dis_val   = prop_val.get("m_strDisableValue")
            mv_type   = prop_val.get("m_eProvidedPropertyType")
            is_damage = bool(prop_val.get("m_bIsAbilityDamageProperty", False))

            # Open-world rule: skip disabled/zero values
            if raw_val is None:
                continue
            if str(raw_val) == str(dis_val):
                continue
            try:
                if float(raw_val) == 0.0 and not mv_type:
                    continue
            except (ValueError, TypeError):
                pass

            # Scale function
            sf_raw    = prop_val.get("m_subclassScaleFunction")
            sf        = unwrap_flag(sf_raw) if sf_raw else {}
            if not isinstance(sf, dict):
                sf = {}
            sf_class  = sf.get("_class")
            sf_stat   = sf.get("m_eSpecificStatScaleType")
            sf_factor = sf.get("m_flStatScale")
            sf_multi  = sf.get("m_vecScalingStats")

            # Skip props with no graph significance
            if not mv_type and not sf_class:
                continue

            for hero_key, slot in hero_refs:
                edges.append({
                    "ability":         ab_key,
                    "ability_class":   ab_class,
                    "property":        prop_name,
                    "base_value":      str(raw_val),
                    "modifier_value":  mv_type,
                    "scale_function":  sf_class,
                    "scale_stat":      sf_stat,
                    "scale_factor":    str(sf_factor) if sf_factor is not None else None,
                    "scale_stats_multi": sf_multi if isinstance(sf_multi, list) else None,
                    "is_damage":       is_damage,
                    "hero_binding":    hero_key,
                    "slot":            slot,
                })

    return edges


def render_bridge_summary(edges: list[dict]) -> str:
    mv_counts   = Counter(e["modifier_value"]  for e in edges if e["modifier_value"])
    sf_counts   = Counter((e["scale_function"], e["scale_stat"] or "")
                          for e in edges if e["scale_function"])
    hero_counts = Counter(e["hero_binding"]
                          for e in edges if e["hero_binding"] not in ("(shared)",))

    # One representative ability per (sf_class, sf_stat) pair
    sf_example: dict[tuple, str] = {}
    for e in edges:
        if e["scale_function"]:
            k = (e["scale_function"], e["scale_stat"] or "")
            if k not in sf_example and e["base_value"]:
                sf_example[k] = e["ability"]

    lines = [
        "# Stat Bridge Summary",
        "",
        f"> Total edges: **{len(edges)}**  |  "
        f"Unique MODIFIER_VALUE types: **{len(mv_counts)}**  |  "
        f"Unique scale functions: **{len(sf_counts)}**",
        "",
        "## MODIFIER_VALUE_* edge frequency  (top 30)",
        "",
        "| Modifier Value Type | Edges |",
        "|---|---|",
    ]
    for mv, cnt in mv_counts.most_common(30):
        lines.append(f"| `{mv}` | {cnt} |")

    lines += [
        "",
        "## Scale Function Inventory",
        "",
        "> Every row below is an unknown formula — calibration required.",
        "",
        "| Scale Function | Scaling Stat | Edges | Example Ability |",
        "|---|---|---|---|",
    ]
    for (sf, stat), cnt in sorted(sf_counts.items(), key=lambda x: -x[1]):
        ex = sf_example.get((sf, stat), "—")
        lines.append(f"| `{sf}` | `{stat}` | {cnt} | `{ex}` |")

    lines += [
        "",
        "## Per-hero edge counts",
        "",
        "| Hero Binding | Edges |",
        "|---|---|",
    ]
    for hero, cnt in hero_counts.most_common():
        lines.append(f"| `{hero}` | {cnt} |")

    return "\n".join(lines)

# =============================================================================
# WANDER QUESTION DECK
# =============================================================================

def generate_wander_deck(edges: list[dict], roster: list[dict]) -> str:
    """
    Elimination strategy — reduce to minimum question set:

    AUTO-ELIMINATED (no Wander needed):
      1. ability_recharge_time base=-1.0  → engine sentinel (1,238 entries)
      2. tech_damage + explicit stat + factor  → formula: base + factor*stat (140 entries)
      3. ability_charges with no stat/factor   → static integer charge counts (42 entries)

    VERIFICATION ONLY (1 question confirms the formula for all entries in class):
      4. scale_function_single_stat  → confirm formula structure once
      5. scale_function_tech_damage (no stat, factor varies) → confirm implied ETechPower
      6. scale_function_tech_duration / tech_range  → confirm formula once each

    FULL CALIBRATION (unknown combination method):
      7. scale_function_multi_stats → one per unique stat combo (7 combos)
      8. ability_recharge_time non-sentinel (43 entries, likely passthrough)

    IDENTITY:
      9. Uncertain hero public names
    """

    # --- Classify each (sf, stat) group ---
    SKIP_GROUPS: set[tuple] = set()   # auto-eliminated, no question
    VERIFY_ONLY: set[tuple] = set()   # 1 question, formula known pending confirmation

    # Rule 1: recharge_time sentinel — gather examples; skip group if ALL are sentinel
    recharge_key = ("scale_function_ability_recharge_time", "")
    rt_edges = [e for e in edges if e["scale_function"] == "scale_function_ability_recharge_time"]
    rt_real   = [e for e in rt_edges if str(e.get("base_value")) != "-1.0"]
    if not rt_real:
        SKIP_GROUPS.add(recharge_key)

    # Rule 2: tech_damage — two sub-cases
    #   (a) with explicit stat + factor: formula base+factor*stat is in the data → verify
    #   (b) no stat (implied ETechPower): one verification covers the family → verify
    # Both collapse to a single verification once formula is confirmed.
    # tech_damage: both explicit-ETechPower and implied cases confirm the same formula.
    # Keep explicit-ETechPower as canonical verify; skip the no-stat implied variant.
    VERIFY_ONLY.add(("scale_function_tech_damage", "ETechPower"))
    SKIP_GROUPS.add(("scale_function_tech_damage", ""))
    # Skip exotic 1-2-edge tech_damage variants (EStatsCount, EWeaponDamageScale)
    SKIP_GROUPS.add(("scale_function_tech_damage", "EStatsCount"))
    SKIP_GROUPS.add(("scale_function_tech_damage", "EWeaponDamageScale"))

    # Rule 3: ability_charges with no stat and integer base → static, no scaling
    ac_no_stat = all(
        not e.get("scale_stat") and not e.get("scale_factor")
        for e in edges if e.get("scale_function") == "scale_function_ability_charges"
    )
    if ac_no_stat:
        SKIP_GROUPS.add(("scale_function_ability_charges", ""))

    # Rule 4: single_stat — all variants share the same formula structure.
    # Collapse to ONE verification question (pick ETechCooldown as canonical).
    SINGLE_STAT_CANONICAL = ("scale_function_single_stat", "ETechCooldown")
    VERIFY_ONLY.add(SINGLE_STAT_CANONICAL)
    for e in edges:
        if e.get("scale_function") == "scale_function_single_stat":
            k = (e["scale_function"], e["scale_stat"] or "")
            if k != SINGLE_STAT_CANONICAL:
                SKIP_GROUPS.add(k)

    # Rule 5: tech_duration and tech_range — one verify each covers the family
    VERIFY_ONLY.add(("scale_function_tech_duration", ""))
    VERIFY_ONLY.add(("scale_function_tech_range", ""))
    # Skip sub-variants that are covered by the canonical verify
    SKIP_GROUPS.add(("scale_function_tech_duration", "ETechDuration"))
    SKIP_GROUPS.add(("scale_function_tech_duration", "EStatsCount"))
    SKIP_GROUPS.add(("scale_function_tech_range", "ETechRange"))

    # Rule 6: ultra-rare entries (≤2 edges globally) — not worth Wander's time
    from collections import Counter as _Counter
    edge_counts = _Counter((e.get("scale_function",""), e.get("scale_stat") or "") for e in edges)
    RARE_THRESHOLD = 2
    for k, cnt in edge_counts.items():
        sf = k[0]
        if cnt <= RARE_THRESHOLD and sf not in (
            "scale_function_multi_stats",        # always keep — combination method unknown
            "scale_function_ability_recharge_time",
        ):
            SKIP_GROUPS.add(k)

    # --- Build best example per (sf, stat) group ---
    sf_examples: dict[tuple, dict] = {}
    for e in edges:
        if not e["scale_function"]:
            continue
        # For recharge_time, only use non-sentinel examples
        if e["scale_function"] == "scale_function_ability_recharge_time" and str(e.get("base_value")) == "-1.0":
            continue
        k = (e["scale_function"], e["scale_stat"] or "")
        if k in SKIP_GROUPS:
            continue
        if k not in sf_examples and e["base_value"] and e["ability"] != "(shared)":
            sf_examples[k] = e
        elif k in sf_examples:
            # prefer hero-bound over shared
            if (sf_examples[k]["hero_binding"] in ("(shared)", None)
                    and e["hero_binding"] not in ("(shared)", None)):
                sf_examples[k] = e

    verify_qs = {k: v for k, v in sf_examples.items() if k in VERIFY_ONLY}
    full_qs   = {k: v for k, v in sf_examples.items() if k not in VERIFY_ONLY}

    eliminated_count = len(SKIP_GROUPS) + (
        sum(1 for e in edges
            if e.get("scale_function") == "scale_function_ability_recharge_time"
            and str(e.get("base_value")) == "-1.0")
    )

    uncertain = [r for r in roster if r["status"] == "ACTIVE" and r["uncertain"]]

    lines = [
        "# Nydus — Calibration Questions for Wander",
        "",
        "> Hi Wander — only questions that cannot be answered from the data appear here.",
        "> No data science knowledge needed; just in-game observation.",
        "> Answer in whatever form is convenient. We handle the math.",
        "",
        "---",
        "",
        "## What we already know  (eliminated)",
        "",
        "| Category | Entries | How we solved it |",
        "|---|---|---|",
        f"| `ability_recharge_time` base=`-1.0` | 1,238 | Engine sentinel — fire rate from weapon stats |",
        f"| `tech_damage` + explicit stat + factor | 140 | Formula `base + factor × stat` in the data |",
        f"| `ability_charges` (static) | 42 | Integer charge counts, no scaling |",
        "",
        "---",
        "",
        f"## Part A — Formula Verifications  ({len(verify_qs)} questions)",
        "",
        "> We have the data — we just need one confirmed output to lock in the formula.",
        "> Set Training Mode stat slider to each value; read the tooltip.",
        "",
    ]

    for i, ((sf_class, sf_stat), ex) in enumerate(sorted(verify_qs.items()), 1):
        ability_display = (ex["ability"]
                           .replace("citadel_ability_", "")
                           .replace("citadel_weapon_", "")
                           .replace("_", " ").title())
        hero_display = (CODENAME_TO_PUBLIC.get(ex["hero_binding"], ex["hero_binding"])
                        .lstrip("?") if ex["hero_binding"] else "(shared)")
        sf_short = sf_class.replace("scale_function_", "").replace("_", " ")
        factor_note = f" (scale factor in data: {ex['scale_factor']})" if ex.get("scale_factor") else ""
        formula_hint = f"`base + factor × {sf_stat or 'stat'}`" if ex.get("scale_factor") else f"`base × f({sf_stat})`"

        lines += [
            f"### V{i} — `{sf_short}` on `{sf_stat}`",
            "",
            f"**Our formula hypothesis**: {formula_hint}{factor_note}",
            "",
            f"| Field | Value |",
            f"|---|---|",
            f"| Hero | {hero_display} |",
            f"| Ability | {ability_display} |",
            f"| Property | {ex['property']} |",
            f"| Base value (stat=0) | **{ex['base_value']}** |",
            "",
            "**Verify at these stat values:**",
            "",
            "| Stat Value | Tooltip shows |",
            "|---|---|",
            f"| 0 | *(should be {ex['base_value']})* |",
            "| 42 | ? |",
            "| 100 | ? |",
            "",
        ]

    lines += [
        "---",
        "",
        f"## Part B — Unknown Formulas  ({len(full_qs)} questions)",
        "",
        "> These scale functions combine stats in ways not derivable from the data.",
        "> Full calibration needed — 4 data points per question.",
        "",
    ]

    q_num = 1
    for (sf_class, sf_stat), ex in sorted(full_qs.items()):
        ability_display = (ex["ability"]
                           .replace("citadel_ability_", "")
                           .replace("citadel_weapon_", "")
                           .replace("_", " ").title())
        hero_display = (CODENAME_TO_PUBLIC.get(ex["hero_binding"], ex["hero_binding"])
                        .lstrip("?") if ex["hero_binding"] else "(shared)")
        sf_short = sf_class.replace("scale_function_", "").replace("_", " ")
        stat_list = ex.get("scale_stats_multi") or ([sf_stat] if sf_stat else ["(implied from function name)"])
        factor_note = f"  *(data factor: {ex['scale_factor']})*" if ex.get("scale_factor") else ""

        lines += [
            f"### Q{q_num} — `{sf_short}`",
            "",
            f"| Field | Value |",
            f"|---|---|",
            f"| Stats involved | `{'`, `'.join(stat_list)}` |",
            f"| Hero | {hero_display} |",
            f"| Ability | {ability_display} |",
            f"| Property | {ex['property']} |",
            f"| Base value (no stats) | **{ex['base_value']}**{factor_note} |",
            "",
            "**Fill in observed values:**",
            "",
            "| Stat Value | What tooltip / dummy shows |",
            "|---|---|",
            f"| 0 | *(baseline — should be {ex['base_value']})* |",
            "| 42 | ? |",
            "| 100 | ? |",
            "| 200 | ? |",
            "",
        ]
        q_num += 1

    lines += [
        "---",
        "",
        f"## Part C — Hero Identity  ({len(uncertain)} questions)",
        "",
        "> Some heroes have developer codenames only — no confirmed public name.",
        "",
    ]
    for i, r in enumerate(uncertain, 1):
        hint = (r["model_dir"].replace("_", " ").title()
                if r["model_dir"] not in ("gen_man", "") else "(no distinct model)")
        lines += [
            f"### HI{i} — `{r['codename']}`  (ID #{r['hero_id']})  |  model: **{hint}**  |  stage: {r['stage']}",
            "",
            "Public name, or any recognition from playtests?",
            "",
            "**Answer**: _____________________",
            "",
        ]

    lines += [
        "---",
        "",
        "## Part D — Mechanics  (5 questions)",
        "",
        "**M1**: Can you buy two different items that both grant Bullet Armor and receive "
        "full value from both, or does one cap out / get diminished?",
        "",
        "**Answer**: _____________________",
        "",
        "**M2**: Is there a hard cap on Cooldown Reduction? If yes, what is it?",
        "",
        "**Answer**: _____________________",
        "",
        "**M3**: Lifesteal — do multiple lifesteal items add together directly, "
        "or does stacking give diminishing returns?",
        "",
        "**Answer**: _____________________",
        "",
        "**M4**: The data shows exactly one hero with a `Rage` resource type (not mana/none). "
        "Which hero, and how does Rage build / drain?",
        "",
        "**Answer**: _____________________",
        "",
        "**M5**: For Spirit (tech) power scaling — does the damage formula feel linear "
        "across the whole range, or does it cap/curve at high values?",
        "",
        "**Answer**: _____________________",
        "",
        "---",
        "",
        "*Thank you Wander. Every answer closes a formula gap between what the*",
        "*data declares and what the game actually computes.*",
    ]

    return "\n".join(lines)

# =============================================================================
# PHASE A — ABRAMS VERTICAL SLICE — TURTLE
# =============================================================================

# DID_SWAP_TARGET: replace http://nydus.gg/ontology# with did:key:z6Mk...#ward/ on publish
TTL_PREFIXES = """\
@base            <http://nydus.gg/source/> .
@prefix nydus:   <http://nydus.gg/ontology#> .
@prefix hero:    <http://nydus.gg/ontology#hero/> .
@prefix ability: <http://nydus.gg/ontology#ability/> .
@prefix stat:    <http://nydus.gg/ontology#stat/> .
@prefix mv:      <http://nydus.gg/ontology#mv/> .
@prefix slot:    <http://nydus.gg/ontology#slot/> .
@prefix sf:      <http://nydus.gg/ontology#sf/> .
@prefix cat:     <http://nydus.gg/ontology#cat/> .
@prefix stage:   <http://nydus.gg/ontology#stage/> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix schema:  <http://schema.org/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .
"""

def _tstr(s: str) -> str:
    escaped = str(s).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'

def _tstr_lang(s: str, lang: str = "en") -> str:
    return f'{_tstr(s)}@{lang}'

def _tint(v) -> str:
    return f'"{int(float(str(v)))}"^^xsd:integer'

def _tdec(v) -> str:
    try:
        return f'"{float(str(v)):.6g}"^^xsd:decimal'
    except (ValueError, TypeError):
        return _tstr(str(v))

def _tbool(v) -> str:
    return "true" if v else "false"


# Wheat starting stats to model (from rubric.md)
STAT_WHEAT = [
    "EMaxMoveSpeed", "ESprintSpeed", "EMaxHealth", "EBaseHealthRegen",
    "EStamina", "EStaminaRegenPerSecond", "EWeaponPower", "EBulletDamage",
    "EFireRate", "EClipSize", "EReloadSpeed",
    "ELightMeleeDamage", "EHeavyMeleeDamage",
    "EBulletLifesteal", "EBulletArmorDamageReduction", "ETechArmorDamageReduction",
    "ETechDuration", "ETechRange",
]

# Mechanical properties to extract from m_mapAbilityProperties
MECH_PROPS = [
    "AbilityCooldown", "AbilityDuration", "AbilityCastRange", "AbilityCharges",
    "Damage", "HealAmount", "HealPercent", "MaxStacks",
    "TechPower", "WeaponPower", "StunDuration",
    "SlowPercent", "SlowDuration", "SpeedInitial",
    "ChargeSpeedMax", "ChargeRadius", "DamageTaken",
    "MoveSpeedBonus", "HealthRegenBonus", "DamageBuff",
]

# Property category map: raw property name -> (primary, secondary_or_None, determinism, note_or_None)
# Categories are shared semantic nodes — the cross-ability comparison anchor.
# Low-determinism entries have secondary category + explanatory note.
PROPERTY_CATEGORY_MAP: dict[str, tuple] = {
    # High-determinism: single clear category
    "AbilityCooldown":              ("Cooldown",    None,        "high", None),
    "AbilityDuration":              ("Duration",    None,        "high", None),
    "AbilityCastRange":             ("Range",       None,        "high", None),
    "AbilityCharges":               ("Charges",     None,        "high", None),
    "Damage":                       ("Damage",      None,        "high", None),
    "DamageBuff":                   ("Damage",      None,        "high", None),
    "DamageTaken":                  ("Damage",      None,        "high", None),
    "HealAmount":                   ("Healing",     None,        "high", None),
    "HealPercent":                  ("Healing",     None,        "high", None),
    "HealthRegenBonus":             ("Healing",     None,        "high", None),
    "MaxStacks":                    ("Stack",       None,        "high", None),
    "MoveSpeedBonus":               ("Speed",       None,        "high", None),
    "SpeedInitial":                 ("Speed",       None,        "high", None),
    "ChargeSpeedMax":               ("Speed",       None,        "high", None),
    "ChargeRadius":                 ("Range",       None,        "high", None),
    "StunDuration":                 ("Duration",    None,        "high", None),
    "TechPower":                    ("Stat",        None,        "high", None),
    "WeaponPower":                  ("Weapon",      None,        "high", None),
    # Low-determinism: dual-mechanic or scope ambiguity
    "SlowPercent":                  ("Speed",       None,        "low",
                                     "Speed debuff — reduces target movement by percentage; filed under Speed as the affected stat"),
    "SlowDuration":                 ("Duration",    "Speed",     "low",
                                     "Duration of a speed debuff — temporal in form, speed in function"),
    "AbilityCooldownBetweenCharge": ("Cooldown",    "Charges",   "low",
                                     "Rate between charge uses — cooldown in form, charge mechanic in function"),
    "WeaponDamageBonus":            ("Damage",      "Weapon",    "low",
                                     "Weapon-specific damage modifier; may not be additive with base ability damage"),
    "RegenIncomingDamagePercent":   ("Healing",     "Damage",    "low",
                                     "Converts a fraction of incoming damage to health regen — dual-mechanic"),
    "WeaponPowerIncreaseDuration":  ("Duration",    "Weapon",    "low",
                                     "Duration scoped to a weapon power buff, not the ability itself"),
}

# All unique category names referenced in the map (plus Unknown for unmapped properties)
_ALL_CATEGORIES: set[str] = {"Unknown"}
for _prim, _sec, _det, _note in PROPERTY_CATEGORY_MAP.values():
    _ALL_CATEGORIES.add(_prim)
    if _sec:
        _ALL_CATEGORIES.add(_sec)

# Human labels for each category node
CATEGORY_LABELS: dict[str, str] = {
    "Cooldown":  "Cooldown",
    "Damage":    "Damage",
    "Duration":  "Duration",
    "Range":     "Range",
    "Speed":     "Speed",
    "Charges":   "Charges",
    "Healing":   "Healing",
    "Stack":     "Stack",
    "Weapon":    "Weapon",
    "Stat":      "Stat Modifier",
    "Unknown":   "Unknown",
}

# ============================================================================
# DISPLAY-LABEL RESOLVERS
#
# Deadlock ships English localization tokens for most stats and ability-property
# names (e.g. "TechPower_label" -> "Spirit Power", "AbilityDuration_label" ->
# "Duration"). Slots and scale-function codes have no official translation, so
# we hand-map them. All loc lookups are lowercase; _resolve() tries several
# token patterns in order before falling back to a prettified internal name.
# ============================================================================

SLOT_LABEL_MAP: dict[str, str] = {
    # Keys are the IRI local-name produced by slot_iri() (ESlot_ stripped,
    # underscores removed). Values are what Deadlock tooltips/HUD display.
    "WeaponPrimary":    "Primary Weapon",
    "WeaponSecondary":  "Secondary Weapon",
    "WeaponMelee":      "Melee",
    "Signature1":       "Ability 1",
    "Signature2":       "Ability 2",
    "Signature3":       "Ability 3",
    "Signature4":       "Ultimate",
    "AbilityInnate1":   "Innate 1",
    "AbilityInnate2":   "Innate 2",
    "AbilityInnate3":   "Innate 3",
    "AbilityInnate4":   "Innate 4",
    "AbilityMantle":    "Mantle",
    "AbilityJump":      "Jump",
    "AbilityDoubleJump":"Double Jump",
    "AbilityCrouch":    "Crouch",
    "AbilitySlide":     "Slide",
    "AbilityZipLine":   "Zip Line",
    "AbilityZipLineBoost": "Zip Line Boost",
    "AbilityClimbRope": "Climb Rope",
    "AbilityPing":      "Ping",
    "AbilityVault":     "Vault",
}

SF_LABEL_MAP: dict[str, str] = {
    # Scale function codes -> human-readable display.
    "scale_function_tech_damage":         "Scales with Spirit Power",
    "scale_function_tech_range":          "Scales with Spirit Range",
    "scale_function_tech_duration":       "Scales with Spirit Duration",
    "scale_function_light_melee_damage":  "Scales with Light Melee",
    "scale_function_heavy_melee_damage":  "Scales with Heavy Melee",
    "scale_function_weapon_damage":       "Scales with Weapon Damage",
    "scale_function_multi_stats":         "Scales with Multiple Stats",
    "scale_function_single_stat":         "Scales with a Single Stat",
    "scale_function_tech_cooldown":       "Scales with Spirit Cooldown",
    "scale_function_ability_charges":     "Scales with Ability Charges",
    "scale_function_ability_cooldown":    "Scales with Ability Cooldown",
    "scale_function_ability_duration":    "Scales with Ability Duration",
    "scale_function_weapon_falloff":      "Scales with Weapon Falloff",
    "scale_function_no_scaling":          "No Scaling",
}


def _prettify(name: str) -> str:
    """CamelCase / snake_case / lowercase -> 'Title Case With Spaces'."""
    if not name:
        return name
    # snake_case
    if "_" in name:
        return " ".join(w.capitalize() for w in name.replace("_", " ").split())
    # all lowercase single word -> Title
    if name.islower():
        return name.capitalize()
    # CamelCase: split on capital-letter boundaries
    out = []
    for i, ch in enumerate(name):
        if i > 0 and ch.isupper() and not name[i - 1].isupper():
            out.append(" ")
        out.append(ch)
    return "".join(out).strip()


def _clean_loc_label(s: Optional[str]) -> Optional[str]:
    """Return s if it looks like a display label; None if it looks like a token.

    Loc dicts occasionally contain engine-internal token strings as values
    (e.g. 'Sandbox_Tutorial_Controls_task_AirDash') that leak through when a
    shared key happens to collide. Reject anything that contains an underscore —
    real Deadlock display names never do. Also title-case bare lowercase
    single-word hits ('mantle' -> 'Mantle').
    """
    if not s or not isinstance(s, str):
        return None
    if "_" in s:
        return None
    s = s.strip()
    if not s:
        return None
    if s.islower() and " " not in s:
        return s.title()
    return s


def resolve_stat_label(e_key: str, loc: dict) -> str:
    """stat_iri input -> human label. e_key is the raw enum like 'ETechPower' or 'TechPower'."""
    name = e_key.lstrip("E")
    key = name.lower()
    for tok in (f"{key}_label", f"statdesc_{key}", f"statdesc_{key}_postvalue_label"):
        hit = _clean_loc_label(loc.get(tok))
        if hit:
            return hit
    return _prettify(name)


def resolve_property_label(internal_name: str, loc: dict) -> str:
    """AbilityProperty internalName -> human label."""
    key = internal_name.lower()
    for tok in (f"{key}_label", f"statdesc_{key}", f"statdesc_{key}_postvalue_label"):
        hit = _clean_loc_label(loc.get(tok))
        if hit:
            return hit
    return _prettify(internal_name)


def resolve_slot_label(slot_local: str) -> str:
    """slot_iri local-name (e.g. 'WeaponPrimary') -> human label."""
    return SLOT_LABEL_MAP.get(slot_local, _prettify(slot_local))


def resolve_sf_label(sf_code: str) -> str:
    """Raw scale-function code (e.g. 'scale_function_tech_damage') -> human label."""
    return SF_LABEL_MAP.get(sf_code, _prettify(sf_code.replace("scale_function_", "")))


def resolve_ability_label(ab_key: str, loc: dict) -> str:
    """Ability internal key (e.g. 'citadel_ability_jump') -> human label ('Jump')."""
    key_short = ab_key
    for _p in ("citadel_ability_", "citadel_weapon_", "ability_"):
        if key_short.startswith(_p):
            key_short = key_short[len(_p):]
            break
    return (
        _clean_loc_label(loc.get(ab_key))
        or _clean_loc_label(loc.get(ab_key.replace("citadel_ability_", "")))
        or _clean_loc_label(loc.get(ab_key.replace("citadel_weapon_", "")))
        or _prettify(key_short)
    )


def resolve_mv_label(mv_code: str, loc: dict) -> str:
    """MODIFIER_VALUE_* enum -> human label."""
    name = mv_code.replace("MODIFIER_VALUE_", "")
    key = name.lower().replace("_", "")
    for tok in (f"{key}_label", f"{name.lower()}_label"):
        hit = _clean_loc_label(loc.get(tok))
        if hit:
            return hit
    return _prettify(name)


def _ability_property_block(
    prop_name: str,
    raw: Any,
    sf_stat: Optional[str],
    sf_factor: Any,
    sf_class: Optional[str],
    sf_multi: Any,
    mv: Optional[str],
    loc: dict,
) -> str:
    """Return a nydus:hasProperty [...] ; block string for one ability property."""
    prop_label = resolve_property_label(prop_name, loc)
    lines = [
        "    nydus:hasProperty [",
        "        a nydus:AbilityProperty ;",
        f"        rdfs:label {_tstr_lang(prop_label)} ;",
        f"        nydus:internalName {_tstr(prop_name)} ;",
        f"        nydus:baseValue {_tdec(raw)} ;",
    ]

    cat_info = PROPERTY_CATEGORY_MAP.get(prop_name)
    if cat_info:
        prim, sec, det, note = cat_info
        lines.append(f"        nydus:primaryCategory cat:{prim} ;")
        if sec:
            lines.append(f"        nydus:secondaryCategory cat:{sec} ;")
        lines.append(f"        nydus:categoryDeterminism {_tstr(det)} ;")
        if note:
            lines.append(f"        nydus:categoryNote {_tstr(note)} ;")
    else:
        lines.append(f"        nydus:primaryCategory cat:Unknown ;")
        lines.append(f"        nydus:categoryDeterminism {_tstr('low')} ;")
        lines.append(f"        nydus:categoryNote {_tstr('Property not in category map — manual review required')} ;")

    if sf_stat:
        lines.append(f"        nydus:scalesStat {stat_iri(sf_stat)} ;")
    if sf_factor is not None:
        lines.append(f"        nydus:scaleFactor {_tdec(sf_factor)} ;")
    if sf_class:
        lines.append(f"        nydus:scaleFunction {_tstr(sf_class)} ;")
    if isinstance(sf_multi, list):
        for ms in sf_multi:
            lines.append(f"        nydus:scalesStat {stat_iri(str(ms))} ;")
    if mv:
        lines.append(f"        nydus:providesModifierType {mv_iri(str(mv))} ;")

    lines.append("    ] ;")
    return "\n".join(lines)


def generate_turtle(heroes_data: dict,
                    abilities_data: dict,
                    loc: dict,
                    hero_key: str = "hero_atlas") -> str:
    hero_val = heroes_data.get(hero_key, {})
    h_iri    = hero_iri(hero_key)

    bound = hero_val.get("m_mapBoundAbilities", {})
    if not isinstance(bound, dict):
        bound = {}
    # Unwrap any flagged values in bindings
    bound = {k: str(unwrap_flag(v)) for k, v in bound.items()}

    sig_ability_keys = [v for k, v in bound.items()
                        if "Signature" in k or "Innate" in k]

    stats = hero_val.get("m_mapStartingStats", {})

    # --- Resolve localization ---
    sort_name   = (resolve_loc(get_str(hero_val, "m_strHeroSortName"), loc)
                   or CODENAME_TO_PUBLIC.get(hero_key, "").lstrip("?")
                   or hero_key)
    search_name = resolve_loc(get_str(hero_val, "m_strHeroSearchName"), loc)
    tags_raw    = hero_val.get("m_vecHeroTags", [])
    tag_labels  = []
    if isinstance(tags_raw, list):
        for t in tags_raw:
            resolved = resolve_loc(str(unwrap_flag(t)), loc)
            if resolved:
                tag_labels.append(resolved)

    out: list[str] = [TTL_PREFIXES]

    # ================================================================
    # PROPERTY CATEGORY NODES  (shared semantic anchors)
    # ================================================================
    out.append(f"# {'='*60}")
    out.append("# Property Categories  (cross-ability comparison anchors)")
    out.append(f"# {'='*60}\n")
    for cat_name in sorted(_ALL_CATEGORIES):
        label = CATEGORY_LABELS.get(cat_name, cat_name)
        out.append(f"cat:{cat_name}  a nydus:PropertyCategory ; rdfs:label {_tstr_lang(label)} .")
    out.append("")

    # ================================================================
    # HERO
    # ================================================================
    out.append(f"# {'='*60}")
    out.append(f"# Hero: {sort_name}  ({hero_key}  ID={hero_val.get('m_HeroID', '?')})")
    out.append(f"# {'='*60}\n")

    hero_lines = [f"{h_iri}"]
    hero_lines.append(f"    a nydus:Hero ;")
    hero_lines.append(f"    rdfs:label {_tstr_lang(sort_name)} ;")
    if search_name:
        hero_lines.append(f"    skos:altLabel {_tstr_lang(search_name)} ;")
    for tl in tag_labels:
        hero_lines.append(f"    nydus:heroTag {_tstr(tl)} ;")
    hero_lines.append(f"    schema:identifier {_tint(hero_val.get('m_HeroID', 0))} ;")
    hero_lines.append(f"    nydus:internalKey {_tstr(hero_key)} ;")
    hero_lines.append(f"    nydus:developerStage stage:WIP ;")
    hero_lines.append(f"    nydus:isPlayerSelectable {_tbool(hero_val.get('m_bPlayerSelectable', False))} ;")
    hero_lines.append(f"    nydus:isDisabled {_tbool(hero_val.get('m_bDisabled', False))} ;")
    hero_lines.append(f"    nydus:complexity {_tint(hero_val.get('m_nComplexity', 0))} ;")

    # Enums
    for field, pred in [("m_eHeroType", "nydus:heroType"),
                         ("m_eAbilityResourceType", "nydus:abilityResourceType")]:
        v = hero_val.get(field)
        if v:
            hero_lines.append(f"    {pred} {_tstr(str(v))} ;")

    # Slot -> ability bindings (all slots)
    for slot, ab_key in sorted(bound.items()):
        slot_local = slot_iri(slot).split(":", 1)[-1]
        slot_lbl = resolve_slot_label(slot_local)
        ab_lbl   = resolve_ability_label(ab_key, loc)
        bind_label = ab_lbl if slot_lbl == ab_lbl else f"{slot_lbl}: {ab_lbl}"
        hero_lines.append(
            f"    nydus:hasAbilityInSlot [ "
            f"rdfs:label {_tstr_lang(bind_label)} ; "
            f"nydus:slot {slot_iri(slot)} ; "
            f"nydus:ability {ability_iri(ab_key)} ] ;"
        )

    # Starting stats (wheat keys only)
    if isinstance(stats, dict):
        for sk in STAT_WHEAT:
            raw = stats.get(sk)
            if raw is None:
                continue
            try:
                fv = float(str(raw))
            except (ValueError, TypeError):
                continue
            if fv == 0.0:
                continue
            hero_lines.append(f"    nydus:starting{sk.lstrip('E')} {_tdec(raw)} ;")

    hero_lines.append(f"    prov:wasDerivedFrom <scripts/heroes.vdata> .")
    out.append("\n".join(hero_lines))
    out.append("")

    # ================================================================
    # ABILITIES  (signature + innate slots)
    # ================================================================
    for ab_key in sig_ability_keys:
        ab_val = abilities_data.get(ab_key)
        if not isinstance(ab_val, dict):
            continue

        a_iri     = ability_iri(ab_key)
        ab_props  = ab_val.get("m_mapAbilityProperties", {})
        upgrades  = ab_val.get("m_vecAbilityUpgrades",   [])
        ab_type   = str(ab_val.get("m_eAbilityType",     ""))
        ab_activ  = str(ab_val.get("m_eAbilityActivation", ""))

        ab_label = resolve_ability_label(ab_key, loc)

        out.append(f"# Ability: {ab_label}  ({ab_key})")
        ab_lines = [f"{a_iri}"]
        ab_lines.append(f"    a nydus:Ability ;")
        ab_lines.append(f"    rdfs:label {_tstr_lang(ab_label)} ;")
        ab_lines.append(f"    nydus:internalKey {_tstr(ab_key)} ;")
        if ab_type:
            ab_lines.append(f"    nydus:abilityType {_tstr(ab_type)} ;")
        if ab_activ:
            ab_lines.append(f"    nydus:activationType {_tstr(ab_activ)} ;")

        # Mechanical properties as categorized AbilityProperty blank nodes
        if isinstance(ab_props, dict):
            for prop_name in MECH_PROPS:
                pv = ab_props.get(prop_name)
                if not isinstance(pv, dict):
                    continue

                raw  = pv.get("m_strValue")
                dis  = pv.get("m_strDisableValue")
                if raw is None or str(raw) == str(dis):
                    continue
                try:
                    if float(str(raw)) == 0.0:
                        continue
                except (ValueError, TypeError):
                    pass

                sf_raw    = pv.get("m_subclassScaleFunction")
                sf        = unwrap_flag(sf_raw) if sf_raw else {}
                if not isinstance(sf, dict):
                    sf = {}
                sf_class  = sf.get("_class")
                sf_stat   = sf.get("m_eSpecificStatScaleType")
                sf_factor = sf.get("m_flStatScale")
                sf_multi  = sf.get("m_vecScalingStats")
                mv        = pv.get("m_eProvidedPropertyType")

                ab_lines.append(
                    _ability_property_block(prop_name, raw, sf_stat, sf_factor, sf_class, sf_multi, mv, loc)
                )

        # Upgrade tiers as first-class AbilityUpgrade blank nodes
        if isinstance(upgrades, list):
            for tier_idx, tier in enumerate(upgrades, 1):
                if not isinstance(tier, dict):
                    continue
                pups = tier.get("m_vecPropertyUpgrades", [])
                if not isinstance(pups, list):
                    continue
                for pu in pups:
                    if not isinstance(pu, dict):
                        continue
                    pname = pu.get("m_strPropertyName", "")
                    bonus = pu.get("m_strBonus", "")
                    if pname and bonus is not None:
                        # Strip leading 'upg<N>_' — that level is captured in
                        # nydus:upgradeLevel; what's left is the property.
                        pname_str = str(pname)
                        prop_core = re.sub(r"^upg\d+_", "", pname_str)
                        prop_label = resolve_property_label(prop_core, loc)
                        ab_lines.extend([
                            f"    nydus:hasUpgrade [",
                            f"        a nydus:AbilityUpgrade ;",
                            f"        rdfs:label {_tstr_lang(prop_label)} ;",
                            f"        nydus:upgradeLevel {_tint(tier_idx)} ;",
                            f"        nydus:modifiesProperty {_tstr(pname_str)} ;",
                            f"        nydus:bonusValue {_tstr(str(bonus))} ;",
                            f"    ] ;",
                        ])

        ab_lines.append(f"    prov:wasDerivedFrom <scripts/abilities.vdata> .")
        out.append("\n".join(ab_lines))
        out.append("")

    ttl_text = "\n".join(out)

    # ================================================================
    # VOCAB LABELS for referenced stat/slot/sf/mv IRIs.
    # Scan the finished TTL text, collect every IRI in these prefixes,
    # and emit one rdfs:label triple per distinct IRI so the viewer
    # and any other consumer get human names.
    # ================================================================
    vocab_lines: list[str] = []

    stats_used = sorted(set(re.findall(r"stat:(\w+)", ttl_text)))
    slots_used = sorted(set(re.findall(r"slot:(\w+)", ttl_text)))
    sfs_used_raw = sorted({s for s in re.findall(r"nydus:scaleFunction\s+\"([^\"]+)\"", ttl_text)})
    mvs_used = sorted(set(re.findall(r"mv:(\w+)", ttl_text)))

    # Ability IRIs referenced via slot bindings but NOT already declared with
    # rdf:type (i.e. shared innates / weapons not in sig_ability_keys). Emit a
    # label stub so the viewer shows "Primary Weapon" instead of "WeaponInfernoSet".
    abilities_declared = set(re.findall(r"^ability:(\w+)\s", ttl_text, re.MULTILINE))
    ability_stubs: list[tuple[str, str]] = []
    for ab_key in bound.values():
        a_iri_local = ability_iri(ab_key).split(":", 1)[-1]
        if a_iri_local in abilities_declared:
            continue
        ability_stubs.append((a_iri_local, resolve_ability_label(ab_key, loc)))

    if stats_used or slots_used or sfs_used_raw or mvs_used or ability_stubs:
        vocab_lines.append(f"# {'='*60}")
        vocab_lines.append("# Vocabulary labels  (stat / slot / scale-function / modifier / shared abilities)")
        vocab_lines.append(f"# {'='*60}\n")

    for a_local, lbl in sorted(ability_stubs):
        # Note: no `a nydus:Ability` — full Ability shape requires internalKey,
        # abilityType, etc., which we don't have for shared innates. The viewer
        # infers Ability styling from the `ability:` IRI prefix.
        vocab_lines.append(f"ability:{a_local}  rdfs:label {_tstr_lang(lbl)} .")
    for name in stats_used:
        lbl = resolve_stat_label(name, loc)
        vocab_lines.append(f"stat:{name}  a nydus:Stat ; rdfs:label {_tstr_lang(lbl)} .")
    for name in slots_used:
        lbl = resolve_slot_label(name)
        vocab_lines.append(f"slot:{name}  a nydus:Slot ; rdfs:label {_tstr_lang(lbl)} .")
    for name in mvs_used:
        # Recover the original MODIFIER_VALUE_* form by searching the TTL
        vocab_lines.append(f"mv:{name}  a nydus:ModifierValue ; rdfs:label {_tstr_lang(_prettify(name))} .")
    # Scale functions: also declare a ScaleFunction IRI per referenced sf_class
    # so they're reachable as graph nodes, not just literals.
    for sf_code in sfs_used_raw:
        sf_local = sf_iri(sf_code).split(":", 1)[-1]
        lbl = resolve_sf_label(sf_code)
        vocab_lines.append(f"sf:{sf_local}  a nydus:ScaleFunction ; rdfs:label {_tstr_lang(lbl)} .")

    if vocab_lines:
        vocab_lines.append("")
        return ttl_text + "\n" + "\n".join(vocab_lines)
    return ttl_text

# =============================================================================
# SHACL VALIDATION
# =============================================================================

def validate_ttl(data_path: Path, shapes_path: Path) -> bool:
    """Validate a Turtle file against SHACL shapes. Returns True if conformant."""
    try:
        from pyshacl import validate
    except ImportError:
        print("      [SHACL] pyshacl not installed — skipping validation")
        print("              pip install pyshacl")
        return True

    conforms, _, results_text = validate(
        str(data_path),
        shacl_graph=str(shapes_path),
        inference="rdfs",
        abort_on_first=False,
        serialize_report_graph=False,
    )
    if conforms:
        print(f"      [SHACL] {data_path.name} CONFORMS ✓")
    else:
        print(f"      [SHACL] {data_path.name} VIOLATIONS:")
        for line in results_text.splitlines():
            if line.strip():
                print(f"        {line}")
    return conforms


# =============================================================================
# MAIN
# =============================================================================

def main():
    OUTPUTS_DIR.mkdir(exist_ok=True)

    print("=" * 55)
    print("  Nydus Graph Builder — C -> B -> A")
    print("=" * 55)

    print("\n[1/5] Loading localization...")
    loc = load_loc()
    print(f"      {len(loc):,} tokens")

    print("\n[2/5] Parsing heroes.vdata...")
    heroes_data = load_vdata("heroes.vdata")
    hero_count  = sum(1 for k in heroes_data if k.startswith("hero_") and k != "hero_base")
    print(f"      {hero_count} hero entities")

    print("\n[3/5] Parsing abilities.vdata...")
    abilities_data = load_vdata("abilities.vdata")
    ab_count = sum(1 for k in abilities_data
                   if k not in ("generic_data_type", "_include"))
    print(f"      {ab_count} ability/item entities")

    print("\n[4/5] Building graph outputs...")

    # Phase B
    roster = build_roster(heroes_data)
    (OUTPUTS_DIR / "roster.jsonl").write_text(
        "\n".join(json.dumps(r) for r in roster), encoding="utf-8")
    (OUTPUTS_DIR / "roster_intelligence.md").write_text(
        render_roster_md(roster), encoding="utf-8")
    active = sum(1 for r in roster if r["status"] == "ACTIVE")
    print(f"      B: roster.jsonl  ({len(roster)} total, {active} active)")

    # Phase C
    hero_bindings = build_hero_bindings(heroes_data)
    edges = extract_stat_bridge(abilities_data, hero_bindings)
    (OUTPUTS_DIR / "stat_bridge.jsonl").write_text(
        "\n".join(json.dumps(e) for e in edges), encoding="utf-8")
    (OUTPUTS_DIR / "stat_bridge_summary.md").write_text(
        render_bridge_summary(edges), encoding="utf-8")
    bound_edges = sum(1 for e in edges if e["hero_binding"] != "(shared)")
    print(f"      C: stat_bridge.jsonl  ({len(edges):,} edges, {bound_edges:,} hero-bound)")

    # Wander deck
    (OUTPUTS_DIR / "wander_questions.md").write_text(
        generate_wander_deck(edges, roster), encoding="utf-8")
    print(f"      +: wander_questions.md")

    print("\n[5/5] Generating hero Turtles (A)...")
    shapes_path = BASE_DIR / "src" / "nydus.shacl.ttl"

    # All ACTIVE heroes -> outputs/heroes/{codename}.ttl
    heroes_dir = OUTPUTS_DIR / "heroes"
    heroes_dir.mkdir(exist_ok=True)
    active_codenames = [r["codename"] for r in roster if r["status"] == "ACTIVE"]
    print(f"      Emitting per-hero TTLs for {len(active_codenames)} ACTIVE heroes...")
    manifest = []
    for codename in active_codenames:
        try:
            ttl = generate_turtle(heroes_data, abilities_data, loc, hero_key=codename)
            out_path = heroes_dir / f"{codename}.ttl"
            out_path.write_text(ttl, encoding="utf-8")
            public = CODENAME_TO_PUBLIC.get(codename, codename).lstrip("?")
            triples = ttl.count(" ;") + ttl.count(" .")
            manifest.append({
                "codename": codename,
                "public_name": public,
                "hero_id": next((r["hero_id"] for r in roster if r["codename"] == codename), -1),
                "ttl": f"heroes/{codename}.ttl",
                "triples": triples,
            })
        except Exception as e:
            print(f"      ! {codename}: {type(e).__name__}: {e}")
    manifest.sort(key=lambda m: m["public_name"].lower())
    (heroes_dir / "index.json").write_text(
        json.dumps({"heroes": manifest}, indent=2), encoding="utf-8")
    print(f"      Wrote {len(manifest)} hero TTLs to outputs/heroes/")
    print(f"\n[SHACL] Validating outputs/heroes/*.ttl...")
    violations = 0
    for m in manifest:
        ok = validate_ttl(OUTPUTS_DIR / m["ttl"], shapes_path)
        if not ok:
            violations += 1
    print(f"      SHACL summary: {len(manifest) - violations}/{len(manifest)} conform")

    print("\n" + "=" * 55)
    print("  Done. Outputs written to:")
    for f in sorted(OUTPUTS_DIR.iterdir()):
        kb = f.stat().st_size // 1024
        print(f"    {f.name:<35s} {kb:4d} KB")
    print("=" * 55)


if __name__ == "__main__":
    main()
