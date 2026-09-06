"""
Unit tests for Deterministic Cultivation Combat Evaluator.
"""
import unittest
from novelforge.tools.cultivation_evaluator import CultivationCombatEvaluator
from novelforge.schemas.story_schemas import Character, CultivationState


class TestCultivationEvaluator(unittest.TestCase):
    def test_overwhelming_realm_gap_impossible(self):
        mortal = Character(
            id="c1",
            name="Mortal Lin",
            age=16,
            gender="Male",
            cultivation=CultivationState(realm="Mortal", sub_realm="None")
        )
        nascent_elder = Character(
            id="c2",
            name="Grand Elder Gu",
            age=500,
            gender="Male",
            cultivation=CultivationState(realm="Nascent Soul", sub_realm="Peak")
        )

        matchup = CultivationCombatEvaluator.evaluate_matchup(attacker=mortal, defender=nascent_elder)
        
        self.assertEqual(matchup["verdict"], "IMPOSSIBLE_VICTORY")
        self.assertIn("LLM scene writer must NOT generate a clean solo victory", matchup["boundary_rule"])

    def test_equal_matchup(self):
        disciple1 = Character(
            id="d1",
            name="Disciple Zhao",
            age=19,
            gender="Male",
            cultivation=CultivationState(realm="Qi Condensation", sub_realm="Middle")
        )
        disciple2 = Character(
            id="d2",
            name="Disciple Wang",
            age=20,
            gender="Male",
            cultivation=CultivationState(realm="Qi Condensation", sub_realm="Middle")
        )

        matchup = CultivationCombatEvaluator.evaluate_matchup(attacker=disciple1, defender=disciple2)
        self.assertEqual(matchup["verdict"], "CONTESTED_SKILL_MATCHUP")

    def test_awakening_levels_evaluation(self):
        novice_arthur = Character(
            id="a1",
            name="Arthur Vance",
            age=23,
            gender="Male",
            cultivation=CultivationState(realm="Novice", sub_realm="Peak")
        )
        intermediate_warlord = Character(
            id="w1",
            name="Ironfang Cole",
            age=34,
            gender="Male",
            cultivation=CultivationState(realm="Intermediate", sub_realm="Peak")
        )

        matchup = CultivationCombatEvaluator.evaluate_matchup(attacker=novice_arthur, defender=intermediate_warlord)
        # 1-realm gap makes direct solo combat desperate without traps/poisons
        self.assertIn(matchup["verdict"], ["DESPERATE_PYRRHIC_POSSIBILITY", "IMPOSSIBLE_VICTORY"])



if __name__ == "__main__":
    unittest.main()
