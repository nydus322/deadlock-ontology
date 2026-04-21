import 'package:flutter_test/flutter_test.dart';
import 'package:nydus_flutter/data/extractors/topology.dart';
import 'package:nydus_flutter/data/models/bundle_data.dart';
import 'package:nydus_flutter/data/models/graph_elements.dart';

// Helpers -----------------------------------------------------------------------

GraphNode _node(String id, String classes, {String label = ''}) => GraphNode(
      data: NodeData(
        id: id,
        label: label.isNotEmpty ? label : id,
        classes: classes,
      ),
    );

GraphEdge _edge(String id, String src, String tgt, String label,
        {String? classes}) =>
    GraphEdge(
      data: EdgeData(
        id: id,
        source: src,
        target: tgt,
        label: label,
        classes: classes,
      ),
    );

const _meta = GraphMeta(source: 'test', nodeCount: 0, edgeCount: 0);

/// Build a minimal HeroGraph with the standard blank-node pattern:
///   hero --hasAbilityInSlot--> bn
///   bn   --slot-->  slot
///   bn   --ability--> ability
HeroGraph _minimalGraph() {
  return HeroGraph(
    codename: 'test_hero',
    publicName: 'Test Hero',
    heroId: 0,
    meta: _meta,
    nodes: [
      _node('hero', 'Hero', label: 'Test Hero'),
      _node('bn1', 'BlankNode', label: '_:bn1'),
      _node('slot1', 'Slot', label: 'Primary'),
      _node('ability1', 'Ability', label: 'Fireball'),
    ],
    edges: [
      _edge('e1', 'hero', 'bn1', 'hasAbilityInSlot'),
      _edge('e2', 'bn1', 'slot1', 'slot'),
      _edge('e3', 'bn1', 'ability1', 'ability'),
    ],
  );
}

// Tests -------------------------------------------------------------------------

void main() {
  group('TopologyExtractor.synthesize — blank node collapsing', () {
    test('blank node is removed from output nodes', () {
      final result = TopologyExtractor.synthesize(_minimalGraph());
      final ids = result.nodes.map((n) => n.data.id).toSet();
      expect(ids.contains('bn1'), isFalse);
    });

    test('hero, slot, ability are retained', () {
      final result = TopologyExtractor.synthesize(_minimalGraph());
      final ids = result.nodes.map((n) => n.data.id).toSet();
      expect(ids.containsAll({'hero', 'slot1', 'ability1'}), isTrue);
    });

    test('original blank-node edges are removed', () {
      final result = TopologyExtractor.synthesize(_minimalGraph());
      for (final e in result.edges) {
        expect(e.data.source, isNot('bn1'));
        expect(e.data.target, isNot('bn1'));
      }
    });

    test('synthetic hasSlot edge is added (hero → slot)', () {
      final result = TopologyExtractor.synthesize(_minimalGraph());
      final hasSlotEdges = result.edges.where((e) =>
          e.data.source == 'hero' &&
          e.data.target == 'slot1' &&
          (e.data.classes?.contains('hasSlot') ?? false));
      expect(hasSlotEdges, isNotEmpty);
    });

    test('synthetic filledBy edge is added (slot → ability)', () {
      final result = TopologyExtractor.synthesize(_minimalGraph());
      final filledByEdges = result.edges.where((e) =>
          e.data.source == 'slot1' &&
          e.data.target == 'ability1' &&
          (e.data.classes?.contains('filledBy') ?? false));
      expect(filledByEdges, isNotEmpty);
    });

    test('synthetic edges are marked as synthetic', () {
      final result = TopologyExtractor.synthesize(_minimalGraph());
      final synEdges = result.edges
          .where((e) => e.data.classes?.contains('synthetic') ?? false);
      expect(synEdges.length, 2); // one hasSlot + one filledBy
    });
  });

  group('TopologyExtractor.synthesize — no hero node', () {
    test('returns original graph unchanged when no hero node exists', () {
      final graph = HeroGraph(
        codename: 'x',
        publicName: 'X',
        heroId: 0,
        meta: _meta,
        nodes: [_node('slot1', 'Slot')],
        edges: [],
      );
      final result = TopologyExtractor.synthesize(graph);
      expect(result.nodes.length, 1);
      expect(result.edges, isEmpty);
    });
  });

  group('TopologyExtractor.synthesize — multiple slots', () {
    test('produces two hasSlot and two filledBy edges for two slots', () {
      final graph = HeroGraph(
        codename: 'h',
        publicName: 'H',
        heroId: 0,
        meta: _meta,
        nodes: [
          _node('hero', 'Hero'),
          _node('bn1', 'BlankNode'),
          _node('slot1', 'Slot'),
          _node('ab1', 'Ability'),
          _node('bn2', 'BlankNode'),
          _node('slot2', 'Slot'),
          _node('ab2', 'Ability'),
        ],
        edges: [
          _edge('e1', 'hero', 'bn1', 'hasAbilityInSlot'),
          _edge('e2', 'bn1', 'slot1', 'slot'),
          _edge('e3', 'bn1', 'ab1', 'ability'),
          _edge('e4', 'hero', 'bn2', 'hasAbilityInSlot'),
          _edge('e5', 'bn2', 'slot2', 'slot'),
          _edge('e6', 'bn2', 'ab2', 'ability'),
        ],
      );
      final result = TopologyExtractor.synthesize(graph);
      final synEdges = result.edges
          .where((e) => e.data.classes?.contains('synthetic') ?? false)
          .toList();
      expect(synEdges.length, 4); // 2 hasSlot + 2 filledBy
    });
  });

  group('TopologyExtractor.synthesize — unrelated edges preserved', () {
    test('edges not touching blank nodes are kept', () {
      final graph = HeroGraph(
        codename: 'h',
        publicName: 'H',
        heroId: 0,
        meta: _meta,
        nodes: [
          _node('hero', 'Hero'),
          _node('bn1', 'BlankNode'),
          _node('slot1', 'Slot'),
          _node('ab1', 'Ability'),
          _node('stat1', 'Stat'),
        ],
        edges: [
          _edge('e1', 'hero', 'bn1', 'hasAbilityInSlot'),
          _edge('e2', 'bn1', 'slot1', 'slot'),
          _edge('e3', 'bn1', 'ab1', 'ability'),
          _edge('prop', 'ab1', 'stat1', 'hasProperty'),
        ],
      );
      final result = TopologyExtractor.synthesize(graph);
      final propEdge = result.edges.where((e) => e.data.id == 'prop');
      expect(propEdge, isNotEmpty);
    });
  });
}
