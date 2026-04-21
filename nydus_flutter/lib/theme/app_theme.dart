import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';
import 'hero_accents.dart';

// ThemeExtension carrying the per-hero dynamic accent color.
// Consumed via Theme.of(context).extension<HeroAccentTheme>()!
@immutable
class HeroAccentTheme extends ThemeExtension<HeroAccentTheme> {
  final Color accent;
  final Color accentSoft;

  const HeroAccentTheme({
    required this.accent,
    required this.accentSoft,
  });

  factory HeroAccentTheme.forHero(String codename) => HeroAccentTheme(
        accent: HeroAccents.forHero(codename),
        accentSoft: HeroAccents.softFor(codename),
      );

  @override
  HeroAccentTheme copyWith({Color? accent, Color? accentSoft}) => HeroAccentTheme(
        accent: accent ?? this.accent,
        accentSoft: accentSoft ?? this.accentSoft,
      );

  @override
  HeroAccentTheme lerp(HeroAccentTheme? other, double t) {
    if (other == null) return this;
    return HeroAccentTheme(
      accent: Color.lerp(accent, other.accent, t) ?? accent,
      accentSoft: Color.lerp(accentSoft, other.accentSoft, t) ?? accentSoft,
    );
  }
}

ThemeData buildAppTheme({String heroCodename = 'hero_inferno'}) {
  final heroAccent = HeroAccentTheme.forHero(heroCodename);

  return ThemeData(
    brightness: Brightness.dark,
    scaffoldBackgroundColor: AppColors.bg,
    colorScheme: ColorScheme.dark(
      surface: AppColors.bg,
      primary: heroAccent.accent,
      onPrimary: AppColors.fg,
      secondary: AppColors.accent,
      onSecondary: AppColors.bg,
    ),
    textTheme: GoogleFonts.latoTextTheme(ThemeData.dark().textTheme).copyWith(
      bodyMedium: const TextStyle(color: AppColors.fg, fontSize: 13),
      bodySmall: const TextStyle(color: AppColors.fgMuted, fontSize: 11),
    ),
    appBarTheme: const AppBarTheme(
      backgroundColor: AppColors.bgElev,
      foregroundColor: AppColors.fg,
      elevation: 0,
      surfaceTintColor: Colors.transparent,
    ),
    dividerColor: AppColors.border,
    extensions: [heroAccent],
  );
}
