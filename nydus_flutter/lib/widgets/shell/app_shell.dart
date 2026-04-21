import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../state/app_providers.dart';
import '../../state/app_state.dart';
import '../../theme/app_colors.dart';
import '../card_view/hero_card_view.dart';
import '../graph_view/graph_view.dart';
import 'nydus_app_bar.dart';

class AppShell extends ConsumerWidget {
  const AppShell({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final heroAccent = ref.watch(heroAccentThemeProvider);
    final baseTheme = Theme.of(context);

    // Propagate per-hero accent via ThemeExtension so all descendant
    // widgets can access it via Theme.of(context).extension<HeroAccentTheme>()
    final themedChild = Theme(
      data: baseTheme.copyWith(
        colorScheme: baseTheme.colorScheme.copyWith(
          primary: heroAccent.accent,
        ),
        extensions: {heroAccent},
      ),
      child: const _ShellBody(),
    );

    return themedChild;
  }
}

class _ShellBody extends ConsumerWidget {
  const _ShellBody();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final viewMode = ref.watch(viewModeProvider);
    final bundleAsync = ref.watch(bundleProvider);

    return Scaffold(
      backgroundColor: AppColors.bg,
      appBar: const NydusAppBar(),
      body: bundleAsync.when(
        loading: () => const Center(
          child: CircularProgressIndicator(color: AppColors.accent),
        ),
        error: (err, _) => Center(
          child: Text(
            'Failed to load bundle: $err',
            style: const TextStyle(color: AppColors.catDamage),
          ),
        ),
        data: (_) => AnimatedSwitcher(
          duration: const Duration(milliseconds: 200),
          child: viewMode == AppViewMode.card
              ? const HeroCardView(key: ValueKey('card'))
              : const GraphView(key: ValueKey('graph')),
        ),
      ),
    );
  }
}
