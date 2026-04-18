import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../theme/app_text_styles.dart';
import 'hero_picker.dart';
import 'view_mode_toggle.dart';

class NydusAppBar extends StatelessWidget implements PreferredSizeWidget {
  const NydusAppBar({super.key});

  @override
  Size get preferredSize => const Size.fromHeight(44);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 44,
      decoration: const BoxDecoration(
        color: AppColors.bgElev,
        border: Border(bottom: BorderSide(color: AppColors.border)),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        children: [
          // Logo
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Nydus', style: AppTextStyles.appTitle),
              Text('the Deadlock knowledge graph',
                  style: AppTextStyles.appSubtitle),
            ],
          ),
          const Spacer(),
          // Hero picker
          const HeroPicker(),
          const SizedBox(width: 12),
          // View mode toggle
          const ViewModeToggle(),
        ],
      ),
    );
  }
}
