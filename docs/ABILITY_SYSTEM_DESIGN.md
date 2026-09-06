# NovelForge AI — Ability & Technique System Design
**Phase 3: 17 Ability Types, 5 Mastery Ranks, and Martial Evolution**

---

## 1. Overview

Abilities and Techniques define the practical combat repertoire of characters. While cultivation realms determine energy capacity and base velocity, abilities dictate *how* energy is shaped, directed, and weaponized.

---

## 2. The 17 Canonical Ability Types

1. **OFFENSIVE**: Direct kinetic, elemental, or spiritual damage strikes (e.g. *Void Splitting Palm*).
2. **DEFENSIVE**: Energy shields, barrier spheres, parrying auras (e.g. *Golden Bell Resonator*).
3. **MOVEMENT**: Short-range blinks, wind steps, shadow gliding (e.g. *Seven Step Cloud Tread*).
4. **SENSORY**: Divine sense projection, thermal aura tracking (e.g. *Omnipresent Perception*).
5. **HEALING**: Cellular mending, blood replenishment, meridian detox (e.g. *Spring Bloom Vitality*).
6. **BUFF**: Temporary attribute acceleration, berserk resonance (e.g. *Blood Boiling Stance*).
7. **DEBUFF**: Slowing fields, energy suppression, joint lock (e.g. *Gravity Mire Curse*).
8. **UTILITY**: Invisibility, vocal mimicry, aura concealment (e.g. *Silent Breath Shroud*).
9. **DOMAIN**: Territory control creating favorable physical laws (e.g. *Ashen Sword Domain*).
10. **SUMMONING**: Manifesting spiritual beasts, puppet soldiers, or elemental constructs.
11. **SEALING**: Locking meridians, suppressing artifacts, binding souls (e.g. *Five Element Lock*).
12. **ILLUSION**: Optical trickery, sensory displacement, mirages (e.g. *Moonlight Mirage*).
13. **SOUL**: Direct spiritual damage bypassing physical armor (e.g. *Soul Severing Needle*).
14. **SPATIAL**: Folding space, dimensional tears, compression (e.g. *Void Anchor*).
15. **TEMPORAL**: Micro-delays, acceleration, precognitive echo (e.g. *One-Second Foresight*).
16. **CURSING**: Persistent negative entropy, rot, meridian decay (e.g. *Seven Day Rot Curse*).
17. **PASSIVE**: Constant baseline enhancements, poison immunity, photographic memory.

---

## 3. The 5 Mastery Ranks

Every ability scales non-linearly across five mastery ranks:

| Rank | Multiplier | Energy Cost | Description |
| :--- | :--- | :--- | :--- |
| **Initiate** | $1.0\times$ | $100\%$ | Basic execution; requires full concentration and hand signs. |
| **Practitioner** | $1.3\times$ | $85\%$ | Smooth invocation; reduced telegraphing. |
| **Adept** | $1.7\times$ | $70\%$ | Instant casting; can weave during movement. |
| **Master** | $2.2\times$ | $55\%$ | Can alter trajectory mid-flight; reduced cooldown. |
| **Grandmaster** | $3.0\times$ | $40\%$ | Conceptual mastery; requires no physical motion; bypasses common counters. |

---

## 4. Cooldown & Energy Depletion Continuity

Writing agents are strictly constrained by ability cooldowns:
- If an ability with `cooldown_scenes > 0` was unleashed in Scene 1, it cannot be reused in Scene 2 without incurring meridian backlash or severe energy exhaustion.
- The Power QA Validator flags repetitive spamming of signature trump cards as a **WARNING** or **CRITICAL** continuity error.
