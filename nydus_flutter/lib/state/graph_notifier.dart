import 'package:flutter_riverpod/flutter_riverpod.dart';

class GraphState {
  final Set<String> classFilter;
  final Set<String> edgeFilter;
  final Set<String> expanded;
  final bool kitMode;
  final String? selectedNodeId;

  const GraphState({
    required this.classFilter,
    required this.edgeFilter,
    required this.expanded,
    required this.kitMode,
    this.selectedNodeId,
  });

  GraphState copyWith({
    Set<String>? classFilter,
    Set<String>? edgeFilter,
    Set<String>? expanded,
    bool? kitMode,
    String? selectedNodeId,
    bool clearSelectedNode = false,
  }) {
    return GraphState(
      classFilter: classFilter ?? this.classFilter,
      edgeFilter: edgeFilter ?? this.edgeFilter,
      expanded: expanded ?? this.expanded,
      kitMode: kitMode ?? this.kitMode,
      selectedNodeId: clearSelectedNode ? null : (selectedNodeId ?? this.selectedNodeId),
    );
  }
}

class GraphNotifier extends Notifier<GraphState> {
  static const _defaultClassFilter = <String>{
    'Hero', 'Ability', 'AbilityProperty', 'AbilityUpgrade',
    'PropertyCategory', 'Stat', 'Slot', 'ScaleFunction',
  };

  static const _defaultEdgeFilter = <String>{
    'hasSlot', 'filledBy',
    'hasProperty', 'hasUpgrade', 'scalesStat',
    'primaryCategory', 'secondaryCategory',
  };

  @override
  GraphState build() => GraphState(
        classFilter: Set.from(_defaultClassFilter),
        edgeFilter: Set.from(_defaultEdgeFilter),
        expanded: {},
        kitMode: true,
      );

  void toggleClassFilter(String cls) {
    final updated = Set<String>.from(state.classFilter);
    if (updated.contains(cls)) {
      updated.remove(cls);
    } else {
      updated.add(cls);
    }
    state = state.copyWith(classFilter: updated);
  }

  void toggleEdgeFilter(String predicate) {
    final updated = Set<String>.from(state.edgeFilter);
    if (updated.contains(predicate)) {
      updated.remove(predicate);
    } else {
      updated.add(predicate);
    }
    state = state.copyWith(edgeFilter: updated);
  }

  void toggleKitMode() {
    state = state.copyWith(kitMode: !state.kitMode);
  }

  void selectNode(String? nodeId) {
    if (nodeId == null) {
      state = state.copyWith(clearSelectedNode: true);
    } else {
      state = state.copyWith(selectedNodeId: nodeId);
    }
  }

  void toggleExpanded(String nodeId) {
    final updated = Set<String>.from(state.expanded);
    if (updated.contains(nodeId)) {
      updated.remove(nodeId);
    } else {
      updated.add(nodeId);
    }
    state = state.copyWith(expanded: updated);
  }
}

final graphNotifierProvider =
    NotifierProvider<GraphNotifier, GraphState>(GraphNotifier.new);
