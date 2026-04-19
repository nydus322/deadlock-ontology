import 'package:flutter/material.dart';
import '../../data/models/kit_data.dart';
import 'ability_card.dart';

// Stagger delays matching the HTML's nth-child animation offsets.
const _staggerDelays = [0, 80, 160, 240, 320, 400];

const _rowSpacing = 16.0;
const _colSpacing = 16.0;
const _cardsPerRow = 3;

class AbilityGrid extends StatelessWidget {
  final List<SlotData> slots;

  const AbilityGrid({super.key, required this.slots});

  @override
  Widget build(BuildContext context) {
    // Separate the Primary Weapon from all other slots.
    final weapon = slots.where((s) => s.isWeapon).toList();
    final others = slots.where((s) => !s.isWeapon).toList();

    // Stagger index starts after the weapon card.
    int staggerIndex = weapon.length;

    return LayoutBuilder(
      builder: (context, constraints) {
        final totalWidth = constraints.maxWidth;
        final colWidth =
            (totalWidth - (_cardsPerRow - 1) * _colSpacing) / _cardsPerRow;

        final rows = <Widget>[];

        // Row 0 — Primary Weapon, full width.
        if (weapon.isNotEmpty) {
          rows.add(AbilityCard(
            slot: weapon.first,
            animationDelayMs: _staggerDelays[0],
          ));
        }

        // Remaining slots in rows of 3.
        for (var i = 0; i < others.length; i += _cardsPerRow) {
          final rowSlots = others.sublist(
            i,
            (i + _cardsPerRow).clamp(0, others.length),
          );
          final cells = <Widget>[];
          for (var j = 0; j < rowSlots.length; j++) {
            final delay = staggerIndex < _staggerDelays.length
                ? _staggerDelays[staggerIndex]
                : 400;
            staggerIndex++;
            cells.add(SizedBox(
              width: colWidth,
              child: AbilityCard(
                slot: rowSlots[j],
                animationDelayMs: delay,
              ),
            ));
          }
          rows.add(Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: cells
                .expand((c) => [c, const SizedBox(width: _colSpacing)])
                .toList()
              ..removeLast(), // drop the trailing spacer
          ));
        }

        return Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: rows
              .expand((r) => [r, const SizedBox(height: _rowSpacing)])
              .toList()
            ..removeLast(), // drop the trailing spacer
        );
      },
    );
  }
}
