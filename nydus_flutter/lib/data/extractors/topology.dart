// Port of synthesizeKitTopology() from nydus.html lines 11986-12041.
// Collapses RDF blank-node hasAbilityInSlot intermediaries into direct
// Hero → Slot → Ability edges for a cleaner graph view.

import '../models/bundle_data.dart';
import '../models/graph_elements.dart';

class SynthesizedGraph {
  final List<GraphNode> nodes;
  final List<GraphEdge> edges;
  const SynthesizedGraph({required this.nodes, required this.edges});
}

class TopologyExtractor {
  static SynthesizedGraph synthesize(HeroGraph graph) {
    final outgoing = <String, List<(String, String)>>{};
    for (final e in graph.edges) {
      outgoing.putIfAbsent(e.data.source, () => []);
      outgoing[e.data.source]!.add((e.data.target, e.data.label));
    }

    final heroNode =
        graph.nodes.where((n) => n.data.classList.contains('Hero')).firstOrNull;
    if (heroNode == null) {
      return SynthesizedGraph(nodes: graph.nodes, edges: graph.edges);
    }
    final heroId = heroNode.data.id;

    final bnodeIds = <String>{};
    final syntheticEdges = <GraphEdge>[];

    for (final (bn, pred) in (outgoing[heroId] ?? <(String, String)>[])) {
      if (pred != 'hasAbilityInSlot') continue;

      final bnOuts = outgoing[bn] ?? <(String, String)>[];
      final slotEntry = bnOuts.where((o) => o.$2 == 'slot').firstOrNull;
      final abEntry   = bnOuts.where((o) => o.$2 == 'ability').firstOrNull;
      if (slotEntry == null || abEntry == null) continue;

      bnodeIds.add(bn);
      final slotId = slotEntry.$1;
      final abId   = abEntry.$1;

      // Hero → Slot  (label = predicate so edge filter + painter work correctly)
      syntheticEdges.add(GraphEdge(
        data: EdgeData(
          id: 'syn-hs-$slotId',
          source: heroId,
          target: slotId,
          label: 'hasSlot',
          classes: 'hasSlot synthetic',
        ),
      ));

      // Slot → Ability
      syntheticEdges.add(GraphEdge(
        data: EdgeData(
          id: 'syn-sa-$slotId-$abId',
          source: slotId,
          target: abId,
          label: 'filledBy',
          classes: 'filledBy synthetic',
        ),
      ));
    }

    // Drop blank nodes and any edges touching them; add synthetic replacements.
    final nodes =
        graph.nodes.where((n) => !bnodeIds.contains(n.data.id)).toList();
    final edges = graph.edges
        .where((e) =>
            !bnodeIds.contains(e.data.source) &&
            !bnodeIds.contains(e.data.target))
        .toList()
      ..addAll(syntheticEdges);

    return SynthesizedGraph(nodes: nodes, edges: edges);
  }
}
