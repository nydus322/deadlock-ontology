import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';

class TagChip extends StatelessWidget {
  final String label;
  final Color? color;

  const TagChip({super.key, required this.label, this.color});

  @override
  Widget build(BuildContext context) {
    final c = color ?? AppColors.fgSoft;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      decoration: BoxDecoration(
        border: Border.all(color: c.withValues(alpha: 0.5)),
        borderRadius: BorderRadius.circular(999),
        color: c.withValues(alpha: 0.08),
      ),
      child: Text(label, style: AppTextStyles.tagChip.copyWith(color: c)),
    );
  }
}
