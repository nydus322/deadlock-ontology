import 'package:flutter/material.dart';
import 'app_colors.dart';

class AppTextStyles {
  // Cinzel serif — used for hero names and ability names
  static const String _cinzel = 'Cinzel';
  // Fira Code monospace — used for stat values, IRIs, code
  static const String _firaCode = 'Fira Code';

  static const heroName = TextStyle(
    fontFamily: _cinzel,
    fontSize: 48,
    fontWeight: FontWeight.w600,
    letterSpacing: 2.88, // 0.06em @ 48px
    color: AppColors.fg,
    height: 1.1,
  );

  static const abilityName = TextStyle(
    fontFamily: _cinzel,
    fontSize: 18,
    fontWeight: FontWeight.w600,
    letterSpacing: 0.36, // 0.02em @ 18px
    color: AppColors.fg,
    height: 1.3,
  );

  static const slotLabel = TextStyle(
    fontSize: 10,
    fontWeight: FontWeight.w600,
    letterSpacing: 2.4, // 0.24em @ 10px
    color: AppColors.fgMuted,
    height: 1.4,
  );

  static const statLabel = TextStyle(
    fontSize: 12,
    color: AppColors.fgMuted,
    letterSpacing: 0.2,
    height: 1.4,
  );

  static const statValue = TextStyle(
    fontFamily: _firaCode,
    fontSize: 12,
    color: AppColors.fg,
    height: 1.4,
  );

  static const scalesWith = TextStyle(
    fontSize: 10,
    color: AppColors.fgSoft,
    letterSpacing: 0.1,
  );

  static const sectionHeading = TextStyle(
    fontSize: 10,
    fontWeight: FontWeight.w600,
    letterSpacing: 2.8, // 0.28em @ 10px
    color: AppColors.fgMuted,
    height: 1.4,
  );

  static const tagChip = TextStyle(
    fontSize: 11,
    fontWeight: FontWeight.w500,
    letterSpacing: 0.5,
    color: AppColors.fg,
  );

  static const tierLabel = TextStyle(
    fontFamily: _firaCode,
    fontSize: 10,
    fontWeight: FontWeight.w700,
    color: AppColors.fgMuted,
  );

  static const tierValue = TextStyle(
    fontFamily: _firaCode,
    fontSize: 11,
    fontWeight: FontWeight.w700,
    color: AppColors.fg,
  );

  static const tierProp = TextStyle(
    fontSize: 9,
    color: AppColors.fgSoft,
    letterSpacing: 0.1,
  );

  static const appTitle = TextStyle(
    fontFamily: _firaCode,
    fontSize: 15,
    fontWeight: FontWeight.w700,
    color: AppColors.fg,
    letterSpacing: 0.5,
  );

  static const appSubtitle = TextStyle(
    fontSize: 11,
    color: AppColors.fgSoft,
    letterSpacing: 0.2,
  );

  static const iriCode = TextStyle(
    fontFamily: _firaCode,
    fontSize: 11,
    color: AppColors.fgMuted,
  );
}
