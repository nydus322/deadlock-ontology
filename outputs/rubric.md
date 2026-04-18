# Wheat / Chaff / Context-Dependent Rubric

> Source file: `heroes.vdata` — `CitadelHeroData_t`  
> Confidence target: ~80% first pass. Unknowns → `unknowns.jsonl`.

## Auto-Classified Chaff — Denylist

Pre-populated from Known Facts; no analysis needed.

| Pattern | Rationale |
|---|---|
| `^m_nEditorNode` | Editor: node positioning metadata |
| `^m_editorNode` | Editor: node handle |
| `^m_sComment$` | Editor: comment annotation |
| `^m_bDebug` | Debug: debug flag |
| `^m_bIsTestOnly$` | Debug/test: entity excluded from live builds |
| `^m_bTest` | Debug/test: test flag |
| `^m_pEntity$` | Identity: entity pointer plumbing |
| `^m_name$` | Identity: CUtlSymbolLarge internal name |
| `^m_hParticle` | Asset handle: particle effect (chaff for stats, wheat for assets) |
| `^m_hModel` | Asset handle: model (chaff for stats, wheat for assets) |
| `^m_hSound` | Asset handle: sound (chaff for stats, wheat for assets) |
| `^m_hTexture` | Asset handle: texture (chaff for stats, wheat for assets) |
| `^m_hCastAnimGraph` | Asset handle: cast anim graph |
| `^m_hGlobalAnim` | Asset handle: global animation |
| `^m_vecParticle` | Asset array: particle systems |
| `^m_strSound` | Asset string: sound path |
| `^m_strIcon$` | Asset string: icon SVG path (chaff for stats, wheat for assets) |
| `^m_strAbilityImage$` | Asset string: ability image path (chaff for stats, wheat for assets) |

**Observed drops in this file:**


---

## Confirmed Wheat

- `m_HeroID` -- H3: >=3 distinct values across instances (designed variation)
- `m_ShopStatDisplay` -- H5: localization token hit -> player-visible by definition
- `m_bDisabled` -- H2: naming convention signals meaningful game data
- `m_bInDevelopment` -- H2: naming convention signals meaningful game data
- `m_bLaneTestingRecommended` -- H2: naming convention signals meaningful game data
- `m_bNeedsTesting` -- H2: naming convention signals meaningful game data
- `m_bNewPlayerRecommended` -- H2: naming convention signals meaningful game data
- `m_bPlayerSelectable` -- H2: naming convention signals meaningful game data
- `m_colorUI` -- H3: >=3 distinct values across instances (designed variation)
- `m_eAbilityResourceType` -- H2: naming convention signals meaningful game data
- `m_eHeroType` -- H3: >=3 distinct values across instances (designed variation)
- `m_hGameSoundEventScript` -- H3: >=3 distinct values across instances (designed variation)
- `m_hGeneratedVOEventScript` -- H3: >=3 distinct values across instances (designed variation)
- `m_mapBoundAbilities` -- H3: >=3 distinct values across instances (designed variation)
- `m_mapItemDraftCounterWeights` -- H2: naming convention signals meaningful game data
- `m_mapScalingStats` -- H2: naming convention signals meaningful game data
- `m_mapStandardLevelUpUpgrades` -- H3: >=3 distinct values across instances (designed variation)
- `m_mapStartingStats` -- H3: >=3 distinct values across instances (designed variation)
- `m_nAllyBotDifficulty` -- H3: >=3 distinct values across instances (designed variation)
- `m_nComplexity` -- H3: >=3 distinct values across instances (designed variation)
- `m_nEnemyBotDifficulty` -- H3: >=3 distinct values across instances (designed variation)
- `m_nModelSkin` -- H2: naming convention signals meaningful game data
- `m_strDeathVOSound` -- H3: >=3 distinct values across instances (designed variation)
- `m_strGunTag` -- H5: localization token hit -> player-visible by definition
- `m_strHeroSearchName` -- H5: localization token hit -> player-visible by definition
- `m_strHeroSortName` -- H5: localization token hit -> player-visible by definition
- `m_strHideoutRichPresence` -- H5: localization token hit -> player-visible by definition
- `m_strIconHeroCard` -- H3: >=3 distinct values across instances (designed variation)
- `m_strIconHeroCardCritical` -- H3: >=3 distinct values across instances (designed variation)
- `m_strIconHeroCardGloat` -- H3: >=3 distinct values across instances (designed variation)
- `m_strIconImageSmall` -- H3: >=3 distinct values across instances (designed variation)
- `m_strLogoImageEnglish` -- H3: >=3 distinct values across instances (designed variation)
- `m_strLogoImageLocalized` -- H3: >=3 distinct values across instances (designed variation)
- `m_strMinimapImage` -- H3: >=3 distinct values across instances (designed variation)
- `m_strModelName` -- H3: >=3 distinct values across instances (designed variation)
- `m_strPostGameDefeatSound` -- H3: >=3 distinct values across instances (designed variation)
- `m_strPostGameVictorySound` -- H3: >=3 distinct values across instances (designed variation)
- `m_strRosterRemovedSound` -- H3: >=3 distinct values across instances (designed variation)
- `m_strRosterSelectedSound` -- H3: >=3 distinct values across instances (designed variation)
- `m_strTopBarVertical` -- H3: >=3 distinct values across instances (designed variation)
- `m_strUIPortraitMap` -- H3: >=3 distinct values across instances (designed variation)
- `m_strUIPostgamePortraitMap` -- H3: >=3 distinct values across instances (designed variation)
- `m_strUIShoppingMap` -- H3: >=3 distinct values across instances (designed variation)
- `m_strUITeamRevealMap` -- H3: >=3 distinct values across instances (designed variation)
- `m_strVoteRevealSound` -- H3: >=3 distinct values across instances (designed variation)
- `m_vecAnimGraphDefaultValueOverrides` -- H2: naming convention signals meaningful game data
- `m_vecHeroTags` -- H5: localization token hit -> player-visible by definition

---

## H3 Constants (Single-Value Chaff)

Keys with exactly 1 distinct value across all instances — engine defaults.

- `_base` = `hero_base` — constant
- `_class` = `CitadelHeroData_t` — constant
- `_not_pickable` = `2` — constant
- `m_MapModCostBonuses` = `10` — constant
- `m_bAssignedPlayersOnly` = `False` — constant
- `m_bBotSelectable` = `False` — constant
- `m_bLimitedTesting` = `False` — constant
- `m_bPrereleaseOnly` = `False` — constant
- `m_bUseMainOnlyModelForExperimental` = `False` — constant
- `m_flCollisionRadius` = `28` — constant
- `m_flStealthSpeedMetersPerSecond` = `4` — constant
- `m_flStepHeight` = `24` — constant
- `m_flStepSoundTime` = `0.325` — constant
- `m_groundDashPositionCurve` = `2` — constant
- `m_hAmbientParticle` = `resource_name:particles/abilities/inferno/inferno_hand_ambie` — constant
- `m_hDamageTakenParticle` = `resource_name:particles/generic/player_damage_screen.vpcf` — constant
- `m_hDeathParticle` = `resource_name:particles/generic/player_death_screen.vpcf` — constant
- `m_hGroundDamageTakenParticle` = `resource_name:particles/generic/player_ground_damage_screen.` — constant
- `m_hLowHealthParticle` = `resource_name:particles/generic/player_low_health_screen.vpc` — constant
- `m_hRespawnParticle` = `resource_name:particles/generic/player_respawn_deploy.vpcf` — constant
- `m_heroStatsDisplay` = `2` — constant
- `m_heroStatsUI` = `14` — constant
- `m_mapItemSlotInfo` = `3` — constant
- `m_mapLevelInfo` = `0` — constant
- `m_mapPurchaseBonuses` = `5` — constant
- `m_nReadability` = `4` — constant
- `m_sAG2VariationName` = `resource_name:animgraphs/animgraph2/hero/hero.vnmgraph+vampi` — constant
- `m_strDeathSound` = `soundevent:Damage.Receive.Lethal` — constant
- `m_strLastHitSound` = `soundevent:LastHit.Default` — constant
- `m_strLowHealthSound` = `soundevent:PlayerAlert.LowHealth` — constant
- `m_strMainOnlyModelName` = `resource_name:` — constant
- `m_strMovementLoop` = `soundevent:` — constant
- `m_strRosterBackgroundLayout` = `` — constant
- `m_strWIPModelName` = `resource_name:models/heroes_wip/viscous/viscous_tourist_shap` — constant

---

## H3 Booleans (Two-Value Keys)

Keys with exactly 2 distinct values — likely boolean flags.

- `m_bDisabled`
- `m_bInDevelopment`
- `m_bLaneTestingRecommended`
- `m_bNeedsTesting`
- `m_bNewPlayerRecommended`
- `m_bPlayerSelectable`
- `m_eAbilityResourceType`
- `m_mapItemDraftBucketing`
- `m_mapItemDraftCounterWeights`
- `m_mapScalingStats`
- `m_nModelSkin`
- `m_vecAmbientParticleSettings`
- `m_vecAnimGraphDefaultValueOverrides`

---

## Context-Dependent — Flag for Design Decision

Gameplay-relevant but encoding-complex; include only with explicit modeling decision.

- `m_bitsInterruptingStates` — State machine bitmask — states that interrupt this ability
- `m_bitsPostCastEnabledStateMask` — State machine bitmask — which cast states re-enable post-cast
- `m_eAbilityActivation` — Ability type enum — how the ability is activated
- `m_eAbilityType` — Ability type enum — category (passive/active/etc)
- `m_nAbilityBehaviors` — Ability behavior bitmask — bitfield of EAbilityBehavior flags
- `m_nAbilityTargetTypes` — Ability target type enum — valid target types

---

## Broken Localization References

10 token references failed to resolve.

- `m_vecHeroTags[0]` on `hero_drifter`: token `#Citadel_Drifter_HeroTag_1`
- `m_vecHeroTags[1]` on `hero_drifter`: token `#Citadel_Drifter_HeroTag_2`
- `m_vecHeroTags[2]` on `hero_drifter`: token `#Citadel_Drifter_HeroTag_3`
- `m_vecHeroTags[0]` on `hero_frank`: token `#Citadel_Frank_HeroTag_1`
- `m_vecHeroTags[1]` on `hero_frank`: token `#Citadel_Frank_HeroTag_2`
- `m_vecHeroTags[2]` on `hero_frank`: token `#Citadel_Frank_HeroTag_3`
- `m_vecHeroTags[0]` on `hero_bookworm`: token `#Citadel_Bookworm_HeroTag_1`
- `m_vecHeroTags[1]` on `hero_bookworm`: token `#Citadel_Bookworm_HeroTag_2`
- `m_vecHeroTags[2]` on `hero_bookworm`: token `#Citadel_Bookworm_HeroTag_3`
- `m_strHeroSearchName` on `hero_airheart`: token `#hero_airheart_search`

---

## Quarantined (unknowns.jsonl)

2 keys sent to `unknowns.jsonl` for human review.

| Key | Distinct Values | Note |
|---|---|---|
| `m_mapItemDraftBucketing` | 2 | binary (Good, Normal) — possible boolean flag |
| `m_vecAmbientParticleSettings` | 2 | binary (ability_apply, palm_R) — possible boolean flag |
