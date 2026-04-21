import 'package:flutter/material.dart';
import 'theme/app_theme.dart';
import 'widgets/shell/app_shell.dart';

class NydusApp extends StatelessWidget {
  const NydusApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Nydus',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: const AppShell(),
    );
  }
}
