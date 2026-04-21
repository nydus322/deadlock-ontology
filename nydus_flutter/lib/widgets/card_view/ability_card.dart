import 'package:flutter/material.dart';
import '../../data/models/kit_data.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_theme.dart';
import 'ability_stats_list.dart';
import 'upgrade_row.dart';

class AbilityCard extends StatefulWidget {
  final SlotData slot;
  /// Stagger delay for the settle-in animation (ms).
  final int animationDelayMs;

  const AbilityCard({
    super.key,
    required this.slot,
    this.animationDelayMs = 0,
  });

  @override
  State<AbilityCard> createState() => _AbilityCardState();
}

class _AbilityCardState extends State<AbilityCard>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _opacity;
  late final Animation<Offset> _slide;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 400),
    );
    _opacity = CurvedAnimation(parent: _ctrl, curve: Curves.easeOut);
    _slide = Tween<Offset>(
      begin: const Offset(0, 0.06),
      end: Offset.zero,
    ).animate(CurvedAnimation(parent: _ctrl, curve: Curves.easeOut));

    Future.delayed(Duration(milliseconds: widget.animationDelayMs), () {
      if (mounted) _ctrl.forward();
    });
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _opacity,
      child: SlideTransition(
        position: _slide,
        child: _CardContent(slot: widget.slot),
      ),
    );
  }
}

class _CardContent extends StatefulWidget {
  final SlotData slot;
  const _CardContent({required this.slot});

  @override
  State<_CardContent> createState() => _CardContentState();
}

class _CardContentState extends State<_CardContent> {
  bool _hovered = false;

  @override
  Widget build(BuildContext context) {
    final heroAccent = Theme.of(context).extension<HeroAccentTheme>();
    final accent = widget.slot.isWeapon
        ? AppColors.accentWarm
        : widget.slot.isAberrant
            ? AppColors.fgSoft
            : (heroAccent?.accent ?? AppColors.accentWarm);

    return MouseRegion(
      onEnter: (_) => setState(() => _hovered = true),
      onExit: (_) => setState(() => _hovered = false),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 160),
        transform: Matrix4.translationValues(0, _hovered ? -3 : 0, 0),
        decoration: BoxDecoration(
          color: AppColors.bgElev,
          borderRadius: BorderRadius.circular(6),
          border: Border(top: BorderSide(color: accent, width: 2)),
          boxShadow: _hovered
              ? [BoxShadow(color: Colors.black.withValues(alpha: 0.5), blurRadius: 32, offset: const Offset(0, 8))]
              : [],
        ),
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Slot label
            Text(
              widget.slot.slotLabel,
              style: AppTextStyles.slotLabel.copyWith(color: accent),
            ),
            const SizedBox(height: 4),
            // Ability name
            if (widget.slot.ability.name.isNotEmpty) ...[
              Text(widget.slot.ability.name, style: AppTextStyles.abilityName),
              const SizedBox(height: 10),
            ],
            // Stats
            if (widget.slot.ability.stats.isNotEmpty) ...[
              AbilityStatsList(stats: widget.slot.ability.stats),
              const SizedBox(height: 10),
            ],
            // Upgrade tier stamps
            if (widget.slot.ability.upgrades.isNotEmpty)
              UpgradeRow(upgrades: widget.slot.ability.upgrades),
          ],
        ),
      ),
    );
  }
}
