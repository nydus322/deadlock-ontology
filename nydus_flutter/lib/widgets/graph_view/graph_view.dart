import 'package:flutter/material.dart';
import 'graph_canvas.dart';
import 'graph_left_sidebar.dart';
import 'graph_right_sidebar.dart';

class GraphView extends StatelessWidget {
  const GraphView({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const GraphLeftSidebar(),
        const Expanded(child: GraphCanvas()),
        const GraphRightSidebar(),
      ],
    );
  }
}
