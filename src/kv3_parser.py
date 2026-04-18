#!/usr/bin/env python3
"""
Deadlock VData bootstrap pipeline — Steps 1-6.
Usage: python3 src/kv3_parser.py [heroes|abilities|modifiers|npc_units]
Default: heroes

Outputs (written to outputs/, never printed inline):
  - frequency_report.md
  - unknowns.jsonl
  - rubric.md

Hard rules (CLAUDE.md):
  - Never read .vdata content into stdout
  - All file reading goes through this module
  - Preserve the "Modifer" typo verbatim
  - Quarantine over delete
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

# =============================================================================
# PATHS
# =============================================================================

BASE_DIR          = Path(__file__).resolve().parent.parent
EXTRACTED_DIR     = BASE_DIR / "extracted" / "scripts"
LOC_BASE          = Path("D:/SteamLibrary/steamapps/common/Deadlock/game/citadel/resource/localization")
OUTPUTS_DIR       = BASE_DIR / "outputs"

LOC_SUBDIRS = [
    "citadel_attributes",
    "citadel_gc",
    "citadel_gc_hero_names",   # hero sort/search names
    "citadel_gc_mod_names",    # modifier display names
    "citadel_heroes",
    "citadel_main",
    "citadel_mods",
    "citadel_patch_notes",     # present on disk
    # citadel_vdata has no _english.txt (auto-generated stub, skipped)
]

# =============================================================================
# KNOWN TAXONOMY (from task Known Facts — do not rediscover)
# =============================================================================

KNOWN_GENERIC_DATA_TYPES = {
    # key: (expected category, source file)
    "CitadelHeroData_t":            ("hero",     "heroes.vdata"),
    "CitadelAbilityVData":          ("ability",  "abilities.vdata"),
    "CCitadelModifierVData":        ("modifier", "modifiers.vdata"),
    "CAI_CitadelNPCVData":          ("npc",      "npc_units.vdata"),
    "CAI_BaseNPCVData":             ("npc",      "npc_units.vdata"),
}

BASE_CLASS_TAXONOMY = {
    "CitadelAbilityVData":   "ability",
    "CCitadelModifierVData": "modifier",
    "CBasePlayerVData":      "hero",
    "CAI_BaseNPCVData":      "npc",
    "CAI_CitadelNPCVData":   "npc",
}

# =============================================================================
# DENYLIST (from Known Facts — pre-population, no rediscovery)
# =============================================================================

DENYLIST_RULES = [
    # (pattern, rationale)
    (r"^m_nEditorNode",      "Editor: node positioning metadata"),
    (r"^m_editorNode",       "Editor: node handle"),
    (r"^m_sComment$",        "Editor: comment annotation"),
    (r"^m_bDebug",           "Debug: debug flag"),
    (r"^m_bIsTestOnly$",     "Debug/test: entity excluded from live builds"),
    (r"^m_bTest",            "Debug/test: test flag"),
    (r"^m_pEntity$",         "Identity: entity pointer plumbing"),
    (r"^m_name$",            "Identity: CUtlSymbolLarge internal name"),
    (r"^m_hParticle",        "Asset handle: particle effect (chaff for stats, wheat for assets)"),
    (r"^m_hModel",           "Asset handle: model (chaff for stats, wheat for assets)"),
    (r"^m_hSound",           "Asset handle: sound (chaff for stats, wheat for assets)"),
    (r"^m_hTexture",         "Asset handle: texture (chaff for stats, wheat for assets)"),
    (r"^m_hCastAnimGraph",   "Asset handle: cast anim graph"),
    (r"^m_hGlobalAnim",      "Asset handle: global animation"),
    (r"^m_vecParticle",      "Asset array: particle systems"),
    (r"^m_strSound",         "Asset string: sound path"),
    (r"^m_strIcon$",         "Asset string: icon SVG path (chaff for stats, wheat for assets)"),
    (r"^m_strAbilityImage$", "Asset string: ability image path (chaff for stats, wheat for assets)"),
]

DENYLIST_RE = [(re.compile(p), note) for p, note in DENYLIST_RULES]

# Context-dependent — flag for design decision, don't auto-classify
CONTEXT_DEPENDENT = {
    "m_bitsPostCastEnabledStateMask": "State machine bitmask — which cast states re-enable post-cast",
    "m_bitsInterruptingStates":       "State machine bitmask — states that interrupt this ability",
    "m_nAbilityBehaviors":            "Ability behavior bitmask — bitfield of EAbilityBehavior flags",
    "m_eAbilityActivation":           "Ability type enum — how the ability is activated",
    "m_nAbilityTargetTypes":          "Ability target type enum — valid target types",
    "m_eAbilityType":                 "Ability type enum — category (passive/active/etc)",
}


def is_denylist(key: str) -> Optional[str]:
    """Return denylist rationale if key matches, else None."""
    for rx, note in DENYLIST_RE:
        if rx.match(key):
            return note
    return None


def base_key(key_path: str) -> str:
    """First segment of a dot-notation path (strips array indices)."""
    return key_path.split(".")[0].split("[")[0]


# =============================================================================
# KV3 TEXT PARSER
# =============================================================================

class KV3TextParser:
    """
    Recursive-descent parser for KV3 text format (VRF decompiler output).
    KV3 value flags (resource:, resource_name:, panorama:, soundevent:, subclass:)
    are preserved as {'_flag': name, '_value': inner}.
    Schema-tolerant: unknown structure skips gracefully instead of crashing.
    """

    KV3_FLAGS = {"resource", "resource_name", "panorama", "soundevent", "subclass"}

    def __init__(self, text: str):
        self._tok: list[tuple[str, str]] = []
        self._pos = 0
        self._tokenize(text)

    # ------------------------------------------------------------------
    # Tokenizer
    # ------------------------------------------------------------------

    def _tokenize(self, text: str) -> None:
        toks: list[tuple[str, str]] = []
        i, n = 0, len(text)

        while i < n:
            c = text[i]

            # HTML comment header  <!-- ... -->
            if text[i : i + 4] == "<!--":
                end = text.find("-->", i)
                i = end + 3 if end != -1 else n
                continue

            # Line comment  // ...
            if text[i : i + 2] == "//":
                end = text.find("\n", i)
                i = end + 1 if end != -1 else n
                continue

            # Whitespace
            if c in " \t\r\n":
                i += 1
                continue

            # Single-char tokens
            if c == "{":   toks.append(("LBRACE",   "{")); i += 1; continue
            if c == "}":   toks.append(("RBRACE",   "}")); i += 1; continue
            if c == "[":   toks.append(("LBRACKET", "[")); i += 1; continue
            if c == "]":   toks.append(("RBRACKET", "]")); i += 1; continue
            if c == "=":   toks.append(("EQUALS",   "=")); i += 1; continue
            if c == ":":   toks.append(("COLON",    ":")); i += 1; continue
            if c == ",":   toks.append(("COMMA",    ",")); i += 1; continue

            # Quoted string
            if c == '"':
                j = i + 1
                while j < n:
                    if text[j] == "\\":
                        j += 2
                    elif text[j] == '"':
                        break
                    else:
                        j += 1
                toks.append(("STRING", text[i + 1 : j]))
                i = j + 1
                continue

            # Number  (handles -3.14e-5)
            if c == "-" or c.isdigit():
                j = i
                if text[j] == "-":
                    j += 1
                while j < n and (text[j].isdigit() or text[j] in ".eE+"):
                    j += 1
                # Guard: lone minus that's not a number
                raw = text[i:j]
                if raw in ("-", ""):
                    i += 1
                    continue
                toks.append(("NUMBER", raw))
                i = j
                continue

            # Identifier: key name, bool, null, flag
            if c.isalpha() or c == "_":
                j = i
                while j < n and (text[j].isalnum() or text[j] == "_"):
                    j += 1
                toks.append(("IDENT", text[i:j]))
                i = j
                continue

            i += 1  # skip unknown char

        self._tok = toks

    # ------------------------------------------------------------------
    # Parser helpers
    # ------------------------------------------------------------------

    def _peek(self) -> Optional[tuple]:
        return self._tok[self._pos] if self._pos < len(self._tok) else None

    def _consume(self, expected: str = None) -> tuple:
        if self._pos >= len(self._tok):
            raise IndexError(f"EOF, expected {expected}")
        t = self._tok[self._pos]
        self._pos += 1
        if expected and t[0] != expected:
            raise ValueError(f"Expected {expected}, got {t} at pos {self._pos}")
        return t

    # ------------------------------------------------------------------
    # Grammar
    # ------------------------------------------------------------------

    def parse(self) -> dict:
        return self._object()

    def _object(self) -> dict:
        self._consume("LBRACE")
        result: dict = {}
        while self._peek() and self._peek()[0] != "RBRACE":
            try:
                k, v = self._kv()
                result[k] = v
            except (ValueError, IndexError):
                # Schema-tolerant: skip one token and keep going
                if self._pos < len(self._tok):
                    self._pos += 1
        if self._peek():
            self._consume("RBRACE")
        return result

    def _kv(self) -> tuple[str, Any]:
        tok = self._peek()
        if tok is None or tok[0] not in ("STRING", "IDENT", "NUMBER"):
            raise ValueError(f"Expected key, got {tok}")
        self._consume()
        key = tok[1]
        self._consume("EQUALS")
        return key, self._value()

    def _value(self) -> Any:
        tok = self._peek()
        if tok is None:
            return None

        t = tok[0]

        if t == "LBRACE":
            return self._object()

        if t == "LBRACKET":
            return self._array()

        if t == "STRING":
            self._consume()
            return tok[1]

        if t == "NUMBER":
            self._consume()
            raw = tok[1]
            try:
                return float(raw) if ("." in raw or "e" in raw.lower()) else int(raw)
            except ValueError:
                return raw

        if t == "IDENT":
            val = tok[1]
            if val == "true":  self._consume(); return True
            if val == "false": self._consume(); return False
            if val == "null":  self._consume(); return None
            # Check for flag:value  (IDENT COLON value)
            nxt = self._tok[self._pos + 1] if self._pos + 1 < len(self._tok) else None
            if nxt and nxt[0] == "COLON":
                self._consume()  # flag ident
                self._consume("COLON")
                inner = self._value()
                return {"_flag": val, "_value": inner}
            # Bare ident (fallback)
            self._consume()
            return val

        # Fallback
        self._consume()
        return tok[1]

    def _array(self) -> list:
        self._consume("LBRACKET")
        items = []
        while self._peek() and self._peek()[0] != "RBRACKET":
            items.append(self._value())
            if self._peek() and self._peek()[0] == "COMMA":
                self._consume("COMMA")
        if self._peek():
            self._consume("RBRACKET")
        return items


# =============================================================================
# KV1 LOCALIZATION PARSER
# =============================================================================

def parse_kv1_localization(text: str) -> dict[str, str]:
    """
    Parse Valve KV1 localization file.
    Format: "lang" { "Language" "English" "Tokens" { "key" "value" ... } }
    Returns {token_key_lower: display_text}.

    Namespace suffixes are stripped: "hero_inferno_sort:n" -> key "hero_inferno_sort".
    The colon-suffix is a Valve grammatical-number marker, not part of the canonical key.
    """
    result: dict[str, str] = {}
    m = re.search(r'"Tokens"\s*\{(.+)', text, re.DOTALL | re.IGNORECASE)
    if not m:
        return result
    block = m.group(1)
    # Find matching close brace
    depth, idx = 1, 0
    while idx < len(block) and depth > 0:
        if block[idx] == '{':
            depth += 1
        elif block[idx] == '}':
            depth -= 1
        idx += 1
    block = block[:idx - 1]

    for raw_key, val in re.findall(r'"([^"]+?)"\s+"((?:[^"\\]|\\\.)*)"', block):
        # Strip Valve namespace suffix (:n :p :np :pn etc.)
        key = raw_key
        if ':' in key:
            base, suffix = key.rsplit(':', 1)
            if suffix.isalpha():
                key = base
        result[key.lower()] = val
    return result


def load_localization() -> dict[str, str]:
    """
    Load all localization subdirectories, merge into {token_lower: text}.
    Warns on missing files but never fails.
    """
    merged: dict[str, str] = {}
    for subdir in LOC_SUBDIRS:
        f = LOC_BASE / subdir / f"{subdir}_english.txt"
        if not f.exists():
            print(f"  [LOC WARN] not found: {f.name}")
            continue
        try:
            partial = parse_kv1_localization(f.read_text(encoding="utf-8-sig", errors="replace"))
            merged.update(partial)
        except Exception as e:
            print(f"  [LOC WARN] failed to parse {f.name}: {e}")
    return merged


# =============================================================================
# KEY FLATTENING
# =============================================================================

def flatten(obj: Any, prefix: str = "", depth: int = 5) -> dict[str, Any]:
    """
    Recursively flatten a parsed KV3 dict to {key_path: value}.
    KV3 flag wrappers are preserved as strings like "resource_name:some/path".
    Arrays: store length + up to 3 sampled element paths.
    """
    out: dict[str, Any] = {}

    if not isinstance(obj, dict):
        out[prefix] = obj
        return out

    if depth == 0:
        out[prefix or "__root__"] = "<depth_limit>"
        return out

    for k, v in obj.items():
        path = f"{prefix}.{k}" if prefix else k

        if isinstance(v, dict) and "_flag" in v:
            flag, inner = v["_flag"], v["_value"]
            if isinstance(inner, str):
                out[path] = f"{flag}:{inner}"
            elif isinstance(inner, (int, float, bool)) or inner is None:
                out[path] = f"{flag}:{inner}"
            else:
                # flag with complex inner (object/array) — record flag annotation
                out[f"{path}.__flag__"] = flag
                out.update(flatten(inner, path, depth - 1))
        elif isinstance(v, dict):
            out.update(flatten(v, path, depth - 1))
        elif isinstance(v, list):
            out[f"{path}.__len__"] = len(v)
            for i, item in enumerate(v[:3]):
                if isinstance(item, dict):
                    out.update(flatten(item, f"{path}[{i}]", depth - 1))
                else:
                    out[f"{path}[{i}]"] = item
        else:
            out[path] = v

    return out


# =============================================================================
# LOCALIZATION JOIN HELPER
# =============================================================================

def try_loc_join(value: Any, loc: dict[str, str]) -> Optional[str]:
    """
    Return resolved English text if value is a localization token reference.
    Handles: '#token_name' → strip # → look up lowercase.
    Returns None if not a token reference or if lookup fails.
    """
    if not isinstance(value, str):
        return None
    if value.startswith("#"):
        return loc.get(value[1:].lower())
    # m_sLocalizationName convention: uppercase + prepend #
    # This is called separately in the sweep.
    return None


def loc_join_modifier_name(name: str, loc: dict[str, str]) -> Optional[str]:
    """
    m_sLocalizationName join: uppercase and prepend #, then look up.
    E.g. "modifier_citadel_stunned" → "#MODIFIER_CITADEL_STUNNED" → look up "modifier_citadel_stunned".
    """
    if not name:
        return None
    # Try direct lowercase lookup first
    direct = loc.get(name.lower())
    if direct:
        return direct
    # Try with modifier_ prefix convention
    upped = name.upper()
    return loc.get(upped.lower()) or loc.get(f"modifier_{name}".lower())


# =============================================================================
# PIPELINE
# =============================================================================

def run(vdata_path: Path, label: str) -> dict:
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}\n")

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------
    # STEP 1 — Parse
    # -------------------------------------------------------
    print("[Step 1] Parsing KV3...")
    text = vdata_path.read_text(encoding="utf-8", errors="replace")
    root = KV3TextParser(text).parse()

    generic_data_type = root.get("generic_data_type", "UNKNOWN")
    print(f"  generic_data_type : {generic_data_type}")

    # Taxonomy check — STOP CONDITION A
    if generic_data_type not in KNOWN_GENERIC_DATA_TYPES and generic_data_type != "UNKNOWN":
        print(f"\n  *** STOP CONDITION A ***")
        print(f"  generic_data_type '{generic_data_type}' is outside the known taxonomy.")
        print(f"  This is likely from a recent patch. Flagged for human review.")

    entities = {k: v for k, v in root.items() if k != "generic_data_type"}
    print(f"  Entity count      : {len(entities)}")

    # Leaf-class histogram
    class_hist: Counter = Counter()
    for name, ent in entities.items():
        cls = ent.get("_class", "UNKNOWN") if isinstance(ent, dict) else "NON_DICT"
        class_hist[cls] += 1

    print(f"  Leaf classes      : {len(class_hist)} distinct")
    for cls, cnt in class_hist.most_common(10):
        print(f"    {cls}: {cnt}")
    if len(class_hist) > 10:
        print(f"    ... ({len(class_hist) - 10} more)")

    # -------------------------------------------------------
    # STEP 2 — Denylist
    # -------------------------------------------------------
    print("\n[Step 2] Applying denylist...")

    all_flat: dict[str, dict[str, Any]] = {}
    for name, ent in entities.items():
        if isinstance(ent, dict):
            all_flat[name] = flatten(ent)

    denylist_drops: Counter = Counter()     # base_key → total instances dropped
    kept: dict[str, dict[str, Any]] = {}    # entity_name → {key_path: value}

    for name, kv in all_flat.items():
        kv_kept: dict[str, Any] = {}
        for key_path, val in kv.items():
            bk = base_key(key_path)
            reason = is_denylist(bk)
            if reason:
                denylist_drops[bk] += 1
            else:
                kv_kept[key_path] = val
        kept[name] = kv_kept

    total_dropped = sum(denylist_drops.values())
    print(f"  Dropped {total_dropped} key instances ({len(denylist_drops)} distinct base keys)")

    # -------------------------------------------------------
    # STEP 3 — Frequency analysis
    # -------------------------------------------------------
    print("\n[Step 3] Frequency analysis per leaf class...")

    # Group entity names by leaf class
    by_class: dict[str, list[str]] = defaultdict(list)
    for name, ent in entities.items():
        cls = ent.get("_class", "UNKNOWN") if isinstance(ent, dict) else "NON_DICT"
        by_class[cls].append(name)

    # Per-class: {key_path: {distinct values set, entity_count}}
    freq: dict[str, dict[str, dict]] = {}
    for cls, names in by_class.items():
        kv_vals: dict[str, set] = defaultdict(set)
        kv_entity_count: Counter = Counter()
        for name in names:
            for key_path, val in kept.get(name, {}).items():
                kv_vals[key_path].add(str(val)[:120])
                kv_entity_count[key_path] += 1
        freq[cls] = {
            kp: {
                "distinct": len(s),
                "samples": list(s)[:5],
                "entity_count": kv_entity_count[kp],
            }
            for kp, s in kv_vals.items()
        }

    # H3 verdicts (cross-class, using max distinct count per base key)
    base_key_max_distinct: dict[str, int] = {}
    base_key_samples: dict[str, list] = {}
    for cls_data in freq.values():
        for kp, info in cls_data.items():
            bk = base_key(kp)
            if info["distinct"] > base_key_max_distinct.get(bk, 0):
                base_key_max_distinct[bk] = info["distinct"]
                base_key_samples[bk] = info["samples"]

    h3_constants:  dict[str, str]  = {}  # bk → constant value
    h3_booleans:   set[str]         = set()
    h3_wheat:      set[str]         = set()

    for bk, distinct in base_key_max_distinct.items():
        if distinct == 1:
            h3_constants[bk] = base_key_samples.get(bk, ["?"])[0]
        elif distinct == 2:
            h3_booleans.add(bk)
        else:
            h3_wheat.add(bk)

    print(f"  H3 -- constant (chaff): {len(h3_constants)}")
    print(f"  H3 -- boolean (2 vals): {len(h3_booleans)}")
    print(f"  H3 -- wheat (>=3 vals): {len(h3_wheat)}")

    # -------------------------------------------------------
    # STEP 4 — Localization join sweep
    # -------------------------------------------------------
    print("\n[Step 4] Localization join sweep...")
    loc = load_localization()
    print(f"  Loaded {len(loc)} localization tokens")

    loc_wheat_keys: set[str] = set()
    loc_failures: list[dict]  = []

    for name, kv in kept.items():
        for key_path, val in kv.items():
            bk = base_key(key_path)
            if isinstance(val, str) and val.startswith("#"):
                resolved = try_loc_join(val, loc)
                if resolved is not None:
                    loc_wheat_keys.add(bk)
                else:
                    loc_failures.append({"entity": name, "key": key_path, "token": val})

    # m_sLocalizationName (modifier convention)
    for name, ent in entities.items():
        if isinstance(ent, dict):
            lname = ent.get("m_sLocalizationName")
            if lname and isinstance(lname, str):
                resolved = loc_join_modifier_name(lname, loc)
                if resolved:
                    loc_wheat_keys.add("m_sLocalizationName")
                else:
                    loc_failures.append({"entity": name, "key": "m_sLocalizationName", "token": lname})

    print(f"  Loc-wheat keys confirmed: {sorted(loc_wheat_keys)}")
    print(f"  Broken loc references   : {len(loc_failures)}")

    # STOP CONDITION C — systematic failures
    if len(loc_failures) > 20:
        # Check if all failures are from one field (systematic)
        fail_keys = Counter(f["key"] for f in loc_failures)
        systematic = [k for k, c in fail_keys.items() if c > 5]
        if systematic:
            print(f"\n  *** STOP CONDITION C candidate ***")
            print(f"  Fields with >5 broken loc refs: {systematic}")
            print(f"  Sample failures: {loc_failures[:3]}")
            print(f"  These need human review before proceeding.")

    # -------------------------------------------------------
    # STEP 5 — H1/H2 residue pass
    # -------------------------------------------------------
    print("\n[Step 5] H1/H2 residue classification...")

    all_base_keys: set[str] = set(base_key_max_distinct.keys())

    # Already classified sets
    auto_chaff:      set[str] = set(denylist_drops.keys())
    h3_chaff_keys:   set[str] = set(h3_constants.keys())   # cardinality-1 constants — override H2
    already_wheat:   set[str] = loc_wheat_keys.copy()
    already_wheat.update(h3_wheat)   # H3 wheat (>=3 distinct) is confirmed wheat regardless of H2

    # H2 prefix classification for remainder (h3_booleans + unclassified structural keys)
    # Note: h3_chaff_keys are excluded — H3 constant beats H2 prefix match
    WHEAT_PREFIXES = ("m_fl", "m_n", "m_b", "m_str", "m_sz", "m_psz")
    WHEAT_KEYWORDS = ("tooltip", "display", "locali", "label", "token", "name",
                      "description", "stat", "damage", "cooldown", "range",
                      "duration", "speed", "health", "regen", "resist", "scale",
                      "bonus", "penalty", "upgrade", "slot", "tier", "level",
                      "cast", "target", "radius", "angle", "count", "max", "min",
                      "rate", "chance", "delay", "time", "cost", "ammo", "bullet",
                      "reload", "weapon", "ability", "hero", "id", "type")
    # H2: m_h = handle (chaff by default per HEURISTICS.md H2); m_p = pointer
    # The denylist covers specific prefixes; m_h here catches remaining handles
    CHAFF_PREFIXES = ("m_h", "m_p")

    h2_wheat_new:  set[str] = set()
    h2_chaff_new:  set[str] = set()
    h2_unknown:    set[str] = set()

    for bk in all_base_keys:
        if bk in auto_chaff or bk in h3_chaff_keys or bk in already_wheat or bk in CONTEXT_DEPENDENT:
            continue
        bk_lower = bk.lower()
        if any(bk.startswith(p) for p in WHEAT_PREFIXES):
            h2_wheat_new.add(bk)
        elif any(kw in bk_lower for kw in WHEAT_KEYWORDS):
            h2_wheat_new.add(bk)
        elif any(bk.startswith(p) for p in CHAFF_PREFIXES):
            h2_chaff_new.add(bk)
        else:
            h2_unknown.add(bk)

    print(f"  H2 new wheat : {len(h2_wheat_new)}")
    print(f"  H2 new chaff : {len(h2_chaff_new)}")
    print(f"  H2 unknown   : {len(h2_unknown)} → quarantine")

    # -------------------------------------------------------
    # STEP 6 — Quarantine
    # -------------------------------------------------------
    print("\n[Step 6] Writing outputs...")

    # Build per-base-key entity samples for unknowns
    bk_entity_samples: dict[str, list[dict]] = defaultdict(list)
    for name, kv in kept.items():
        for key_path, val in kv.items():
            bk = base_key(key_path)
            if bk in h2_unknown and len(bk_entity_samples[bk]) < 5:
                bk_entity_samples[bk].append({"entity": name, "key": key_path, "value": str(val)[:200]})

    unknowns: list[dict] = []
    for bk in sorted(h2_unknown):
        distinct = base_key_max_distinct.get(bk, 0)
        samples  = base_key_samples.get(bk, [])
        # Determine note
        if distinct == 1:
            note = f"constant ({samples[0][:40] if samples else '?'}) — likely chaff"
        elif distinct == 2:
            note = f"binary ({', '.join(str(s)[:20] for s in samples[:2])}) — possible boolean flag"
        elif distinct <= 10:
            note = f"{distinct} distinct values — low cardinality, may encode enum"
        else:
            note = f"{distinct} distinct values — probable wheat"

        unknowns.append({
            "key":            bk,
            "file":           label,
            "distinct_count": distinct,
            "samples":        samples[:5],
            "entity_samples": bk_entity_samples.get(bk, []),
            "note":           note,
        })

    unknowns.sort(key=lambda x: -x["distinct_count"])

    # Write unknowns.jsonl (append mode for multi-file runs)
    unknowns_path = OUTPUTS_DIR / "unknowns.jsonl"
    with unknowns_path.open("a", encoding="utf-8") as f:
        for entry in unknowns:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"  → {unknowns_path} (+{len(unknowns)} entries)")

    # Write frequency_report.md
    freq_path = OUTPUTS_DIR / "frequency_report.md"
    _write_frequency_report(
        freq_path, label, generic_data_type, entities, class_hist,
        denylist_drops, freq, base_key_max_distinct, base_key_samples,
    )
    print(f"  → {freq_path}")

    # Write rubric.md
    rubric_path = OUTPUTS_DIR / "rubric.md"
    _write_rubric(
        rubric_path, label, generic_data_type, class_hist,
        denylist_drops, loc_wheat_keys, h2_wheat_new, h2_chaff_new,
        h3_constants, h3_booleans, h3_wheat, unknowns, loc_failures,
    )
    print(f"  → {rubric_path}")

    summary = {
        "file":               label,
        "generic_data_type":  generic_data_type,
        "entity_count":       len(entities),
        "leaf_classes":       len(class_hist),
        "denylist_dropped":   total_dropped,
        "loc_wheat_keys":     sorted(loc_wheat_keys),
        "h2_wheat_new":       len(h2_wheat_new),
        "h2_chaff_new":       len(h2_chaff_new),
        "unknowns":           len(unknowns),
        "loc_failures":       len(loc_failures),
    }
    print(f"\nSummary: {json.dumps(summary, indent=2)}")
    return summary


# =============================================================================
# OUTPUT WRITERS
# =============================================================================

def _write_frequency_report(
    path: Path,
    label: str,
    gdt: str,
    entities: dict,
    class_hist: Counter,
    denylist_drops: Counter,
    freq: dict,
    base_key_distinct: dict,
    base_key_samples: dict,
) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write(f"# Frequency Report — {label}\n\n")
        f.write(f"**`generic_data_type`:** `{gdt}`  \n")
        f.write(f"**Entity count:** {len(entities)}  \n")
        f.write(f"**Leaf classes:** {len(class_hist)}  \n\n")

        # Class histogram
        f.write("## Class Histogram\n\n")
        f.write("| Class | Count |\n|---|---|\n")
        for cls, cnt in class_hist.most_common():
            f.write(f"| `{cls}` | {cnt} |\n")

        # Denylist drops
        f.write("\n## Auto-Classified Chaff (Denylist Drops)\n\n")
        f.write(f"Total instances dropped: **{sum(denylist_drops.values())}**\n\n")
        f.write("| Base Key | Instances Dropped |\n|---|---|\n")
        for k, c in sorted(denylist_drops.items(), key=lambda x: -x[1]):
            f.write(f"| `{k}` | {c} |\n")

        # H3 summary — sorted ascending by cardinality
        f.write("\n## H3 Cardinality Analysis (ascending by max distinct values)\n\n")
        f.write("| Key | Max Distinct | Sample Values | H3 Verdict |\n|---|---|---|---|\n")
        sorted_bks = sorted(base_key_distinct.items(), key=lambda x: x[1])
        for bk, d in sorted_bks:
            samples = base_key_samples.get(bk, [])
            sv = " · ".join(f"`{str(s)[:25]}`" for s in samples[:2])
            verdict = (
                "constant — likely chaff" if d == 1
                else "boolean (2 values)" if d == 2
                else f"wheat ({d} values)"
            )
            f.write(f"| `{bk}` | {d} | {sv} | {verdict} |\n")

        # Per-class breakdown
        f.write("\n## Per-Class Breakdown\n\n")
        for cls in sorted(freq.keys()):
            cls_data = freq[cls]
            entity_cnt = class_hist.get(cls, "?")
            f.write(f"\n### `{cls}` ({entity_cnt} entities)\n\n")
            f.write("| Key Path | Distinct | Entity Count | H3 Verdict |\n|---|---|---|---|\n")
            for kp, info in sorted(cls_data.items(), key=lambda x: x[1]["distinct"]):
                d = info["distinct"]
                ec = info["entity_count"]
                sv = " · ".join(f"`{str(s)[:20]}`" for s in info["samples"][:2])
                verdict = (
                    f"constant {sv}" if d == 1
                    else f"boolean {sv}" if d == 2
                    else f"wheat ({d})"
                )
                f.write(f"| `{kp}` | {d} | {ec} | {verdict} |\n")


def _write_rubric(
    path: Path,
    label: str,
    gdt: str,
    class_hist: Counter,
    denylist_drops: Counter,
    loc_wheat: set,
    h2_wheat: set,
    h2_chaff: set,
    h3_constants: dict,
    h3_booleans: set,
    h3_wheat: set,
    unknowns: list,
    loc_failures: list,
) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write(f"# Wheat / Chaff / Context-Dependent Rubric\n\n")
        f.write(f"> Source file: `{label}` — `{gdt}`  \n")
        f.write(f"> Confidence target: ~80% first pass. Unknowns → `unknowns.jsonl`.\n\n")

        # --- Auto chaff (denylist) ---
        f.write("## Auto-Classified Chaff — Denylist\n\n")
        f.write("Pre-populated from Known Facts; no analysis needed.\n\n")
        f.write("| Pattern | Rationale |\n|---|---|\n")
        for p, note in DENYLIST_RULES:
            f.write(f"| `{p}` | {note} |\n")
        f.write("\n**Observed drops in this file:**\n\n")
        for k in sorted(denylist_drops):
            f.write(f"- `{k}` ({denylist_drops[k]} instances)\n")

        # --- Confirmed wheat ---
        f.write("\n---\n\n## Confirmed Wheat\n\n")
        all_wheat = sorted(loc_wheat | h2_wheat | h3_wheat)
        for k in all_wheat:
            if k in loc_wheat:
                f.write(f"- `{k}` -- H5: localization token hit -> player-visible by definition\n")
            elif k in h3_wheat:
                f.write(f"- `{k}` -- H3: >=3 distinct values across instances (designed variation)\n")
            else:
                f.write(f"- `{k}` -- H2: naming convention signals meaningful game data\n")

        # --- H3 constants (chaff) ---
        f.write("\n---\n\n## H3 Constants (Single-Value Chaff)\n\n")
        f.write("Keys with exactly 1 distinct value across all instances — engine defaults.\n\n")
        for k in sorted(h3_constants.keys())[:60]:
            v = h3_constants[k]
            f.write(f"- `{k}` = `{str(v)[:60]}` — constant\n")
        if len(h3_constants) > 60:
            f.write(f"- *...{len(h3_constants)-60} more — see frequency_report.md*\n")

        # --- H3 booleans ---
        f.write("\n---\n\n## H3 Booleans (Two-Value Keys)\n\n")
        f.write("Keys with exactly 2 distinct values — likely boolean flags.\n\n")
        for k in sorted(h3_booleans):
            f.write(f"- `{k}`\n")

        # --- Context-dependent ---
        f.write("\n---\n\n## Context-Dependent — Flag for Design Decision\n\n")
        f.write("Gameplay-relevant but encoding-complex; include only with explicit modeling decision.\n\n")
        for k, desc in sorted(CONTEXT_DEPENDENT.items()):
            f.write(f"- `{k}` — {desc}\n")

        # --- H2 additional chaff ---
        if h2_chaff:
            f.write("\n---\n\n## H2 Additional Chaff (Pointer/Handle Prefix)\n\n")
            for k in sorted(h2_chaff):
                f.write(f"- `{k}` — H2: pointer/handle prefix signals engine plumbing\n")

        # --- Localization failures ---
        if loc_failures:
            f.write("\n---\n\n## Broken Localization References\n\n")
            f.write(f"{len(loc_failures)} token references failed to resolve.\n\n")
            if len(loc_failures) > 20:
                f.write("> **Review needed:** systematic failure count exceeds threshold.\n\n")
            for entry in loc_failures[:10]:
                f.write(f"- `{entry['key']}` on `{entry['entity']}`: token `{entry['token']}`\n")
            if len(loc_failures) > 10:
                f.write(f"- *...{len(loc_failures)-10} more in unknowns.jsonl*\n")

        # --- Quarantined ---
        f.write("\n---\n\n## Quarantined (unknowns.jsonl)\n\n")
        f.write(f"{len(unknowns)} keys sent to `unknowns.jsonl` for human review.\n\n")
        f.write("| Key | Distinct Values | Note |\n|---|---|---|\n")
        for entry in unknowns[:30]:
            note = entry["note"][:80].replace("|", "\\|")
            f.write(f"| `{entry['key']}` | {entry['distinct_count']} | {note} |\n")
        if len(unknowns) > 30:
            f.write(f"\n*...{len(unknowns)-30} more entries in unknowns.jsonl*\n")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Deadlock VData bootstrap pipeline")
    ap.add_argument(
        "file",
        nargs="?",
        default="heroes",
        choices=["heroes", "abilities", "modifiers", "npc_units"],
        help="Which VData file to process (default: heroes)",
    )
    args = ap.parse_args()

    vdata = EXTRACTED_DIR / f"{args.file}.vdata"
    if not vdata.exists():
        print(f"ERROR: {vdata} not found", file=sys.stderr)
        sys.exit(1)

    run(vdata, f"{args.file}.vdata")
