"""
NovelForge AI — Power State Repository & Historical State Reconstructor
Phase 3: High-Performance SQLite Power & Progression Storage
"""
from __future__ import annotations
import sqlite3
import json
import uuid
import datetime
import os
from typing import List, Dict, Optional, Any, Tuple

from novelforge.schemas.power_models import (
    PowerSystem, PowerTierDefinition, PowerStageDefinition, CharacterPowerState,
    PowerVector, PowerPotential, EnergyPool, ProgressionEvent, ProgressionTrigger,
    Mutation, MutationCategory, MutationStability, Ability, AbilityType, MasteryRank,
    Technique, TechniqueType, Equipment, EquipmentRarity, EquipmentSlot,
    EquipmentOwnershipRecord, StatusEffect, StatusEffectType
)


class PowerRepository:
    def __init__(self, db_path: str = "novelforge/database/novelforge.sqlite3", conn: Optional[sqlite3.Connection] = None):
        self.db_path = db_path
        if conn is not None:
            self.conn = conn
        else:
            if db_path != ":memory:":
                os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS power_systems (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    system_type TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    energy_type TEXT NOT NULL,
                    tiers_data TEXT DEFAULT '[]',
                    rules_data TEXT DEFAULT '{}',
                    created_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS character_power_states (
                    id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    story_id TEXT NOT NULL,
                    system_id TEXT NOT NULL,
                    current_tier INTEGER NOT NULL,
                    current_stage TEXT NOT NULL,
                    tier_name TEXT DEFAULT '',
                    power_vector_data TEXT DEFAULT '{}',
                    potential_data TEXT DEFAULT '{}',
                    energy_pools_data TEXT DEFAULT '[]',
                    active_buffs_data TEXT DEFAULT '[]',
                    conditions_data TEXT DEFAULT '[]',
                    raw_combat_rating REAL DEFAULT 0.0,
                    chapter_acquired INTEGER DEFAULT 1,
                    is_active INTEGER DEFAULT 1,
                    updated_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS progression_events (
                    id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    story_id TEXT NOT NULL,
                    system_id TEXT NOT NULL,
                    from_tier INTEGER NOT NULL,
                    from_stage TEXT NOT NULL,
                    to_tier INTEGER NOT NULL,
                    to_stage TEXT NOT NULL,
                    chapter_number INTEGER NOT NULL,
                    trigger_type TEXT NOT NULL,
                    catalyst_description TEXT DEFAULT '',
                    cost_paid_data TEXT DEFAULT '{}',
                    bottleneck_broken INTEGER DEFAULT 1,
                    success INTEGER DEFAULT 1,
                    failure_reason TEXT,
                    stat_growth_data TEXT DEFAULT '{}',
                    created_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS mutations (
                    id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    stability TEXT NOT NULL,
                    tier INTEGER DEFAULT 1,
                    stat_modifiers_data TEXT DEFAULT '{}',
                    abilities_granted_data TEXT DEFAULT '[]',
                    drawbacks_data TEXT DEFAULT '[]',
                    triggers_data TEXT DEFAULT '[]',
                    hidden_from_character INTEGER DEFAULT 0,
                    hidden_from_world INTEGER DEFAULT 0,
                    chapter_manifested INTEGER DEFAULT 1,
                    created_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS abilities (
                    id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    ability_type TEXT NOT NULL,
                    mastery TEXT NOT NULL,
                    energy_cost REAL DEFAULT 20.0,
                    energy_type TEXT NOT NULL,
                    cooldown_scenes INTEGER DEFAULT 0,
                    cast_time_seconds REAL DEFAULT 1.0,
                    range_meters REAL DEFAULT 5.0,
                    aoe_radius_meters REAL DEFAULT 0.0,
                    damage_type TEXT DEFAULT 'Kinetic',
                    description TEXT DEFAULT '',
                    requirements_data TEXT DEFAULT '{}',
                    synergies_data TEXT DEFAULT '[]',
                    counter_types_data TEXT DEFAULT '[]',
                    chapter_unlocked INTEGER DEFAULT 1,
                    last_used_chapter INTEGER,
                    created_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS techniques (
                    id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    technique_type TEXT NOT NULL,
                    rank TEXT DEFAULT 'Common',
                    current_level INTEGER DEFAULT 1,
                    max_level INTEGER DEFAULT 9,
                    requirements_data TEXT DEFAULT '{}',
                    evolution_path_data TEXT DEFAULT '[]',
                    stat_modifiers_data TEXT DEFAULT '{}',
                    description TEXT DEFAULT '',
                    chapter_learned INTEGER DEFAULT 1,
                    created_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS equipment (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    rarity TEXT NOT NULL,
                    slot TEXT NOT NULL,
                    current_owner_id TEXT,
                    current_durability REAL DEFAULT 100.0,
                    max_durability REAL DEFAULT 100.0,
                    is_bound INTEGER DEFAULT 0,
                    attributes_data TEXT DEFAULT '{}',
                    passive_effects_data TEXT DEFAULT '[]',
                    active_skills_data TEXT DEFAULT '[]',
                    spirit_resonance REAL DEFAULT 0.0,
                    evolution_tier INTEGER DEFAULT 1,
                    is_destroyed INTEGER DEFAULT 0,
                    chapter_created INTEGER DEFAULT 1,
                    destruction_chapter INTEGER,
                    created_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS equipment_history (
                    id TEXT PRIMARY KEY,
                    equipment_id TEXT NOT NULL,
                    previous_owner_id TEXT,
                    new_owner_id TEXT,
                    chapter_transferred INTEGER NOT NULL,
                    transfer_reason TEXT NOT NULL,
                    timestamp TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS status_effects (
                    id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    effect_type TEXT NOT NULL,
                    severity REAL DEFAULT 1.0,
                    duration_scenes INTEGER DEFAULT 1,
                    stat_penalties_data TEXT DEFAULT '{}',
                    description TEXT DEFAULT '',
                    chapter_applied INTEGER DEFAULT 1,
                    created_at TEXT
                );
            """)

    # =========================================================================
    # POWER SYSTEMS
    # =========================================================================

    def create_power_system(self, system: PowerSystem) -> PowerSystem:
        with self.conn:
            tiers_json = json.dumps([t.to_dict() if hasattr(t, "to_dict") else t for t in system.tiers])
            self.conn.execute("""
                INSERT OR REPLACE INTO power_systems (
                    id, story_id, name, system_type, description, energy_type, tiers_data, rules_data, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                system.id,
                system.story_id,
                system.name,
                system.system_type.value if hasattr(system.system_type, "value") else str(system.system_type),
                system.description,
                system.energy_type.value if hasattr(system.energy_type, "value") else str(system.energy_type),
                tiers_json,
                json.dumps(system.rules),
                system.created_at
            ))
        return system

    def get_power_system(self, system_id: str) -> Optional[PowerSystem]:
        cur = self.conn.execute("SELECT * FROM power_systems WHERE id = ?", (system_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_power_system(row)

    def get_power_systems_for_story(self, story_id: str) -> List[PowerSystem]:
        cur = self.conn.execute("SELECT * FROM power_systems WHERE story_id = ?", (story_id,))
        return [self._row_to_power_system(row) for row in cur.fetchall()]

    def _row_to_power_system(self, row: sqlite3.Row) -> PowerSystem:
        tiers_raw = json.loads(row["tiers_data"] or "[]")
        tiers = [PowerTierDefinition.from_dict(t) for t in tiers_raw]
        return PowerSystem(
            id=row["id"],
            story_id=row["story_id"],
            name=row["name"],
            system_type=row["system_type"],
            description=row["description"],
            energy_type=row["energy_type"],
            tiers=tiers,
            rules=json.loads(row["rules_data"] or "{}"),
            created_at=row["created_at"],
        )

    # =========================================================================
    # CHARACTER POWER STATES
    # =========================================================================

    def create_or_update_character_power(self, state: CharacterPowerState) -> CharacterPowerState:
        state.calculate_combat_rating()
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO character_power_states (
                    id, character_id, story_id, system_id, current_tier, current_stage, tier_name,
                    power_vector_data, potential_data, energy_pools_data, active_buffs_data, conditions_data,
                    raw_combat_rating, chapter_acquired, is_active, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                state.id,
                state.character_id,
                state.story_id,
                state.system_id,
                state.current_tier,
                state.current_stage,
                state.tier_name,
                json.dumps(state.power_vector.to_dict() if hasattr(state.power_vector, "to_dict") else state.power_vector),
                json.dumps(state.potential.to_dict() if hasattr(state.potential, "to_dict") else state.potential),
                json.dumps([p.to_dict() if hasattr(p, "to_dict") else p for p in state.energy_pools]),
                json.dumps(state.active_buffs),
                json.dumps(state.conditions),
                state.raw_combat_rating,
                state.chapter_acquired,
                1 if state.is_active else 0,
                datetime.datetime.utcnow().isoformat(),
            ))
        return state

    def get_character_power_state(self, character_id: str, at_chapter: Optional[int] = None) -> Optional[CharacterPowerState]:
        # If at_chapter is specified, find the power state active at that chapter
        if at_chapter is not None:
            cur = self.conn.execute("""
                SELECT * FROM character_power_states
                WHERE character_id = ? AND chapter_acquired <= ?
                ORDER BY chapter_acquired DESC, updated_at DESC LIMIT 1
            """, (character_id, at_chapter))
        else:
            cur = self.conn.execute("""
                SELECT * FROM character_power_states
                WHERE character_id = ? AND is_active = 1
                ORDER BY chapter_acquired DESC, updated_at DESC LIMIT 1
            """, (character_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_character_power_state(row)

    def _row_to_character_power_state(self, row: sqlite3.Row) -> CharacterPowerState:
        return CharacterPowerState(
            id=row["id"],
            character_id=row["character_id"],
            story_id=row["story_id"],
            system_id=row["system_id"],
            current_tier=row["current_tier"],
            current_stage=row["current_stage"],
            tier_name=row["tier_name"],
            power_vector=PowerVector.from_dict(json.loads(row["power_vector_data"] or "{}")),
            potential=PowerPotential.from_dict(json.loads(row["potential_data"] or "{}")),
            energy_pools=[EnergyPool.from_dict(p) for p in json.loads(row["energy_pools_data"] or "[]")],
            active_buffs=json.loads(row["active_buffs_data"] or "[]"),
            conditions=json.loads(row["conditions_data"] or "[]"),
            raw_combat_rating=row["raw_combat_rating"],
            chapter_acquired=row["chapter_acquired"],
            is_active=bool(row["is_active"]),
            updated_at=row["updated_at"],
        )

    # =========================================================================
    # PROGRESSION EVENTS
    # =========================================================================

    def record_progression_event(self, event: ProgressionEvent) -> ProgressionEvent:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO progression_events (
                    id, character_id, story_id, system_id, from_tier, from_stage, to_tier, to_stage,
                    chapter_number, trigger_type, catalyst_description, cost_paid_data, bottleneck_broken,
                    success, failure_reason, stat_growth_data, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.id,
                event.character_id,
                event.story_id,
                event.system_id,
                event.from_tier,
                event.from_stage,
                event.to_tier,
                event.to_stage,
                event.chapter_number,
                event.trigger_type.value if hasattr(event.trigger_type, "value") else str(event.trigger_type),
                event.catalyst_description,
                json.dumps(event.cost_paid),
                1 if event.bottleneck_broken else 0,
                1 if event.success else 0,
                event.failure_reason,
                json.dumps(event.stat_growth),
                event.created_at,
            ))
        return event

    def get_progression_history(self, character_id: str, up_to_chapter: Optional[int] = None) -> List[ProgressionEvent]:
        if up_to_chapter is not None:
            cur = self.conn.execute("""
                SELECT * FROM progression_events
                WHERE character_id = ? AND chapter_number <= ?
                ORDER BY chapter_number ASC, created_at ASC
            """, (character_id, up_to_chapter))
        else:
            cur = self.conn.execute("""
                SELECT * FROM progression_events
                WHERE character_id = ?
                ORDER BY chapter_number ASC, created_at ASC
            """, (character_id,))
        return [self._row_to_progression_event(r) for r in cur.fetchall()]

    def _row_to_progression_event(self, row: sqlite3.Row) -> ProgressionEvent:
        return ProgressionEvent(
            id=row["id"],
            character_id=row["character_id"],
            story_id=row["story_id"],
            system_id=row["system_id"],
            from_tier=row["from_tier"],
            from_stage=row["from_stage"],
            to_tier=row["to_tier"],
            to_stage=row["to_stage"],
            chapter_number=row["chapter_number"],
            trigger_type=row["trigger_type"],
            catalyst_description=row["catalyst_description"],
            cost_paid=json.loads(row["cost_paid_data"] or "{}"),
            bottleneck_broken=bool(row["bottleneck_broken"]),
            success=bool(row["success"]),
            failure_reason=row["failure_reason"],
            stat_growth=json.loads(row["stat_growth_data"] or "{}"),
            created_at=row["created_at"],
        )

    # =========================================================================
    # MUTATIONS
    # =========================================================================

    def create_mutation(self, mutation: Mutation) -> Mutation:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO mutations (
                    id, character_id, story_id, name, category, stability, tier,
                    stat_modifiers_data, abilities_granted_data, drawbacks_data, triggers_data,
                    hidden_from_character, hidden_from_world, chapter_manifested, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mutation.id,
                mutation.character_id,
                mutation.story_id,
                mutation.name,
                mutation.category.value if hasattr(mutation.category, "value") else str(mutation.category),
                mutation.stability.value if hasattr(mutation.stability, "value") else str(mutation.stability),
                mutation.tier,
                json.dumps(mutation.stat_modifiers),
                json.dumps(mutation.abilities_granted),
                json.dumps(mutation.drawbacks),
                json.dumps(mutation.triggers),
                1 if mutation.hidden_from_character else 0,
                1 if mutation.hidden_from_world else 0,
                mutation.chapter_manifested,
                mutation.created_at,
            ))
        return mutation

    def update_mutation(self, mutation: Mutation) -> Mutation:
        return self.create_mutation(mutation)

    def get_mutations_for_character(
        self,
        character_id: str,
        at_chapter: Optional[int] = None,
        include_hidden_char: bool = True,
        include_hidden_world: bool = True
    ) -> List[Mutation]:
        query = "SELECT * FROM mutations WHERE character_id = ?"
        params = [character_id]
        if at_chapter is not None:
            query += " AND chapter_manifested <= ?"
            params.append(at_chapter)
        if not include_hidden_char:
            query += " AND hidden_from_character = 0"
        if not include_hidden_world:
            query += " AND hidden_from_world = 0"
        query += " ORDER BY tier DESC, chapter_manifested ASC"
        cur = self.conn.execute(query, tuple(params))
        return [self._row_to_mutation(r) for r in cur.fetchall()]

    def _row_to_mutation(self, row: sqlite3.Row) -> Mutation:
        return Mutation(
            id=row["id"],
            character_id=row["character_id"],
            story_id=row["story_id"],
            name=row["name"],
            category=row["category"],
            stability=row["stability"],
            tier=row["tier"],
            stat_modifiers=json.loads(row["stat_modifiers_data"] or "{}"),
            abilities_granted=json.loads(row["abilities_granted_data"] or "[]"),
            drawbacks=json.loads(row["drawbacks_data"] or "[]"),
            triggers=json.loads(row["triggers_data"] or "[]"),
            hidden_from_character=bool(row["hidden_from_character"]),
            hidden_from_world=bool(row["hidden_from_world"]),
            chapter_manifested=row["chapter_manifested"],
            created_at=row["created_at"],
        )

    # =========================================================================
    # ABILITIES & TECHNIQUES
    # =========================================================================

    def create_ability(self, ability: Ability) -> Ability:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO abilities (
                    id, character_id, story_id, name, ability_type, mastery, energy_cost, energy_type,
                    cooldown_scenes, cast_time_seconds, range_meters, aoe_radius_meters, damage_type,
                    description, requirements_data, synergies_data, counter_types_data, chapter_unlocked,
                    last_used_chapter, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ability.id,
                ability.character_id,
                ability.story_id,
                ability.name,
                ability.ability_type.value if hasattr(ability.ability_type, "value") else str(ability.ability_type),
                ability.mastery.value if hasattr(ability.mastery, "value") else str(ability.mastery),
                ability.energy_cost,
                ability.energy_type.value if hasattr(ability.energy_type, "value") else str(ability.energy_type),
                ability.cooldown_scenes,
                ability.cast_time_seconds,
                ability.range_meters,
                ability.aoe_radius_meters,
                ability.damage_type,
                ability.description,
                json.dumps(ability.requirements),
                json.dumps(ability.synergies),
                json.dumps(ability.counter_types),
                ability.chapter_unlocked,
                ability.last_used_chapter,
                ability.created_at,
            ))
        return ability

    def update_ability(self, ability: Ability) -> Ability:
        return self.create_ability(ability)

    def get_abilities_for_character(self, character_id: str, at_chapter: Optional[int] = None) -> List[Ability]:
        if at_chapter is not None:
            cur = self.conn.execute("""
                SELECT * FROM abilities WHERE character_id = ? AND chapter_unlocked <= ?
                ORDER BY chapter_unlocked ASC, name ASC
            """, (character_id, at_chapter))
        else:
            cur = self.conn.execute("""
                SELECT * FROM abilities WHERE character_id = ? ORDER BY chapter_unlocked ASC, name ASC
            """, (character_id,))
        return [self._row_to_ability(r) for r in cur.fetchall()]

    def _row_to_ability(self, row: sqlite3.Row) -> Ability:
        return Ability(
            id=row["id"],
            character_id=row["character_id"],
            story_id=row["story_id"],
            name=row["name"],
            ability_type=row["ability_type"],
            mastery=row["mastery"],
            energy_cost=row["energy_cost"],
            energy_type=row["energy_type"],
            cooldown_scenes=row["cooldown_scenes"],
            cast_time_seconds=row["cast_time_seconds"],
            range_meters=row["range_meters"],
            aoe_radius_meters=row["aoe_radius_meters"],
            damage_type=row["damage_type"],
            description=row["description"],
            requirements=json.loads(row["requirements_data"] or "{}"),
            synergies=json.loads(row["synergies_data"] or "[]"),
            counter_types=json.loads(row["counter_types_data"] or "[]"),
            chapter_unlocked=row["chapter_unlocked"],
            last_used_chapter=row["last_used_chapter"],
            created_at=row["created_at"],
        )

    def create_technique(self, technique: Technique) -> Technique:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO techniques (
                    id, character_id, story_id, name, technique_type, rank, current_level, max_level,
                    requirements_data, evolution_path_data, stat_modifiers_data, description,
                    chapter_learned, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                technique.id,
                technique.character_id,
                technique.story_id,
                technique.name,
                technique.technique_type.value if hasattr(technique.technique_type, "value") else str(technique.technique_type),
                technique.rank,
                technique.current_level,
                technique.max_level,
                json.dumps(technique.requirements),
                json.dumps(technique.evolution_path),
                json.dumps(technique.stat_modifiers),
                technique.description,
                technique.chapter_learned,
                technique.created_at,
            ))
        return technique

    def get_techniques_for_character(self, character_id: str, at_chapter: Optional[int] = None) -> List[Technique]:
        if at_chapter is not None:
            cur = self.conn.execute("""
                SELECT * FROM techniques WHERE character_id = ? AND chapter_learned <= ?
                ORDER BY chapter_learned ASC
            """, (character_id, at_chapter))
        else:
            cur = self.conn.execute("""
                SELECT * FROM techniques WHERE character_id = ? ORDER BY chapter_learned ASC
            """, (character_id,))
        return [self._row_to_technique(r) for r in cur.fetchall()]

    def _row_to_technique(self, row: sqlite3.Row) -> Technique:
        return Technique(
            id=row["id"],
            character_id=row["character_id"],
            story_id=row["story_id"],
            name=row["name"],
            technique_type=row["technique_type"],
            rank=row["rank"],
            current_level=row["current_level"],
            max_level=row["max_level"],
            requirements=json.loads(row["requirements_data"] or "{}"),
            evolution_path=json.loads(row["evolution_path_data"] or "[]"),
            stat_modifiers=json.loads(row["stat_modifiers_data"] or "{}"),
            description=row["description"],
            chapter_learned=row["chapter_learned"],
            created_at=row["created_at"],
        )

    # =========================================================================
    # EQUIPMENT & ARTIFACT ENGINE
    # =========================================================================

    def create_equipment(self, item: Equipment) -> Equipment:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO equipment (
                    id, story_id, name, rarity, slot, current_owner_id, current_durability, max_durability,
                    is_bound, attributes_data, passive_effects_data, active_skills_data, spirit_resonance,
                    evolution_tier, is_destroyed, chapter_created, destruction_chapter, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.id,
                item.story_id,
                item.name,
                item.rarity.value if hasattr(item.rarity, "value") else str(item.rarity),
                item.slot.value if hasattr(item.slot, "value") else str(item.slot),
                item.current_owner_id,
                item.current_durability,
                item.max_durability,
                1 if item.is_bound else 0,
                json.dumps(item.attributes),
                json.dumps(item.passive_effects),
                json.dumps(item.active_skills),
                item.spirit_resonance,
                item.evolution_tier,
                1 if item.is_destroyed else 0,
                item.chapter_created,
                item.destruction_chapter,
                item.created_at,
            ))
        return item

    def get_equipment(self, equipment_id: str) -> Optional[Equipment]:
        cur = self.conn.execute("SELECT * FROM equipment WHERE id = ?", (equipment_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_equipment(row)

    def get_equipment_for_character(self, character_id: str, at_chapter: Optional[int] = None) -> List[Equipment]:
        if at_chapter is not None:
            # Check ownership at chapter: equipment must be created <= at_chapter, and not destroyed before at_chapter
            # Also check ownership history up to that chapter
            cur = self.conn.execute("""
                SELECT * FROM equipment
                WHERE current_owner_id = ? AND chapter_created <= ?
                AND (is_destroyed = 0 OR destruction_chapter > ?)
            """, (character_id, at_chapter, at_chapter))
        else:
            cur = self.conn.execute("""
                SELECT * FROM equipment WHERE current_owner_id = ? AND is_destroyed = 0
            """, (character_id,))
        return [self._row_to_equipment(r) for r in cur.fetchall()]

    def transfer_equipment(
        self,
        equipment_id: str,
        new_owner_id: Optional[str],
        chapter_number: int,
        reason: str
    ) -> EquipmentOwnershipRecord:
        eq = self.get_equipment(equipment_id)
        if not eq:
            raise ValueError(f"Equipment {equipment_id} not found")
        prev_owner = eq.current_owner_id
        eq.current_owner_id = new_owner_id
        self.create_equipment(eq)

        rec = EquipmentOwnershipRecord(
            id=str(uuid.uuid4()),
            equipment_id=equipment_id,
            previous_owner_id=prev_owner,
            new_owner_id=new_owner_id,
            chapter_transferred=chapter_number,
            transfer_reason=reason,
            timestamp=datetime.datetime.utcnow().isoformat(),
        )
        with self.conn:
            self.conn.execute("""
                INSERT INTO equipment_history (
                    id, equipment_id, previous_owner_id, new_owner_id, chapter_transferred, transfer_reason, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                rec.id, rec.equipment_id, rec.previous_owner_id, rec.new_owner_id,
                rec.chapter_transferred, rec.transfer_reason, rec.timestamp
            ))
        return rec

    def destroy_equipment(self, equipment_id: str, chapter_number: int) -> Equipment:
        eq = self.get_equipment(equipment_id)
        if not eq:
            raise ValueError(f"Equipment {equipment_id} not found")
        eq.is_destroyed = True
        eq.destruction_chapter = chapter_number
        eq.current_durability = 0.0
        self.create_equipment(eq)
        self.transfer_equipment(equipment_id, None, chapter_number, "DESTROYED")
        return eq

    def get_equipment_history(self, equipment_id: str) -> List[EquipmentOwnershipRecord]:
        cur = self.conn.execute("""
            SELECT * FROM equipment_history WHERE equipment_id = ? ORDER BY chapter_transferred ASC, timestamp ASC
        """, (equipment_id,))
        return [
            EquipmentOwnershipRecord(
                id=r["id"],
                equipment_id=r["equipment_id"],
                previous_owner_id=r["previous_owner_id"],
                new_owner_id=r["new_owner_id"],
                chapter_transferred=r["chapter_transferred"],
                transfer_reason=r["transfer_reason"],
                timestamp=r["timestamp"],
            ) for r in cur.fetchall()
        ]

    def _row_to_equipment(self, row: sqlite3.Row) -> Equipment:
        return Equipment(
            id=row["id"],
            story_id=row["story_id"],
            name=row["name"],
            rarity=row["rarity"],
            slot=row["slot"],
            current_owner_id=row["current_owner_id"],
            current_durability=row["current_durability"],
            max_durability=row["max_durability"],
            is_bound=bool(row["is_bound"]),
            attributes=json.loads(row["attributes_data"] or "{}"),
            passive_effects=json.loads(row["passive_effects_data"] or "[]"),
            active_skills=json.loads(row["active_skills_data"] or "[]"),
            spirit_resonance=row["spirit_resonance"],
            evolution_tier=row["evolution_tier"],
            is_destroyed=bool(row["is_destroyed"]),
            chapter_created=row["chapter_created"],
            destruction_chapter=row["destruction_chapter"],
            created_at=row["created_at"],
        )

    # =========================================================================
    # STATUS EFFECTS
    # =========================================================================

    def apply_status_effect(self, effect: StatusEffect) -> StatusEffect:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO status_effects (
                    id, character_id, effect_type, severity, duration_scenes, stat_penalties_data,
                    description, chapter_applied, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                effect.id,
                effect.character_id,
                effect.effect_type.value if hasattr(effect.effect_type, "value") else str(effect.effect_type),
                effect.severity,
                effect.duration_scenes,
                json.dumps(effect.stat_penalties),
                effect.description,
                effect.chapter_applied,
                effect.created_at,
            ))
        return effect

    def get_active_status_effects(self, character_id: str, current_chapter: Optional[int] = None) -> List[StatusEffect]:
        if current_chapter is not None:
            cur = self.conn.execute("""
                SELECT * FROM status_effects
                WHERE character_id = ? AND chapter_applied <= ?
                ORDER BY chapter_applied DESC
            """, (character_id, current_chapter))
        else:
            cur = self.conn.execute("""
                SELECT * FROM status_effects WHERE character_id = ? ORDER BY chapter_applied DESC
            """, (character_id,))
        return [
            StatusEffect(
                id=r["id"],
                character_id=r["character_id"],
                effect_type=r["effect_type"],
                severity=r["severity"],
                duration_scenes=r["duration_scenes"],
                stat_penalties=json.loads(r["stat_penalties_data"] or "{}"),
                description=r["description"],
                chapter_applied=r["chapter_applied"],
                created_at=r["created_at"],
            ) for r in cur.fetchall()
        ]
