"""
NovelForge AI — Multi-Dimensional Combat Assessment Engine
Phase 3: The Physics Engine of Combat & Progression
Computes probabilistic match outcomes, decisive factors, and reversal conditions.
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any
import math

from novelforge.database.power_repository import PowerRepository
from novelforge.schemas.power_models import (
    CombatAssessmentResult, CombatFactor, ReversalCondition, PowerVector
)


class CombatAssessmentService:
    def __init__(self, power_repo: PowerRepository):
        self.power_repo = power_repo

    def evaluate_matchup(
        self,
        combatant_a_id: str,
        combatant_b_id: str,
        combatant_a_name: str = "Combatant A",
        combatant_b_name: str = "Combatant B",
        chapter_number: Optional[int] = None,
        environment: Optional[Dict[str, Any]] = None,
    ) -> CombatAssessmentResult:
        env = environment or {}
        state_a = self.power_repo.get_character_power_state(combatant_a_id, at_chapter=chapter_number)
        state_b = self.power_repo.get_character_power_state(combatant_b_id, at_chapter=chapter_number)

        if not state_a or not state_b:
            # Fallback if one or both are uninitialized
            return CombatAssessmentResult(
                combatant_a_id=combatant_a_id,
                combatant_b_id=combatant_b_id,
                combatant_a_name=combatant_a_name,
                combatant_b_name=combatant_b_name,
                win_probability_a=0.5,
                win_probability_b=0.5,
                draw_probability=0.0,
                confidence_level=0.1,
                power_gap_description="Incomplete combat data for one or both combatants.",
            )

        # 1. Base rating & Tier Gap
        rating_a = state_a.calculate_combat_rating()
        rating_b = state_b.calculate_combat_rating()
        tier_gap = state_a.current_tier - state_b.current_tier

        decisive_factors: List[CombatFactor] = []
        reversal_conditions: List[ReversalCondition] = []

        score_a = rating_a
        score_b = rating_b

        if abs(tier_gap) >= 2:
            adv = combatant_a_id if tier_gap > 0 else combatant_b_id
            higher_name = combatant_a_name if tier_gap > 0 else combatant_b_name
            decisive_factors.append(CombatFactor(
                name="Overwhelming Realm Suppression",
                category="TIER",
                advantage_to=adv,
                weight=3.5,
                description=f"{higher_name} possesses a {abs(tier_gap)}-tier realm advantage, exerting crushing dimensional aura."
            ))
            # Heavy exponential scaling for 2+ tier gaps
            if tier_gap > 0:
                score_a *= (2.0 ** tier_gap)
            else:
                score_b *= (2.0 ** abs(tier_gap))
        elif abs(tier_gap) == 1:
            adv = combatant_a_id if tier_gap > 0 else combatant_b_id
            higher_name = combatant_a_name if tier_gap > 0 else combatant_b_name
            decisive_factors.append(CombatFactor(
                name="Realm Elevation Advantage",
                category="TIER",
                advantage_to=adv,
                weight=1.5,
                description=f"{higher_name} is one realm higher, yielding superior energy density and reserve capacity."
            ))

        # 2. 12D Vector Sub-Attribute Comparisons
        vec_a = state_a.power_vector
        vec_b = state_b.power_vector

        # Speed comparison
        if vec_a.speed > vec_b.speed * 1.25:
            decisive_factors.append(CombatFactor(
                name="Superior Velocity & Reflexes",
                category="ATTRIBUTES",
                advantage_to=combatant_a_id,
                weight=1.2,
                description=f"{combatant_a_name} moves fast enough to exploit tactical blind spots."
            ))
            score_a *= 1.15
        elif vec_b.speed > vec_a.speed * 1.25:
            decisive_factors.append(CombatFactor(
                name="Superior Velocity & Reflexes",
                category="ATTRIBUTES",
                advantage_to=combatant_b_id,
                weight=1.2,
                description=f"{combatant_b_name} moves fast enough to exploit tactical blind spots."
            ))
            score_b *= 1.15

        # Technique / Combat Skill vs Raw Force
        if vec_a.technique + vec_a.combat_skill > (vec_b.technique + vec_b.combat_skill) * 1.3:
            decisive_factors.append(CombatFactor(
                name="Martial Mastery & Battle IQ",
                category="TECHNIQUE",
                advantage_to=combatant_a_id,
                weight=1.3,
                description=f"{combatant_a_name} outclasses in martial precision, energy efficiency, and counter-strikes."
            ))
            score_a *= 1.20
        elif vec_b.technique + vec_b.combat_skill > (vec_a.technique + vec_a.combat_skill) * 1.3:
            decisive_factors.append(CombatFactor(
                name="Martial Mastery & Battle IQ",
                category="TECHNIQUE",
                advantage_to=combatant_b_id,
                weight=1.3,
                description=f"{combatant_b_name} outclasses in martial precision, energy efficiency, and counter-strikes."
            ))
            score_b *= 1.20

        # 3. Equipment Advantage
        eq_a = self.power_repo.get_equipment_for_character(combatant_a_id, at_chapter=chapter_number)
        eq_b = self.power_repo.get_equipment_for_character(combatant_b_id, at_chapter=chapter_number)

        def calc_eq_power(items):
            total = 0.0
            rarity_weights = {"COMMON": 5, "UNCOMMON": 15, "RARE": 35, "EPIC": 80, "LEGENDARY": 200, "MYTHIC": 500, "TRANSCENDENT": 1200}
            for itm in items:
                if not itm.is_destroyed:
                    r_val = itm.rarity.value if hasattr(itm.rarity, "value") else str(itm.rarity)
                    total += rarity_weights.get(r_val, 10) * (itm.current_durability / max(1.0, itm.max_durability))
            return total

        eq_score_a = calc_eq_power(eq_a)
        eq_score_b = calc_eq_power(eq_b)

        if eq_score_a > eq_score_b * 1.5 and eq_score_a > 50:
            decisive_factors.append(CombatFactor(
                name="Superior Armament & Artifacts",
                category="EQUIPMENT",
                advantage_to=combatant_a_id,
                weight=1.3,
                description=f"{combatant_a_name} carries high-tier artifacts providing warding and destructive amplification."
            ))
            score_a *= 1.25
        elif eq_score_b > eq_score_a * 1.5 and eq_score_b > 50:
            decisive_factors.append(CombatFactor(
                name="Superior Armament & Artifacts",
                category="EQUIPMENT",
                advantage_to=combatant_b_id,
                weight=1.3,
                description=f"{combatant_b_name} carries high-tier artifacts providing warding and destructive amplification."
            ))
            score_b *= 1.25

        # 4. Status Effects / Conditions
        eff_a = self.power_repo.get_active_status_effects(combatant_a_id, current_chapter=chapter_number)
        eff_b = self.power_repo.get_active_status_effects(combatant_b_id, current_chapter=chapter_number)

        if eff_a:
            score_a *= 0.85
            decisive_factors.append(CombatFactor(
                name="Impaired Physical/Energetic State",
                category="CONDITION",
                advantage_to=combatant_b_id,
                weight=1.1,
                description=f"{combatant_a_name} is suffering from active status effects: {[e.effect_type for e in eff_a]}."
            ))
        if eff_b:
            score_b *= 0.85
            decisive_factors.append(CombatFactor(
                name="Impaired Physical/Energetic State",
                category="CONDITION",
                advantage_to=combatant_a_id,
                weight=1.1,
                description=f"{combatant_b_name} is suffering from active status effects: {[e.effect_type for e in eff_b]}."
            ))

        # 5. Hidden Mutations & Trump Cards (Reversals)
        mut_a = self.power_repo.get_mutations_for_character(combatant_a_id, at_chapter=chapter_number)
        mut_b = self.power_repo.get_mutations_for_character(combatant_b_id, at_chapter=chapter_number)

        for m in mut_a:
            if m.hidden_from_world or m.hidden_from_character:
                reversal_conditions.append(ReversalCondition(
                    condition_name=f"{combatant_a_name}'s Hidden {m.name}",
                    required_trigger=f"Activation of latent {m.category} mutation in life-and-death crisis",
                    likelihood=0.35,
                    outcome_shift=f"Grants +{sum(m.stat_modifiers.values()):.0f} total attribute burst to {combatant_a_name}",
                ))

        for m in mut_b:
            if m.hidden_from_world or m.hidden_from_character:
                reversal_conditions.append(ReversalCondition(
                    condition_name=f"{combatant_b_name}'s Hidden {m.name}",
                    required_trigger=f"Activation of latent {m.category} mutation in life-and-death crisis",
                    likelihood=0.35,
                    outcome_shift=f"Grants +{sum(m.stat_modifiers.values()):.0f} total attribute burst to {combatant_b_name}",
                ))

        # 6. Environmental Modifiers
        env_affinity = env.get("energy_affinity")
        if env_affinity:
            for pool in state_a.energy_pools:
                if pool.energy_type.value == env_affinity:
                    score_a *= 1.20
                    decisive_factors.append(CombatFactor(
                        name="Environmental Energy Resonance",
                        category="ENVIRONMENT",
                        advantage_to=combatant_a_id,
                        weight=1.2,
                        description=f"Local {env_affinity} environment actively nourishes {combatant_a_name}'s techniques."
                    ))
            for pool in state_b.energy_pools:
                if pool.energy_type.value == env_affinity:
                    score_b *= 1.20
                    decisive_factors.append(CombatFactor(
                        name="Environmental Energy Resonance",
                        category="ENVIRONMENT",
                        advantage_to=combatant_b_id,
                        weight=1.2,
                        description=f"Local {env_affinity} environment actively nourishes {combatant_b_name}'s techniques."
                    ))

        # 7. Probability Calculation
        total_score = score_a + score_b
        if total_score == 0:
            prob_a = 0.5
            prob_b = 0.5
            draw_prob = 0.0
        else:
            raw_prob_a = score_a / total_score
            raw_prob_b = score_b / total_score

            # Draw probability depends on how close they are
            closeness = 1.0 - abs(raw_prob_a - raw_prob_b)
            draw_prob = round(max(0.02, closeness * 0.12), 3)

            remaining = 1.0 - draw_prob
            prob_a = round(raw_prob_a * remaining, 3)
            prob_b = round(raw_prob_b * remaining, 3)

        # Confidence is high when decisive factors are clear and tier gap is non-zero
        confidence = min(0.95, max(0.40, abs(prob_a - prob_b) + 0.35))

        # Expected injury descriptions
        if prob_a > 0.85:
            injuries_a = "Negligible to superficial scrapes."
            injuries_b = "Severe to mortal trauma; energy core depletion."
            gap_desc = f"Decisive advantage for {combatant_a_name}."
        elif prob_b > 0.85:
            injuries_a = "Severe to mortal trauma; energy core depletion."
            injuries_b = "Negligible to superficial scrapes."
            gap_desc = f"Decisive advantage for {combatant_b_name}."
        elif prob_a > 0.60:
            injuries_a = "Moderate internal fatigue and minor meridian shock."
            injuries_b = "Heavy flesh trauma, possible broken bones or fractured armor."
            gap_desc = f"Favorable for {combatant_a_name}, but substantial struggle expected."
        elif prob_b > 0.60:
            injuries_a = "Heavy flesh trauma, possible broken bones or fractured armor."
            injuries_b = "Moderate internal fatigue and minor meridian shock."
            gap_desc = f"Favorable for {combatant_b_name}, but substantial struggle expected."
        else:
            injuries_a = "Both parties risk severe mutual exhaustion and structural damage."
            injuries_b = "Both parties risk severe mutual exhaustion and structural damage."
            gap_desc = "Highly volatile, nail-biting dead heat."

        return CombatAssessmentResult(
            combatant_a_id=combatant_a_id,
            combatant_b_id=combatant_b_id,
            combatant_a_name=combatant_a_name,
            combatant_b_name=combatant_b_name,
            win_probability_a=prob_a,
            win_probability_b=prob_b,
            draw_probability=draw_prob,
            confidence_level=confidence,
            decisive_factors=decisive_factors,
            reversal_conditions=reversal_conditions,
            expected_injuries_a=injuries_a,
            expected_injuries_b=injuries_b,
            power_gap_description=gap_desc,
            detailed_breakdown={
                "rating_a": rating_a,
                "rating_b": rating_b,
                "tier_a": state_a.current_tier,
                "stage_a": state_a.current_stage,
                "tier_b": state_b.current_tier,
                "stage_b": state_b.current_stage,
                "tier_gap": tier_gap,
                "effective_score_a": round(score_a, 1),
                "effective_score_b": round(score_b, 1),
            }
        )
