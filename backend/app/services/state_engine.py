"""
NovelForge AI — Narrative State Engine Service
The heart of the application. Answers all authoritative story state queries.
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional
from novelforge.database.event_store import EventStore
from novelforge.schemas.story_schemas import Character, KnowledgeFact, Promise, PromiseStatus


class NarrativeStateEngine:
    def __init__(self, event_store: EventStore):
        self.event_store = event_store

    def get_narrative_state(
        self,
        story_id: str,
        current_chapter: int,
        active_location: str = "Azure Dragon Sect"
    ) -> Dict[str, Any]:
        """
        Calculates and answers the authoritative story questions at the target chapter.
        """
        projection = self.event_store.project_state(story_id, at_chapter=current_chapter)
        characters: Dict[str, Character] = projection["characters"]
        knowledge_facts: Dict[str, KnowledgeFact] = projection["knowledge_facts"]
        promises: Dict[str, Promise] = projection["promises"]
        inventory: Dict[str, str] = projection["inventory_locations"]

        # 1. Who is present at active location?
        present_characters = [
            c for c in characters.values() if c.current_location == active_location and c.is_alive
        ]

        # 2. What does each character know vs. reader vs. author?
        epistemic_summary = {}
        for key, fact in knowledge_facts.items():
            epistemic_summary[key] = {
                "description": fact.description,
                "author_knows": fact.author_knows,
                "reader_knows": fact.reader_knows,
                "known_by_characters": [characters[cid].name for cid in fact.known_by_characters if cid in characters]
            }

        # 3. Active / overdue narrative promises
        active_promises = []
        overdue_promises = []
        for p in promises.values():
            status = p.check_status(current_chapter)
            if status == PromiseStatus.OVERDUE:
                overdue_promises.append(p.title)
            elif status in [PromiseStatus.OPEN, PromiseStatus.ACTIVE, PromiseStatus.APPROACHING_PAYOFF]:
                active_promises.append(p.title)

        # 4. Equipment distribution
        equipment_map = {}
        for item_id, owner_id in inventory.items():
            owner_name = characters[owner_id].name if owner_id in characters else "Unassigned"
            equipment_map[item_id] = owner_name

        # 5. Character power levels
        power_levels = {
            c.name: f"{c.cultivation.realm} ({c.cultivation.sub_realm}, Rank {c.cultivation.rank_level})"
            for c in characters.values()
        }

        # 6. What must NOT happen yet? (Knowledge & Realm boundaries)
        forbidden_actions = []
        for fact in knowledge_facts.values():
            if not fact.reader_knows:
                forbidden_actions.append(f"Do not reveal secret '{fact.fact_key}' to the reader yet.")
            for c in present_characters:
                if not fact.is_known_by(c.id):
                    forbidden_actions.append(f"Character {c.name} must NOT act on secret '{fact.fact_key}'.")

        return {
            "where_are_we": active_location,
            "current_chapter": current_chapter,
            "who_is_present": [c.name for c in present_characters],
            "what_has_happened_events_count": projection["total_events_applied"],
            "epistemic_knowledge": epistemic_summary,
            "active_promises": active_promises,
            "overdue_promises": overdue_promises,
            "equipment_ownership": equipment_map,
            "character_power_levels": power_levels,
            "what_must_not_happen_yet": forbidden_actions
        }
