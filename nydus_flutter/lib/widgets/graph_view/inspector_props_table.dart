import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';

class InspectorPropsTable extends StatelessWidget {
  final Map<String, dynamic> properties;

  const InspectorPropsTable({super.key, required this.properties});

  @override
  Widget build(BuildContext context) {
    if (properties.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: properties.entries.map((e) {
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 2),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                flex: 4,
                child: Text(e.key,
                    style: AppTextStyles.statLabel
                        .copyWith(color: AppColors.fgMuted)),
              ),
              const SizedBox(width: 8),
              Expanded(
                flex: 5,
                child: Text(
                  e.value?.toString() ?? '—',
                  style: AppTextStyles.statValue,
                  textAlign: TextAlign.end,
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }
}
