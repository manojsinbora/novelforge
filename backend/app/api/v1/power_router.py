"""
NovelForge AI — Power & Progression Engine REST API (FastAPI Router)
Phase 3 Endpoints: Systems, Power Dossiers, Breakthroughs, Mutations, Equipment, Combat, QA Validation
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional

try:
    from fastapi import APIRouter, HTTPException, Query
    from pydantic import BaseModel, Field
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    class APIRouter:
        def __init__(self, *args, **kwargs):
            self.routes = []
        def get(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def post(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def put(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def delete(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            self.status_code = status_code
            self.detail = detail
    class BaseModel:
        pass
    def Field(*args, **kwargs):
        return None

from novelforge.database.power_repository import PowerRepository
from novelforge.backend.app.services.power_state_service import PowerStateService
from novelforge.backend.app.services.progression_service import ProgressionService
from novelforge.backend.app.services.mutation_service import MutationService
from novelforge.backend.app.services.ability_service import AbilityService
from novelforge.backend.app.services.equipment_service import EquipmentService
from novelforge.backend.app.services.combat_assessment_service import CombatAssessmentService
from novelforge.backend.app.services.power_validation_service import PowerValidationService
from novelforge.backend.app.services.scene_power_context_service import ScenePowerContextService
from novelforge.schemas.power_models import (
    PowerSystem, CharacterPowerState, ProgressionTrigger, Mutation,
    Ability, Technique, Equipment, EquipmentRarity, EquipmentSlot
)

router = APIRouter(prefix="/api/v1/power", tags=["Power & Progression Engine"])

# Shared service instances
default_power_repo = PowerRepository("novelforge/database/novelforge.sqlite3")
power_state_svc = PowerStateService(default_power_repo)
progression_svc = ProgressionService(default_power_repo)
mutation_svc = MutationService(default_power_repo)
ability_svc = AbilityService(default_power_repo)
equipment_svc = EquipmentService(default_power_repo)
combat_svc = CombatAssessmentService(default_power_repo)
validation_svc = PowerValidationService(default_power_repo)
scene_context_svc = ScenePowerContextService(default_power_repo, power_state_svc, mutation_svc)


# =============================================================================
# 1. POWER SYSTEMS
# =============================================================================

@router.post("/systems/default")
def create_default_system(story_id: str, name: str = "Sevenfold Awakening Cultivation"):
    sys = power_state_svc.create_default_seven_tier_system(story_id=story_id, name=name)
    return sys.to_dict()

@router.get("/systems/{system_id}")
def get_power_system(system_id: str):
    sys = default_power_repo.get_power_system(system_id)
    if not sys:
        raise HTTPException(status_code=404, detail="Power system not found")
    return sys.to_dict()

@router.get("/stories/{story_id}/systems")
def get_systems_for_story(story_id: str):
    systems = default_power_repo.get_power_systems_for_story(story_id)
    return [s.to_dict() for s in systems]


# =============================================================================
# 2. CHARACTER POWER DOSSIER & PROGRESSION
# =============================================================================

@router.post("/characters/{character_id}/init")
def initialize_character_power(
    character_id: str,
    story_id: str,
    system_id: str,
    tier: int = 1,
    stage: str = "Early",
    chapter_acquired: int = 1
):
    state = power_state_svc.initialize_character_power(
        character_id=character_id,
        story_id=story_id,
        system_id=system_id,
        tier=tier,
        stage=stage,
        chapter_acquired=chapter_acquired,
    )
    return state.to_dict()

@router.get("/characters/{character_id}/dossier")
def get_character_power_dossier(character_id: str, at_chapter: Optional[int] = None):
    dossier = power_state_svc.get_character_power_dossier(character_id, at_chapter=at_chapter)
    if "error" in dossier:
        raise HTTPException(status_code=404, detail=dossier["error"])
    return dossier

@router.get("/characters/{character_id}/history")
def get_progression_history(character_id: str, up_to_chapter: Optional[int] = None):
    history = default_power_repo.get_progression_history(character_id, up_to_chapter=up_to_chapter)
    return [p.to_dict() for p in history]

@router.post("/characters/{character_id}/breakthrough")
def execute_breakthrough(
    character_id: str,
    target_tier: int,
    target_stage: str,
    chapter_number: int,
    catalyst_description: str = "",
    trigger_type: str = "MEDITATION",
    canon_override: bool = False
):
    trig = ProgressionTrigger.MEDITATION
    try:
        trig = ProgressionTrigger(trigger_type)
    except ValueError:
        pass
    try:
        event = progression_svc.execute_breakthrough(
            character_id=character_id,
            target_tier=target_tier,
            target_stage=target_stage,
            chapter_number=chapter_number,
            catalyst_description=catalyst_description,
            trigger_type=trig,
            canon_override=canon_override,
        )
        return {"status": "success", "event": event.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =============================================================================
# 3. MUTATIONS, ABILITIES & TECHNIQUES
# =============================================================================

@router.get("/characters/{character_id}/mutations")
def get_mutations(character_id: str, at_chapter: Optional[int] = None, viewer_is_world: bool = False):
    mutations = mutation_svc.get_visible_mutations(
        character_id=character_id,
        viewer_is_character=not viewer_is_world,
        viewer_is_world=viewer_is_world,
        at_chapter=at_chapter,
    )
    return [m.to_dict() for m in mutations]

@router.get("/characters/{character_id}/abilities")
def get_abilities(character_id: str, at_chapter: Optional[int] = None):
    abilities = default_power_repo.get_abilities_for_character(character_id, at_chapter=at_chapter)
    return [a.to_dict() for a in abilities]

@router.get("/characters/{character_id}/techniques")
def get_techniques(character_id: str, at_chapter: Optional[int] = None):
    techniques = default_power_repo.get_techniques_for_character(character_id, at_chapter=at_chapter)
    return [t.to_dict() for t in techniques]


# =============================================================================
# 4. EQUIPMENT & PROVENANCE
# =============================================================================

@router.get("/equipment/{equipment_id}")
def get_equipment_detail(equipment_id: str):
    eq = default_power_repo.get_equipment(equipment_id)
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")
    history = default_power_repo.get_equipment_history(equipment_id)
    return {"equipment": eq.to_dict(), "provenance": [h.to_dict() for h in history]}

@router.get("/characters/{character_id}/equipment")
def get_character_equipment(character_id: str, at_chapter: Optional[int] = None):
    eq = default_power_repo.get_equipment_for_character(character_id, at_chapter=at_chapter)
    return [e.to_dict() for e in eq]

@router.post("/equipment/{equipment_id}/transfer")
def transfer_equipment(equipment_id: str, new_owner_id: Optional[str], chapter_number: int, reason: str = "LOOTED"):
    try:
        rec = equipment_svc.transfer_ownership(equipment_id, new_owner_id, chapter_number, reason)
        return {"status": "success", "record": rec.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# =============================================================================
# 5. COMBAT ASSESSMENT SIMULATOR
# =============================================================================

@router.post("/combat/simulate")
def simulate_combat(
    combatant_a_id: str,
    combatant_b_id: str,
    combatant_a_name: str = "Combatant A",
    combatant_b_name: str = "Combatant B",
    chapter_number: Optional[int] = None,
    environment: Optional[Dict[str, Any]] = None
):
    result = combat_svc.evaluate_matchup(
        combatant_a_id=combatant_a_id,
        combatant_b_id=combatant_b_id,
        combatant_a_name=combatant_a_name,
        combatant_b_name=combatant_b_name,
        chapter_number=chapter_number,
        environment=environment,
    )
    return result.to_dict()


# =============================================================================
# 6. POWER QA CONTINUITY VALIDATION
# =============================================================================

@router.post("/validate")
def validate_power_continuity(
    character_id: str,
    chapter_number: int,
    attempted_abilities: Optional[List[str]] = None,
    wielded_equipment_ids: Optional[List[str]] = None,
    claimed_tier: Optional[int] = None,
    claimed_stage: Optional[str] = None
):
    result = validation_svc.validate_scene_power_continuity(
        character_id=character_id,
        current_chapter=chapter_number,
        attempted_abilities=attempted_abilities,
        wielded_equipment_ids=wielded_equipment_ids,
        claimed_tier=claimed_tier,
        claimed_stage=claimed_stage,
    )
    return result.to_dict()


# =============================================================================
# 7. SCENE POWER CONTEXT INJECTION
# =============================================================================

@router.post("/scene-context")
def get_scene_power_context(
    character_ids: List[str],
    chapter_number: int,
    pov_character_id: Optional[str] = None
):
    ctx = scene_context_svc.get_scene_power_context(
        character_ids=character_ids,
        chapter_number=chapter_number,
        pov_character_id=pov_character_id,
    )
    return ctx
