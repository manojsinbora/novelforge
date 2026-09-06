"""
NovelForge AI — Epistemic Knowledge Service
Tracks Author, Reader, and Character Knowledge, preventing secret leaks.
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional
from novelforge.database.narrative_repository import NarrativeRepository
from novelforge.schemas.narrative_models import KnowledgeState, KnowledgeFactEntity


class KnowledgeService:
    def __init__(self, repository: NarrativeRepository):
        self.repo = repository

    def can_character_know_fact(
        self,
        story_id: str,
        character_id: str,
        fact_key: str,
        at_chapter: int
    ) -> bool:
        """
        Validates if a character canonically knows a fact at a specific chapter.
        """
        facts = self.repo.get_knowledge_facts(story_id)
        target_fact = next((f for f in facts if f["fact_key"] == fact_key), None)
        if not target_fact:
            return False

        cmap = target_fact.get("character_knowledge_map", {})
        entry = cmap.get(character_id)
        if not entry:
            return False

        state = entry.get("state")
        if state not in [KnowledgeState.KNOWN_TRUE.value, KnowledgeState.BELIEVED_TRUE.value, KnowledgeState.PARTIALLY_KNOWN.value]:
            return False

        learned_ch = entry.get("learned_at_chapter")
        if learned_ch is not None and learned_ch > at_chapter:
            # Fact was learned in a later chapter! Invariant violation!
            return False

        return True

    def assert_character_has_knowledge(
        self,
        story_id: str,
        character_id: str,
        character_name: str,
        fact_key: str,
        at_chapter: int
    ) -> None:
        """
        Raises an AssertionError if a character attempts to access or act on a secret they do not know.
        """
        if not self.can_character_know_fact(story_id, character_id, fact_key, at_chapter):
            raise AssertionError(
                f"Epistemic Invariant Violation: Character '{character_name}' ({character_id}) "
                f"does NOT know secret '{fact_key}' at Chapter {at_chapter}!"
            )


    def get_character_known_facts(
        self,
        story_id: str,
        character_id: str,
        at_chapter: int
    ) -> List[Dict[str, Any]]:
        facts = self.repo.get_knowledge_facts(story_id)
        known = []
        for f in facts:
            if self.can_character_know_fact(story_id, character_id, f["fact_key"], at_chapter):
                known.append(f)
        return known
