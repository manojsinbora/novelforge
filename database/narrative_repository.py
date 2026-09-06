"""
NovelForge AI — Narrative State Repository
Phase 2: High-Performance Persistent Narrative Repository & State Query Engine
Supports standard-library sqlite3 (zero external dependencies) and SQLAlchemy when available.
"""
from __future__ import annotations
import sqlite3
import json
import uuid
import datetime
import os
from typing import List, Dict, Optional, Any, Tuple
from novelforge.schemas.narrative_models import (
    StoryModel, StoryBible, Saga, Arc, Chapter, Scene, CharacterEntity,
    CharacterRelationship, KnowledgeFactEntity, WorldLocation, FactionEntity,
    StoryEventEntity, StoryFactTriplet, ChapterMemory, StoryStateSnapshot,
    ProposedChange, AuditLogRecord, PermissionLevel, ProposalStatus, CanonStatus,
    KnowledgeState, FactKnowledgeEntry
)


class NarrativeRepository:
    def __init__(self, db_path: str = "novelforge/database/novelforge.sqlite3"):
        self.db_path = db_path
        if db_path != ":memory:":
            os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS stories (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    working_title TEXT DEFAULT '',
                    premise TEXT DEFAULT '',
                    genre TEXT DEFAULT '',
                    subgenres TEXT DEFAULT '[]',
                    target_audience TEXT DEFAULT '',
                    tone TEXT DEFAULT '',
                    themes TEXT DEFAULT '[]',
                    narrative_style TEXT DEFAULT '',
                    target_chapter_count INTEGER DEFAULT 500,
                    target_chapter_word_count INTEGER DEFAULT 2000,
                    planned_ending TEXT DEFAULT '',
                    current_saga INTEGER DEFAULT 1,
                    current_arc INTEGER DEFAULT 1,
                    current_chapter INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'ACTIVE',
                    created_at TEXT,
                    updated_at TEXT,
                    meta_info TEXT DEFAULT '{}'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS story_bibles (
                    id TEXT PRIMARY KEY,
                    story_id TEXT UNIQUE NOT NULL,
                    premise_data TEXT DEFAULT '{}',
                    themes_data TEXT DEFAULT '{}',
                    tone_data TEXT DEFAULT '{}',
                    narrative_rules_data TEXT DEFAULT '{}',
                    world_rules_data TEXT DEFAULT '{}',
                    version INTEGER DEFAULT 1,
                    updated_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS sagas (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    sequence_order INTEGER DEFAULT 1,
                    name TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    start_chapter INTEGER DEFAULT 1,
                    end_chapter INTEGER DEFAULT 100,
                    summary TEXT DEFAULT '',
                    objectives TEXT DEFAULT '[]',
                    status TEXT DEFAULT 'PLANNED',
                    version INTEGER DEFAULT 1
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS arcs (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    saga_id TEXT,
                    sequence_order INTEGER DEFAULT 1,
                    name TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    start_chapter INTEGER DEFAULT 1,
                    end_chapter INTEGER DEFAULT 30,
                    summary TEXT DEFAULT '',
                    objectives TEXT DEFAULT '[]',
                    status TEXT DEFAULT 'PLANNED',
                    version INTEGER DEFAULT 1
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS chapters (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    arc_id TEXT,
                    chapter_number INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    summary TEXT DEFAULT '',
                    objectives TEXT DEFAULT '[]',
                    word_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'PLANNED',
                    canon_status TEXT DEFAULT 'DRAFT',
                    qa_score REAL,
                    blueprint TEXT DEFAULT '{}',
                    version INTEGER DEFAULT 1,
                    UNIQUE(story_id, chapter_number)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    aliases TEXT DEFAULT '[]',
                    age INTEGER DEFAULT 20,
                    gender TEXT DEFAULT 'Unknown',
                    species_race TEXT DEFAULT 'Human',
                    appearance TEXT DEFAULT '',
                    personality TEXT DEFAULT '',
                    strengths TEXT DEFAULT '[]',
                    weaknesses TEXT DEFAULT '[]',
                    fears TEXT DEFAULT '[]',
                    desires TEXT DEFAULT '[]',
                    goals TEXT DEFAULT '[]',
                    motivations TEXT DEFAULT '[]',
                    secrets TEXT DEFAULT '[]',
                    backstory TEXT DEFAULT '',
                    beliefs TEXT DEFAULT '[]',
                    misconceptions TEXT DEFAULT '[]',
                    skills TEXT DEFAULT '[]',
                    abilities TEXT DEFAULT '[]',
                    cultivation_data TEXT DEFAULT '{}',
                    voice_profile_data TEXT DEFAULT '{}',
                    current_location_id TEXT DEFAULT '',
                    current_location_name TEXT DEFAULT 'Unknown',
                    equipment_ids TEXT DEFAULT '[]',
                    emotional_state TEXT DEFAULT 'Calm',
                    character_arc TEXT DEFAULT '',
                    development_stage TEXT DEFAULT 'Initial Stage',
                    is_alive INTEGER DEFAULT 1,
                    canon_status TEXT DEFAULT 'CANON',
                    version INTEGER DEFAULT 1,
                    meta_info TEXT DEFAULT '{}',
                    created_at TEXT,
                    updated_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS character_relationships (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    source_character_id TEXT NOT NULL,
                    target_character_id TEXT NOT NULL,
                    relationship_type TEXT DEFAULT 'UNKNOWN',
                    strength REAL DEFAULT 0.5,
                    trust REAL DEFAULT 0.5,
                    hostility REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'ACTIVE',
                    beginning_chapter INTEGER DEFAULT 1,
                    current_chapter INTEGER DEFAULT 1,
                    history_log TEXT DEFAULT '[]',
                    notes TEXT DEFAULT '',
                    version INTEGER DEFAULT 1,
                    updated_at TEXT,
                    UNIQUE(story_id, source_character_id, target_character_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_facts (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    fact_key TEXT NOT NULL,
                    description TEXT NOT NULL,
                    is_true INTEGER DEFAULT 1,
                    author_knowledge INTEGER DEFAULT 1,
                    reader_knowledge INTEGER DEFAULT 0,
                    character_knowledge_map TEXT DEFAULT '{}',
                    planned_reveal_chapter INTEGER DEFAULT 0,
                    actual_revealed_chapter INTEGER,
                    canon_status TEXT DEFAULT 'CANON',
                    version INTEGER DEFAULT 1,
                    created_at TEXT,
                    updated_at TEXT,
                    UNIQUE(story_id, fact_key)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS world_locations (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    type TEXT DEFAULT 'CITY',
                    description TEXT DEFAULT '',
                    parent_location_id TEXT,
                    controlling_faction_id TEXT,
                    inhabitants_count_estimate INTEGER DEFAULT 0,
                    political_status TEXT DEFAULT 'Neutral',
                    resources TEXT DEFAULT '[]',
                    danger_level TEXT DEFAULT 'Low',
                    history TEXT DEFAULT '',
                    coordinates TEXT DEFAULT '{"x": 0.0, "y": 0.0}',
                    known_secrets TEXT DEFAULT '[]',
                    canon_status TEXT DEFAULT 'CANON',
                    version INTEGER DEFAULT 1,
                    meta_info TEXT DEFAULT '{}'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS factions (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    faction_type TEXT DEFAULT 'Sect',
                    description TEXT DEFAULT '',
                    leader_character_id TEXT,
                    headquarters_location_id TEXT,
                    alignment TEXT DEFAULT 'Neutral',
                    military_strength_rating REAL DEFAULT 5.0,
                    allied_faction_ids TEXT DEFAULT '[]',
                    rival_faction_ids TEXT DEFAULT '[]',
                    canon_status TEXT DEFAULT 'CANON',
                    version INTEGER DEFAULT 1,
                    meta_info TEXT DEFAULT '{}'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS narrative_events (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    chapter_number INTEGER NOT NULL,
                    scene_number INTEGER DEFAULT 1,
                    story_day INTEGER DEFAULT 1,
                    story_year INTEGER DEFAULT 1,
                    real_world_timestamp TEXT,
                    location_id TEXT DEFAULT '',
                    location_name TEXT DEFAULT '',
                    participants TEXT DEFAULT '[]',
                    event_type TEXT DEFAULT 'DISCOVERY',
                    description TEXT DEFAULT '',
                    consequences TEXT DEFAULT '[]',
                    canon_status TEXT DEFAULT 'CANON',
                    meta_info TEXT DEFAULT '{}'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS chapter_memories (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    chapter_number INTEGER NOT NULL,
                    chapter_summary TEXT DEFAULT '',
                    important_events TEXT DEFAULT '[]',
                    characters_present TEXT DEFAULT '[]',
                    locations TEXT DEFAULT '[]',
                    items_acquired_or_used TEXT DEFAULT '[]',
                    powers_revealed_or_leveled TEXT DEFAULT '[]',
                    revelations_and_secrets TEXT DEFAULT '[]',
                    relationships_changed TEXT DEFAULT '[]',
                    promises_introduced TEXT DEFAULT '[]',
                    promises_advanced TEXT DEFAULT '[]',
                    foreshadowing_introduced TEXT DEFAULT '[]',
                    mysteries_advanced TEXT DEFAULT '[]',
                    unresolved_threads TEXT DEFAULT '[]',
                    emotional_state_changes TEXT DEFAULT '{}',
                    created_at TEXT,
                    UNIQUE(story_id, chapter_number)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS proposed_changes (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    agent TEXT DEFAULT '',
                    model TEXT DEFAULT '',
                    permission_level TEXT DEFAULT 'PROPOSAL_AGENT',
                    entity_type TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    field_name TEXT NOT NULL,
                    previous_value TEXT,
                    proposed_value TEXT,
                    reason TEXT DEFAULT '',
                    status TEXT DEFAULT 'PENDING',
                    approved_by TEXT,
                    created_at TEXT,
                    reviewed_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    timestamp TEXT,
                    agent TEXT DEFAULT '',
                    model TEXT DEFAULT '',
                    action TEXT NOT NULL,
                    entity_type TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    previous_value TEXT,
                    new_value TEXT,
                    reason TEXT DEFAULT '',
                    approval_status TEXT DEFAULT 'APPROVED'
                );
            """)

    # =========================================================================
    # 1. STORY & STORY BIBLE
    # =========================================================================

    def create_story(self, story_data: StoryModel) -> StoryModel:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO stories (
                    id, title, working_title, premise, genre, subgenres,
                    target_audience, tone, themes, narrative_style,
                    target_chapter_count, target_chapter_word_count,
                    planned_ending, current_saga, current_arc, current_chapter,
                    status, created_at, updated_at, meta_info
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                story_data.id, story_data.title, story_data.working_title,
                story_data.premise, story_data.genre, json.dumps(story_data.subgenres),
                story_data.target_audience, story_data.tone, json.dumps(story_data.themes),
                story_data.narrative_style, story_data.target_chapter_count,
                story_data.target_chapter_word_count, story_data.planned_ending,
                story_data.current_saga, story_data.current_arc, story_data.current_chapter,
                story_data.status.value, story_data.created_at, story_data.updated_at,
                json.dumps(story_data.metadata)
            ))
        return story_data

    def get_story(self, story_id: str) -> Optional[StoryModel]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM stories WHERE id = ?", (story_id,))
        r = cursor.fetchone()
        if not r:
            return None
        return StoryModel(
            id=r["id"],
            title=r["title"],
            working_title=r["working_title"] or "",
            premise=r["premise"] or "",
            genre=r["genre"] or "",
            subgenres=json.loads(r["subgenres"] or "[]"),
            target_audience=r["target_audience"] or "",
            tone=r["tone"] or "",
            themes=json.loads(r["themes"] or "[]"),
            narrative_style=r["narrative_style"] or "",
            target_chapter_count=r["target_chapter_count"],
            target_chapter_word_count=r["target_chapter_word_count"],
            planned_ending=r["planned_ending"] or "",
            current_saga=r["current_saga"],
            current_arc=r["current_arc"],
            current_chapter=r["current_chapter"],
            status=r["status"],
            created_at=r["created_at"] or "",
            updated_at=r["updated_at"] or "",
            metadata=json.loads(r["meta_info"] or "{}")
        )

    def set_story_bible(self, bible: StoryBible) -> None:
        b_dict = bible.to_dict()
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO story_bibles (
                    id, story_id, premise_data, themes_data, tone_data,
                    narrative_rules_data, world_rules_data, version, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()), bible.story_id,
                json.dumps(b_dict.get("premise", {})),
                json.dumps(b_dict.get("themes", {})),
                json.dumps(b_dict.get("tone", {})),
                json.dumps(b_dict.get("narrative_rules", {})),
                json.dumps(b_dict.get("world_rules", {})),
                bible.version,
                datetime.datetime.utcnow().isoformat()
            ))

    def get_story_bible(self, story_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM story_bibles WHERE story_id = ?", (story_id,))
        r = cursor.fetchone()
        if not r:
            return None
        return {
            "story_id": r["story_id"],
            "premise": json.loads(r["premise_data"] or "{}"),
            "themes": json.loads(r["themes_data"] or "{}"),
            "tone": json.loads(r["tone_data"] or "{}"),
            "narrative_rules": json.loads(r["narrative_rules_data"] or "{}"),
            "world_rules": json.loads(r["world_rules_data"] or "{}"),
            "version": r["version"],
            "updated_at": r["updated_at"] or ""
        }

    # =========================================================================
    # 2. STORY HIERARCHY
    # =========================================================================

    def add_saga(self, saga: Saga) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO sagas (
                    id, story_id, sequence_order, name, description,
                    start_chapter, end_chapter, summary, objectives, status, version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                saga.id, saga.story_id, saga.sequence_order, saga.name,
                saga.description, saga.start_chapter, saga.end_chapter,
                saga.summary, json.dumps(saga.objectives), saga.status.value, saga.version
            ))

    def get_sagas(self, story_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sagas WHERE story_id = ? ORDER BY sequence_order", (story_id,))
        return [{
            "id": r["id"], "story_id": r["story_id"], "sequence_order": r["sequence_order"],
            "name": r["name"], "description": r["description"], "start_chapter": r["start_chapter"],
            "end_chapter": r["end_chapter"], "summary": r["summary"],
            "objectives": json.loads(r["objectives"] or "[]"),
            "status": r["status"], "version": r["version"]
        } for r in cursor.fetchall()]

    def add_arc(self, arc: Arc) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO arcs (
                    id, story_id, saga_id, sequence_order, name, description,
                    start_chapter, end_chapter, summary, objectives, status, version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                arc.id, arc.story_id, arc.saga_id, arc.sequence_order, arc.name,
                arc.description, arc.start_chapter, arc.end_chapter,
                arc.summary, json.dumps(arc.objectives), arc.status.value, arc.version
            ))

    def get_arcs(self, story_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM arcs WHERE story_id = ? ORDER BY sequence_order", (story_id,))
        return [{
            "id": r["id"], "story_id": r["story_id"], "saga_id": r["saga_id"],
            "sequence_order": r["sequence_order"], "name": r["name"], "description": r["description"],
            "start_chapter": r["start_chapter"], "end_chapter": r["end_chapter"],
            "summary": r["summary"], "objectives": json.loads(r["objectives"] or "[]"),
            "status": r["status"], "version": r["version"]
        } for r in cursor.fetchall()]

    def add_chapter(self, chapter: Chapter) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO chapters (
                    id, story_id, arc_id, chapter_number, title, description,
                    summary, objectives, word_count, status, canon_status,
                    qa_score, blueprint, version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chapter.id, chapter.story_id, chapter.arc_id, chapter.chapter_number,
                chapter.title, chapter.description, chapter.summary,
                json.dumps(chapter.objectives), chapter.word_count, chapter.status.value,
                chapter.canon_status.value, chapter.qa_score, json.dumps(chapter.blueprint), chapter.version
            ))

    def get_chapters(self, story_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chapters WHERE story_id = ? ORDER BY chapter_number", (story_id,))
        return [{
            "id": r["id"], "story_id": r["story_id"], "arc_id": r["arc_id"],
            "chapter_number": r["chapter_number"], "title": r["title"], "description": r["description"],
            "summary": r["summary"], "word_count": r["word_count"], "status": r["status"],
            "canon_status": r["canon_status"], "qa_score": r["qa_score"],
            "blueprint": json.loads(r["blueprint"] or "{}"), "version": r["version"]
        } for r in cursor.fetchall()]

    def get_chapter(self, story_id: str, chapter_number: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chapters WHERE story_id = ? AND chapter_number = ?", (story_id, chapter_number))
        r = cursor.fetchone()
        if not r:
            return None
        return {
            "id": r["id"], "story_id": r["story_id"], "arc_id": r["arc_id"],
            "chapter_number": r["chapter_number"], "title": r["title"], "description": r["description"],
            "summary": r["summary"], "word_count": r["word_count"], "status": r["status"],
            "canon_status": r["canon_status"], "qa_score": r["qa_score"],
            "blueprint": json.loads(r["blueprint"] or "{}"), "version": r["version"]
        }

    # =========================================================================
    # 3. CHARACTERS & RELATIONSHIPS
    # =========================================================================

    def add_character(self, character: CharacterEntity) -> None:
        c_dict = character.to_dict()
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO characters (
                    id, story_id, name, aliases, age, gender, species_race,
                    appearance, personality, strengths, weaknesses, fears,
                    desires, goals, motivations, secrets, backstory, beliefs,
                    misconceptions, skills, abilities, cultivation_data,
                    voice_profile_data, current_location_id, current_location_name,
                    equipment_ids, emotional_state, character_arc, development_stage,
                    is_alive, canon_status, version, meta_info, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                character.id, character.story_id, character.name,
                json.dumps(character.aliases), character.age, character.gender,
                character.species_race, character.appearance, character.personality,
                json.dumps(character.strengths), json.dumps(character.weaknesses),
                json.dumps(character.fears), json.dumps(character.desires),
                json.dumps(character.goals), json.dumps(character.motivations),
                json.dumps(character.secrets), character.backstory,
                json.dumps(character.beliefs), json.dumps(character.misconceptions),
                json.dumps(character.skills), json.dumps(character.abilities),
                json.dumps(c_dict.get("cultivation", {})),
                json.dumps(c_dict.get("voice_profile", {})),
                character.current_location_id, character.current_location_name,
                json.dumps(character.equipment_ids), character.emotional_state,
                character.character_arc, character.development_stage,
                1 if character.is_alive else 0, character.canon_status.value,
                character.version, json.dumps(character.metadata),
                character.created_at, character.updated_at
            ))

    def get_character(self, story_id: str, character_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM characters WHERE story_id = ? AND id = ?", (story_id, character_id))
        r = cursor.fetchone()
        if not r:
            return None
        return self._char_row_to_dict(r)

    def get_characters(self, story_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM characters WHERE story_id = ?", (story_id,))
        return [self._char_row_to_dict(r) for r in cursor.fetchall()]

    def _char_row_to_dict(self, r: sqlite3.Row) -> Dict[str, Any]:
        return {
            "id": r["id"], "story_id": r["story_id"], "name": r["name"],
            "aliases": json.loads(r["aliases"] or "[]"), "age": r["age"],
            "gender": r["gender"], "species_race": r["species_race"],
            "appearance": r["appearance"] or "", "personality": r["personality"] or "",
            "strengths": json.loads(r["strengths"] or "[]"),
            "weaknesses": json.loads(r["weaknesses"] or "[]"),
            "fears": json.loads(r["fears"] or "[]"),
            "desires": json.loads(r["desires"] or "[]"),
            "goals": json.loads(r["goals"] or "[]"),
            "motivations": json.loads(r["motivations"] or "[]"),
            "secrets": json.loads(r["secrets"] or "[]"),
            "backstory": r["backstory"] or "",
            "beliefs": json.loads(r["beliefs"] or "[]"),
            "misconceptions": json.loads(r["misconceptions"] or "[]"),
            "skills": json.loads(r["skills"] or "[]"),
            "abilities": json.loads(r["abilities"] or "[]"),
            "cultivation": json.loads(r["cultivation_data"] or "{}"),
            "voice_profile": json.loads(r["voice_profile_data"] or "{}"),
            "current_location_id": r["current_location_id"] or "",
            "current_location_name": r["current_location_name"] or "",
            "equipment_ids": json.loads(r["equipment_ids"] or "[]"),
            "emotional_state": r["emotional_state"] or "Calm",
            "character_arc": r["character_arc"] or "",
            "development_stage": r["development_stage"] or "",
            "is_alive": bool(r["is_alive"]),
            "canon_status": r["canon_status"],
            "version": r["version"],
            "metadata": json.loads(r["meta_info"] or "{}")
        }

    def set_relationship(self, rel: CharacterRelationship) -> None:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, history_log, version FROM character_relationships
            WHERE story_id = ? AND source_character_id = ? AND target_character_id = ?
        """, (rel.story_id, rel.source_character_id, rel.target_character_id))
        existing = cursor.fetchone()

        now_str = datetime.datetime.utcnow().isoformat()
        if not existing:
            with self.conn:
                self.conn.execute("""
                    INSERT INTO character_relationships (
                        id, story_id, source_character_id, target_character_id,
                        relationship_type, strength, trust, hostility, status,
                        beginning_chapter, current_chapter, history_log, notes,
                        version, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    rel.id, rel.story_id, rel.source_character_id, rel.target_character_id,
                    rel.relationship_type.value, rel.strength, rel.trust, rel.hostility,
                    rel.status, rel.beginning_chapter, rel.current_chapter,
                    json.dumps(rel.history), rel.notes, rel.version, now_str
                ))
        else:
            history = json.loads(existing["history_log"] or "[]")
            history.append({
                "chapter": rel.current_chapter,
                "type": rel.relationship_type.value,
                "trust": rel.trust,
                "notes": rel.notes,
                "timestamp": now_str
            })
            new_version = existing["version"] + 1
            with self.conn:
                self.conn.execute("""
                    UPDATE character_relationships SET
                        relationship_type = ?, strength = ?, trust = ?,
                        hostility = ?, status = ?, current_chapter = ?,
                        history_log = ?, notes = ?, version = ?, updated_at = ?
                    WHERE id = ?
                """, (
                    rel.relationship_type.value, rel.strength, rel.trust,
                    rel.hostility, rel.status, rel.current_chapter,
                    json.dumps(history), rel.notes, new_version, now_str, existing["id"]
                ))

    def get_relationships(self, story_id: str, character_id: Optional[str] = None) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        if character_id:
            cursor.execute("""
                SELECT * FROM character_relationships 
                WHERE story_id = ? AND (source_character_id = ? OR target_character_id = ?)
            """, (story_id, character_id, character_id))
        else:
            cursor.execute("SELECT * FROM character_relationships WHERE story_id = ?", (story_id,))
        return [{
            "id": r["id"], "story_id": r["story_id"],
            "source_character_id": r["source_character_id"],
            "target_character_id": r["target_character_id"],
            "relationship_type": r["relationship_type"],
            "strength": r["strength"], "trust": r["trust"], "hostility": r["hostility"],
            "status": r["status"], "beginning_chapter": r["beginning_chapter"],
            "current_chapter": r["current_chapter"],
            "history": json.loads(r["history_log"] or "[]"),
            "notes": r["notes"], "version": r["version"]
        } for r in cursor.fetchall()]

    # =========================================================================
    # 4. KNOWLEDGE FACTS & EPISTEMIC TRACKING
    # =========================================================================

    def add_knowledge_fact(self, fact: KnowledgeFactEntity) -> None:
        f_dict = fact.to_dict()
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO knowledge_facts (
                    id, story_id, fact_key, description, is_true,
                    author_knowledge, reader_knowledge, character_knowledge_map,
                    planned_reveal_chapter, actual_revealed_chapter, canon_status,
                    version, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fact.id, fact.story_id, fact.fact_key, fact.description,
                1 if fact.is_true else 0, 1 if fact.author_knowledge else 0,
                1 if fact.reader_knowledge else 0,
                json.dumps(f_dict.get("character_knowledge_map", {})),
                fact.planned_reveal_chapter, fact.actual_revealed_chapter,
                fact.canon_status.value, fact.version, fact.created_at, fact.updated_at
            ))

    def update_character_knowledge(
        self,
        story_id: str,
        fact_key: str,
        character_id: str,
        character_name: str,
        state: KnowledgeState,
        chapter: int,
        story_day: int = 1,
        how_learned: str = ""
    ) -> None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT character_knowledge_map, version FROM knowledge_facts WHERE story_id = ? AND fact_key = ?", (story_id, fact_key))
        row = cursor.fetchone()
        if row:
            cmap = json.loads(row["character_knowledge_map"] or "{}")
            cmap[character_id] = {
                "character_id": character_id,
                "character_name": character_name,
                "state": state.value,
                "learned_at_chapter": chapter,
                "learned_at_story_day": story_day,
                "how_learned": how_learned,
                "is_misconception": state == KnowledgeState.KNOWN_FALSE
            }
            with self.conn:
                self.conn.execute("""
                    UPDATE knowledge_facts SET character_knowledge_map = ?, version = ?, updated_at = ?
                    WHERE story_id = ? AND fact_key = ?
                """, (
                    json.dumps(cmap), row["version"] + 1, datetime.datetime.utcnow().isoformat(),
                    story_id, fact_key
                ))

    def get_knowledge_facts(self, story_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM knowledge_facts WHERE story_id = ?", (story_id,))
        return [{
            "id": r["id"], "story_id": r["story_id"], "fact_key": r["fact_key"],
            "description": r["description"], "is_true": bool(r["is_true"]),
            "author_knowledge": bool(r["author_knowledge"]), "reader_knowledge": bool(r["reader_knowledge"]),
            "character_knowledge_map": json.loads(r["character_knowledge_map"] or "{}"),
            "planned_reveal_chapter": r["planned_reveal_chapter"],
            "actual_revealed_chapter": r["actual_revealed_chapter"],
            "canon_status": r["canon_status"], "version": r["version"]
        } for r in cursor.fetchall()]

    # =========================================================================
    # 5. WORLD ENGINE (Locations & Factions)
    # =========================================================================

    def add_location(self, loc: WorldLocation) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO world_locations (
                    id, story_id, name, type, description, parent_location_id,
                    controlling_faction_id, inhabitants_count_estimate,
                    political_status, resources, danger_level, history,
                    coordinates, known_secrets, canon_status, version, meta_info
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                loc.id, loc.story_id, loc.name, loc.type.value, loc.description,
                loc.parent_location_id, loc.controlling_faction_id,
                loc.inhabitants_count_estimate, loc.political_status,
                json.dumps(loc.resources), loc.danger_level, loc.history,
                json.dumps(loc.coordinates), json.dumps(loc.known_secrets),
                loc.canon_status.value, loc.version, json.dumps(loc.metadata)
            ))

    def get_locations(self, story_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM world_locations WHERE story_id = ?", (story_id,))
        return [{
            "id": r["id"], "story_id": r["story_id"], "name": r["name"], "type": r["type"],
            "description": r["description"], "parent_location_id": r["parent_location_id"],
            "controlling_faction_id": r["controlling_faction_id"],
            "inhabitants_count": r["inhabitants_count_estimate"],
            "political_status": r["political_status"],
            "resources": json.loads(r["resources"] or "[]"),
            "danger_level": r["danger_level"], "history": r["history"],
            "coordinates": json.loads(r["coordinates"] or "{\"x\":0.0,\"y\":0.0}"),
            "known_secrets": json.loads(r["known_secrets"] or "[]"),
            "canon_status": r["canon_status"], "version": r["version"]
        } for r in cursor.fetchall()]

    def add_faction(self, fac: FactionEntity) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO factions (
                    id, story_id, name, faction_type, description,
                    leader_character_id, headquarters_location_id, alignment,
                    military_strength_rating, allied_faction_ids, rival_faction_ids,
                    canon_status, version, meta_info
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fac.id, fac.story_id, fac.name, fac.faction_type, fac.description,
                fac.leader_character_id, fac.headquarters_location_id, fac.alignment,
                fac.military_strength_rating, json.dumps(fac.allied_faction_ids),
                json.dumps(fac.rival_faction_ids), fac.canon_status.value,
                fac.version, json.dumps(fac.metadata)
            ))

    def get_factions(self, story_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM factions WHERE story_id = ?", (story_id,))
        return [{
            "id": r["id"], "story_id": r["story_id"], "name": r["name"],
            "faction_type": r["faction_type"], "description": r["description"],
            "leader_character_id": r["leader_character_id"],
            "headquarters_location_id": r["headquarters_location_id"],
            "alignment": r["alignment"], "military_strength": r["military_strength_rating"],
            "allied_factions": json.loads(r["allied_faction_ids"] or "[]"),
            "rival_factions": json.loads(r["rival_faction_ids"] or "[]"),
            "canon_status": r["canon_status"], "version": r["version"]
        } for r in cursor.fetchall()]

    # =========================================================================
    # 6. STORY EVENTS & TIMELINE
    # =========================================================================

    def add_event(self, ev: StoryEventEntity) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO narrative_events (
                    id, story_id, chapter_number, scene_number, story_day,
                    story_year, real_world_timestamp, location_id, location_name,
                    participants, event_type, description, consequences,
                    canon_status, meta_info
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ev.id, ev.story_id, ev.chapter_number, ev.scene_number,
                ev.story_day, ev.story_year, ev.real_world_timestamp,
                ev.location_id, ev.location_name, json.dumps(ev.participants),
                ev.event_type.value, ev.description, json.dumps(ev.consequences),
                ev.canon_status.value, json.dumps(ev.metadata)
            ))

    def get_events(self, story_id: str, up_to_chapter: Optional[int] = None) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        if up_to_chapter is not None:
            cursor.execute("""
                SELECT * FROM narrative_events 
                WHERE story_id = ? AND chapter_number <= ?
                ORDER BY story_year ASC, story_day ASC, chapter_number ASC
            """, (story_id, up_to_chapter))
        else:
            cursor.execute("""
                SELECT * FROM narrative_events 
                WHERE story_id = ?
                ORDER BY story_year ASC, story_day ASC, chapter_number ASC
            """, (story_id,))
        return [{
            "id": r["id"], "story_id": r["story_id"], "chapter_number": r["chapter_number"],
            "scene_number": r["scene_number"], "story_day": r["story_day"],
            "story_year": r["story_year"], "real_world_timestamp": r["real_world_timestamp"],
            "location_id": r["location_id"], "location_name": r["location_name"],
            "participants": json.loads(r["participants"] or "[]"),
            "event_type": r["event_type"], "description": r["description"],
            "consequences": json.loads(r["consequences"] or "[]"),
            "canon_status": r["canon_status"]
        } for r in cursor.fetchall()]

    # =========================================================================
    # 7. CHAPTER MEMORIES
    # =========================================================================

    def save_chapter_memory(self, memory: ChapterMemory) -> None:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO chapter_memories (
                    id, story_id, chapter_number, chapter_summary,
                    important_events, characters_present, locations,
                    items_acquired_or_used, powers_revealed_or_leveled,
                    revelations_and_secrets, relationships_changed,
                    promises_introduced, promises_advanced, foreshadowing_introduced,
                    mysteries_advanced, unresolved_threads, emotional_state_changes, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()), memory.story_id, memory.chapter_number,
                memory.chapter_summary, json.dumps(memory.important_events),
                json.dumps(memory.characters_present), json.dumps(memory.locations),
                json.dumps(memory.items_acquired_or_used), json.dumps(memory.powers_revealed_or_leveled),
                json.dumps(memory.revelations_and_secrets), json.dumps(memory.relationships_changed),
                json.dumps(memory.promises_introduced), json.dumps(memory.promises_advanced),
                json.dumps(memory.foreshadowing_introduced), json.dumps(memory.mysteries_advanced),
                json.dumps(memory.unresolved_threads), json.dumps(memory.emotional_state_changes),
                datetime.datetime.utcnow().isoformat()
            ))

    def get_chapter_memory(self, story_id: str, chapter_number: int) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM chapter_memories WHERE story_id = ? AND chapter_number = ?", (story_id, chapter_number))
        r = cursor.fetchone()
        if not r:
            return None
        return {
            "story_id": r["story_id"], "chapter_number": r["chapter_number"],
            "chapter_summary": r["chapter_summary"],
            "important_events": json.loads(r["important_events"] or "[]"),
            "characters_present": json.loads(r["characters_present"] or "[]"),
            "locations": json.loads(r["locations"] or "[]"),
            "items_acquired_or_used": json.loads(r["items_acquired_or_used"] or "[]"),
            "powers_revealed_or_leveled": json.loads(r["powers_revealed_or_leveled"] or "[]"),
            "revelations_and_secrets": json.loads(r["revelations_and_secrets"] or "[]"),
            "relationships_changed": json.loads(r["relationships_changed"] or "[]"),
            "promises_introduced": json.loads(r["promises_introduced"] or "[]"),
            "promises_advanced": json.loads(r["promises_advanced"] or "[]"),
            "foreshadowing_introduced": json.loads(r["foreshadowing_introduced"] or "[]"),
            "mysteries_advanced": json.loads(r["mysteries_advanced"] or "[]"),
            "unresolved_threads": json.loads(r["unresolved_threads"] or "[]"),
            "emotional_state_changes": json.loads(r["emotional_state_changes"] or "{}")
        }

    # =========================================================================
    # 8. CANON PROTECTION, PROPOSALS & AUDIT LOG
    # =========================================================================

    def submit_proposal(self, proposal: ProposedChange) -> ProposedChange:
        with self.conn:
            self.conn.execute("""
                INSERT INTO proposed_changes (
                    id, story_id, agent, model, permission_level,
                    entity_type, entity_id, field_name, previous_value,
                    proposed_value, reason, status, approved_by, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                proposal.id, proposal.story_id, proposal.agent, proposal.model,
                proposal.permission_level.value, proposal.entity_type, proposal.entity_id,
                proposal.field_name, json.dumps(proposal.previous_value),
                json.dumps(proposal.proposed_value), proposal.reason,
                proposal.status.value, proposal.approved_by, proposal.created_at
            ))
            # Write audit log
            self.conn.execute("""
                INSERT INTO audit_logs (
                    id, story_id, timestamp, agent, model, action,
                    entity_type, entity_id, previous_value, new_value,
                    reason, approval_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()), proposal.story_id, datetime.datetime.utcnow().isoformat(),
                proposal.agent, proposal.model, "PROPOSAL_CREATED", proposal.entity_type,
                proposal.entity_id, json.dumps(proposal.previous_value),
                json.dumps(proposal.proposed_value), proposal.reason, "PENDING"
            ))
        return proposal

    def approve_proposal(
        self,
        proposal_id: str,
        approver: str,
        permission_level: PermissionLevel
    ) -> bool:
        if permission_level not in [PermissionLevel.CANON_EDITOR, PermissionLevel.SYSTEM]:
            raise PermissionError("Unauthorized: Only CANON_EDITOR or SYSTEM may approve canon proposals.")

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM proposed_changes WHERE id = ?", (proposal_id,))
        prop = cursor.fetchone()
        if not prop or prop["status"] != "PENDING":
            return False

        now_str = datetime.datetime.utcnow().isoformat()
        with self.conn:
            self.conn.execute("""
                UPDATE proposed_changes SET status = 'APPROVED', approved_by = ?, reviewed_at = ?
                WHERE id = ?
            """, (approver, now_str, proposal_id))

            # Apply mutation to character if entity_type == 'CHARACTER'
            if prop["entity_type"] == "CHARACTER":
                val = json.loads(prop["proposed_value"])
                field_name = prop["field_name"]
                if field_name in ["age", "gender", "species_race", "current_location_name", "emotional_state"]:
                    self.conn.execute(f"UPDATE characters SET {field_name} = ?, version = version + 1, updated_at = ? WHERE id = ?",
                                      (val, now_str, prop["entity_id"]))

            # Write Audit Log
            self.conn.execute("""
                INSERT INTO audit_logs (
                    id, story_id, timestamp, agent, model, action,
                    entity_type, entity_id, previous_value, new_value,
                    reason, approval_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(uuid.uuid4()), prop["story_id"], now_str, approver, "manual/director",
                "CANON_MUTATED", prop["entity_type"], prop["entity_id"],
                prop["previous_value"], prop["proposed_value"],
                f"Approved proposal: {prop['reason']}", "APPROVED"
            ))
        return True

    def get_audit_logs(self, story_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM audit_logs WHERE story_id = ? ORDER BY timestamp DESC", (story_id,))
        return [{
            "id": r["id"], "story_id": r["story_id"], "timestamp": r["timestamp"],
            "agent": r["agent"], "model": r["model"], "action": r["action"],
            "entity_type": r["entity_type"], "entity_id": r["entity_id"],
            "previous_value": json.loads(r["previous_value"] or "null"),
            "new_value": json.loads(r["new_value"] or "null"),
            "reason": r["reason"], "approval_status": r["approval_status"]
        } for r in cursor.fetchall()]

    def get_proposals(self, story_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        if status:
            cursor.execute("SELECT * FROM proposed_changes WHERE story_id = ? AND status = ?", (story_id, status))
        else:
            cursor.execute("SELECT * FROM proposed_changes WHERE story_id = ?", (story_id,))
        return [{
            "id": r["id"], "story_id": r["story_id"], "agent": r["agent"],
            "model": r["model"], "entity_type": r["entity_type"], "entity_id": r["entity_id"],
            "field_name": r["field_name"],
            "previous_value": json.loads(r["previous_value"] or "null"),
            "proposed_value": json.loads(r["proposed_value"] or "null"),
            "reason": r["reason"], "status": r["status"],
            "approved_by": r["approved_by"], "created_at": r["created_at"]
        } for r in cursor.fetchall()]

    # =========================================================================
    # 9. STATE SNAPSHOTS & HISTORICAL TIME-TRAVEL RECONSTRUCTION
    # =========================================================================

    def get_story_state_snapshot(
        self,
        story_id: str,
        at_chapter: Optional[int] = None
    ) -> StoryStateSnapshot:
        story = self.get_story(story_id)
        current_ch = at_chapter if at_chapter is not None else (story.current_chapter if story else 1)
        current_arc = story.current_arc if story else 1
        current_saga = story.current_saga if story else 1

        characters = self.get_characters(story_id)
        active_chars = []
        char_locations = {}
        char_powers = {}
        equipment_map = {}

        for c in characters:
            if c.get("is_alive", True):
                active_chars.append({"id": c["id"], "name": c["name"], "age": c["age"], "gender": c["gender"]})
                char_locations[c["name"]] = c.get("current_location_name", "Unknown")
                cult = c.get("cultivation", {})
                char_powers[c["name"]] = f"{cult.get('realm', 'Novice')} ({cult.get('sub_realm', 'Early')}, Rank {cult.get('rank_level', 1)})"
                for itm in c.get("equipment_ids", []):
                    equipment_map[itm] = c["name"]

        relationships = self.get_relationships(story_id)
        factions = self.get_factions(story_id)
        recent_events = self.get_events(story_id, up_to_chapter=current_ch)

        recent_mem = self.get_chapter_memory(story_id, current_ch)
        recent_summary = recent_mem.get("chapter_summary", "") if recent_mem else ""

        facts = self.get_knowledge_facts(story_id)
        active_mysteries = []
        for f in facts:
            if not f.get("reader_knowledge", False):
                active_mysteries.append({
                    "fact_key": f["fact_key"],
                    "description": f["description"],
                    "planned_reveal": f.get("planned_reveal_chapter", 0)
                })

        return StoryStateSnapshot(
            story_id=story_id,
            current_chapter=current_ch,
            current_arc=current_arc,
            current_saga=current_saga,
            active_characters=active_chars,
            character_locations=char_locations,
            character_power_levels=char_powers,
            character_relationships=relationships,
            current_world_state={"total_locations": len(self.get_locations(story_id))},
            current_factions=factions,
            equipment_ownership=equipment_map,
            active_mysteries=active_mysteries,
            active_promises=[],
            active_foreshadowing=[],
            open_plot_threads=["Escaping the city", "Securing Blackwood Bunker"],
            recent_events=recent_events[-5:] if recent_events else [],
            recent_chapter_summary=recent_summary,
            upcoming_planned_events=[]
        )
