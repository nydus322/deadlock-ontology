import 'package:flutter/material.dart';
import '../../data/models/kit_data.dart';
import '../../theme/app_colors.dart';
import '../shared/section_header.dart';
import '../shared/stat_row.dart';

class StatsSpine extends StatelessWidget {
  final HeroStats stats;

  const StatsSpine({super.key, required this.stats});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 220,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.bgElev,
        border: Border.all(color: AppColors.border),
        borderRadius: BorderRadius.circular(6),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (stats.core.isNotEmpty) ...[
            const SectionHeader(title: 'Core'),
            ...stats.core.map((s) => StatRow(label: s.key, value: s.value)),
          ],
          if (stats.core.isNotEmpty && stats.combat.isNotEmpty)
            const StatDivider(),
          if (stats.combat.isNotEmpty) ...[
            const SectionHeader(title: 'Combat'),
            ...stats.combat.map((s) => StatRow(label: s.key, value: s.value)),
          ],
        ],
      ),
    );
  }
}
