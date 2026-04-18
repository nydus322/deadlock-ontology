import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../state/app_providers.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_theme.dart';
import 'hero_card_header.dart';
import 'ability_grid.dart';
import 'stats_spine.dart';

class HeroCardView extends ConsumerWidget {
  const HeroCardView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final kit = ref.watch(kitDataProvider);
    final heroAccent = Theme.of(context).extension<HeroAccentTheme>();
    final accentSoft = heroAccent?.accentSoft ?? AppColors.accentWarm.withValues(alpha: 0.2);

    if (kit == null) {
      return const Center(
        child: CircularProgressIndicator(color: AppColors.accent),
      );
    }

    return Container(
      decoration: BoxDecoration(
        gradient: RadialGradient(
          center: const Alignment(0, -1),
          radius: 1.0,
          colors: [accentSoft, Colors.transparent],
          stops: const [0.0, 0.55],
        ),
      ),
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(32),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 1200),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                HeroCardHeader(
                  heroName: kit.hero.name,
                  tags: kit.hero.tags,
                ),
                _CardBody(kit: kit),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _CardBody extends StatelessWidget {
  final dynamic kit;

  const _CardBody({required this.kit});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final showSpine = constraints.maxWidth > 680;

        if (showSpine) {
          return Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(child: AbilityGrid(slots: kit.slots)),
              const SizedBox(width: 32),
              StatsSpine(stats: kit.hero.stats),
            ],
          );
        }

        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            AbilityGrid(slots: kit.slots),
            const SizedBox(height: 24),
            StatsSpine(stats: kit.hero.stats),
          ],
        );
      },
    );
  }
}
