import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/graph/force_layout.dart';
import '../../data/graph/hierarchical_layout.dart';
import '../../data/models/graph_elements.dart';
import '../../state/app_providers.dart';
import '../../state/graph_notifier.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_theme.dart';
import 'graph_painter.dart';

const _canvasWidth  = 3200.0;
const _canvasHeight = 2000.0;
const _canvasCenter = Offset(_canvasWidth / 2, _canvasHeight / 2);

class GraphCanvas extends ConsumerStatefulWidget {
  const GraphCanvas({super.key});

  @override
  ConsumerState<GraphCanvas> createState() => _GraphCanvasState();
}

class _GraphCanvasState extends ConsumerState<GraphCanvas> {
  List<ForceNode> _nodes = [];
  List<ForceEdge> _edges = [];

  final _transform = TransformationController();

  // Cache keys — rebuild layout only when these change.
  String?      _lastHeroCode;
  Set<String>? _lastClassFilter;
  Set<String>? _lastEdgeFilter;
  bool?        _lastKitMode;

  // Pointer-down state for tap detection.
  Offset?   _pointerDownLocal;
  DateTime? _pointerDownTime;

  // Hovered edge id.
  String? _hoveredEdgeId;

  @override
  void dispose() {
    _transform.dispose();
    super.dispose();
  }

  // ---- Layout --------------------------------------------------------------

  void _rebuildLayout(
    List<GraphNode>  synthNodes,
    List<GraphEdge>  synthEdges,
    Set<String>      visibleIds,
    Set<String>      edgeFilter,
    String           heroCode,
    String           rootId,
  ) {
    final nodeSpecs = synthNodes
        .where((n) => visibleIds.contains(n.data.id))
        .map((n) => (id: n.data.id, primaryClass: n.data.primaryClass))
        .toList();

    final forceEdges = synthEdges
        .where((e) =>
            visibleIds.contains(e.data.source) &&
            visibleIds.contains(e.data.target) &&
            (edgeFilter.contains(e.data.label) ||
             edgeFilter.contains(e.data.classes ?? '')))
        .map((e) => ForceEdge(
              id:      e.data.id,
              source:  e.data.source,
              target:  e.data.target,
              label:   e.data.label,
              classes: e.data.classes ?? '',
            ))
        .toList();

    final result = HierarchicalLayout.compute(
      nodeSpecs: nodeSpecs,
      edges:     forceEdges,
      rootId:    rootId,
      center:    _canvasCenter,
    );

    _nodes = result.nodes;
    _edges = result.edges;
    _lastHeroCode    = heroCode;
    _lastClassFilter = Set.from(edgeFilter);   // reused as combined key
    _lastEdgeFilter  = Set.from(edgeFilter);
    _lastKitMode     = null; // reset — will be set below by caller

    // Fit viewport after the frame is rendered.
    WidgetsBinding.instance.addPostFrameCallback((_) => _fitToView());
  }

  void _fitToView() {
    if (!mounted) return;
    final box = context.findRenderObject() as RenderBox?;
    if (box == null) return;
    final size  = box.size;
    final scaleX = size.width  / _canvasWidth;
    final scaleY = size.height / _canvasHeight;
    final scale  = (scaleX < scaleY ? scaleX : scaleY) * 0.88;
    final tx = (size.width  - _canvasWidth  * scale) / 2;
    final ty = (size.height - _canvasHeight * scale) / 2;
    _transform.value = Matrix4.diagonal3Values(scale, scale, 1.0)
      ..setTranslationRaw(tx, ty, 0.0);
  }

  // ---- Interaction ---------------------------------------------------------

  void _onPointerDown(PointerDownEvent e) {
    _pointerDownLocal = e.localPosition;
    _pointerDownTime  = DateTime.now();
  }

  void _onPointerUp(PointerUpEvent e) {
    final down = _pointerDownLocal;
    final time = _pointerDownTime;
    if (down == null || time == null) return;
    if (DateTime.now().difference(time).inMilliseconds < 350 &&
        (e.localPosition - down).distance < 12) {
      _handleTap(e.localPosition);
    }
    _pointerDownLocal = null;
    _pointerDownTime  = null;
  }

  void _handleTap(Offset localPos) {
    final inv    = _transform.value.clone()..invert();
    final gPos   = MatrixUtils.transformPoint(inv, localPos);
    ForceNode? hit;
    double best = double.infinity;
    for (final n in _nodes) {
      final d = (n.position - gPos).distance;
      if (d <= n.radius + 6 && d < best) { hit = n; best = d; }
    }
    ref.read(graphNotifierProvider.notifier).selectNode(hit?.id);
  }

  void _onPointerHover(PointerEvent e) {
    final inv  = _transform.value.clone()..invert();
    final gPos = MatrixUtils.transformPoint(inv, e.localPosition);
    String? nearest;
    double  nearDist = 14.0;
    // Build a node-position lookup for edge midpoints.
    final posById = <String, Offset>{for (final n in _nodes) n.id: n.position};
    for (final edge in _edges) {
      final s = posById[edge.source];
      final t = posById[edge.target];
      if (s == null || t == null) continue;
      final d = ((s + t) / 2 - gPos).distance;
      if (d < nearDist) { nearDist = d; nearest = edge.id; }
    }
    if (nearest != _hoveredEdgeId) setState(() => _hoveredEdgeId = nearest);
  }

  // ---- Visible node set ----------------------------------------------------

  Set<String> _visibleIds(
    List<GraphNode> nodes,
    GraphState      gs,
    Set<String>     kitIds,
  ) {
    return {
      for (final n in nodes)
        if (gs.classFilter.contains(n.data.primaryClass) &&
            (!gs.kitMode || kitIds.contains(n.data.id)))
          n.data.id,
    };
  }

  // ---- Build ---------------------------------------------------------------

  @override
  Widget build(BuildContext context) {
    final synthGraph = ref.watch(synthesizedGraphProvider);
    final graphState = ref.watch(graphNotifierProvider);
    final kitIds     = ref.watch(kitNodeIdsProvider);
    final heroCode   = ref.watch(currentHeroCodeProvider);
    final accent     = Theme.of(context).extension<HeroAccentTheme>()?.accent
                       ?? AppColors.accentWarm;

    if (synthGraph == null) {
      return const Center(
          child: CircularProgressIndicator(color: AppColors.accent));
    }

    final visibleIds = _visibleIds(synthGraph.nodes, graphState, kitIds);

    // Find the Hero node id to use as BFS root.
    final rootId = synthGraph.nodes
        .where((n) => n.data.classList.contains('Hero'))
        .map((n) => n.data.id)
        .firstOrNull ?? '';

    // Rebuild when hero, filters, or kit mode change.
    final needsRebuild = _lastHeroCode   != heroCode        ||
                         _lastKitMode    != graphState.kitMode  ||
                         _lastClassFilter != graphState.classFilter ||
                         _lastEdgeFilter  != graphState.edgeFilter  ||
                         _nodes.isEmpty;

    if (needsRebuild) {
      _rebuildLayout(
        synthGraph.nodes, synthGraph.edges,
        visibleIds, graphState.edgeFilter,
        heroCode, rootId,
      );
      _lastKitMode     = graphState.kitMode;
      _lastClassFilter = Set.from(graphState.classFilter);
      _lastEdgeFilter  = Set.from(graphState.edgeFilter);
    }

    final nodeDataById = <String, NodeData>{
      for (final n in synthGraph.nodes) n.data.id: n.data,
    };
    final visNodes = _nodes.where((n) => visibleIds.contains(n.id)).toList();
    final visEdges = _edges.where((e) =>
        visibleIds.contains(e.source) && visibleIds.contains(e.target)).toList();

    return Listener(
      onPointerDown:  _onPointerDown,
      onPointerUp:    _onPointerUp,
      onPointerHover: _onPointerHover,
      behavior: HitTestBehavior.opaque,
      child: InteractiveViewer(
        transformationController: _transform,
        minScale: 0.03,
        maxScale: 5.0,
        constrained: false,
        child: SizedBox(
          width:  _canvasWidth,
          height: _canvasHeight,
          child: RepaintBoundary(
            child: CustomPaint(
              painter: GraphPainter(
                nodes:          visNodes,
                edges:          visEdges,
                nodeDataById:   nodeDataById,
                accent:         accent,
                selectedNodeId: graphState.selectedNodeId,
                hoveredEdgeId:  _hoveredEdgeId,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
