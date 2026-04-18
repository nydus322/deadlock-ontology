import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:nydus_flutter/data/models/kit_data.dart';
import 'package:nydus_flutter/widgets/shared/tag_chip.dart';
import 'package:nydus_flutter/widgets/shared/stat_row.dart';
import 'package:nydus_flutter/widgets/shared/section_header.dart';
import 'package:nydus_flutter/widgets/card_view/tier_stamp.dart';

// Minimal dark theme so widgets that read theme colors don't throw.
Widget _wrap(Widget child) => MaterialApp(
      theme: ThemeData.dark(),
      home: Scaffold(body: Center(child: child)),
    );

void main() {
  group('TagChip', () {
    testWidgets('renders its label text', (tester) async {
      await tester.pumpWidget(_wrap(const TagChip(label: 'Carry')));
      expect(find.text('Carry'), findsOneWidget);
    });

    testWidgets('accepts a custom color without throwing', (tester) async {
      await tester.pumpWidget(
          _wrap(const TagChip(label: 'Durable', color: Colors.red)));
      expect(find.text('Durable'), findsOneWidget);
    });

    testWidgets('uses default color when none provided', (tester) async {
      await tester.pumpWidget(_wrap(const TagChip(label: 'Flex')));
      // Widget renders without error; label is visible.
      expect(find.text('Flex'), findsOneWidget);
    });
  });

  group('StatRow', () {
    testWidgets('renders label and value', (tester) async {
      await tester.pumpWidget(
          _wrap(const StatRow(label: 'Max Health', value: '625')));
      expect(find.text('Max Health'), findsOneWidget);
      expect(find.text('625'), findsOneWidget);
    });

    testWidgets('long label does not overflow (Flexible wraps it)', (tester) async {
      await tester.pumpWidget(_wrap(
        const SizedBox(
          width: 200,
          child: StatRow(
            label: 'A Very Long Property Name That Would Overflow',
            value: '99',
          ),
        ),
      ));
      // Should render without a layout overflow error.
      expect(tester.takeException(), isNull);
    });
  });

  group('StatDivider', () {
    testWidgets('renders without error', (tester) async {
      await tester.pumpWidget(_wrap(const StatDivider()));
      expect(tester.takeException(), isNull);
    });
  });

  group('SectionHeader', () {
    testWidgets('renders title in uppercase', (tester) async {
      await tester.pumpWidget(_wrap(const SectionHeader(title: 'core')));
      expect(find.text('CORE'), findsOneWidget);
    });

    testWidgets('already-uppercase title is preserved', (tester) async {
      await tester.pumpWidget(_wrap(const SectionHeader(title: 'COMBAT')));
      expect(find.text('COMBAT'), findsOneWidget);
    });
  });

  group('TierStamp', () {
    const upgrade = UpgradeData(
      level: '1',
      effects: [
        UpgradeEffect(bonus: '+10%', prop: 'Damage'),
      ],
    );

    testWidgets('shows tier label', (tester) async {
      await tester.pumpWidget(_wrap(const TierStamp(upgrade: upgrade)));
      expect(find.text('T1'), findsOneWidget);
    });

    testWidgets('shows bonus value', (tester) async {
      await tester.pumpWidget(_wrap(const TierStamp(upgrade: upgrade)));
      expect(find.text('+10%'), findsOneWidget);
    });

    testWidgets('shows prop name', (tester) async {
      await tester.pumpWidget(_wrap(const TierStamp(upgrade: upgrade)));
      expect(find.text('Damage'), findsOneWidget);
    });

    testWidgets('empty prop is not rendered', (tester) async {
      const noProps = UpgradeData(
        level: '2',
        effects: [UpgradeEffect(bonus: '+5s', prop: '')],
      );
      await tester.pumpWidget(_wrap(const TierStamp(upgrade: noProps)));
      expect(find.text('T2'), findsOneWidget);
      expect(find.text('+5s'), findsOneWidget);
      // No extra empty Text widget for the prop.
      expect(find.text(''), findsNothing);
    });

    testWidgets('multiple effects are all rendered', (tester) async {
      const multi = UpgradeData(
        level: '3',
        effects: [
          UpgradeEffect(bonus: '+15%', prop: 'Range'),
          UpgradeEffect(bonus: '-1s', prop: 'Cooldown'),
        ],
      );
      await tester.pumpWidget(_wrap(const TierStamp(upgrade: multi)));
      expect(find.text('+15%'), findsOneWidget);
      expect(find.text('-1s'), findsOneWidget);
    });
  });
}
