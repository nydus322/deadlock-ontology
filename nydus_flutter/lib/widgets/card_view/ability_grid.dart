import 'package:flutter/material.dart';
import '../../data/models/kit_data.dart';
import 'ability_card.dart';

// Stagger delays matching the HTML's nth-child animation offsets.
const _staggerDelays = [0, 80, 160, 240, 320, 400];

class AbilityGrid extends StatelessWidget {
  final List<SlotData> slots;

  const AbilityGrid({super.key, required this.slots});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        // auto-fit: minmax(240px, 1fr) equivalent
        final minWidth = 240.0;
        final cols = (constraints.maxWidth / minWidth).floor().clamp(1, 6);
        return Wrap(
          spacing: 16,
          runSpacing: 16,
          children: [
            for (var i = 0; i < slots.length; i++)
              SizedBox(
                width: (constraints.maxWidth - (cols - 1) * 16) / cols,
                child: AbilityCard(
                  slot: slots[i],
                  animationDelayMs:
                      i < _staggerDelays.length ? _staggerDelays[i] : 400,
                ),
              ),
          ],
        );
      },
    );
  }
}
