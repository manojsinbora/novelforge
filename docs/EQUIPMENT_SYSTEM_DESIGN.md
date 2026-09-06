# NovelForge AI — Equipment & Artifact Engine Design
**Phase 3: Rarity Tiers, Durability, Provenance, and Synergies**

---

## 1. Overview

Equipment and relics are tangible game-changers in web novel progression. A single high-grade sword or defensive jade talisman can reverse a realm gap. The Equipment Engine tracks item ownership, physical durability, active and passive powers, and immutable provenance history across centuries.

---

## 2. The 7 Rarity Tiers

| Rarity | Base Scaling | Spirit Resonance Max | Narrative Typical Scarcity |
| :--- | :--- | :--- | :--- |
| **COMMON** | $1.0\times$ | $0.0$ | Mass-produced mortal iron, standard disciple swords |
| **UNCOMMON** | $1.5\times$ | $0.2$ | Low-tier spirit iron, inscribed talismans |
| **RARE** | $2.5\times$ | $0.4$ | Sect inner court weapons, elder-forged armor |
| **EPIC** | $4.5\times$ | $0.6$ | Family heirlooms, ancient cavern relics |
| **LEGENDARY** | $8.0\times$ | $0.85$ | Sect foundation treasures, named blades of past heroes |
| **MYTHIC** | $15.0\times$ | $1.0$ | World-grade anomalies, fallen god relics |
| **TRANSCENDENT** | $30.0\times$ | $1.0$ | Conceptual constructs, cosmic origin treasures |

---

## 3. Durability & Destruction Rules

- **Current Durability ($0.0 - 100.0$)**:
  - High-tier clashes inflict durability loss proportional to the opponent's strike power and artifact hardness.
  - At $0.0$ durability, the equipment is automatically flagged as `is_destroyed = True` and its `destruction_chapter` is recorded.
- **Destruction Invariant**:
  - Once destroyed, any subsequent chapter depicting a character wielding the item triggers a **`DESTROYED_EQUIPMENT_WIELDED`** violation in Power QA.
  - Only explicit reforging narrative events with rare materials can restore a destroyed relic.

---

## 4. Provenance History & Ownership Tracking

Every transfer of equipment creates an immutable `EquipmentOwnershipRecord`:
- `previous_owner_id` $\to$ `new_owner_id`
- `chapter_transferred`
- `transfer_reason`: `LOOTED`, `GIFTED`, `PURCHASED`, `FORGED`, `STOLEN`, `INHERITED`, or `DESTROYED`

Writing agents cannot spontaneously hand an opponent's signature weapon to the protagonist without an audited transfer or battle loot event!
