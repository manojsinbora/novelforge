"""
NovelForge AI — Long-Term Story Architecture Schemas
Phase 4: Plot, Arc Planning, Mysteries, Promises & Foreshadowing Models
Supports Python standard library (dataclasses) and Pydantic v2 serialization.
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

class StoryState(str, Enum):
    IDEA = "IDEA"
    PLANNED = "PLANNED"
    OUTLINED = "OUTLINED"
    ACTIVE = "ACTIVE"
    IN_PROGRESS = "IN_PROGRESS"
    DRAFTED = "DRAFTED"
    REVIEW = "REVIEW"
    CANON = "CANON"
    REVISED = "REVISED"
    DEPRECATED = "DEPRECATED"
    ABANDONED = "ABANDONED"


class PlotThreadType(str, Enum):
    MAIN_PLOT = "MAIN_PLOT"
    SUBPLOT = "SUBPLOT"
    CHARACTER_PLOT = "CHARACTER_PLOT"
    ROMANCE = "ROMANCE"
    REVENGE = "REVENGE"
    MYSTERY = "MYSTERY"
    POLITICAL = "POLITICAL"
    FACTION = "FACTION"
    SURVIVAL = "SURVIVAL"
    CULTIVATION = "CULTIVATION"
    WORLD_BUILDING = "WORLD_BUILDING"
    EXPLORATION = "EXPLORATION"
    RELATIONSHIP = "RELATIONSHIP"
    TECHNOLOGY = "TECHNOLOGY"
    FAMILY = "FAMILY"
    INHERITANCE = "INHERITANCE"
    WAR = "WAR"
    ECONOMIC = "ECONOMIC"
    OTHER = "OTHER"


class ThreadStatus(str, Enum):
    SEED = "SEED"
    OPEN = "OPEN"
    ACTIVE = "ACTIVE"
    DEVELOPING = "DEVELOPING"
    ESCALATING = "ESCALATING"
    DORMANT = "DORMANT"
    READY_FOR_PAYOFF = "READY_FOR_PAYOFF"
    RESOLVED = "RESOLVED"
    FAILED = "FAILED"
    ABANDONED = "ABANDONED"
    RETCONNED = "RETCONNED"


class ArcType(str, Enum):
    POSITIVE_TRANSFORMATION = "POSITIVE_TRANSFORMATION"
    NEGATIVE_TRANSFORMATION = "NEGATIVE_TRANSFORMATION"
    TRAGIC = "TRAGIC"
    REDEMPTION = "REDEMPTION"
    CORRUPTION = "CORRUPTION"
    REVENGE = "REVENGE"
    SURVIVAL = "SURVIVAL"
    MATURITY = "MATURITY"
    LEADERSHIP = "LEADERSHIP"
    SACRIFICE = "SACRIFICE"
    IDENTITY = "IDENTITY"
    RELATIONSHIP = "RELATIONSHIP"
    AMBITION = "AMBITION"
    FALL = "FALL"
    RISE = "RISE"
    STATIC = "STATIC"
    CUSTOM = "CUSTOM"


class GoalType(str, Enum):
    SURVIVAL = "SURVIVAL"
    PERSONAL = "PERSONAL"
    RELATIONSHIP = "RELATIONSHIP"
    POWER = "POWER"
    REVENGE = "REVENGE"
    EXPLORATION = "EXPLORATION"
    POLITICAL = "POLITICAL"
    FACTION = "FACTION"
    MYSTERY = "MYSTERY"
    WORLD = "WORLD"
    ULTIMATE = "ULTIMATE"


class GoalStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    FORMING = "FORMING"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    PROGRESSING = "PROGRESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABANDONED = "ABANDONED"
    TRANSFORMED = "TRANSFORMED"


class ConflictType(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    INTERNAL = "INTERNAL"
    FACTION = "FACTION"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    SYSTEMIC = "SYSTEMIC"
    EXISTENTIAL = "EXISTENTIAL"


class MysteryStatus(str, Enum):
    UNSOLVED = "UNSOLVED"
    INVESTIGATING = "INVESTIGATING"
    THEORIZED = "THEORIZED"
    PARTIALLY_REVEALED = "PARTIALLY_REVEALED"
    SOLVED = "SOLVED"
    RETCONNED = "RETCONNED"
    ABANDONED = "ABANDONED"


class PromiseStatus(str, Enum):
    INTRODUCED = "INTRODUCED"
    OPEN = "OPEN"
    ACTIVE = "ACTIVE"
    DEVELOPING = "DEVELOPING"
    READY_FOR_PAYOFF = "READY_FOR_PAYOFF"
    RESOLVED = "RESOLVED"
    ABANDONED = "ABANDONED"
    OVERDUE = "OVERDUE"


class ForeshadowingType(str, Enum):
    DIALOGUE = "DIALOGUE"
    OBJECT = "OBJECT"
    VISUAL = "VISUAL"
    ENVIRONMENTAL = "ENVIRONMENTAL"
    BEHAVIORAL = "BEHAVIORAL"
    HISTORICAL = "HISTORICAL"
    DREAM = "DREAM"
    PROPHECY = "PROPHECY"
    COINCIDENCE = "COINCIDENCE"
    ABILITY = "ABILITY"
    NAME = "NAME"
    SYMBOLISM = "SYMBOLISM"
    WORLD_EVENT = "WORLD_EVENT"
    BACKGROUND_DETAIL = "BACKGROUND_DETAIL"


class ForeshadowingQuality(str, Enum):
    PERFECTLY_TIMED = "PERFECTLY_TIMED"
    TOO_OBVIOUS = "TOO_OBVIOUS"
    TOO_SUBTLE = "TOO_SUBTLE"
    DISCONNECTED = "DISCONNECTED"
    REPETITIVE = "REPETITIVE"
    CONTRADICTORY = "CONTRADICTORY"
    UNSUPPORTED = "UNSUPPORTED"


class ReversalType(str, Enum):
    VICTORY_TO_DEFEAT = "VICTORY_TO_DEFEAT"
    DEFEAT_TO_VICTORY = "DEFEAT_TO_VICTORY"
    ALLY_TO_ENEMY = "ALLY_TO_ENEMY"
    ENEMY_TO_ALLY = "ENEMY_TO_ALLY"
    SAFE_TO_DANGEROUS = "SAFE_TO_DANGEROUS"
    WEAK_TO_POWERFUL = "WEAK_TO_POWERFUL"
    POWERFUL_TO_POWERLESS = "POWERFUL_TO_POWERLESS"
    TRUSTED_TO_BETRAYAL = "TRUSTED_TO_BETRAYAL"
    TRUTH_TO_LIE = "TRUTH_TO_LIE"


class PlanningHorizon(str, Enum):
    HORIZON_1_CURRENT = "HORIZON_1_CURRENT"    # 1–5 chapters
    HORIZON_2_NEAR = "HORIZON_2_NEAR"          # 5–30 chapters
    HORIZON_3_MEDIUM = "HORIZON_3_MEDIUM"      # 30–150 chapters
    HORIZON_4_LONG = "HORIZON_4_LONG"          # 150–500 chapters
    HORIZON_5_DISTANT = "HORIZON_5_DISTANT"    # 500+ chapters


class DebtSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class HookType(str, Enum):
    MYSTERY = "MYSTERY"
    DANGER = "DANGER"
    REVELATION = "REVELATION"
    EMOTIONAL = "EMOTIONAL"
    POWER = "POWER"
    CONFLICT = "CONFLICT"
    CHARACTER = "CHARACTER"
    DISCOVERY = "DISCOVERY"
    CLIFFHANGER = "CLIFFHANGER"


class PlanConfidence(str, Enum):
    CANON = "CANON"
    HIGH_CONFIDENCE = "HIGH_CONFIDENCE"
    MEDIUM_CONFIDENCE = "MEDIUM_CONFIDENCE"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    IDEA = "IDEA"


# =====================================================================
# MAIN STORYLINE & STRATEGIC MILESTONES
# =====================================================================

@dataclass
class StoryMilestone:
    id: str
    title: str
    description: str
    target_saga: int = 1
    target_arc: int = 1
    approximate_chapter: int = 10
    status: str = "PLANNED"  # PLANNED, IN_PROGRESS, ACHIEVED, CANCELLED
    consequences: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StoryMilestone:
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", ""),
            description=data.get("description", ""),
            target_saga=int(data.get("target_saga", 1)),
            target_arc=int(data.get("target_arc", 1)),
            approximate_chapter=int(data.get("approximate_chapter", 10)),
            status=data.get("status", "PLANNED"),
            consequences=data.get("consequences", []),
        )


@dataclass
class MainPlot:
    id: str
    story_id: str
    premise: str
    central_conflict: str
    protagonist_goal: str
    ultimate_antagonistic_force: str
    central_stakes: str
    thematic_question: str
    desired_ending: str
    turning_points: List[StoryMilestone] = field(default_factory=list)
    current_state: StoryState = StoryState.ACTIVE
    unresolved_threads: List[str] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "premise": self.premise,
            "central_conflict": self.central_conflict,
            "protagonist_goal": self.protagonist_goal,
            "ultimate_antagonistic_force": self.ultimate_antagonistic_force,
            "central_stakes": self.central_stakes,
            "thematic_question": self.thematic_question,
            "desired_ending": self.desired_ending,
            "turning_points": [t.to_dict() if hasattr(t, "to_dict") else t for t in self.turning_points],
            "current_state": self.current_state.value if isinstance(self.current_state, Enum) else self.current_state,
            "unresolved_threads": self.unresolved_threads,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MainPlot:
        tpoints = [StoryMilestone.from_dict(t) if isinstance(t, dict) else t for t in data.get("turning_points", [])]
        st = data.get("current_state", StoryState.ACTIVE)
        if isinstance(st, str):
            try:
                st = StoryState(st)
            except ValueError:
                st = StoryState.ACTIVE
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            premise=data.get("premise", ""),
            central_conflict=data.get("central_conflict", ""),
            protagonist_goal=data.get("protagonist_goal", ""),
            ultimate_antagonistic_force=data.get("ultimate_antagonistic_force", ""),
            central_stakes=data.get("central_stakes", ""),
            thematic_question=data.get("thematic_question", ""),
            desired_ending=data.get("desired_ending", ""),
            turning_points=tpoints,
            current_state=st,
            unresolved_threads=data.get("unresolved_threads", []),
            updated_at=data.get("updated_at", datetime.datetime.utcnow().isoformat()),
        )


# =====================================================================
# PLOT THREADS & SUBPLOTS
# =====================================================================

@dataclass
class PlotThread:
    id: str
    story_id: str
    name: str
    thread_type: PlotThreadType
    description: str
    importance: float = 5.0  # 1.0 to 10.0
    priority: int = 3  # 1 (highest) to 5 (lowest)
    status: ThreadStatus = ThreadStatus.OPEN
    origin: str = "PROLOGUE"
    related_characters: List[str] = field(default_factory=list)
    related_factions: List[str] = field(default_factory=list)
    related_locations: List[str] = field(default_factory=list)
    related_mysteries: List[str] = field(default_factory=list)
    related_promises: List[str] = field(default_factory=list)
    started_chapter: int = 1
    target_resolution_chapter: int = 50
    actual_resolution_chapter: Optional[int] = None
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "name": self.name,
            "thread_type": self.thread_type.value if isinstance(self.thread_type, Enum) else self.thread_type,
            "description": self.description,
            "importance": self.importance,
            "priority": self.priority,
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
            "origin": self.origin,
            "related_characters": self.related_characters,
            "related_factions": self.related_factions,
            "related_locations": self.related_locations,
            "related_mysteries": self.related_mysteries,
            "related_promises": self.related_promises,
            "started_chapter": self.started_chapter,
            "target_resolution_chapter": self.target_resolution_chapter,
            "actual_resolution_chapter": self.actual_resolution_chapter,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlotThread:
        ttype = data.get("thread_type", PlotThreadType.SUBPLOT)
        if isinstance(ttype, str):
            try:
                ttype = PlotThreadType(ttype)
            except ValueError:
                ttype = PlotThreadType.SUBPLOT
        stat = data.get("status", ThreadStatus.OPEN)
        if isinstance(stat, str):
            try:
                stat = ThreadStatus(stat)
            except ValueError:
                stat = ThreadStatus.OPEN
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            name=data.get("name", "Unnamed Thread"),
            thread_type=ttype,
            description=data.get("description", ""),
            importance=float(data.get("importance", 5.0)),
            priority=int(data.get("priority", 3)),
            status=stat,
            origin=data.get("origin", "PROLOGUE"),
            related_characters=data.get("related_characters", []),
            related_factions=data.get("related_factions", []),
            related_locations=data.get("related_locations", []),
            related_mysteries=data.get("related_mysteries", []),
            related_promises=data.get("related_promises", []),
            started_chapter=int(data.get("started_chapter", 1)),
            target_resolution_chapter=int(data.get("target_resolution_chapter", 50)),
            actual_resolution_chapter=data.get("actual_resolution_chapter"),
            notes=data.get("notes", ""),
            created_at=data.get("created_at", datetime.datetime.utcnow().isoformat()),
            updated_at=data.get("updated_at", datetime.datetime.utcnow().isoformat()),
        )


@dataclass
class SubplotPlan:
    id: str
    story_id: str
    name: str
    parent_thread_id: str
    setup: str
    development: str
    escalation: str
    midpoint: str
    crisis: str
    climax: str
    resolution: str
    active_stage: str = "setup"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SubplotPlan:
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            name=data.get("name", ""),
            parent_thread_id=data.get("parent_thread_id", ""),
            setup=data.get("setup", ""),
            development=data.get("development", ""),
            escalation=data.get("escalation", ""),
            midpoint=data.get("midpoint", ""),
            crisis=data.get("crisis", ""),
            climax=data.get("climax", ""),
            resolution=data.get("resolution", ""),
            active_stage=data.get("active_stage", "setup"),
        )


# =====================================================================
# CHARACTER ARCS & GOALS
# =====================================================================

@dataclass
class CharacterArcMilestone:
    id: str
    arc_id: str
    chapter_number: int
    title: str
    description: str
    character_id: str
    emotional_state_before: str
    emotional_state_after: str
    belief_shift: str
    status: str = "PLANNED"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CharacterArcMilestone:
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            arc_id=data.get("arc_id", ""),
            chapter_number=int(data.get("chapter_number", 1)),
            title=data.get("title", ""),
            description=data.get("description", ""),
            character_id=data.get("character_id", ""),
            emotional_state_before=data.get("emotional_state_before", ""),
            emotional_state_after=data.get("emotional_state_after", ""),
            belief_shift=data.get("belief_shift", ""),
            status=data.get("status", "PLANNED"),
        )


@dataclass
class CharacterArc:
    id: str
    character_id: str
    story_id: str
    arc_type: ArcType
    initial_state: str
    internal_problem: str
    want: str
    need: str
    pressure: str
    transformation: str
    final_state: str
    beliefs: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    desires: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    relationships_trajectory: Dict[str, str] = field(default_factory=dict)
    flaws: List[str] = field(default_factory=list)
    current_worldview: str = ""
    milestones: List[CharacterArcMilestone] = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "character_id": self.character_id,
            "story_id": self.story_id,
            "arc_type": self.arc_type.value if isinstance(self.arc_type, Enum) else self.arc_type,
            "initial_state": self.initial_state,
            "internal_problem": self.internal_problem,
            "want": self.want,
            "need": self.need,
            "pressure": self.pressure,
            "transformation": self.transformation,
            "final_state": self.final_state,
            "beliefs": self.beliefs,
            "fears": self.fears,
            "desires": self.desires,
            "values": self.values,
            "relationships_trajectory": self.relationships_trajectory,
            "flaws": self.flaws,
            "current_worldview": self.current_worldview,
            "milestones": [m.to_dict() if hasattr(m, "to_dict") else m for m in self.milestones],
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CharacterArc:
        atype = data.get("arc_type", ArcType.POSITIVE_TRANSFORMATION)
        if isinstance(atype, str):
            try:
                atype = ArcType(atype)
            except ValueError:
                atype = ArcType.POSITIVE_TRANSFORMATION
        ms = [CharacterArcMilestone.from_dict(m) if isinstance(m, dict) else m for m in data.get("milestones", [])]
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            character_id=data.get("character_id", ""),
            story_id=data.get("story_id", ""),
            arc_type=atype,
            initial_state=data.get("initial_state", ""),
            internal_problem=data.get("internal_problem", ""),
            want=data.get("want", ""),
            need=data.get("need", ""),
            pressure=data.get("pressure", ""),
            transformation=data.get("transformation", ""),
            final_state=data.get("final_state", ""),
            beliefs=data.get("beliefs", []),
            fears=data.get("fears", []),
            desires=data.get("desires", []),
            values=data.get("values", []),
            relationships_trajectory=data.get("relationships_trajectory", {}),
            flaws=data.get("flaws", []),
            current_worldview=data.get("current_worldview", ""),
            milestones=ms,
            updated_at=data.get("updated_at", datetime.datetime.utcnow().isoformat()),
        )


@dataclass
class Goal:
    id: str
    character_id: str
    story_id: str
    description: str
    goal_type: GoalType = GoalType.PERSONAL
    priority: int = 3
    motivation: str = ""
    deadline_chapter: Optional[int] = None
    obstacles: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    progress: float = 0.0  # 0.0 to 1.0
    status: GoalStatus = GoalStatus.ACTIVE
    consequences: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "character_id": self.character_id,
            "story_id": self.story_id,
            "description": self.description,
            "goal_type": self.goal_type.value if isinstance(self.goal_type, Enum) else self.goal_type,
            "priority": self.priority,
            "motivation": self.motivation,
            "deadline_chapter": self.deadline_chapter,
            "obstacles": self.obstacles,
            "resources": self.resources,
            "progress": self.progress,
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
            "consequences": self.consequences,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Goal:
        gtype = data.get("goal_type", GoalType.PERSONAL)
        if isinstance(gtype, str):
            try:
                gtype = GoalType(gtype)
            except ValueError:
                gtype = GoalType.PERSONAL
        stat = data.get("status", GoalStatus.ACTIVE)
        if isinstance(stat, str):
            try:
                stat = GoalStatus(stat)
            except ValueError:
                stat = GoalStatus.ACTIVE
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            character_id=data.get("character_id", ""),
            story_id=data.get("story_id", ""),
            description=data.get("description", ""),
            goal_type=gtype,
            priority=int(data.get("priority", 3)),
            motivation=data.get("motivation", ""),
            deadline_chapter=data.get("deadline_chapter"),
            obstacles=data.get("obstacles", []),
            resources=data.get("resources", []),
            progress=float(data.get("progress", 0.0)),
            status=stat,
            consequences=data.get("consequences", []),
        )


# =====================================================================
# CONFLICT & STAKES ENGINE
# =====================================================================

@dataclass
class ConflictParty:
    entity_id: str
    entity_type: str  # "CHARACTER", "FACTION"
    role: str  # "PROTAGONIST", "ANTAGONIST", "THIRD_PARTY"
    stance: str = "Hostile"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Conflict:
    id: str
    story_id: str
    title: str
    conflict_type: ConflictType
    parties: List[ConflictParty] = field(default_factory=list)
    objective: str = ""
    opposing_goals: Dict[str, str] = field(default_factory=dict)
    stakes: Dict[str, str] = field(default_factory=dict)  # personal, immediate, long_term, emotional
    resources: Dict[str, str] = field(default_factory=dict)
    escalation_level: int = 1  # 1 (mild) to 10 (existential extinction)
    consequences: List[str] = field(default_factory=list)
    resolution_conditions: List[str] = field(default_factory=list)
    status: str = "ACTIVE"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "title": self.title,
            "conflict_type": self.conflict_type.value if isinstance(self.conflict_type, Enum) else self.conflict_type,
            "parties": [p.to_dict() if hasattr(p, "to_dict") else p for p in self.parties],
            "objective": self.objective,
            "opposing_goals": self.opposing_goals,
            "stakes": self.stakes,
            "resources": self.resources,
            "escalation_level": self.escalation_level,
            "consequences": self.consequences,
            "resolution_conditions": self.resolution_conditions,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Conflict:
        ctype = data.get("conflict_type", ConflictType.INDIVIDUAL)
        if isinstance(ctype, str):
            try:
                ctype = ConflictType(ctype)
            except ValueError:
                ctype = ConflictType.INDIVIDUAL
        parties = []
        for p in data.get("parties", []):
            if isinstance(p, dict):
                parties.append(ConflictParty(**p))
            else:
                parties.append(p)
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            title=data.get("title", ""),
            conflict_type=ctype,
            parties=parties,
            objective=data.get("objective", ""),
            opposing_goals=data.get("opposing_goals", {}),
            stakes=data.get("stakes", {}),
            resources=data.get("resources", {}),
            escalation_level=int(data.get("escalation_level", 1)),
            consequences=data.get("consequences", []),
            resolution_conditions=data.get("resolution_conditions", []),
            status=data.get("status", "ACTIVE"),
        )


# =====================================================================
# MYSTERIES, CLUES & SECRETS (EPISTEMIC PROTECTION)
# =====================================================================

@dataclass
class MysteryClue:
    id: str
    mystery_id: str
    clue_text: str
    chapter_introduced: int
    location_id: str = ""
    discoverer_id: str = ""
    visibility: str = "PUBLIC"  # PUBLIC, SECRET, HIDDEN
    interpretation: str = ""
    true_meaning: str = ""
    false_interpretations: List[str] = field(default_factory=list)
    importance: str = "MAJOR"  # MINOR, MODERATE, MAJOR, CRUCIAL
    payoff_chapter: Optional[int] = None
    status: str = "DISCOVERED"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MysteryClue:
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            mystery_id=data.get("mystery_id", ""),
            clue_text=data.get("clue_text", ""),
            chapter_introduced=int(data.get("chapter_introduced", 1)),
            location_id=data.get("location_id", ""),
            discoverer_id=data.get("discoverer_id", ""),
            visibility=data.get("visibility", "PUBLIC"),
            interpretation=data.get("interpretation", ""),
            true_meaning=data.get("true_meaning", ""),
            false_interpretations=data.get("false_interpretations", []),
            importance=data.get("importance", "MAJOR"),
            payoff_chapter=data.get("payoff_chapter"),
            status=data.get("status", "DISCOVERED"),
        )


@dataclass
class Mystery:
    id: str
    story_id: str
    title: str
    question: str
    hidden_truth: str  # CANON PROTECTED: Only SYSTEM / AUTHOR access
    visible_clues: List[str] = field(default_factory=list)
    false_leads: List[str] = field(default_factory=list)
    true_leads: List[str] = field(default_factory=list)
    suspects: List[str] = field(default_factory=list)
    theories: List[str] = field(default_factory=list)
    reveal_plan: str = ""
    reveal_conditions: List[str] = field(default_factory=list)
    resolution: str = ""
    status: MysteryStatus = MysteryStatus.UNSOLVED
    importance: str = "CORE"  # CORE, MAJOR, MINOR
    intended_reader_suspicion: str = ""
    epistemic_knowledge: Dict[str, str] = field(default_factory=lambda: {
        "AUTHOR": "KNOWN_TRUE",
        "SYSTEM": "KNOWN_TRUE",
        "READER": "UNKNOWN",
        "PROTAGONIST": "UNKNOWN"
    })
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self, mask_hidden_truth: bool = False) -> Dict[str, Any]:
        d = {
            "id": self.id,
            "story_id": self.story_id,
            "title": self.title,
            "question": self.question,
            "hidden_truth": "[PROTECTED CANONICAL TRUTH]" if mask_hidden_truth else self.hidden_truth,
            "visible_clues": self.visible_clues,
            "false_leads": self.false_leads,
            "true_leads": self.true_leads,
            "suspects": self.suspects,
            "theories": self.theories,
            "reveal_plan": self.reveal_plan,
            "reveal_conditions": self.reveal_conditions,
            "resolution": self.resolution,
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
            "importance": self.importance,
            "intended_reader_suspicion": self.intended_reader_suspicion,
            "epistemic_knowledge": self.epistemic_knowledge,
            "created_at": self.created_at,
        }
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Mystery:
        stat = data.get("status", MysteryStatus.UNSOLVED)
        if isinstance(stat, str):
            try:
                stat = MysteryStatus(stat)
            except ValueError:
                stat = MysteryStatus.UNSOLVED
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            title=data.get("title", ""),
            question=data.get("question", ""),
            hidden_truth=data.get("hidden_truth", ""),
            visible_clues=data.get("visible_clues", []),
            false_leads=data.get("false_leads", []),
            true_leads=data.get("true_leads", []),
            suspects=data.get("suspects", []),
            theories=data.get("theories", []),
            reveal_plan=data.get("reveal_plan", ""),
            reveal_conditions=data.get("reveal_conditions", []),
            resolution=data.get("resolution", ""),
            status=stat,
            importance=data.get("importance", "CORE"),
            intended_reader_suspicion=data.get("intended_reader_suspicion", ""),
            epistemic_knowledge=data.get("epistemic_knowledge", {}),
            created_at=data.get("created_at", datetime.datetime.utcnow().isoformat()),
        )


@dataclass
class Secret:
    id: str
    story_id: str
    secret_text: str
    owner_id: str
    truth: str
    who_knows: List[str] = field(default_factory=list)
    who_suspects: List[str] = field(default_factory=list)
    discovery_conditions: str = ""
    reveal_importance: str = "HIGH"
    reveal_target: str = ""
    is_revealed: bool = False
    reveal_chapter: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Secret:
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            secret_text=data.get("secret_text", ""),
            owner_id=data.get("owner_id", ""),
            truth=data.get("truth", ""),
            who_knows=data.get("who_knows", []),
            who_suspects=data.get("who_suspects", []),
            discovery_conditions=data.get("discovery_conditions", ""),
            reveal_importance=data.get("reveal_importance", "HIGH"),
            reveal_target=data.get("reveal_target", ""),
            is_revealed=bool(data.get("is_revealed", False)),
            reveal_chapter=data.get("reveal_chapter"),
        )


# =====================================================================
# NARRATIVE PROMISES & PROMISE DEBT
# =====================================================================

@dataclass
class StoryPromise:
    id: str
    story_id: str
    description: str
    promise_type: str  # "ARTIFACT", "PROPHECY", "ENEMY", "REUNION", "REVELATION", "TRAITOR", "POWER"
    introduced_chapter: int
    importance: str = "HIGH"  # CRITICAL, HIGH, MEDIUM, LOW
    expected_payoff_window: int = 30  # Number of chapters before debt accumulates
    payoff_requirements: List[str] = field(default_factory=list)
    related_thread_id: Optional[str] = None
    related_mystery_id: Optional[str] = None
    status: PromiseStatus = PromiseStatus.OPEN
    payoff_chapter: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "description": self.description,
            "promise_type": self.promise_type,
            "introduced_chapter": self.introduced_chapter,
            "importance": self.importance,
            "expected_payoff_window": self.expected_payoff_window,
            "payoff_requirements": self.payoff_requirements,
            "related_thread_id": self.related_thread_id,
            "related_mystery_id": self.related_mystery_id,
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
            "payoff_chapter": self.payoff_chapter,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StoryPromise:
        stat = data.get("status", PromiseStatus.OPEN)
        if isinstance(stat, str):
            try:
                stat = PromiseStatus(stat)
            except ValueError:
                stat = PromiseStatus.OPEN
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            description=data.get("description", ""),
            promise_type=data.get("promise_type", "REVELATION"),
            introduced_chapter=int(data.get("introduced_chapter", 1)),
            importance=data.get("importance", "HIGH"),
            expected_payoff_window=int(data.get("expected_payoff_window", 30)),
            payoff_requirements=data.get("payoff_requirements", []),
            related_thread_id=data.get("related_thread_id"),
            related_mystery_id=data.get("related_mystery_id"),
            status=stat,
            payoff_chapter=data.get("payoff_chapter"),
            created_at=data.get("created_at", datetime.datetime.utcnow().isoformat()),
        )


# =====================================================================
# FORESHADOWING, TWISTS & REVERSALS
# =====================================================================

@dataclass
class ForeshadowingSeed:
    id: str
    story_id: str
    seed_text: str
    foreshadowing_type: ForeshadowingType
    target_event: str
    target_reveal: str
    chapter_introduced: int
    clue_strength: float = 0.5  # 0.0 (imperceptible) to 1.0 (blatant)
    visibility: str = "BACKGROUND"  # BACKGROUND, DIALOGUE, PROMINENT
    intended_interpretation: str = ""
    actual_meaning: str = ""
    payoff_window_end: int = 50
    status: str = "PLANTED"  # PLANTED, REINFORCED, PAID_OFF, ABANDONED
    quality: ForeshadowingQuality = ForeshadowingQuality.PERFECTLY_TIMED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "seed_text": self.seed_text,
            "foreshadowing_type": self.foreshadowing_type.value if isinstance(self.foreshadowing_type, Enum) else self.foreshadowing_type,
            "target_event": self.target_event,
            "target_reveal": self.target_reveal,
            "chapter_introduced": self.chapter_introduced,
            "clue_strength": self.clue_strength,
            "visibility": self.visibility,
            "intended_interpretation": self.intended_interpretation,
            "actual_meaning": self.actual_meaning,
            "payoff_window_end": self.payoff_window_end,
            "status": self.status,
            "quality": self.quality.value if isinstance(self.quality, Enum) else self.quality,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ForeshadowingSeed:
        ftype = data.get("foreshadowing_type", ForeshadowingType.DIALOGUE)
        if isinstance(ftype, str):
            try:
                ftype = ForeshadowingType(ftype)
            except ValueError:
                ftype = ForeshadowingType.DIALOGUE
        qual = data.get("quality", ForeshadowingQuality.PERFECTLY_TIMED)
        if isinstance(qual, str):
            try:
                qual = ForeshadowingQuality(qual)
            except ValueError:
                qual = ForeshadowingQuality.PERFECTLY_TIMED
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            seed_text=data.get("seed_text", ""),
            foreshadowing_type=ftype,
            target_event=data.get("target_event", ""),
            target_reveal=data.get("target_reveal", ""),
            chapter_introduced=int(data.get("chapter_introduced", 1)),
            clue_strength=float(data.get("clue_strength", 0.5)),
            visibility=data.get("visibility", "BACKGROUND"),
            intended_interpretation=data.get("intended_interpretation", ""),
            actual_meaning=data.get("actual_meaning", ""),
            payoff_window_end=int(data.get("payoff_window_end", 50)),
            status=data.get("status", "PLANTED"),
            quality=qual,
        )


@dataclass
class PlotTwist:
    id: str
    story_id: str
    title: str
    setup: str
    hidden_truth: str
    reveal_text: str
    expected_reader_belief: str
    actual_truth: str
    affected_characters: List[str] = field(default_factory=list)
    consequences: List[str] = field(default_factory=list)
    foreshadowing_ids: List[str] = field(default_factory=list)
    reveal_chapter: int = 1
    importance: str = "MAJOR"
    surprise_rating: float = 8.5  # 1.0 to 10.0
    fairness_rating: float = 9.0  # Fair-play clues present

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlotTwist:
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            title=data.get("title", ""),
            setup=data.get("setup", ""),
            hidden_truth=data.get("hidden_truth", ""),
            reveal_text=data.get("reveal_text", ""),
            expected_reader_belief=data.get("expected_reader_belief", ""),
            actual_truth=data.get("actual_truth", ""),
            affected_characters=data.get("affected_characters", []),
            consequences=data.get("consequences", []),
            foreshadowing_ids=data.get("foreshadowing_ids", []),
            reveal_chapter=int(data.get("reveal_chapter", 1)),
            importance=data.get("importance", "MAJOR"),
            surprise_rating=float(data.get("surprise_rating", 8.5)),
            fairness_rating=float(data.get("fairness_rating", 9.0)),
        )


@dataclass
class Reversal:
    id: str
    story_id: str
    title: str
    reversal_type: ReversalType
    trigger_chapter: int
    affected_characters: List[str] = field(default_factory=list)
    setup_events: List[str] = field(default_factory=list)
    outcome_description: str = ""
    consequences: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "title": self.title,
            "reversal_type": self.reversal_type.value if isinstance(self.reversal_type, Enum) else self.reversal_type,
            "trigger_chapter": self.trigger_chapter,
            "affected_characters": self.affected_characters,
            "setup_events": self.setup_events,
            "outcome_description": self.outcome_description,
            "consequences": self.consequences,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Reversal:
        rtype = data.get("reversal_type", ReversalType.VICTORY_TO_DEFEAT)
        if isinstance(rtype, str):
            try:
                rtype = ReversalType(rtype)
            except ValueError:
                rtype = ReversalType.VICTORY_TO_DEFEAT
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            title=data.get("title", ""),
            reversal_type=rtype,
            trigger_chapter=int(data.get("trigger_chapter", 1)),
            affected_characters=data.get("affected_characters", []),
            setup_events=data.get("setup_events", []),
            outcome_description=data.get("outcome_description", ""),
            consequences=data.get("consequences", []),
        )


# =====================================================================
# HIERARCHICAL PLANNING: ARC, CHAPTER & SCENE BLUEPRINTS
# =====================================================================

@dataclass
class BeatPlan:
    id: str
    scene_id: str
    sequence_order: int
    beat_type: str  # "ACTION", "DIALOGUE", "REVELATION", "INTERNAL", "DECISION", "CLIFFHANGER"
    action: str
    character_reactions: Dict[str, str] = field(default_factory=dict)
    revelation: Optional[str] = None
    tension_rating: float = 5.0  # 1.0 to 10.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ScenePlan:
    id: str
    chapter_id: str
    sequence_order: int
    title: str
    purpose: str
    location_id: str
    characters_present: List[str] = field(default_factory=list)
    primary_conflict: str = ""
    scene_goal: str = ""
    obstacle: str = ""
    information_revealed: List[str] = field(default_factory=list)
    emotional_change: str = ""
    power_change: str = ""
    relationship_change: str = ""
    world_change: str = ""
    mystery_change: str = ""
    promise_change: str = ""
    entry_state: Dict[str, Any] = field(default_factory=dict)
    exit_state: Dict[str, Any] = field(default_factory=dict)
    beats: List[BeatPlan] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "chapter_id": self.chapter_id,
            "sequence_order": self.sequence_order,
            "title": self.title,
            "purpose": self.purpose,
            "location_id": self.location_id,
            "characters_present": self.characters_present,
            "primary_conflict": self.primary_conflict,
            "scene_goal": self.scene_goal,
            "obstacle": self.obstacle,
            "information_revealed": self.information_revealed,
            "emotional_change": self.emotional_change,
            "power_change": self.power_change,
            "relationship_change": self.relationship_change,
            "world_change": self.world_change,
            "mystery_change": self.mystery_change,
            "promise_change": self.promise_change,
            "entry_state": self.entry_state,
            "exit_state": self.exit_state,
            "beats": [b.to_dict() if hasattr(b, "to_dict") else b for b in self.beats],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ScenePlan:
        beats = []
        for b in data.get("beats", []):
            if isinstance(b, dict):
                beats.append(BeatPlan(**b))
            else:
                beats.append(b)
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            chapter_id=data.get("chapter_id", ""),
            sequence_order=int(data.get("sequence_order", 1)),
            title=data.get("title", ""),
            purpose=data.get("purpose", ""),
            location_id=data.get("location_id", ""),
            characters_present=data.get("characters_present", []),
            primary_conflict=data.get("primary_conflict", ""),
            scene_goal=data.get("scene_goal", ""),
            obstacle=data.get("obstacle", ""),
            information_revealed=data.get("information_revealed", []),
            emotional_change=data.get("emotional_change", ""),
            power_change=data.get("power_change", ""),
            relationship_change=data.get("relationship_change", ""),
            world_change=data.get("world_change", ""),
            mystery_change=data.get("mystery_change", ""),
            promise_change=data.get("promise_change", ""),
            entry_state=data.get("entry_state", {}),
            exit_state=data.get("exit_state", {}),
            beats=beats,
        )


@dataclass
class ChapterPlan:
    id: str
    arc_id: str
    chapter_number: int
    title: str
    chapter_objective: str
    main_conflict: str
    character_objectives: Dict[str, str] = field(default_factory=dict)
    scenes: List[ScenePlan] = field(default_factory=list)
    important_reveals: List[str] = field(default_factory=list)
    power_events: List[str] = field(default_factory=list)
    emotional_beats: List[str] = field(default_factory=list)
    mystery_clues: List[str] = field(default_factory=list)
    foreshadowing_seeds: List[str] = field(default_factory=list)
    promise_advancement: List[str] = field(default_factory=list)
    ending_hook: str = ""
    hook_type: HookType = HookType.CURIOSITY if hasattr(HookType, "CURIOSITY") else HookType.MYSTERY
    pacing_metrics: Dict[str, float] = field(default_factory=dict)
    confidence: PlanConfidence = PlanConfidence.HIGH_CONFIDENCE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "arc_id": self.arc_id,
            "chapter_number": self.chapter_number,
            "title": self.title,
            "chapter_objective": self.chapter_objective,
            "main_conflict": self.main_conflict,
            "character_objectives": self.character_objectives,
            "scenes": [s.to_dict() if hasattr(s, "to_dict") else s for s in self.scenes],
            "important_reveals": self.important_reveals,
            "power_events": self.power_events,
            "emotional_beats": self.emotional_beats,
            "mystery_clues": self.mystery_clues,
            "foreshadowing_seeds": self.foreshadowing_seeds,
            "promise_advancement": self.promise_advancement,
            "ending_hook": self.ending_hook,
            "hook_type": self.hook_type.value if isinstance(self.hook_type, Enum) else self.hook_type,
            "pacing_metrics": self.pacing_metrics,
            "confidence": self.confidence.value if isinstance(self.confidence, Enum) else self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ChapterPlan:
        scenes = [ScenePlan.from_dict(s) if isinstance(s, dict) else s for s in data.get("scenes", [])]
        htype = data.get("hook_type", HookType.MYSTERY)
        if isinstance(htype, str):
            try:
                htype = HookType(htype)
            except ValueError:
                htype = HookType.MYSTERY
        conf = data.get("confidence", PlanConfidence.HIGH_CONFIDENCE)
        if isinstance(conf, str):
            try:
                conf = PlanConfidence(conf)
            except ValueError:
                conf = PlanConfidence.HIGH_CONFIDENCE
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            arc_id=data.get("arc_id", ""),
            chapter_number=int(data.get("chapter_number", 1)),
            title=data.get("title", ""),
            chapter_objective=data.get("chapter_objective", ""),
            main_conflict=data.get("main_conflict", ""),
            character_objectives=data.get("character_objectives", {}),
            scenes=scenes,
            important_reveals=data.get("important_reveals", []),
            power_events=data.get("power_events", []),
            emotional_beats=data.get("emotional_beats", []),
            mystery_clues=data.get("mystery_clues", []),
            foreshadowing_seeds=data.get("foreshadowing_seeds", []),
            promise_advancement=data.get("promise_advancement", []),
            ending_hook=data.get("ending_hook", ""),
            hook_type=htype,
            pacing_metrics=data.get("pacing_metrics", {}),
            confidence=conf,
        )


@dataclass
class ArcPlan:
    id: str
    saga_id: str
    story_id: str
    arc_name: str
    sequence_order: int
    start_chapter: int
    end_chapter: int
    arc_objective: str
    central_conflict: str
    primary_characters: List[str] = field(default_factory=list)
    secondary_characters: List[str] = field(default_factory=list)
    setting: str = ""
    opening_state: str = ""
    escalation_milestones: List[str] = field(default_factory=list)
    midpoint_reversal: str = ""
    major_reversal: str = ""
    climax: str = ""
    resolution: str = ""
    character_changes: Dict[str, str] = field(default_factory=dict)
    power_changes: Dict[str, str] = field(default_factory=dict)
    world_changes: List[str] = field(default_factory=list)
    open_threads: List[str] = field(default_factory=list)
    resolved_threads: List[str] = field(default_factory=list)
    future_hooks: List[str] = field(default_factory=list)
    arc_purpose: List[str] = field(default_factory=list)
    confidence: PlanConfidence = PlanConfidence.HIGH_CONFIDENCE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "saga_id": self.saga_id,
            "story_id": self.story_id,
            "arc_name": self.arc_name,
            "sequence_order": self.sequence_order,
            "start_chapter": self.start_chapter,
            "end_chapter": self.end_chapter,
            "arc_objective": self.arc_objective,
            "central_conflict": self.central_conflict,
            "primary_characters": self.primary_characters,
            "secondary_characters": self.secondary_characters,
            "setting": self.setting,
            "opening_state": self.opening_state,
            "escalation_milestones": self.escalation_milestones,
            "midpoint_reversal": self.midpoint_reversal,
            "major_reversal": self.major_reversal,
            "climax": self.climax,
            "resolution": self.resolution,
            "character_changes": self.character_changes,
            "power_changes": self.power_changes,
            "world_changes": self.world_changes,
            "open_threads": self.open_threads,
            "resolved_threads": self.resolved_threads,
            "future_hooks": self.future_hooks,
            "arc_purpose": self.arc_purpose,
            "confidence": self.confidence.value if isinstance(self.confidence, Enum) else self.confidence,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ArcPlan:
        conf = data.get("confidence", PlanConfidence.HIGH_CONFIDENCE)
        if isinstance(conf, str):
            try:
                conf = PlanConfidence(conf)
            except ValueError:
                conf = PlanConfidence.HIGH_CONFIDENCE
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            saga_id=data.get("saga_id", ""),
            story_id=data.get("story_id", ""),
            arc_name=data.get("arc_name", ""),
            sequence_order=int(data.get("sequence_order", 1)),
            start_chapter=int(data.get("start_chapter", 1)),
            end_chapter=int(data.get("end_chapter", 20)),
            arc_objective=data.get("arc_objective", ""),
            central_conflict=data.get("central_conflict", ""),
            primary_characters=data.get("primary_characters", []),
            secondary_characters=data.get("secondary_characters", []),
            setting=data.get("setting", ""),
            opening_state=data.get("opening_state", ""),
            escalation_milestones=data.get("escalation_milestones", []),
            midpoint_reversal=data.get("midpoint_reversal", ""),
            major_reversal=data.get("major_reversal", ""),
            climax=data.get("climax", ""),
            resolution=data.get("resolution", ""),
            character_changes=data.get("character_changes", {}),
            power_changes=data.get("power_changes", {}),
            world_changes=data.get("world_changes", []),
            open_threads=data.get("open_threads", []),
            resolved_threads=data.get("resolved_threads", []),
            future_hooks=data.get("future_hooks", []),
            arc_purpose=data.get("arc_purpose", []),
            confidence=conf,
        )


# =====================================================================
# STORY DEPENDENCY GRAPH & CONSEQUENCES
# =====================================================================

@dataclass
class NarrativeDependency:
    id: str
    story_id: str
    source_type: str  # "MYSTERY", "CLUE", "CHARACTER", "FACTION", "ARC", "EVENT", "PROMISE"
    source_id: str
    target_type: str
    target_id: str
    dependency_type: str  # "REQUIRES", "REVEALS", "RESOLVES", "ESCALATES", "BLOCKS"
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> NarrativeDependency:
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            source_type=data.get("source_type", ""),
            source_id=data.get("source_id", ""),
            target_type=data.get("target_type", ""),
            target_id=data.get("target_id", ""),
            dependency_type=data.get("dependency_type", "REQUIRES"),
            description=data.get("description", ""),
        )


@dataclass
class Consequence:
    id: str
    event_id: str
    chapter_number: int
    immediate_consequences: List[str] = field(default_factory=list)
    character_consequences: Dict[str, List[str]] = field(default_factory=dict)
    faction_consequences: Dict[str, List[str]] = field(default_factory=dict)
    world_consequences: List[str] = field(default_factory=list)
    future_plot_consequences: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =====================================================================
# NARRATIVE DEBT & STORY HEALTH
# =====================================================================

@dataclass
class NarrativeDebt:
    id: str
    story_id: str
    debt_type: str  # "OVERDUE_PROMISE", "ABANDONED_SUBPLOT", "UNEXPLAINED_ABILITY", "ABSENT_CHARACTER", "UNRESOLVED_MYSTERY"
    severity: DebtSeverity
    title: str
    description: str
    introduced_chapter: int
    age_chapters: int
    importance: str = "HIGH"
    affected_entities: List[str] = field(default_factory=list)
    suggested_remedy: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "debt_type": self.debt_type,
            "severity": self.severity.value if isinstance(self.severity, Enum) else self.severity,
            "title": self.title,
            "description": self.description,
            "introduced_chapter": self.introduced_chapter,
            "age_chapters": self.age_chapters,
            "importance": self.importance,
            "affected_entities": self.affected_entities,
            "suggested_remedy": self.suggested_remedy,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> NarrativeDebt:
        sev = data.get("severity", DebtSeverity.MEDIUM)
        if isinstance(sev, str):
            try:
                sev = DebtSeverity(sev)
            except ValueError:
                sev = DebtSeverity.MEDIUM
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            debt_type=data.get("debt_type", "OVERDUE_PROMISE"),
            severity=sev,
            title=data.get("title", ""),
            description=data.get("description", ""),
            introduced_chapter=int(data.get("introduced_chapter", 1)),
            age_chapters=int(data.get("age_chapters", 0)),
            importance=data.get("importance", "HIGH"),
            affected_entities=data.get("affected_entities", []),
            suggested_remedy=data.get("suggested_remedy", ""),
        )


@dataclass
class StoryHealthReport:
    story_id: str
    overall_health_score: float  # 0.0 to 100.0
    total_open_threads: int
    total_open_promises: int
    overdue_promises_count: int
    unresolved_mysteries_count: int
    active_character_arcs_count: int
    high_risk_debt_count: int
    debts: List[NarrativeDebt] = field(default_factory=list)
    pacing_balance: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "story_id": self.story_id,
            "overall_health_score": round(self.overall_health_score, 1),
            "total_open_threads": self.total_open_threads,
            "total_open_promises": self.total_open_promises,
            "overdue_promises_count": self.overdue_promises_count,
            "unresolved_mysteries_count": self.unresolved_mysteries_count,
            "active_character_arcs_count": self.active_character_arcs_count,
            "high_risk_debt_count": self.high_risk_debt_count,
            "debts": [d.to_dict() if hasattr(d, "to_dict") else d for d in self.debts],
            "pacing_balance": self.pacing_balance,
            "recommendations": self.recommendations,
        }


# =====================================================================
# CHANGE IMPACT ANALYSIS
# =====================================================================

@dataclass
class ChangeImpactReport:
    modified_entity_type: str
    modified_entity_id: str
    modified_chapter: int
    affected_arcs: List[str] = field(default_factory=list)
    affected_chapters: List[int] = field(default_factory=list)
    affected_mysteries: List[str] = field(default_factory=list)
    affected_promises: List[str] = field(default_factory=list)
    affected_foreshadowing: List[str] = field(default_factory=list)
    affected_characters: List[str] = field(default_factory=list)
    downstream_rewrite_risk: str = "LOW"  # LOW, MEDIUM, HIGH, CATASTROPHIC
    total_affected_elements: int = 0
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
