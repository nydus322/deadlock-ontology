import 'package:flutter/material.dart';

class HeroAccents {
  static const defaultAccent = Color(0xFFE8743A);

  static const _map = <String, Color>{
    'hero_inferno':   Color(0xFFE8743A), // Infernus — fire orange
    'hero_atlas':     Color(0xFFC65A3F), // Abrams — rust red
    'hero_astro':     Color(0xFFD9B15A), // Calico — gold
    'hero_bebop':     Color(0xFFB88647), // Bebop — brass
    'hero_bookworm':  Color(0xFF6E8CB8), // Mo & Krill — steel blue
    'hero_chrono':    Color(0xFF8F6FC4), // Paradox — violet
    'hero_doorman':   Color(0xFF8A9BB0), // Doorman — slate
    'hero_drifter':   Color(0xFF5A6F8F), // Drifter — cold grey
    'hero_dynamo':    Color(0xFF7FB8D6), // Dynamo — electric cyan
    'hero_familiar':  Color(0xFF9B6DFF), // Pocket — purple
    'hero_fencer':    Color(0xFFD9B15A), // Shiv-adjacent — gold
    'hero_forge':     Color(0xFFE05C5C), // McGinnis — red
    'hero_frank':     Color(0xFFA5784A), // Goo — amber
    'hero_ghost':     Color(0xFF8FB8C4), // Ivy — teal pale
    'hero_gigawatt':  Color(0xFFF5A623), // Gigawatt — electric yellow
    'hero_haze':      Color(0xFFA35FB5), // Haze — violet smoke
    'hero_hornet':    Color(0xFFE0A84A), // Vindicta — gold hornet
    'hero_kelvin':    Color(0xFF8FD4E6), // Kelvin — pale cyan ice
    'hero_krill':     Color(0xFFC4704A), // Krill — rust
    'hero_lash':      Color(0xFFC44A4A), // Lash — red
    'hero_magician':  Color(0xFF8F6FC4), // Magician — violet
    'hero_mirage':    Color(0xFFD9B15A), // Mirage — gold sand
    'hero_nano':      Color(0xFF7FC48A), // Nano — green
    'hero_necro':     Color(0xFF6FA3C4), // Seven — electric blue
    'hero_orion':     Color(0xFFD9A04A), // Sinclair — gold-red
    'hero_priest':    Color(0xFFE6D8A8), // Priest — ivory
    'hero_punkgoat':  Color(0xFFC0657A), // Punkgoat — magenta
    'hero_shiv':      Color(0xFFE05C5C), // Shiv — red
    'hero_synth':     Color(0xFFF5A623), // Synth — yellow
    'hero_tengu':     Color(0xFFC65A3F), // Tengu — red
    'hero_unicorn':   Color(0xFFE8A3D2), // Unicorn — pink
    'hero_vampirebat':Color(0xFF8A4A4A), // Vampire — oxblood
    'hero_viper':     Color(0xFF7FC48A), // Viper — green venom
    'hero_viscous':   Color(0xFF8FD4A8), // Viscous — slime green
    'hero_warden':    Color(0xFF6E8CB8), // Warden — steel blue
    'hero_werewolf':  Color(0xFFA3784A), // Wrecker — brown
    'hero_wraith':    Color(0xFFC4A3E8), // Wraith — ethereal purple
    'hero_yamato':    Color(0xFFC44A4A), // Yamato — crimson
  };

  static Color forHero(String codename) => _map[codename] ?? defaultAccent;

  static Color softFor(String codename) =>
      forHero(codename).withValues(alpha: 0.2);
}
