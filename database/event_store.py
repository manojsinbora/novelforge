"""
NovelForge AI — Persistent Event Sourcing Engine & Story State Ledger
Provides an immutable event ledger and deterministic state projections.
"""
from __future__ import annotations
import sqlite3
import json
import uuid
from typing import List, Dict, Optional, Any
from novelforge.schemas.story_schemas import (
    StoryEvent, Character, KnowledgeFact, Promise, PromiseStatus, CultivationState, VoiceProfile
)


class EventStore:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS story_events (
                    event_id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    chapter_number INTEGER NOT NULL,
                    scene_number INTEGER NOT NULL,
                    sequence_num INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    author TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_story_events_seq 
                ON story_events (story_id, chapter_number, sequence_num);
            """)

    def append_event(self, event: StoryEvent) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT INTO story_events (
                    event_id, story_id, chapter_number, scene_number,
                    sequence_num, event_type, entity_type, entity_id,
                    payload, author
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.event_id, event.story_id, event.chapter_number,
                event.scene_number, event.sequence_num, event.event_type,
                event.entity_type, event.entity_id, json.dumps(event.payload),
                event.author
            ))

    def get_events(self, story_id: str, up_to_chapter: Optional[int] = None) -> List[StoryEvent]:
        cursor = self.conn.cursor()
        if up_to_chapter is not None:
            cursor.execute("""
                SELECT * FROM story_events 
                WHERE story_id = ? AND chapter_number <= ? 
                ORDER BY chapter_number ASC, sequence_num ASC
            """, (story_id, up_to_chapter))
        else:
            cursor.execute("""
                SELECT * FROM story_events 
                WHERE story_id = ? 
                ORDER BY chapter_number ASC, sequence_num ASC
            """, (story_id,))

        events = []
        for row in cursor.fetchall():
            events.append(StoryEvent(
                event_id=row["event_id"],
                story_id=row["story_id"],
                chapter_number=row["chapter_number"],
                scene_number=row["scene_number"],
                sequence_num=row["sequence_num"],
                event_type=row["event_type"],
                entity_type=row["entity_type"],
                entity_id=row["entity_id"],
                payload=json.loads(row["payload"]),
                author=row["author"]
            ))
        return events

    def project_state(self, story_id: str, at_chapter: Optional[int] = None) -> Dict[str, Any]:
        """
        Deterministically replays the event ledger to project story truth at a specific chapter.
        """
        events = self.get_events(story_id, up_to_chapter=at_chapter)
        
        characters: Dict[str, Character] = {}
        knowledge_facts: Dict[str, KnowledgeFact] = {}
        promises: Dict[str, Promise] = {}
        inventory_locations: Dict[str, str] = {} # item_id -> owner_character_id

        for ev in events:
            p = ev.payload
            
            if ev.event_type == "CHARACTER_CREATED":
                char_id = ev.entity_id
                characters[char_id] = Character(
                    id=char_id,
                    name=p.get("name", "Unknown"),
                    age=p.get("age", 18),
                    gender=p.get("gender", "Unknown"),
                    personality_traits=p.get("personality_traits", []),
                    driving_want=p.get("driving_want", ""),
                    core_fear=p.get("core_fear", ""),
                    current_location=p.get("current_location", "Unknown"),
                    cultivation=CultivationState(
                        realm=p.get("realm", "Mortal"),
                        sub_realm=p.get("sub_realm", "None"),
                        rank_level=p.get("rank_level", 1)
                    )
                )

            elif ev.event_type == "CHARACTER_PROMOTED":
                char = characters.get(ev.entity_id)
                if char:
                    if "realm" in p:
                        char.cultivation.realm = p["realm"]
                    if "sub_realm" in p:
                        char.cultivation.sub_realm = p["sub_realm"]
                    if "rank_level" in p:
                        char.cultivation.rank_level = p["rank_level"]

            elif ev.event_type == "ITEM_TRANSFERRED":
                item_id = ev.entity_id
                from_char = p.get("from_character_id")
                to_char = p.get("to_character_id")
                if from_char and from_char in characters:
                    if item_id in characters[from_char].equipped_items:
                        characters[from_char].equipped_items.remove(item_id)
                if to_char and to_char in characters:
                    characters[to_char].equipped_items.append(item_id)
                inventory_locations[item_id] = to_char

            elif ev.event_type == "SECRET_REVEALED":
                fact_key = p["fact_key"]
                if fact_key not in knowledge_facts:
                    knowledge_facts[fact_key] = KnowledgeFact(
                        fact_key=fact_key,
                        description=p.get("description", ""),
                        author_knows=True,
                        reader_knows=p.get("reader_knows", False),
                        known_by_characters=p.get("known_by_characters", [])
                    )
                else:
                    fact = knowledge_facts[fact_key]
                    if p.get("reader_knows"):
                        fact.reader_knows = True
                    for c_id in p.get("newly_learned_by", []):
                        if c_id not in fact.known_by_characters:
                            fact.known_by_characters.append(c_id)

            elif ev.event_type == "PROMISE_CREATED":
                promises[ev.entity_id] = Promise(
                    id=ev.entity_id,
                    title=p.get("title", ""),
                    description=p.get("description", ""),
                    introduced_chapter=ev.chapter_number,
                    expected_payoff_min=p.get("expected_payoff_min", ev.chapter_number + 50),
                    expected_payoff_max=p.get("expected_payoff_max", ev.chapter_number + 200),
                    status=PromiseStatus.OPEN
                )

            elif ev.event_type == "PROMISE_RESOLVED":
                prom = promises.get(ev.entity_id)
                if prom:
                    prom.status = PromiseStatus.RESOLVED
                    prom.resolution_chapter = ev.chapter_number

        return {
            "story_id": story_id,
            "projected_at_chapter": at_chapter,
            "characters": characters,
            "knowledge_facts": knowledge_facts,
            "promises": promises,
            "inventory_locations": inventory_locations,
            "total_events_applied": len(events)
        }
