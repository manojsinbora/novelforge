"""
NovelForge AI — Story Schema & Entity Definitions
Supports Python standard library (dataclasses) and Pydantic if installed.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from enum import Enum
import uuid
import json


class KnowledgeScope(str, Enum):
    AUTHOR_ONLY = "AUTHOR_ONLY"
    AUTHOR_AND_READER = "AUTHOR_AND_READER"
    AUTHOR_AND_CHARACTER = "AUTHOR_AND_CHARACTER"
    UNIVERSAL = "UNIVERSAL"


class PromiseStatus(str, Enum):
    OPEN = "OPEN"
    ACTIVE = "ACTIVE"
    DEVELOPING = "DEVELOPING"
    APPROACHING_PAYOFF = "APPROACHING_PAYOFF"
    OVERDUE = "OVERDUE"
    RESOLVED = "RESOLVED"


class EventType(str, Enum):
    CHARACTER_CREATED = "CHARACTER_CREATED"
    CHARACTER_PROMOTED = "CHARACTER_PROMOTED"
    ITEM_TRANSFERRED = "ITEM_TRANSFERRED"
    SECRET_REVEALED = "SECRET_REVEALED"
    PROMISE_CREATED = "PROMISE_CREATED"
    PROMISE_RESOLVED = "PROMISE_RESOLVED"
    FORESHADOWING_SEEDED = "FORESHADOWING_SEEDED"
    FORESHADOWING_CLUE_ADDED = "FORESHADOWING_CLUE_ADDED"
    CHAPTER_COMMITTED = "CHAPTER_COMMITTED"


@dataclass
class VoiceProfile:
    sentence_cadence: str = "balanced"
    vocabulary_tier: str = "standard"
    verbal_tics: List[str] = field(default_factory=list)
    formality_level: float = 0.5
    banned_words: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CultivationState:
    realm: str = "Mortal"
    sub_realm: str = "None"
    rank_level: int = 1
    active_techniques: List[str] = field(default_factory=list)
    spiritual_root: str = "Mortal Grade"
    bottleneck: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Character:
    id: str
    name: str
    age: int
    gender: str
    personality_traits: List[str] = field(default_factory=list)
    driving_want: str = ""
    core_fear: str = ""
    voice_profile: VoiceProfile = field(default_factory=VoiceProfile)
    cultivation: CultivationState = field(default_factory=CultivationState)
    current_location: str = "Unknown"
    equipped_items: List[str] = field(default_factory=list)
    is_alive: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class KnowledgeFact:
    fact_key: str
    description: str
    author_knows: bool = True
    reader_knows: bool = False
    known_by_characters: List[str] = field(default_factory=list)
    planned_reveal_chapter: int = 0
    actual_revealed_chapter: Optional[int] = None

    def is_known_by(self, character_id: str) -> bool:
        return character_id in self.known_by_characters


@dataclass
class Promise:
    id: str
    title: str
    description: str
    introduced_chapter: int
    expected_payoff_min: int
    expected_payoff_max: int
    status: PromiseStatus = PromiseStatus.OPEN
    resolution_chapter: Optional[int] = None

    def check_status(self, current_chapter: int) -> PromiseStatus:
        if self.status == PromiseStatus.RESOLVED:
            return PromiseStatus.RESOLVED
        if current_chapter > self.expected_payoff_max:
            return PromiseStatus.OVERDUE
        if current_chapter >= self.expected_payoff_min:
            return PromiseStatus.APPROACHING_PAYOFF
        return self.status


@dataclass
class ForeshadowingItem:
    id: str
    seed_chapter: int
    clues: List[Dict[str, Any]] = field(default_factory=list)
    intended_false_meaning: str = ""
    true_meaning: str = ""
    planned_payoff_chapter: int = 0
    is_revealed: bool = False


@dataclass
class StoryEvent:
    event_id: str
    story_id: str
    chapter_number: int
    scene_number: int
    sequence_num: int
    event_type: str
    entity_type: str
    entity_id: str
    payload: Dict[str, Any]
    author: str = "AI"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> StoryEvent:
        return cls(**d)
