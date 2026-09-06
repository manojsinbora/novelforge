"""
NovelForge AI — Comprehensive Phase 3 Power Engine Test Suite
Tests Power System, 12D Vectors, Breakthroughs, Mutations, Cooldowns, Equipment Provenance,
Combat Assessment, and Power QA Validation Guard.
Runs on Python standard library with zero external dependencies.
"""
import unittest
import uuid
import datetime

from novelforge.database.power_repository import PowerRepository
from novelforge.schemas.power_models import (
    PowerSystem, PowerSystemType, PowerVector, PowerPotential, EnergyPool, EnergyType,
    CharacterPowerState, ProgressionEvent, ProgressionTrigger, Mutation, MutationCategory,
    MutationStability, Ability, AbilityType, MasteryRank, Technique, TechniqueType,
    Equipment, EquipmentRarity, EquipmentSlot, StatusEffect, StatusEffectType,
    ViolationSeverity
)
from novelforge.backend.app.services.power_state_service import PowerStateService
from novelforge.backend.app.services.progression_service import ProgressionService
from novelforge.backend.app.services.mutation_service import MutationService
from novelforge.backend.app.services.ability_service import AbilityService
from novelforge.backend.app.services.equipment_service import EquipmentService
from novelforge.backend.app.services.combat_assessment_service import CombatAssessmentService
from novelforge.backend.app.services.power_validation_service import PowerValidationService
from novelforge.backend.app.services.scene_power_context_service import ScenePowerContextService


class TestPhase3PowerEngine(unittest.TestCase):

    def setUp(self):
        # In-memory database for isolated, lightning-fast execution
        self.repo = PowerRepository(":memory:")
        self.state_svc = PowerStateService(self.repo)
        self.prog_svc = ProgressionService(self.repo)
        self.mut_svc = MutationService(self.repo)
        self.ability_svc = AbilityService(self.repo)
        self.eq_svc = EquipmentService(self.repo)
        self.combat_svc = CombatAssessmentService(self.repo)
        self.val_svc = PowerValidationService(self.repo)
        self.scene_ctx_svc = ScenePowerContextService(self.repo, self.state_svc, self.mut_svc)

        self.story_id = "story-echoes-test"
        self.system = self.state_svc.create_default_seven_tier_system(self.story_id)

    # =========================================================================
    # 1. POWER SYSTEM & TIER LADDER
    # =========================================================================

    def test_default_seven_tier_system_initialization(self):
        """Verifies 7 tiers with 4 sub-stages each, base multipliers, and bottleneck rules."""
        self.assertEqual(len(self.system.tiers), 7)
        tier_names = [t.name for t in self.system.tiers]
        expected_names = [
            "Novice", "Intermediate", "Master", "Grand Master",
            "Great Grand Master", "Sovereign", "Transcendent"
        ]
        self.assertEqual(tier_names, expected_names)

        # Check sub-realms in Novice
        novice = self.system.tiers[0]
        self.assertEqual(len(novice.stages), 4)
        self.assertEqual([s.name for s in novice.stages], ["Early", "Mid", "Late", "Peak"])

        # Check non-linear base multiplier growth
        self.assertLess(self.system.tiers[0].base_multiplier, self.system.tiers[1].base_multiplier)
        self.assertLess(self.system.tiers[3].base_multiplier, self.system.tiers[6].base_multiplier)

    # =========================================================================
    # 2. 12D POWER VECTOR & EFFECTIVE COMBAT RATING
    # =========================================================================

    def test_12d_power_vector_and_modifiers(self):
        """Verifies 12-dimensional vector math and modifier aggregation."""
        vec = PowerVector(
            physical=20.0, energy=25.0, speed=18.0, durability=22.0,
            perception=30.0, mental=28.0, technique=35.0, combat_skill=40.0,
            control=26.0, adaptability=24.0, regeneration=15.0, special_ability=50.0
        )
        self.assertEqual(vec.total(), 333.0)
        self.assertAlmostEqual(vec.average(), 27.75, places=2)

        # Apply equipment modifier
        mod_vec = vec.apply_modifiers({"physical": 10.0, "speed": 5.0})
        self.assertEqual(mod_vec.physical, 30.0)
        self.assertEqual(mod_vec.speed, 23.0)

    # =========================================================================
    # 3. BREAKTHROUGH VALIDATION (LEGAL VS IMPOSSIBLE JUMPS)
    # =========================================================================

    def test_legal_breakthrough_sequence(self):
        """Verifies that step-by-step breakthrough succeeds and records progression events."""
        char_id = "char-lin-chen"
        state = self.state_svc.initialize_character_power(
            character_id=char_id,
            story_id=self.story_id,
            system_id=self.system.id,
            tier=1,
            stage="Early",
            chapter_acquired=1
        )
        self.assertEqual(state.current_tier, 1)
        self.assertEqual(state.current_stage, "Early")

        # Step 1: Early -> Mid at Chapter 3
        evt1 = self.prog_svc.execute_breakthrough(
            character_id=char_id,
            target_tier=1,
            target_stage="Mid",
            chapter_number=3,
            catalyst_description="Circulated Qi for 36 cycles"
        )
        self.assertTrue(evt1.success)
        self.assertTrue(evt1.bottleneck_broken)

        # Step 2: Mid -> Late -> Peak at Chapter 6
        evt2 = self.prog_svc.execute_breakthrough(
            character_id=char_id,
            target_tier=1,
            target_stage="Peak",
            chapter_number=6,
            catalyst_description="Consumed Spirit Spring Dew",
            stat_growth={"physical": 8.0, "energy": 12.0}
        )
        self.assertTrue(evt2.success)

        # Step 3: Peak Tier 1 -> Early Tier 2 at Chapter 10
        evt3 = self.prog_svc.execute_breakthrough(
            character_id=char_id,
            target_tier=2,
            target_stage="Early",
            chapter_number=10,
            catalyst_description="Foundation Condensation Pill"
        )
        self.assertTrue(evt3.success)

        # Check updated state
        updated = self.repo.get_character_power_state(char_id)
        self.assertEqual(updated.current_tier, 2)
        self.assertEqual(updated.current_stage, "Early")
        self.assertEqual(updated.tier_name, "Intermediate")

        # Check progression history log
        history = self.repo.get_progression_history(char_id)
        self.assertEqual(len(history), 3)

    def test_impossible_breakthrough_rejected(self):
        """MANDATORY REQUIREMENT: Arbitrary jumps without prerequisite stages or catalysts are rejected."""
        char_id = "char-rival"
        self.state_svc.initialize_character_power(
            character_id=char_id,
            story_id=self.story_id,
            system_id=self.system.id,
            tier=1,
            stage="Early",
            chapter_acquired=1
        )

        # Attempt illegal jump: Novice Early -> Master Peak (Tier 1 to Tier 3)
        with self.assertRaises(ValueError) as ctx:
            self.prog_svc.execute_breakthrough(
                character_id=char_id,
                target_tier=3,
                target_stage="Peak",
                chapter_number=5,
                catalyst_description=""
            )
        self.assertIn("Impossible tier jump", str(ctx.exception))

    def test_potential_ceiling_enforcement(self):
        """Verifies character cannot break through beyond potential ceiling."""
        char_id = "char-limited"
        state = self.state_svc.initialize_character_power(
            character_id=char_id,
            story_id=self.story_id,
            system_id=self.system.id,
            tier=2,
            stage="Peak",
            ceiling_tier=2, # Ceiling is capped at Tier 2
            chapter_acquired=1
        )
        with self.assertRaises(ValueError) as ctx:
            self.prog_svc.execute_breakthrough(
                character_id=char_id,
                target_tier=3,
                target_stage="Early",
                chapter_number=8,
                catalyst_description="Standard Pill"
            )
        self.assertIn("exceeds character potential ceiling", str(ctx.exception))

    # =========================================================================
    # 4. HISTORICAL ISOLATION (CHAPTER 5 != CHAPTER 50)
    # =========================================================================

    def test_historical_power_state_reconstruction(self):
        """MANDATORY REQUIREMENT: Querying power state at Chapter N reconstructs exact state at that chapter."""
        char_id = "char-time-travel"
        # Chapter 1: Novice Early
        self.state_svc.initialize_character_power(
            character_id=char_id,
            story_id=self.story_id,
            system_id=self.system.id,
            tier=1,
            stage="Early",
            chapter_acquired=1
        )
        # Chapter 15: Novice Peak
        self.prog_svc.execute_breakthrough(
            character_id=char_id,
            target_tier=1,
            target_stage="Peak",
            chapter_number=15,
            catalyst_description="Epiphany"
        )
        # Chapter 40: Intermediate Early
        self.prog_svc.execute_breakthrough(
            character_id=char_id,
            target_tier=2,
            target_stage="Early",
            chapter_number=40,
            catalyst_description="Core Condensation Pill"
        )

        # Historical query at Chapter 5 -> Must be Tier 1 Early!
        state_ch5 = self.repo.get_character_power_state(char_id, at_chapter=5)
        self.assertIsNotNone(state_ch5)
        self.assertEqual(state_ch5.current_tier, 1)
        self.assertEqual(state_ch5.current_stage, "Early")

        # Historical query at Chapter 25 -> Must be Tier 1 Peak!
        state_ch25 = self.repo.get_character_power_state(char_id, at_chapter=25)
        self.assertIsNotNone(state_ch25)
        self.assertEqual(state_ch25.current_tier, 1)
        self.assertEqual(state_ch25.current_stage, "Peak")

        # Current query at Chapter 50 -> Must be Tier 2 Early!
        state_ch50 = self.repo.get_character_power_state(char_id, at_chapter=50)
        self.assertIsNotNone(state_ch50)
        self.assertEqual(state_ch50.current_tier, 2)
        self.assertEqual(state_ch50.current_stage, "Early")

    # =========================================================================
    # 5. MUTATION ENGINE & EPISTEMIC VISIBILITY
    # =========================================================================

    def test_hidden_mutation_visibility(self):
        """Verifies hidden mutations respect epistemic boundaries between character and world."""
        char_id = "char-mc"
        # Public mutation: Jade Skin
        self.mut_svc.register_mutation(
            character_id=char_id,
            story_id=self.story_id,
            name="Jade Meridian Skin",
            category=MutationCategory.BIOLOGICAL,
            stability=MutationStability.STABLE,
            hidden_from_character=False,
            hidden_from_world=False,
            chapter_manifested=1
        )
        # Private mutation: Regression Soul Imprint (character knows, world does not)
        self.mut_svc.register_mutation(
            character_id=char_id,
            story_id=self.story_id,
            name="Reincarnator Soul Eye",
            category=MutationCategory.SOUL,
            stability=MutationStability.STABLE,
            hidden_from_character=False,
            hidden_from_world=True,
            chapter_manifested=1
        )
        # Latent parasite: Eldritch Heart Seed (neither character nor world knows yet)
        self.mut_svc.register_mutation(
            character_id=char_id,
            story_id=self.story_id,
            name="Void Parasite Seed",
            category=MutationCategory.VOID_ELDRITCH,
            stability=MutationStability.DORMANT,
            hidden_from_character=True,
            hidden_from_world=True,
            chapter_manifested=1
        )

        # Check view from Character POV
        char_view = self.mut_svc.get_visible_mutations(char_id, viewer_is_character=True, viewer_is_world=False)
        char_names = [m.name for m in char_view]
        self.assertIn("Jade Meridian Skin", char_names)
        self.assertIn("Reincarnator Soul Eye", char_names)
        self.assertNotIn("Void Parasite Seed", char_names) # Character does not know about the dormant seed!

        # Check view from Public World POV
        world_view = self.mut_svc.get_visible_mutations(char_id, viewer_is_character=False, viewer_is_world=True)
        world_names = [m.name for m in world_view]
        self.assertIn("Jade Meridian Skin", world_names)
        self.assertNotIn("Reincarnator Soul Eye", world_names) # Secret from the world!
        self.assertNotIn("Void Parasite Seed", world_names)

    # =========================================================================
    # 6. ABILITY SYSTEM & COOLDOWNS
    # =========================================================================

    def test_ability_cooldown_and_mastery(self):
        """Verifies cooldown enforcement and mastery rank scaling."""
        char_id = "char-swordsman"
        self.state_svc.initialize_character_power(
            character_id=char_id,
            story_id=self.story_id,
            system_id=self.system.id,
            tier=1,
            stage="Early"
        )
        ab = self.ability_svc.register_ability(
            character_id=char_id,
            story_id=self.story_id,
            name="Flash Strike",
            ability_type=AbilityType.OFFENSIVE,
            mastery=MasteryRank.INITIATE,
            energy_cost=10.0,
            cooldown_scenes=3, # Requires cooldown
            chapter_unlocked=2
        )

        # Before unlock chapter (Chapter 1) -> cannot use
        usable, reason = self.ability_svc.check_ability_usable(char_id, ab.id, current_chapter=1)
        self.assertFalse(usable)
        self.assertIn("not been unlocked", reason)

        # At unlock chapter (Chapter 2) -> can use
        usable, _ = self.ability_svc.check_ability_usable(char_id, ab.id, current_chapter=2)
        self.assertTrue(usable)

        # Record usage in Chapter 2
        self.ability_svc.record_ability_usage(ab.id, chapter_number=2)

        # Try to use again in Chapter 2 -> should trigger cooldown check
        usable_again, reason_again = self.ability_svc.check_ability_usable(char_id, ab.id, current_chapter=2)
        self.assertFalse(usable_again)
        self.assertIn("on cooldown", reason_again)

        # Advance mastery rank to GRANDMASTER
        updated_ab = self.ability_svc.advance_mastery(ab.id, MasteryRank.GRANDMASTER)
        self.assertEqual(updated_ab.mastery, MasteryRank.GRANDMASTER)
        self.assertEqual(updated_ab.get_mastery_multiplier(), 3.0)

    # =========================================================================
    # 7. EQUIPMENT ENGINE & PROVENANCE HISTORY
    # =========================================================================

    def test_equipment_ownership_transfer_and_destruction(self):
        """Verifies provenance logging, ownership transfers, and post-destruction wield prohibitions."""
        char_a = "char-elder"
        char_b = "char-lin-chen"

        blade = self.eq_svc.create_equipment(
            story_id=self.story_id,
            name="Thunder Core Sabre",
            rarity=EquipmentRarity.EPIC,
            slot=EquipmentSlot.MAIN_HAND,
            owner_id=char_a,
            attributes={"physical": 45.0, "speed": 20.0},
            chapter_created=1
        )
        self.assertEqual(blade.current_owner_id, char_a)

        # Transfer blade to Lin Chen in Chapter 12
        self.eq_svc.transfer_ownership(
            equipment_id=blade.id,
            new_owner_id=char_b,
            chapter_number=12,
            reason="BEQUEST_AFTER_TRIAL"
        )
        history = self.repo.get_equipment_history(blade.id)
        self.assertEqual(len(history), 2)
        self.assertEqual(history[-1].new_owner_id, char_b)
        self.assertEqual(history[-1].chapter_transferred, 12)

        # Destroy blade in Chapter 25 during climatic clash
        destroyed = self.eq_svc.destroy_equipment(blade.id, chapter_number=25)
        self.assertTrue(destroyed.is_destroyed)
        self.assertEqual(destroyed.destruction_chapter, 25)

        # Validate that Lin Chen attempting to wield destroyed blade in Chapter 30 fails QA
        qa = self.val_svc.validate_scene_power_continuity(
            character_id=char_b,
            current_chapter=30,
            wielded_equipment_ids=[blade.id]
        )
        self.assertFalse(qa.is_valid)
        violation_rules = [v.rule_violated for v in qa.violations]
        self.assertIn("DESTROYED_EQUIPMENT_WIELDED", violation_rules)

    # =========================================================================
    # 8. MULTI-DIMENSIONAL COMBAT ASSESSMENT
    # =========================================================================

    def test_combat_assessment_tier_suppression_and_reversals(self):
        """Verifies multi-dimensional combat evaluator correctly models realm gaps and reversals."""
        mc = "char-mc-fighter"
        boss = "char-boss"

        # MC: Tier 1 Peak (Rating ~228)
        self.state_svc.initialize_character_power(
            character_id=mc,
            story_id=self.story_id,
            system_id=self.system.id,
            tier=1,
            stage="Peak",
            base_vector=PowerVector(technique=50.0, combat_skill=55.0), # High Battle IQ
            chapter_acquired=1
        )
        # Register a secret hidden mutation for MC
        self.mut_svc.register_mutation(
            character_id=mc,
            story_id=self.story_id,
            name="Ashen Dragon Bloodline",
            category=MutationCategory.BLOODLINE,
            stability=MutationStability.VOLATILE,
            hidden_from_world=True,
            stat_modifiers={"physical": 40.0, "energy": 30.0}
        )

        # Boss: Tier 3 Early (Master Realm)
        self.state_svc.initialize_character_power(
            character_id=boss,
            story_id=self.story_id,
            system_id=self.system.id,
            tier=3,
            stage="Early",
            base_vector=PowerVector(physical=30.0, energy=40.0),
            chapter_acquired=1
        )

        # Run combat simulation
        result = self.combat_svc.evaluate_matchup(
            combatant_a_id=mc,
            combatant_b_id=boss,
            combatant_a_name="Lin Chen",
            combatant_b_name="Sect Master Xiao",
            chapter_number=10
        )

        # Boss has a 2-tier gap: Boss should have decisive advantage
        self.assertGreater(result.win_probability_b, 0.70)
        self.assertLess(result.win_probability_a, 0.30)

        # Decisive factors must include Overwhelming Realm Suppression
        factor_names = [f.name for f in result.decisive_factors]
        self.assertIn("Overwhelming Realm Suppression", factor_names)

        # Reversal conditions must identify MC's hidden bloodline
        reversal_names = [r.condition_name for r in result.reversal_conditions]
        self.assertTrue(any("Ashen Dragon Bloodline" in name for name in reversal_names))

    # =========================================================================
    # 9. POWER QA CONTINUITY GUARD
    # =========================================================================

    def test_power_qa_catches_flashback_leak_and_false_realm(self):
        """Verifies QA validator catches historical leaks and impossible tier claims."""
        char_id = "char-qa-tester"
        self.state_svc.initialize_character_power(
            character_id=char_id,
            story_id=self.story_id,
            system_id=self.system.id,
            tier=1,
            stage="Early",
            chapter_acquired=1
        )
        # Register ability unlocked at Chapter 45
        self.ability_svc.register_ability(
            character_id=char_id,
            story_id=self.story_id,
            name="Void Sovereign Slash",
            ability_type=AbilityType.OFFENSIVE,
            chapter_unlocked=45
        )

        # Validate a flashback scene set in Chapter 5 where author accidentally wrote Void Sovereign Slash
        # and claimed character was Tier 3 Master
        res = self.val_svc.validate_scene_power_continuity(
            character_id=char_id,
            current_chapter=5,
            attempted_abilities=["Void Sovereign Slash"],
            claimed_tier=3
        )
        self.assertFalse(res.is_valid)
        self.assertLess(res.power_qa_score, 70.0)

        rules = [v.rule_violated for v in res.violations]
        self.assertIn("HISTORICAL_FLASHBACK_LEAK", rules)
        self.assertIn("IMPOSSIBLE_TIER_CLAIM", rules)

    # =========================================================================
    # 10. SCENE POWER CONTEXT INJECTION
    # =========================================================================

    def test_scene_power_context_generation(self):
        """Verifies generation of compact, prompt-ready markdown power context."""
        char_a = "char-alice"
        char_b = "char-bob"
        self.state_svc.initialize_character_power(char_a, self.story_id, self.system.id, tier=1, stage="Peak")
        self.state_svc.initialize_character_power(char_b, self.story_id, self.system.id, tier=2, stage="Early")

        ctx = self.scene_ctx_svc.get_scene_power_context(
            character_ids=[char_a, char_b],
            chapter_number=15,
            pov_character_id=char_a
        )
        self.assertIn("prompt_text", ctx)
        prompt = ctx["prompt_text"]
        self.assertIn("AUTHORITATIVE CANONICAL POWER CONTEXT", prompt)
        self.assertIn("char-alice (POV Character)", prompt)
        self.assertIn("Novice (Tier 1, Peak Stage)", prompt)
        self.assertIn("Intermediate (Tier 2, Early Stage)", prompt)


if __name__ == "__main__":
    unittest.main()
