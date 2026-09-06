"""
Unit tests for Narrative State Engine.
"""
import unittest
import uuid
from novelforge.database.event_store import EventStore
from novelforge.backend.app.services.state_engine import NarrativeStateEngine
from novelforge.schemas.story_schemas import StoryEvent


class TestNarrativeStateEngine(unittest.TestCase):
    def setUp(self):
        self.store = EventStore(":memory:")
        self.engine = NarrativeStateEngine(self.store)
        self.story_id = str(uuid.uuid4())
        self.char_id = str(uuid.uuid4())

        # Setup character in Azure Dragon Sect
        ev = StoryEvent(
            event_id=str(uuid.uuid4()),
            story_id=self.story_id,
            chapter_number=1,
            scene_number=1,
            sequence_num=1,
            event_type="CHARACTER_CREATED",
            entity_type="CHARACTER",
            entity_id=self.char_id,
            payload={
                "name": "Lin Chen",
                "age": 16,
                "current_location": "Azure Dragon Sect",
                "realm": "Qi Condensation",
                "sub_realm": "Early",
                "rank_level": 2
            }
        )
        self.store.append_event(ev)

    def test_state_queries(self):
        state = self.engine.get_narrative_state(
            story_id=self.story_id,
            current_chapter=1,
            active_location="Azure Dragon Sect"
        )
        self.assertEqual(state["where_are_we"], "Azure Dragon Sect")
        self.assertIn("Lin Chen", state["who_is_present"])
        self.assertIn("Lin Chen", state["character_power_levels"])


if __name__ == "__main__":
    unittest.main()
