import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../state/graph_notifier.dart';
import '../../theme/app_colors.dart';
import '../shared/filter_chip_widget.dart';
import '../shared/section_header.dart';

const _classFilters = [
  ('Hero',             AppColors.classHero),
  ('Ability',          AppColors.classAbility),
  ('AbilityProperty',  AppColors.classAbilityProperty),
  ('AbilityUpgrade',   AppColors.classAbilityUpgrade),
  ('PropertyCategory', AppColors.classPropertyCategory),
  ('Stat',             AppColors.classStat),
  ('Slot',             AppColors.classSlot),
  ('ScaleFunction',    AppColors.classScaleFunction),
];

const _edgeFilters = [
  'hasSlot',
  'filledBy',
  'hasProperty',
  'hasUpgrade',
  'scalesStat',
  'primaryCategory',
  'secondaryCategory',
];

class GraphLeftSidebar extends ConsumerWidget {
  const GraphLeftSidebar({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final graphState = ref.watch(graphNotifierProvider);
    final notifier = ref.read(graphNotifierProvider.notifier);

    return Container(
      width: 240,
      decoration: const BoxDecoration(
        color: AppColors.bgElev,
        border: Border(right: BorderSide(color: AppColors.border)),
      ),
      padding: const EdgeInsets.all(12),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SectionHeader(title: 'Node Types'),
            Wrap(
              spacing: 4,
              runSpacing: 4,
              children: _classFilters.map((entry) {
                final (label, color) = entry;
                return FilterChipWidget(
                  label: label,
                  active: graphState.classFilter.contains(label),
                  color: color,
                  onTap: () => notifier.toggleClassFilter(label),
                );
              }).toList(),
            ),
            const SizedBox(height: 16),
            const SectionHeader(title: 'Edges'),
            Wrap(
              spacing: 4,
              runSpacing: 4,
              children: _edgeFilters.map((pred) {
                return FilterChipWidget(
                  label: pred,
                  active: graphState.edgeFilter.contains(pred),
                  onTap: () => notifier.toggleEdgeFilter(pred),
                );
              }).toList(),
            ),
            const SizedBox(height: 16),
            const SectionHeader(title: 'Mode'),
            FilterChipWidget(
              label: graphState.kitMode ? 'Kit only' : 'All nodes',
              active: true,
              onTap: () => notifier.toggleKitMode(),
            ),
          ],
        ),
      ),
    );
  }
}
