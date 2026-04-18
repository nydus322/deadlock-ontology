// Nydus Deadlock graph viewer.
// Multi-hero: loads graphs.json, hero picker + URL routing, inspector, filters.
// URL hash forms:
//   #hero/Infernus
//   #hero/Infernus/node/ability/InfernusFireBomb
//   (legacy) #node/ability/InfernusFireBomb  -> falls back to current hero

(() => {
  const DEFAULT_HERO = "hero_inferno";

  // Slots a player actually cares about: the 4 signature abilities + primary weapon.
  // Everything else (movement, innates, melee, ziplines) is engine plumbing shared
  // across all heroes and only shown when "Show all" is toggled on.
  const SIGNATURE_SLOT_SHORT_IDS = new Set([
    "slot/Signature1",
    "slot/Signature2",
    "slot/Signature3",
    "slot/Signature4",
    "slot/WeaponPrimary",
  ]);

  // Property-panel keys that duplicate the node label or leak engine internals.
  // These are never shown in the inspector's literal-properties table.
  const HIDDEN_PROP_KEYS = new Set([
    "label",              // duplicates the node's H1 heading
    "altLabel",           // duplicates label
    "internalName",       // engine identifier
    "internalKey",        // engine identifier (e.g. hero_inferno)
    "identifier",         // internal hero_id
    "isDisabled",         // admin flag
    "isPlayerSelectable", // admin flag
    "complexity",         // internal Valve rating (0-3), unclear to players
  ]);

  // Outgoing / Incoming rows whose predicate is one of these are suppressed.
  // Kept in sync with ttl_to_cytoscape.py HIDDEN_PREDICATES — belt-and-suspenders
  // so older pre-filter bundles still display cleanly.
  const HIDDEN_PREDICATES = new Set(["wasDerivedFrom", "developerStage"]);

  // Slot shortIds in presentation order. Hero cards should read weapon first,
  // then Ability 1..4 in slot order. Utility slots (movement, melee, etc.)
  // are sorted after these in the order they happen to appear.
  const SLOT_SORT_ORDER = [
    "slot/WeaponPrimary",
    "slot/Signature1",
    "slot/Signature2",
    "slot/Signature3",
    "slot/Signature4",
  ];

  const CLASS_COLORS = {
    Hero:             "#ff7b72",
    Ability:          "#ffa657",
    PropertyCategory: "#c084fc",
    Stat:             "#9b6dff",
    Slot:             "#79c0ff",
    ScaleFunction:    "#56d4dd",
    ModifierValue:    "#d2a8ff",
    AbilityProperty:  "#6e7681",
    AbilityUpgrade:   "#484f58",
    Stage:            "#8b949e",
    BlankNode:        "#30363d",
    Resource:         "#8b949e",
  };
  const CLASS_ORDER = [
    "Hero", "Ability", "AbilityProperty", "AbilityUpgrade",
    "PropertyCategory", "Stat", "Slot", "ScaleFunction", "ModifierValue",
    "Stage", "BlankNode", "Resource",
  ];
  const CLASS_SIZE = {
    Hero: 62, Ability: 44, PropertyCategory: 34, Stat: 34, Slot: 26,
    ScaleFunction: 30, ModifierValue: 26, AbilityProperty: 20,
    AbilityUpgrade: 18, Stage: 22, BlankNode: 16, Resource: 20,
  };

  const state = {
    bundle:       null,   // whole graphs.json
    currentHero:  null,   // codename (e.g. "hero_inferno")
    graph:        null,   // active hero's {meta, nodes, edges}
    cy:           null,
    classFilter:  new Set(),
    edgeFilter:   new Set(),
    expanded:     new Set(),
    nodesById:    new Map(),
    shortIdToId:  new Map(),
    kitMode:      true,   // default: show only signature kit
    kitSet:       null,   // per-hero set of node IDs that are part of the signature kit
  };

  // ---- Data loading -----------------------------------------------------------

  async function load() {
    // Prefer inline bundle (for single-file build); fallback to fetch.
    if (window.__NYDUS_BUNDLE__) return window.__NYDUS_BUNDLE__;
    const r = await fetch("graphs.json");
    if (!r.ok) throw new Error(`graphs.json load failed: ${r.status}`);
    return r.json();
  }

  function primaryClass(classesStr) {
    const list = (classesStr || "").split(/\s+/).filter(Boolean);
    for (const c of CLASS_ORDER) if (list.includes(c)) return c;
    return list[0] || "Resource";
  }

  // ---- Cytoscape --------------------------------------------------------------

  function makeCy(elements) {
    const styleSheet = [
      {
        selector: "node",
        style: {
          "background-color": (n) => CLASS_COLORS[primaryClass(n.data("classes"))] || "#555",
          "label": "data(label)",
          "color": "#c9d1d9",
          "font-size": 9,
          "text-valign": "bottom",
          "text-margin-y": 4,
          "text-background-color": "#0d1117",
          "text-background-opacity": 0.85,
          "text-background-padding": 2,
          "text-background-shape": "roundrectangle",
          "text-wrap": "wrap",
          "text-max-width": 100,
          "width":  (n) => CLASS_SIZE[primaryClass(n.data("classes"))] || 20,
          "height": (n) => CLASS_SIZE[primaryClass(n.data("classes"))] || 20,
          "border-width": 1,
          "border-color": "#1f2630",
          "transition-property": "opacity, border-color, border-width",
          "transition-duration": "150ms",
        },
      },
      { selector: "node.BlankNode", style: { "shape": "round-rectangle" } },
      { selector: "node.Hero",             style: { "shape": "star",    "font-size": 12, "text-margin-y": 6 } },
      { selector: "node.Ability",          style: { "shape": "round-hexagon", "font-size": 11 } },
      { selector: "node.PropertyCategory", style: { "shape": "round-diamond" } },
      { selector: "node.Stat",             style: { "shape": "round-diamond" } },
      { selector: "node.Slot",             style: { "shape": "round-triangle" } },
      { selector: "node.ScaleFunction",    style: { "shape": "round-pentagon" } },
      { selector: "node.ModifierValue",    style: { "shape": "round-octagon" } },
      { selector: "node:selected", style: {
          "border-color": "#ff9d47", "border-width": 3,
      }},
      { selector: "node.hidden", style: { "display": "none" } },
      { selector: "node.collapsed", style: { "opacity": 0.08 } },
      {
        selector: "edge",
        style: {
          "width": 1,
          "line-color": "#30363d",
          "target-arrow-color": "#30363d",
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
          "opacity": 0.6,
          "label": "data(label)",
          "font-size": 8,
          "color": "#8b949e",
          "text-background-color": "#0d1117",
          "text-background-opacity": 0.9,
          "text-background-padding": 1,
          "text-rotation": "autorotate",
          "text-opacity": 0,
          "transition-property": "opacity, line-color, width, text-opacity",
          "transition-duration": "120ms",
        },
      },
      { selector: "edge.scalesStat",            style: { "line-color": "#9b6dff", "target-arrow-color": "#9b6dff", "width": 1.6, "opacity": 0.85 } },
      { selector: "edge.primaryCategory",       style: { "line-color": "#c084fc", "target-arrow-color": "#c084fc", "opacity": 0.7 } },
      { selector: "edge.secondaryCategory",     style: { "line-color": "#c084fc", "target-arrow-color": "#c084fc", "line-style": "dashed", "opacity": 0.6 } },
      { selector: "edge.hasProperty",           style: { "line-color": "#484f58", "target-arrow-color": "#484f58" } },
      { selector: "edge.hasUpgrade",            style: { "line-color": "#6e7681", "target-arrow-color": "#6e7681" } },
      { selector: "edge.hasAbilityInSlot",      style: { "line-color": "#79c0ff", "target-arrow-color": "#79c0ff" } },
      { selector: "edge.providesModifierType",  style: { "line-color": "#d2a8ff", "target-arrow-color": "#d2a8ff" } },
      { selector: "edge:selected", style: { "line-color": "#ff9d47", "target-arrow-color": "#ff9d47", "width": 2.5, "text-opacity": 1 } },
      { selector: "edge.hidden", style: { "display": "none" } },
      { selector: "edge.collapsed", style: { "opacity": 0.05 } },
      { selector: ".highlighted", style: { "text-opacity": 1 } },
    ];

    const cy = cytoscape({
      container: document.getElementById("graph"),
      elements,
      style: styleSheet,
      wheelSensitivity: 0.25,
      minZoom: 0.2,
      maxZoom: 4,
    });

    cy.nodes().forEach((n) => {
      const pc = primaryClass(n.data("classes"));
      n.addClass(pc);
      (n.data("classes") || "").split(/\s+/).filter(Boolean).forEach((c) => {
        if (c !== pc) n.addClass(c);
      });
    });
    cy.edges().forEach((e) => {
      const p = e.data("classes");
      if (p) e.addClass(p);
    });
    return cy;
  }

  // ---- Kit mode (Hero -> 4 Abilities -> effects) ------------------------------

  function computeKitSet(graph) {
    const heroNode = graph.nodes.find((n) => (n.data.classes || "").split(/\s+/).includes("Hero"));
    if (!heroNode) return new Set(graph.nodes.map((n) => n.data.id));
    const heroId = heroNode.data.id;

    const outgoing = new Map();
    graph.edges.forEach((e) => {
      const s = e.data.source, t = e.data.target, p = e.data.label;
      if (!outgoing.has(s)) outgoing.set(s, []);
      outgoing.get(s).push([t, p]);
    });
    const nodeById = new Map(graph.nodes.map((n) => [n.data.id, n.data]));

    const kit = new Set([heroId]);
    const sigAbilities = [];

    (outgoing.get(heroId) || []).forEach(([bnodeId, pred]) => {
      if (pred !== "hasAbilityInSlot") return;
      const bnodeOuts = outgoing.get(bnodeId) || [];
      const slotEdge = bnodeOuts.find(([, pp]) => pp === "slot");
      if (!slotEdge) return;
      const slotNode = nodeById.get(slotEdge[0]);
      const slotShort = slotNode?.shortId || "";
      if (!SIGNATURE_SLOT_SHORT_IDS.has(slotShort)) return;
      kit.add(bnodeId);
      bnodeOuts.forEach(([t, pp]) => {
        kit.add(t);
        if (pp === "ability") sigAbilities.push(t);
      });
    });

    // For each signature ability, include its properties, upgrades, and their 1-hop
    // (scale functions -> stats, property categories, modifier values).
    sigAbilities.forEach((aid) => {
      (outgoing.get(aid) || []).forEach(([t]) => {
        kit.add(t);
        (outgoing.get(t) || []).forEach(([t2]) => {
          kit.add(t2);
          (outgoing.get(t2) || []).forEach(([t3]) => kit.add(t3));
        });
      });
    });

    return kit;
  }

  function applyKitMode() {
    if (!state.cy || !state.kitSet) return;
    if (state.kitMode) {
      state.cy.nodes().forEach((n) => n.toggleClass("hidden", !state.kitSet.has(n.id())));
    } else {
      state.cy.nodes().forEach((n) => n.removeClass("hidden"));
    }
    applyEdgeFilter();
    updateKitModeButton();
  }

  function updateKitModeButton() {
    const btn = document.getElementById("btn-kit-mode");
    if (!btn) return;
    btn.textContent = state.kitMode ? "Show all nodes" : "Kit only";
    btn.title = state.kitMode
      ? "Currently showing the signature kit — click to reveal movement, melee, and utility nodes."
      : "Currently showing every node — click to focus on the 4 signature abilities.";
  }

  // ---- Property-panel pretty-print --------------------------------------------

  function prettifyPropKey(k) {
    // Strip "starting" prefix that Deadlock uses on hero-base stats.
    //   startingMaxHealth -> "Max Health"
    //   startingStaminaRegenPerSecond -> "Stamina Regen Per Second"
    let key = k.replace(/^starting/, "");
    if (key.length === 0) key = k;
    const spaced = key.replace(/([a-z0-9])([A-Z])/g, "$1 $2");
    return spaced.charAt(0).toUpperCase() + spaced.slice(1);
  }
  function prettifyPropValue(k, v) {
    if (typeof v === "number") {
      // Round floats to 3 sig figs; leave ints alone.
      return Number.isInteger(v) ? String(v) : String(Math.round(v * 1000) / 1000);
    }
    if (typeof v !== "string") return String(v);

    // Round stringified floats coming from the TTL ("0.222222" -> "0.222").
    if (/^-?\d+\.\d{4,}$/.test(v)) {
      const n = parseFloat(v);
      if (!Number.isNaN(n)) return String(Math.round(n * 1000) / 1000);
    }

    // Strip Valve's ubiquitous `E<Kind>_` enum prefixes.
    //   EResourceType_None -> "None"
    //   ECitadelHeroType_Marksman -> "Marksman"
    const enumStrip = v.match(/^E[A-Z][A-Za-z0-9]*_(.+)$/);
    if (enumStrip) {
      const inner = enumStrip[1];
      // "SingleStat" -> "Single Stat"
      return inner.replace(/([a-z0-9])([A-Z])/g, "$1 $2");
    }

    if (k === "scaleFunction") {
      return v.replace(/^scale_function_/, "")
              .split("_")
              .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
              .join(" ");
    }
    if (k === "modifiesProperty") {
      // Preserve bare acronyms (DPS, HP); CamelCase split otherwise.
      if (/^[A-Z0-9]+$/.test(v) && v.length <= 5) return v;
      return v.replace(/([a-z0-9])([A-Z])/g, "$1 $2")
              .replace(/^./, (c) => c.toUpperCase());
    }
    return v;
  }

  // Predicate name -> human label. Unknown predicates fall back to a Camel
  // split with first letter capitalised.
  const PREDICATE_LABELS = {
    hasAbilityInSlot:     "Ability in slot",
    ability:              "Ability",
    slot:                 "Slot",
    hasProperty:          "Property",
    hasUpgrade:           "Upgrade",
    scalesStat:           "Scales with",
    primaryCategory:      "Primary category",
    secondaryCategory:    "Secondary category",
    providesModifierType: "Modifier type",
  };
  function prettifyPredicate(p) {
    if (PREDICATE_LABELS[p]) return PREDICATE_LABELS[p];
    return p.replace(/([a-z0-9])([A-Z])/g, "$1 $2")
            .replace(/^./, (c) => c.toUpperCase());
  }

  // RDF-internal classes. Players never need to filter by these; they're
  // revealed only in dev mode.
  const DEV_ONLY_CLASSES = new Set([
    "BlankNode", "Resource", "Stage", "ModifierValue",
  ]);
  // Predicates that are also dev-ish.
  const DEV_ONLY_PREDICATES = new Set([
    "wasDerivedFrom", "developerStage", "providesModifierType",
  ]);

  // Bucket a property key into an inspector section.
  //   "Core"    = vitals (health / move / stamina / regen)
  //   "Combat"  = melee damage, tech range/duration, reload, charges
  //   "Meta"    = tags, role strings, anything else that slipped through
  function classifyPropKey(k) {
    const core = /^starting(Max(Health|MoveSpeed)|HeavyMeleeDamage|LightMeleeDamage|BaseHealthRegen|Stamina(RegenPerSecond)?|SprintSpeed|ReloadSpeed|TechDuration|TechRange)$/;
    if (core.test(k)) {
      if (/MoveSpeed|SprintSpeed|HealthRegen|Max(Health|MoveSpeed)|Stamina/.test(k)) return "Core";
      return "Combat";
    }
    return "Meta";
  }

  // ---- Filters ----------------------------------------------------------------

  function applyClassFilter() {
    state.cy.nodes().forEach((n) => {
      const pc = primaryClass(n.data("classes"));
      n.toggleClass("hidden", !state.classFilter.has(pc));
    });
    applyEdgeFilter();
  }
  function applyEdgeFilter() {
    state.cy.edges().forEach((e) => {
      const pred = e.data("label");
      const predVisible = state.edgeFilter.has(pred);
      const endpointsVisible = !e.source().hasClass("hidden") && !e.target().hasClass("hidden");
      e.toggleClass("hidden", !(predVisible && endpointsVisible));
    });
  }

  // ---- Expand / collapse ------------------------------------------------------

  function applyExpansion() {
    const visible = new Set(state.expanded);
    visible.add(rootId());
    state.expanded.forEach((id) => {
      const node = state.cy.getElementById(id);
      node.connectedEdges().forEach((e) => {
        visible.add(e.source().id());
        visible.add(e.target().id());
      });
    });
    state.cy.nodes().forEach((n) => n.toggleClass("collapsed", !visible.has(n.id())));
    state.cy.edges().forEach((e) => {
      const both = visible.has(e.source().id()) && visible.has(e.target().id());
      e.toggleClass("collapsed", !both);
    });
  }
  function expandNode(id) { state.expanded.add(id); applyExpansion(); }
  function collapseNode(id) {
    if (id === rootId()) return;
    state.expanded.delete(id);
    applyExpansion();
  }
  function expandAll() {
    state.cy.nodes().forEach((n) => state.expanded.add(n.id()));
    applyExpansion();
  }
  function collapseToRoot() {
    state.expanded = new Set([rootId()]);
    applyExpansion();
  }
  function expandKit() {
    if (!state.kitSet) return;
    state.expanded = new Set(state.kitSet);
    applyExpansion();
  }

  // ---- Root resolution --------------------------------------------------------

  function rootShortId() {
    const h = state.bundle.heroes[state.currentHero];
    return `hero/${h.public_name}`;
  }
  function rootId() {
    return state.shortIdToId.get(rootShortId()) || state.graph.nodes[0].data.id;
  }

  // ---- Inspector --------------------------------------------------------------

  function showInspector(nodeId) {
    const n = state.nodesById.get(nodeId);
    if (!n) { hideInspector(); return; }

    document.getElementById("inspector-empty").hidden = true;
    document.getElementById("inspector").hidden = false;

    const tagsEl = document.getElementById("inspector-class-tags");
    tagsEl.innerHTML = "";
    (n.classes || "").split(/\s+/).filter(Boolean).forEach((c) => {
      const t = document.createElement("span");
      t.className = "class-tag";
      t.textContent = c;
      t.style.color = CLASS_COLORS[c] || "#8b949e";
      t.style.borderColor = CLASS_COLORS[c] || "#30363d";
      tagsEl.appendChild(t);
    });

    document.getElementById("inspector-label").textContent = n.label;

    const iriEl = document.getElementById("inspector-iri");
    iriEl.textContent = n.iri || n.id;
    document.getElementById("btn-copy-iri").onclick = () => {
      navigator.clipboard.writeText(iriEl.textContent).catch(() => {});
      toast("IRI copied");
    };

    // Grouped literal properties: Core / Combat / Tags / Other.
    const sectionIds = ["props-core", "props-combat", "props-tags", "props-meta"];
    sectionIds.forEach((id) => {
      const el = document.getElementById(id);
      el.hidden = true;
      const tbody = el.querySelector("tbody");
      if (tbody) tbody.innerHTML = "";
    });
    document.getElementById("props-tags-chips").innerHTML = "";

    const rawEntries = Object.entries(n.properties || {})
      .filter(([k]) => !HIDDEN_PROP_KEYS.has(k));
    const hasAny = rawEntries.length > 0;
    document.getElementById("props-empty-wrap").hidden = hasAny;
    document.getElementById("props-empty").hidden = hasAny;

    const buckets = { Core: [], Combat: [], Meta: [] };
    let tagValue = null;
    rawEntries.forEach(([k, v]) => {
      if (k === "heroTag") { tagValue = v; return; }
      buckets[classifyPropKey(k)].push([k, v]);
    });

    // Stable sort within bucket: Core in vitals order, Combat alpha, Meta alpha.
    const CORE_ORDER = [
      "startingMaxHealth", "startingBaseHealthRegen", "startingMaxMoveSpeed",
      "startingSprintSpeed", "startingStamina", "startingStaminaRegenPerSecond",
    ];
    buckets.Core.sort(([a], [b]) => {
      const ai = CORE_ORDER.indexOf(a), bi = CORE_ORDER.indexOf(b);
      if (ai === -1 && bi === -1) return a.localeCompare(b);
      if (ai === -1) return 1;
      if (bi === -1) return -1;
      return ai - bi;
    });
    buckets.Combat.sort(([a], [b]) => a.localeCompare(b));
    buckets.Meta.sort(([a], [b]) => a.localeCompare(b));

    function fillSection(sectionId, entries) {
      if (!entries.length) return;
      const el = document.getElementById(sectionId);
      el.hidden = false;
      const tbody = el.querySelector("tbody");
      entries.forEach(([k, v]) => {
        const tr = document.createElement("tr");
        const td1 = document.createElement("td"); td1.textContent = prettifyPropKey(k);
        const td2 = document.createElement("td");
        const pretty = Array.isArray(v)
          ? v.map((vv) => prettifyPropValue(k, vv)).join(", ")
          : prettifyPropValue(k, v);
        td2.textContent = pretty;
        tr.append(td1, td2);
        tbody.appendChild(tr);
      });
    }
    fillSection("props-core", buckets.Core);
    fillSection("props-combat", buckets.Combat);
    fillSection("props-meta", buckets.Meta);

    if (tagValue != null) {
      const tagEl = document.getElementById("props-tags");
      tagEl.hidden = false;
      const chips = document.getElementById("props-tags-chips");
      const raw = Array.isArray(tagValue) ? tagValue : String(tagValue).split(",");
      raw.map((s) => s.trim()).filter(Boolean).forEach((tag) => {
        const c = document.createElement("span");
        c.className = "tag-chip";
        c.textContent = tag;
        chips.appendChild(c);
      });
    }

    const cyNode = state.cy.getElementById(nodeId);
    const outgoingList = document.getElementById("inspector-outgoing");
    const incomingList = document.getElementById("inspector-incoming");
    outgoingList.innerHTML = "";
    incomingList.innerHTML = "";

    // Outgoing rows sorted by slot order for Hero nodes (Weapon -> Ab1..4),
    // by predicate name otherwise. Provenance-ish predicates are filtered.
    const outsVisible = cyNode.outgoers("edge")
      .filter((e) => !HIDDEN_PREDICATES.has(e.data("label")));
    const insVisible = cyNode.incomers("edge")
      .filter((e) => !HIDDEN_PREDICATES.has(e.data("label")));

    document.getElementById("outgoing-empty").hidden = outsVisible.length > 0;
    document.getElementById("incoming-empty").hidden = insVisible.length > 0;

    function outgoingSortKey(e) {
      // For Hero -> hasAbilityInSlot bnode edges, sort by the slot that bnode
      // binds to (Weapon first, then Ability 1..4, then utility alphabetical).
      if (e.data("label") === "hasAbilityInSlot") {
        const bnode = e.target();
        const slotEdge = bnode.outgoers("edge").filter((ee) => ee.data("label") === "slot")[0];
        if (slotEdge) {
          const slotShort = slotEdge.target().data("shortId") || "";
          const idx = SLOT_SORT_ORDER.indexOf(slotShort);
          return [0, idx === -1 ? 99 : idx, slotShort];
        }
      }
      return [1, 0, e.data("label")];
    }
    const outsSorted = outsVisible.toArray().sort((a, b) => {
      const ka = outgoingSortKey(a), kb = outgoingSortKey(b);
      for (let i = 0; i < ka.length; i++) {
        if (ka[i] < kb[i]) return -1;
        if (ka[i] > kb[i]) return 1;
      }
      return 0;
    });

    outsSorted.forEach((e) => {
      const target = e.target();
      const li = document.createElement("li");
      const predSpan = document.createElement("span");
      predSpan.className = "pred";
      predSpan.textContent = prettifyPredicate(e.data("label")) + " \u2192";
      const targetSpan = document.createElement("span");
      targetSpan.className = "target";
      targetSpan.textContent = target.data("label");
      targetSpan.addEventListener("click", () => selectNodeById(target.id(), { expand: true }));
      li.append(predSpan, targetSpan);
      outgoingList.appendChild(li);
    });
    insVisible.forEach((e) => {
      const source = e.source();
      const li = document.createElement("li");
      const predSpan = document.createElement("span");
      predSpan.className = "pred";
      predSpan.textContent = "\u2190 " + prettifyPredicate(e.data("label"));
      const srcSpan = document.createElement("span");
      srcSpan.className = "target";
      srcSpan.textContent = source.data("label");
      srcSpan.addEventListener("click", () => selectNodeById(source.id(), { expand: true }));
      li.append(srcSpan, predSpan);
      incomingList.appendChild(li);
    });
  }
  function hideInspector() {
    document.getElementById("inspector").hidden = true;
    document.getElementById("inspector-empty").hidden = false;
  }

  // ---- Selection + URL routing ------------------------------------------------

  function currentHash() {
    const h = state.bundle.heroes[state.currentHero];
    return `#hero/${encodeURIComponent(h.public_name)}`;
  }
  function setHash(suffix) {
    const next = suffix ? `${currentHash()}/${suffix}` : currentHash();
    if (window.location.hash !== next) history.replaceState(null, "", next);
  }

  function selectNodeById(id, { expand = false, center = true } = {}) {
    const node = state.cy.getElementById(id);
    if (!node || node.length === 0) return;

    state.cy.elements().unselect();
    node.select();

    if (expand) expandNode(id);
    showInspector(id);

    if (center) {
      state.cy.animate({
        center: { eles: node },
        zoom: Math.max(state.cy.zoom(), 1.0),
      }, { duration: 250 });
    }

    const short = node.data("shortId");
    if (short) {
      // Don't pollute the hash with the root hero node — "#hero/X" already
      // means "viewing X", a trailing "/node/hero/X" is redundant.
      if (short === rootShortId()) setHash("");
      else setHash(`node/${encodeURIComponent(short)}`);
    }
  }

  function parseHash() {
    // Supported forms:
    //   #hero/Infernus
    //   #hero/Infernus/node/ability/InfernusFireBomb
    //   #node/ability/InfernusFireBomb     (legacy, stays on current hero)
    const h = window.location.hash.replace(/^#/, "");
    if (!h) return {};
    const parts = h.split("/");
    const out = {};
    if (parts[0] === "hero" && parts.length >= 2) {
      out.hero = decodeURIComponent(parts[1]);
      if (parts[2] === "node" && parts.length >= 4) {
        out.node = decodeURIComponent(parts.slice(3).join("/"));
      }
    } else if (parts[0] === "node" && parts.length >= 2) {
      out.node = decodeURIComponent(parts.slice(1).join("/"));
    }
    return out;
  }

  function resolveHeroCodename(publicOrCode) {
    if (!publicOrCode) return null;
    if (state.bundle.heroes[publicOrCode]) return publicOrCode;
    for (const [code, h] of Object.entries(state.bundle.heroes)) {
      if (h.public_name.toLowerCase() === publicOrCode.toLowerCase()) return code;
    }
    return null;
  }

  function applyHash() {
    const parsed = parseHash();
    const targetHero = resolveHeroCodename(parsed.hero) || state.currentHero;
    if (targetHero !== state.currentHero) {
      switchHero(targetHero, { fromHash: true });
    }
    if (parsed.node) {
      const id = state.shortIdToId.get(parsed.node);
      if (id) selectNodeById(id, { expand: true });
    }
  }

  // ---- Filter UI --------------------------------------------------------------

  function buildClassFilters() {
    const container = document.getElementById("class-filters");
    container.innerHTML = "";
    state.classFilter = new Set();
    const counts = {};
    state.graph.nodes.forEach((n) => {
      const pc = primaryClass(n.data.classes);
      counts[pc] = (counts[pc] || 0) + 1;
    });
    const present = CLASS_ORDER.filter((c) => counts[c]);
    present.forEach((c) => state.classFilter.add(c));
    present.forEach((c) => {
      const chip = document.createElement("span");
      chip.className = "chip";
      if (DEV_ONLY_CLASSES.has(c)) chip.classList.add("dev-only");
      chip.innerHTML =
        `<span class="chip-swatch" style="background:${CLASS_COLORS[c]}"></span>` +
        `<span class="chip-label">${c}</span>` +
        `<span class="chip-count">${counts[c]}</span>`;
      chip.addEventListener("click", () => {
        if (state.classFilter.has(c)) {
          state.classFilter.delete(c);
          chip.classList.add("off");
        } else {
          state.classFilter.add(c);
          chip.classList.remove("off");
        }
        applyClassFilter();
      });
      container.appendChild(chip);
    });
  }

  function buildEdgeFilters() {
    const container = document.getElementById("edge-filters");
    container.innerHTML = "";
    state.edgeFilter = new Set();
    const counts = {};
    state.graph.edges.forEach((e) => {
      const p = e.data.label;
      counts[p] = (counts[p] || 0) + 1;
    });
    const preds = Object.keys(counts).sort((a, b) => counts[b] - counts[a]);
    preds.forEach((p) => state.edgeFilter.add(p));
    preds.forEach((p) => {
      const chip = document.createElement("span");
      chip.className = "chip";
      if (DEV_ONLY_PREDICATES.has(p)) chip.classList.add("dev-only");
      chip.innerHTML =
        `<span class="chip-label">${prettifyPredicate(p)}</span>` +
        `<span class="chip-count">${counts[p]}</span>`;
      chip.addEventListener("click", () => {
        if (state.edgeFilter.has(p)) {
          state.edgeFilter.delete(p);
          chip.classList.add("off");
        } else {
          state.edgeFilter.add(p);
          chip.classList.remove("off");
        }
        applyEdgeFilter();
      });
      container.appendChild(chip);
    });
  }

  function buildNodeList() {
    const listEl = document.getElementById("node-list");
    const inputEl = document.getElementById("node-search");

    // Scope-by-parent: for blank-node ability properties / upgrades, many labels
    // are generic ("Cooldown", "Damage"). Find the parent Ability node and
    // prepend its label, so "Afterburn › Cooldown" disambiguates four Cooldowns.
    const nodeById = new Map(state.graph.nodes.map((n) => [n.data.id, n.data]));
    const parentAbilityLabel = (nid) => {
      // A blank-node ability property/upgrade has exactly one incoming
      // hasProperty or hasUpgrade edge from an ability.
      for (const e of state.graph.edges) {
        if (e.data.target === nid && (e.data.label === "hasProperty" || e.data.label === "hasUpgrade")) {
          const parent = nodeById.get(e.data.source);
          if (parent) return parent.label;
        }
      }
      return null;
    };

    const entries = state.graph.nodes
      .map((n) => {
        const cls = primaryClass(n.data.classes);
        let label = n.data.label;
        // Scope generic blank-node labels by their parent ability.
        if (cls === "AbilityProperty" || cls === "AbilityUpgrade") {
          const parent = parentAbilityLabel(n.data.id);
          if (parent) label = `${parent} \u203A ${n.data.label}`;
        }
        return {
          id: n.data.id,
          label,
          cls,
          devOnly: DEV_ONLY_CLASSES.has(cls),
        };
      })
      .sort((a, b) => {
        const ao = CLASS_ORDER.indexOf(a.cls);
        const bo = CLASS_ORDER.indexOf(b.cls);
        if (ao !== bo) return ao - bo;
        return a.label.localeCompare(b.label);
      });
    function render(filter) {
      listEl.innerHTML = "";
      const ql = (filter || "").toLowerCase();
      for (const e of entries) {
        if (ql && !e.label.toLowerCase().includes(ql) && !e.cls.toLowerCase().includes(ql)) continue;
        const li = document.createElement("li");
        if (e.devOnly) li.classList.add("dev-only");
        li.innerHTML =
          `<span class="swatch" style="background:${CLASS_COLORS[e.cls] || "#888"}"></span>` +
          `<span class="node-label" title="${e.cls} \u2014 ${e.label}">${e.label}</span>`;
        li.addEventListener("click", () => selectNodeById(e.id, { expand: true }));
        listEl.appendChild(li);
      }
    }
    inputEl.oninput = () => render(inputEl.value);
    inputEl.value = "";
    render("");
  }

  // ---- Hero picker + switching ------------------------------------------------

  function buildHeroPicker() {
    const sel = document.getElementById("hero-picker");
    sel.innerHTML = "";
    state.bundle.order.forEach((code) => {
      const h = state.bundle.heroes[code];
      const opt = document.createElement("option");
      opt.value = code;
      opt.textContent = h.public_name;
      sel.appendChild(opt);
    });
    sel.value = state.currentHero;
    sel.onchange = () => switchHero(sel.value);
  }

  function switchHero(codename, { fromHash = false } = {}) {
    if (!state.bundle.heroes[codename]) return;
    state.currentHero = codename;
    state.graph = state.bundle.heroes[codename];

    if (state.cy) state.cy.destroy();

    state.nodesById = new Map();
    state.shortIdToId = new Map();
    state.graph.nodes.forEach((n) => {
      state.nodesById.set(n.data.id, n.data);
      if (n.data.shortId) state.shortIdToId.set(n.data.shortId, n.data.id);
    });

    state.cy = makeCy([...state.graph.nodes, ...state.graph.edges]);
    registerCyEvents();

    buildClassFilters();
    buildEdgeFilters();
    buildNodeList();

    state.kitSet = computeKitSet(state.graph);
    state.expanded = new Set([rootId()]);
    if (state.kitMode) state.kitSet.forEach((id) => state.expanded.add(id));
    applyKitMode();
    applyExpansion();

    document.getElementById("meta-summary").innerHTML =
      `${state.graph.public_name} &middot; ${state.graph.meta.node_count} nodes &middot; ${state.graph.meta.edge_count} edges`;

    const sel = document.getElementById("hero-picker");
    if (sel.value !== codename) sel.value = codename;

    state.cy.layout({
      name: "fcose", animate: false, randomize: true,
      nodeSeparation: 100, idealEdgeLength: 90,
      nodeRepulsion: 8000, gravity: 0.2, numIter: 2000, padding: 40,
    }).run();

    if (!fromHash) setHash("");
    selectNodeById(rootId(), { expand: true });
  }

  // ---- Cy events --------------------------------------------------------------

  function registerCyEvents() {
    state.cy.on("tap", "node", (evt) => {
      selectNodeById(evt.target.id(), { expand: true, center: false });
    });
    state.cy.on("dbltap", "node", (evt) => {
      collapseNode(evt.target.id());
    });
    state.cy.on("tap", (evt) => {
      if (evt.target === state.cy) hideInspector();
    });
    state.cy.on("mouseover", "edge", (evt) => evt.target.addClass("highlighted"));
    state.cy.on("mouseout",  "edge", (evt) => evt.target.removeClass("highlighted"));
  }

  // ---- Toast + onboarding -----------------------------------------------------

  let toastEl = null;
  let toastTimer = null;
  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement("div");
      toastEl.className = "toast";
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove("show"), 1600);
  }

  function maybeShowOnboarding() {
    const overlay = document.getElementById("onboarding");
    const card = overlay?.querySelector(".onboarding-card");
    try {
      if (!localStorage.getItem("nydus.onboarded")) {
        overlay.hidden = false;
      }
    } catch (_) {}
    const dismiss = () => {
      overlay.hidden = true;
      try { localStorage.setItem("nydus.onboarded", "1"); } catch (_) {}
    };
    document.getElementById("btn-onboarding-close").onclick = dismiss;
    // Click backdrop (outside the card) dismisses
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) dismiss();
    });
    // ESC dismisses
    document.addEventListener("keydown", (e) => {
      if (!overlay.hidden && e.key === "Escape") dismiss();
    });
  }

  // ---- Init -------------------------------------------------------------------

  async function init() {
    try {
      if (typeof cytoscape !== "function") {
        throw new Error("Cytoscape did not load — check lib/cytoscape.min.js");
      }

      state.bundle = await load();

      const parsed = parseHash();
      const fromHash = resolveHeroCodename(parsed.hero);
      state.currentHero = fromHash || (state.bundle.heroes[DEFAULT_HERO] ? DEFAULT_HERO : state.bundle.order[0]);

      buildHeroPicker();
      switchHero(state.currentHero, { fromHash: !!fromHash });

      if (parsed.node) {
        const id = state.shortIdToId.get(parsed.node);
        if (id) selectNodeById(id, { expand: true });
      }

      window.addEventListener("hashchange", applyHash);

      document.getElementById("btn-reset").addEventListener("click", () => {
        state.cy.layout({
          name: "fcose", animate: true, animationDuration: 500,
          randomize: false, idealEdgeLength: 90, nodeRepulsion: 8000,
        }).run();
        state.cy.fit(null, 40);
      });
      document.getElementById("btn-expand-all").addEventListener("click", expandAll);
      document.getElementById("btn-collapse-all").addEventListener("click", collapseToRoot);
      document.getElementById("btn-kit-mode").addEventListener("click", () => {
        state.kitMode = !state.kitMode;
        if (state.kitMode) expandKit();
        applyKitMode();
        state.cy.layout({
          name: "fcose", animate: true, animationDuration: 400,
          randomize: false, idealEdgeLength: 90, nodeRepulsion: 8000,
        }).run();
        state.cy.fit(null, 40);
      });
      document.getElementById("btn-dev-mode").addEventListener("click", () => {
        document.body.classList.toggle("dev-mode");
        const on = document.body.classList.contains("dev-mode");
        document.getElementById("btn-dev-mode").classList.toggle("active", on);
      });
      document.getElementById("btn-share").addEventListener("click", () => {
        const url = window.location.href;
        navigator.clipboard.writeText(url).then(() => toast("Link copied")).catch(() => toast(url));
      });

    } catch (err) {
      console.error(err);
      const g = document.getElementById("graph");
      g.innerHTML = `<div style="padding:20px;color:#e05c5c">
        <h3>Failed to load graph</h3>
        <pre>${err.message}</pre>
        <p>If opened via <code>file://</code>, your browser may be blocking <code>fetch(graphs.json)</code>.
        Serve the folder: <code>python3 -m http.server</code> in <code>outputs/viewer</code>.</p>
      </div>`;
    }
  }

  init();
})();
