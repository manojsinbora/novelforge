"""
NovelForge AI — Progression & Breakthrough Service
Phase 3: Validated Cultivation & Awakening Breakthroughs
Prevents arbitrary jumps, tracks bottlenecks, and records immutable progression events.
"""
from __future__ import annotations
from typing import Dict, Optional, Any, Tuple
import uuid
import datetime

from novelforge.database.power_repository import PowerRepository
from novelforge.schemas.power_models import (
    ProgressionEvent, ProgressionTrigger, CharacterPowerState, PowerVector, StatusEffect, StatusEffectType
)

STAGE_ORDER = {"Early": 1, "Mid": 2, "Late": 3, "Peak": 4}
ORDER_TO_STAGE = {1: "Early", 2: "Mid", 3: "Late", 4: "Peak"}


class ProgressionService:
    def __init__(self, power_repo: PowerRepository):
        self.power_repo = power_repo

    def validate_breakthrough(
        self,
        character_id: str,
        target_tier: int,
        target_stage: str,
        catalyst: Optional[str] = None,
        canon_override: bool = False
    ) -> Tuple[bool, Optional[str]]:
        state = self.power_repo.get_character_power_state(character_id)
        if not state:
            return False, f"Character {character_id} has no initialized power state."

        if canon_override:
            return True, None

        current_tier = state.current_tier
        current_stage = state.current_stage

        # Check for invalid regression without explicit flag
        if target_tier < current_tier:
            return False, f"Target tier ({target_tier}) is lower than current tier ({current_tier}). Cultivation regression requires canon override."

        # Check ceiling limit
        if target_tier > state.potential.ceiling_tier:
            return False, f"Target tier ({target_tier}) exceeds character potential ceiling ({state.potential.ceiling_tier})."

        # Tier jump check: Cannot jump more than 1 tier at a time
        if target_tier > current_tier + 1:
            return False, f"Impossible tier jump: Attempting to leap from Tier {current_tier} to Tier {target_tier} in a single step."

        # Intra-tier progression
        if target_tier == current_tier:
            curr_idx = STAGE_ORDER.get(current_stage, 1)
            targ_idx = STAGE_ORDER.get(target_stage, 1)
            if targ_idx <= curr_idx:
                return False, f"Target stage ({target_stage}) is not greater than current stage ({current_stage})."
            if targ_idx - curr_idx > 1 and not catalyst:
                return False, f"Skipping stages ({current_stage} -> {target_stage}) requires a catalyst or sudden epiphany."

        # Inter-tier progression (advancing to tier + 1)
        if target_tier == current_tier + 1:
            if current_stage != "Peak" and not catalyst:
                return False, f"Cannot break through to Tier {target_tier} from stage '{current_stage}'. Must reach 'Peak' or consume an extraordinary breakthrough catalyst."
            if target_tier >= 3 and not catalyst:
                return False, f"Tier {target_tier} breakthrough requires an explicit catalyst or life-and-death crisis."

        return True, None

    def execute_breakthrough(
        self,
        character_id: str,
        target_tier: int,
        target_stage: str,
        chapter_number: int,
        catalyst_description: str = "",
        trigger_type: ProgressionTrigger = ProgressionTrigger.MEDITATION,
        cost_paid: Optional[Dict[str, Any]] = None,
        stat_growth: Optional[Dict[str, float]] = None,
        force_failure: bool = False,
        canon_override: bool = False
    ) -> ProgressionEvent:
        state = self.power_repo.get_character_power_state(character_id)
        if not state:
            raise ValueError(f"Character {character_id} has no power state.")

        valid, error_msg = self.validate_breakthrough(
            character_id=character_id,
            target_tier=target_tier,
            target_stage=target_stage,
            catalyst=catalyst_description,
            canon_override=canon_override
        )

        if not valid and not canon_override:
            # Record failed progression event
            failed_event = ProgressionEvent(
                id=str(uuid.uuid4()),
                character_id=character_id,
                story_id=state.story_id,
                system_id=state.system_id,
                from_tier=state.current_tier,
                from_stage=state.current_stage,
                to_tier=target_tier,
                to_stage=target_stage,
                chapter_number=chapter_number,
                trigger_type=trigger_type,
                catalyst_description=catalyst_description,
                cost_paid=cost_paid or {},
                bottleneck_broken=False,
                success=False,
                failure_reason=error_msg,
                stat_growth={},
            )
            self.power_repo.record_progression_event(failed_event)
            raise ValueError(f"Breakthrough validation failed: {error_msg}")

        if force_failure:
            # Intentional failed attempt (e.g., tribulation failure / Qi deviation)
            failed_event = ProgressionEvent(
                id=str(uuid.uuid4()),
                character_id=character_id,
                story_id=state.story_id,
                system_id=state.system_id,
                from_tier=state.current_tier,
                from_stage=state.current_stage,
                to_tier=target_tier,
                to_stage=target_stage,
                chapter_number=chapter_number,
                trigger_type=trigger_type,
                catalyst_description=catalyst_description,
                cost_paid=cost_paid or {},
                bottleneck_broken=False,
                success=False,
                failure_reason="Backlash occurred during core condensation; meridians suffered internal shock.",
                stat_growth={},
            )
            self.power_repo.record_progression_event(failed_event)

            # Apply Qi deviation status effect
            eff = StatusEffect(
                id=str(uuid.uuid4()),
                character_id=character_id,
                effect_type=StatusEffectType.QI_DEVIATION,
                severity=2.5,
                duration_scenes=3,
                stat_penalties={"energy": 15.0, "durability": 10.0},
                description="Qi deviation from failed breakthrough attempt.",
                chapter_applied=chapter_number,
            )
            self.power_repo.apply_status_effect(eff)
            return failed_event

        # Successful breakthrough!
        system = self.power_repo.get_power_system(state.system_id)
        new_tier_name = state.tier_name
        if system:
            for t in system.tiers:
                if t.rank == target_tier:
                    new_tier_name = t.name
                    break

        default_stat_growth = {
            "physical": 5.0 * (target_tier),
            "energy": 8.0 * (target_tier),
            "speed": 5.0 * (target_tier),
            "durability": 5.0 * (target_tier),
            "perception": 6.0 * (target_tier),
            "control": 4.0 * (target_tier),
        }
        growth = stat_growth or default_stat_growth

        # Update power vector
        new_vec = state.power_vector.apply_modifiers(growth)

        # Scale energy pools
        for pool in state.energy_pools:
            pool.maximum += 100.0 * target_tier
            pool.current = pool.maximum
            pool.density = round(pool.density * 1.25, 2)
            pool.purity = min(1.0, round(pool.purity + 0.05, 2))

        # Create new state snapshot for chapter
        new_state = CharacterPowerState(
            id=str(uuid.uuid4()),
            character_id=character_id,
            story_id=state.story_id,
            system_id=state.system_id,
            current_tier=target_tier,
            current_stage=target_stage,
            tier_name=new_tier_name,
            power_vector=new_vec,
            potential=state.potential,
            energy_pools=state.energy_pools,
            active_buffs=state.active_buffs,
            conditions=state.conditions,
            chapter_acquired=chapter_number,
            is_active=True,
        )
        new_state.calculate_combat_rating()
        self.power_repo.create_or_update_character_power(new_state)

        event = ProgressionEvent(
            id=str(uuid.uuid4()),
            character_id=character_id,
            story_id=state.story_id,
            system_id=state.system_id,
            from_tier=state.current_tier,
            from_stage=state.current_stage,
            to_tier=target_tier,
            to_stage=target_stage,
            chapter_number=chapter_number,
            trigger_type=trigger_type,
            catalyst_description=catalyst_description,
            cost_paid=cost_paid or {},
            bottleneck_broken=True,
            success=True,
            stat_growth=growth,
        )
        self.power_repo.record_progression_event(event)
        return event
