# Stat Bridge Summary

> Total edges: **4884**  |  Unique MODIFIER_VALUE types: **99**  |  Unique scale functions: **43**

## MODIFIER_VALUE_* edge frequency  (top 30)

| Modifier Value Type | Edges |
|---|---|
| `MODIFIER_VALUE_FIRE_RATE` | 140 |
| `MODIFIER_VALUE_MOVEMENT_SPEED_SLOW_PERCENT` | 114 |
| `MODIFIER_VALUE_MOVEMENT_SPEED_MAX` | 65 |
| `MODIFIER_VALUE_HEALTH_MAX` | 65 |
| `MODIFIER_VALUE_TECH_POWER` | 47 |
| `MODIFIER_VALUE_BASEATTACK_DAMAGE_PERCENT` | 46 |
| `MODIFIER_VALUE_TECH_ARMOR_DAMAGE_RESIST` | 43 |
| `MODIFIER_VALUE_BULLET_ARMOR_DAMAGE_RESIST` | 40 |
| `MODIFIER_VALUE_FIRE_RATE_SLOW` | 31 |
| `MODIFIER_VALUE_BULLET_ARMOR_DAMAGE_RESIST_REDUCTION` | 26 |
| `MODIFIER_VALUE_BARRIER_HEALTH` | 26 |
| `MODIFIER_VALUE_TECH_ARMOR_DAMAGE_RESIST_REDUCTION` | 25 |
| `MODIFIER_VALUE_SPRINT_SPEED_BONUS` | 24 |
| `MODIFIER_VALUE_MOVEMENT_GROUND_DASH_REDUCTION_PERCENT` | 22 |
| `MODIFIER_VALUE_OUT_OF_COMBAT_HEALTH_REGEN` | 22 |
| `MODIFIER_VALUE_HEALTH_REGEN_PER_SECOND` | 20 |
| `MODIFIER_VALUE_HEAL_AMP_REGEN_PERCENT` | 19 |
| `MODIFIER_VALUE_BULLET_LIFESTEAL` | 18 |
| `MODIFIER_VALUE_HEAL_AMP_RECEIVE_PERCENT` | 17 |
| `MODIFIER_VALUE_TECH_RANGE_PERCENT` | 17 |
| `MODIFIER_VALUE_TECH_RADIUS_PERCENT` | 17 |
| `MODIFIER_VALUE_AMMO_CLIP_SIZE_PERCENT` | 16 |
| `MODIFIER_VALUE_DAMAGE_PERCENT` | 16 |
| `MODIFIER_VALUE_TECH_LIFESTEAL` | 14 |
| `MODIFIER_VALUE_STAMINA_REGEN_PER_SECOND_PERCENTAGE` | 12 |
| `MODIFIER_VALUE_COOLDOWN_REDUCTION_PERCENTAGE` | 12 |
| `MODIFIER_VALUE_STATUS_RESISTANCE` | 11 |
| `MODIFIER_VALUE_BASE_MELEE_DAMAGE_PERCENT` | 10 |
| `MODIFIER_VALUE_BONUS_BULLET_SPEED_PERCENT` | 10 |
| `MODIFIER_VALUE_BONUS_ABILITY_DURATION_PERCENTAGE` | 10 |

## Scale Function Inventory

> Every row below is an unknown formula — calibration required.

| Scale Function | Scaling Stat | Edges | Example Ability |
|---|---|---|---|
| `scale_function_ability_recharge_time` | `` | 1281 | `citadel_weapon_bosstier2_set` |
| `scale_function_single_stat` | `ETechCooldown` | 634 | `ability_medic_trooper_heal` |
| `scale_function_single_stat` | `ETechDuration` | 478 | `super_neutral_shield` |
| `scale_function_single_stat` | `ETechRange` | 293 | `ability_medic_trooper_heal` |
| `scale_function_single_stat` | `EItemCooldown` | 139 | `item_projectile_test_01` |
| `scale_function_tech_damage` | `ETechPower` | 137 | `ability_explosive_barrel` |
| `scale_function_tech_duration` | `` | 130 | `citadel_ability_hornet_sting` |
| `scale_function_tech_damage` | `` | 123 | `super_neutral_charge` |
| `scale_function_single_stat` | `ETechRadius` | 76 | `rutger_force_field` |
| `scale_function_single_stat` | `EMeleeRange` | 66 | `ability_melee_butcher` |
| `scale_function_single_stat` | `EHealingOutput` | 66 | `rutger_cheat_death` |
| `scale_function_single_stat` | `EAirMoveDistanceScale` | 64 | `citadel_ability_jump` |
| `scale_function_single_stat` | `EParryCooldown` | 64 | `citadel_ability_melee_parry` |
| `scale_function_ability_charges` | `` | 42 | `ability_medic_trooper_heal` |
| `scale_function_multi_stats` | `` | 41 | `gunslinger_rapid_fire` |
| `scale_function_tech_range` | `` | 39 | `citadel_ability_storm_cloud` |
| `scale_function_multi_stats` | `ETechPower` | 33 | `citadel_ability_nikuman` |
| `scale_function_single_stat` | `ETechPower` | 30 | `ability_bounce_pad` |
| `scale_function_single_stat` | `ELevelUpBoons` | 20 | `citadel_ability_shieldedsentry` |
| `scale_function_single_stat` | `EBuildUpRate` | 10 | `upgrade_weighted_shots` |
| `scale_function_multi_stats` | `ELevelUpBoons` | 9 | `upgrade_headhunter` |
| `scale_function_single_stat` | `EReloadSpeed` | 4 | `citadel_weapon_bebop_set` |
| `scale_function_single_stat` | `EProcBuildUpRateScale` | 4 | `ability_afterburn` |
| `scale_function_tech_duration` | `ETechDuration` | 4 | `citadel_ability_wraith_rapidfire` |
| `scale_function_ability_weapon_damage` | `EBaseWeaponDamageIncrease` | 4 | `ability_priest_knockback` |
| `scale_function_single_stat` | `ELightMeleeDamage` | 3 | `citadel_ability_uppercut` |
| `scale_function_kinetic_carbine_damage` | `EWeaponPower` | 2 | `citadel_ability_chrono_kinetic_carbine` |
| `scale_function_base` | `` | 2 | `ability_charged_shot` |
| `scale_function_tech_damage` | `EWeaponDamageScale` | 2 | `ability_empowerbullet` |
| `scale_function_tech_range` | `ETechRange` | 2 | `ability_punkgoat_tether` |
| `scale_function_single_stat` | `EDamageScale` | 1 | `ability_stacking_damage` |
| `scale_function_single_stat` | `` | 1 | `mirage_teleport` |
| `scale_function_tech_duration` | `EStatsCount` | 1 | `citadel_ability_card_toss` |
| `scale_function_kinetic_carbine_damage` | `EBulletDamage` | 1 | `ability_gunslinger_demon_carbine` |
| `scale_function_tech_damage` | `EStatsCount` | 1 | `ability_vampirebat_steallife` |
| `scale_function_nanotech_rounds_damage` | `ETechPower` | 1 | `upgrade_proc_tech_damage` |
| `scale_function_base_weapon_damage` | `` | 1 | `upgrade_proc_tech_damage` |
| `scale_function_base` | `ETechDuration` | 1 | `upgrade_self_bubble` |
| `scale_function_single_stat` | `EMaxChargesIncrease` | 1 | `cosmetic_item_snowball` |
| `scale_function_single_stat` | `ETechDamageScale` | 1 | `cosmetic_item_snowball` |
| `scale_function_single_stat` | `EClipSizeIncrease` | 1 | `cosmetic_item_snowball` |
| `scale_function_single_stat` | `EBaseWeaponDamageIncrease` | 1 | `ability_priest_barrage` |
| `scale_function_healing_spirit_scale` | `` | 1 | `ability_necro_gravestone` |

## Per-hero edge counts

| Hero Binding | Edges |
|---|---|
| `hero_necro` | 63 |
| `hero_familiar` | 62 |
| `hero_kelvin` | 61 |
| `hero_fencer` | 61 |
| `hero_forge` | 60 |
| `hero_bebop` | 59 |
| `hero_tengu` | 59 |
| `hero_viscous` | 59 |
| `hero_bookworm` | 59 |
| `hero_punkgoat` | 59 |
| `hero_werewolf` | 56 |
| `hero_wraith` | 53 |
| `hero_priest` | 53 |
| `hero_frank` | 53 |
| `hero_unicorn` | 53 |
| `hero_inferno` | 52 |
| `hero_gigawatt` | 52 |
| `hero_yamato` | 52 |
| `hero_lash` | 52 |
| `hero_mirage` | 52 |
| `hero_hornet` | 51 |
| `hero_warden` | 51 |
| `hero_magician` | 51 |
| `hero_trapper` | 51 |
| `hero_drifter` | 51 |
| `hero_orion` | 50 |
| `hero_wrecker` | 50 |
| `hero_synth` | 50 |
| `hero_boho` | 50 |
| `hero_atlas` | 49 |
| `hero_chrono` | 49 |
| `hero_krill` | 49 |
| `hero_viper` | 49 |
| `hero_operative` | 49 |
| `hero_doorman` | 49 |
| `hero_kali` | 48 |
| `hero_haze` | 48 |
| `hero_slork` | 48 |
| `hero_cadence` | 48 |
| `hero_rutger` | 47 |
| `hero_astro` | 47 |
| `hero_vampirebat` | 47 |
| `hero_ghost` | 46 |
| `hero_nano` | 46 |
| `hero_tokamak` | 46 |
| `hero_vandal` | 46 |
| `hero_thumper` | 44 |
| `hero_dynamo` | 44 |
| `hero_shiv` | 44 |
| `hero_yakuza` | 43 |
| `hero_gunslinger` | 43 |
| `hero_skyrunner` | 37 |
| `hero_airheart` | 34 |
| `hero_bomber` | 32 |
| `hero_swan` | 32 |
| `hero_genericperson` | 30 |
| `hero_targetdummy` | 30 |
| `hero_shieldguy` | 30 |
| `hero_graf` | 30 |
| `hero_fortuna` | 30 |
| `hero_base` | 22 |
| `hero_druid` | 20 |
| `hero_opera` | 20 |
| `hero_testhero` | 20 |