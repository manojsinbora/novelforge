"""
NovelForge AI — Scene Power Context Service
Phase 3: Compact, Token-Budgeted Power Prompt Injection for Writing Agents
Generates authoritative power state dossiers for active scene characters.
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any

from novelforge.database.power_repository import PowerRepository
from novelforge.backend.app.services.power_state_service import PowerStateService
from novelforge.backend.app.services.mutation_service import MutationService


class ScenePowerContextService:
    def __init__(
        self,
        power_repo: PowerRepository,
        power_state_service: PowerStateService,
        mutation_service: MutationService
    ):
        self.power_repo = power_repo
        self.power_state_service = power_state_service
        self.mutation_service = mutation_service

    def get_scene_power_context(
        self,
        character_ids: List[str],
        chapter_number: int,
        pov_character_id: Optional[str] = None,
        token_budget: int = 1500
    ) -> Dict[str, Any]:
        """
        Builds a compact, authoritative power context block for a scene.
        Respects epistemic visibility: POV character knows their own private mutations,
        but only public details of rivals.
        """
        characters_dossiers = []

        for cid in character_ids:
            state = self.power_repo.get_character_power_state(cid, at_chapter=chapter_number)
            if not state:
                continue

            is_pov = (cid == pov_character_id)
            # Epistemic filtering for mutations
            mutations = self.mutation_service.get_visible_mutations(
                character_id=cid,
                viewer_is_character=is_pov,
                viewer_is_world=not is_pov,
                at_chapter=chapter_number
            )
            abilities = self.power_repo.get_abilities_for_character(cid, at_chapter=chapter_number)
            equipment = self.power_repo.get_equipment_for_character(cid, at_chapter=chapter_number)
            status_effects = self.power_repo.get_active_status_effects(cid, current_chapter=chapter_number)

            dossier = {
                "character_id": cid,
                "is_pov": is_pov,
                "tier": state.current_tier,
                "stage": state.current_stage,
                "tier_name": state.tier_name,
                "combat_rating": state.raw_combat_rating,
                "mutations": [m.name for m in mutations],
                "active_abilities": [a.name for a in abilities],
                "equipment": [f"{e.name} ({e.rarity.value if hasattr(e.rarity, 'value') else e.rarity}, {e.current_durability:.0f}% dur)" for e in equipment if not e.is_destroyed],
                "conditions": [s.effect_type.value if hasattr(s.effect_type, 'value') else s.effect_type for s in status_effects],
            }
            characters_dossiers.append(dossier)

        # Format into clean Markdown prompt block
        lines = [
            "### AUTHORITATIVE CANONICAL POWER CONTEXT (DO NOT OVERRIDE IN NARRATIVE)",
            f"**Chapter**: {chapter_number}",
            "**Enforced Invariants**: Characters CANNOT use abilities not listed below. Realm gaps must dictate base kinetic/energetic exchange.",
            "",
        ]

        for d in characters_dossiers:
            role = " (POV Character)" if d["is_pov"] else ""
            lines.append(f"#### Character {d['character_id']}{role}")
            lines.append(f"- **Cultivation Realm**: {d['tier_name']} (Tier {d['tier']}, {d['stage']} Stage) [Combat Index: {d['combat_rating']}]")
            if d["conditions"]:
                lines.append(f"- **Active Conditions / Debuffs**: {', '.join(d['conditions'])}")
            if d["equipment"]:
                lines.append(f"- **Equipped Gear**: {', '.join(d['equipment'])}")
            if d["active_abilities"]:
                lines.append(f"- **Usable Abilities**: {', '.join(d['active_abilities'])}")
            if d["mutations"]:
                lines.append(f"- **Visible Mutations**: {', '.join(d['mutations'])}")
            lines.append("")

        prompt_text = "\n".join(lines)
        return {
            "prompt_text": prompt_text,
            "characters_count": len(characters_dossiers),
            "chapter_number": chapter_number,
            "character_dossiers": characters_dossiers,
        }
