// Port of extractKitData() from nydus.html line 12048.
// Pure Dart — no Flutter dependencies.

import '../models/bundle_data.dart';
import '../models/graph_elements.dart';
import '../models/kit_data.dart';
import 'prop_formatter.dart';

class KitExtractor {
  static const _signatureSlotShortIds = <String>{
    'slot/Signature1',
    'slot/Signature2',
    'slot/Signature3',
    'slot/Signature4',
    'slot/WeaponPrimary',
  };

  static const _slotSortOrder = [
    'slot/WeaponPrimary',
    'slot/Signature1',
    'slot/Signature2',
    'slot/Signature3',
    'slot/Signature4',
  ];

  static const _slotDisplayNames = <String, String>{
    'slot/WeaponPrimary': 'Primary Weapon',
    'slot/Signature1':    'Ability 1',
    'slot/Signature2':    'Ability 2',
    'slot/Signature3':    'Ability 3',
    'slot/Signature4':    'Ultimate',
  };

  static const _statPriority = [
    'Cooldown', 'Damage', 'DPS', 'Duration', 'Cast Range', 'Radius',
    'Charges', 'Stun Duration', 'Slow Percent', 'Slow Duration',
    'Burn Damage', 'Burn Duration',
  ];

  static KitData? extract(HeroGraph graph) {
    final nodeById = <String, NodeData>{
      for (final n in graph.nodes) n.data.id: n.data,
    };

    // Build outgoing adjacency: source -> [(target, predicate)]
    final outgoing = <String, List<(String, String)>>{};
    for (final e in graph.edges) {
      outgoing.putIfAbsent(e.data.source, () => []);
      outgoing[e.data.source]!.add((e.data.target, e.data.label));
    }

    final heroNode = graph.nodes
        .where((n) => n.data.classList.contains('Hero'))
        .firstOrNull;
    if (heroNode == null) return null;
    final heroData = heroNode.data;

    // Bucket hero stats
    final coreStats = <StatEntry>[];
    final combatStats = <StatEntry>[];
    final tags = <String>[];

    for (final entry in (heroData.properties ?? {}).entries) {
      final k = entry.key;
      final v = entry.value;
      if (PropFormatter.isHiddenPropKey(k)) continue;

      if (k == 'heroTag') {
        final raw = v is List
            ? v.cast<String>()
            : v.toString().split(',');
        tags.addAll(raw.map((s) => s.trim()).where((s) => s.isNotEmpty));
        continue;
      }

      final bucket = PropFormatter.classifyPropKey(k);
      final pretty = v is List
          ? v.map((vv) => PropFormatter.prettifyPropValue(k, vv) ?? '').join(', ')
          : PropFormatter.prettifyPropValue(k, v) ?? '';

      if (bucket == 'Core') {
        coreStats.add(StatEntry(key: PropFormatter.prettifyPropKey(k), value: pretty));
      } else if (bucket == 'Combat') {
        combatStats.add(StatEntry(key: PropFormatter.prettifyPropKey(k), value: pretty));
      }
    }

    // Walk hero -> hasAbilityInSlot -> bnode -> [slot, ability]
    final slotBindings = <_SlotBinding>[];
    for (final (bnId, pred) in (outgoing[heroData.id] ?? [])) {
      if (pred != 'hasAbilityInSlot') continue;

      final bnOuts = outgoing[bnId] ?? [];
      final slotEdge = bnOuts.where((o) => o.$2 == 'slot').firstOrNull;
      final abEdge   = bnOuts.where((o) => o.$2 == 'ability').firstOrNull;
      if (slotEdge == null || abEdge == null) continue;

      final slotNode = nodeById[slotEdge.$1];
      final abNode   = nodeById[abEdge.$1];
      if (slotNode == null || abNode == null) continue;

      final slotShort = slotNode.shortId ?? '';
      final isSig = _signatureSlotShortIds.contains(slotShort);

      final abPreds = (outgoing[abNode.id] ?? []).map((o) => o.$2).toSet();
      final isAberrant =
          abPreds.contains('hasProperty') || abPreds.contains('hasUpgrade');

      if (!isSig && !isAberrant) continue;

      slotBindings.add(_SlotBinding(
        slotShort: slotShort,
        slotNode: slotNode,
        abNode: abNode,
        isAberrant: isAberrant && !isSig,
      ));
    }

    slotBindings.sort((a, b) {
      final ai = _slotSortOrder.indexOf(a.slotShort);
      final bi = _slotSortOrder.indexOf(b.slotShort);
      final ax = ai == -1 ? 99 : ai;
      final bx = bi == -1 ? 99 : bi;
      if (ax != bx) return ax - bx;
      return a.slotShort.compareTo(b.slotShort);
    });

    final slots = slotBindings.map((binding) {
      return _buildSlot(binding, outgoing, nodeById);
    }).toList();

    return KitData(
      hero: HeroKitInfo(
        name: heroData.label,
        tags: tags,
        stats: HeroStats(core: coreStats, combat: combatStats),
      ),
      slots: slots,
    );
  }

  static SlotData _buildSlot(
    _SlotBinding binding,
    Map<String, List<(String, String)>> outgoing,
    Map<String, NodeData> nodeById,
  ) {
    final abNode = binding.abNode;
    final slotShort = binding.slotShort;

    // Collect properties and upgrades
    final properties = <NodeData>[];
    final upgrades = <NodeData>[];
    for (final (t, p) in (outgoing[abNode.id] ?? [])) {
      final target = nodeById[t];
      if (target == null) continue;
      if (p == 'hasProperty') properties.add(target);
      if (p == 'hasUpgrade') upgrades.add(target);
    }

    // Pick up to 4 stats from priority list
    final statDisplay = <AbilityStat>[];
    for (final label in _statPriority) {
      if (statDisplay.length >= 4) break;
      final match = properties.where((p) => p.label == label).firstOrNull;
      if (match == null) continue;

      final props = match.properties ?? {};
      final baseRaw = props['baseValue'] != null
          ? PropFormatter.prettifyPropValue('baseValue', props['baseValue'])
          : null;
      final unitHint = (props['internalName'] as String?) ?? match.label;
      final baseValue = baseRaw != null
          ? PropFormatter.withUnit(baseRaw, unitHint)
          : null;
      final scaleFn = props['scaleFunction'] != null
          ? PropFormatter.prettifyPropValue('scaleFunction', props['scaleFunction'])
          : null;

      statDisplay.add(AbilityStat(
        label: PropFormatter.spiritize(
            PropFormatter.stripParentName(match.label, abNode.label)),
        value: baseValue,
        scalesWith: scaleFn,
      ));
    }

    // Group upgrades by tier level
    final tierBuckets = <String, List<NodeData>>{};
    for (final u in upgrades) {
      final lvl = u.properties?['upgradeLevel']?.toString() ?? '?';
      tierBuckets.putIfAbsent(lvl, () => []).add(u);
    }

    final upgradeStamps = tierBuckets.entries.toList()
      ..sort((a, b) {
        final ai = int.tryParse(a.key) ?? 99;
        final bi = int.tryParse(b.key) ?? 99;
        return ai.compareTo(bi);
      });

    final formattedUpgrades = upgradeStamps.take(3).map((entry) {
      final effects = entry.value.map((u) {
        final raw = u.properties?['bonusValue']?.toString() ?? '';
        final modProp = u.properties?['modifiesProperty']?.toString() ?? '';
        String propLabel = modProp.isNotEmpty
            ? PropFormatter.prettifyPropValue('modifiesProperty', modProp) ?? u.label
            : u.label;
        propLabel = PropFormatter.spiritize(
            PropFormatter.stripParentName(propLabel, abNode.label));
        final unitHint = modProp.isNotEmpty ? modProp : propLabel;
        String bonus = raw;
        if (bonus.isNotEmpty &&
            !RegExp(r'^[+-]').hasMatch(bonus) &&
            bonus != '0') {
          bonus = '+$bonus';
        }
        return UpgradeEffect(
          bonus: PropFormatter.withUnit(bonus, unitHint),
          prop: propLabel,
        );
      }).toList();
      return UpgradeData(level: entry.key, effects: effects);
    }).toList();

    // Build display name
    final heroLabel = binding.slotNode.properties?['label'] as String? ?? '';
    String displayAbilityName = PropFormatter.spiritize(
        PropFormatter.stripParentName(abNode.label, heroLabel.isNotEmpty
            ? heroLabel
            : _extractHeroLabel(abNode, outgoing, nodeById)));
    if (slotShort == 'slot/WeaponPrimary' &&
        RegExp(r'^set$', caseSensitive: false).hasMatch(displayAbilityName)) {
      displayAbilityName = '';
    }

    String slotLabel = _slotDisplayNames[slotShort] ?? _fallbackSlotLabel(slotShort);

    return SlotData(
      slotLabel: slotLabel,
      slotShort: slotShort,
      isAberrant: binding.isAberrant,
      ability: AbilityKitData(
        name: displayAbilityName,
        stats: statDisplay,
        upgrades: formattedUpgrades,
      ),
    );
  }

  static String _fallbackSlotLabel(String slotShort) {
    return slotShort
        .replaceFirst(RegExp(r'^slot/'), '')
        .replaceFirst(RegExp(r'^Ability'), '')
        .replaceAllMapped(RegExp(r'([a-z0-9])([A-Z])'),
            (m) => '${m.group(1)} ${m.group(2)}');
  }

  /// Port of computeKitSet() from nydus.html line 11241.
  /// Returns the set of node IDs that belong to the signature kit
  /// (Hero + signature slots + their abilities + ability properties/upgrades).
  static Set<String> computeKitNodeIds(HeroGraph graph) {
    final outgoing = <String, List<(String, String)>>{};
    for (final e in graph.edges) {
      outgoing.putIfAbsent(e.data.source, () => []);
      outgoing[e.data.source]!.add((e.data.target, e.data.label));
    }
    final nodeById = <String, NodeData>{
      for (final n in graph.nodes) n.data.id: n.data,
    };

    final heroNode =
        graph.nodes.where((n) => n.data.classList.contains('Hero')).firstOrNull;
    if (heroNode == null) {
      return graph.nodes.map((n) => n.data.id).toSet();
    }
    final heroId = heroNode.data.id;

    // Abilities with hero-specific hasProperty or hasUpgrade edges.
    final aberrantAbilities = <String>{};
    for (final n in graph.nodes) {
      if (!n.data.classList.contains('Ability')) continue;
      final preds =
          (outgoing[n.data.id] ?? <(String, String)>[]).map((o) => o.$2).toSet();
      if (preds.contains('hasProperty') || preds.contains('hasUpgrade')) {
        aberrantAbilities.add(n.data.id);
      }
    }

    final kit = <String>{heroId};
    final sigAbilities = <String>[];

    for (final (bnodeId, pred)
        in (outgoing[heroId] ?? <(String, String)>[])) {
      if (pred != 'hasAbilityInSlot') continue;

      final bnOuts = outgoing[bnodeId] ?? <(String, String)>[];
      final slotEntry = bnOuts.where((o) => o.$2 == 'slot').firstOrNull;
      if (slotEntry == null) continue;
      final slotNode = nodeById[slotEntry.$1];
      final slotShort = slotNode?.shortId ?? '';

      final abEntry = bnOuts.where((o) => o.$2 == 'ability').firstOrNull;
      final abId = abEntry?.$1;
      final isSig = _signatureSlotShortIds.contains(slotShort);
      final isAberrantMovement = abId != null && aberrantAbilities.contains(abId);

      if (!isSig && !isAberrantMovement) continue;

      kit.add(bnodeId);
      for (final (t, pp) in bnOuts) {
        kit.add(t);
        if (pp == 'ability') sigAbilities.add(t);
      }
    }

    // Include 1-3 hop descendants of each signature ability.
    for (final aid in sigAbilities) {
      for (final (t1, _) in (outgoing[aid] ?? <(String, String)>[])) {
        kit.add(t1);
        for (final (t2, _) in (outgoing[t1] ?? <(String, String)>[])) {
          kit.add(t2);
          for (final (t3, _) in (outgoing[t2] ?? <(String, String)>[])) {
            kit.add(t3);
          }
        }
      }
    }

    return kit;
  }

  // Extracts hero label by traversing back up to find the hero node label.
  static String _extractHeroLabel(
    NodeData abNode,
    Map<String, List<(String, String)>> outgoing,
    Map<String, NodeData> nodeById,
  ) {
    // The ability name often includes the hero name as a prefix; we just
    // use a best-effort extraction from the ability label itself.
    final parts = abNode.label.split(RegExp(r'(?=[A-Z])'));
    return parts.isNotEmpty ? parts.first : '';
  }
}

class _SlotBinding {
  final String slotShort;
  final NodeData slotNode;
  final NodeData abNode;
  final bool isAberrant;

  const _SlotBinding({
    required this.slotShort,
    required this.slotNode,
    required this.abNode,
    required this.isAberrant,
  });
}
