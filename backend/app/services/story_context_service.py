"""
NovelForge AI — Story Context Service (Agent Access Layer)
The clean, controlled interface through which all future AI agents retrieve story truth.
Agents are strictly prohibited from issuing raw arbitrary database queries.
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional
from novelforge.database.narrative_repository import NarrativeRepository
from novelforge.schemas.narrative_models import StoryStateSnapshot


class StoryContextService:
    def __init__(self, repository: NarrativeRepository):
        self.repo = repository

    def get_story_bible(self, story_id: str) -> Dict[str, Any]:
        bible = self.repo.get_story_bible(story_id)
        if not bible:
            return {}
        return bible

    def get_story_state(self, story_id: str, at_chapter: Optional[int] = None) -> Dict[str, Any]:
        snapshot = self.repo.get_story_state_snapshot(story_id, at_chapter=at_chapter)
        return snapshot.to_dict()

    def get_character(self, story_id: str, character_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.get_character(story_id, character_id)

    def get_characters(self, story_id: str) -> List[Dict[str, Any]]:
        return self.repo.get_characters(story_id)

    def get_character_knowledge(self, story_id: str, character_id: str, at_chapter: int) -> List[Dict[str, Any]]:
        from novelforge.backend.app.services.knowledge_service import KnowledgeService
        ks = KnowledgeService(self.repo)
        return ks.get_character_known_facts(story_id, character_id, at_chapter)

    def get_relationships(self, story_id: str, character_id: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.repo.get_relationships(story_id, character_id)

    def get_location(self, story_id: str, location_id: str) -> Optional[Dict[str, Any]]:
        locations = self.repo.get_locations(story_id)
        return next((loc for loc in locations if loc["id"] == location_id), None)

    def get_world_rules(self, story_id: str) -> Dict[str, Any]:
        bible = self.get_story_bible(story_id)
        return bible.get("world_rules", {})

    def get_recent_events(self, story_id: str, count: int = 5, up_to_chapter: Optional[int] = None) -> List[Dict[str, Any]]:
        events = self.repo.get_events(story_id, up_to_chapter=up_to_chapter)
        return events[-count:] if events else []

    def get_active_plot_threads(self, story_id: str) -> List[str]:
        # Derives active plot threads from unresolved mysteries and promises
        snapshot = self.repo.get_story_state_snapshot(story_id)
        return snapshot.open_plot_threads

    def get_current_arc(self, story_id: str) -> Optional[Dict[str, Any]]:
        story = self.repo.get_story(story_id)
        if not story:
            return None
        arcs = self.repo.get_arcs(story_id)
        return next((a for a in arcs if a["sequence_order"] == story.current_arc), arcs[0] if arcs else None)

    def get_current_chapter(self, story_id: str) -> Optional[Dict[str, Any]]:
        story = self.repo.get_story(story_id)
        if not story:
            return None
        return self.repo.get_chapter(story_id, story.current_chapter)
