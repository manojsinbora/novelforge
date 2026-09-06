"""
NovelForge AI — Power, Mutation, Cultivation, Progression & Equipment Schemas
Phase 3: The Physics Engine of the Novel Universe
Supports Python standard library (dataclasses) and Pydantic v2 serialization.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Union
from enum import Enum
import uuid
import datetime
import json
import math


# =====================================================================
# ENUMS & CONSTANTS
# =====================================================================

class PowerSystemType(str, Enum):
    CULTIVATION = "CULTIVATION"
    MUTATION = "MUTATION"
    AWAKENING = "AWAKENING"
    MARTIAL_ARTS = "MARTIAL_ARTS"
    MAGIC = "MAGIC"
    TECH = "TECH"
    SOUL = "SOUL"
    HYBRID = "HYBRID"


class PowerStage(str, Enum):
    EARLY = "Early"
    MID = "Mid"
    LATE = "Late"
    PEAK = "Peak"


class EnergyType(str, Enum):
    QI = "QI"
    MANA = "MANA"
    AETHER = "AETHER"
    BLOOD_ENERGY = "BLOOD_ENERGY"
    PSIONIC = "PSIONIC"
    VOID_ESSENCE = "VOID_ESSENCE"
    SOLAR = "SOLAR"
    ELEMENTAL = "ELEMENTAL"
    DIVINE = "DIVINE"
    CORRUPTED = "CORRUPTED"


class MutationCategory(str, Enum):
    BIOLOGICAL = "BIOLOGICAL"
    ENERGETIC = "ENERGETIC"
    SKELETAL = "SKELETAL"
    SENSORY = "SENSORY"
    ORGAN = "ORGAN"
    BLOODLINE = "BLOODLINE"
    SOUL = "SOUL"
    SYMBIOTIC = "SYMBIOTIC"
    SPATIAL = "SPATIAL"
    VOID_ELDRITCH = "VOID_ELDRITCH"


class MutationStability(str, Enum):
    DORMANT = "DORMANT"
    STABLE = "STABLE"
    VOLATILE = "VOLATILE"
    EVOLVING = "EVOLVING"
    CORRUPTED = "CORRUPTED"
    MUTATING = "MUTATING"


class AbilityType(str, Enum):
    OFFENSIVE = "OFFENSIVE"
    DEFENSIVE = "DEFENSIVE"
    MOVEMENT = "MOVEMENT"
    SENSORY = "SENSORY"
    HEALING = "HEALING"
    BUFF = "BUFF"
    DEBUFF = "DEBUFF"
    UTILITY = "UTILITY"
    DOMAIN = "DOMAIN"
    SUMMONING = "SUMMONING"
    SEALING = "SEALING"
    ILLUSION = "ILLUSION"
    SOUL = "SOUL"
    SPATIAL = "SPATIAL"
    TEMPORAL = "TEMPORAL"
    CURSING = "CURSING"
    PASSIVE = "PASSIVE"


class MasteryRank(str, Enum):
    INITIATE = "INITIATE"
    PRACTITIONER = "PRACTITIONER"
    ADEPT = "ADEPT"
    MASTER = "MASTER"
    GRANDMASTER = "GRANDMASTER"


class TechniqueType(str, Enum):
    MARTIAL_ART = "MARTIAL_ART"
    CULTIVATION_METHOD = "CULTIVATION_METHOD"
    SPELL_FORM = "SPELL_FORM"
    ARRAY_FORMATION = "ARRAY_FORMATION"
    BREATH_TECHNIQUE = "BREATH_TECHNIQUE"
    SOUL_MANUAL = "SOUL_MANUAL"


class EquipmentRarity(str, Enum):
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"
    EPIC = "EPIC"
    LEGENDARY = "LEGENDARY"
    MYTHIC = "MYTHIC"
    TRANSCENDENT = "TRANSCENDENT"


class EquipmentSlot(str, Enum):
    MAIN_HAND = "MAIN_HAND"
    OFF_HAND = "OFF_HAND"
    ARMOR = "ARMOR"
    HEAD = "HEAD"
    BOOTS = "BOOTS"
    RING = "RING"
    AMULET = "AMULET"
    TALISMAN = "TALISMAN"
    ARTIFACT = "ARTIFACT"
    STORAGE = "STORAGE"


class StatusEffectType(str, Enum):
    BLEED = "BLEED"
    POISON = "POISON"
    QI_DEVIATION = "QI_DEVIATION"
    BURN = "BURN"
    FROZEN = "FROZEN"
    STUN = "STUN"
    BLIND = "BLIND"
    CURSE = "CURSE"
    EXHAUSTION = "EXHAUSTION"
    ENRAGED = "ENRAGED"
    SUPPRESSED = "SUPPRESSED"
    EMPOWERED = "EMPOWERED"
    SHIELDED = "SHIELDED"
    STEALTH = "STEALTH"


class ProgressionTrigger(str, Enum):
    RESOURCE_ABSORPTION = "RESOURCE_ABSORPTION"
    COMBAT_EPIPHANY = "COMBAT_EPIPHANY"
    LIFE_DEATH_CRISIS = "LIFE_DEATH_CRISIS"
    MEDITATION = "MEDITATION"
    PILL_CONSUMPTION = "PILL_CONSUMPTION"
    BLOODLINE_AWAKENING = "BLOODLINE_AWAKENING"
    EXTERNAL_CATALYST = "EXTERNAL_CATALYST"
    SECT_RITUAL = "SECT_RITUAL"
    TRIBULATION = "TRIBULATION"


class ViolationSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"


# =====================================================================
# 12-DIMENSIONAL COMBAT & POWER VECTOR
# =====================================================================

@dataclass
class PowerVector:
    physical: float = 10.0
    energy: float = 10.0
    speed: float = 10.0
    durability: float = 10.0
    perception: float = 10.0
    mental: float = 10.0
    technique: float = 10.0
    combat_skill: float = 10.0
    control: float = 10.0
    adaptability: float = 10.0
    regeneration: float = 10.0
    special_ability: float = 10.0

    def total(self) -> float:
        return (
            self.physical + self.energy + self.speed + self.durability +
            self.perception + self.mental + self.technique + self.combat_skill +
            self.control + self.adaptability + self.regeneration + self.special_ability
        )

    def average(self) -> float:
        return self.total() / 12.0

    def scale(self, factor: float) -> PowerVector:
        return PowerVector(
            physical=round(self.physical * factor, 2),
            energy=round(self.energy * factor, 2),
            speed=round(self.speed * factor, 2),
            durability=round(self.durability * factor, 2),
            perception=round(self.perception * factor, 2),
            mental=round(self.mental * factor, 2),
            technique=round(self.technique * factor, 2),
            combat_skill=round(self.combat_skill * factor, 2),
            control=round(self.control * factor, 2),
            adaptability=round(self.adaptability * factor, 2),
            regeneration=round(self.regeneration * factor, 2),
            special_ability=round(self.special_ability * factor, 2),
        )

    def apply_modifiers(self, modifiers: Dict[str, float]) -> PowerVector:
        return PowerVector(
            physical=max(0.0, self.physical + modifiers.get("physical", 0.0)),
            energy=max(0.0, self.energy + modifiers.get("energy", 0.0)),
            speed=max(0.0, self.speed + modifiers.get("speed", 0.0)),
            durability=max(0.0, self.durability + modifiers.get("durability", 0.0)),
            perception=max(0.0, self.perception + modifiers.get("perception", 0.0)),
            mental=max(0.0, self.mental + modifiers.get("mental", 0.0)),
            technique=max(0.0, self.technique + modifiers.get("technique", 0.0)),
            combat_skill=max(0.0, self.combat_skill + modifiers.get("combat_skill", 0.0)),
            control=max(0.0, self.control + modifiers.get("control", 0.0)),
            adaptability=max(0.0, self.adaptability + modifiers.get("adaptability", 0.0)),
            regeneration=max(0.0, self.regeneration + modifiers.get("regeneration", 0.0)),
            special_ability=max(0.0, self.special_ability + modifiers.get("special_ability", 0.0)),
        )

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PowerVector:
        if not data:
            return cls()
        return cls(
            physical=float(data.get("physical", 10.0)),
            energy=float(data.get("energy", 10.0)),
            speed=float(data.get("speed", 10.0)),
            durability=float(data.get("durability", 10.0)),
            perception=float(data.get("perception", 10.0)),
            mental=float(data.get("mental", 10.0)),
            technique=float(data.get("technique", 10.0)),
            combat_skill=float(data.get("combat_skill", 10.0)),
            control=float(data.get("control", 10.0)),
            adaptability=float(data.get("adaptability", 10.0)),
            regeneration=float(data.get("regeneration", 10.0)),
            special_ability=float(data.get("special_ability", 10.0)),
        )


@dataclass
class PowerPotential:
    ceiling_tier: int = 7
    latent_attributes: Dict[str, float] = field(default_factory=dict)
    bottleneck_difficulty: float = 1.0  # 1.0 is standard; higher means harder breakthroughs
    growth_rate: float = 1.0  # multiplier for cultivation speed

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PowerPotential:
        if not data:
            return cls()
        return cls(
            ceiling_tier=int(data.get("ceiling_tier", 7)),
            latent_attributes=data.get("latent_attributes", {}),
            bottleneck_difficulty=float(data.get("bottleneck_difficulty", 1.0)),
            growth_rate=float(data.get("growth_rate", 1.0)),
        )


@dataclass
class EnergyPool:
    energy_type: EnergyType = EnergyType.QI
    current: float = 100.0
    maximum: float = 100.0
    purity: float = 0.5  # 0.0 to 1.0 (higher purity improves efficiency)
    density: float = 1.0  # compression multiplier
    regeneration_rate: float = 5.0  # points per scene/minute

    def to_dict(self) -> Dict[str, Any]:
        return {
            "energy_type": self.energy_type.value if isinstance(self.energy_type, Enum) else self.energy_type,
            "current": self.current,
            "maximum": self.maximum,
            "purity": self.purity,
            "density": self.density,
            "regeneration_rate": self.regeneration_rate,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EnergyPool:
        if not data:
            return cls()
        e_type = data.get("energy_type", EnergyType.QI)
        if isinstance(e_type, str):
            try:
                e_type = EnergyType(e_type)
            except ValueError:
                e_type = EnergyType.QI
        return cls(
            energy_type=e_type,
            current=float(data.get("current", 100.0)),
            maximum=float(data.get("maximum", 100.0)),
            purity=float(data.get("purity", 0.5)),
            density=float(data.get("density", 1.0)),
            regeneration_rate=float(data.get("regeneration_rate", 5.0)),
        )


# =====================================================================
# POWER SYSTEM DEFINITION & TIERS
# =====================================================================

@dataclass
class PowerStageDefinition:
    name: str  # "Early", "Mid", "Late", "Peak"
    order: int
    stat_multiplier: float
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PowerTierDefinition:
    rank: int  # 1 to 7 (or more)
    name: str  # Novice, Intermediate, Master, Grand Master, Great Grand Master, Sovereign, Transcendent
    description: str = ""
    base_multiplier: float = 1.0
    stages: List[PowerStageDefinition] = field(default_factory=list)
    breakthrough_requirements: Dict[str, Any] = field(default_factory=dict)
    bottleneck_description: str = ""
    failure_penalty: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rank": self.rank,
            "name": self.name,
            "description": self.description,
            "base_multiplier": self.base_multiplier,
            "stages": [s.to_dict() if hasattr(s, "to_dict") else s for s in self.stages],
            "breakthrough_requirements": self.breakthrough_requirements,
            "bottleneck_description": self.bottleneck_description,
            "failure_penalty": self.failure_penalty,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PowerTierDefinition:
        stages = []
        for s in data.get("stages", []):
            if isinstance(s, dict):
                stages.append(PowerStageDefinition(**s))
            else:
                stages.append(s)
        return cls(
            rank=int(data.get("rank", 1)),
            name=data.get("name", "Novice"),
            description=data.get("description", ""),
            base_multiplier=float(data.get("base_multiplier", 1.0)),
            stages=stages,
            breakthrough_requirements=data.get("breakthrough_requirements", {}),
            bottleneck_description=data.get("bottleneck_description", ""),
            failure_penalty=data.get("failure_penalty", {}),
        )


@dataclass
class PowerSystem:
    id: str
    story_id: str
    name: str
    system_type: PowerSystemType
    description: str = ""
    energy_type: EnergyType = EnergyType.QI
    tiers: List[PowerTierDefinition] = field(default_factory=list)
    rules: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "name": self.name,
            "system_type": self.system_type.value if isinstance(self.system_type, Enum) else self.system_type,
            "description": self.description,
            "energy_type": self.energy_type.value if isinstance(self.energy_type, Enum) else self.energy_type,
            "tiers": [t.to_dict() if hasattr(t, "to_dict") else t for t in self.tiers],
            "rules": self.rules,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PowerSystem:
        stype = data.get("system_type", PowerSystemType.CULTIVATION)
        if isinstance(stype, str):
            try:
                stype = PowerSystemType(stype)
            except ValueError:
                stype = PowerSystemType.CULTIVATION
        etype = data.get("energy_type", EnergyType.QI)
        if isinstance(etype, str):
            try:
                etype = EnergyType(etype)
            except ValueError:
                etype = EnergyType.QI
        tiers = [PowerTierDefinition.from_dict(t) if isinstance(t, dict) else t for t in data.get("tiers", [])]
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            name=data.get("name", "Standard Awakening"),
            system_type=stype,
            description=data.get("description", ""),
            energy_type=etype,
            tiers=tiers,
            rules=data.get("rules", {}),
            created_at=data.get("created_at", datetime.datetime.utcnow().isoformat()),
        )


# =====================================================================
# CHARACTER POWER STATE & PROGRESSION
# =====================================================================

@dataclass
class CharacterPowerState:
    id: str
    character_id: str
    story_id: str
    system_id: str
    current_tier: int  # 1 to 7
    current_stage: str  # "Early", "Mid", "Late", "Peak"
    tier_name: str = "Novice"
    power_vector: PowerVector = field(default_factory=PowerVector)
    potential: PowerPotential = field(default_factory=PowerPotential)
    energy_pools: List[EnergyPool] = field(default_factory=list)
    active_buffs: List[Dict[str, Any]] = field(default_factory=list)
    conditions: List[Dict[str, Any]] = field(default_factory=list)  # injuries, meridians, curses
    raw_combat_rating: float = 120.0
    chapter_acquired: int = 1
    is_active: bool = True
    updated_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def calculate_combat_rating(self) -> float:
        stage_mult = {"Early": 1.0, "Mid": 1.25, "Late": 1.55, "Peak": 1.9}.get(self.current_stage, 1.0)
        tier_mult = 2.0 ** (self.current_tier - 1)
        base = self.power_vector.total()
        self.raw_combat_rating = round(base * tier_mult * stage_mult, 1)
        return self.raw_combat_rating

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "character_id": self.character_id,
            "story_id": self.story_id,
            "system_id": self.system_id,
            "current_tier": self.current_tier,
            "current_stage": self.current_stage,
            "tier_name": self.tier_name,
            "power_vector": self.power_vector.to_dict() if hasattr(self.power_vector, "to_dict") else self.power_vector,
            "potential": self.potential.to_dict() if hasattr(self.potential, "to_dict") else self.potential,
            "energy_pools": [e.to_dict() if hasattr(e, "to_dict") else e for e in self.energy_pools],
            "active_buffs": self.active_buffs,
            "conditions": self.conditions,
            "raw_combat_rating": self.raw_combat_rating,
            "chapter_acquired": self.chapter_acquired,
            "is_active": self.is_active,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CharacterPowerState:
        p_vec = PowerVector.from_dict(data.get("power_vector", {}))
        pot = PowerPotential.from_dict(data.get("potential", {}))
        pools = [EnergyPool.from_dict(p) if isinstance(p, dict) else p for p in data.get("energy_pools", [])]
        inst = cls(
            id=data.get("id", str(uuid.uuid4())),
            character_id=data.get("character_id", ""),
            story_id=data.get("story_id", ""),
            system_id=data.get("system_id", ""),
            current_tier=int(data.get("current_tier", 1)),
            current_stage=data.get("current_stage", "Early"),
            tier_name=data.get("tier_name", "Novice"),
            power_vector=p_vec,
            potential=pot,
            energy_pools=pools,
            active_buffs=data.get("active_buffs", []),
            conditions=data.get("conditions", []),
            raw_combat_rating=float(data.get("raw_combat_rating", 120.0)),
            chapter_acquired=int(data.get("chapter_acquired", 1)),
            is_active=bool(data.get("is_active", True)),
            updated_at=data.get("updated_at", datetime.datetime.utcnow().isoformat()),
        )
        return inst


@dataclass
class ProgressionEvent:
    id: str
    character_id: str
    story_id: str
    system_id: str
    from_tier: int
    from_stage: str
    to_tier: int
    to_stage: str
    chapter_number: int
    trigger_type: ProgressionTrigger
    catalyst_description: str
    cost_paid: Dict[str, Any] = field(default_factory=dict)
    bottleneck_broken: bool = True
    success: bool = True
    failure_reason: Optional[str] = None
    stat_growth: Dict[str, float] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "character_id": self.character_id,
            "story_id": self.story_id,
            "system_id": self.system_id,
            "from_tier": self.from_tier,
            "from_stage": self.from_stage,
            "to_tier": self.to_tier,
            "to_stage": self.to_stage,
            "chapter_number": self.chapter_number,
            "trigger_type": self.trigger_type.value if isinstance(self.trigger_type, Enum) else self.trigger_type,
            "catalyst_description": self.catalyst_description,
            "cost_paid": self.cost_paid,
            "bottleneck_broken": self.bottleneck_broken,
            "success": self.success,
            "failure_reason": self.failure_reason,
            "stat_growth": self.stat_growth,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ProgressionEvent:
        trig = data.get("trigger_type", ProgressionTrigger.MEDITATION)
        if isinstance(trig, str):
            try:
                trig = ProgressionTrigger(trig)
            except ValueError:
                trig = ProgressionTrigger.MEDITATION
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            character_id=data.get("character_id", ""),
            story_id=data.get("story_id", ""),
            system_id=data.get("system_id", ""),
            from_tier=int(data.get("from_tier", 1)),
            from_stage=data.get("from_stage", "Early"),
            to_tier=int(data.get("to_tier", 1)),
            to_stage=data.get("to_stage", "Mid"),
            chapter_number=int(data.get("chapter_number", 1)),
            trigger_type=trig,
            catalyst_description=data.get("catalyst_description", ""),
            cost_paid=data.get("cost_paid", {}),
            bottleneck_broken=bool(data.get("bottleneck_broken", True)),
            success=bool(data.get("success", True)),
            failure_reason=data.get("failure_reason"),
            stat_growth=data.get("stat_growth", {}),
            created_at=data.get("created_at", datetime.datetime.utcnow().isoformat()),
        )


# =====================================================================
# MUTATION ENGINE
# =====================================================================

@dataclass
class Mutation:
    id: str
    character_id: str
    story_id: str
    name: str
    category: MutationCategory
    stability: MutationStability
    tier: int = 1
    stat_modifiers: Dict[str, float] = field(default_factory=dict)
    abilities_granted: List[str] = field(default_factory=list)
    drawbacks: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    hidden_from_character: bool = False
    hidden_from_world: bool = False
    chapter_manifested: int = 1
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "character_id": self.character_id,
            "story_id": self.story_id,
            "name": self.name,
            "category": self.category.value if isinstance(self.category, Enum) else self.category,
            "stability": self.stability.value if isinstance(self.stability, Enum) else self.stability,
            "tier": self.tier,
            "stat_modifiers": self.stat_modifiers,
            "abilities_granted": self.abilities_granted,
            "drawbacks": self.drawbacks,
            "triggers": self.triggers,
            "hidden_from_character": self.hidden_from_character,
            "hidden_from_world": self.hidden_from_world,
            "chapter_manifested": self.chapter_manifested,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Mutation:
        cat = data.get("category", MutationCategory.BIOLOGICAL)
        if isinstance(cat, str):
            try:
                cat = MutationCategory(cat)
            except ValueError:
                cat = MutationCategory.BIOLOGICAL
        stab = data.get("stability", MutationStability.STABLE)
        if isinstance(stab, str):
            try:
                stab = MutationStability(stab)
            except ValueError:
                stab = MutationStability.STABLE
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            character_id=data.get("character_id", ""),
            story_id=data.get("story_id", ""),
            name=data.get("name", "Latent Mutation"),
            category=cat,
            stability=stab,
            tier=int(data.get("tier", 1)),
            stat_modifiers=data.get("stat_modifiers", {}),
            abilities_granted=data.get("abilities_granted", []),
            drawbacks=data.get("drawbacks", []),
            triggers=data.get("triggers", []),
            hidden_from_character=bool(data.get("hidden_from_character", False)),
            hidden_from_world=bool(data.get("hidden_from_world", False)),
            chapter_manifested=int(data.get("chapter_manifested", 1)),
            created_at=data.get("created_at", datetime.datetime.utcnow().isoformat()),
        )


# =====================================================================
# ABILITY & TECHNIQUE SYSTEM
# =====================================================================

@dataclass
class Ability:
    id: str
    character_id: str
    story_id: str
    name: str
    ability_type: AbilityType
    mastery: MasteryRank = MasteryRank.INITIATE
    energy_cost: float = 20.0
    energy_type: EnergyType = EnergyType.QI
    cooldown_scenes: int = 0  # 0 means usable each scene / turn
    cast_time_seconds: float = 1.0
    range_meters: float = 5.0
    aoe_radius_meters: float = 0.0
    damage_type: str = "Kinetic"
    description: str = ""
    requirements: Dict[str, Any] = field(default_factory=dict)
    synergies: List[str] = field(default_factory=list)
    counter_types: List[str] = field(default_factory=list)
    chapter_unlocked: int = 1
    last_used_chapter: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def get_mastery_multiplier(self) -> float:
        multipliers = {
            MasteryRank.INITIATE: 1.0,
            MasteryRank.PRACTITIONER: 1.3,
            MasteryRank.ADEPT: 1.7,
            MasteryRank.MASTER: 2.2,
            MasteryRank.GRANDMASTER: 3.0,
        }
        return multipliers.get(self.mastery, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "character_id": self.character_id,
            "story_id": self.story_id,
            "name": self.name,
            "ability_type": self.ability_type.value if isinstance(self.ability_type, Enum) else self.ability_type,
            "mastery": self.mastery.value if isinstance(self.mastery, Enum) else self.mastery,
            "energy_cost": self.energy_cost,
            "energy_type": self.energy_type.value if isinstance(self.energy_type, Enum) else self.energy_type,
            "cooldown_scenes": self.cooldown_scenes,
            "cast_time_seconds": self.cast_time_seconds,
            "range_meters": self.range_meters,
            "aoe_radius_meters": self.aoe_radius_meters,
            "damage_type": self.damage_type,
            "description": self.description,
            "requirements": self.requirements,
            "synergies": self.synergies,
            "counter_types": self.counter_types,
            "chapter_unlocked": self.chapter_unlocked,
            "last_used_chapter": self.last_used_chapter,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Ability:
        atype = data.get("ability_type", AbilityType.OFFENSIVE)
        if isinstance(atype, str):
            try:
                atype = AbilityType(atype)
            except ValueError:
                atype = AbilityType.OFFENSIVE
        mrank = data.get("mastery", MasteryRank.INITIATE)
        if isinstance(mrank, str):
            try:
                mrank = MasteryRank(mrank)
            except ValueError:
                mrank = MasteryRank.INITIATE
        etype = data.get("energy_type", EnergyType.QI)
        if isinstance(etype, str):
            try:
                etype = EnergyType(etype)
            except ValueError:
                etype = EnergyType.QI
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            character_id=data.get("character_id", ""),
            story_id=data.get("story_id", ""),
            name=data.get("name", "Strike"),
            ability_type=atype,
            mastery=mrank,
            energy_cost=float(data.get("energy_cost", 20.0)),
            energy_type=etype,
            cooldown_scenes=int(data.get("cooldown_scenes", 0)),
            cast_time_seconds=float(data.get("cast_time_seconds", 1.0)),
            range_meters=float(data.get("range_meters", 5.0)),
            aoe_radius_meters=float(data.get("aoe_radius_meters", 0.0)),
            damage_type=data.get("damage_type", "Kinetic"),
            description=data.get("description", ""),
            requirements=data.get("requirements", {}),
            synergies=data.get("synergies", []),
            counter_types=data.get("counter_types", []),
            chapter_unlocked=int(data.get("chapter_unlocked", 1)),
            last_used_chapter=data.get("last_used_chapter"),
            created_at=data.get("created_at", datetime.datetime.utcnow().isoformat()),
        )


@dataclass
class Technique:
    id: str
    character_id: str
    story_id: str
    name: str
    technique_type: TechniqueType
    rank: str = "Common"  # Common, Earth, Heaven, Divine
    current_level: int = 1
    max_level: int = 9
    requirements: Dict[str, Any] = field(default_factory=dict)
    evolution_path: List[str] = field(default_factory=list)
    stat_modifiers: Dict[str, float] = field(default_factory=dict)
    description: str = ""
    chapter_learned: int = 1
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "character_id": self.character_id,
            "story_id": self.story_id,
            "name": self.name,
            "technique_type": self.technique_type.value if isinstance(self.technique_type, Enum) else self.technique_type,
            "rank": self.rank,
            "current_level": self.current_level,
            "max_level": self.max_level,
            "requirements": self.requirements,
            "evolution_path": self.evolution_path,
            "stat_modifiers": self.stat_modifiers,
            "description": self.description,
            "chapter_learned": self.chapter_learned,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Technique:
        ttype = data.get("technique_type", TechniqueType.MARTIAL_ART)
        if isinstance(ttype, str):
            try:
                ttype = TechniqueType(ttype)
            except ValueError:
                ttype = TechniqueType.MARTIAL_ART
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            character_id=data.get("character_id", ""),
            story_id=data.get("story_id", ""),
            name=data.get("name", "Formless Palm"),
            technique_type=ttype,
            rank=data.get("rank", "Common"),
            current_level=int(data.get("current_level", 1)),
            max_level=int(data.get("max_level", 9)),
            requirements=data.get("requirements", {}),
            evolution_path=data.get("evolution_path", []),
            stat_modifiers=data.get("stat_modifiers", {}),
            description=data.get("description", ""),
            chapter_learned=int(data.get("chapter_learned", 1)),
            created_at=data.get("created_at", datetime.datetime.utcnow().isoformat()),
        )


# =====================================================================
# EQUIPMENT & ARTIFACT ENGINE
# =====================================================================

@dataclass
class Equipment:
    id: str
    story_id: str
    name: str
    rarity: EquipmentRarity
    slot: EquipmentSlot
    current_owner_id: Optional[str] = None
    current_durability: float = 100.0
    max_durability: float = 100.0
    is_bound: bool = False
    attributes: Dict[str, float] = field(default_factory=dict)
    passive_effects: List[str] = field(default_factory=list)
    active_skills: List[str] = field(default_factory=list)
    spirit_resonance: float = 0.0  # 0.0 to 1.0
    evolution_tier: int = 1
    is_destroyed: bool = False
    chapter_created: int = 1
    destruction_chapter: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "story_id": self.story_id,
            "name": self.name,
            "rarity": self.rarity.value if isinstance(self.rarity, Enum) else self.rarity,
            "slot": self.slot.value if isinstance(self.slot, Enum) else self.slot,
            "current_owner_id": self.current_owner_id,
            "current_durability": self.current_durability,
            "max_durability": self.max_durability,
            "is_bound": self.is_bound,
            "attributes": self.attributes,
            "passive_effects": self.passive_effects,
            "active_skills": self.active_skills,
            "spirit_resonance": self.spirit_resonance,
            "evolution_tier": self.evolution_tier,
            "is_destroyed": self.is_destroyed,
            "chapter_created": self.chapter_created,
            "destruction_chapter": self.destruction_chapter,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Equipment:
        rarity = data.get("rarity", EquipmentRarity.COMMON)
        if isinstance(rarity, str):
            try:
                rarity = EquipmentRarity(rarity)
            except ValueError:
                rarity = EquipmentRarity.COMMON
        slot = data.get("slot", EquipmentSlot.MAIN_HAND)
        if isinstance(slot, str):
            try:
                slot = EquipmentSlot(slot)
            except ValueError:
                slot = EquipmentSlot.MAIN_HAND
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            story_id=data.get("story_id", ""),
            name=data.get("name", "Iron Blade"),
            rarity=rarity,
            slot=slot,
            current_owner_id=data.get("current_owner_id"),
            current_durability=float(data.get("current_durability", 100.0)),
            max_durability=float(data.get("max_durability", 100.0)),
            is_bound=bool(data.get("is_bound", False)),
            attributes=data.get("attributes", {}),
            passive_effects=data.get("passive_effects", []),
            active_skills=data.get("active_skills", []),
            spirit_resonance=float(data.get("spirit_resonance", 0.0)),
            evolution_tier=int(data.get("evolution_tier", 1)),
            is_destroyed=bool(data.get("is_destroyed", False)),
            chapter_created=int(data.get("chapter_created", 1)),
            destruction_chapter=data.get("destruction_chapter"),
            created_at=data.get("created_at", datetime.datetime.utcnow().isoformat()),
        )


@dataclass
class EquipmentOwnershipRecord:
    id: str
    equipment_id: str
    previous_owner_id: Optional[str]
    new_owner_id: Optional[str]
    chapter_transferred: int
    transfer_reason: str  # "LOOTED", "GIFTED", "PURCHASED", "FORGED", "STOLEN", "INHERITED", "DESTROYED"
    timestamp: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# =====================================================================
# STATUS EFFECTS
# =====================================================================

@dataclass
class StatusEffect:
    id: str
    character_id: str
    effect_type: StatusEffectType
    severity: float = 1.0  # 1.0 to 5.0
    duration_scenes: int = 1
    stat_penalties: Dict[str, float] = field(default_factory=dict)
    description: str = ""
    chapter_applied: int = 1
    created_at: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "character_id": self.character_id,
            "effect_type": self.effect_type.value if isinstance(self.effect_type, Enum) else self.effect_type,
            "severity": self.severity,
            "duration_scenes": self.duration_scenes,
            "stat_penalties": self.stat_penalties,
            "description": self.description,
            "chapter_applied": self.chapter_applied,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> StatusEffect:
        etype = data.get("effect_type", StatusEffectType.BLEED)
        if isinstance(etype, str):
            try:
                etype = StatusEffectType(etype)
            except ValueError:
                etype = StatusEffectType.BLEED
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            character_id=data.get("character_id", ""),
            effect_type=etype,
            severity=float(data.get("severity", 1.0)),
            duration_scenes=int(data.get("duration_scenes", 1)),
            stat_penalties=data.get("stat_penalties", {}),
            description=data.get("description", ""),
            chapter_applied=int(data.get("chapter_applied", 1)),
            created_at=data.get("created_at", datetime.datetime.utcnow().isoformat()),
        )


# =====================================================================
# COMBAT ASSESSMENT MODELS
# =====================================================================

@dataclass
class CombatFactor:
    name: str
    category: str  # "TIER", "ATTRIBUTES", "EQUIPMENT", "TECHNIQUE", "ENVIRONMENT", "CONDITION", "ELEMENT"
    advantage_to: str  # character_id or "NONE"
    weight: float = 1.0
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReversalCondition:
    condition_name: str
    required_trigger: str
    likelihood: float  # 0.0 to 1.0
    outcome_shift: str  # e.g., "Shifts win probability to Character B by +35%"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CombatAssessmentResult:
    combatant_a_id: str
    combatant_b_id: str
    combatant_a_name: str
    combatant_b_name: str
    win_probability_a: float
    win_probability_b: float
    draw_probability: float
    confidence_level: float
    decisive_factors: List[CombatFactor] = field(default_factory=list)
    reversal_conditions: List[ReversalCondition] = field(default_factory=list)
    expected_injuries_a: str = "None"
    expected_injuries_b: str = "None"
    power_gap_description: str = "Balanced encounter"
    detailed_breakdown: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "combatant_a_id": self.combatant_a_id,
            "combatant_b_id": self.combatant_b_id,
            "combatant_a_name": self.combatant_a_name,
            "combatant_b_name": self.combatant_b_name,
            "win_probability_a": round(self.win_probability_a, 3),
            "win_probability_b": round(self.win_probability_b, 3),
            "draw_probability": round(self.draw_probability, 3),
            "confidence_level": round(self.confidence_level, 2),
            "decisive_factors": [f.to_dict() if hasattr(f, "to_dict") else f for f in self.decisive_factors],
            "reversal_conditions": [r.to_dict() if hasattr(r, "to_dict") else r for r in self.reversal_conditions],
            "expected_injuries_a": self.expected_injuries_a,
            "expected_injuries_b": self.expected_injuries_b,
            "power_gap_description": self.power_gap_description,
            "detailed_breakdown": self.detailed_breakdown,
        }


# =====================================================================
# POWER CONTINUITY & QA VALIDATION MODELS
# =====================================================================

@dataclass
class PowerContinuityViolation:
    rule_violated: str
    severity: ViolationSeverity
    description: str
    offending_chapter: int
    character_id: Optional[str] = None
    suggested_fix: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_violated": self.rule_violated,
            "severity": self.severity.value if isinstance(self.severity, Enum) else self.severity,
            "description": self.description,
            "offending_chapter": self.offending_chapter,
            "character_id": self.character_id,
            "suggested_fix": self.suggested_fix,
        }


@dataclass
class PowerValidationResult:
    is_valid: bool
    power_qa_score: float  # 0.0 to 100.0
    violations: List[PowerContinuityViolation] = field(default_factory=list)
    audited_chapter: int = 1
    total_rules_checked: int = 0
    summary: str = "All power continuity invariants satisfied."

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "power_qa_score": round(self.power_qa_score, 1),
            "violations": [v.to_dict() if hasattr(v, "to_dict") else v for v in self.violations],
            "audited_chapter": self.audited_chapter,
            "total_rules_checked": self.total_rules_checked,
            "summary": self.summary,
        }
