"""
Unit tests for Context Allocator & Token Budgeting.
"""
import unittest
import uuid
from novelforge.models.context_budgeter import ContextBudgeter
from novelforge.schemas.story_schemas import Character, KnowledgeFact, Promise, PromiseStatus


class TestContextBudgeter(unittest.TestCase):
    def setUp(self):
        self.budgeter = ContextBudgeter(total_budget_tokens=4000)

    def test_epistemic_guard_and_budgeting(self):
        char1 = Character(
            id="char-1",
            name="Lin Chen",
            age=17,
            gender="Male"
        )
        char2 = Character(
            id="char-2",
            name="Elder Han",
            age=150,
            gender="Male"
        )

        secret_fact = KnowledgeFact(
            fact_key="poisoned_tea",
            description="Elder Han poisoned the jade cup.",
            author_knows=True,
            reader_knows=False,
            known_by_characters=["char-2"] # Only Elder Han knows
        )

        result = self.budgeter.assemble_scene_prompt(
            scene_objective="Lin Chen enters Elder Han's pavilion to request guidance.",
            present_characters=[char1, char2],
            knowledge_facts=[secret_fact],
            environment_desc="Rain drumming on pine eaves, incense drifting.",
            power_rules_desc="Elder Han is a Core Formation expert; Lin Chen cannot resist spiritual pressure.",
            active_promises=[],
            recent_prose_context="Lin Chen bowed deeply at the wooden threshold."
        )

        self.assertTrue(result["under_budget"])
        self.assertEqual(result["epistemic_guards_count"], 1)
        # Verify that Lin Chen is explicitly listed as NOT knowing the secret in the header
        self.assertIn("Lin Chen DO NOT KNOW THIS", result["prompt_text"])


if __name__ == "__main__":
    unittest.main()
