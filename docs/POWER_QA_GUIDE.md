# NovelForge AI — Power QA & Continuity Guide
**Phase 3: Automated Quality Assurance for Progression Fantasy**

---

## 1. Overview

The Power QA Guard is the automated verification system that inspects novel draft scenes before they are accepted into canon. It acts as an automated editor catching:
1. Plot holes regarding strength levels.
2. Inconsistent realm titles.
3. Flashback leaks (anachronistic powers).
4. Forgotten item destructions.
5. Cooldown cheating.

---

## 2. Invariant Rules & Violation Severity

| Rule Code | Severity | Trigger Condition | Suggested Fix |
| :--- | :--- | :--- | :--- |
| **`UNINITIALIZED_POWER_STATE`** | CRITICAL | Character has no canonical power state at audited chapter. | Initialize character power state before drafting scene. |
| **`IMPOSSIBLE_TIER_CLAIM`** | CRITICAL | Text claims character is Tier $X$, but database has Tier $Y \neq X$. | Align narrative text to canonical tier or execute breakthrough. |
| **`IMPOSSIBLE_STAGE_CLAIM`** | WARNING | Text claims stage (e.g. Peak) when state is Mid. | Correct dialogue or narrative exposition to true stage. |
| **`HISTORICAL_FLASHBACK_LEAK`** | CRITICAL | An ability unlocked in Chapter $M$ is used in Chapter $N < M$. | Remove anachronistic ability from historical scene. |
| **`UNLEARNED_ABILITY_USAGE`** | CRITICAL | Character uses an ability never registered in story database. | Register ability in character's technique tree first. |
| **`ABILITY_COOLDOWN_VIOLATION`** | WARNING | Ability used in consecutive scenes while on cooldown. | Introduce alternative martial martial strike or rest. |
| **`DESTROYED_EQUIPMENT_WIELDED`**| CRITICAL | Item destroyed in prior chapter is wielded in combat. | Replace item or introduce reforging plot thread. |
| **`ILLEGAL_EQUIPMENT_POSSESSION`**| CRITICAL | Character wields gear belonging to another living character. | Add looting, gift, or disarming narrative event. |
| **`ESCALATION_RUNAWAY`** | WARNING | 3+ breakthroughs occur within 10 chapters without pacing. | Add training setbacks or consolidate bottlenecks. |

---

## 3. Power QA Score Calculation

The Power QA Score starts at $100.0$ and deducts points based on severity:
- **CRITICAL Violation**: $-20.0$ points per occurrence.
- **WARNING Violation**: $-8.0$ points per occurrence.
- **INFO Violation**: $-2.0$ points per occurrence.

A scene is considered **Canon Ready** (`is_valid = True`) only when **zero CRITICAL violations** are present and the score is $\ge 80.0$.
