"""
NovelForge AI — Ability & Technique Service
Phase 3: 17 Ability Types, 5 Mastery Ranks, and Martial Evolution Engine
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any, Tuple
import uuid
import datetime

from novelforge.database.power_repository import PowerRepository
from novelforge.schemas.power_models import (
    Ability, AbilityType, MasteryRank, Technique, TechniqueType, EnergyType
)

MASTERY_LADDER = [
    MasteryRank.INITIATE,
    MasteryRank.PRACTITIONER,
    MasteryRank.ADEPT,
    MasteryRank.MASTER,
    MasteryRank.GRANDMASTER,
]


class AbilityService:
    def __init__(self, power_repo: PowerRepository):
        self.power_repo = power_repo

    def register_ability(
        self,
        character_id: str,
        story_id: str,
        name: str,
        ability_type: AbilityType,
        mastery: MasteryRank = MasteryRank.INITIATE,
        energy_cost: float = 20.0,
        energy_type: EnergyType = EnergyType.QI,
        cooldown_scenes: int = 0,
        cast_time_seconds: float = 1.0,
        range_meters: float = 5.0,
        aoe_radius_meters: float = 0.0,
        damage_type: str = "Kinetic",
        description: str = "",
        requirements: Optional[Dict[str, Any]] = None,
        synergies: Optional[List[str]] = None,
        counter_types: Optional[List[str]] = None,
        chapter_unlocked: int = 1,
    ) -> Ability:
        ability = Ability(
            id=str(uuid.uuid4()),
            character_id=character_id,
            story_id=story_id,
            name=name,
            ability_type=ability_type,
            mastery=mastery,
            energy_cost=energy_cost,
            energy_type=energy_type,
            cooldown_scenes=cooldown_scenes,
            cast_time_seconds=cast_time_seconds,
            range_meters=range_meters,
            aoe_radius_meters=aoe_radius_meters,
            damage_type=damage_type,
            description=description,
            requirements=requirements or {},
            synergies=synergies or [],
            counter_types=counter_types or [],
            chapter_unlocked=chapter_unlocked,
        )
        return self.power_repo.create_ability(ability)

    def check_ability_usable(
        self,
        character_id: str,
        ability_id: str,
        current_chapter: int,
    ) -> Tuple[bool, Optional[str]]:
        cur = self.power_repo.conn.execute("SELECT * FROM abilities WHERE id = ?", (ability_id,))
        row = cur.fetchone()
        if not row:
            return False, f"Ability {ability_id} not found."
        ability = self.power_repo._row_to_ability(row)

        if ability.character_id != character_id:
            return False, f"Character {character_id} does not possess ability '{ability.name}'."

        if current_chapter < ability.chapter_unlocked:
            return False, f"Ability '{ability.name}' has not been unlocked yet (unlocked at Chapter {ability.chapter_unlocked}, current is Chapter {current_chapter})."

        # Check cooldown: if cooldown_scenes > 0 and last_used_chapter is equal to current_chapter
        if ability.cooldown_scenes > 0 and ability.last_used_chapter is not None:
            # If used in same chapter and cooldown covers it
            if current_chapter == ability.last_used_chapter and ability.cooldown_scenes > 1:
                return False, f"Ability '{ability.name}' is on cooldown (last used Chapter {ability.last_used_chapter}, requires {ability.cooldown_scenes} chapters/scenes of rest)."

        # Check energy availability
        state = self.power_repo.get_character_power_state(character_id, at_chapter=current_chapter)
        if state:
            for pool in state.energy_pools:
                if pool.energy_type == ability.energy_type:
                    effective_cost = ability.energy_cost / ability.get_mastery_multiplier()
                    if pool.current < effective_cost:
                        return False, f"Insufficient {pool.energy_type.value}: Requires {effective_cost:.1f}, but only {pool.current:.1f} available."

        return True, None

    def record_ability_usage(self, ability_id: str, chapter_number: int) -> Ability:
        cur = self.power_repo.conn.execute("SELECT * FROM abilities WHERE id = ?", (ability_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Ability {ability_id} not found")
        ability = self.power_repo._row_to_ability(row)
        ability.last_used_chapter = chapter_number
        return self.power_repo.update_ability(ability)

    def advance_mastery(self, ability_id: str, new_rank: MasteryRank) -> Ability:
        cur = self.power_repo.conn.execute("SELECT * FROM abilities WHERE id = ?", (ability_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Ability {ability_id} not found")
        ability = self.power_repo._row_to_ability(row)
        ability.mastery = new_rank
        return self.power_repo.update_ability(ability)

    def register_technique(
        self,
        character_id: str,
        story_id: str,
        name: str,
        technique_type: TechniqueType,
        rank: str = "Common",
        current_level: int = 1,
        max_level: int = 9,
        requirements: Optional[Dict[str, Any]] = None,
        evolution_path: Optional[List[str]] = None,
        stat_modifiers: Optional[Dict[str, float]] = None,
        description: str = "",
        chapter_learned: int = 1,
    ) -> Technique:
        technique = Technique(
            id=str(uuid.uuid4()),
            character_id=character_id,
            story_id=story_id,
            name=name,
            technique_type=technique_type,
            rank=rank,
            current_level=current_level,
            max_level=max_level,
            requirements=requirements or {},
            evolution_path=evolution_path or [],
            stat_modifiers=stat_modifiers or {},
            description=description,
            chapter_learned=chapter_learned,
        )
        return self.power_repo.create_technique(technique)

    def advance_technique(self, technique_id: str, levels: int = 1) -> Technique:
        cur = self.power_repo.conn.execute("SELECT * FROM techniques WHERE id = ?", (technique_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Technique {technique_id} not found")
        technique = self.power_repo._row_to_technique(row)
        technique.current_level = min(technique.max_level, technique.current_level + levels)
        # Scale stat modifiers proportionally with levels
        scale = 1.0 + (technique.current_level * 0.1)
        for k in technique.stat_modifiers:
            technique.stat_modifiers[k] = round(technique.stat_modifiers[k] * 1.15, 2)
        return self.power_repo.create_technique(technique)
