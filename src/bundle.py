#!/usr/bin/env python3
"""
bundle.py  —  single-file build of the Nydus viewer.

Inlines styles.css, lib/*.js, viewer.js, and graphs.json into a single
outputs/nydus.html that is self-contained: open via file:// or paste into
any static host (GitHub Gist raw, Pastebin, Netlify drop, etc.).

The generated HTML still reads the URL hash for deep linking
(#hero/<name>, #hero/<name>/node/<shortId>), so shared links survive.

Usage:
  PYTHONUTF8=1 python3 src/bundle.py
"""

import html
import json
from pathlib import Path

ROOT     = Path(__file__).parent.parent
VIEWER   = ROOT / "outputs" / "viewer"
OUT_PATH = ROOT / "outputs" / "nydus.html"

# Libs are inlined in dependency order.
LIB_ORDER = [
    "lib/cytoscape.min.js",
    "lib/layout-base.js",
    "lib/cose-base.js",
    "lib/cytoscape-fcose.js",
]

OG_TITLE = "Nydus — Deadlock Ontology Graph"
OG_DESCRIPTION = (
    "Navigable knowledge graph of every Deadlock hero's abilities, "
    "properties, and stat scaling. Click a hero, walk the topology."
)


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def build() -> None:
    css        = read_text(VIEWER / "styles.css")
    viewer_js  = read_text(VIEWER / "viewer.js")
    graphs     = read_text(VIEWER / "graphs.json")
    libs_js    = "\n".join(read_text(VIEWER / lib) for lib in LIB_ORDER)

    # Parse to count heroes for the subtitle.
    graphs_data = json.loads(graphs)
    hero_count  = graphs_data["meta"]["hero_count"]

    # Read the viewer index.html as a template.
    index_html = read_text(VIEWER / "index.html")

    # Strip external references: <link rel="stylesheet" href="styles.css">,
    # all <script src="lib/...">, and <script src="viewer.js">.
    lines = []
    skip_tokens = (
        'href="styles.css"',
        'src="lib/',
        'src="viewer.js"',
    )
    for line in index_html.splitlines():
        if any(tok in line for tok in skip_tokens):
            continue
        lines.append(line)
    stripped = "\n".join(lines)

    # Insert inline assets in the same spots:
    #  - inline <style> right before </head>
    #  - inline bundle <script> (libs + data + viewer) right before </body>
    inline_style = f"<style>\n{css}\n</style>"

    bundle_script = (
        "<script>\n"
        f"window.__NYDUS_BUNDLE__ = {graphs};\n"
        "</script>\n"
        f"<script>\n{libs_js}\n</script>\n"
        f"<script>\n{viewer_js}\n</script>"
    )

    stripped = stripped.replace("</head>", f"{inline_style}\n</head>", 1)
    stripped = stripped.replace("</body>", f"{bundle_script}\n</body>", 1)

    # Update title + subtitle copy for the shipped build (count-aware).
    stripped = stripped.replace(
        'loading&hellip;',
        f"{hero_count} heroes &middot; click the picker",
    )
    # Tighten the <title> with the hero count.
    stripped = stripped.replace(
        "<title>Nydus — Deadlock Ontology Graph</title>",
        f"<title>{html.escape(OG_TITLE)} &middot; {hero_count} heroes</title>",
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(stripped, encoding="utf-8")

    size_kb = OUT_PATH.stat().st_size / 1024
    print(f"Wrote {OUT_PATH} ({size_kb:.1f} KB)")
    print(f"  {hero_count} heroes inlined")
    print(f"  Open directly (file://) or drop on any static host.")


if __name__ == "__main__":
    build()
