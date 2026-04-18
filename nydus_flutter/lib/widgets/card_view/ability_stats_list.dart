import 'package:flutter/material.dart';
import '../../data/models/kit_data.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';

class AbilityStatsList extends StatelessWidget {
  final List<AbilityStat> stats;

  const AbilityStatsList({super.key, required this.stats});

  @override
  Widget build(BuildContext context) {
    if (stats.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: stats.map((s) => _StatEntry(stat: s)).toList(),
    );
  }
}

class _StatEntry extends StatelessWidget {
  final AbilityStat stat;

  const _StatEntry({required this.stat});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            flex: 5,
            child: Text(stat.label, style: AppTextStyles.statLabel),
          ),
          const SizedBox(width: 8),
          Expanded(
            flex: 4,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  stat.value ?? '—',
                  style: AppTextStyles.statValue,
                  textAlign: TextAlign.end,
                ),
                if (stat.scalesWith != null)
                  Text(
                    'scales ${stat.scalesWith}',
                    style: AppTextStyles.scalesWith.copyWith(
                      color: AppColors.accent.withValues(alpha: 0.8),
                    ),
                    textAlign: TextAlign.end,
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
