import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../state/app_providers.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';

class HeroPicker extends ConsumerWidget {
  const HeroPicker({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final heroList = ref.watch(heroListProvider);
    final currentCode = ref.watch(currentHeroCodeProvider);

    if (heroList.isEmpty) {
      return const SizedBox(width: 140);
    }

    return Container(
      height: 30,
      padding: const EdgeInsets.symmetric(horizontal: 10),
      decoration: BoxDecoration(
        color: AppColors.bgElev2,
        border: Border.all(color: AppColors.border),
        borderRadius: BorderRadius.circular(6),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: heroList.any((h) => h.codename == currentCode)
              ? currentCode
              : heroList.first.codename,
          dropdownColor: AppColors.bgElev2,
          style: AppTextStyles.statValue,
          icon: const Icon(Icons.keyboard_arrow_down,
              size: 16, color: AppColors.fgMuted),
          isDense: true,
          items: heroList
              .map((h) => DropdownMenuItem(
                    value: h.codename,
                    child: Text(h.publicName,
                        style: AppTextStyles.statValue),
                  ))
              .toList(),
          onChanged: (code) {
            if (code != null) {
              ref.read(currentHeroCodeProvider.notifier).state = code;
            }
          },
        ),
      ),
    );
  }
}
