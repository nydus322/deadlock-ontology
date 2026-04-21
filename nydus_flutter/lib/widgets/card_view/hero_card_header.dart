import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import '../../theme/app_theme.dart';
import '../shared/tag_chip.dart';

class HeroCardHeader extends StatefulWidget {
  final String heroName;
  final List<String> tags;

  const HeroCardHeader({
    super.key,
    required this.heroName,
    required this.tags,
  });

  @override
  State<HeroCardHeader> createState() => _HeroCardHeaderState();
}

class _HeroCardHeaderState extends State<HeroCardHeader>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _opacity;
  late final Animation<Offset> _slide;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 500),
    );
    _opacity = CurvedAnimation(parent: _ctrl, curve: Curves.easeOut);
    _slide = Tween<Offset>(
      begin: const Offset(0, -0.04),
      end: Offset.zero,
    ).animate(CurvedAnimation(parent: _ctrl, curve: Curves.easeOut));
    _ctrl.forward();
  }

  @override
  void didUpdateWidget(HeroCardHeader oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.heroName != widget.heroName) {
      _ctrl.forward(from: 0);
    }
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final heroAccent = Theme.of(context).extension<HeroAccentTheme>();
    final accent = heroAccent?.accent ?? AppColors.accentWarm;

    return FadeTransition(
      opacity: _opacity,
      child: SlideTransition(
        position: _slide,
        child: Padding(
          padding: const EdgeInsets.only(bottom: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Decorative accent line above name
              Container(
                height: 2,
                width: 48,
                color: accent,
                margin: const EdgeInsets.only(bottom: 12),
              ),
              // Hero name
              Text(widget.heroName, style: AppTextStyles.heroName),
              const SizedBox(height: 10),
              // Tag chips
              if (widget.tags.isNotEmpty)
                Wrap(
                  spacing: 6,
                  runSpacing: 6,
                  children: widget.tags
                      .map((t) => TagChip(label: t, color: accent))
                      .toList(),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
