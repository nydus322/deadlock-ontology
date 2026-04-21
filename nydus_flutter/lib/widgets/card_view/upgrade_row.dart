import 'package:flutter/material.dart';
import '../../data/models/kit_data.dart';
import 'tier_stamp.dart';

class UpgradeRow extends StatelessWidget {
  final List<UpgradeData> upgrades;

  const UpgradeRow({super.key, required this.upgrades});

  @override
  Widget build(BuildContext context) {
    if (upgrades.isEmpty) return const SizedBox.shrink();
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: upgrades
          .expand((u) => [
                Expanded(child: TierStamp(upgrade: u)),
                if (u != upgrades.last) const SizedBox(width: 4),
              ])
          .toList(),
    );
  }
}
