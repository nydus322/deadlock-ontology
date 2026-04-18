const _classOrder = [
  'Hero', 'Ability', 'AbilityProperty', 'AbilityUpgrade',
  'PropertyCategory', 'Stat', 'Slot', 'ScaleFunction', 'ModifierValue',
  'Stage', 'BlankNode', 'Resource',
];

class NodeData {
  final String id;
  final String? shortId;
  final String? iri;
  final String label;
  final String classes;
  final Map<String, dynamic>? properties;

  const NodeData({
    required this.id,
    this.shortId,
    this.iri,
    required this.label,
    required this.classes,
    this.properties,
  });

  factory NodeData.fromJson(Map<String, dynamic> j) => NodeData(
        id: j['id'] as String? ?? '',
        shortId: j['shortId'] as String?,
        iri: j['iri'] as String?,
        label: j['label'] as String? ?? '',
        classes: j['classes'] as String? ?? '',
        properties: j['properties'] as Map<String, dynamic>?,
      );

  List<String> get classList =>
      classes.split(RegExp(r'\s+')).where((s) => s.isNotEmpty).toList();

  String get primaryClass {
    final list = classList;
    for (final c in _classOrder) {
      if (list.contains(c)) return c;
    }
    return list.isNotEmpty ? list.first : 'Resource';
  }
}

class GraphNode {
  final NodeData data;

  const GraphNode({required this.data});

  factory GraphNode.fromJson(Map<String, dynamic> j) =>
      GraphNode(data: NodeData.fromJson(j['data'] as Map<String, dynamic>? ?? {}));
}

class EdgeData {
  final String id;
  final String source;
  final String target;
  final String label;
  final String? classes;

  const EdgeData({
    required this.id,
    required this.source,
    required this.target,
    required this.label,
    this.classes,
  });

  factory EdgeData.fromJson(Map<String, dynamic> j) => EdgeData(
        id: j['id'] as String? ?? '',
        source: j['source'] as String? ?? '',
        target: j['target'] as String? ?? '',
        label: j['label'] as String? ?? '',
        classes: j['classes'] as String?,
      );
}

class GraphEdge {
  final EdgeData data;

  const GraphEdge({required this.data});

  factory GraphEdge.fromJson(Map<String, dynamic> j) =>
      GraphEdge(data: EdgeData.fromJson(j['data'] as Map<String, dynamic>? ?? {}));
}
