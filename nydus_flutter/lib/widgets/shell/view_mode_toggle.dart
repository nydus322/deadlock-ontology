import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../state/app_providers.dart';
import '../../state/app_state.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';

class ViewModeToggle extends ConsumerWidget {
  const ViewModeToggle({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final mode = ref.watch(viewModeProvider);

    return Container(
      height: 30,
      decoration: BoxDecoration(
        color: AppColors.bgElev2,
        border: Border.all(color: AppColors.border),
        borderRadius: BorderRadius.circular(6),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          _ToggleButton(
            label: 'Card',
            active: mode == AppViewMode.card,
            onTap: () =>
                ref.read(viewModeProvider.notifier).state = AppViewMode.card,
            isFirst: true,
          ),
          _ToggleButton(
            label: 'Map',
            active: mode == AppViewMode.graph,
            onTap: () =>
                ref.read(viewModeProvider.notifier).state = AppViewMode.graph,
            isFirst: false,
          ),
        ],
      ),
    );
  }
}

class _ToggleButton extends ConsumerWidget {
  final String label;
  final bool active;
  final VoidCallback onTap;
  final bool isFirst;

  const _ToggleButton({
    required this.label,
    required this.active,
    required this.onTap,
    required this.isFirst,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final accent = Theme.of(context).colorScheme.primary;
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 140),
        padding: const EdgeInsets.symmetric(horizontal: 12),
        decoration: BoxDecoration(
          color: active ? accent.withValues(alpha: 0.15) : Colors.transparent,
          border: Border(
            left: isFirst
                ? BorderSide.none
                : const BorderSide(color: AppColors.border),
          ),
          borderRadius: isFirst
              ? const BorderRadius.horizontal(left: Radius.circular(5))
              : const BorderRadius.horizontal(right: Radius.circular(5)),
        ),
        child: Text(
          label,
          style: AppTextStyles.tagChip.copyWith(
            color: active ? accent : AppColors.fgMuted,
            fontWeight: active ? FontWeight.w700 : FontWeight.w500,
          ),
        ),
      ),
    );
  }
}
