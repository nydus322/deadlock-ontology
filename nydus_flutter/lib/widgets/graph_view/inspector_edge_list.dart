import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';

class InspectorEdgeEntry {
  final String predicate;
  final String nodeLabel;
  final String nodeId;

  const InspectorEdgeEntry({
    required this.predicate,
    required this.nodeLabel,
    required this.nodeId,
  });
}

class InspectorEdgeList extends StatelessWidget {
  final String heading;
  final List<InspectorEdgeEntry> edges;
  final void Function(String nodeId)? onNodeTap;

  const InspectorEdgeList({
    super.key,
    required this.heading,
    required this.edges,
    this.onNodeTap,
  });

  @override
  Widget build(BuildContext context) {
    if (edges.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(heading.toUpperCase(), style: AppTextStyles.sectionHeading),
        const SizedBox(height: 6),
        ...edges.map((e) => _EdgeRow(entry: e, onTap: onNodeTap)),
      ],
    );
  }
}

class _EdgeRow extends StatelessWidget {
  final InspectorEdgeEntry entry;
  final void Function(String)? onTap;

  const _EdgeRow({required this.entry, this.onTap});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        children: [
          Text(
            entry.predicate,
            style: AppTextStyles.statLabel.copyWith(
                color: AppColors.fgSoft, fontStyle: FontStyle.italic),
          ),
          const SizedBox(width: 6),
          const Text('→', style: TextStyle(color: AppColors.fgSoft, fontSize: 11)),
          const SizedBox(width: 6),
          Expanded(
            child: GestureDetector(
              onTap: onTap != null ? () => onTap!(entry.nodeId) : null,
              child: Text(
                entry.nodeLabel,
                style: AppTextStyles.statValue.copyWith(
                  color: onTap != null ? AppColors.accent : AppColors.fg,
                  decoration:
                      onTap != null ? TextDecoration.underline : null,
                ),
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
