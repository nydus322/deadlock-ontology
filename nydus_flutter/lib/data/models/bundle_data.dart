import 'graph_elements.dart';

class BundleMeta {
  final int heroCount;
  final String sourceDir;

  const BundleMeta({required this.heroCount, required this.sourceDir});

  factory BundleMeta.fromJson(Map<String, dynamic> j) => BundleMeta(
        heroCount: (j['hero_count'] as num?)?.toInt() ?? 0,
        sourceDir: j['source_dir'] as String? ?? '',
      );
}

class HeroGraph {
  final String codename;
  final String publicName;
  final int heroId;
  final GraphMeta meta;
  final List<GraphNode> nodes;
  final List<GraphEdge> edges;

  const HeroGraph({
    required this.codename,
    required this.publicName,
    required this.heroId,
    required this.meta,
    required this.nodes,
    required this.edges,
  });

  factory HeroGraph.fromJson(String codename, Map<String, dynamic> j) {
    final nodes = (j['nodes'] as List<dynamic>? ?? [])
        .map((n) => GraphNode.fromJson(n as Map<String, dynamic>))
        .toList();
    final edges = (j['edges'] as List<dynamic>? ?? [])
        .map((e) => GraphEdge.fromJson(e as Map<String, dynamic>))
        .toList();
    return HeroGraph(
      codename: codename,
      publicName: j['public_name'] as String? ?? codename,
      heroId: (j['hero_id'] as num?)?.toInt() ?? 0,
      meta: GraphMeta.fromJson(j['meta'] as Map<String, dynamic>? ?? {}),
      nodes: nodes,
      edges: edges,
    );
  }
}

class GraphMeta {
  final String source;
  final int nodeCount;
  final int edgeCount;

  const GraphMeta({
    required this.source,
    required this.nodeCount,
    required this.edgeCount,
  });

  factory GraphMeta.fromJson(Map<String, dynamic> j) => GraphMeta(
        source: j['source'] as String? ?? '',
        nodeCount: (j['node_count'] as num?)?.toInt() ?? 0,
        edgeCount: (j['edge_count'] as num?)?.toInt() ?? 0,
      );
}

class BundleData {
  final BundleMeta meta;
  final List<String> order;
  final Map<String, Map<String, dynamic>> _rawHeroes;
  final Map<String, HeroGraph> _heroCache = {};

  BundleData({
    required this.meta,
    required this.order,
    required Map<String, Map<String, dynamic>> rawHeroes,
  }) : _rawHeroes = rawHeroes;

  factory BundleData.fromJson(Map<String, dynamic> j) {
    final rawHeroes = <String, Map<String, dynamic>>{};
    final heroesMap = j['heroes'] as Map<String, dynamic>? ?? {};
    for (final entry in heroesMap.entries) {
      rawHeroes[entry.key] = entry.value as Map<String, dynamic>;
    }
    return BundleData(
      meta: BundleMeta.fromJson(j['meta'] as Map<String, dynamic>? ?? {}),
      order: (j['order'] as List<dynamic>? ?? []).cast<String>(),
      rawHeroes: rawHeroes,
    );
  }

  HeroGraph? hero(String codename) {
    if (_heroCache.containsKey(codename)) return _heroCache[codename];
    final raw = _rawHeroes[codename];
    if (raw == null) return null;
    final graph = HeroGraph.fromJson(codename, raw);
    _heroCache[codename] = graph;
    return graph;
  }

  List<HeroEntry> get heroList => order
      .map((code) {
        final raw = _rawHeroes[code];
        final name = raw?['public_name'] as String? ?? code;
        return HeroEntry(codename: code, publicName: name);
      })
      .toList();

  bool containsHero(String codename) => _rawHeroes.containsKey(codename);
}

class HeroEntry {
  final String codename;
  final String publicName;

  const HeroEntry({required this.codename, required this.publicName});
}
