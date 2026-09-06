"""
NovelForge AI — SQLAlchemy ORM Models
Phase 2: Narrative State Engine Database Layer
"""
from __future__ import annotations
import uuid
import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, Index, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Story(Base):
    __tablename__ = "stories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    working_title = Column(String(255), default="")
    premise = Column(Text, default="")
    genre = Column(String(100), default="Progression Fantasy")
    subgenres = Column(JSON, default=list)
    target_audience = Column(String(100), default="Young Adult / Web Novel Readers")
    tone = Column(String(100), default="Dark / Humorous")
    themes = Column(JSON, default=list)
    narrative_style = Column(String(100), default="Third Person Limited")
    target_chapter_count = Column(Integer, default=500)
    target_chapter_word_count = Column(Integer, default=2000)
    planned_ending = Column(Text, default="")
    current_saga = Column(Integer, default=1)
    current_arc = Column(Integer, default=1)
    current_chapter = Column(Integer, default=1)
    status = Column(String(32), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    meta_info = Column(JSON, default=dict)


class StoryBibleRecord(Base):
    __tablename__ = "story_bibles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), unique=True, nullable=False)
    premise_data = Column(JSON, default=dict)
    themes_data = Column(JSON, default=dict)
    tone_data = Column(JSON, default=dict)
    narrative_rules_data = Column(JSON, default=dict)
    world_rules_data = Column(JSON, default=dict)
    version = Column(Integer, default=1)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class SagaRecord(Base):
    __tablename__ = "sagas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    sequence_order = Column(Integer, default=1)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    start_chapter = Column(Integer, default=1)
    end_chapter = Column(Integer, default=100)
    summary = Column(Text, default="")
    objectives = Column(JSON, default=list)
    status = Column(String(32), default="PLANNED")
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class ArcRecord(Base):
    __tablename__ = "arcs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    saga_id = Column(String(36), ForeignKey("sagas.id", ondelete="SET NULL"), nullable=True)
    sequence_order = Column(Integer, default=1)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    start_chapter = Column(Integer, default=1)
    end_chapter = Column(Integer, default=30)
    summary = Column(Text, default="")
    objectives = Column(JSON, default=list)
    status = Column(String(32), default="PLANNED")
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class ChapterRecord(Base):
    __tablename__ = "chapters"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    arc_id = Column(String(36), ForeignKey("arcs.id", ondelete="SET NULL"), nullable=True)
    chapter_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    summary = Column(Text, default="")
    objectives = Column(JSON, default=list)
    word_count = Column(Integer, default=0)
    status = Column(String(32), default="PLANNED")
    canon_status = Column(String(32), default="DRAFT")
    qa_score = Column(Float, nullable=True)
    blueprint = Column(JSON, default=dict)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index("idx_story_chapter_num", "story_id", "chapter_number", unique=True),
    )


class SceneRecord(Base):
    __tablename__ = "scenes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    chapter_id = Column(String(36), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    scene_number = Column(Integer, default=1)
    name = Column(String(255), default="")
    pov_character_id = Column(String(36), nullable=True)
    location_id = Column(String(36), nullable=True)
    objective = Column(Text, default="")
    conflict = Column(Text, default="")
    content = Column(Text, default="")
    word_count = Column(Integer, default=0)
    status = Column(String(32), default="DRAFT")
    canon_status = Column(String(32), default="DRAFT")
    local_state_delta = Column(JSON, default=dict)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class CharacterRecord(Base):
    __tablename__ = "characters"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    aliases = Column(JSON, default=list)
    age = Column(Integer, default=20)
    gender = Column(String(32), default="Unknown")
    species_race = Column(String(64), default="Human")
    appearance = Column(Text, default="")
    personality = Column(Text, default="")
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    fears = Column(JSON, default=list)
    desires = Column(JSON, default=list)
    goals = Column(JSON, default=list)
    motivations = Column(JSON, default=list)
    secrets = Column(JSON, default=list)
    backstory = Column(Text, default="")
    beliefs = Column(JSON, default=list)
    misconceptions = Column(JSON, default=list)
    skills = Column(JSON, default=list)
    abilities = Column(JSON, default=list)
    cultivation_data = Column(JSON, default=dict)
    voice_profile_data = Column(JSON, default=dict)
    current_location_id = Column(String(36), default="")
    current_location_name = Column(String(255), default="Unknown")
    equipment_ids = Column(JSON, default=list)
    emotional_state = Column(String(128), default="Calm")
    character_arc = Column(Text, default="")
    development_stage = Column(String(64), default="Initial Stage")
    is_alive = Column(Boolean, default=True)
    canon_status = Column(String(32), default="CANON")
    version = Column(Integer, default=1)
    meta_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class CharacterRelationshipRecord(Base):
    __tablename__ = "character_relationships"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    source_character_id = Column(String(36), ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    target_character_id = Column(String(36), ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(String(64), default="UNKNOWN")
    strength = Column(Float, default=0.5)
    trust = Column(Float, default=0.5)
    hostility = Column(Float, default=0.0)
    status = Column(String(32), default="ACTIVE")
    beginning_chapter = Column(Integer, default=1)
    current_chapter = Column(Integer, default=1)
    history_log = Column(JSON, default=list)
    notes = Column(Text, default="")
    version = Column(Integer, default=1)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class KnowledgeFactRecord(Base):
    __tablename__ = "knowledge_facts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    fact_key = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    is_true = Column(Boolean, default=True)
    author_knowledge = Column(Boolean, default=True)
    reader_knowledge = Column(Boolean, default=False)
    character_knowledge_map = Column(JSON, default=dict)
    planned_reveal_chapter = Column(Integer, default=0)
    actual_revealed_chapter = Column(Integer, nullable=True)
    canon_status = Column(String(32), default="CANON")
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index("idx_story_fact_key", "story_id", "fact_key", unique=True),
    )


class WorldLocationRecord(Base):
    __tablename__ = "world_locations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(64), default="CITY")
    description = Column(Text, default="")
    parent_location_id = Column(String(36), nullable=True)
    controlling_faction_id = Column(String(36), nullable=True)
    inhabitants_count_estimate = Column(Integer, default=0)
    political_status = Column(String(64), default="Neutral")
    resources = Column(JSON, default=list)
    danger_level = Column(String(32), default="Low")
    history = Column(Text, default="")
    coordinates = Column(JSON, default=lambda: {"x": 0.0, "y": 0.0})
    known_secrets = Column(JSON, default=list)
    canon_status = Column(String(32), default="CANON")
    version = Column(Integer, default=1)
    meta_info = Column(JSON, default=dict)


class FactionRecord(Base):
    __tablename__ = "factions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    faction_type = Column(String(64), default="Sect")
    description = Column(Text, default="")
    leader_character_id = Column(String(36), nullable=True)
    headquarters_location_id = Column(String(36), nullable=True)
    alignment = Column(String(64), default="Neutral")
    military_strength_rating = Column(Float, default=5.0)
    allied_faction_ids = Column(JSON, default=list)
    rival_faction_ids = Column(JSON, default=list)
    canon_status = Column(String(32), default="CANON")
    version = Column(Integer, default=1)
    meta_info = Column(JSON, default=dict)


class StoryEventRecord(Base):
    __tablename__ = "narrative_events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    scene_number = Column(Integer, default=1)
    story_day = Column(Integer, default=1)
    story_year = Column(Integer, default=1)
    real_world_timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    location_id = Column(String(36), default="")
    location_name = Column(String(255), default="")
    participants = Column(JSON, default=list)
    event_type = Column(String(64), default="DISCOVERY")
    description = Column(Text, default="")
    consequences = Column(JSON, default=list)
    canon_status = Column(String(32), default="CANON")
    meta_info = Column(JSON, default=dict)

    __table_args__ = (
        Index("idx_event_story_chronology", "story_id", "story_year", "story_day"),
    )


class StoryFactRecord(Base):
    __tablename__ = "story_facts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    subject = Column(String(255), nullable=False)
    predicate = Column(String(128), nullable=False)
    object_value = Column(Text, nullable=False)
    source = Column(String(128), default="Narrative")
    chapter_introduced = Column(Integer, default=1)
    confidence = Column(Float, default=1.0)
    canon_status = Column(String(32), default="CANON")
    visibility = Column(String(32), default="PUBLIC")
    applicable_entities = Column(JSON, default=list)


class ChapterMemoryRecord(Base):
    __tablename__ = "chapter_memories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    chapter_summary = Column(Text, default="")
    important_events = Column(JSON, default=list)
    characters_present = Column(JSON, default=list)
    locations = Column(JSON, default=list)
    items_acquired_or_used = Column(JSON, default=list)
    powers_revealed_or_leveled = Column(JSON, default=list)
    revelations_and_secrets = Column(JSON, default=list)
    relationships_changed = Column(JSON, default=list)
    promises_introduced = Column(JSON, default=list)
    promises_advanced = Column(JSON, default=list)
    foreshadowing_introduced = Column(JSON, default=list)
    mysteries_advanced = Column(JSON, default=list)
    unresolved_threads = Column(JSON, default=list)
    emotional_state_changes = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        Index("idx_chapter_memory_lookup", "story_id", "chapter_number", unique=True),
    )


class ProposedChangeRecord(Base):
    __tablename__ = "proposed_changes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    agent = Column(String(128), default="")
    model = Column(String(128), default="")
    permission_level = Column(String(64), default="PROPOSAL_AGENT")
    entity_type = Column(String(64), nullable=False)
    entity_id = Column(String(36), nullable=False)
    field_name = Column(String(64), nullable=False)
    previous_value = Column(JSON, nullable=True)
    proposed_value = Column(JSON, nullable=True)
    reason = Column(Text, default="")
    status = Column(String(32), default="PENDING")
    approved_by = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)


class AuditLogRecordModel(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String(36), ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    agent = Column(String(128), default="")
    model = Column(String(128), default="")
    action = Column(String(64), nullable=False)
    entity_type = Column(String(64), nullable=False)
    entity_id = Column(String(36), nullable=False)
    previous_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    reason = Column(Text, default="")
    approval_status = Column(String(32), default="APPROVED")
