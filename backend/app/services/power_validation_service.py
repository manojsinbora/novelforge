"""
NovelForge AI — Power QA & Continuity Guard Service
Phase 3: Automated Validation of Cultivation, Ability, and Equipment Continuity
Detects impossible breakthroughs, timeline leaks, cooldown violations, and equipment anomalies.
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any
import datetime

from novelforge.database.power_repository import PowerRepository
from novelforge.schemas.power_models import (
    PowerValidationResult, PowerContinuityViolation, ViolationSeverity,
    CharacterPowerState, Ability, Equipment, Mutation
)


class PowerValidationService:
    def __init__(self, power_repo: PowerRepository):
        self.power_repo = power_repo

    def validate_scene_power_continuity(
        self,
        character_id: str,
        current_chapter: int,
        attempted_abilities: Optional[List[str]] = None,
        wielded_equipment_ids: Optional[List[str]] = None,
        claimed_tier: Optional[int] = None,
        claimed_stage: Optional[str] = None,
    ) -> PowerValidationResult:
        violations: List[PowerContinuityViolation] = []
        rules_checked = 0

        # 1. Check Character Power State at this Chapter
        rules_checked += 1
        state = self.power_repo.get_character_power_state(character_id, at_chapter=current_chapter)
        if not state:
            violations.append(PowerContinuityViolation(
                rule_violated="UNINITIALIZED_POWER_STATE",
                severity=ViolationSeverity.CRITICAL,
                description=f"Character {character_id} has no valid power state at Chapter {current_chapter}.",
                offending_chapter=current_chapter,
                character_id=character_id,
                suggested_fix="Initialize character power state before drafting scene."
            ))
        else:
            # 2. Check Tier / Stage claims
            if claimed_tier is not None:
                rules_checked += 1
                if claimed_tier != state.current_tier:
                    violations.append(PowerContinuityViolation(
                        rule_violated="IMPOSSIBLE_TIER_CLAIM",
                        severity=ViolationSeverity.CRITICAL,
                        description=f"Scene claims character is Tier {claimed_tier}, but canonical power state at Chapter {current_chapter} is Tier {state.current_tier} ({state.tier_name}).",
                        offending_chapter=current_chapter,
                        character_id=character_id,
                        suggested_fix=f"Adjust narrative text to reflect Tier {state.current_tier} ({state.tier_name}) or record a valid progression event."
                    ))

            if claimed_stage is not None and state:
                rules_checked += 1
                if claimed_stage != state.current_stage:
                    violations.append(PowerContinuityViolation(
                        rule_violated="IMPOSSIBLE_STAGE_CLAIM",
                        severity=ViolationSeverity.WARNING,
                        description=f"Scene claims stage '{claimed_stage}', but canonical power state is '{state.current_stage}'.",
                        offending_chapter=current_chapter,
                        character_id=character_id,
                        suggested_fix=f"Align stage references to '{state.current_stage}'."
                    ))

        # 3. Check Attempted Abilities
        if attempted_abilities:
            char_abilities = self.power_repo.get_abilities_for_character(character_id, at_chapter=current_chapter)
            unlocked_names = {a.name: a for a in char_abilities}

            # Also check if ability exists in future chapters (Timeline Leak)
            all_abilities = self.power_repo.get_abilities_for_character(character_id, at_chapter=None)
            future_names = {a.name: a for a in all_abilities}

            for ability_name in attempted_abilities:
                rules_checked += 1
                if ability_name not in unlocked_names:
                    if ability_name in future_names:
                        future_ab = future_names[ability_name]
                        violations.append(PowerContinuityViolation(
                            rule_violated="HISTORICAL_FLASHBACK_LEAK",
                            severity=ViolationSeverity.CRITICAL,
                            description=f"Anachronistic ability usage: Ability '{ability_name}' is not unlocked until Chapter {future_ab.chapter_unlocked}, but used in Chapter {current_chapter}.",
                            offending_chapter=current_chapter,
                            character_id=character_id,
                            suggested_fix=f"Remove '{ability_name}' from Chapter {current_chapter} or move unlock to an earlier chapter."
                        ))
                    else:
                        violations.append(PowerContinuityViolation(
                            rule_violated="UNLEARNED_ABILITY_USAGE",
                            severity=ViolationSeverity.CRITICAL,
                            description=f"Character {character_id} has never learned ability '{ability_name}'.",
                            offending_chapter=current_chapter,
                            character_id=character_id,
                            suggested_fix=f"Register ability '{ability_name}' in story bible or character techniques first."
                        ))
                else:
                    ab = unlocked_names[ability_name]
                    # Check cooldown
                    rules_checked += 1
                    if ab.cooldown_scenes > 1 and ab.last_used_chapter == current_chapter:
                        violations.append(PowerContinuityViolation(
                            rule_violated="ABILITY_COOLDOWN_VIOLATION",
                            severity=ViolationSeverity.WARNING,
                            description=f"Ability '{ability_name}' is currently on cooldown (cooldown: {ab.cooldown_scenes} scenes).",
                            offending_chapter=current_chapter,
                            character_id=character_id,
                            suggested_fix=f"Have character rely on alternative martial technique while '{ability_name}' recharges."
                        ))

        # 4. Check Equipment Continuity
        if wielded_equipment_ids:
            for eq_id in wielded_equipment_ids:
                rules_checked += 1
                eq = self.power_repo.get_equipment(eq_id)
                if not eq:
                    violations.append(PowerContinuityViolation(
                        rule_violated="NONEXISTENT_EQUIPMENT",
                        severity=ViolationSeverity.CRITICAL,
                        description=f"Equipment ID {eq_id} does not exist in the story database.",
                        offending_chapter=current_chapter,
                        character_id=character_id,
                        suggested_fix="Register equipment or correct item ID."
                    ))
                    continue

                # Check if item was destroyed before or during this chapter
                if eq.is_destroyed and eq.destruction_chapter is not None and eq.destruction_chapter <= current_chapter:
                    violations.append(PowerContinuityViolation(
                        rule_violated="DESTROYED_EQUIPMENT_WIELDED",
                        severity=ViolationSeverity.CRITICAL,
                        description=f"Equipment '{eq.name}' was destroyed in Chapter {eq.destruction_chapter}, cannot be used in Chapter {current_chapter}.",
                        offending_chapter=current_chapter,
                        character_id=character_id,
                        suggested_fix=f"Remove '{eq.name}' or introduce a repair/reforging narrative event."
                    ))

                # Check ownership
                if eq.current_owner_id != character_id:
                    violations.append(PowerContinuityViolation(
                        rule_violated="ILLEGAL_EQUIPMENT_POSSESSION",
                        severity=ViolationSeverity.CRITICAL,
                        description=f"Equipment '{eq.name}' belongs to {eq.current_owner_id}, not {character_id}.",
                        offending_chapter=current_chapter,
                        character_id=character_id,
                        suggested_fix=f"Execute an equipment transfer event before character {character_id} wields it."
                    ))

                # Check creation timeline
                if eq.chapter_created > current_chapter:
                    violations.append(PowerContinuityViolation(
                        rule_violated="PREMATURE_EQUIPMENT_USE",
                        severity=ViolationSeverity.CRITICAL,
                        description=f"Equipment '{eq.name}' is forged in Chapter {eq.chapter_created}, but used in Chapter {current_chapter}.",
                        offending_chapter=current_chapter,
                        character_id=character_id,
                        suggested_fix=f"Adjust item creation chapter or remove it from Chapter {current_chapter}."
                    ))

        # 5. Check Escalation Runaway
        rules_checked += 1
        history = self.power_repo.get_progression_history(character_id, up_to_chapter=current_chapter)
        if len(history) >= 3:
            recent_events = [e for e in history if current_chapter - e.chapter_number <= 10]
            if len(recent_events) >= 3:
                violations.append(PowerContinuityViolation(
                    rule_violated="ESCALATION_RUNAWAY",
                    severity=ViolationSeverity.WARNING,
                    description=f"Power creep warning: Character {character_id} underwent {len(recent_events)} breakthroughs in under 10 chapters. Risk of narrative pace runaway.",
                    offending_chapter=current_chapter,
                    character_id=character_id,
                    suggested_fix="Pace out progression with training arcs, setbacks, or consolidating bottlenecks."
                ))

        # Calculate Power QA Score
        score = 100.0
        for v in violations:
            if v.severity == ViolationSeverity.CRITICAL:
                score -= 20.0
            elif v.severity == ViolationSeverity.WARNING:
                score -= 8.0
            elif v.severity == ViolationSeverity.INFO:
                score -= 2.0
        score = max(0.0, score)

        is_valid = not any(v.severity == ViolationSeverity.CRITICAL for v in violations)
        summary = "All power continuity invariants satisfied." if is_valid else f"Detected {len(violations)} power continuity violations."

        return PowerValidationResult(
            is_valid=is_valid,
            power_qa_score=score,
            violations=violations,
            audited_chapter=current_chapter,
            total_rules_checked=rules_checked,
            summary=summary,
        )
