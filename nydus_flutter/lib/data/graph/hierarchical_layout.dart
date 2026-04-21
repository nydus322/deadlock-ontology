import 'dart:collection';
import 'dart:math' as math;
import 'dart:ui' show Offset;
import 'force_layout.dart';

/// Class-based hierarchical layout.
///
/// Algorithm:
/// 1. Assign each node a level from its [primaryClass] using a fixed map,
///    so every node of the same class shares the same horizontal row.
/// 2. Run a BFS from the Hero root to determine a discovery order for nodes
///    within each level, keeping slot-ability clusters together.
/// 3. x is evenly distributed within each level; y = level × [levelGap].
///    The whole graph is centered on [center].
///
/// The result is a set of [ForceNode]s with final positions and zero
/// velocity — no animation is needed.
class HierarchicalLayout {
  static const double levelGap     = 160.0;
  static const double nodeSpacing  = 86.0;
  static const double groupPadding = 24.0;

  static const _classLevel = <String, int>{
    'Hero':             0,
    'Slot':             1,
    'Ability':          2,
    'AbilityProperty':  3,
    'PropertyCategory': 3,
    'Stat':             3,
    'AbilityUpgrade':   4,
    'ScaleFunction':    4,
    'ModifierValue':    4,
    'Stage':            4,
  };

  static ({List<ForceNode> nodes, List<ForceEdge> edges}) compute({
    required List<({String id, String primaryClass})> nodeSpecs,
    required List<ForceEdge> edges,
    required String rootId,
    required Offset center,
  }) {
    final nodeIds = {for (final n in nodeSpecs) n.id};

    // ---- 1. Assign level by class ----------------------------------------
    final levelOf = <String, int>{
      for (final n in nodeSpecs) n.id: _classLevel[n.primaryClass] ?? 5,
    };

    // ---- 2. BFS from root to determine ordering within each level ---------
    final children = <String, List<String>>{};
    for (final e in edges) {
      if (!nodeIds.contains(e.source) || !nodeIds.contains(e.target)) continue;
      children.putIfAbsent(e.source, () => []).add(e.target);
    }

    final bfsRank   = <String, int>{};
    final bfsParent = <String, String>{};
    final queue     = Queue<String>();
    int rank        = 0;

    if (nodeIds.contains(rootId)) {
      bfsRank[rootId] = rank++;
      queue.add(rootId);
    }
    while (queue.isNotEmpty) {
      final id = queue.removeFirst();
      for (final child in (children[id] ?? [])) {
        if (!bfsRank.containsKey(child)) {
          bfsRank[child]   = rank++;
          bfsParent[child] = id;
          queue.add(child);
        }
      }
    }
    // Unreachable nodes get an order after all reachable ones.
    for (final n in nodeSpecs) {
      if (!bfsRank.containsKey(n.id)) bfsRank[n.id] = rank++;
    }

    // ---- 3. Group by level, sort by BFS rank -----------------------------
    final byLevel = <int, List<String>>{};
    for (final n in nodeSpecs) {
      byLevel.putIfAbsent(levelOf[n.id]!, () => []).add(n.id);
    }
    for (final list in byLevel.values) {
      list.sort((a, b) => (bfsRank[a] ?? 0).compareTo(bfsRank[b] ?? 0));
    }

    // ---- 4. Assign positions ---------------------------------------------
    final maxLevel   = levelOf.values.fold(0, math.max);
    final totalHeight = maxLevel * levelGap;
    final positions  = <String, Offset>{};

    for (final entry in byLevel.entries) {
      final lvl      = entry.key;
      final lvlNodes = entry.value;
      final count    = lvlNodes.length;

      final y = center.dy - totalHeight / 2 + lvl * levelGap;

      double totalWidth = (count - 1) * nodeSpacing;
      if (count > 1) {
        for (var i = 1; i < count; i++) {
          if (bfsParent[lvlNodes[i]] != bfsParent[lvlNodes[i - 1]]) {
            totalWidth += groupPadding;
          }
        }
      }

      double x = center.dx - totalWidth / 2;
      for (var i = 0; i < count; i++) {
        positions[lvlNodes[i]] = Offset(x, y);
        final gap = nodeSpacing +
            (i < count - 1 &&
                    bfsParent[lvlNodes[i + 1]] != bfsParent[lvlNodes[i]]
                ? groupPadding
                : 0);
        x += gap;
      }
    }

    // ---- 5. Build output -------------------------------------------------
    final forceNodes = nodeSpecs.map((spec) {
      return ForceNode(
        id:       spec.id,
        position: positions[spec.id] ?? center,
        velocity: Offset.zero,
        radius:   radiusForClass(spec.primaryClass),
        pinned:   true,
      );
    }).toList();

    return (nodes: forceNodes, edges: edges);
  }
}
