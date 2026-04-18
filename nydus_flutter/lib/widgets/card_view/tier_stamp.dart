import 'package:flutter/material.dart';
import '../../data/models/kit_data.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';

class TierStamp extends StatelessWidget {
  final UpgradeData upgrade;

  const TierStamp({super.key, required this.upgrade});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(6),
      decoration: BoxDecoration(
        color: AppColors.bgElev2,
        border: Border.all(color: AppColors.border),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('T${upgrade.level}', style: AppTextStyles.tierLabel),
          const SizedBox(height: 4),
          ...upgrade.effects.map((eff) => Padding(
                padding: const EdgeInsets.only(top: 1),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(eff.bonus, style: AppTextStyles.tierValue),
                    if (eff.prop.isNotEmpty)
                      Text(eff.prop, style: AppTextStyles.tierProp),
                  ],
                ),
              )),
        ],
      ),
    );
  }
}
