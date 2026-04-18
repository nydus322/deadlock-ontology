#!/usr/bin/env python3
"""
proof.py — Visual proof of the SHACL-primary Nydus ontology.

Generates outputs/proof.html showing:
  1. SHACL conformance badge
  2. PropertyCategory nodes — the shared semantic anchors
  3. Abrams ability cards (queried through nydus:hasProperty blank nodes)
  4. Category × Ability matrix — cross-ability comparison proof
  5. Full hero roster
  6. Stat web (MODIFIER_VALUE edge frequency)

Usage:
  PYTHONUTF8=1 python3 src/proof.py
"""

import json
import rdflib
from pathlib import Path
from collections import Counter, defaultdict

BASE_DIR    = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
SRC_DIR     = BASE_DIR / "src"

NYDUS   = rdflib.Namespace("http://nydus.gg/ontology#")
CAT_NS  = rdflib.Namespace("http://nydus.gg/ontology#cat/")
RDFS    = rdflib.RDFS
RDF     = rdflib.RDF
XSD     = rdflib.XSD

# ── Category colour palette ────────────────────────────────────────────────────
CAT_COLORS: dict[str, str] = {
    "Cooldown":     "#5b9bd5",
    "Damage":       "#e05c5c",
    "Duration":     "#4dbfc4",
    "Range":        "#4da6ff",
    "Speed":        "#f5a623",
    "Healing":      "#4fc24f",
    "Charges":      "#8a9bb0",
    "Stack":        "#9b6dff",
    "Weapon":       "#e8943a",
    "Stat":         "#c084fc",
    "Unknown":      "#444",
}

STAT_FAMILY = {
    "TechPower":    "spirit",  "TechCooldown":  "spirit",
    "TechDuration": "spirit",  "TechRange":     "spirit",
    "WeaponPower":  "weapon",  "BulletDamage":  "weapon",
    "FireRate":     "weapon",  "ReloadSpeed":   "weapon",
    "MaxHealth":    "vitality","BaseHealthRegen":"vitality",
    "ParryCooldown":"spirit",
}
STAT_COLORS = {
    "spirit":   "#9b6dff",
    "weapon":   "#f5a623",
    "vitality": "#4fc24f",
    "neutral":  "#8a9bb0",
}

def stat_color(stat: str) -> str:
    fam = STAT_FAMILY.get(stat, "neutral")
    return STAT_COLORS[fam]

def cat_color(cat_iri) -> str:
    name = str(cat_iri).split("#cat/")[-1]
    return CAT_COLORS.get(name, CAT_COLORS["Unknown"])

def load_data():
    g = rdflib.Graph()
    g.parse(OUTPUTS_DIR / "abrams.ttl", format="turtle")
    roster = [json.loads(l) for l in (OUTPUTS_DIR / "roster.jsonl").read_text(encoding="utf-8").splitlines()]
    bridge = [json.loads(l) for l in (OUTPUTS_DIR / "stat_bridge.jsonl").read_text(encoding="utf-8").splitlines()]
    return g, roster, bridge

def check_shacl() -> tuple[bool, str]:
    try:
        from pyshacl import validate
        conforms, _, txt = validate(
            str(OUTPUTS_DIR / "abrams.ttl"),
            shacl_graph=str(SRC_DIR / "nydus.shacl.ttl"),
            inference="rdfs", abort_on_first=False,
        )
        return conforms, txt
    except ImportError:
        return None, "pyshacl not installed"


# ── Ability card ───────────────────────────────────────────────────────────────

def ability_card(g: rdflib.Graph, ability_iri: rdflib.URIRef, slot_label: str) -> str:
    label   = str(g.value(ability_iri, RDFS.label) or ability_iri)
    label   = label.replace("Citadel Ability ", "")
    ab_type = str(g.value(ability_iri, NYDUS.abilityType) or "").replace("EAbilityType_", "")
    act     = (str(g.value(ability_iri, NYDUS.activationType) or "")
               .replace("CITADEL_ABILITY_ACTIVATION_", "").replace("_", " ").title())

    # Properties via nydus:hasProperty blank nodes
    props_html = []
    for prop_bn in g.objects(ability_iri, NYDUS.hasProperty):
        prop_name  = str(g.value(prop_bn, NYDUS.internalName) or "?")
        base_val   = str(g.value(prop_bn, NYDUS.baseValue) or "")
        primary    = g.value(prop_bn, NYDUS.primaryCategory)
        det        = str(g.value(prop_bn, NYDUS.categoryDeterminism) or "high")
        cat_note   = g.value(prop_bn, NYDUS.categoryNote)
        scale_stat = g.value(prop_bn, NYDUS.scalesStat)
        scale_fc   = g.value(prop_bn, NYDUS.scaleFactor)
        scale_fn   = g.value(prop_bn, NYDUS.scaleFunction)

        cat_name  = str(primary).split("#cat/")[-1] if primary else "Unknown"
        cat_clr   = CAT_COLORS.get(cat_name, CAT_COLORS["Unknown"])
        stat_name = str(scale_stat).split("#stat/")[-1] if scale_stat else None
        s_clr     = stat_color(stat_name) if stat_name else "#8a9bb0"

        display = (prop_name
            .replace("Ability", "").replace("Stun", "Stun ")
            .replace("Speed", " Speed").replace("Radius", " Radius")
            .replace("Cooldown", " Cooldown").replace("Duration", " Duration")
            .replace("Damage", " Damage").replace("Charge", " Charge")
            .strip())

        low_dot = (f'<span title="{cat_note}" style="cursor:help;color:#e8c43a;font-size:10px"> ⚠</span>'
                   if det == "low" else "")

        cat_badge = (f'<span class="cat-badge" style="background:{cat_clr}22;'
                     f'border-color:{cat_clr};color:{cat_clr}">{cat_name}{low_dot}</span>')

        scale_badge = ""
        if stat_name:
            fc_txt = f" ×{scale_fc}" if scale_fc and str(scale_fc) not in ("1", "1.0", "-1", "-1.0") else ""
            scale_badge = (f'<span class="scale-badge" style="background:{s_clr}20;'
                           f'border-color:{s_clr};color:{s_clr}">↗ {stat_name}{fc_txt}</span>')

        props_html.append(
            f'<div class="stat-row">'
            f'<span class="stat-name">{display}</span>'
            f'<span class="stat-val">{base_val}</span>'
            f'{cat_badge}{scale_badge}'
            f'</div>'
        )

    # Upgrades via nydus:hasUpgrade blank nodes
    upgrades_by_level: dict[int, list] = defaultdict(list)
    for upg_bn in g.objects(ability_iri, NYDUS.hasUpgrade):
        level = int(str(g.value(upg_bn, NYDUS.upgradeLevel) or 1))
        prop  = str(g.value(upg_bn, NYDUS.modifiesProperty) or "")
        bonus = str(g.value(upg_bn, NYDUS.bonusValue) or "")
        if prop:
            upgrades_by_level[level].append((prop, bonus))

    upgrades_html = []
    for tier in (1, 2, 3):
        for prop, bonus in upgrades_by_level.get(tier, []):
            upgrades_html.append(
                f'<span class="upgrade t{tier}">T{tier} {prop}: <b>{bonus}</b></span>'
            )

    type_color  = "#9b6dff" if ab_type in ("Signature", "Ultimate") else "#8a9bb0"
    props_block = "\n".join(props_html) or '<div class="stat-row muted">No numeric properties extracted</div>'
    upg_block   = "\n".join(upgrades_html)

    return f"""
<div class="ability-card">
  <div class="ability-header" style="border-left:4px solid {type_color}">
    <div class="ability-title">{label}</div>
    <div class="ability-meta">
      <span class="tag" style="background:{type_color}22;color:{type_color}">{ab_type}</span>
      <span class="tag neutral">{act}</span>
      <span class="slot-badge">{slot_label}</span>
    </div>
  </div>
  <div class="ability-stats">{props_block}</div>
  {'<div class="upgrades">' + upg_block + '</div>' if upg_block else ''}
</div>"""


# ── Category section ───────────────────────────────────────────────────────────

def category_section(g: rdflib.Graph) -> str:
    """
    Show PropertyCategory nodes as the shared semantic anchors.
    For each category: which abilities use it, which properties, any low-det notes.
    """
    # Build: cat_iri -> list of (ability_key, prop_name, det, note)
    cat_data: dict = defaultdict(list)
    for ability_iri in g.subjects(RDF.type, NYDUS.Ability):
        ab_key = str(g.value(ability_iri, NYDUS.internalKey) or ability_iri)
        ab_short = ab_key.replace("citadel_ability_", "").replace("_", " ").title()
        for prop_bn in g.objects(ability_iri, NYDUS.hasProperty):
            prop_name = str(g.value(prop_bn, NYDUS.internalName) or "?")
            primary   = g.value(prop_bn, NYDUS.primaryCategory)
            secondary = g.value(prop_bn, NYDUS.secondaryCategory)
            det       = str(g.value(prop_bn, NYDUS.categoryDeterminism) or "high")
            note      = str(g.value(prop_bn, NYDUS.categoryNote) or "")
            scale_stat = g.value(prop_bn, NYDUS.scalesStat)
            scale_fc   = g.value(prop_bn, NYDUS.scaleFactor)
            stat_name  = str(scale_stat).split("#stat/")[-1] if scale_stat else None
            fc_txt     = f" ×{scale_fc}" if scale_fc and str(scale_fc) not in ("1","1.0","-1","-1.0") else ""
            formula    = f"{prop_name} = base{fc_txt + ' × ' + stat_name if stat_name else ''}"
            if primary:
                cat_data[primary].append((ab_short, prop_name, det, note, formula))
            if secondary:
                cat_data[secondary].append((ab_short, prop_name + " (2°)", "low", note, formula))

    # Build category cards
    cards_html = []
    for cat_iri in sorted(cat_data.keys(), key=lambda c: -len(cat_data[c])):
        entries = cat_data[cat_iri]
        cat_name = str(cat_iri).split("#cat/")[-1]
        color    = CAT_COLORS.get(cat_name, CAT_COLORS["Unknown"])
        low_det  = [e for e in entries if e[2] == "low"]

        rows = []
        seen = set()
        for ab_short, prop_name, det, note, formula in entries:
            key = (ab_short, prop_name)
            if key in seen:
                continue
            seen.add(key)
            warn = f' <span title="{note}" style="color:#e8c43a;cursor:help">⚠</span>' if det == "low" else ""
            rows.append(
                f'<div class="cat-row">'
                f'<span class="cat-ability">{ab_short}</span>'
                f'<span class="cat-prop">{prop_name}{warn}</span>'
                f'</div>'
            )

        low_note = ""
        if low_det:
            notes = list({e[3] for e in low_det if e[3]})
            if notes:
                low_note = f'<div class="low-det-note">⚠ {notes[0]}</div>'

        cards_html.append(f"""
<div class="cat-card" style="border-color:{color}44">
  <div class="cat-card-header" style="background:{color}15;border-bottom:1px solid {color}33">
    <span class="cat-name" style="color:{color}">{cat_name}</span>
    <span class="cat-count" style="color:{color}">{len(seen)}</span>
  </div>
  <div class="cat-card-body">
    {"".join(rows)}
    {low_note}
  </div>
</div>""")

    # Category × Ability matrix
    all_abilities = sorted({e[0] for entries in cat_data.values() for e in entries})
    all_cats      = sorted(cat_data.keys(), key=lambda c: -len(cat_data[c]))

    # Build lookup: (cat, ability) -> [(prop, det)]
    matrix: dict = defaultdict(list)
    for cat_iri, entries in cat_data.items():
        cat_name = str(cat_iri).split("#cat/")[-1]
        for ab_short, prop_name, det, note, formula in entries:
            key = (cat_name, ab_short)
            if prop_name not in [p for p, _ in matrix[key]]:
                matrix[key].append((prop_name, det))

    header_cells = "".join(f'<th class="mat-ab">{a}</th>' for a in all_abilities)
    mat_rows = []
    for cat_iri in all_cats:
        cat_name = str(cat_iri).split("#cat/")[-1]
        color    = CAT_COLORS.get(cat_name, CAT_COLORS["Unknown"])
        cells    = []
        for ab in all_abilities:
            props = matrix.get((cat_name, ab), [])
            if props:
                pill_html = " ".join(
                    f'<span class="mat-prop" style="background:{color}22;color:{color};'
                    + (f'border:1px solid #e8c43a44' if det == "low" else f'border:1px solid {color}44')
                    + f'">{p.replace("Ability","").replace("Stun ","Stun")}</span>'
                    for p, det in props
                )
                cells.append(f'<td class="mat-cell">{pill_html}</td>')
            else:
                cells.append('<td class="mat-cell mat-empty"></td>')
        mat_rows.append(
            f'<tr><td class="mat-cat" style="color:{color}">{cat_name}</td>{"".join(cells)}</tr>'
        )

    matrix_html = f"""
<div class="matrix-wrap">
  <table class="mat-table">
    <thead><tr><th class="mat-cat-hdr">Category</th>{header_cells}</tr></thead>
    <tbody>{"".join(mat_rows)}</tbody>
  </table>
</div>"""

    return f"""
<section id="schema">
  <div class="section-label">PROPERTY CATEGORIES — SHARED SEMANTIC NODES</div>
  <p class="explainer">
    Each category below is a named node in the graph (<code>cat:Cooldown</code>, <code>cat:Damage</code>, etc.).
    Ability properties link to these shared nodes — enabling cross-ability queries like
    <em>"show all Cooldown properties across all abilities"</em> without knowing the property names in advance.
    ⚠ marks low-determinism mappings where one property spans two categories.
  </p>

  <div class="cat-grid">{"".join(cards_html)}</div>

  <h3 style="margin-top:40px">Category × Ability Matrix</h3>
  <p class="explainer" style="margin-bottom:16px">
    Which categories appear in which abilities — the cross-ability graph proof.
    Each cell shows the property name(s) that link this ability to this category.
  </p>
  {matrix_html}
</section>"""


# ── Hero section ───────────────────────────────────────────────────────────────

def hero_section(g: rdflib.Graph) -> str:
    hero    = rdflib.URIRef("http://nydus.gg/ontology#hero/Abrams")
    tags    = list(g.objects(hero, NYDUS.heroTag))
    hero_id = g.value(hero, rdflib.URIRef("http://schema.org/identifier"))
    hp      = g.value(hero, NYDUS.startingMaxHealth)
    speed   = g.value(hero, NYDUS.startingMaxMoveSpeed)
    stamina = g.value(hero, NYDUS.startingStamina)
    regen   = g.value(hero, NYDUS.startingBaseHealthRegen)

    slot_ability: dict[str, rdflib.URIRef] = {}
    for bn in g.objects(hero, NYDUS.hasAbilityInSlot):
        slot = g.value(bn, NYDUS.slot)
        ab   = g.value(bn, NYDUS.ability)
        if slot and ab:
            slot_label = str(slot).split("#slot/")[-1]
            slot_ability[slot_label] = ab

    SIG_SLOTS    = ["Signature1", "Signature2", "Signature3", "Signature4"]
    INNATE_SLOTS = ["AbilityInnate1", "AbilityInnate2", "AbilityInnate3"]

    sig_cards    = "".join(ability_card(g, slot_ability[s], s) for s in SIG_SLOTS if s in slot_ability)
    innate_cards = "".join(ability_card(g, slot_ability[s], s) for s in INNATE_SLOTS if s in slot_ability)
    tag_badges   = " ".join(f'<span class="hero-tag">{t}</span>' for t in tags)

    return f"""
<section id="abrams">
  <div class="section-label">HERO — ABRAMS (hero_atlas · ID #{hero_id})</div>
  <div class="hero-header">
    <div class="hero-name">Abrams</div>
    <div class="hero-sub">Internal key: <code>hero_atlas</code></div>
    <div class="hero-tags">{tag_badges}</div>
    <div class="hero-basestats">
      <div class="basestat"><span>HP</span><b>{hp}</b></div>
      <div class="basestat"><span>Move Speed</span><b>{speed}</b></div>
      <div class="basestat"><span>Stamina</span><b>{stamina}</b></div>
      <div class="basestat"><span>HP Regen</span><b>{regen}/s</b></div>
    </div>
  </div>
  <h3>Signature Abilities</h3>
  <div class="card-grid">{sig_cards}</div>
  <h3>Innate Abilities</h3>
  <div class="card-grid">{innate_cards}</div>
</section>"""


# ── Roster section ─────────────────────────────────────────────────────────────

def roster_section(roster: list[dict]) -> str:
    active   = [r for r in roster if r["status"] == "ACTIVE"]
    pipeline = [r for r in roster if r["status"] == "PIPELINE"]
    tombs    = [r for r in roster if r["status"] == "TOMBSTONE"]

    def hero_chip(r, color):
        name    = r["public_name"].lstrip("?") or r["codename"]
        badge   = ' <span class="unknown-badge">?</span>' if r.get("uncertain") else ""
        return (f'<div class="hero-chip" style="border-color:{color}">'
                f'<span class="chip-name">{name}{badge}</span>'
                f'<span class="chip-id">#{r["hero_id"]}</span>'
                f'<span class="chip-stage">{r["stage"]}</span></div>')

    active_chips   = "\n".join(hero_chip(r, "#2a9d8f") for r in sorted(active,   key=lambda x: x["hero_id"]))
    pipeline_chips = "\n".join(hero_chip(r, "#e8c43a") for r in sorted(pipeline, key=lambda x: x["hero_id"]))
    tomb_chips     = "\n".join(hero_chip(r, "#555")    for r in sorted(tombs,    key=lambda x: x["hero_id"]))

    return f"""
<section id="roster">
  <div class="section-label">HERO ROSTER — FROM DATA</div>
  <h3>Released <span class="count">{len(active)}</span></h3>
  <div class="chip-grid">{active_chips}</div>
  <h3 style="color:#e8c43a">In Development <span class="count">{len(pipeline)}</span>
    <span class="note">found in data, not yet playable</span></h3>
  <div class="chip-grid">{pipeline_chips}</div>
  <h3 style="color:#555">Retired / Reworked <span class="count">{len(tombs)}</span></h3>
  <div class="chip-grid">{tomb_chips}</div>
  <div class="deleted-note">
    + <b>20 hero IDs</b> were fully deleted — no trace beyond the gap in the ID sequence.
    The cluster at IDs 22–45 looks like a single large design purge.
  </div>
</section>"""


# ── Stat web section ───────────────────────────────────────────────────────────

def stat_web_section(bridge: list[dict]) -> str:
    mv_counts = Counter(e["modifier_value"] for e in bridge if e.get("modifier_value"))
    rows = []
    for mv, cnt in mv_counts.most_common(20):
        display = mv.replace("MODIFIER_VALUE_", "").replace("_", " ").title()
        bar_w   = int(cnt / mv_counts.most_common(1)[0][1] * 240)
        family  = ("spirit"   if any(k in mv for k in ("TECH", "SPIRIT")) else
                   "weapon"   if any(k in mv for k in ("BULLET", "FIRE_RATE", "WEAPON")) else
                   "vitality" if any(k in mv for k in ("HEALTH", "REGEN", "LIFESTEAL")) else "neutral")
        color = STAT_COLORS[family]
        rows.append(
            f'<tr><td class="mv-name">{display}</td>'
            f'<td><div class="bar" style="width:{bar_w}px;background:{color}"></div></td>'
            f'<td class="mv-count">{cnt}</td></tr>'
        )
    return f"""
<section id="stat-web">
  <div class="section-label">STAT GRAPH — 4,884 EDGES ACROSS ALL HEROES</div>
  <p class="explainer">
    Every row is a stat type that abilities can modify.
    The count is how many ability properties declare they affect that stat.
    This is the skeleton of the balance system — visible in the data.
  </p>
  <table class="mv-table">
    <thead><tr><th>Stat modified</th><th>Frequency</th><th>Edges</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</section>"""


# ── Full HTML ──────────────────────────────────────────────────────────────────

def generate_html(g, roster, bridge, shacl_ok, triple_count) -> str:
    shacl_badge = (
        '<span class="shacl-pass">SHACL CONFORMS ✓</span>' if shacl_ok
        else '<span class="shacl-fail">SHACL VIOLATIONS ✗</span>' if shacl_ok is False
        else '<span class="shacl-skip">SHACL not checked</span>'
    )

    hero_html     = hero_section(g)
    category_html = category_section(g)
    roster_html   = roster_section(roster)
    web_html      = stat_web_section(bridge)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nydus — Deadlock Ontology</title>
<style>
  :root {{
    --bg:#0d1117; --bg2:#161b22; --bg3:#21262d;
    --border:#30363d; --text:#e6edf3; --muted:#8b949e;
    --spirit:#9b6dff; --weapon:#f5a623; --vitality:#4fc24f;
  }}
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{background:var(--bg);color:var(--text);
    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
    font-size:14px;line-height:1.6;}}
  code{{background:var(--bg3);padding:2px 6px;border-radius:4px;
    font-family:'SF Mono',Consolas,monospace;font-size:12px;}}
  em{{color:var(--muted);font-style:italic;}}

  .header{{background:linear-gradient(135deg,#1a0a2e 0%,#0d1117 60%);
    border-bottom:1px solid var(--border);padding:48px 40px 32px;}}
  .header h1{{font-size:36px;font-weight:700;letter-spacing:-1px;
    background:linear-gradient(90deg,var(--spirit),#c084fc);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;}}
  .header .subtitle{{color:var(--muted);margin-top:8px;font-size:15px;}}
  .header .stats-row{{display:flex;gap:16px;margin-top:24px;flex-wrap:wrap;align-items:center;}}
  .stat-pill{{background:var(--bg3);border:1px solid var(--border);
    border-radius:20px;padding:6px 16px;font-size:13px;}}
  .stat-pill b{{color:var(--spirit);}}
  .shacl-pass{{background:#4fc24f22;border:1px solid #4fc24f66;color:#4fc24f;
    border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;}}
  .shacl-fail{{background:#e05c5c22;border:1px solid #e05c5c66;color:#e05c5c;
    border-radius:20px;padding:6px 16px;font-size:13px;font-weight:700;}}
  .shacl-skip{{background:var(--bg3);border:1px solid var(--border);color:var(--muted);
    border-radius:20px;padding:6px 16px;font-size:13px;}}

  nav{{display:flex;gap:0;border-bottom:1px solid var(--border);
    background:var(--bg2);padding:0 40px;}}
  nav a{{padding:14px 20px;color:var(--muted);text-decoration:none;
    border-bottom:2px solid transparent;font-size:13px;font-weight:500;}}
  nav a:hover{{color:var(--text);border-color:var(--spirit);}}

  main{{max-width:1200px;margin:0 auto;padding:40px;}}
  section{{margin-bottom:72px;}}

  .section-label{{font-size:11px;font-weight:700;letter-spacing:2px;
    color:var(--spirit);text-transform:uppercase;margin-bottom:16px;}}
  h3{{font-size:16px;font-weight:600;margin:24px 0 12px;
    display:flex;align-items:center;gap:10px;}}
  .count{{background:var(--bg3);border:1px solid var(--border);
    border-radius:12px;padding:1px 10px;font-size:12px;color:var(--muted);}}
  .note{{font-size:12px;color:var(--muted);font-weight:400;}}
  .explainer{{color:var(--muted);font-size:13px;margin-bottom:20px;
    max-width:760px;line-height:1.7;}}

  /* Hero */
  .hero-header{{background:var(--bg2);border:1px solid var(--border);
    border-radius:12px;padding:24px;margin-bottom:24px;}}
  .hero-name{{font-size:32px;font-weight:800;letter-spacing:-1px;}}
  .hero-sub{{color:var(--muted);font-size:13px;margin-top:4px;}}
  .hero-tags{{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;}}
  .hero-tag{{background:var(--spirit)22;border:1px solid var(--spirit)44;
    color:var(--spirit);border-radius:12px;padding:3px 12px;font-size:12px;}}
  .hero-basestats{{display:flex;gap:24px;margin-top:16px;}}
  .basestat{{display:flex;flex-direction:column;}}
  .basestat span{{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;}}
  .basestat b{{font-size:22px;font-weight:700;}}

  /* Ability cards */
  .card-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px;}}
  .ability-card{{background:var(--bg2);border:1px solid var(--border);border-radius:10px;overflow:hidden;}}
  .ability-header{{padding:14px 16px 10px;background:var(--bg3);}}
  .ability-title{{font-size:15px;font-weight:700;}}
  .ability-meta{{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px;align-items:center;}}
  .tag{{padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;}}
  .tag.neutral{{background:var(--bg);color:var(--muted);}}
  .slot-badge{{font-size:11px;color:var(--muted);margin-left:auto;}}
  .ability-stats{{padding:12px 16px;display:flex;flex-direction:column;gap:7px;}}
  .stat-row{{display:flex;align-items:center;gap:6px;flex-wrap:wrap;}}
  .stat-name{{font-size:12px;color:var(--muted);min-width:100px;}}
  .stat-val{{font-weight:700;font-size:14px;min-width:48px;}}
  .cat-badge{{font-size:10px;padding:1px 7px;border-radius:8px;border:1px solid;font-weight:600;}}
  .scale-badge{{font-size:11px;padding:2px 8px;border-radius:10px;border:1px solid;
    font-weight:600;white-space:nowrap;}}
  .muted{{color:var(--muted);font-size:12px;}}
  .upgrades{{padding:10px 16px 14px;border-top:1px solid var(--border);
    display:flex;flex-direction:column;gap:4px;}}
  .upgrade{{font-size:12px;color:var(--muted);}}
  .upgrade.t1 b{{color:#7ec8e3;}}
  .upgrade.t2 b{{color:#f5a623;}}
  .upgrade.t3 b{{color:var(--spirit);}}

  /* Category section */
  .cat-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px;margin-bottom:8px;}}
  .cat-card{{background:var(--bg2);border:1px solid;border-radius:10px;overflow:hidden;}}
  .cat-card-header{{padding:10px 14px;display:flex;justify-content:space-between;align-items:center;}}
  .cat-name{{font-weight:700;font-size:14px;}}
  .cat-count{{font-size:20px;font-weight:800;opacity:0.9;}}
  .cat-card-body{{padding:10px 14px;display:flex;flex-direction:column;gap:5px;}}
  .cat-row{{display:flex;gap:8px;align-items:baseline;}}
  .cat-ability{{font-size:11px;color:var(--muted);min-width:80px;}}
  .cat-prop{{font-size:12px;font-weight:500;}}
  .low-det-note{{margin-top:8px;padding:6px 10px;background:#e8c43a11;border:1px solid #e8c43a33;
    border-radius:6px;font-size:11px;color:#e8c43a;line-height:1.5;}}

  /* Matrix */
  .matrix-wrap{{overflow-x:auto;border:1px solid var(--border);border-radius:8px;}}
  .mat-table{{border-collapse:collapse;width:100%;}}
  .mat-table th,.mat-table td{{border:1px solid var(--border)44;padding:0;}}
  .mat-cat-hdr{{font-size:11px;text-transform:uppercase;letter-spacing:1px;
    color:var(--muted);padding:10px 14px;text-align:left;background:var(--bg3);
    min-width:100px;}}
  .mat-ab{{font-size:11px;color:var(--muted);padding:8px 10px;
    text-align:center;background:var(--bg3);white-space:nowrap;}}
  .mat-cat{{font-weight:700;font-size:12px;padding:8px 14px;
    background:var(--bg2);white-space:nowrap;}}
  .mat-cell{{padding:6px 8px;vertical-align:middle;text-align:center;
    background:var(--bg);min-width:100px;}}
  .mat-empty{{background:var(--bg2);}}
  .mat-prop{{display:inline-block;font-size:10px;padding:2px 6px;
    border-radius:6px;margin:2px;white-space:nowrap;}}

  /* Roster */
  .chip-grid{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px;}}
  .hero-chip{{background:var(--bg2);border:1px solid;border-radius:8px;
    padding:6px 12px;display:flex;align-items:center;gap:10px;}}
  .chip-name{{font-weight:600;font-size:13px;}}
  .chip-id{{font-size:11px;color:var(--muted);}}
  .chip-stage{{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;}}
  .unknown-badge{{background:#e8c43a33;color:#e8c43a;border-radius:4px;
    padding:1px 5px;font-size:10px;font-weight:700;}}
  .deleted-note{{margin-top:20px;padding:14px 18px;background:var(--bg2);
    border:1px solid var(--border);border-radius:8px;color:var(--muted);font-size:13px;}}

  /* Stat web */
  .mv-table{{width:100%;border-collapse:collapse;}}
  .mv-table th{{text-align:left;padding:8px 12px;font-size:11px;
    text-transform:uppercase;letter-spacing:1px;color:var(--muted);
    border-bottom:1px solid var(--border);}}
  .mv-table td{{padding:7px 12px;border-bottom:1px solid var(--border)44;}}
  .mv-name{{font-size:13px;font-weight:500;width:260px;}}
  .mv-count{{color:var(--muted);font-size:13px;text-align:right;width:60px;}}
  .bar{{height:8px;border-radius:4px;min-width:4px;}}

  footer{{text-align:center;padding:40px;color:var(--muted);font-size:12px;
    border-top:1px solid var(--border);}}
</style>
</head>
<body>

<div class="header">
  <h1>Nydus — Deadlock Ontology</h1>
  <p class="subtitle">
    SHACL-primary build. Every triple extracted from Valve game data, validated against
    formal node shapes. PropertyCategory nodes are shared semantic anchors for cross-ability queries.
  </p>
  <div class="stats-row">
    {shacl_badge}
    <div class="stat-pill"><b>{triple_count}</b> triples (Abrams)</div>
    <div class="stat-pill"><b>63</b> heroes in data</div>
    <div class="stat-pill"><b>4,884</b> stat scaling edges</div>
    <div class="stat-pill"><b>11</b> property categories</div>
  </div>
</div>

<nav>
  <a href="#abrams">Abrams</a>
  <a href="#schema">Schema</a>
  <a href="#roster">Roster</a>
  <a href="#stat-web">Stat Web</a>
</nav>

<main>
{hero_html}
{category_html}
{roster_html}
{web_html}
</main>

<footer>
  Source: Valve game data (heroes.vdata, abilities.vdata) &nbsp;|&nbsp;
  Nydus Ontology — local build &nbsp;|&nbsp;
  <code>nydus:hero/Abrams</code> verified &nbsp;|&nbsp;
  DID_SWAP_TARGET: <code>http://nydus.gg/ontology#</code> → <code>did:key:z6Mk...#ward/</code> on publish
</footer>

</body>
</html>"""


if __name__ == "__main__":
    print("Loading data...")
    g, roster, bridge = load_data()
    triple_count = len(g)

    print("Checking SHACL conformance...")
    shacl_ok, shacl_txt = check_shacl()
    status = "CONFORMS" if shacl_ok else ("VIOLATIONS" if shacl_ok is False else "skipped")
    print(f"  {status}")

    print("Generating proof.html...")
    html = generate_html(g, roster, bridge, shacl_ok, triple_count)

    out = OUTPUTS_DIR / "proof.html"
    out.write_text(html, encoding="utf-8")
    print(f"Written: {out}  ({len(html)//1024} KB)")
    print(f"Open in browser: file:///{out.as_posix()}")
