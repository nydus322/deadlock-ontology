# Nydus — Calibration Questions for Wander

> Hi Wander — only questions that cannot be answered from the data appear here.
> No data science knowledge needed; just in-game observation.
> Answer in whatever form is convenient. We handle the math.

---

## What we already know  (eliminated)

| Category | Entries | How we solved it |
|---|---|---|
| `ability_recharge_time` base=`-1.0` | 1,238 | Engine sentinel — fire rate from weapon stats |
| `tech_damage` + explicit stat + factor | 140 | Formula `base + factor × stat` in the data |
| `ability_charges` (static) | 42 | Integer charge counts, no scaling |

---

## Part A — Formula Verifications  (4 questions)

> We have the data — we just need one confirmed output to lock in the formula.
> Set Training Mode stat slider to each value; read the tooltip.

### V1 — `single stat` on `ETechCooldown`

**Our formula hypothesis**: `base × f(ETechCooldown)`

| Field | Value |
|---|---|
| Hero | hero_base |
| Ability | Zip Line |
| Property | DamageCooldown |
| Base value (stat=0) | **3** |

**Verify at these stat values:**

| Stat Value | Tooltip shows |
|---|---|
| 0 | *(should be 3)* |
| 42 | ? |
| 100 | ? |

### V2 — `tech damage` on `ETechPower`

**Our formula hypothesis**: `base + factor × ETechPower` (scale factor in data: 1.6)

| Field | Value |
|---|---|
| Hero | Astro |
| Ability | Ability Explosive Barrel |
| Property | BarrelDamage |
| Base value (stat=0) | **80** |

**Verify at these stat values:**

| Stat Value | Tooltip shows |
|---|---|
| 0 | *(should be 80)* |
| 42 | ? |
| 100 | ? |

### V3 — `tech duration` on ``

**Our formula hypothesis**: `base × f()`

| Field | Value |
|---|---|
| Hero | Hornet |
| Ability | Hornet Sting |
| Property | DebuffDuration |
| Base value (stat=0) | **5** |

**Verify at these stat values:**

| Stat Value | Tooltip shows |
|---|---|
| 0 | *(should be 5)* |
| 42 | ? |
| 100 | ? |

### V4 — `tech range` on ``

**Our formula hypothesis**: `base × f()`

| Field | Value |
|---|---|
| Hero | Gigawatt |
| Ability | Storm Cloud |
| Property | LightningStrikeRadius |
| Base value (stat=0) | **7m** |

**Verify at these stat values:**

| Stat Value | Tooltip shows |
|---|---|
| 0 | *(should be 7m)* |
| 42 | ? |
| 100 | ? |

---

## Part B — Unknown Formulas  (5 questions)

> These scale functions combine stats in ways not derivable from the data.
> Full calibration needed — 4 data points per question.

### Q1 — `ability recharge time`

| Field | Value |
|---|---|
| Stats involved | `(implied from function name)` |
| Hero | hero_rutger |
| Ability | Rutger Rocket |
| Property | AbilityCooldownBetweenCharge |
| Base value (no stats) | **1** |

**Fill in observed values:**

| Stat Value | What tooltip / dummy shows |
|---|---|
| 0 | *(baseline — should be 1)* |
| 42 | ? |
| 100 | ? |
| 200 | ? |

### Q2 — `ability weapon damage`

| Field | Value |
|---|---|
| Stats involved | `EBaseWeaponDamageIncrease` |
| Hero | Priest |
| Ability | Ability Priest Knockback |
| Property | Damage |
| Base value (no stats) | **60**  *(data factor: 0.8)* |

**Fill in observed values:**

| Stat Value | What tooltip / dummy shows |
|---|---|
| 0 | *(baseline — should be 60)* |
| 42 | ? |
| 100 | ? |
| 200 | ? |

### Q3 — `multi stats`

| Field | Value |
|---|---|
| Stats involved | `EChannelDuration`, `ETechDuration` |
| Hero | Bebop |
| Ability | Bebop Laser Beam |
| Property | AbilityChannelTime |
| Base value (no stats) | **11** |

**Fill in observed values:**

| Stat Value | What tooltip / dummy shows |
|---|---|
| 0 | *(baseline — should be 11)* |
| 42 | ? |
| 100 | ? |
| 200 | ? |

### Q4 — `multi stats`

| Field | Value |
|---|---|
| Stats involved | `ELevelUpBoons`, `EWeaponDamageScale`, `EDamageScale` |
| Hero | Priest |
| Ability | Ability Priest Weaponswap |
| Property | BonusDamage |
| Base value (no stats) | **100**  *(data factor: 3.0)* |

**Fill in observed values:**

| Stat Value | What tooltip / dummy shows |
|---|---|
| 0 | *(baseline — should be 100)* |
| 42 | ? |
| 100 | ? |
| 200 | ? |

### Q5 — `multi stats`

| Field | Value |
|---|---|
| Stats involved | `ETechPower`, `EHealingOutput` |
| Hero | Dynamo |
| Ability | Nikuman |
| Property | HealingPerSecond |
| Base value (no stats) | **25**  *(data factor: 0.4)* |

**Fill in observed values:**

| Stat Value | What tooltip / dummy shows |
|---|---|
| 0 | *(baseline — should be 25)* |
| 42 | ? |
| 100 | ? |
| 200 | ? |

---

## Part C — Hero Identity  (4 questions)

> Some heroes have developer codenames only — no confirmed public name.

### HI1 — `hero_gigawatt`  (ID #2)  |  model: **Gigawatt Prisoner**  |  stage: STAGING

Public name, or any recognition from playtests?

**Answer**: _____________________

### HI2 — `hero_hornet`  (ID #3)  |  model: **Hornet V3**  |  stage: STAGING

Public name, or any recognition from playtests?

**Answer**: _____________________

### HI3 — `hero_astro`  (ID #14)  |  model: **Astro**  |  stage: STAGING

Public name, or any recognition from playtests?

**Answer**: _____________________

### HI4 — `hero_magician`  (ID #60)  |  model: **Magician V2**  |  stage: STAGING

Public name, or any recognition from playtests?

**Answer**: _____________________

---

## Part D — Mechanics  (5 questions)

**M1**: Can you buy two different items that both grant Bullet Armor and receive full value from both, or does one cap out / get diminished?

**Answer**: _____________________

**M2**: Is there a hard cap on Cooldown Reduction? If yes, what is it?

**Answer**: _____________________

**M3**: Lifesteal — do multiple lifesteal items add together directly, or does stacking give diminishing returns?

**Answer**: _____________________

**M4**: The data shows exactly one hero with a `Rage` resource type (not mana/none). Which hero, and how does Rage build / drain?

**Answer**: _____________________

**M5**: For Spirit (tech) power scaling — does the damage formula feel linear across the whole range, or does it cap/curve at high values?

**Answer**: _____________________

---

*Thank you Wander. Every answer closes a formula gap between what the*
*data declares and what the game actually computes.*