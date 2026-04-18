import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/models/bundle_data.dart';
import '../data/models/kit_data.dart';
import '../data/extractors/kit_extractor.dart';
import '../data/extractors/topology.dart';
import '../data/repository/bundle_repository.dart';
import '../theme/hero_accents.dart';
import '../theme/app_theme.dart';
import 'app_state.dart';

// ---- Bundle loading -----------------------------------------------------------

final bundleProvider = FutureProvider<BundleData>((ref) async {
  return BundleRepository().load();
});

// ---- Hero list (order + display names) ----------------------------------------

final heroListProvider = Provider<List<HeroEntry>>((ref) {
  return ref.watch(bundleProvider).valueOrNull?.heroList ?? [];
});

// ---- Current hero selection ---------------------------------------------------

final currentHeroCodeProvider = StateProvider<String>((ref) {
  final bundle = ref.watch(bundleProvider).valueOrNull;
  return bundle?.order.firstOrNull ?? 'hero_inferno';
});

// ---- Current hero's graph data ------------------------------------------------

final currentHeroGraphProvider = Provider((ref) {
  final code = ref.watch(currentHeroCodeProvider);
  return ref.watch(bundleProvider).valueOrNull?.hero(code);
});

// ---- Extracted kit data (card view) ------------------------------------------

final kitDataProvider = Provider<KitData?>((ref) {
  final graph = ref.watch(currentHeroGraphProvider);
  if (graph == null) return null;
  return KitExtractor.extract(graph);
});

// ---- Per-hero accent color ---------------------------------------------------

final heroAccentColorProvider = Provider<Color>((ref) {
  final code = ref.watch(currentHeroCodeProvider);
  return HeroAccents.forHero(code);
});

final heroAccentThemeProvider = Provider<HeroAccentTheme>((ref) {
  final code = ref.watch(currentHeroCodeProvider);
  return HeroAccentTheme.forHero(code);
});

// ---- View mode (card | graph) ------------------------------------------------

final viewModeProvider = StateProvider<AppViewMode>((_) => AppViewMode.card);

// ---- Graph view: synthesized topology (blank nodes collapsed) ----------------

final synthesizedGraphProvider = Provider<SynthesizedGraph?>((ref) {
  final graph = ref.watch(currentHeroGraphProvider);
  if (graph == null) return null;
  return TopologyExtractor.synthesize(graph);
});

// ---- Graph view: kit node IDs (for kit-mode visibility filtering) ------------

final kitNodeIdsProvider = Provider<Set<String>>((ref) {
  final graph = ref.watch(currentHeroGraphProvider);
  if (graph == null) return {};
  return KitExtractor.computeKitNodeIds(graph);
});
