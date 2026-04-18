import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/models/graph_elements.dart';
import '../../state/app_providers.dart';
import '../../state/graph_notifier.dart';
import '../../theme/app_colors.dart';
import 'inspector_panel.dart';
import 'inspector_edge_list.dart';

class GraphRightSidebar extends ConsumerWidget {
  const GraphRightSidebar({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final graphState = ref.watch(graphNotifierProvider);
    final heroGraph = ref.watch(currentHeroGraphProvider);

    NodeData? selectedNode;
    List<InspectorEdgeEntry> outgoing = [];
    List<InspectorEdgeEntry> incoming = [];

    if (graphState.selectedNodeId != null && heroGraph != null) {
      final nodeById = {for (final n in heroGraph.nodes) n.data.id: n.data};
      selectedNode = nodeById[graphState.selectedNodeId];

      if (selectedNode != null) {
        for (final e in heroGraph.edges) {
          final target = nodeById[e.data.target];
          final source = nodeById[e.data.source];
          if (e.data.source == selectedNode.id && target != null) {
            outgoing.add(InspectorEdgeEntry(
              predicate: e.data.label,
              nodeLabel: target.label,
              nodeId: e.data.target,
            ));
          }
          if (e.data.target == selectedNode.id && source != null) {
            incoming.add(InspectorEdgeEntry(
              predicate: e.data.label,
              nodeLabel: source.label,
              nodeId: e.data.source,
            ));
          }
        }
      }
    }

    return Container(
      width: 300,
      decoration: const BoxDecoration(
        color: AppColors.bgElev,
        border: Border(left: BorderSide(color: AppColors.border)),
      ),
      child: InspectorPanel(
        node: selectedNode,
        outgoing: outgoing,
        incoming: incoming,
        onNodeTap: (id) {
          ref.read(graphNotifierProvider.notifier).selectNode(id);
        },
      ),
    );
  }
}
