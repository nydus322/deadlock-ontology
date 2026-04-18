import 'dart:math' as math;
import 'dart:ui' show Offset;

/// A single node in the force simulation.
class ForceNode {
  final String id;
  Offset position;
  Offset velocity;
  final double radius;
  bool pinned;

  ForceNode({
    required this.id,
    required this.position,
    this.velocity = Offset.zero,
    required this.radius,
    this.pinned = false,
  });
}

/// An edge in the force simulation.
class ForceEdge {
  final String id;
  final String source;
  final String target;
  final String label;
  final String classes;

  const ForceEdge({
    required this.id,
    required this.source,
    required this.target,
    required this.label,
    this.classes = '',
  });
}

// Node radii matching CLASS_SIZE / 2 from nydus.html line 11058.
const _classRadius = <String, double>{
  'Hero':             48,
  'Ability':          34,
  'PropertyCategory': 18,
  'Stat':             17,
  'Slot':             14,
  'ScaleFunction':    15,
  'ModifierValue':    13,
  'AbilityProperty':  16,
  'AbilityUpgrade':   12,
  'Stage':            11,
  'BlankNode':         8,
  'Resource':         10,
};

double radiusForClass(String cls) => _classRadius[cls] ?? 12;

/// Spring/repulsion force-directed layout.
///
/// Forces applied each tick:
///  - Repulsion : every pair of nodes pushes apart (Coulomb-like)
///  - Spring    : every edge pulls its endpoints toward _springLen apart
///  - Gravity   : weak pull toward [center] prevents unbounded drift
///  - Damping   : velocity decays so the system eventually settles
class ForceLayout {
  final List<ForceNode> nodes;
  final List<ForceEdge> edges;
  final Offset center;

  static const double _repulsion   = 6000;
  static const double _springLen   = 110;
  static const double _springK     = 0.04;
  static const double _gravity     = 0.006;
  static const double _damping     = 0.82;
  static const double _maxVelocity = 180;
  static const double _minEnergy   = 0.08;

  double _energy = double.infinity;
  int _stepCount = 0;

  ForceLayout({
    required this.nodes,
    required this.edges,
    required this.center,
  });

  bool get settled => _energy < _minEnergy || _stepCount > 600;
  double get energy => _energy;

  /// Advance one tick (~16 ms at 60 fps).
  void step() {
    if (settled) return;
    final n = nodes.length;
    if (n == 0) return;

    final posById = <String, int>{
      for (var i = 0; i < n; i++) nodes[i].id: i,
    };

    final forces = List.generate(n, (_) => Offset.zero);

    // 1. Repulsion between every pair
    for (var i = 0; i < n; i++) {
      for (var j = i + 1; j < n; j++) {
        final delta = nodes[i].position - nodes[j].position;
        final dist = delta.distance.clamp(1.0, 1000.0);
        final mag = _repulsion / (dist * dist);
        final dir = delta / dist;
        forces[i] = forces[i] + dir * mag;
        forces[j] = forces[j] - dir * mag;
      }
    }

    // 2. Spring attraction along edges
    for (final edge in edges) {
      final si = posById[edge.source];
      final ti = posById[edge.target];
      if (si == null || ti == null) continue;
      final delta = nodes[ti].position - nodes[si].position;
      final dist = delta.distance.clamp(1.0, 2000.0);
      final stretch = dist - _springLen;
      final mag = _springK * stretch;
      final dir = delta / dist;
      forces[si] = forces[si] + dir * mag;
      forces[ti] = forces[ti] - dir * mag;
    }

    // 3. Gravity toward center
    for (var i = 0; i < n; i++) {
      final toCenter = center - nodes[i].position;
      forces[i] = forces[i] + toCenter * _gravity;
    }

    // 4. Integrate
    double totalEnergy = 0;
    for (var i = 0; i < n; i++) {
      if (nodes[i].pinned) continue;
      var vel = (nodes[i].velocity + forces[i]) * _damping;
      final speed = vel.distance;
      if (speed > _maxVelocity) vel = vel / speed * _maxVelocity;
      nodes[i].velocity = vel;
      nodes[i].position = nodes[i].position + vel;
      totalEnergy += speed * speed;
    }

    _energy = totalEnergy / n;
    _stepCount++;
  }

  /// Build a fresh layout with nodes placed in a Fibonacci spiral.
  static ForceLayout buildFrom({
    required List<({String id, String primaryClass})> nodeSpecs,
    required List<ForceEdge> edges,
    required Offset center,
    int seed = 42,
  }) {
    final rng = math.Random(seed);
    const phi = 2.3999632; // golden angle ≈ 2π / φ²
    final nodes = <ForceNode>[];

    for (var i = 0; i < nodeSpecs.length; i++) {
      final spec = nodeSpecs[i];
      final angle = phi * i;
      final r = 70 * math.sqrt(i.toDouble() + 1);
      final jitter = Offset(
        (rng.nextDouble() - 0.5) * 16,
        (rng.nextDouble() - 0.5) * 16,
      );
      nodes.add(ForceNode(
        id: spec.id,
        position: center +
            Offset(r * math.cos(angle), r * math.sin(angle)) +
            jitter,
        radius: radiusForClass(spec.primaryClass),
      ));
    }

    return ForceLayout(nodes: nodes, edges: edges, center: center);
  }
}
