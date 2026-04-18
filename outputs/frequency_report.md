# Frequency Report — heroes.vdata

**`generic_data_type`:** `CitadelHeroData_t`  
**Entity count:** 64  
**Leaf classes:** 1  

## Class Histogram

| Class | Count |
|---|---|
| `CitadelHeroData_t` | 64 |

## Auto-Classified Chaff (Denylist Drops)

Total instances dropped: **0**

| Base Key | Instances Dropped |
|---|---|

## H3 Cardinality Analysis (ascending by max distinct values)

| Key | Max Distinct | Sample Values | H3 Verdict |
|---|---|---|---|
| `_not_pickable` | 1 | `2` | constant — likely chaff |
| `_class` | 1 | `CitadelHeroData_t` | constant — likely chaff |
| `m_bAssignedPlayersOnly` | 1 | `False` | constant — likely chaff |
| `m_bLimitedTesting` | 1 | `False` | constant — likely chaff |
| `m_bPrereleaseOnly` | 1 | `False` | constant — likely chaff |
| `m_hDamageTakenParticle` | 1 | `resource_name:particles/g` | constant — likely chaff |
| `m_hGroundDamageTakenParticle` | 1 | `resource_name:particles/g` | constant — likely chaff |
| `m_hDeathParticle` | 1 | `resource_name:particles/g` | constant — likely chaff |
| `m_hLowHealthParticle` | 1 | `resource_name:particles/g` | constant — likely chaff |
| `m_hRespawnParticle` | 1 | `resource_name:particles/g` | constant — likely chaff |
| `m_groundDashPositionCurve` | 1 | `2` | constant — likely chaff |
| `m_mapItemSlotInfo` | 1 | `3` | constant — likely chaff |
| `m_mapPurchaseBonuses` | 1 | `5` | constant — likely chaff |
| `m_mapLevelInfo` | 1 | `0` | constant — likely chaff |
| `m_flStealthSpeedMetersPerSecond` | 1 | `4` | constant — likely chaff |
| `m_strLastHitSound` | 1 | `soundevent:LastHit.Defaul` | constant — likely chaff |
| `m_strLowHealthSound` | 1 | `soundevent:PlayerAlert.Lo` | constant — likely chaff |
| `m_heroStatsUI` | 1 | `14` | constant — likely chaff |
| `m_heroStatsDisplay` | 1 | `2` | constant — likely chaff |
| `m_MapModCostBonuses` | 1 | `10` | constant — likely chaff |
| `m_strDeathSound` | 1 | `soundevent:Damage.Receive` | constant — likely chaff |
| `_base` | 1 | `hero_base` | constant — likely chaff |
| `m_hAmbientParticle` | 1 | `resource_name:particles/a` | constant — likely chaff |
| `m_strRosterBackgroundLayout` | 1 | `` | constant — likely chaff |
| `m_strMovementLoop` | 1 | `soundevent:` | constant — likely chaff |
| `m_flCollisionRadius` | 1 | `28` | constant — likely chaff |
| `m_flStepHeight` | 1 | `24` | constant — likely chaff |
| `m_bUseMainOnlyModelForExperimental` | 1 | `False` | constant — likely chaff |
| `m_strWIPModelName` | 1 | `resource_name:models/hero` | constant — likely chaff |
| `m_sAG2VariationName` | 1 | `resource_name:animgraphs/` | constant — likely chaff |
| `m_strMainOnlyModelName` | 1 | `resource_name:` | constant — likely chaff |
| `m_nReadability` | 1 | `4` | constant — likely chaff |
| `m_bBotSelectable` | 1 | `False` | constant — likely chaff |
| `m_flStepSoundTime` | 1 | `0.325` | constant — likely chaff |
| `m_bPlayerSelectable` | 2 | `False` · `True` | boolean (2 values) |
| `m_bDisabled` | 2 | `False` · `True` | boolean (2 values) |
| `m_bInDevelopment` | 2 | `False` · `True` | boolean (2 values) |
| `m_bNeedsTesting` | 2 | `False` · `True` | boolean (2 values) |
| `m_nModelSkin` | 2 | `0` · `1` | boolean (2 values) |
| `m_vecAnimGraphDefaultValueOverrides` | 2 | `4` · `5` | boolean (2 values) |
| `m_vecAmbientParticleSettings` | 2 | `ability_apply` · `palm_R` | boolean (2 values) |
| `m_eAbilityResourceType` | 2 | `EResourceType_Rage` · `EResourceType_None` | boolean (2 values) |
| `m_mapItemDraftBucketing` | 2 | `Good` · `Normal` | boolean (2 values) |
| `m_bNewPlayerRecommended` | 2 | `False` · `True` | boolean (2 values) |
| `m_bLaneTestingRecommended` | 2 | `False` · `True` | boolean (2 values) |
| `m_mapItemDraftCounterWeights` | 2 | `2.0` · `2.5` | boolean (2 values) |
| `m_mapScalingStats` | 2 | `0.08` · `0.022` | boolean (2 values) |
| `m_nComplexity` | 4 | `3` · `2` | wheat (4 values) |
| `m_eHeroType` | 4 | `ECitadelHeroType_Marksman` · `ECitadelHeroType_Brawler` | wheat (4 values) |
| `m_nAllyBotDifficulty` | 5 | `0` · `1` | wheat (5 values) |
| `m_nEnemyBotDifficulty` | 5 | `0` · `1` | wheat (5 values) |
| `m_strVoteRevealSound` | 11 | `soundevent:Vo.VoteReveal.` · `soundevent:Vo.VoteReveal.` | wheat (11 values) |
| `m_strGunTag` | 13 | `#Attribute_EWeaponAttribu` · `#Attribute_EWeaponAttribu` | wheat (13 values) |
| `m_strHeroSortName` | 15 | `#hero_frank_sort` · `#hero_vampirebat_sort` | wheat (15 values) |
| `m_mapStartingStats` | 16 | `715` · `700` | wheat (16 values) |
| `m_strPostGameDefeatSound` | 25 | `soundevent:Inferno.Proges` · `soundevent:Nano.Progessio` | wheat (25 values) |
| `m_colorUI` | 27 | `66` · `207` | wheat (27 values) |
| `m_hGameSoundEventScript` | 30 | `resource_name:soundevents` · `resource_name:soundevents` | wheat (30 values) |
| `m_strHideoutRichPresence` | 36 | `#Steam_Citadel_Hideout_Ig` · `#Steam_Citadel_Hideout_Av` | wheat (36 values) |
| `m_strLogoImageEnglish` | 38 | `panorama:file://{images}/` · `panorama:file://{images}/` | wheat (38 values) |
| `m_strLogoImageLocalized` | 38 | `panorama:file://{images}/` · `panorama:file://{images}/` | wheat (38 values) |
| `m_strPostGameVictorySound` | 38 | `soundevent:Inferno.Proges` · `soundevent:Bookworm.Proge` | wheat (38 values) |
| `m_vecHeroTags` | 38 | `#Citadel_Familiar_HeroTag` · `#Citadel_Tengu_HeroTag_1` | wheat (38 values) |
| `m_strIconHeroCardCritical` | 38 | `panorama:file://{images}/` · `panorama:file://{images}/` | wheat (38 values) |
| `m_strIconHeroCardGloat` | 38 | `panorama:file://{images}/` · `panorama:file://{images}/` | wheat (38 values) |
| `m_strRosterRemovedSound` | 39 | `soundevent:Generated.Fran` · `soundevent:Generated.Atla` | wheat (39 values) |
| `m_ShopStatDisplay` | 40 | `panorama:file://{images}/` · `panorama:file://{images}/` | wheat (40 values) |
| `m_strUIPortraitMap` | 40 | `maps/ui/hero_prefabs/yama` · `maps/ui/hero_prefabs/shiv` | wheat (40 values) |
| `m_hGeneratedVOEventScript` | 40 | `resource_name:soundevents` · `resource_name:soundevents` | wheat (40 values) |
| `m_strUIShoppingMap` | 41 | `maps/ui/hero_shop/ghost_s` · `maps/ui/hero_shop/familia` | wheat (41 values) |
| `m_strUITeamRevealMap` | 42 | `maps/ui/team_reveal_hero/` · `maps/ui/team_reveal_hero/` | wheat (42 values) |
| `m_strUIPostgamePortraitMap` | 42 | `maps/ui/hero_postgame_por` · `maps/ui/hero_postgame_por` | wheat (42 values) |
| `m_strRosterSelectedSound` | 43 | `soundevent:Generated.Punk` · `soundevent:Generated.Vipe` | wheat (43 values) |
| `m_strDeathVOSound` | 44 | `soundevent:Generated.Unic` · `soundevent:Generated.Boho` | wheat (44 values) |
| `m_strModelName` | 45 | `resource_name:models/hero` · `resource_name:models/hero` | wheat (45 values) |
| `m_mapStandardLevelUpUpgrades` | 47 | `0.077` · `0.26` | wheat (47 values) |
| `m_strTopBarVertical` | 51 | `panorama:file://{images}/` · `panorama:file://{images}/` | wheat (51 values) |
| `m_strIconImageSmall` | 56 | `panorama:file://{images}/` · `panorama:file://{images}/` | wheat (56 values) |
| `m_strMinimapImage` | 57 | `panorama:file://{images}/` · `panorama:file://{images}/` | wheat (57 values) |
| `m_strIconHeroCard` | 58 | `panorama:file://{images}/` · `panorama:file://{images}/` | wheat (58 values) |
| `m_strHeroSearchName` | 60 | `#hero_gigawatt_search` · `#hero_airheart_search` | wheat (60 values) |
| `m_mapBoundAbilities` | 63 | `citadel_weapon_shiv_set` · `citadel_weapon_bull_set` | wheat (63 values) |
| `m_HeroID` | 64 | `6` · `8` | wheat (64 values) |

## Per-Class Breakdown


### `CitadelHeroData_t` (64 entities)

| Key Path | Distinct | Entity Count | H3 Verdict |
|---|---|---|---|
| `_not_pickable` | 1 | 1 | constant `2` |
| `_class` | 1 | 64 | constant `CitadelHeroData_t` |
| `m_bAssignedPlayersOnly` | 1 | 64 | constant `False` |
| `m_bLimitedTesting` | 1 | 64 | constant `False` |
| `m_bPrereleaseOnly` | 1 | 64 | constant `False` |
| `m_hDamageTakenParticle` | 1 | 64 | constant `resource_name:partic` |
| `m_hGroundDamageTakenParticle` | 1 | 64 | constant `resource_name:partic` |
| `m_hDeathParticle` | 1 | 64 | constant `resource_name:partic` |
| `m_hLowHealthParticle` | 1 | 64 | constant `resource_name:partic` |
| `m_hRespawnParticle` | 1 | 64 | constant `resource_name:partic` |
| `m_mapStartingStats.ECrouchSpeed` | 1 | 64 | constant `4.75` |
| `m_mapStartingStats.EMoveAcceleration` | 1 | 64 | constant `4` |
| `m_mapStartingStats.EWeaponPower` | 1 | 64 | constant `0` |
| `m_mapStartingStats.EReloadSpeed` | 1 | 64 | constant `1` |
| `m_mapStartingStats.EWeaponPowerScale` | 1 | 64 | constant `1` |
| `m_mapStartingStats.EProcBuildUpRateScale` | 1 | 64 | constant `1` |
| `m_mapStartingStats.EAbilityResourceMax` | 1 | 64 | constant `0` |
| `m_mapStartingStats.EAbilityResourceRegenPerSecond` | 1 | 64 | constant `0` |
| `m_mapStartingStats.ETechDuration` | 1 | 64 | constant `1` |
| `m_mapStartingStats.ETechRange` | 1 | 64 | constant `1` |
| `m_mapStartingStats.EHeroSpiritLifestealEffectiveness` | 1 | 64 | constant `1.0` |
| `m_mapStartingStats.EHeroBulletLifestealEffectiveness` | 1 | 64 | constant `1.0` |
| `m_mapStartingStats.EGroundDashDistanceInMeters` | 1 | 64 | constant `10.0` |
| `m_mapStartingStats.EAirDashDistanceInMeters` | 1 | 64 | constant `8.0` |
| `m_groundDashPositionCurve.m_spline.__len__` | 1 | 64 | constant `2` |
| `m_groundDashPositionCurve.m_spline[0].x` | 1 | 64 | constant `0.0` |
| `m_groundDashPositionCurve.m_spline[0].y` | 1 | 64 | constant `0.0` |
| `m_groundDashPositionCurve.m_spline[0].m_flSlopeIncoming` | 1 | 64 | constant `1.0` |
| `m_groundDashPositionCurve.m_spline[0].m_flSlopeOutgoing` | 1 | 64 | constant `1.0` |
| `m_groundDashPositionCurve.m_spline[1].x` | 1 | 64 | constant `1.0` |
| `m_groundDashPositionCurve.m_spline[1].y` | 1 | 64 | constant `1.0` |
| `m_groundDashPositionCurve.m_spline[1].m_flSlopeIncoming` | 1 | 64 | constant `1.0` |
| `m_groundDashPositionCurve.m_spline[1].m_flSlopeOutgoing` | 1 | 64 | constant `1.0` |
| `m_groundDashPositionCurve.m_tangents.__len__` | 1 | 64 | constant `2` |
| `m_groundDashPositionCurve.m_tangents[0].m_nIncomingTangent` | 1 | 64 | constant `CURVE_TANGENT_SPLINE` |
| `m_groundDashPositionCurve.m_tangents[0].m_nOutgoingTangent` | 1 | 64 | constant `CURVE_TANGENT_SPLINE` |
| `m_groundDashPositionCurve.m_tangents[1].m_nIncomingTangent` | 1 | 64 | constant `CURVE_TANGENT_SPLINE` |
| `m_groundDashPositionCurve.m_tangents[1].m_nOutgoingTangent` | 1 | 64 | constant `CURVE_TANGENT_SPLINE` |
| `m_groundDashPositionCurve.m_vDomainMins.__len__` | 1 | 64 | constant `2` |
| `m_groundDashPositionCurve.m_vDomainMins[0]` | 1 | 64 | constant `0.0` |
| `m_groundDashPositionCurve.m_vDomainMins[1]` | 1 | 64 | constant `0.0` |
| `m_groundDashPositionCurve.m_vDomainMaxs.__len__` | 1 | 64 | constant `2` |
| `m_groundDashPositionCurve.m_vDomainMaxs[0]` | 1 | 64 | constant `1.0` |
| `m_groundDashPositionCurve.m_vDomainMaxs[1]` | 1 | 64 | constant `1.0` |
| `m_mapBoundAbilities.ESlot_Ability_Mantle` | 1 | 64 | constant `citadel_ability_mant` |
| `m_mapBoundAbilities.ESlot_Ability_Jump` | 1 | 64 | constant `citadel_ability_jump` |
| `m_mapBoundAbilities.ESlot_Ability_ZipLine` | 1 | 64 | constant `citadel_ability_zip_` |
| `m_mapBoundAbilities.ESlot_Ability_ZipLineBoost` | 1 | 64 | constant `citadel_ability_zipl` |
| `m_mapBoundAbilities.ESlot_Ability_ClimbRope` | 1 | 64 | constant `citadel_ability_clim` |
| `m_mapBoundAbilities.ESlot_Ability_Innate_1` | 1 | 64 | constant `citadel_ability_dash` |
| `m_mapBoundAbilities.ESlot_Ability_Innate_2` | 1 | 64 | constant `citadel_ability_spri` |
| `m_mapBoundAbilities.ESlot_Ability_Innate_3` | 1 | 64 | constant `citadel_ability_mele` |
| `m_mapItemSlotInfo.EItemSlotType_WeaponMod.m_arMaxPurchasesForTier.__len__` | 1 | 64 | constant `3` |
| `m_mapItemSlotInfo.EItemSlotType_WeaponMod.m_arMaxPurchasesForTier[0]` | 1 | 64 | constant `6` |
| `m_mapItemSlotInfo.EItemSlotType_WeaponMod.m_arMaxPurchasesForTier[1]` | 1 | 64 | constant `6` |
| `m_mapItemSlotInfo.EItemSlotType_WeaponMod.m_arMaxPurchasesForTier[2]` | 1 | 64 | constant `6` |
| `m_mapItemSlotInfo.EItemSlotType_Armor.m_arMaxPurchasesForTier.__len__` | 1 | 64 | constant `3` |
| `m_mapItemSlotInfo.EItemSlotType_Armor.m_arMaxPurchasesForTier[0]` | 1 | 64 | constant `6` |
| `m_mapItemSlotInfo.EItemSlotType_Armor.m_arMaxPurchasesForTier[1]` | 1 | 64 | constant `6` |
| `m_mapItemSlotInfo.EItemSlotType_Armor.m_arMaxPurchasesForTier[2]` | 1 | 64 | constant `6` |
| `m_mapItemSlotInfo.EItemSlotType_Tech.m_arMaxPurchasesForTier.__len__` | 1 | 64 | constant `3` |
| `m_mapItemSlotInfo.EItemSlotType_Tech.m_arMaxPurchasesForTier[0]` | 1 | 64 | constant `6` |
| `m_mapItemSlotInfo.EItemSlotType_Tech.m_arMaxPurchasesForTier[1]` | 1 | 64 | constant `6` |
| `m_mapItemSlotInfo.EItemSlotType_Tech.m_arMaxPurchasesForTier[2]` | 1 | 64 | constant `6` |
| `m_mapPurchaseBonuses.EItemSlotType_WeaponMod.__len__` | 1 | 64 | constant `5` |
| `m_mapPurchaseBonuses.EItemSlotType_WeaponMod[0].m_nTier` | 1 | 64 | constant `1` |
| `m_mapPurchaseBonuses.EItemSlotType_WeaponMod[0].m_strValue` | 1 | 64 | constant `4` |
| `m_mapPurchaseBonuses.EItemSlotType_WeaponMod[0].m_ValueType` | 1 | 64 | constant `MODIFIER_VALUE_BASEA` |
| `m_mapPurchaseBonuses.EItemSlotType_WeaponMod[1].m_nTier` | 1 | 64 | constant `2` |
| `m_mapPurchaseBonuses.EItemSlotType_WeaponMod[1].m_strValue` | 1 | 64 | constant `8` |
| `m_mapPurchaseBonuses.EItemSlotType_WeaponMod[1].m_ValueType` | 1 | 64 | constant `MODIFIER_VALUE_BASEA` |
| `m_mapPurchaseBonuses.EItemSlotType_WeaponMod[2].m_nTier` | 1 | 64 | constant `3` |
| `m_mapPurchaseBonuses.EItemSlotType_WeaponMod[2].m_strValue` | 1 | 64 | constant `13` |
| `m_mapPurchaseBonuses.EItemSlotType_WeaponMod[2].m_ValueType` | 1 | 64 | constant `MODIFIER_VALUE_BASEA` |
| `m_mapPurchaseBonuses.EItemSlotType_Armor.__len__` | 1 | 64 | constant `5` |
| `m_mapPurchaseBonuses.EItemSlotType_Armor[0].m_nTier` | 1 | 64 | constant `1` |
| `m_mapPurchaseBonuses.EItemSlotType_Armor[0].m_strValue` | 1 | 64 | constant `7` |
| `m_mapPurchaseBonuses.EItemSlotType_Armor[0].m_ValueType` | 1 | 64 | constant `MODIFIER_VALUE_BASE_` |
| `m_mapPurchaseBonuses.EItemSlotType_Armor[1].m_nTier` | 1 | 64 | constant `2` |
| `m_mapPurchaseBonuses.EItemSlotType_Armor[1].m_strValue` | 1 | 64 | constant `8` |
| `m_mapPurchaseBonuses.EItemSlotType_Armor[1].m_ValueType` | 1 | 64 | constant `MODIFIER_VALUE_BASE_` |
| `m_mapPurchaseBonuses.EItemSlotType_Armor[2].m_nTier` | 1 | 64 | constant `3` |
| `m_mapPurchaseBonuses.EItemSlotType_Armor[2].m_strValue` | 1 | 64 | constant `9` |
| `m_mapPurchaseBonuses.EItemSlotType_Armor[2].m_ValueType` | 1 | 64 | constant `MODIFIER_VALUE_BASE_` |
| `m_mapPurchaseBonuses.EItemSlotType_Tech.__len__` | 1 | 64 | constant `5` |
| `m_mapPurchaseBonuses.EItemSlotType_Tech[0].m_nTier` | 1 | 64 | constant `1` |
| `m_mapPurchaseBonuses.EItemSlotType_Tech[0].m_strValue` | 1 | 64 | constant `4` |
| `m_mapPurchaseBonuses.EItemSlotType_Tech[0].m_ValueType` | 1 | 64 | constant `MODIFIER_VALUE_TECH_` |
| `m_mapPurchaseBonuses.EItemSlotType_Tech[1].m_nTier` | 1 | 64 | constant `2` |
| `m_mapPurchaseBonuses.EItemSlotType_Tech[1].m_strValue` | 1 | 64 | constant `7` |
| `m_mapPurchaseBonuses.EItemSlotType_Tech[1].m_ValueType` | 1 | 64 | constant `MODIFIER_VALUE_TECH_` |
| `m_mapPurchaseBonuses.EItemSlotType_Tech[2].m_nTier` | 1 | 64 | constant `3` |
| `m_mapPurchaseBonuses.EItemSlotType_Tech[2].m_strValue` | 1 | 64 | constant `10` |
| `m_mapPurchaseBonuses.EItemSlotType_Tech[2].m_ValueType` | 1 | 64 | constant `MODIFIER_VALUE_TECH_` |
| `m_mapLevelInfo.1.m_unRequiredGold` | 1 | 64 | constant `0` |
| `m_mapLevelInfo.1.m_mapBonusCurrencies.EAbilityUnlocks` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.2.m_unRequiredGold` | 1 | 64 | constant `300` |
| `m_mapLevelInfo.2.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.2.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.3.m_unRequiredGold` | 1 | 64 | constant `600` |
| `m_mapLevelInfo.3.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.3.m_mapBonusCurrencies.EAbilityUnlocks` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.4.m_unRequiredGold` | 1 | 64 | constant `900` |
| `m_mapLevelInfo.4.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.4.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.5.m_unRequiredGold` | 1 | 64 | constant `1500` |
| `m_mapLevelInfo.5.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.5.m_mapBonusCurrencies.EAbilityUnlocks` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.6.m_unRequiredGold` | 1 | 64 | constant `2200` |
| `m_mapLevelInfo.6.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.6.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.7.m_unRequiredGold` | 1 | 64 | constant `3000` |
| `m_mapLevelInfo.7.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.7.m_mapBonusCurrencies.EAbilityUnlocks` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.8.m_unRequiredGold` | 1 | 64 | constant `3800` |
| `m_mapLevelInfo.8.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.8.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.9.m_unRequiredGold` | 1 | 64 | constant `4600` |
| `m_mapLevelInfo.9.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.9.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.10.m_unRequiredGold` | 1 | 64 | constant `5400` |
| `m_mapLevelInfo.10.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.10.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.11.m_unRequiredGold` | 1 | 64 | constant `6200` |
| `m_mapLevelInfo.11.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.11.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.12.m_unRequiredGold` | 1 | 64 | constant `7100` |
| `m_mapLevelInfo.12.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.12.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.13.m_unRequiredGold` | 1 | 64 | constant `8000` |
| `m_mapLevelInfo.13.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.13.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.14.m_unRequiredGold` | 1 | 64 | constant `9000` |
| `m_mapLevelInfo.14.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.14.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.15.m_unRequiredGold` | 1 | 64 | constant `10000` |
| `m_mapLevelInfo.15.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.15.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.16.m_unRequiredGold` | 1 | 64 | constant `11000` |
| `m_mapLevelInfo.16.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.16.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.17.m_unRequiredGold` | 1 | 64 | constant `12000` |
| `m_mapLevelInfo.17.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.17.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.18.m_unRequiredGold` | 1 | 64 | constant `13200` |
| `m_mapLevelInfo.18.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.18.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.19.m_unRequiredGold` | 1 | 64 | constant `15000` |
| `m_mapLevelInfo.19.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.19.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.20.m_unRequiredGold` | 1 | 64 | constant `17000` |
| `m_mapLevelInfo.20.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.20.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.21.m_unRequiredGold` | 1 | 64 | constant `19000` |
| `m_mapLevelInfo.21.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.21.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.22.m_unRequiredGold` | 1 | 64 | constant `21000` |
| `m_mapLevelInfo.22.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.22.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.23.m_unRequiredGold` | 1 | 64 | constant `23000` |
| `m_mapLevelInfo.23.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.23.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.24.m_unRequiredGold` | 1 | 64 | constant `25000` |
| `m_mapLevelInfo.24.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.24.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.25.m_unRequiredGold` | 1 | 64 | constant `27000` |
| `m_mapLevelInfo.25.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.25.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.26.m_unRequiredGold` | 1 | 64 | constant `29000` |
| `m_mapLevelInfo.26.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.26.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.27.m_unRequiredGold` | 1 | 64 | constant `31000` |
| `m_mapLevelInfo.27.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.27.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.28.m_unRequiredGold` | 1 | 64 | constant `33000` |
| `m_mapLevelInfo.28.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.28.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.29.m_unRequiredGold` | 1 | 64 | constant `35000` |
| `m_mapLevelInfo.29.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.29.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.30.m_unRequiredGold` | 1 | 64 | constant `37000` |
| `m_mapLevelInfo.30.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.30.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.31.m_unRequiredGold` | 1 | 64 | constant `39000` |
| `m_mapLevelInfo.31.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.31.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.32.m_unRequiredGold` | 1 | 64 | constant `41000` |
| `m_mapLevelInfo.32.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.32.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.33.m_unRequiredGold` | 1 | 64 | constant `43000` |
| `m_mapLevelInfo.33.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.33.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.34.m_unRequiredGold` | 1 | 64 | constant `45000` |
| `m_mapLevelInfo.34.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.34.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.35.m_unRequiredGold` | 1 | 64 | constant `47000` |
| `m_mapLevelInfo.35.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.35.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_mapLevelInfo.36.m_unRequiredGold` | 1 | 64 | constant `49000` |
| `m_mapLevelInfo.36.m_bUseStandardUpgrade` | 1 | 64 | constant `True` |
| `m_mapLevelInfo.36.m_mapBonusCurrencies.EAbilityPoints` | 1 | 64 | constant `1` |
| `m_flStealthSpeedMetersPerSecond` | 1 | 64 | constant `4` |
| `m_vecAnimGraphDefaultValueOverrides[0].m_strParamName` | 1 | 64 | constant `e_SWITCH_4wayRoll_ON` |
| `m_vecAnimGraphDefaultValueOverrides[0].m_strParamValue` | 1 | 64 | constant `0` |
| `m_vecAnimGraphDefaultValueOverrides[1].m_strParamName` | 1 | 64 | constant `e_SWITCH_Recoil_ON/O` |
| `m_vecAnimGraphDefaultValueOverrides[2].m_strParamName` | 1 | 64 | constant `e_SWITCH_ZiplinePhys` |
| `m_vecAnimGraphDefaultValueOverrides[2].m_strParamValue` | 1 | 64 | constant `0` |
| `m_strLastHitSound` | 1 | 64 | constant `soundevent:LastHit.D` |
| `m_strLowHealthSound` | 1 | 64 | constant `soundevent:PlayerAle` |
| `m_colorUI.__len__` | 1 | 64 | constant `3` |
| `m_vecAmbientParticleSettings.__len__` | 1 | 64 | constant `2` |
| `m_vecAmbientParticleSettings[0].m_eAttachmentType` | 1 | 64 | constant `PATTACH_ABSORIGIN_FO` |
| `m_vecAmbientParticleSettings[0].m_nCP` | 1 | 64 | constant `0` |
| `m_vecAmbientParticleSettings[1].m_nCP` | 1 | 64 | constant `1` |
| `m_vecAmbientParticleSettings[1].m_eAttachmentType` | 1 | 64 | constant `PATTACH_POINT_FOLLOW` |
| `m_heroStatsUI.m_vecDisplayStats.__len__` | 1 | 64 | constant `14` |
| `m_heroStatsUI.m_vecDisplayStats[0].m_eStatType` | 1 | 64 | constant `EMaxHealth` |
| `m_heroStatsUI.m_vecDisplayStats[0].m_eStatCategory` | 1 | 64 | constant `ECitadelStat_Vitalit` |
| `m_heroStatsUI.m_vecDisplayStats[1].m_eStatType` | 1 | 64 | constant `EBaseHealthRegen` |
| `m_heroStatsUI.m_vecDisplayStats[1].m_eStatCategory` | 1 | 64 | constant `ECitadelStat_Vitalit` |
| `m_heroStatsUI.m_vecDisplayStats[2].m_eStatType` | 1 | 64 | constant `EBulletArmorDamageRe` |
| `m_heroStatsUI.m_vecDisplayStats[2].m_eStatCategory` | 1 | 64 | constant `ECitadelStat_Vitalit` |
| `m_heroStatsUI.m_eWeaponStatDisplay` | 1 | 64 | constant `EMeleeDamage_DEPRECA` |
| `m_heroStatsDisplay.m_vecHealthHeaderStats.__len__` | 1 | 64 | constant `2` |
| `m_heroStatsDisplay.m_vecHealthHeaderStats[0]` | 1 | 64 | constant `EMaxHealth` |
| `m_heroStatsDisplay.m_vecHealthHeaderStats[1]` | 1 | 64 | constant `EBaseHealthRegen` |
| `m_heroStatsDisplay.m_vecHealthStats.__len__` | 1 | 64 | constant `9` |
| `m_heroStatsDisplay.m_vecHealthStats[0]` | 1 | 64 | constant `EBulletArmorDamageRe` |
| `m_heroStatsDisplay.m_vecHealthStats[1]` | 1 | 64 | constant `ETechArmorDamageRedu` |
| `m_heroStatsDisplay.m_vecHealthStats[2]` | 1 | 64 | constant `EBulletShieldHealth` |
| `m_heroStatsDisplay.m_vecWeaponHeaderStats.__len__` | 1 | 64 | constant `2` |
| `m_heroStatsDisplay.m_vecWeaponHeaderStats[0]` | 1 | 64 | constant `EWeaponDPS` |
| `m_heroStatsDisplay.m_vecWeaponHeaderStats[1]` | 1 | 64 | constant `EBulletDamage` |
| `m_heroStatsDisplay.m_vecWeaponStats.__len__` | 1 | 64 | constant `4` |
| `m_heroStatsDisplay.m_vecWeaponStats[0]` | 1 | 64 | constant `ELightMeleeDamage` |
| `m_heroStatsDisplay.m_vecWeaponStats[1]` | 1 | 64 | constant `EHeavyMeleeDamage` |
| `m_heroStatsDisplay.m_vecWeaponStats[2]` | 1 | 64 | constant `EFireRate` |
| `m_heroStatsDisplay.m_vecMagicHeaderStats.__len__` | 1 | 64 | constant `1` |
| `m_heroStatsDisplay.m_vecMagicHeaderStats[0]` | 1 | 64 | constant `ETechPower` |
| `m_heroStatsDisplay.m_vecMagicStats.__len__` | 1 | 64 | constant `3` |
| `m_heroStatsDisplay.m_vecMagicStats[0]` | 1 | 64 | constant `ETechCooldown` |
| `m_heroStatsDisplay.m_vecMagicStats[1]` | 1 | 64 | constant `ETechRange` |
| `m_heroStatsDisplay.m_vecMagicStats[2]` | 1 | 64 | constant `ETechDuration` |
| `m_mapStandardLevelUpUpgrades.MODIFIER_VALUE_BOON_COUNT` | 1 | 64 | constant `1` |
| `m_mapStandardLevelUpUpgrades.MODIFIER_VALUE_TECH_DAMAGE_PERCENT` | 1 | 64 | constant `0.0` |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_vecDisplayStats.__len__` | 1 | 64 | constant `12` |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_vecDisplayStats[0]` | 1 | 64 | constant `EBulletDamage` |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_vecDisplayStats[1]` | 1 | 64 | constant `EBaseWeaponDamageInc` |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_vecDisplayStats[2]` | 1 | 64 | constant `ERoundsPerSecond` |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_vecOtherDisplayStats.__len__` | 1 | 64 | constant `2` |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_vecOtherDisplayStats[0]` | 1 | 64 | constant `ELightMeleeDamage` |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_vecOtherDisplayStats[1]` | 1 | 64 | constant `EHeavyMeleeDamage` |
| `m_ShopStatDisplay.m_eVitalityStatsDisplay.m_vecDisplayStats.__len__` | 1 | 64 | constant `9` |
| `m_ShopStatDisplay.m_eVitalityStatsDisplay.m_vecDisplayStats[0]` | 1 | 64 | constant `EMaxHealth` |
| `m_ShopStatDisplay.m_eVitalityStatsDisplay.m_vecDisplayStats[1]` | 1 | 64 | constant `EBaseHealthRegen` |
| `m_ShopStatDisplay.m_eVitalityStatsDisplay.m_vecDisplayStats[2]` | 1 | 64 | constant `EHealingOutput` |
| `m_ShopStatDisplay.m_eVitalityStatsDisplay.m_vecOtherDisplayStats.__len__` | 1 | 64 | constant `6` |
| `m_ShopStatDisplay.m_eVitalityStatsDisplay.m_vecOtherDisplayStats[0]` | 1 | 64 | constant `EMaxMoveSpeed` |
| `m_ShopStatDisplay.m_eVitalityStatsDisplay.m_vecOtherDisplayStats[1]` | 1 | 64 | constant `ESprintSpeed` |
| `m_ShopStatDisplay.m_eVitalityStatsDisplay.m_vecOtherDisplayStats[2]` | 1 | 64 | constant `EStaminaCooldown` |
| `m_ShopStatDisplay.m_eSpiritStatsDisplay.m_vecDisplayStats.__len__` | 1 | 64 | constant `6` |
| `m_ShopStatDisplay.m_eSpiritStatsDisplay.m_vecDisplayStats[0]` | 1 | 64 | constant `ETechCooldown` |
| `m_ShopStatDisplay.m_eSpiritStatsDisplay.m_vecDisplayStats[1]` | 1 | 64 | constant `ETechDuration` |
| `m_ShopStatDisplay.m_eSpiritStatsDisplay.m_vecDisplayStats[2]` | 1 | 64 | constant `ETechRange` |
| `m_MapModCostBonuses.EItemSlotType_WeaponMod.__len__` | 1 | 64 | constant `10` |
| `m_MapModCostBonuses.EItemSlotType_WeaponMod[0].nGoldThreshold` | 1 | 64 | constant `800` |
| `m_MapModCostBonuses.EItemSlotType_WeaponMod[0].flBonus` | 1 | 64 | constant `7` |
| `m_MapModCostBonuses.EItemSlotType_WeaponMod[0].flPercentOnGraph` | 1 | 64 | constant `8` |
| `m_MapModCostBonuses.EItemSlotType_WeaponMod[1].nGoldThreshold` | 1 | 64 | constant `1600` |
| `m_MapModCostBonuses.EItemSlotType_WeaponMod[1].flBonus` | 1 | 64 | constant `9` |
| `m_MapModCostBonuses.EItemSlotType_WeaponMod[1].flPercentOnGraph` | 1 | 64 | constant `8` |
| `m_MapModCostBonuses.EItemSlotType_WeaponMod[2].nGoldThreshold` | 1 | 64 | constant `2400` |
| `m_MapModCostBonuses.EItemSlotType_WeaponMod[2].flBonus` | 1 | 64 | constant `13` |
| `m_MapModCostBonuses.EItemSlotType_WeaponMod[2].flPercentOnGraph` | 1 | 64 | constant `9` |
| `m_MapModCostBonuses.EItemSlotType_Armor.__len__` | 1 | 64 | constant `10` |
| `m_MapModCostBonuses.EItemSlotType_Armor[0].nGoldThreshold` | 1 | 64 | constant `800` |
| `m_MapModCostBonuses.EItemSlotType_Armor[0].flBonus` | 1 | 64 | constant `8` |
| `m_MapModCostBonuses.EItemSlotType_Armor[0].flPercentOnGraph` | 1 | 64 | constant `8` |
| `m_MapModCostBonuses.EItemSlotType_Armor[1].nGoldThreshold` | 1 | 64 | constant `1600` |
| `m_MapModCostBonuses.EItemSlotType_Armor[1].flBonus` | 1 | 64 | constant `10` |
| `m_MapModCostBonuses.EItemSlotType_Armor[1].flPercentOnGraph` | 1 | 64 | constant `8` |
| `m_MapModCostBonuses.EItemSlotType_Armor[2].nGoldThreshold` | 1 | 64 | constant `2400` |
| `m_MapModCostBonuses.EItemSlotType_Armor[2].flBonus` | 1 | 64 | constant `13` |
| `m_MapModCostBonuses.EItemSlotType_Armor[2].flPercentOnGraph` | 1 | 64 | constant `9` |
| `m_MapModCostBonuses.EItemSlotType_Tech.__len__` | 1 | 64 | constant `10` |
| `m_MapModCostBonuses.EItemSlotType_Tech[0].nGoldThreshold` | 1 | 64 | constant `800` |
| `m_MapModCostBonuses.EItemSlotType_Tech[0].flBonus` | 1 | 64 | constant `7` |
| `m_MapModCostBonuses.EItemSlotType_Tech[0].flPercentOnGraph` | 1 | 64 | constant `8` |
| `m_MapModCostBonuses.EItemSlotType_Tech[1].nGoldThreshold` | 1 | 64 | constant `1600` |
| `m_MapModCostBonuses.EItemSlotType_Tech[1].flBonus` | 1 | 64 | constant `11` |
| `m_MapModCostBonuses.EItemSlotType_Tech[1].flPercentOnGraph` | 1 | 64 | constant `8` |
| `m_MapModCostBonuses.EItemSlotType_Tech[2].nGoldThreshold` | 1 | 64 | constant `2400` |
| `m_MapModCostBonuses.EItemSlotType_Tech[2].flBonus` | 1 | 64 | constant `15` |
| `m_MapModCostBonuses.EItemSlotType_Tech[2].flPercentOnGraph` | 1 | 64 | constant `9` |
| `m_strDeathSound` | 1 | 64 | constant `soundevent:Damage.Re` |
| `m_mapItemDraftBucketing.upgrade_ability_power_shard.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_ability_refresher.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_absorbing_armor.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_acolytes_glove.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_active_reload.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_aerial_supremacy.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_aerial_supremacy.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_ancient_shield.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_ancient_shield.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_aoe_root.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_apex_combat.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_apex_combat.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_aprounds.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_arcane_extension.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_arcane_surge.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_arctic_blast.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_banshee_slugs.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_berserker.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_blitz_bullets.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_blood_tribute.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_blood_tribute.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_boundless_spirit.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_boxing_glove.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_bullet_armor_reduction_aura.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_bullet_resist_shredder.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_bulletshredimbue.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_burst_fire.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_capacitor.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_cardio_calibrator.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_celestial_guidance.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_celestial_guidance.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_chain_lightning.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_cheat_death.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_chonky.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_clip_size.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_cloak_of_opportunity.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_cloak_of_opportunity.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_cloaking_device_active.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_cloaking_device_active.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_close_quarter_combat.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_close_range.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_cold_front.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_colossus.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_containment.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_cooldown_reduction.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_counterspell.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_crackshot.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_critshot.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_crushing_fists.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_damage_recycler.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_debuff_reducer.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_deflecting_armor.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_discord.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_divine_barrier.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_diviners_kevlar.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_dps_aura.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_eldritch_shot.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_eldritch_shot.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_electric_slippers.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_electric_slippers.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_enchanted_holsters.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_escalating_exposure.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_eternal_gift.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_eternal_gift.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_ethereal_bullets.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_express_shot.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_extra_charge.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_fervor.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_fleetfoot_boots.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_focus_lens.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_fury_trance.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_glass_cannon.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_glitch.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_greater_withering_whip.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_guardian_ward.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_haunting_scream.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_haunting_scream.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_headhunter.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_headshot_booster.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_headshot_booster2.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_healbane.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_healbuff.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_healing_booster.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_health.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_health_nova.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_health_stealing_magic.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_health_stimpak.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_high_velocity_mag.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_hollow_point_rounds.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_icarus_wings.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_icarus_wings.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_imbued_duration_extender.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_improved_bullet_armor.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_improved_spirit.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_improved_stamina.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_infinite_rounds.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_infinite_rounds.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_infuser.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_inhibitor.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_intensifying_clip.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_juggernaut.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_kinetic_sash.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_lifestrike_gauntlets.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_long_range.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_magic_burst.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_magic_carpet.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_magic_reach.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_magic_shield.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_magic_shock.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_magic_slow.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_magic_storm.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_magic_tempo.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_magic_vulnerability.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_melee_charge.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_melee_rebuttal.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_melee_rebuttal.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_metal_skin.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_mystic_regeneration.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_mystic_reverb.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_mystical_piano.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_mystical_piano.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_non_player_bonus.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_non_player_bonus_sacrifice.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_nullification_aura.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_nullification_aura.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_omnicharge_pendant.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_omnicharge_pendant.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_patrons_blessing.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_patrons_blessing.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_phantom_strike.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_prism_blast.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_prism_blast.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_pristine_emblem.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_proc_silence.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_quick_silver.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_rapid_recharge.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_rapid_rounds.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_rechargingbullets.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_reduce_debuff_duration.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_regenerating_bullet_shield.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_reinforcing_casings.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_rescue_beam.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_resonant_healing.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_restorative_locket.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_return_fire.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_return_fire.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_ricochet.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_rocket_booster.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_runed_gauntlets.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_rupture.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_self_bubble.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_shadow_step.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_shadow_step.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_shadow_strike.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_shadow_strike.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_sharpshooter.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_shivas_bracelet.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_shivas_bracelet.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_shrink_ray.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_shrink_ray.m_flWeight` | 1 | 64 | constant `0.3` |
| `m_mapItemDraftBucketing.upgrade_siphon_bullets.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_slowing_bullets.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_soaring_spirit.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_spellbreaker.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_spellslinger_headshots.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_spirit_bubble.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_spirit_burn.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_spirit_sap.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_spirit_sap.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_spirit_snatch.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_split_shot.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_sprint_booster.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_superior_stamina.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_suppressor.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_surging_power.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_target_stun.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_targeted_silence.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_targeted_silence.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_tech_damage_pulse.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_tech_defense_shredders.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_tech_overflow.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_tech_purge.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_tech_range.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_thermal_detonator.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_timeless_emblem.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_timeless_emblem.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_titan_round.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_toxic_bullets.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_transcendent_cooldown.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_trophy_collector.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_ultimate_burst.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_unstable_concoction.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_unstable_concoction.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_unstoppable.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_vampire.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_veil_walker.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_vex_barrier.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_warp_stone.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_weapon_backstabber.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_weapon_shielding.m_strBucket` | 1 | 64 | constant `Normal` |
| `m_mapItemDraftBucketing.upgrade_weapon_shielding.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_weighted_shots.m_flWeight` | 1 | 64 | constant `1.0` |
| `m_mapItemDraftBucketing.upgrade_withering_whip.m_flWeight` | 1 | 64 | constant `1.0` |
| `_base` | 1 | 63 | constant `hero_base` |
| `m_hAmbientParticle` | 1 | 1 | constant `resource_name:partic` |
| `m_vecHeroTags.__len__` | 1 | 41 | constant `3` |
| `m_mapScalingStats.EBulletDamage.eScalingStat` | 1 | 2 | constant `ETechPower` |
| `m_heroStatsUI.m_eWeaponType` | 1 | 1 | constant `ECitadelWeapon_Inval` |
| `m_strRosterBackgroundLayout` | 1 | 2 | constant `` |
| `m_mapScalingStats.ESprintSpeed.eScalingStat` | 1 | 2 | constant `ETechPower` |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_strSecondaryWeaponDescLocString` | 1 | 2 | constant `` |
| `m_mapItemDraftCounterWeights.upgrade_healbane` | 1 | 1 | constant `2.0` |
| `m_mapScalingStats.EClipSize.eScalingStat` | 1 | 2 | constant `ETechPower` |
| `m_strMovementLoop` | 1 | 1 | constant `soundevent:` |
| `m_mapScalingStats.EMaxMoveSpeed.eScalingStat` | 1 | 3 | constant `ETechPower` |
| `m_flCollisionRadius` | 1 | 1 | constant `28` |
| `m_flStepHeight` | 1 | 1 | constant `24` |
| `m_mapScalingStats.ERoundsPerSecond.eScalingStat` | 1 | 1 | constant `ETechPower` |
| `m_mapScalingStats.ERoundsPerSecond.flScale` | 1 | 1 | constant `0.01` |
| `m_mapScalingStats.EFireRate.eScalingStat` | 1 | 1 | constant `ETechPower` |
| `m_mapScalingStats.EFireRate.flScale` | 1 | 1 | constant `0.25` |
| `m_bUseMainOnlyModelForExperimental` | 1 | 1 | constant `False` |
| `m_strWIPModelName` | 1 | 1 | constant `resource_name:models` |
| `m_sAG2VariationName` | 1 | 2 | constant `resource_name:animgr` |
| `m_mapScalingStats.ETechArmorDamageReduction.flScale` | 1 | 1 | constant `0.12178` |
| `m_mapScalingStats.ETechArmorDamageReduction.eScalingStat` | 1 | 1 | constant `ETechPower` |
| `m_mapScalingStats.EBulletArmorDamageReduction.eScalingStat` | 1 | 1 | constant `ETechPower` |
| `m_mapScalingStats.EBulletArmorDamageReduction.flScale` | 1 | 1 | constant `0.12178` |
| `m_mapScalingStats.EBaseHealthRegen.eScalingStat` | 1 | 1 | constant `ETechPower` |
| `m_mapScalingStats.EBaseHealthRegen.flScale` | 1 | 1 | constant `0.08` |
| `m_mapScalingStats.EHeavyMeleeDamage.eScalingStat` | 1 | 1 | constant `ETechPower` |
| `m_mapScalingStats.EHeavyMeleeDamage.flScale` | 1 | 1 | constant `0.3` |
| `m_strMainOnlyModelName` | 1 | 2 | constant `resource_name:` |
| `m_nReadability` | 1 | 1 | constant `4` |
| `m_bBotSelectable` | 1 | 1 | constant `False` |
| `m_flStepSoundTime` | 1 | 1 | constant `0.325` |
| `m_mapStartingStats.EBuildUpRate` | 1 | 1 | constant `-50.0` |
| `m_mapStartingStats.EBulletLifesteal` | 1 | 1 | constant `8.0` |
| `m_mapStartingStats.EMeleeResist` | 1 | 1 | constant `-5.0` |
| `m_bPlayerSelectable` | 2 | 64 | boolean `False` · `True` |
| `m_bDisabled` | 2 | 64 | boolean `False` · `True` |
| `m_bInDevelopment` | 2 | 64 | boolean `False` · `True` |
| `m_bNeedsTesting` | 2 | 64 | boolean `False` · `True` |
| `m_nModelSkin` | 2 | 64 | boolean `0` · `1` |
| `m_mapBoundAbilities.ESlot_Ability_Slide` | 2 | 64 | boolean `ability_punkgoat_sli` · `citadel_ability_slid` |
| `m_vecAnimGraphDefaultValueOverrides.__len__` | 2 | 64 | boolean `4` · `5` |
| `m_vecAnimGraphDefaultValueOverrides[1].m_strParamValue` | 2 | 64 | boolean `0` · `1` |
| `m_vecAmbientParticleSettings[1].m_strAttachmentName` | 2 | 64 | boolean `ability_apply` · `palm_R` |
| `m_mapStandardLevelUpUpgrades.MODIFIER_VALUE_BONUS_ATTACK_RANGE` | 2 | 64 | boolean `0.0` · `59` |
| `m_mapStandardLevelUpUpgrades.MODIFIER_VALUE_TECH_ARMOR_DAMAGE_RESIST` | 2 | 64 | boolean `0.0` · `0.625` |
| `m_eAbilityResourceType` | 2 | 64 | boolean `EResourceType_Rage` · `EResourceType_None` |
| `m_mapItemDraftBucketing.upgrade_ability_power_shard.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_ability_refresher.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_absorbing_armor.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_acolytes_glove.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_active_reload.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_aoe_root.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_aprounds.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_arcane_extension.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_arcane_surge.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_arctic_blast.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_banshee_slugs.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_berserker.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_blitz_bullets.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_boundless_spirit.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_boxing_glove.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_bullet_armor_reduction_aura.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_bullet_resist_shredder.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_bulletshredimbue.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_burst_fire.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_capacitor.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_cardio_calibrator.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_chain_lightning.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_cheat_death.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_chonky.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_clip_size.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_close_quarter_combat.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_close_range.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_cold_front.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_colossus.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_containment.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_cooldown_reduction.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_counterspell.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_crackshot.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_critshot.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_crushing_fists.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_damage_recycler.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_debuff_reducer.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_deflecting_armor.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_discord.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_divine_barrier.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_diviners_kevlar.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_dps_aura.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_enchanted_holsters.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_endurance.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_endurance.m_flWeight` | 2 | 64 | boolean `1.0` · `0.4` |
| `m_mapItemDraftBucketing.upgrade_escalating_exposure.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_ethereal_bullets.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_express_shot.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_extra_charge.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_fervor.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_fleetfoot_boots.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_focus_lens.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_fury_trance.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_glass_cannon.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_glitch.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_greater_withering_whip.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_guardian_ward.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_headhunter.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_headshot_booster.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_headshot_booster2.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_healbane.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_healbuff.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_healing_booster.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_health.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_health_nova.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_health_stealing_magic.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_health_stimpak.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_high_velocity_mag.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_hollow_point_rounds.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_imbued_duration_extender.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_improved_bullet_armor.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_improved_spirit.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_improved_stamina.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_infuser.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_inhibitor.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_intensifying_clip.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_juggernaut.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_kinetic_sash.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_lifestrike_gauntlets.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_long_range.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_magic_burst.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_magic_carpet.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_magic_reach.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_magic_shield.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_magic_shock.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_magic_slow.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_magic_storm.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_magic_tempo.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_magic_vulnerability.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_medic_bullets.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_medic_bullets.m_flWeight` | 2 | 64 | boolean `1.0` · `0.4` |
| `m_mapItemDraftBucketing.upgrade_melee_charge.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_metal_skin.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_mystic_regeneration.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_mystic_reverb.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_non_player_bonus.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_non_player_bonus_sacrifice.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_phantom_strike.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_pristine_emblem.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_proc_silence.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_quick_silver.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_rapid_recharge.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_rapid_rounds.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_rechargingbullets.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_reduce_debuff_duration.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_regenerating_bullet_shield.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_reinforcing_casings.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_rescue_beam.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_resonant_healing.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_restorative_locket.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_ricochet.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_rocket_booster.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_runed_gauntlets.m_flWeight` | 2 | 64 | boolean `1.0` · `0.4` |
| `m_mapItemDraftBucketing.upgrade_rupture.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_self_bubble.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_sharpshooter.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_siphon_bullets.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_slowing_bullets.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_soaring_spirit.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_spellbreaker.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_spellslinger_headshots.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_spirit_bubble.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_spirit_burn.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_spirit_snatch.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_split_shot.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_sprint_booster.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_superior_stamina.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_suppressor.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_surging_power.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_target_stun.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_tech_damage_pulse.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_tech_defense_shredders.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_tech_overflow.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_tech_purge.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_tech_range.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_thermal_detonator.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_titan_round.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_toxic_bullets.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_transcendent_cooldown.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_trophy_collector.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_ultimate_burst.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_unstoppable.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_vampire.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_veil_walker.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_vex_barrier.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_warp_stone.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_weapon_backstabber.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_weighted_shots.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_mapItemDraftBucketing.upgrade_withering_whip.m_strBucket` | 2 | 64 | boolean `Good` · `Normal` |
| `m_bNewPlayerRecommended` | 2 | 13 | boolean `False` · `True` |
| `m_bLaneTestingRecommended` | 2 | 17 | boolean `False` · `True` |
| `m_mapItemDraftCounterWeights.upgrade_target_stun` | 2 | 2 | boolean `2.0` · `2.5` |
| `m_mapScalingStats.EBulletDamage.flScale` | 2 | 2 | boolean `0.08` · `0.022` |
| `m_mapScalingStats.ESprintSpeed.flScale` | 2 | 2 | boolean `0.06` · `0.05` |
| `m_mapScalingStats.EClipSize.flScale` | 2 | 2 | boolean `0.15` · `0.5` |
| `m_mapScalingStats.EMaxMoveSpeed.flScale` | 2 | 3 | boolean `0.0084` · `0.0138` |
| `m_mapStartingStats.EGroundDashDuration` | 3 | 64 | wheat (3) |
| `m_mapStartingStats.EAirDashDuration` | 3 | 64 | wheat (3) |
| `m_mapStandardLevelUpUpgrades.MODIFIER_VALUE_BULLET_ARMOR_DAMAGE_RESIST` | 3 | 64 | wheat (3) |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_strWeaponDescLocString` | 3 | 3 | wheat (3) |
| `m_mapStartingStats.ETechArmorDamageReduction` | 3 | 5 | wheat (3) |
| `m_nComplexity` | 4 | 64 | wheat (4) |
| `m_mapStartingStats.EStaminaRegenPerSecond` | 4 | 64 | wheat (4) |
| `m_mapStartingStats.ECritDamageReceivedScale` | 4 | 64 | wheat (4) |
| `m_mapStandardLevelUpUpgrades.MODIFIER_VALUE_BASE_MELEE_DAMAGE_FROM_LEVEL` | 4 | 64 | wheat (4) |
| `m_eHeroType` | 4 | 38 | wheat (4) |
| `m_nAllyBotDifficulty` | 5 | 64 | wheat (5) |
| `m_nEnemyBotDifficulty` | 5 | 64 | wheat (5) |
| `m_mapStartingStats.EHeavyMeleeDamage` | 5 | 64 | wheat (5) |
| `m_mapStartingStats.EStamina` | 5 | 64 | wheat (5) |
| `m_mapStartingStats.ECritDamageBonusScale` | 5 | 64 | wheat (5) |
| `m_mapStandardLevelUpUpgrades.MODIFIER_VALUE_BASE_BULLET_DAMAGE_FROM_LEVEL_ALT_FIRE` | 5 | 64 | wheat (5) |
| `m_mapStandardLevelUpUpgrades.MODIFIER_VALUE_TECH_POWER` | 5 | 64 | wheat (5) |
| `m_mapBoundAbilities.ESlot_Weapon_Secondary` | 5 | 5 | wheat (5) |
| `m_mapStartingStats.ELightMeleeDamage` | 7 | 64 | wheat (7) |
| `m_mapStartingStats.EBaseHealthRegen` | 8 | 64 | wheat (8) |
| `m_mapStartingStats.ESprintSpeed` | 9 | 64 | wheat (9) |
| `m_strVoteRevealSound` | 11 | 11 | wheat (11) |
| `m_mapStartingStats.EMaxMoveSpeed` | 13 | 64 | wheat (13) |
| `m_strGunTag` | 13 | 40 | wheat (13) |
| `m_strHeroSortName` | 15 | 15 | wheat (15) |
| `m_mapStartingStats.EMaxHealth` | 16 | 64 | wheat (16) |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_eWeaponAttributes` | 17 | 50 | wheat (17) |
| `m_strPostGameDefeatSound` | 25 | 32 | wheat (25) |
| `m_colorUI[2]` | 26 | 64 | wheat (26) |
| `m_colorUI[0]` | 27 | 64 | wheat (27) |
| `m_colorUI[1]` | 27 | 64 | wheat (27) |
| `m_mapStandardLevelUpUpgrades.MODIFIER_VALUE_BASE_HEALTH_FROM_LEVEL` | 27 | 64 | wheat (27) |
| `m_hGameSoundEventScript` | 30 | 49 | wheat (30) |
| `m_strHideoutRichPresence` | 36 | 38 | wheat (36) |
| `m_strLogoImageEnglish` | 38 | 39 | wheat (38) |
| `m_strLogoImageLocalized` | 38 | 39 | wheat (38) |
| `m_strPostGameVictorySound` | 38 | 40 | wheat (38) |
| `m_vecHeroTags[0]` | 38 | 41 | wheat (38) |
| `m_vecHeroTags[1]` | 38 | 41 | wheat (38) |
| `m_vecHeroTags[2]` | 38 | 41 | wheat (38) |
| `m_strIconHeroCardCritical` | 38 | 39 | wheat (38) |
| `m_strIconHeroCardGloat` | 38 | 39 | wheat (38) |
| `m_strRosterRemovedSound` | 39 | 46 | wheat (39) |
| `m_ShopStatDisplay.m_eWeaponStatsDisplay.m_strWeaponImage` | 40 | 48 | wheat (40) |
| `m_strUIPortraitMap` | 40 | 49 | wheat (40) |
| `m_hGeneratedVOEventScript` | 40 | 41 | wheat (40) |
| `m_strUIShoppingMap` | 41 | 64 | wheat (41) |
| `m_strUITeamRevealMap` | 42 | 64 | wheat (42) |
| `m_strUIPostgamePortraitMap` | 42 | 64 | wheat (42) |
| `m_strRosterSelectedSound` | 43 | 49 | wheat (43) |
| `m_strDeathVOSound` | 44 | 56 | wheat (44) |
| `m_strModelName` | 45 | 64 | wheat (45) |
| `m_mapStandardLevelUpUpgrades.MODIFIER_VALUE_BASE_BULLET_DAMAGE_FROM_LEVEL` | 47 | 64 | wheat (47) |
| `m_strTopBarVertical` | 51 | 52 | wheat (51) |
| `m_strIconImageSmall` | 56 | 60 | wheat (56) |
| `m_strMinimapImage` | 57 | 60 | wheat (57) |
| `m_strIconHeroCard` | 58 | 60 | wheat (58) |
| `m_mapBoundAbilities.ESlot_Weapon_Melee` | 59 | 64 | wheat (59) |
| `m_strHeroSearchName` | 60 | 61 | wheat (60) |
| `m_mapBoundAbilities.ESlot_Signature_1` | 61 | 63 | wheat (61) |
| `m_mapBoundAbilities.ESlot_Signature_4` | 61 | 63 | wheat (61) |
| `m_mapBoundAbilities.ESlot_Signature_3` | 62 | 63 | wheat (62) |
| `m_mapBoundAbilities.ESlot_Weapon_Primary` | 63 | 64 | wheat (63) |
| `m_mapBoundAbilities.ESlot_Signature_2` | 63 | 63 | wheat (63) |
| `m_HeroID` | 64 | 64 | wheat (64) |
