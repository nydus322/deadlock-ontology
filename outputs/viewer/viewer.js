// Nydus Deadlock graph viewer.
// Multi-hero: loads graphs.json, hero picker + URL routing, inspector, filters.
// URL hash forms:
//   #hero/Infernus
//   #hero/Infernus/node/ability/InfernusFireBomb
//   (legacy) #node/ability/InfernusFireBomb  -> falls back to current hero

(() => {
  const DEFAULT_HERO = "hero_inferno";

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

    const tbody = document.querySelector("#inspector-props tbody");
    tbody.innerHTML = "";
    const entries = Object.entries(n.properties || {});
    document.getElementById("props-empty").hidden = entries.length > 0;
    entries.sort(([a], [b]) => a.localeCompare(b)).forEach(([k, v]) => {
      const tr = document.createElement("tr");
      const td1 = document.createElement("td"); td1.textContent = k;
      const td2 = document.createElement("td");
      td2.textContent = Array.isArray(v) ? v.join(", ") : String(v);
      tr.append(td1, td2);
      tbody.appendChild(tr);
    });

    const cyNode = state.cy.getElementById(nodeId);
    const outgoingList = document.getElementById("inspector-outgoing");
    const incomingList = document.getElementById("inspector-incoming");
    outgoingList.innerHTML = "";
    incomingList.innerHTML = "";

    const outs = cyNode.outgoers("edge");
    const ins  = cyNode.incomers("edge");
    document.getElementById("outgoing-empty").hidden = outs.length > 0;
    document.getElementById("incoming-empty").hidden = ins.length > 0;

    outs.forEach((e) => {
      const target = e.target();
      const li = document.createElement("li");
      const predSpan = document.createElement("span");
      predSpan.className = "pred";
      predSpan.textContent = e.data("label") + " \u2192";
      const targetSpan = document.createElement("span");
      targetSpan.className = "target";
      targetSpan.textContent = target.data("label");
      targetSpan.addEventListener("click", () => selectNodeById(target.id(), { expand: true }));
      li.append(predSpan, targetSpan);
      outgoingList.appendChild(li);
    });
    ins.forEach((e) => {
      const source = e.source();
      const li = document.createElement("li");
      const predSpan = document.createElement("span");
      predSpan.className = "pred";
      predSpan.textContent = "\u2190 " + e.data("label");
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
      chip.innerHTML =
        `<span class="chip-label">${p}</span>` +
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
    const entries = state.graph.nodes
      .map((n) => ({
        id: n.data.id,
        label: n.data.label,
        cls: primaryClass(n.data.classes),
      }))
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

    state.expanded = new Set([rootId()]);
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
