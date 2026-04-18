class StatEntry {
  final String key;
  final String value;

  const StatEntry({required this.key, required this.value});
}

class HeroStats {
  final List<StatEntry> core;
  final List<StatEntry> combat;

  const HeroStats({required this.core, required this.combat});
}

class HeroKitInfo {
  final String name;
  final List<String> tags;
  final HeroStats stats;

  const HeroKitInfo({
    required this.name,
    required this.tags,
    required this.stats,
  });
}

class AbilityStat {
  final String label;
  final String? value;
  final String? scalesWith;

  const AbilityStat({
    required this.label,
    this.value,
    this.scalesWith,
  });
}

class UpgradeEffect {
  final String bonus;
  final String prop;

  const UpgradeEffect({required this.bonus, required this.prop});
}

class UpgradeData {
  final String level;
  final List<UpgradeEffect> effects;

  const UpgradeData({required this.level, required this.effects});
}

class AbilityKitData {
  final String name;
  final List<AbilityStat> stats;
  final List<UpgradeData> upgrades;

  const AbilityKitData({
    required this.name,
    required this.stats,
    required this.upgrades,
  });
}

class SlotData {
  final String slotLabel;
  final String slotShort;
  final bool isAberrant;
  final AbilityKitData ability;

  const SlotData({
    required this.slotLabel,
    required this.slotShort,
    required this.isAberrant,
    required this.ability,
  });

  bool get isWeapon => slotShort == 'slot/WeaponPrimary';
}

class KitData {
  final HeroKitInfo hero;
  final List<SlotData> slots;

  const KitData({required this.hero, required this.slots});
}
