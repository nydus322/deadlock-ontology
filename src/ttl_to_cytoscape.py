#!/usr/bin/env python3
"""
ttl_to_cytoscape.py  —  Turtle -> Cytoscape.js graph JSON.

Converts a Nydus TTL file to the elements format consumed by the viewer:

    {
      "nodes": [{"data": {"id", "label", "classes", "shortId",
                          "properties": {predicate: literal, ...}}}, ...],
      "edges": [{"data": {"id", "source", "target", "label", "classes"}}, ...]
    }

Rules:
  - Named resource (IRI)       -> node, id = full IRI
  - Blank node                 -> node, id = stable synthetic ID derived from
                                  parent subject + discriminator (internalName,
                                  upgradeLevel, or edge index). NOT rdflib's
                                  ephemeral _:NbN.
  - Triple (s, p, literal)     -> stored on s node as properties[predicate]
  - Triple (s, p, resource)    -> edge s -> o, labelled by predicate
  - rdf:type                   -> folded into node "classes" tag

Usage:
  # Single TTL -> single graph.json:
  PYTHONUTF8=1 python3 src/ttl_to_cytoscape.py <input.ttl> <output.json>

  # Directory of per-hero TTLs (outputs/heroes/) -> combined graphs.json:
  PYTHONUTF8=1 python3 src/ttl_to_cytoscape.py --bundle <heroes_dir> <output.json>
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import rdflib
from rdflib import BNode, Literal, URIRef
from rdflib.namespace import RDF, RDFS

NYDUS_BASE = "http://nydus.gg/ontology#"

PREFIXES = {
    f"{NYDUS_BASE}hero/":    "hero",
    f"{NYDUS_BASE}ability/": "ability",
    f"{NYDUS_BASE}stat/":    "stat",
    f"{NYDUS_BASE}mv/":      "mv",
    f"{NYDUS_BASE}slot/":    "slot",
    f"{NYDUS_BASE}sf/":      "sf",
    f"{NYDUS_BASE}cat/":     "cat",
    f"{NYDUS_BASE}stage/":   "stage",
    NYDUS_BASE:                          "nydus",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
    "http://www.w3.org/2001/XMLSchema#":   "xsd",
    "http://www.w3.org/2004/02/skos/core#": "skos",
    "http://schema.org/":                   "schema",
    "http://www.w3.org/ns/prov#":           "prov",
}


def shorten(iri: str) -> str:
    """IRI -> prefix:local (e.g. 'ability:BullCharge'). Falls back to full IRI."""
    for base, prefix in PREFIXES.items():
        if iri.startswith(base):
            return f"{prefix}:{iri[len(base):]}"
    return iri


def short_id(iri: str) -> str:
    """URL-safe short identifier for hash routing: 'ability/BullCharge'."""
    for base, prefix in PREFIXES.items():
        if iri.startswith(base):
            return f"{prefix}/{iri[len(base):]}"
    return iri


def local_name(iri: str) -> str:
    s = shorten(iri)
    return s.split(":", 1)[-1] if ":" in s else s


def type_class(rdf_type_iri: str) -> str:
    """rdf:type URI -> short class tag, e.g. nydus:Ability -> 'Ability'."""
    s = shorten(rdf_type_iri)
    return s.split(":", 1)[-1] if ":" in s else s


# IRI prefix -> class tag inferred when no rdf:type is declared.
PREFIX_CLASS = {
    "stat":    "Stat",
    "slot":    "Slot",
    "sf":      "ScaleFunction",
    "mv":      "ModifierValue",
    "stage":   "Stage",
    "cat":     "PropertyCategory",
    "hero":    "Hero",
    "ability": "Ability",
}


def infer_class_from_iri(iri: str) -> str | None:
    s = shorten(iri)
    if ":" in s:
        prefix = s.split(":", 1)[0]
        return PREFIX_CLASS.get(prefix)
    return None


def predicate_class(pred_iri: str) -> str:
    """Predicate IRI -> short class tag for edge styling."""
    s = shorten(pred_iri)
    return s.split(":", 1)[-1] if ":" in s else s


def stable_blank_id(g: rdflib.Graph, bnode: BNode, parent_iri: str | None) -> str:
    """Synthesize a stable, human-readable ID for a blank node.

    Blank-node IDs from rdflib are ephemeral (NbN hex). For a viewer we want
    reruns to produce the same IDs so the graph doesn't churn on regeneration.
    Derive from (parent IRI, discriminator from blank node's own triples).
    """
    parent_short = short_id(parent_iri) if parent_iri else "orphan"

    # Try to extract a stable discriminator from the blank node's content.
    discriminators = []
    for p, o in g.predicate_objects(bnode):
        pn = local_name(str(p))
        if pn in ("internalName", "modifiesProperty") and isinstance(o, Literal):
            discriminators.append(str(o))
            break
        if pn == "upgradeLevel" and isinstance(o, Literal):
            discriminators.append(f"upg{o}")
        if pn == "slot":
            discriminators.append(local_name(str(o)))
        if pn == "ability":
            discriminators.append(local_name(str(o)))
        if pn == "bonusValue" and isinstance(o, Literal):
            discriminators.append(str(o).replace(" ", "_")[:20])

    disc = "_".join(discriminators) if discriminators else f"b{hash(bnode) & 0xFFFFFF:06x}"
    return f"_:{parent_short}::{disc}"


def build_payload(ttl_path: Path) -> dict:
    """Parse a single TTL and return a {meta, nodes, edges} payload dict."""
    g = rdflib.Graph()
    g.parse(ttl_path, format="turtle")

    # Pass 1: assign every RDF node (URIRef or BNode) a canonical string id.
    # For blank nodes we walk from parent to child to get stable IDs.
    bnode_id: dict[BNode, str] = {}

    # Find blank-node parents: any triple (s, p, bnode) where s is a URIRef
    # assigns that URIRef as the blank node's parent.
    for s, p, o in g:
        if isinstance(o, BNode) and isinstance(s, URIRef) and o not in bnode_id:
            bnode_id[o] = stable_blank_id(g, o, str(s))

    # Handle chained blank nodes (blank-node -> blank-node).
    # Iterate until no new assignments.
    progressed = True
    while progressed:
        progressed = False
        for s, p, o in g:
            if isinstance(o, BNode) and o not in bnode_id and isinstance(s, BNode) and s in bnode_id:
                bnode_id[o] = stable_blank_id(g, o, bnode_id[s])
                progressed = True

    # Fallback for any orphan blank nodes.
    for s in g.all_nodes():
        if isinstance(s, BNode) and s not in bnode_id:
            bnode_id[s] = stable_blank_id(g, s, None)

    def node_id(n) -> str:
        if isinstance(n, BNode):
            return bnode_id[n]
        return str(n)

    # Pass 2: build node records keyed by id.
    nodes: dict[str, dict] = {}

    def ensure_node(n) -> dict:
        nid = node_id(n)
        if nid not in nodes:
            is_blank = isinstance(n, BNode)
            label_fallback = local_name(nid.split("::", 1)[-1]) if is_blank else local_name(str(n))
            nodes[nid] = {
                "id":         nid,
                "shortId":    short_id(nid) if not is_blank else nid,
                "iri":        nid if not is_blank else None,
                "label":      label_fallback,
                "classes":    set(["BlankNode"]) if is_blank else set(),
                "properties": {},  # predicate_short -> [values]
            }
        return nodes[nid]

    # Pass 3: walk all triples.
    for s, p, o in g:
        s_node = ensure_node(s)
        pn = predicate_class(str(p))

        if p == RDF.type and isinstance(o, URIRef):
            s_node["classes"].add(type_class(str(o)))
            continue

        if p == RDFS.label and isinstance(o, Literal):
            # Use the English label if available; any rdfs:label is a candidate.
            lang = getattr(o, "language", None)
            if lang in (None, "en") or not s_node.get("_label_set"):
                s_node["label"] = str(o)
                s_node["_label_set"] = True
            # Also retain as a property
            s_node["properties"].setdefault(pn, []).append(str(o))
            continue

        if isinstance(o, Literal):
            s_node["properties"].setdefault(pn, []).append(str(o))
        else:
            # Resource or blank node -> edge
            ensure_node(o)

    # Pass 4: emit edges in a stable order.
    edges_seen = set()
    edges_out = []
    for s, p, o in g:
        if p == RDF.type or p == RDFS.label:
            continue
        if isinstance(o, Literal):
            continue
        sid = node_id(s)
        oid = node_id(o)
        pn = predicate_class(str(p))
        eid = f"{sid}|{pn}|{oid}"
        if eid in edges_seen:
            continue
        edges_seen.add(eid)
        edges_out.append({
            "data": {
                "id":      eid,
                "source":  sid,
                "target":  oid,
                "label":   pn,
                "classes": pn,
            }
        })

    # Finalize nodes: convert sets to space-separated class strings, clean up.
    nodes_out = []
    for nid in sorted(nodes.keys()):
        n = nodes[nid]
        # Infer class from IRI prefix when no rdf:type was declared.
        if not n["classes"] and n.get("iri"):
            inferred = infer_class_from_iri(n["iri"])
            if inferred:
                n["classes"].add(inferred)
        classes = n["classes"] or {"Resource"}
        n.pop("_label_set", None)
        # Flatten single-value property lists for readability.
        props = {}
        for k, vs in n["properties"].items():
            props[k] = vs[0] if len(vs) == 1 else vs
        nodes_out.append({
            "data": {
                "id":         n["id"],
                "shortId":    n["shortId"],
                "iri":        n["iri"],
                "label":      n["label"],
                "classes":    " ".join(sorted(classes)),
                "properties": props,
            }
        })

    class_counts: dict[str, int] = defaultdict(int)
    for n in nodes_out:
        for c in n["data"]["classes"].split():
            class_counts[c] += 1

    return {
        "meta": {
            "source":        str(ttl_path.name),
            "node_count":    len(nodes_out),
            "edge_count":    len(edges_out),
            "class_counts":  dict(class_counts),
        },
        "nodes": nodes_out,
        "edges": edges_out,
    }


def convert(ttl_path: Path, out_path: Path) -> None:
    """Single TTL -> single graph.json."""
    payload = build_payload(ttl_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    edge_label_counts: dict[str, int] = defaultdict(int)
    for e in payload["edges"]:
        edge_label_counts[e["data"]["label"]] += 1
    print(f"Wrote {out_path}")
    print(f"  {payload['meta']['node_count']} nodes, {payload['meta']['edge_count']} edges")
    print(f"  Node classes: {payload['meta']['class_counts']}")
    print(f"  Edge predicates: {dict(sorted(edge_label_counts.items(), key=lambda x: -x[1]))}")


def bundle(heroes_dir: Path, out_path: Path) -> None:
    """Directory of {codename}.ttl + index.json -> combined graphs.json.

    Output shape:
      {
        "meta":   {"hero_count": N, "source_dir": "..."},
        "heroes": {
           "hero_inferno": {"codename", "public_name", "hero_id",
                            "meta", "nodes", "edges"},
           ...
        },
        "order":  ["hero_inferno", "hero_atlas", ...]   # display order
      }
    """
    index_path = heroes_dir / "index.json"
    if not index_path.exists():
        raise SystemExit(f"Missing {index_path}. Run graph_builder.py first.")
    index = json.loads(index_path.read_text(encoding="utf-8"))

    heroes_entries = index.get("heroes", index) if isinstance(index, dict) else index

    heroes_payload: dict[str, dict] = {}
    order: list[str] = []
    for entry in heroes_entries:
        codename = entry["codename"]
        ttl_path = heroes_dir / f"{codename}.ttl"
        if not ttl_path.exists():
            print(f"  SKIP {codename}: missing {ttl_path}", file=sys.stderr)
            continue
        payload = build_payload(ttl_path)
        heroes_payload[codename] = {
            "codename":    codename,
            "public_name": entry.get("public_name", codename),
            "hero_id":     entry.get("hero_id"),
            "meta":        payload["meta"],
            "nodes":       payload["nodes"],
            "edges":       payload["edges"],
        }
        order.append(codename)
        print(f"  {codename:24s} {payload['meta']['node_count']:4d} nodes  {payload['meta']['edge_count']:4d} edges  ({entry.get('public_name', '')})")

    order.sort(key=lambda c: heroes_payload[c]["public_name"].lower())

    combined = {
        "meta": {
            "hero_count": len(heroes_payload),
            "source_dir": str(heroes_dir),
        },
        "order":  order,
        "heroes": heroes_payload,
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(combined), encoding="utf-8")
    total_nodes = sum(h["meta"]["node_count"] for h in heroes_payload.values())
    total_edges = sum(h["meta"]["edge_count"] for h in heroes_payload.values())
    print(f"Wrote {out_path}")
    print(f"  {len(heroes_payload)} heroes, {total_nodes} nodes total, {total_edges} edges total")


def main():
    args = sys.argv[1:]
    if len(args) == 3 and args[0] == "--bundle":
        bundle(Path(args[1]), Path(args[2]))
    elif len(args) == 2:
        convert(Path(args[0]), Path(args[1]))
    else:
        print(
            "Usage:\n"
            "  ttl_to_cytoscape.py <input.ttl> <output.json>\n"
            "  ttl_to_cytoscape.py --bundle <heroes_dir> <output.json>",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
