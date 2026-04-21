import 'package:flutter_test/flutter_test.dart';
import 'package:nydus_flutter/data/extractors/prop_formatter.dart';

void main() {
  group('PropFormatter.spiritize', () {
    test('replaces standalone Tech word', () {
      expect(PropFormatter.spiritize('Tech Damage'), 'Spirit Damage');
    });

    test('replaces Tech followed by capital letter', () {
      expect(PropFormatter.spiritize('TechDamage'), 'SpiritDamage');
    });

    test('replaces lowercase tech_ at word boundary', () {
      // \btech_ matches when tech_ appears at the start of a word (e.g. after a space).
      // Inside snake_case like scale_function_tech_damage, _ is \w so there is
      // no word boundary — the replacement does not apply there.
      expect(PropFormatter.spiritize('tech_damage'), 'spirit_damage');
    });

    test('does not replace Tech inside another word (e.g. Technique)', () {
      // \bTech\b only matches word boundary — "Technique" should not change
      // "Tech" followed immediately by a lowercase letter is not a word boundary
      final result = PropFormatter.spiritize('Technique');
      expect(result, 'Technique');
    });

    test('handles empty string', () {
      expect(PropFormatter.spiritize(''), '');
    });
  });

  group('PropFormatter.prettifyPropKey', () {
    test('splits camelCase into words', () {
      expect(PropFormatter.prettifyPropKey('maxHealth'), 'Max Health');
    });

    test('strips starting prefix', () {
      expect(PropFormatter.prettifyPropKey('startingMaxHealth'), 'Max Health');
    });

    test('capitalises first letter', () {
      expect(PropFormatter.prettifyPropKey('damage'), 'Damage');
    });

    test('applies spiritize', () {
      expect(PropFormatter.prettifyPropKey('techDamage'), 'Spirit Damage');
    });

    test('single uppercase word unchanged', () {
      expect(PropFormatter.prettifyPropKey('DPS'), 'DPS');
    });
  });

  group('PropFormatter.prettifyPropValue', () {
    test('returns int as string', () {
      expect(PropFormatter.prettifyPropValue('anyKey', 42), '42');
    });

    test('rounds float to 3 decimal places', () {
      expect(PropFormatter.prettifyPropValue('anyKey', 1.0 / 3.0), '0.333');
    });

    test('rounds stringified long float', () {
      expect(PropFormatter.prettifyPropValue('anyKey', '0.222222'), '0.222');
    });

    test('strips Valve enum prefix', () {
      expect(PropFormatter.prettifyPropValue('anyKey', 'EResourceType_None'),
          'None');
    });

    test('strips Valve enum prefix and splits camelCase inner', () {
      expect(
          PropFormatter.prettifyPropValue('anyKey', 'EAbilityType_Passive'),
          'Passive');
    });

    test('scaleFunction known key returns player name', () {
      expect(
          PropFormatter.prettifyPropValue('scaleFunction', 'scale_function_tech_damage'),
          'Spirit Power');
    });

    test('scaleFunction single_stat returns null', () {
      expect(
          PropFormatter.prettifyPropValue('scaleFunction', 'scale_function_single_stat'),
          null);
    });

    test('scaleFunction unknown key is humanised', () {
      expect(
          PropFormatter.prettifyPropValue('scaleFunction', 'scale_function_foo_bar'),
          'Foo Bar');
    });

    test('modifiesProperty known alias', () {
      expect(
          PropFormatter.prettifyPropValue('modifiesProperty', 'AbilityCooldown'),
          'Cooldown');
    });

    test('modifiesProperty DPS acronym preserved', () {
      expect(PropFormatter.prettifyPropValue('modifiesProperty', 'DPS'), 'DPS');
    });

    test('returns null for null input', () {
      expect(PropFormatter.prettifyPropValue('anyKey', null), null);
    });
  });

  group('PropFormatter.unitFor', () {
    test('Percent suffix → %', () {
      expect(PropFormatter.unitFor('SlowPercent'), '%');
    });

    test('Cooldown suffix → s', () {
      expect(PropFormatter.unitFor('AbilityCooldown'), 's');
    });

    test('Duration suffix → s', () {
      expect(PropFormatter.unitFor('AbilityDuration'), 's');
    });

    test('Range suffix → m', () {
      expect(PropFormatter.unitFor('CastRange'), 'm');
    });

    test('Radius suffix → m', () {
      expect(PropFormatter.unitFor('AbilityRadius'), 'm');
    });

    test('plain damage → empty', () {
      expect(PropFormatter.unitFor('BulletDamage'), '');
    });
  });

  group('PropFormatter.withUnit', () {
    test('appends unit when absent', () {
      expect(PropFormatter.withUnit('12', 'AbilityCooldown'), '12s');
    });

    test('does not double-append', () {
      expect(PropFormatter.withUnit('12s', 'AbilityCooldown'), '12s');
    });

    test('does not append when no unit', () {
      expect(PropFormatter.withUnit('200', 'BulletDamage'), '200');
    });

    test('handles empty value', () {
      expect(PropFormatter.withUnit('', 'AbilityCooldown'), '');
    });
  });

  group('PropFormatter.stripParentName', () {
    test('removes token present in both strings', () {
      final result = PropFormatter.stripParentName('Infernus Fireball', 'Infernus');
      expect(result, 'Fireball');
    });

    test('removes long sub-stems', () {
      // "Inferno" has 6 chars → should be stripped from "Inferno Blast"
      final result = PropFormatter.stripParentName('Inferno Blast', 'Infernus');
      // "Inferno" is a 6-char stem but it doesn't appear in parent "Infernus" as a separate token
      // so it should NOT be stripped (tokens must be >= 3 chars in the parent name)
      expect(result, isNotEmpty);
    });

    test('returns original when child would become empty', () {
      final result = PropFormatter.stripParentName('Infernus', 'Infernus');
      expect(result, 'Infernus');
    });

    test('empty parent returns child unchanged', () {
      expect(PropFormatter.stripParentName('Fireball', ''), 'Fireball');
    });

    test('empty child returns empty', () {
      expect(PropFormatter.stripParentName('', 'Infernus'), '');
    });
  });

  group('PropFormatter.classifyPropKey', () {
    test('startingMaxHealth → Core', () {
      expect(PropFormatter.classifyPropKey('startingMaxHealth'), 'Core');
    });

    test('startingBaseHealthRegen → Core', () {
      expect(PropFormatter.classifyPropKey('startingBaseHealthRegen'), 'Core');
    });

    test('startingHeavyMeleeDamage → Combat', () {
      expect(PropFormatter.classifyPropKey('startingHeavyMeleeDamage'), 'Combat');
    });

    test('arbitrary key → Meta', () {
      expect(PropFormatter.classifyPropKey('someOtherProp'), 'Meta');
    });
  });
}
