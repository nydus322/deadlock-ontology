import 'package:flutter/material.dart';
import '../../data/models/graph_elements.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_theme.dart';
import '../shared/section_header.dart';
import 'inspector_props_table.dart';
import 'inspector_edge_list.dart';

class InspectorPanel extends StatelessWidget {
  final NodeData? node;
  final List<InspectorEdgeEntry> outgoing;
  final List<InspectorEdgeEntry> incoming;
  final void Function(String nodeId)? onNodeTap;

  const InspectorPanel({
    super.key,
    required this.node,
    this.outgoing = const [],
    this.incoming = const [],
    this.onNodeTap,
  });

  @override
  Widget build(BuildContext context) {
    if (node == null) {
      return const Center(
        child: Text(
          'Click a node to inspect',
          style: TextStyle(color: AppColors.fgSoft, fontSize: 13),
        ),
      );
    }

    final heroAccent = Theme.of(context).extension<HeroAccentTheme>();
    final accent = heroAccent?.accent ?? AppColors.accent;
    final nodeColor = AppColors.forNodeClass(node!.primaryClass);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Class tag
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
            decoration: BoxDecoration(
              color: nodeColor.withValues(alpha: 0.15),
              border: Border.all(color: nodeColor.withValues(alpha: 0.5)),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              node!.primaryClass,
              style: AppTextStyles.tierLabel.copyWith(color: nodeColor),
            ),
          ),
          const SizedBox(height: 8),
          // Node label
          Text(node!.label,
              style: AppTextStyles.abilityName.copyWith(color: accent)),
          const SizedBox(height: 4),
          // IRI (muted)
          if (node!.iri != null)
            Text(node!.iri!, style: AppTextStyles.iriCode),
          const SizedBox(height: 16),
          // Properties
          if ((node!.properties ?? {}).isNotEmpty) ...[
            const SectionHeader(title: 'Properties'),
            InspectorPropsTable(properties: node!.properties ?? {}),
            const SizedBox(height: 12),
          ],
          // Outgoing edges
          if (outgoing.isNotEmpty) ...[
            InspectorEdgeList(
              heading: 'Outgoing',
              edges: outgoing,
              onNodeTap: onNodeTap,
            ),
            const SizedBox(height: 12),
          ],
          // Incoming edges
          if (incoming.isNotEmpty)
            InspectorEdgeList(
              heading: 'Incoming',
              edges: incoming,
              onNodeTap: onNodeTap,
            ),
        ],
      ),
    );
  }
}
