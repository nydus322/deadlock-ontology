import 'package:flutter/material.dart';

class AppColors {
  // Backgrounds
  static const bg      = Color(0xFF12100E);
  static const bgElev  = Color(0xFF1A1712);
  static const bgElev2 = Color(0xFF231D17);

  // Borders
  static const border  = Color(0xFF3B2F23);

  // Foreground
  static const fg      = Color(0xFFF0E6D8);
  static const fgMuted = Color(0xFFA3907A);
  static const fgSoft  = Color(0xFF60503F);

  // Accent
  static const accent      = Color(0xFFD89B4A);
  static const accentWarm  = Color(0xFFE8743A);
  static const accentDeep  = Color(0xFF7A1F1A);

  // Category palette
  static const catCooldown = Color(0xFF5B9BD5);
  static const catDamage   = Color(0xFFE05C5C);
  static const catDuration = Color(0xFF4DBFC4);
  static const catRange    = Color(0xFF4DA6FF);
  static const catSpeed    = Color(0xFFF5A623);
  static const catHealing  = Color(0xFF4FC24F);
  static const catCharges  = Color(0xFF8A9BB0);
  static const catStack    = Color(0xFF9B6DFF);
  static const catWeapon   = Color(0xFFE8943A);
  static const catStat     = Color(0xFFC084FC);
  static const catUnknown  = Color(0xFF444444);

  // Stat families
  static const statSpirit   = Color(0xFF9B6DFF);
  static const statWeapon   = Color(0xFFF5A623);
  static const statVitality = Color(0xFF4FC24F);
  static const statNeutral  = Color(0xFF8A9BB0);

  // Node class colors
  static const classHero             = Color(0xFFFF7B72);
  static const classAbility          = Color(0xFFFFA657);
  static const classPropertyCategory = Color(0xFFC084FC);
  static const classStat             = Color(0xFF9B6DFF);
  static const classSlot             = Color(0xFF79C0FF);
  static const classScaleFunction    = Color(0xFF56D4DD);
  static const classModifierValue    = Color(0xFFD2A8FF);
  static const classAbilityProperty  = Color(0xFF6E7681);
  static const classAbilityUpgrade   = Color(0xFF484F58);
  static const classStage            = Color(0xFF8B949E);
  static const classBlankNode        = Color(0xFF30363D);
  static const classResource         = Color(0xFF8B949E);

  static const _nodeClassColors = <String, Color>{
    'Hero':             classHero,
    'Ability':          classAbility,
    'PropertyCategory': classPropertyCategory,
    'Stat':             classStat,
    'Slot':             classSlot,
    'ScaleFunction':    classScaleFunction,
    'ModifierValue':    classModifierValue,
    'AbilityProperty':  classAbilityProperty,
    'AbilityUpgrade':   classAbilityUpgrade,
    'Stage':            classStage,
    'BlankNode':        classBlankNode,
    'Resource':         classResource,
  };

  static Color forNodeClass(String cls) =>
      _nodeClassColors[cls] ?? classResource;
}
