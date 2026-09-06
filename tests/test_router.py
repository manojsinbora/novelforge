"""
Unit tests for Model Router & LLM Provider Abstraction.
"""
import unittest
from novelforge.models.router import ModelRouter, TaskTier


class TestModelRouter(unittest.TestCase):
    def setUp(self):
        self.router = ModelRouter(mode="mock")

    def test_routing_and_generation(self):
        output = self.router.generate_with_fallback(
            task_type="PROSE_GENERATION",
            prompt="Write the opening scene of chapter 1."
        )
        self.assertTrue(len(output) > 10)
        self.assertIn("Lin Chen", output)

    def test_qa_critique_mock(self):
        output = self.router.generate_with_fallback(
            task_type="CONTINUITY_QA",
            prompt="Evaluate and score chapter critique."
        )
        self.assertIn("overall", output)
        self.assertIn("APPROVED", output)


if __name__ == "__main__":
    unittest.main()
