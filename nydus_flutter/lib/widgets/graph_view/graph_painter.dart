import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../../data/graph/force_layout.dart';
import '../../data/models/graph_elements.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';

// Edge colors by predicate — mirrors the Cytoscape stylesheet.
Color _edgeColor(String label, Color accent) {
  return switch (label) {
    'hasSlot' || 'filledBy' => accent,
    'hasProperty'           => AppColors.fgSoft,
    'hasUpgrade'            => AppColors.border,
    'scalesStat'            => AppColors.accent,
    'primaryCategory' ||
    'secondaryCategory'     => AppColors.catStat,
    _                       => AppColors.border,
  };
}

bool _isDashed(String label) => label == 'hasUpgrade';
bool _hasArrow(String label) => label == 'scalesStat';

/// Draws all edges then all nodes of the force layout onto a [Canvas].
class GraphPainter extends CustomPainter {
  final List<ForceNode> nodes;
  final List<ForceEdge> edges;
  final Map<String, NodeData> nodeDataById;
  final Color accent;
  final String? selectedNodeId;
  final String? hoveredEdgeId;

  const GraphPainter({
    required this.nodes,
    required this.edges,
    required this.nodeDataById,
    required this.accent,
    this.selectedNodeId,
    this.hoveredEdgeId,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final nodePos = <String, Offset>{
      for (final n in nodes) n.id: n.position,
    };

    // ---- Edges ----------------------------------------------------------
    for (final edge in edges) {
      final src = nodePos[edge.source];
      final tgt = nodePos[edge.target];
      if (src == null || tgt == null) continue;

      final isHovered = edge.id == hoveredEdgeId;
      final color = _edgeColor(edge.label, accent);
      final paint = Paint()
        ..color = isHovered ? color : color.withValues(alpha: 0.65)
        ..strokeWidth = isHovered ? 2.0 : 1.5
        ..style = PaintingStyle.stroke;

      if (_isDashed(edge.label)) {
        _drawDashedLine(canvas, src, tgt, paint);
      } else {
        canvas.drawLine(src, tgt, paint);
      }

      if (_hasArrow(edge.label)) {
        _drawArrow(canvas, src, tgt, paint);
      }

      // Edge label on hover
      if (isHovered) {
        _drawEdgeLabel(canvas, src, tgt, edge.label);
      }
    }

    // ---- Nodes ----------------------------------------------------------
    for (final node in nodes) {
      final data = nodeDataById[node.id];
      final cls = data?.primaryClass ?? 'Resource';
      final isSelected = node.id == selectedNodeId;

      _drawNode(canvas, node, cls, isSelected);

      // Node label
      if (data != null) {
        _drawNodeLabel(canvas, node.position, node.radius, data.label, cls, isSelected);
      }
    }
  }

  void _drawNode(Canvas canvas, ForceNode node, String cls, bool selected) {
    final color = AppColors.forNodeClass(cls);
    final r = node.radius;
    final pos = node.position;

    final bgPaint = Paint()
      ..color = cls == 'Hero' ? color.withValues(alpha: 0.9) : AppColors.bgElev
      ..style = PaintingStyle.fill;

    final borderPaint = Paint()
      ..color = selected ? accent : (cls == 'Ability' ? accent.withValues(alpha: 0.7) : color.withValues(alpha: 0.6))
      ..strokeWidth = selected ? 3.0 : 1.5
      ..style = PaintingStyle.stroke;

    switch (cls) {
      case 'Hero':
        canvas.drawCircle(pos, r, bgPaint);
        canvas.drawCircle(pos, r, borderPaint);
      case 'Ability':
        final rr = RRect.fromRectAndRadius(
          Rect.fromCenter(center: pos, width: r * 2, height: r * 1.4),
          const Radius.circular(6),
        );
        canvas.drawRRect(rr, bgPaint);
        canvas.drawRRect(rr, borderPaint);
      case 'Slot':
        _drawTriangle(canvas, pos, r, bgPaint, borderPaint);
      case 'Stat':
        _drawDiamond(canvas, pos, r, bgPaint, borderPaint);
      case 'AbilityUpgrade':
        final rr = RRect.fromRectAndRadius(
          Rect.fromCenter(center: pos, width: r * 2, height: r * 1.6),
          const Radius.circular(4),
        );
        canvas.drawRRect(rr, bgPaint);
        canvas.drawRRect(rr, borderPaint);
      default:
        canvas.drawCircle(pos, r, bgPaint);
        canvas.drawCircle(pos, r, borderPaint);
    }

    if (selected) {
      final glowPaint = Paint()
        ..color = accent.withValues(alpha: 0.2)
        ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 8);
      canvas.drawCircle(pos, r + 4, glowPaint);
    }
  }

  void _drawTriangle(Canvas canvas, Offset center, double r,
      Paint fill, Paint stroke) {
    final path = Path()
      ..moveTo(center.dx, center.dy - r)
      ..lineTo(center.dx + r * 0.87, center.dy + r * 0.5)
      ..lineTo(center.dx - r * 0.87, center.dy + r * 0.5)
      ..close();
    canvas.drawPath(path, fill);
    canvas.drawPath(path, stroke);
  }

  void _drawDiamond(Canvas canvas, Offset center, double r,
      Paint fill, Paint stroke) {
    final path = Path()
      ..moveTo(center.dx, center.dy - r)
      ..lineTo(center.dx + r * 0.7, center.dy)
      ..lineTo(center.dx, center.dy + r)
      ..lineTo(center.dx - r * 0.7, center.dy)
      ..close();
    canvas.drawPath(path, fill);
    canvas.drawPath(path, stroke);
  }

  void _drawNodeLabel(Canvas canvas, Offset pos, double r, String label,
      String cls, bool selected) {
    final fontSize = cls == 'Hero' ? 13.0 : cls == 'Ability' ? 11.0 : 9.0;
    final textColor = selected ? accent : AppColors.fg;

    final tp = TextPainter(
      text: TextSpan(
        text: label,
        style: TextStyle(
          fontFamily: cls == 'Hero' || cls == 'Ability' ? 'Cinzel' : null,
          fontSize: fontSize,
          color: textColor,
          fontWeight: cls == 'Hero' ? FontWeight.w600 : FontWeight.w400,
        ),
      ),
      textDirection: TextDirection.ltr,
      textAlign: TextAlign.center,
      maxLines: 2,
      ellipsis: '…',
    )..layout(maxWidth: math.max(r * 3.0, 80));

    // Draw background pill behind label
    final labelRect = Rect.fromCenter(
      center: Offset(pos.dx, pos.dy + r + 6 + tp.height / 2),
      width: tp.width + 6,
      height: tp.height + 4,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(labelRect, const Radius.circular(3)),
      Paint()..color = AppColors.bg.withValues(alpha: 0.88),
    );

    tp.paint(
      canvas,
      Offset(pos.dx - tp.width / 2, pos.dy + r + 6),
    );
  }

  void _drawEdgeLabel(Canvas canvas, Offset src, Offset tgt, String label) {
    final mid = (src + tgt) / 2;
    final tp = TextPainter(
      text: TextSpan(
        text: label,
        style: AppTextStyles.scalesWith.copyWith(
          color: AppColors.fgMuted,
          fontSize: 9,
        ),
      ),
      textDirection: TextDirection.ltr,
    )..layout();

    final bgRect = Rect.fromCenter(
      center: mid,
      width: tp.width + 6,
      height: tp.height + 4,
    );
    canvas.drawRRect(
      RRect.fromRectAndRadius(bgRect, const Radius.circular(3)),
      Paint()..color = AppColors.bg.withValues(alpha: 0.9),
    );
    tp.paint(canvas, Offset(mid.dx - tp.width / 2, mid.dy - tp.height / 2));
  }

  void _drawDashedLine(Canvas canvas, Offset src, Offset tgt, Paint paint) {
    const dashLen = 6.0;
    const gapLen = 4.0;
    final delta = tgt - src;
    final total = delta.distance;
    final dir = delta / total;
    double d = 0;
    while (d < total) {
      final start = src + dir * d;
      final end = src + dir * math.min(d + dashLen, total);
      canvas.drawLine(start, end, paint);
      d += dashLen + gapLen;
    }
  }

  void _drawArrow(Canvas canvas, Offset src, Offset tgt, Paint paint) {
    const arrowSize = 8.0;
    final delta = tgt - src;
    final angle = math.atan2(delta.dy, delta.dx);
    final arrowPaint = Paint()
      ..color = paint.color
      ..style = PaintingStyle.fill;
    final path = Path()
      ..moveTo(tgt.dx, tgt.dy)
      ..lineTo(
        tgt.dx - arrowSize * math.cos(angle - 0.4),
        tgt.dy - arrowSize * math.sin(angle - 0.4),
      )
      ..lineTo(
        tgt.dx - arrowSize * math.cos(angle + 0.4),
        tgt.dy - arrowSize * math.sin(angle + 0.4),
      )
      ..close();
    canvas.drawPath(path, arrowPaint);
  }

  @override
  bool shouldRepaint(GraphPainter old) =>
      old.nodes != nodes ||
      old.selectedNodeId != selectedNodeId ||
      old.hoveredEdgeId != hoveredEdgeId ||
      old.accent != accent;
}
