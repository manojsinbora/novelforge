"""
NovelForge AI — Comprehensive Narrative Schemas & Entity Definitions
Phase 2: Narrative State Engine & Story Bible System
Supports Python standard library (dataclasses) and Pydantic v2.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from enum import Enum
import uuid
import datetime
import json


# =====================================================================
# ENUMS & CONSTANTS
# =====================================================================

class EntityStatus(str, Enum):
    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"
    CANCELLED = "CANCELLED"


class CanonStatus(str, Enum):
    CANON = "CANON"
    PROVISIONAL = "PROVISIONAL"
    DRAFT = "DRAFT"
    DEPRECATED = "DEPRECATED"


class PermissionLevel(str, Enum):
    READ_ONLY_AGENT = "READ_ONLY_AGENT"
    PROPOSAL_AGENT = "PROPOSAL_AGENT"
    CANON_EDITOR = "CANON_EDITOR"
    SYSTEM = "SYSTEM"


class KnowledgeState(str, Enum):
    UNKNOWN = "UNKNOWN"
    SUSPECTED = "SUSPECTED"
    BELIEVED_TRUE = "BELIEVED_TRUE"
    KNOWN_TRUE = "KNOWN_TRUE"
    KNOWN_FALSE = "KNOWN_FALSE"
    PARTIALLY_KNOWN = "PARTIALLY_KNOWN"


class RelationshipType(str, Enum):
    FRIEND = "FRIEND"
    ALLY = "ALLY"
    RIVAL = "RIVAL"
    ENEMY = "ENEMY"
    MASTER = "MASTER"
    STUDENT = "STUDENT"
    FAMILY = "FAMILY"
    ROMANTIC = "ROMANTIC"
    POLITICAL = "POLITICAL"
    EMPLOYER = "EMPLOYER"
    SERVANT = "SERVANT"
    UNKNOWN = "UNKNOWN"


class LocationType(str, Enum):
    WORLD = "WORLD"
    CONTINENT = "CONTINENT"
    COUNTRY = "COUNTRY"
    KINGDOM = "KINGDOM"
    PROVINCE = "PROVINCE"
    CITY = "CITY"
    VILLAGE = "VILLAGE"
    SECT = "SECT"
    CLAN = "CLAN"
    LANDMARK = "LANDMARK"
    BUILDING = "BUILDING"
    ROOM = "ROOM"


class StoryEventType(str, Enum):
    BATTLE = "BATTLE"
    DEATH = "DEATH"
    MEETING = "MEETING"
    DISCOVERY = "DISCOVERY"
    BREAKTHROUGH = "BREAKTHROUGH"
    BETRAYAL = "BETRAYAL"
    REVELATION = "REVELATION"
    TRAVEL = "TRAVEL"
    ROMANCE = "ROMANCE"
    POLITICAL_CHANGE = "POLITICAL_CHANGE"
    ITEM_ACQUIRED = "ITEM_ACQUIRED"
    ITEM_LOST = "ITEM_LOST"
    RELATIONSHIP_CHANGE = "RELATIONSHIP_CHANGE"


class FactVisibility(str, Enum):
    PUBLIC = "PUBLIC"
    READER_ONLY = "READER_ONLY"
    CHARACTER_ONLY = "CHARACTER_ONLY"
    HIDDEN = "HIDDEN"
    SECRET = "SECRET"


class ProposalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


# =====================================================================
# 1. STORY HIERARCHY ENTITIES
# =====================================================================

@dataclass
class StoryEntityBase:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    story_id: str = ""
    name: str = ""
    description: str = ""
    status: EntityStatus = EntityStatus.PLANNED
    version: int = 1
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Saga(StoryEntityBase):
    sequence_order: int = 1
    start_chapter: int = 1
    end_chapter: int = 100
    summary: str = ""
    objectives: List[str] = field(default_factory=list)


@dataclass
class Arc(StoryEntityBase):
    saga_id: str = ""
    sequence_order: int = 1
    start_chapter: int = 1
    end_chapter: int = 30
    summary: str = ""
    objectives: List[str] = field(default_factory=list)


@dataclass
class Chapter(StoryEntityBase):
    arc_id: str = ""
    chapter_number: int = 1
    title: str = ""
    summary: str = ""
    objectives: List[str] = field(default_factory=list)
    word_count: int = 0
    canon_status: CanonStatus = CanonStatus.DRAFT
    qa_score: Optional[float] = None
    blueprint: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Scene(StoryEntityBase):
    chapter_id: str = ""
    scene_number: int = 1
    pov_character_id: str = ""
    location_id: str = ""
    objective: str = ""
    conflict: str = ""
    content: str = ""
    word_count: int = 0
    canon_status: CanonStatus = CanonStatus.DRAFT
    local_state_delta: Dict[str, Any] = field(default_factory=dict)


# =====================================================================
# 2. STORY MODEL & STORY BIBLE
# =====================================================================

@dataclass
class StoryPremise:
    core_premise: str = ""
    elevator_pitch: str = ""
    central_conflict: str = ""
    protagonist_objective: str = ""
    primary_antagonist: str = ""
    ultimate_stakes: str = ""

@dataclass
class StoryThemes:
    major_themes: List[str] = field(default_factory=list)
    minor_themes: List[str] = field(default_factory=list)
    moral_questions: List[str] = field(default_factory=list)
    recurring_motifs: List[str] = field(default_factory=list)

@dataclass
class StoryTone:
    darkness: float = 0.5        # 0.0 (wholesome) to 1.0 (grimdark)
    humor: float = 0.5           # 0.0 (dead serious) to 1.0 (pure comedy)
    seriousness: float = 0.7
    emotional_intensity: float = 0.8
    violence_level: float = 0.6
    romance_level: float = 0.3

@dataclass
class NarrativeRules:
    pov_rules: str = "Third Person Limited"
    tense: str = "Past Tense"
    chapter_style: str = "Serial Web Novel"
    dialogue_preferences: str = "Fast, character-specific cadences, witty banter"
    pacing_preferences: str = "Fast escalation with chapter-end cliffhangers"
    exposition_limits: str = "Show don't tell; maximum 2 paragraphs of lore per scene"
    combat_style: str = "Tactical, anatomical, visceral, rule-consistent"
    romance_style: str = "Slow-burn, subtle, mutual respect"

@dataclass
class WorldRules:
    magic_rules: Dict[str, Any] = field(default_factory=dict)
    cultivation_rules: Dict[str, Any] = field(default_factory=dict)
    technology_rules: Dict[str, Any] = field(default_factory=dict)
    physics_exceptions: List[str] = field(default_factory=list)
    supernatural_rules: List[str] = field(default_factory=list)
    political_rules: List[str] = field(default_factory=list)
    economic_rules: List[str] = field(default_factory=list)

@dataclass
class StoryBible:
    story_id: str
    premise: StoryPremise = field(default_factory=StoryPremise)
    themes: StoryThemes = field(default_factory=StoryThemes)
    tone: StoryTone = field(default_factory=StoryTone)
    narrative_rules: NarrativeRules = field(default_factory=NarrativeRules)
    world_rules: WorldRules = field(default_factory=WorldRules)
    version: int = 1
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class StoryModel:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    working_title: str = ""
    premise: str = ""
    genre: str = ""
    subgenres: List[str] = field(default_factory=list)
    target_audience: str = ""
    tone: str = ""
    themes: List[str] = field(default_factory=list)
    narrative_style: str = ""
    target_chapter_count: int = 500
    target_chapter_word_count: int = 2000
    planned_ending: str = ""
    current_saga: int = 1
    current_arc: int = 1
    current_chapter: int = 1
    status: EntityStatus = EntityStatus.ACTIVE
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =====================================================================
# 3. CANON SYSTEM & AUDIT LOGS
# =====================================================================

@dataclass
class ProposedChange:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    story_id: str = ""
    agent: str = ""
    model: str = ""
    permission_level: PermissionLevel = PermissionLevel.PROPOSAL_AGENT
    entity_type: str = ""  # CHARACTER, LOCATION, BIBLE, FACT
    entity_id: str = ""
    field_name: str = ""
    previous_value: Any = None
    proposed_value: Any = None
    reason: str = ""
    status: ProposalStatus = ProposalStatus.PENDING
    approved_by: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    reviewed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AuditLogRecord:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    story_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    agent: str = ""
    model: str = ""
    action: str = ""  # PROPOSAL_CREATED, PROPOSAL_APPROVED, CANON_MUTATED, REVERT
    entity_type: str = ""
    entity_id: str = ""
    previous_value: Any = None
    new_value: Any = None
    reason: str = ""
    approval_status: str = "APPROVED"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =====================================================================
# 4. CHARACTER ENGINE & RELATIONSHIPS
# =====================================================================

@dataclass
class CharacterCultivationProfile:
    realm: str = "Novice"
    sub_realm: str = "Early"
    rank_level: int = 1
    active_techniques: List[str] = field(default_factory=list)
    special_physique: Optional[str] = None
    bottleneck: Optional[str] = None

@dataclass
class CharacterVoiceProfile:
    sentence_cadence: str = "balanced"
    vocabulary_tier: str = "standard"
    verbal_tics: List[str] = field(default_factory=list)
    formality_level: float = 0.5
    banned_words: List[str] = field(default_factory=list)

@dataclass
class CharacterEntity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    story_id: str = ""
    name: str = ""
    aliases: List[str] = field(default_factory=list)
    age: int = 20
    gender: str = "Unknown"
    species_race: str = "Human"
    appearance: str = ""
    personality: str = ""
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    desires: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    motivations: List[str] = field(default_factory=list)
    secrets: List[str] = field(default_factory=list)
    backstory: str = ""
    beliefs: List[str] = field(default_factory=list)
    misconceptions: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    abilities: List[str] = field(default_factory=list)
    cultivation: CharacterCultivationProfile = field(default_factory=CharacterCultivationProfile)
    voice_profile: CharacterVoiceProfile = field(default_factory=CharacterVoiceProfile)
    current_location_id: str = ""
    current_location_name: str = "Unknown"
    equipment_ids: List[str] = field(default_factory=list)
    emotional_state: str = "Calm"
    character_arc: str = "Underdog to Sovereign"
    development_stage: str = "Initial Stage"
    is_alive: bool = True
    canon_status: CanonStatus = CanonStatus.CANON
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class CharacterRelationship:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    story_id: str = ""
    source_character_id: str = ""
    target_character_id: str = ""
    relationship_type: RelationshipType = RelationshipType.UNKNOWN
    strength: float = 0.5     # 0.0 to 1.0
    trust: float = 0.5        # -1.0 (extreme distrust) to +1.0 (absolute trust)
    hostility: float = 0.0    # 0.0 (peaceful) to 1.0 (kill on sight)
    status: str = "ACTIVE"
    beginning_chapter: int = 1
    current_chapter: int = 1
    history: List[Dict[str, Any]] = field(default_factory=list)
    notes: str = ""
    version: int = 1
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =====================================================================
# 5. EPISTEMIC KNOWLEDGE SYSTEM
# =====================================================================

@dataclass
class FactKnowledgeEntry:
    character_id: str
    character_name: str
    state: KnowledgeState = KnowledgeState.UNKNOWN
    learned_at_chapter: Optional[int] = None
    learned_at_story_day: Optional[int] = None
    how_learned: str = ""
    is_misconception: bool = False

@dataclass
class KnowledgeFactEntity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    story_id: str = ""
    fact_key: str = ""
    description: str = ""
    is_true: bool = True
    author_knowledge: bool = True
    reader_knowledge: bool = False
    character_knowledge_map: Dict[str, FactKnowledgeEntry] = field(default_factory=dict)
    planned_reveal_chapter: int = 0
    actual_revealed_chapter: Optional[int] = None
    canon_status: CanonStatus = CanonStatus.CANON
    version: int = 1
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def is_known_by(self, character_id: str, at_chapter: Optional[int] = None) -> bool:
        entry = self.character_knowledge_map.get(character_id)
        if not entry:
            return False
        if entry.state not in [KnowledgeState.KNOWN_TRUE, KnowledgeState.BELIEVED_TRUE, KnowledgeState.PARTIALLY_KNOWN]:
            return False
        if at_chapter is not None and entry.learned_at_chapter is not None:
            return entry.learned_at_chapter <= at_chapter
        return True


# =====================================================================
# 6. WORLD ENGINE & LOCATIONS
# =====================================================================

@dataclass
class WorldLocation:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    story_id: str = ""
    name: str = ""
    type: LocationType = LocationType.CITY
    description: str = ""
    parent_location_id: Optional[str] = None
    controlling_faction_id: Optional[str] = None
    inhabitants_count_estimate: int = 0
    political_status: str = "Neutral"
    resources: List[str] = field(default_factory=list)
    danger_level: str = "Low"  # Safe, Low, Moderate, High, Lethal, Extreme
    history: str = ""
    coordinates: Dict[str, float] = field(default_factory=lambda: {"x": 0.0, "y": 0.0})
    known_secrets: List[str] = field(default_factory=list)
    canon_status: CanonStatus = CanonStatus.CANON
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class FactionEntity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    story_id: str = ""
    name: str = ""
    faction_type: str = "Sect" # Sect, Clan, Guild, Warlord Cabal, Kingdom, Corporation
    description: str = ""
    leader_character_id: Optional[str] = None
    headquarters_location_id: Optional[str] = None
    alignment: str = "Neutral"
    military_strength_rating: float = 5.0
    allied_faction_ids: List[str] = field(default_factory=list)
    rival_faction_ids: List[str] = field(default_factory=list)
    canon_status: CanonStatus = CanonStatus.CANON
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =====================================================================
# 7. STORY EVENTS & TIMELINE
# =====================================================================

@dataclass
class StoryEventEntity:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    story_id: str = ""
    chapter_number: int = 1
    scene_number: int = 1
    story_day: int = 1
    story_year: int = 1
    real_world_timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    location_id: str = ""
    location_name: str = ""
    participants: List[str] = field(default_factory=list)
    event_type: StoryEventType = StoryEventType.DISCOVERY
    description: str = ""
    consequences: List[str] = field(default_factory=list)
    canon_status: CanonStatus = CanonStatus.CANON
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =====================================================================
# 8. STORY FACTS & CHAPTER MEMORY
# =====================================================================

@dataclass
class StoryFactTriplet:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    story_id: str = ""
    subject: str = ""
    predicate: str = ""
    object_value: str = ""
    source: str = "Narrative"
    chapter_introduced: int = 1
    confidence: float = 1.0
    canon_status: CanonStatus = CanonStatus.CANON
    visibility: FactVisibility = FactVisibility.PUBLIC
    applicable_entities: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ChapterMemory:
    story_id: str
    chapter_number: int
    chapter_summary: str = ""
    important_events: List[str] = field(default_factory=list)
    characters_present: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    items_acquired_or_used: List[str] = field(default_factory=list)
    powers_revealed_or_leveled: List[str] = field(default_factory=list)
    revelations_and_secrets: List[str] = field(default_factory=list)
    relationships_changed: List[str] = field(default_factory=list)
    promises_introduced: List[str] = field(default_factory=list)
    promises_advanced: List[str] = field(default_factory=list)
    foreshadowing_introduced: List[str] = field(default_factory=list)
    mysteries_advanced: List[str] = field(default_factory=list)
    unresolved_threads: List[str] = field(default_factory=list)
    emotional_state_changes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =====================================================================
# 9. STORY STATE SNAPSHOT
# =====================================================================

@dataclass
class StoryStateSnapshot:
    story_id: str
    current_chapter: int
    current_arc: int
    current_saga: int
    active_characters: List[Dict[str, Any]] = field(default_factory=list)
    character_locations: Dict[str, str] = field(default_factory=dict)
    character_power_levels: Dict[str, str] = field(default_factory=dict)
    character_relationships: List[Dict[str, Any]] = field(default_factory=list)
    current_world_state: Dict[str, Any] = field(default_factory=dict)
    current_factions: List[Dict[str, Any]] = field(default_factory=list)
    equipment_ownership: Dict[str, str] = field(default_factory=dict)
    active_mysteries: List[Dict[str, Any]] = field(default_factory=list)
    active_promises: List[Dict[str, Any]] = field(default_factory=list)
    active_foreshadowing: List[Dict[str, Any]] = field(default_factory=list)
    open_plot_threads: List[str] = field(default_factory=list)
    recent_events: List[Dict[str, Any]] = field(default_factory=list)
    recent_chapter_summary: str = ""
    upcoming_planned_events: List[str] = field(default_factory=list)
    reconstructed_at_timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
