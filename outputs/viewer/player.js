// Nydus — Player profile.
//
// URL: player.html?id=<steam_id>  (SteamID64 or SteamID3)
//
// Borrowed shapes that work:
//   - op.gg / DOTABUFF: rank badge + lifetime totals + hero-affinity grid +
//     recent matches list. Standard MOBA profile shape; nobody needs to
//     learn it.
//   - Spotify Wrapped: a single "playstyle archetype" headline derived from
//     the data, treated as the showpiece. "Spirit Burst Caster", "Sustained
//     Weapon Carry", "Crowd-Control Anchor". One sentence summarises a
//     1000-hour profile.
//   - Stratz / poe.ninja: insight bullets and 5-axis preference bars
//     comparing the player's pool to the roster baseline.
//
// What's unique to Nydus (the graph utility):
//   The archetype tag, the insight bullets, and the preference bars are all
//   derived by aggregating canonical prop:* and sf:* IRIs across the
//   player's hero pool, weighted by playtime. Same vocabulary the heroes
//   speak; same vocabulary the player is described in.
//
// No Cytoscape canvas — graphs literally transcribed are noise. The graph
// stays in the data layer, surfaces as language.

(() => {
  const STEAMID64_BASE = 76561197960265728n;
  const API_BASE       = "https://api.deadlock-api.com/v1";

  const SIG_SLOT_SHORT_IDS = new Set([
    "slot/WeaponPrimary",
    "slot/Signature1", "slot/Signature2", "slot/Signature3", "slot/Signature4",
  ]);

  const PROP_LABEL = {
    "prop/Cooldown":     "Cooldown",
    "prop/Damage":       "Damage",
    "prop/Duration":     "Duration",
    "prop/CastRange":    "Cast Range",
    "prop/Charges":      "Charges",
    "prop/Radius":       "Radius",
    "prop/DPS":          "DPS",
    "prop/SlowPercent":  "Slow",
    "prop/SlowDuration": "Slow Duration",
    "prop/StunDuration": "Stun Duration",
    "prop/HealAmount":   "Healing",
    "prop/MaxStacks":    "Stacks",
    "prop/MoveSpeed":    "Move Speed",
  };
  const SF_LABEL = {
    "sf/SpiritPower":    "Spirit Power",
    "sf/WeaponDamage":   "Weapon Damage",
    "sf/SpiritDuration": "Spirit Duration",
    "sf/SpiritRange":    "Spirit Range",
    "sf/AbilityCharges": "Ability Charges",
    "sf/Self":           "self-scaling",
    "sf/MultipleStats":  "multi-stat",
  };

  const HERO_ACCENT = {
    hero_inferno:    "#e8743a", hero_atlas:      "#c65a3f",
    hero_astro:      "#d9b15a", hero_bebop:      "#b88647",
    hero_bookworm:   "#6e8cb8", hero_chrono:     "#8f6fc4",
    hero_doorman:    "#8a9bb0", hero_drifter:    "#5a6f8f",
    hero_dynamo:     "#7fb8d6", hero_familiar:   "#9b6dff",
    hero_fencer:     "#d9b15a", hero_forge:      "#e05c5c",
    hero_frank:      "#a5784a", hero_ghost:      "#8fb8c4",
    hero_gigawatt:   "#f5a623", hero_haze:       "#a35fb5",
    hero_hornet:     "#e0a84a", hero_kelvin:     "#8fd4e6",
    hero_krill:      "#c4704a", hero_lash:       "#c44a4a",
    hero_magician:   "#8f6fc4", hero_mirage:     "#d9b15a",
    hero_nano:       "#7fc48a", hero_necro:      "#6fa3c4",
    hero_orion:      "#d9a04a", hero_priest:     "#e6d8a8",
    hero_punkgoat:   "#c0657a", hero_shiv:       "#e05c5c",
    hero_synth:      "#f5a623", hero_tengu:      "#c65a3f",
    hero_unicorn:    "#e8a3d2", hero_vampirebat: "#8a4a4a",
    hero_viper:      "#7fc48a", hero_viscous:    "#8fd4a8",
    hero_warden:     "#6e8cb8", hero_werewolf:   "#a3784a",
    hero_wraith:     "#c4a3e8", hero_yamato:     "#c44a4a",
  };
  const DEFAULT_ACCENT = "#e8743a";

  const DIVISION_NAMES = [
    null, "Obscurus", "Initiate", "Seeker", "Alchemist", "Arcanist",
    "Ritualist", "Emissary", "Archon", "Oracle", "Phantom", "Ascendant", "Eternus",
  ];

  function steamIdToAccountId(s) {
    const trimmed = String(s).trim();
    if (!/^\d+$/.test(trimmed)) return null;
    const big = BigInt(trimmed);
    if (big < STEAMID64_BASE) return Number(big);
    return Number(big - STEAMID64_BASE);
  }

  // ---- Bundle indexing -------------------------------------------------------

  function summariseHeroKit(hero) {
    const nodeById = new Map(hero.nodes.map((n) => [n.data.id, n.data]));
    const outgoing = new Map();
    hero.edges.forEach((e) => {
      const s = e.data.source, t = e.data.target, p = e.data.label;
      if (!outgoing.has(s)) outgoing.set(s, []);
      outgoing.get(s).push([t, p]);
    });
    const heroNode = hero.nodes.find((n) =>
      (n.data.classes || "").split(/\s+/).includes("Hero"));
    if (!heroNode) return { propTypes: [], scaleFns: [] };

    const sigAbilityIds = [];
    (outgoing.get(heroNode.data.id) || []).forEach(([bn, pred]) => {
      if (pred !== "hasAbilityInSlot") return;
      const bnOuts = outgoing.get(bn) || [];
      const slotEdge = bnOuts.find(([, p]) => p === "slot");
      const abEdge   = bnOuts.find(([, p]) => p === "ability");
      if (!slotEdge || !abEdge) return;
      const slotShort = nodeById.get(slotEdge[0])?.shortId || "";
      if (!SIG_SLOT_SHORT_IDS.has(slotShort)) return;
      sigAbilityIds.push(abEdge[0]);
    });

    const propTypes = [];
    const scaleFns = [];
    sigAbilityIds.forEach((aid) => {
      (outgoing.get(aid) || []).forEach(([t, pred]) => {
        if (pred !== "hasProperty") return;
        (outgoing.get(t) || []).forEach(([t2, p2]) => {
          if (p2 === "propertyType") {
            const sid = nodeById.get(t2)?.shortId;
            if (sid) propTypes.push(sid);
          } else if (p2 === "scaleFunction") {
            const sid = nodeById.get(t2)?.shortId;
            if (sid) scaleFns.push(sid);
          }
        });
      });
    });
    return { propTypes, scaleFns };
  }

  function buildBundleIndex(bundle) {
    const byId = new Map();
    Object.values(bundle.heroes).forEach((hero) => {
      byId.set(hero.hero_id, {
        codename:   hero.codename,
        publicName: hero.public_name,
        ...summariseHeroKit(hero),
      });
    });
    return byId;
  }

  // ---- Aggregation -----------------------------------------------------------

  function aggregateProfile(heroStats, heroIndex) {
    const propWeight = new Map();
    const sfWeight   = new Map();
    let totalTime    = 0;
    let totalMatches = 0;
    let totalWins    = 0;
    const playedHeroes = [];

    heroStats.forEach((s) => {
      const k = heroIndex.get(s.hero_id);
      if (!k) return;
      const w = s.time_played || 0;
      if (w === 0) return;
      totalTime    += w;
      totalMatches += s.matches_played || 0;
      totalWins    += s.wins || 0;
      playedHeroes.push({
        codename:   k.codename,
        publicName: k.publicName,
        hero_id:    s.hero_id,
        time:       w,
        matches:    s.matches_played || 0,
        wins:       s.wins || 0,
        kpm:        s.kills_per_min  || 0,
        dpm:        s.deaths_per_min || 0,
        apm:        s.assists_per_min || 0,
        accuracy:   s.accuracy || 0,
      });

      // Multiset count of prop/sf occurrences in the hero's kit, weighted
      // by playtime. A property that appears 3x in the kit gets 3x weight.
      const propCount = new Map();
      k.propTypes.forEach((p) => propCount.set(p, (propCount.get(p) || 0) + 1));
      const sfCount = new Map();
      k.scaleFns.forEach((f) => sfCount.set(f, (sfCount.get(f) || 0) + 1));

      propCount.forEach((c, p) => propWeight.set(p, (propWeight.get(p) || 0) + w * c));
      sfCount  .forEach((c, f) => sfWeight  .set(f, (sfWeight  .get(f) || 0) + w * c));
    });

    return { propWeight, sfWeight, totalTime, totalMatches, totalWins, playedHeroes };
  }

  // ---- Roster baseline (the "average hero" so the player's pool can be
  //      compared against the corpus, not just shown in absolute terms). -----

  function rosterBaseline(heroIndex) {
    const propWeight = new Map();
    const sfWeight   = new Map();
    [...heroIndex.values()].forEach((k) => {
      k.propTypes.forEach((p) => propWeight.set(p, (propWeight.get(p) || 0) + 1));
      k.scaleFns.forEach((f) => sfWeight.set(f, (sfWeight.get(f) || 0) + 1));
    });
    return { propWeight, sfWeight };
  }

  function normalise(weightMap) {
    const total = [...weightMap.values()].reduce((a, b) => a + b, 0) || 1;
    const out = new Map();
    weightMap.forEach((v, k) => out.set(k, v / total));
    return out;
  }

  // ---- Archetype synthesis ---------------------------------------------------
  //
  // Inspect the dominant prop:* and sf:* IRIs and return a single short
  // headline that captures the player's lean. Heuristic — no ML, just the
  // canonical vocabulary read out as English.
  function deriveArchetype(profile) {
    const propPct = normalise(profile.propWeight);
    const sfPct   = normalise(profile.sfWeight);

    const get = (m, k) => m.get(k) || 0;
    const spiritShare = get(sfPct, "sf/SpiritPower") + get(sfPct, "sf/SpiritDuration") + get(sfPct, "sf/SpiritRange");
    const weaponShare = get(sfPct, "sf/WeaponDamage");
    const cdShare     = get(propPct, "prop/Cooldown");
    const durShare    = get(propPct, "prop/Duration");
    const dmgShare    = get(propPct, "prop/Damage") + get(propPct, "prop/DPS");
    const ccShare     = get(propPct, "prop/SlowPercent") + get(propPct, "prop/SlowDuration") + get(propPct, "prop/StunDuration");
    const healShare   = get(propPct, "prop/HealAmount");
    const rangeShare  = get(propPct, "prop/CastRange") + get(propPct, "prop/Radius");

    // Discipline axis: Spirit / Weapon / Hybrid
    let discipline;
    if (spiritShare > weaponShare * 2)      discipline = "Spirit";
    else if (weaponShare > spiritShare * 2) discipline = "Weapon";
    else                                    discipline = "Hybrid";

    // Tempo axis: Burst (lots of damage, short duration), Sustained (long
    // duration), Crowd-Control (slows / stuns), Support (healing).
    let tempo;
    if (healShare > 0.10)                                 tempo = "Support";
    else if (ccShare > 0.10)                              tempo = "Crowd-Control";
    else if (durShare > dmgShare && durShare > 0.18)      tempo = "Sustained";
    else                                                  tempo = "Burst";

    // Range axis: zoner if heavy on cast range / radius
    const reach = rangeShare > 0.18 ? "Reach " : "";

    return `${reach}${discipline} ${tempo}`;
  }

  // ---- Insight bullets (derived prose, the actual graph utility) ------------

  function deriveInsights(profile, baseline) {
    const propPct = normalise(profile.propWeight);
    const sfPct   = normalise(profile.sfWeight);
    const basePropPct = normalise(baseline.propWeight);
    const baseSfPct   = normalise(baseline.sfWeight);

    const overIndex = (player, base) => {
      const out = [];
      player.forEach((p, k) => {
        const b = base.get(k) || 0.0001;
        const ratio = p / b;
        if (p > 0.04 && ratio > 1.25) out.push({ key: k, ratio, share: p });
      });
      return out.sort((a, b) => b.ratio - a.ratio);
    };
    const propOver = overIndex(propPct, basePropPct);
    const sfOver   = overIndex(sfPct,   baseSfPct);

    const insights = [];

    // Top scaling lean
    const sortedSf = [...sfPct.entries()].filter(([k]) => k !== "sf/Self").sort(([, a], [, b]) => b - a);
    if (sortedSf.length) {
      const [k, p] = sortedSf[0];
      const lbl = SF_LABEL[k] || k.split("/").pop();
      insights.push(`<b>${(p * 100).toFixed(0)}%</b> of your hero pool's scaling is on <b>${lbl}</b>.`);
    }

    // Property over-indexing
    if (propOver.length) {
      const top = propOver[0];
      const lbl = PROP_LABEL[top.key] || top.key.split("/").pop();
      insights.push(`You touch <b>${lbl}</b> properties <b>${top.ratio.toFixed(1)}×</b> as often as the average roster pick.`);
    }
    if (propOver.length > 1) {
      const second = propOver[1];
      const lbl = PROP_LABEL[second.key] || second.key.split("/").pop();
      insights.push(`Also over-indexed: <b>${lbl}</b> at <b>${second.ratio.toFixed(1)}×</b> baseline.`);
    }

    // Hero-pool concentration
    const sorted = [...profile.playedHeroes].sort((a, b) => b.time - a.time);
    if (sorted.length) {
      const top = sorted[0];
      const topShare = top.time / profile.totalTime;
      insights.push(`<b>${top.publicName}</b> alone is <b>${(topShare * 100).toFixed(0)}%</b> of your time on the roster.`);
    }
    if (sorted.length >= 5) {
      const top5 = sorted.slice(0, 5).reduce((a, h) => a + h.time, 0);
      const top5pct = top5 / profile.totalTime;
      insights.push(`Your top 5 heroes account for <b>${(top5pct * 100).toFixed(0)}%</b> of all playtime &mdash; ${sorted.length} unique heroes total.`);
    }

    return insights;
  }

  // ---- Render ---------------------------------------------------------------

  function renderHeader({ accountId, mmrLatest, profile, archetype }) {
    document.getElementById("p-account-id").textContent = `account ${accountId}`;
    const div = mmrLatest?.division;
    const tier = mmrLatest?.division_tier;
    const rank = (div != null && DIVISION_NAMES[div])
      ? `${DIVISION_NAMES[div]} ${tier ?? ""}`.trim()
      : "Unranked";
    document.getElementById("p-rank").textContent = rank;
    document.getElementById("p-archetype").textContent = archetype;
    document.getElementById("p-matches").textContent = profile.totalMatches.toLocaleString();
    const hours = Math.round(profile.totalTime / 3600);
    document.getElementById("p-hours").textContent = `${hours.toLocaleString()} h`;
    const wr = profile.totalMatches
      ? Math.round((100 * profile.totalWins) / profile.totalMatches)
      : 0;
    document.getElementById("p-winrate").textContent = `${wr}%`;
  }

  function renderInsights(insights) {
    const ul = document.getElementById("p-insights");
    ul.innerHTML = "";
    if (!insights.length) {
      ul.innerHTML = `<li class="p-empty">Not enough match data for insights yet.</li>`;
      return;
    }
    insights.forEach((s) => {
      const li = document.createElement("li");
      li.innerHTML = s;
      ul.appendChild(li);
    });
  }

  function renderHeroAffinity(profile) {
    const grid = document.getElementById("p-hero-grid");
    grid.innerHTML = "";
    [...profile.playedHeroes]
      .sort((a, b) => b.time - a.time)
      .slice(0, 8)
      .forEach((h) => {
        const wr = h.matches ? Math.round((100 * h.wins) / h.matches) : 0;
        const hours = (h.time / 3600).toFixed(1);
        const kda = ((h.kpm + h.apm) / Math.max(0.01, h.dpm)).toFixed(2);
        const accent = HERO_ACCENT[h.codename] || DEFAULT_ACCENT;
        const card = document.createElement("div");
        card.className = "p-hero-card";
        card.style.borderTopColor = accent;
        card.innerHTML = `
          <div class="p-hero-name">${h.publicName}</div>
          <div class="p-hero-grid">
            <span class="k">Hours</span>     <span class="v">${hours}</span>
            <span class="k">Matches</span>   <span class="v">${h.matches}</span>
            <span class="k">Win rate</span>  <span class="v">${wr}%</span>
            <span class="k">KDA / min</span> <span class="v">${kda}</span>
          </div>
        `;
        grid.appendChild(card);
      });
  }

  function renderComparisonBars(targetId, profileMap, baselineMap, labelMap, n) {
    const el = document.getElementById(targetId);
    el.innerHTML = "";
    const profilePct = normalise(profileMap);
    const basePct    = normalise(baselineMap);

    // Sort by player share descending; show top n.
    const rows = [...profilePct.entries()]
      .filter(([k]) => k !== "sf/Self")
      .map(([k, p]) => ({ key: k, label: labelMap[k] || k.split("/").pop(),
                          you: p, baseline: basePct.get(k) || 0 }))
      .sort((a, b) => b.you - a.you)
      .slice(0, n);

    const max = Math.max(...rows.map((r) => Math.max(r.you, r.baseline)), 0.001);
    rows.forEach((r) => {
      const youW   = (100 * r.you) / max;
      const baseW  = (100 * r.baseline) / max;
      const ratio  = r.baseline > 0 ? r.you / r.baseline : null;
      const tag    = ratio ? (ratio >= 1.15 ? `<span class="p-over">+${((ratio-1)*100).toFixed(0)}%</span>`
                            : ratio <= 0.85 ? `<span class="p-under">${((ratio-1)*100).toFixed(0)}%</span>`
                            : "") : "";
      const row = document.createElement("div");
      row.className = "p-bar-row";
      row.innerHTML = `
        <span class="p-bar-label">${r.label} ${tag}</span>
        <span class="p-bar-track">
          <span class="p-bar-baseline" style="width:${baseW.toFixed(1)}%"></span>
          <span class="p-bar-you"      style="width:${youW.toFixed(1)}%"></span>
        </span>
        <span class="p-bar-pct">${(r.you * 100).toFixed(1)}%</span>
      `;
      el.appendChild(row);
    });
  }

  function renderRecentMatches(matches, heroIndex) {
    const ul = document.getElementById("p-matches-list");
    ul.innerHTML = "";
    matches.slice(0, 10).forEach((m) => {
      const k = heroIndex.get(m.hero_id);
      const li = document.createElement("li");
      li.className = "p-match-row " + (m.match_result === 1 ? "p-win" : "p-loss");
      const dur  = `${Math.round((m.match_duration_s || 0) / 60)}m`;
      const date = new Date((m.start_time || 0) * 1000).toISOString().slice(0, 10);
      const accent = HERO_ACCENT[k?.codename] || DEFAULT_ACCENT;
      li.innerHTML = `
        <span class="p-match-result">${m.match_result === 1 ? "W" : "L"}</span>
        <span class="p-match-hero" style="border-left-color:${accent}">${k ? k.publicName : `Hero ${m.hero_id}`}</span>
        <span class="p-match-kda">${m.player_kills}/${m.player_deaths}/${m.player_assists}</span>
        <span class="p-match-dur">${dur}</span>
        <span class="p-match-date">${date}</span>
      `;
      ul.appendChild(li);
    });
  }

  function showError(msg) {
    document.getElementById("p-loading").hidden = true;
    document.getElementById("p-content").hidden = true;
    const el = document.getElementById("p-error");
    el.textContent = msg;
    el.hidden = false;
  }

  // ---- Init ------------------------------------------------------------------

  async function init() {
    const params = new URLSearchParams(window.location.search);
    const idRaw = params.get("id");
    if (!idRaw) {
      document.getElementById("p-loading").hidden = true;
      document.getElementById("p-instructions").hidden = false;
      return;
    }
    const accountId = steamIdToAccountId(idRaw);
    if (accountId == null) {
      showError(`That doesn't look like a Steam ID. Got "${idRaw}".`);
      return;
    }
    document.getElementById("p-id-display").textContent = idRaw;

    let bundle;
    try {
      bundle = window.__NYDUS_BUNDLE__ || await (await fetch("graphs.json")).json();
    } catch (e) {
      showError(`Couldn't load the Nydus ontology bundle: ${e.message}`);
      return;
    }
    const heroIndex = buildBundleIndex(bundle);
    const baseline  = rosterBaseline(heroIndex);

    let heroStats, mmr, matches;
    try {
      const [hsRes, mmrRes, mhRes] = await Promise.all([
        fetch(`${API_BASE}/players/${accountId}/hero-stats`),
        fetch(`${API_BASE}/players/${accountId}/mmr-history?limit=1`),
        fetch(`${API_BASE}/players/${accountId}/match-history?limit=10`),
      ]);
      if (!hsRes.ok)  throw new Error(`hero-stats ${hsRes.status}`);
      if (!mmrRes.ok) throw new Error(`mmr ${mmrRes.status}`);
      if (!mhRes.ok)  throw new Error(`match-history ${mhRes.status}`);
      heroStats = await hsRes.json();
      mmr       = await mmrRes.json();
      matches   = await mhRes.json();
    } catch (e) {
      showError(`Couldn't fetch from data.deadlock-api.com: ${e.message}. ` +
                `Is the Steam profile public, and has this player played Deadlock?`);
      return;
    }
    if (!heroStats || heroStats.length === 0) {
      showError(`No Deadlock match data for account ${accountId}.`);
      return;
    }

    const profile   = aggregateProfile(heroStats, heroIndex);
    const archetype = deriveArchetype(profile);
    const insights  = deriveInsights(profile, baseline);

    document.getElementById("p-loading").hidden = true;
    document.getElementById("p-content").hidden = false;

    renderHeader({ accountId, mmrLatest: mmr?.[0], profile, archetype });
    renderInsights(insights);
    renderHeroAffinity(profile);
    renderComparisonBars("p-prop-bars", profile.propWeight, baseline.propWeight, PROP_LABEL, 8);
    renderComparisonBars("p-sf-bars",   profile.sfWeight,   baseline.sfWeight,   SF_LABEL,   5);
    renderRecentMatches(matches, heroIndex);
  }

  init();
})();
