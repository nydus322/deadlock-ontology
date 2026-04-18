// Port of the property-formatting utility functions from nydus.html lines 11331-11513.
// All methods are stateless and static.

class PropFormatter {
  // Scale function -> player-facing name. null means suppress the badge.
  static const _scaleFunctionNames = <String, String?>{
    'scale_function_tech_damage':           'Spirit Power',
    'scale_function_tech_power':            'Spirit Power',
    'scale_function_tech_range':            'Spirit Range',
    'scale_function_tech_duration':         'Spirit Duration',
    'scale_function_tech_cooldown':         'Cooldown Reduction',
    'scale_function_weapon_damage':         'Weapon Damage',
    'scale_function_ability_weapon_damage': 'Weapon Damage',
    'scale_function_ability_charges':       'Ability Charges',
    'scale_function_multi_stats':           'Multiple Stats',
    'scale_function_single_stat':           null,
  };

  static const _modifiesPropAlias = <String, String>{
    'AbilityCooldown':              'Cooldown',
    'AbilityDuration':              'Duration',
    'AbilityCastRange':             'Cast Range',
    'AbilityCharges':               'Charges',
    'AbilityRadius':                'Radius',
    'AbilityCooldownBetweenCharge': 'Recharge Time',
    'DPS':                          'DPS',
    'HP':                           'Health',
  };

  static const _hiddenPropKeys = <String>{
    'label', 'altLabel', 'internalName', 'internalKey',
    'identifier', 'isDisabled', 'isPlayerSelectable', 'complexity',
  };

  static bool isHiddenPropKey(String k) => _hiddenPropKeys.contains(k);

  /// "Tech" -> "Spirit" substitution, matching Deadlock's player-facing copy.
  static String spiritize(String s) {
    return s
        .replaceAllMapped(RegExp(r'\bTech\b'), (_) => 'Spirit')
        .replaceAllMapped(RegExp(r'\bTech([A-Z])'), (m) => 'Spirit${m.group(1)}')
        .replaceAll(RegExp(r'\btech_'), 'spirit_');
  }

  /// camelCase -> display label, with "starting" prefix stripped.
  static String prettifyPropKey(String k) {
    String key = k.replaceFirst(RegExp(r'^starting'), '');
    if (key.isEmpty) key = k;
    final spaced = key.replaceAllMapped(
      RegExp(r'([a-z0-9])([A-Z])'),
      (m) => '${m.group(1)} ${m.group(2)}',
    );
    final titled = spaced[0].toUpperCase() + spaced.substring(1);
    return spiritize(titled);
  }

  /// Format a raw property value for display.
  static String? prettifyPropValue(String k, dynamic v) {
    if (v == null) return null;

    if (v is num) {
      if (v is int) return v.toString();
      final rounded = (v * 1000).round() / 1000;
      return rounded.toString();
    }

    if (v is! String) return v.toString();

    // Round stringified floats ("0.222222" -> "0.222")
    if (RegExp(r'^-?\d+\.\d{4,}$').hasMatch(v)) {
      final n = double.tryParse(v);
      if (n != null) {
        return ((n * 1000).round() / 1000).toString();
      }
    }

    // Strip Valve enum prefixes: EResourceType_None -> "None"
    final enumMatch = RegExp(r'^E[A-Z][A-Za-z0-9]*_(.+)$').firstMatch(v);
    if (enumMatch != null) {
      final inner = enumMatch.group(1)!;
      return inner.replaceAllMapped(
        RegExp(r'([a-z0-9])([A-Z])'),
        (m) => '${m.group(1)} ${m.group(2)}',
      );
    }

    if (k == 'scaleFunction') {
      if (_scaleFunctionNames.containsKey(v)) {
        return _scaleFunctionNames[v]; // may be null (suppress)
      }
      final stripped = v.replaceFirst(RegExp(r'^scale_function_'), '');
      return stripped.split('_').map((w) {
        if (w.isEmpty) return w;
        return w[0].toUpperCase() + w.substring(1);
      }).join(' ');
    }

    if (k == 'modifiesProperty') {
      if (_modifiesPropAlias.containsKey(v)) {
        return spiritize(_modifiesPropAlias[v]!);
      }
      // Preserve bare acronyms (DPS, HP)
      if (RegExp(r'^[A-Z0-9]+$').hasMatch(v) && v.length <= 5) return v;
      final spaced = v.replaceAllMapped(
        RegExp(r'([a-z0-9])([A-Z])'),
        (m) => '${m.group(1)} ${m.group(2)}',
      );
      return spiritize(spaced[0].toUpperCase() + spaced.substring(1));
    }

    return v;
  }

  /// Detect the unit suffix for a property label/name.
  static String unitFor(String labelOrProp) {
    if (RegExp(r'Percent$', caseSensitive: false).hasMatch(labelOrProp) ||
        RegExp(r'Percent\b', caseSensitive: false).hasMatch(labelOrProp) ||
        RegExp(r'^Slow Percent$', caseSensitive: false).hasMatch(labelOrProp)) {
      return '%';
    }
    if (RegExp(r'(Cooldown|Duration|Delay|Time)$', caseSensitive: false)
        .hasMatch(labelOrProp)) { return 's'; }
    if (RegExp(r'(Range|Radius|Distance)$', caseSensitive: false)
        .hasMatch(labelOrProp)) { return 'm'; }
    return '';
  }

  /// Append unit if value doesn't already have one.
  static String withUnit(String value, String labelOrProp) {
    if (value.isEmpty) return value;
    if (RegExp(r'[a-zA-Z%]$').hasMatch(value)) return value;
    final u = unitFor(labelOrProp);
    return u.isNotEmpty ? '$value$u' : value;
  }

  /// Strip parent name tokens from a child label to reduce redundancy.
  static String stripParentName(String childLabel, String parentName) {
    if (childLabel.isEmpty || parentName.isEmpty) return childLabel;
    final tokens = parentName
        .split(RegExp(r'\s+'))
        .where((t) => t.length >= 3)
        .toList();

    String out = childLabel;
    for (final t in tokens) {
      final safe = RegExp.escape(t);
      out = out.replaceAll(RegExp('\\b$safe\\b', caseSensitive: false), '');
    }

    // Also strip sub-stems of 5+ chars from compound parent names
    final pieces = RegExp(r'[A-Z][a-z]+').allMatches(parentName);
    for (final m in pieces) {
      final piece = m.group(0)!;
      if (piece.length >= 5) {
        final safe = RegExp.escape(piece);
        out = out.replaceAll(RegExp('\\b$safe\\b', caseSensitive: false), '');
      }
    }

    out = out.replaceAll(RegExp(r'\s+'), ' ').trim();
    return out.isEmpty ? childLabel : out;
  }

  /// Classify a hero property key into Core, Combat, or Meta bucket.
  static String classifyPropKey(String k) {
    final corePattern = RegExp(
      r'^starting(Max(Health|MoveSpeed)|HeavyMeleeDamage|LightMeleeDamage|BaseHealthRegen|Stamina(RegenPerSecond)?|SprintSpeed|ReloadSpeed|TechDuration|TechRange)$',
    );
    if (corePattern.hasMatch(k)) {
      if (RegExp(r'MoveSpeed|SprintSpeed|HealthRegen|Max(Health|MoveSpeed)|Stamina')
          .hasMatch(k)) { return 'Core'; }
      return 'Combat';
    }
    return 'Meta';
  }
}
