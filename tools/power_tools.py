"""
NovelForge AI — Controlled Agent Power Tools
Phase 3: Standardized Agent Tool Wrappers for AI Writing & Planning Agents
Enforces epistemic boundaries and schema-safe power manipulation.
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional

from novelforge.database.power_repository import PowerRepository
from novelforge.backend.app.services.power_state_service import PowerStateService
from novelforge.backend.app.services.progression_service import ProgressionService
from novelforge.backend.app.services.mutation_service import MutationService
from novelforge.backend.app.services.ability_service import AbilityService
from novelforge.backend.app.services.equipment_service import EquipmentService
from novelforge.backend.app.services.combat_assessment_service import CombatAssessmentService
from novelforge.backend.app.services.power_validation_service import PowerValidationService
from novelforge.backend.app.services.scene_power_context_service import ScenePowerContextService
from novelforge.schemas.power_models import ProgressionTrigger


class PowerToolSuite:
    def __init__(self, power_repo: Optional[PowerRepository] = None):
        self.power_repo = power_repo or PowerRepository()
        self.power_state_service = PowerStateService(self.power_repo)
        self.progression_service = ProgressionService(self.power_repo)
        self.mutation_service = MutationService(self.power_repo)
        self.ability_service = AbilityService(self.power_repo)
        self.equipment_service = EquipmentService(self.power_repo)
        self.combat_service = CombatAssessmentService(self.power_repo)
        self.validation_service = PowerValidationService(self.power_repo)
        self.scene_context_service = ScenePowerContextService(
            self.power_repo, self.power_state_service, self.mutation_service
        )

    def get_character_power(self, character_id: str, chapter_number: Optional[int] = None) -> Dict[str, Any]:
        """Retrieves authoritative power dossier of character at given chapter."""
        return self.power_state_service.get_character_power_dossier(character_id, at_chapter=chapter_number)

    def compare_combatants(
        self,
        char_a_id: str,
        char_b_id: str,
        char_a_name: str = "Combatant A",
        char_b_name: str = "Combatant B",
        chapter_number: Optional[int] = None,
        environment: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Runs multi-dimensional combat simulation and returns outcome odds and reversal conditions."""
        res = self.combat_service.evaluate_matchup(
            combatant_a_id=char_a_id,
            combatant_b_id=char_b_id,
            combatant_a_name=char_a_name,
            combatant_b_name=char_b_name,
            chapter_number=chapter_number,
            environment=environment,
        )
        return res.to_dict()

    def validate_power_continuity(
        self,
        character_id: str,
        chapter_number: int,
        attempted_abilities: Optional[List[str]] = None,
        wielded_equipment_ids: Optional[List[str]] = None,
        claimed_tier: Optional[int] = None,
        claimed_stage: Optional[str] = None
    ) -> Dict[str, Any]:
        """Audits planned scene actions against canonical power invariants and returns QA score."""
        res = self.validation_service.validate_scene_power_continuity(
            character_id=character_id,
            current_chapter=chapter_number,
            attempted_abilities=attempted_abilities,
            wielded_equipment_ids=wielded_equipment_ids,
            claimed_tier=claimed_tier,
            claimed_stage=claimed_stage,
        )
        return res.to_dict()

    def propose_breakthrough(
        self,
        character_id: str,
        target_tier: int,
        target_stage: str,
        chapter_number: int,
        catalyst_description: str = "",
        trigger_type: str = "MEDITATION"
    ) -> Dict[str, Any]:
        """Submits and evaluates a cultivation breakthrough attempt."""
        trig = ProgressionTrigger.MEDITATION
        try:
            trig = ProgressionTrigger(trigger_type)
        except ValueError:
            pass

        try:
            event = self.progression_service.execute_breakthrough(
                character_id=character_id,
                target_tier=target_tier,
                target_stage=target_stage,
                chapter_number=chapter_number,
                catalyst_description=catalyst_description,
                trigger_type=trig,
            )
            return {"success": True, "progression_event": event.to_dict()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_scene_power_context(
        self,
        character_ids: List[str],
        chapter_number: int,
        pov_character_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generates compact markdown briefing ready to inject into writing prompts."""
        return self.scene_context_service.get_scene_power_context(
            character_ids=character_ids,
            chapter_number=chapter_number,
            pov_character_id=pov_character_id,
        )
