"""
NovelForge AI — Mutation Engine
Phase 3: 10-Category Mutation System & Epistemic Visibility
Manages biological, energetic, bloodline, and soul mutations with stability transitions.
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any
import uuid
import datetime

from novelforge.database.power_repository import PowerRepository
from novelforge.schemas.power_models import (
    Mutation, MutationCategory, MutationStability
)


class MutationService:
    def __init__(self, power_repo: PowerRepository):
        self.power_repo = power_repo

    def register_mutation(
        self,
        character_id: str,
        story_id: str,
        name: str,
        category: MutationCategory,
        stability: MutationStability = MutationStability.STABLE,
        tier: int = 1,
        stat_modifiers: Optional[Dict[str, float]] = None,
        abilities_granted: Optional[List[str]] = None,
        drawbacks: Optional[List[str]] = None,
        triggers: Optional[List[str]] = None,
        hidden_from_character: bool = False,
        hidden_from_world: bool = False,
        chapter_manifested: int = 1,
    ) -> Mutation:
        mutation = Mutation(
            id=str(uuid.uuid4()),
            character_id=character_id,
            story_id=story_id,
            name=name,
            category=category,
            stability=stability,
            tier=tier,
            stat_modifiers=stat_modifiers or {},
            abilities_granted=abilities_granted or [],
            drawbacks=drawbacks or [],
            triggers=triggers or [],
            hidden_from_character=hidden_from_character,
            hidden_from_world=hidden_from_world,
            chapter_manifested=chapter_manifested,
        )
        return self.power_repo.create_mutation(mutation)

    def get_visible_mutations(
        self,
        character_id: str,
        viewer_is_character: bool = True,
        viewer_is_world: bool = False,
        at_chapter: Optional[int] = None
    ) -> List[Mutation]:
        """
        Filters mutations based on who is observing:
        - If viewer is the character: hidden_from_character must be False (unless revealed).
        - If viewer is the outside world/public: hidden_from_world must be False.
        """
        all_mutations = self.power_repo.get_mutations_for_character(
            character_id=character_id,
            at_chapter=at_chapter,
            include_hidden_char=True,
            include_hidden_world=True,
        )
        visible = []
        for m in all_mutations:
            if viewer_is_character and m.hidden_from_character:
                continue
            if viewer_is_world and m.hidden_from_world:
                continue
            visible.append(m)
        return visible

    def update_stability(
        self,
        mutation_id: str,
        new_stability: MutationStability,
        stat_adjustment: Optional[Dict[str, float]] = None
    ) -> Mutation:
        cur = self.power_repo.conn.execute("SELECT * FROM mutations WHERE id = ?", (mutation_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Mutation {mutation_id} not found")
        mutation = self.power_repo._row_to_mutation(row)
        mutation.stability = new_stability
        if stat_adjustment:
            for k, v in stat_adjustment.items():
                mutation.stat_modifiers[k] = round(mutation.stat_modifiers.get(k, 0.0) + v, 2)
        return self.power_repo.update_mutation(mutation)

    def evolve_mutation(
        self,
        mutation_id: str,
        new_tier: int,
        new_stability: MutationStability,
        stat_growth: Dict[str, float],
        new_abilities: Optional[List[str]] = None,
        chapter_number: int = 1
    ) -> Mutation:
        cur = self.power_repo.conn.execute("SELECT * FROM mutations WHERE id = ?", (mutation_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Mutation {mutation_id} not found")
        mutation = self.power_repo._row_to_mutation(row)
        mutation.tier = new_tier
        mutation.stability = new_stability
        for k, v in stat_growth.items():
            mutation.stat_modifiers[k] = round(mutation.stat_modifiers.get(k, 0.0) + v, 2)
        if new_abilities:
            for a in new_abilities:
                if a not in mutation.abilities_granted:
                    mutation.abilities_granted.append(a)
        return self.power_repo.update_mutation(mutation)
