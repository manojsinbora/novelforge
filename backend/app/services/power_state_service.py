"""
NovelForge AI — Power State Service
Phase 3: Real-time & Historical Power State Engine
Computes 12D combat vectors, effective combat ratings, and temporal reconstruction.
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any
import uuid
import datetime

from novelforge.database.power_repository import PowerRepository
from novelforge.schemas.power_models import (
    PowerSystem, PowerSystemType, PowerTierDefinition, PowerStageDefinition,
    CharacterPowerState, PowerVector, PowerPotential, EnergyPool, EnergyType
)


DEFAULT_SEVEN_TIERS = [
    ("Novice", 1.0, "The foundation realm. Energy pathways begin opening; physical senses sharpen."),
    ("Intermediate", 2.2, "Energy condenses into liquid form. Skin and bone density increase threefold."),
    ("Master", 4.8, "Energy core forms. Ability to project aura externally and weaponize intent."),
    ("Grand Master", 10.5, "Domain seed awakens. Flight or extreme levitation becomes effortless."),
    ("Great Grand Master", 22.0, "Conceptual resonance. Flesh merges with energetic pathways."),
    ("Sovereign", 48.0, "Domain manifestation. Can manipulate local space and atmospheric intent."),
    ("Transcendent", 100.0, "Complete transcendence of mortal constraints. Conceptual dominion."),
]


class PowerStateService:
    def __init__(self, power_repo: PowerRepository):
        self.power_repo = power_repo

    def create_default_seven_tier_system(self, story_id: str, name: str = "Sevenfold Awakening Cultivation") -> PowerSystem:
        tiers: List[PowerTierDefinition] = []
        for rank, (tier_name, base_mult, desc) in enumerate(DEFAULT_SEVEN_TIERS, start=1):
            stages = [
                PowerStageDefinition(name="Early", order=1, stat_multiplier=1.0, description=f"{tier_name} Early Stage"),
                PowerStageDefinition(name="Mid", order=2, stat_multiplier=1.25, description=f"{tier_name} Mid Stage"),
                PowerStageDefinition(name="Late", order=3, stat_multiplier=1.55, description=f"{tier_name} Late Stage"),
                PowerStageDefinition(name="Peak", order=4, stat_multiplier=1.9, description=f"{tier_name} Peak Stage"),
            ]
            breakthrough_reqs = {
                "min_stage": "Peak",
                "energy_purity_required": round(0.4 + (rank * 0.08), 2),
                "meditation_hours_required": rank * 100,
                "catalyst_required": rank >= 3,
            }
            penalty = {
                "backlash_damage": rank * 15.0,
                "risk_of_qi_deviation": rank >= 4,
            }
            tiers.append(PowerTierDefinition(
                rank=rank,
                name=tier_name,
                description=desc,
                base_multiplier=base_mult,
                stages=stages,
                breakthrough_requirements=breakthrough_reqs,
                bottleneck_description=f"Bottleneck of the {tier_name} realm requiring condensation and comprehension.",
                failure_penalty=penalty,
            ))

        system = PowerSystem(
            id=str(uuid.uuid4()),
            story_id=story_id,
            name=name,
            system_type=PowerSystemType.CULTIVATION,
            description="Universal seven-tier cultivation progression system with sub-realms.",
            energy_type=EnergyType.QI,
            tiers=tiers,
            rules={
                "cross_tier_suppression": 2.0,
                "domain_unlock_tier": 4,
                "allow_hybrid": True
            },
        )
        return self.power_repo.create_power_system(system)

    def initialize_character_power(
        self,
        character_id: str,
        story_id: str,
        system_id: str,
        tier: int = 1,
        stage: str = "Early",
        base_vector: Optional[PowerVector] = None,
        ceiling_tier: int = 7,
        chapter_acquired: int = 1
    ) -> CharacterPowerState:
        system = self.power_repo.get_power_system(system_id)
        tier_name = "Novice"
        if system:
            for t in system.tiers:
                if t.rank == tier:
                    tier_name = t.name
                    break

        vec = base_vector or PowerVector()
        pot = PowerPotential(ceiling_tier=ceiling_tier, bottleneck_difficulty=1.0, growth_rate=1.0)
        pools = [
            EnergyPool(
                energy_type=system.energy_type if system else EnergyType.QI,
                current=100.0 * tier,
                maximum=100.0 * tier,
                purity=0.5,
                density=1.0 * tier,
                regeneration_rate=5.0 * tier
            )
        ]

        state = CharacterPowerState(
            id=str(uuid.uuid4()),
            character_id=character_id,
            story_id=story_id,
            system_id=system_id,
            current_tier=tier,
            current_stage=stage,
            tier_name=tier_name,
            power_vector=vec,
            potential=pot,
            energy_pools=pools,
            chapter_acquired=chapter_acquired,
        )
        state.calculate_combat_rating()
        return self.power_repo.create_or_update_character_power(state)

    def get_effective_power_vector(
        self,
        character_id: str,
        at_chapter: Optional[int] = None
    ) -> PowerVector:
        state = self.power_repo.get_character_power_state(character_id, at_chapter=at_chapter)
        if not state:
            return PowerVector()

        effective = PowerVector.from_dict(state.power_vector.to_dict())

        # 1. Apply active mutations modifiers
        mutations = self.power_repo.get_mutations_for_character(character_id, at_chapter=at_chapter)
        for m in mutations:
            stab = m.stability.value if hasattr(m.stability, "value") else str(m.stability)
            if stab != "DORMANT":
                effective = effective.apply_modifiers(m.stat_modifiers)

        # 2. Apply techniques modifiers
        techniques = self.power_repo.get_techniques_for_character(character_id, at_chapter=at_chapter)
        for t in techniques:
            if t.stat_modifiers:
                effective = effective.apply_modifiers(t.stat_modifiers)

        # 3. Apply equipment attributes
        equipment = self.power_repo.get_equipment_for_character(character_id, at_chapter=at_chapter)
        for eq in equipment:
            if not eq.is_destroyed and eq.attributes:
                effective = effective.apply_modifiers(eq.attributes)

        # 4. Apply status effects (penalties)
        status_effects = self.power_repo.get_active_status_effects(character_id, current_chapter=at_chapter)
        for eff in status_effects:
            if eff.stat_penalties:
                # Penalties are negative or subtracted
                neg_penalties = {k: -abs(v) for k, v in eff.stat_penalties.items()}
                effective = effective.apply_modifiers(neg_penalties)

        return effective

    def get_character_power_dossier(
        self,
        character_id: str,
        at_chapter: Optional[int] = None
    ) -> Dict[str, Any]:
        state = self.power_repo.get_character_power_state(character_id, at_chapter=at_chapter)
        if not state:
            return {"error": f"No power state found for character {character_id}"}

        effective_vector = self.get_effective_power_vector(character_id, at_chapter=at_chapter)
        mutations = self.power_repo.get_mutations_for_character(character_id, at_chapter=at_chapter)
        abilities = self.power_repo.get_abilities_for_character(character_id, at_chapter=at_chapter)
        techniques = self.power_repo.get_techniques_for_character(character_id, at_chapter=at_chapter)
        equipment = self.power_repo.get_equipment_for_character(character_id, at_chapter=at_chapter)
        progression = self.power_repo.get_progression_history(character_id, up_to_chapter=at_chapter)
        status_effects = self.power_repo.get_active_status_effects(character_id, current_chapter=at_chapter)

        # Calculate effective rating with modifiers
        stage_mult = {"Early": 1.0, "Mid": 1.25, "Late": 1.55, "Peak": 1.9}.get(state.current_stage, 1.0)
        tier_mult = 2.0 ** (state.current_tier - 1)
        effective_rating = round(effective_vector.total() * tier_mult * stage_mult, 1)

        return {
            "character_id": character_id,
            "chapter_audited": at_chapter if at_chapter is not None else state.chapter_acquired,
            "tier": state.current_tier,
            "stage": state.current_stage,
            "tier_name": state.tier_name,
            "base_power_vector": state.power_vector.to_dict(),
            "effective_power_vector": effective_vector.to_dict(),
            "raw_combat_rating": state.raw_combat_rating,
            "effective_combat_rating": effective_rating,
            "potential": state.potential.to_dict(),
            "energy_pools": [p.to_dict() for p in state.energy_pools],
            "mutations": [m.to_dict() for m in mutations],
            "abilities": [a.to_dict() for a in abilities],
            "techniques": [t.to_dict() for t in techniques],
            "equipment": [e.to_dict() for e in equipment],
            "progression_history": [p.to_dict() for p in progression],
            "active_status_effects": [s.to_dict() for s in status_effects],
        }
