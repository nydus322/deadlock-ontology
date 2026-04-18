import 'package:flutter_test/flutter_test.dart';
import 'package:nydus_flutter/data/graph/force_layout.dart';
import 'package:nydus_flutter/data/graph/hierarchical_layout.dart';

const _center = Offset(400, 300);

List<({String id, String primaryClass})> _specs(List<String> ids,
    [String cls = 'Resource']) {
  return ids.map((id) => (id: id, primaryClass: cls)).toList();
}

void main() {
  group('HierarchicalLayout.compute — basic BFS levels', () {
    // Hero → Slot → Ability (3-level chain)
    final specs = [
      (id: 'hero', primaryClass: 'Hero'),
      (id: 'slot1', primaryClass: 'Slot'),
      (id: 'ab1', primaryClass: 'Ability'),
    ];
    final edges = [
      ForceEdge(id: 'e1', source: 'hero', label: 'hasSlot', target: 'slot1'),
      ForceEdge(id: 'e2', source: 'slot1', label: 'filledBy', target: 'ab1'),
    ];

    test('returns a node for every spec', () {
      final result = HierarchicalLayout.compute(
        nodeSpecs: specs, edges: edges, rootId: 'hero', center: _center,
      );
      expect(result.nodes.length, 3);
    });

    test('root is at the topmost y position', () {
      final result = HierarchicalLayout.compute(
        nodeSpecs: specs, edges: edges, rootId: 'hero', center: _center,
      );
      final byId = {for (final n in result.nodes) n.id: n};
      expect(byId['hero']!.position.dy,
          lessThan(byId['slot1']!.position.dy));
      expect(byId['slot1']!.position.dy,
          lessThan(byId['ab1']!.position.dy));
    });

    test('all nodes are pinned', () {
      final result = HierarchicalLayout.compute(
        nodeSpecs: specs, edges: edges, rootId: 'hero', center: _center,
      );
      for (final n in result.nodes) {
        expect(n.pinned, isTrue, reason: '${n.id} should be pinned');
      }
    });

    test('all nodes have zero velocity', () {
      final result = HierarchicalLayout.compute(
        nodeSpecs: specs, edges: edges, rootId: 'hero', center: _center,
      );
      for (final n in result.nodes) {
        expect(n.velocity, Offset.zero, reason: '${n.id} velocity should be zero');
      }
    });
  });

  group('HierarchicalLayout.compute — horizontal distribution', () {
    // Hero with two slots at the same level — they should have different x coords.
    final specs = [
      (id: 'hero', primaryClass: 'Hero'),
      (id: 's1', primaryClass: 'Slot'),
      (id: 's2', primaryClass: 'Slot'),
    ];
    final edges = [
      ForceEdge(id: 'e1', source: 'hero', label: 'hasSlot', target: 's1'),
      ForceEdge(id: 'e2', source: 'hero', label: 'hasSlot', target: 's2'),
    ];

    test('two sibling slots have different x positions', () {
      final result = HierarchicalLayout.compute(
        nodeSpecs: specs, edges: edges, rootId: 'hero', center: _center,
      );
      final byId = {for (final n in result.nodes) n.id: n};
      expect(byId['s1']!.position.dx,
          isNot(closeTo(byId['s2']!.position.dx, 1.0)));
    });

    test('two sibling slots share the same y position', () {
      final result = HierarchicalLayout.compute(
        nodeSpecs: specs, edges: edges, rootId: 'hero', center: _center,
      );
      final byId = {for (final n in result.nodes) n.id: n};
      expect(byId['s1']!.position.dy,
          closeTo(byId['s2']!.position.dy, 0.5));
    });
  });

  group('HierarchicalLayout.compute — single node', () {
    test('single root node is placed at center', () {
      final specs = [(id: 'hero', primaryClass: 'Hero')];
      final result = HierarchicalLayout.compute(
        nodeSpecs: specs, edges: [], rootId: 'hero', center: _center,
      );
      expect(result.nodes.length, 1);
      expect(result.nodes.first.position.dx, closeTo(_center.dx, 0.5));
      expect(result.nodes.first.position.dy, closeTo(_center.dy, 0.5));
    });
  });

  group('HierarchicalLayout.compute — orphan nodes', () {
    // A node with no edges to the root is placed below the reachable levels.
    final specs = [
      (id: 'hero', primaryClass: 'Hero'),
      (id: 'orphan', primaryClass: 'Resource'),
    ];

    test('orphan node is placed below the hero (max level + 1)', () {
      final result = HierarchicalLayout.compute(
        nodeSpecs: specs, edges: [], rootId: 'hero', center: _center,
      );
      final byId = {for (final n in result.nodes) n.id: n};
      expect(byId['orphan']!.position.dy,
          greaterThan(byId['hero']!.position.dy));
    });
  });

  group('HierarchicalLayout.compute — missing root', () {
    test('handles missing rootId gracefully (no crash)', () {
      final specs = _specs(['a', 'b']);
      final edges = [
        ForceEdge(id: 'e1', source: 'a', label: 'rel', target: 'b'),
      ];
      final result = HierarchicalLayout.compute(
        nodeSpecs: specs, edges: edges, rootId: 'nonexistent', center: _center,
      );
      // Both nodes should still be returned (as orphans).
      expect(result.nodes.length, 2);
    });
  });

  group('HierarchicalLayout.compute — group padding', () {
    // Two slots with separate abilities: the gap between the two ability groups
    // should be wider than the gap between siblings within the same group.
    final specs = [
      (id: 'hero', primaryClass: 'Hero'),
      (id: 's1', primaryClass: 'Slot'),
      (id: 's2', primaryClass: 'Slot'),
      (id: 'ab1', primaryClass: 'Ability'),
      (id: 'ab2', primaryClass: 'Ability'),
    ];
    final edges = [
      ForceEdge(id: 'e1', source: 'hero', label: 'hasSlot', target: 's1'),
      ForceEdge(id: 'e2', source: 'hero', label: 'hasSlot', target: 's2'),
      ForceEdge(id: 'e3', source: 's1', label: 'filledBy', target: 'ab1'),
      ForceEdge(id: 'e4', source: 's2', label: 'filledBy', target: 'ab2'),
    ];

    test('group padding: ab1/ab2 gap >= nodeSpacing + groupPadding', () {
      final result = HierarchicalLayout.compute(
        nodeSpecs: specs, edges: edges, rootId: 'hero', center: _center,
      );
      final byId = {for (final n in result.nodes) n.id: n};
      final gap = (byId['ab1']!.position.dx - byId['ab2']!.position.dx).abs();
      expect(gap,
          greaterThanOrEqualTo(
              HierarchicalLayout.nodeSpacing + HierarchicalLayout.groupPadding - 1));
    });
  });
}
