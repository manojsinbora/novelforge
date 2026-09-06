"""
Unit tests for NovelForge AI Event Store and Time-Travel Projections.
"""
import unittest
import uuid
from novelforge.database.event_store import EventStore
from novelforge.schemas.story_schemas import StoryEvent


class TestEventStore(unittest.TestCase):
    def setUp(self):
        self.store = EventStore(":memory:")
        self.story_id = str(uuid.uuid4())
        self.char_id = str(uuid.uuid4())

    def test_append_and_replay_events(self):
        # Event 1: Create Character at Ch 1
        ev1 = StoryEvent(
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
                "gender": "Male",
                "realm": "Qi Condensation",
                "sub_realm": "Early",
                "rank_level": 2
            }
        )
        self.store.append_event(ev1)

        # Event 2: Promote Character at Ch 50
        ev2 = StoryEvent(
            event_id=str(uuid.uuid4()),
            story_id=self.story_id,
            chapter_number=50,
            scene_number=3,
            sequence_num=2,
            event_type="CHARACTER_PROMOTED",
            entity_type="CHARACTER",
            entity_id=self.char_id,
            payload={
                "realm": "Foundation Establishment",
                "sub_realm": "Middle",
                "rank_level": 3
            }
        )
        self.store.append_event(ev2)

        # Time travel test: Project at Ch 25 (Should be Early Qi Condensation)
        state_at_25 = self.store.project_state(self.story_id, at_chapter=25)
        char_at_25 = state_at_25["characters"][self.char_id]
        self.assertEqual(char_at_25.cultivation.realm, "Qi Condensation")
        self.assertEqual(char_at_25.cultivation.sub_realm, "Early")
        self.assertEqual(state_at_25["total_events_applied"], 1)

        # Project at Ch 55 (Should be Foundation Establishment)
        state_at_55 = self.store.project_state(self.story_id, at_chapter=55)
        char_at_55 = state_at_55["characters"][self.char_id]
        self.assertEqual(char_at_55.cultivation.realm, "Foundation Establishment")
        self.assertEqual(char_at_55.cultivation.sub_realm, "Middle")
        self.assertEqual(state_at_55["total_events_applied"], 2)


if __name__ == "__main__":
    unittest.main()
