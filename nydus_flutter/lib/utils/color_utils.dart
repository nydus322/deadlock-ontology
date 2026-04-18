import 'package:flutter/material.dart';

extension ColorAlpha on Color {
  Color withAlpha20() => withValues(alpha: 0.2);
  Color withAlpha10() => withValues(alpha: 0.1);
}
