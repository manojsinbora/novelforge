"""
NovelForge AI — Phase 3 Seed Script
Populates canonical power states, systems, mutations, abilities, and equipment
for seed story: 'Echoes of the Fallen Heaven'.
"""
import json
import os
import uuid

from novelforge.database.power_repository import PowerRepository
from novelforge.backend.app.services.power_state_service import PowerStateService
from novelforge.backend.app.services.mutation_service import MutationService
from novelforge.backend.app.services.ability_service import AbilityService
from novelforge.backend.app.services.equipment_service import EquipmentService
from novelforge.schemas.power_models import (
    PowerVector, PowerPotential, EnergyPool, EnergyType, MutationCategory,
    MutationStability, AbilityType, MasteryRank, TechniqueType, EquipmentRarity,
    EquipmentSlot
)

def run_seed():
    db_path = "novelforge/database/novelforge.sqlite3"
    repo = PowerRepository(db_path)
    state_svc = PowerStateService(repo)
    mut_svc = MutationService(repo)
    ability_svc = AbilityService(repo)
    eq_svc = EquipmentService(repo)

    story_id = "echoes-of-fallen-heaven-001"

    print("Seeding Phase 3 Power Systems...")
    system = state_svc.create_default_seven_tier_system(
        story_id=story_id,
        name="Sevenfold Heavenly Dao Cultivation"
    )

    # 1. Lin Chen (char-001) - Regressor Protagonist
    print("Seeding Lin Chen Power State...")
    state_svc.initialize_character_power(
        character_id="char-001",
        story_id=story_id,
        system_id=system.id,
        tier=1,
        stage="Peak",
        base_vector=PowerVector(
            physical=28.0, energy=35.0, speed=30.0, durability=26.0,
            perception=42.0, mental=48.0, technique=55.0, combat_skill=60.0,
            control=32.0, adaptability=35.0, regeneration=20.0, special_ability=45.0
        ),
        ceiling_tier=7,
        chapter_acquired=1
    )

    # Mutations for Lin Chen
    mut_svc.register_mutation(
        character_id="char-001",
        story_id=story_id,
        name="Reincarnator Soul Eye",
        category=MutationCategory.SOUL,
        stability=MutationStability.STABLE,
        tier=2,
        stat_modifiers={"perception": 15.0, "mental": 20.0},
        abilities_granted=["Temporal Echo Feint"],
        drawbacks=["Soul fatigue under prolonged focus"],
        hidden_from_character=False,
        hidden_from_world=True, # Hidden from public world
        chapter_manifested=1
    )
    mut_svc.register_mutation(
        character_id="char-001",
        story_id=story_id,
        name="Jade Meridian Bone",
        category=MutationCategory.SKELETAL,
        stability=MutationStability.STABLE,
        tier=1,
        stat_modifiers={"durability": 12.0, "physical": 8.0},
        hidden_from_character=False,
        hidden_from_world=False,
        chapter_manifested=1
    )

    # Techniques for Lin Chen
    ability_svc.register_technique(
        character_id="char-001",
        story_id=story_id,
        name="Formless Void Breathing",
        technique_type=TechniqueType.BREATH_TECHNIQUE,
        rank="Heaven",
        current_level=3,
        max_level=9,
        stat_modifiers={"energy": 18.0, "control": 12.0},
        description="Ancient breath circulation method retaining insights from Lin Chen's past life.",
        chapter_learned=1
    )

    # Abilities for Lin Chen
    ability_svc.register_ability(
        character_id="char-001",
        story_id=story_id,
        name="Temporal Echo Feint",
        ability_type=AbilityType.SPATIAL,
        mastery=MasteryRank.ADEPT,
        energy_cost=25.0,
        energy_type=EnergyType.QI,
        cooldown_scenes=2,
        description="Leaves a residual spatial silhouette that absorbs one physical blow.",
        chapter_unlocked=1
    )

    # Equipment for Lin Chen
    needle = eq_svc.create_equipment(
        story_id=story_id,
        name="Heaven-Cleaving Needle",
        rarity=EquipmentRarity.LEGENDARY,
        slot=EquipmentSlot.MAIN_HAND,
        owner_id="char-001",
        attributes={"physical": 35.0, "technique": 25.0},
        passive_effects=["Spatial Puncture: Pierces Tier 2 defenses"],
        active_skills=["Dimensional Fracture: Destroys target core on critical hit"],
        spirit_resonance=0.85,
        chapter_created=1
    )
    ring = eq_svc.create_equipment(
        story_id=story_id,
        name="Fallen Heaven Ring",
        rarity=EquipmentRarity.MYTHIC,
        slot=EquipmentSlot.RING,
        owner_id="char-001",
        attributes={"control": 20.0, "special_ability": 30.0},
        passive_effects=["Spatiotemporal concealment of aura"],
        spirit_resonance=1.0,
        chapter_created=1
    )

    # 2. Song Yu (char-004) - Rival
    print("Seeding Song Yu...")
    state_svc.initialize_character_power(
        character_id="char-004",
        story_id=story_id,
        system_id=system.id,
        tier=1,
        stage="Late",
        base_vector=PowerVector(
            physical=32.0, energy=30.0, speed=25.0, durability=28.0,
            perception=22.0, mental=20.0, technique=28.0, combat_skill=30.0,
            control=24.0, adaptability=20.0, regeneration=15.0, special_ability=15.0
        ),
        ceiling_tier=4,
        chapter_acquired=1
    )
    saber = eq_svc.create_equipment(
        story_id=story_id,
        name="Gilded Cloud Saber",
        rarity=EquipmentRarity.UNCOMMON,
        slot=EquipmentSlot.MAIN_HAND,
        owner_id="char-004",
        attributes={"physical": 15.0},
        chapter_created=1
    )

    # 3. Elder Han (char-003) - Disciplinary Elder
    print("Seeding Elder Han...")
    state_svc.initialize_character_power(
        character_id="char-003",
        story_id=story_id,
        system_id=system.id,
        tier=2,
        stage="Late",
        base_vector=PowerVector(
            physical=55.0, energy=70.0, speed=45.0, durability=60.0,
            perception=40.0, mental=35.0, technique=40.0, combat_skill=45.0,
            control=40.0, adaptability=30.0, regeneration=25.0, special_ability=20.0
        ),
        ceiling_tier=5,
        chapter_acquired=1
    )

    # 4. Patriarch Yan (char-007) - Antagonist
    print("Seeding Patriarch Yan...")
    state_svc.initialize_character_power(
        character_id="char-007",
        story_id=story_id,
        system_id=system.id,
        tier=4,
        stage="Early",
        base_vector=PowerVector(
            physical=120.0, energy=180.0, speed=110.0, durability=130.0,
            perception=140.0, mental=110.0, technique=120.0, combat_skill=135.0,
            control=125.0, adaptability=100.0, regeneration=80.0, special_ability=110.0
        ),
        ceiling_tier=6,
        chapter_acquired=1
    )

    # Export seed data to filesystem
    export_dir = "novelforge/stories/echoes_of_the_fallen_heaven/power"
    os.makedirs(export_dir, exist_ok=True)
    with open(os.path.join(export_dir, "power_system.json"), "w", encoding="utf-8") as f:
        json.dump(system.to_dict(), f, indent=2)

    with open(os.path.join(export_dir, "lin_chen_dossier.json"), "w", encoding="utf-8") as f:
        json.dump(state_svc.get_character_power_dossier("char-001"), f, indent=2)

    print("Phase 3 seed data successfully applied and exported!")

if __name__ == "__main__":
    run_seed()
