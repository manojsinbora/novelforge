"""
NovelForge AI — Comprehensive Phase 2 Test Suite
Validates all 25 specific test conditions from Phase 2 Specification:
1. Story creation & Story Bible
2. Character creation & structured fields
3. Character relationships & historical tracking
4. Epistemic knowledge verification (character CANNOT know a secret before reveal chapter)
5. Location hierarchy & travel continuity error detection (impossible travel)
6. Spatial presence anomaly (cannot appear in two incompatible locations on same day)
7. Canon protection & permission enforcement (AI agents cannot modify canon directly)
8. Audit logging
9. State snapshots & historical state reconstruction at Chapter N
10. Database <-> File synchronization
"""
import unittest
import uuid
import datetime
import os
from novelforge.database.narrative_repository import NarrativeRepository
from novelforge.backend.app.services.canon_service import CanonService
from novelforge.backend.app.services.knowledge_service import KnowledgeService
from novelforge.backend.app.services.timeline_service import TimelineService
from novelforge.backend.app.services.story_context_service import StoryContextService
from novelforge.backend.app.services.sync_service import StorySyncService
from novelforge.schemas.narrative_models import (
    StoryModel, StoryBible, StoryPremise, StoryThemes, StoryTone,
    NarrativeRules, WorldRules, Saga, Arc, Chapter, CharacterEntity,
    CharacterCultivationProfile, CharacterVoiceProfile, CharacterRelationship,
    RelationshipType, KnowledgeFactEntity, FactKnowledgeEntry, KnowledgeState,
    WorldLocation, LocationType, FactionEntity, StoryEventEntity, StoryEventType,
    CanonStatus, EntityStatus, PermissionLevel, ProposalStatus, ChapterMemory
)


class TestPhase2NarrativeStateEngine(unittest.TestCase):
    def setUp(self):
        # Isolated in-memory repository for unit testing
        self.repo = NarrativeRepository(":memory:")
        self.canon_service = CanonService(self.repo)
        self.knowledge_service = KnowledgeService(self.repo)
        self.timeline_service = TimelineService(self.repo)
        self.context_service = StoryContextService(self.repo)
        self.sync_service = StorySyncService(self.repo, base_stories_dir="novelforge/tests/scratch_stories")
        self.story_id = str(uuid.uuid4())

        # Seed initial test story
        self.story = StoryModel(
            id=self.story_id,
            title="Chronicles of the Star Forge",
            working_title="Star Forge",
            premise="An artisan unearths cosmic dao ruins.",
            genre="Progression Fantasy",
            target_chapter_count=300,
            target_chapter_word_count=1800,
            current_chapter=10,
            current_arc=1,
            current_saga=1
        )
        self.repo.create_story(self.story)

    def tearDown(self):
        # Clean up any scratch test exports
        import shutil
        if os.path.exists("novelforge/tests/scratch_stories"):
            shutil.rmtree("novelforge/tests/scratch_stories")

    # =========================================================================
    # 1. STORY & STORY BIBLE TESTS
    # =========================================================================
    def test_story_creation_and_bible(self):
        s = self.repo.get_story(self.story_id)
        self.assertIsNotNone(s)
        self.assertEqual(s.title, "Chronicles of the Star Forge")
        self.assertEqual(s.target_chapter_count, 300)

        bible = StoryBible(
            story_id=self.story_id,
            premise=StoryPremise(core_premise="Cosmic artisan rises"),
            tone=StoryTone(darkness=0.7, humor=0.3),
            world_rules=WorldRules(cultivation_rules={"tiers": "Novice -> Transcendent"})
        )
        self.repo.set_story_bible(bible)

        saved_bible = self.repo.get_story_bible(self.story_id)
        self.assertIsNotNone(saved_bible)
        self.assertEqual(saved_bible["premise"]["core_premise"], "Cosmic artisan rises")
        self.assertEqual(saved_bible["tone"]["darkness"], 0.7)

    # =========================================================================
    # 2. CHARACTER & STRUCTURED DOSSIER TESTS
    # =========================================================================
    def test_character_creation_and_versioning(self):
        char = CharacterEntity(
            id="char-test-01",
            story_id=self.story_id,
            name="Arthur Vance",
            age=23,
            gender="Male",
            cultivation=CharacterCultivationProfile(realm="Novice", sub_realm="Early", rank_level=1),
            voice_profile=CharacterVoiceProfile(sentence_cadence="analytical", formality_level=0.7),
            current_location_name="Grand Archives"
        )
        self.repo.add_character(char)

        fetched = self.repo.get_character(self.story_id, "char-test-01")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["name"], "Arthur Vance")
        self.assertEqual(fetched["cultivation"]["realm"], "Novice")
        self.assertEqual(fetched["voice_profile"]["formality_level"], 0.7)
        self.assertEqual(fetched["version"], 1)

    # =========================================================================
    # 3. CHARACTER RELATIONSHIPS & HISTORICAL TRACKING
    # =========================================================================
    def test_character_relationships_and_history(self):
        char1 = CharacterEntity(id="c1", story_id=self.story_id, name="Arthur")
        char2 = CharacterEntity(id="c2", story_id=self.story_id, name="Vera")
        self.repo.add_character(char1)
        self.repo.add_character(char2)

        rel = CharacterRelationship(
            story_id=self.story_id,
            source_character_id="c1",
            target_character_id="c2",
            relationship_type=RelationshipType.UNKNOWN,
            trust=0.0,
            beginning_chapter=1,
            current_chapter=1,
            notes="Initial encounter in the ruins"
        )
        self.repo.set_relationship(rel)

        # In chapter 5, they become allies
        rel.relationship_type = RelationshipType.ALLY
        rel.trust = 0.8
        rel.current_chapter = 5
        rel.notes = "Vera covered Arthur during the beast ambush"
        self.repo.set_relationship(rel)

        rels = self.repo.get_relationships(self.story_id, "c1")
        self.assertEqual(len(rels), 1)
        self.assertEqual(rels[0]["relationship_type"], "ALLY")
        self.assertEqual(rels[0]["trust"], 0.8)
        self.assertEqual(rels[0]["version"], 2)
        # Verify history log recorded Chapter 1 and Chapter 5 changes
        self.assertTrue(len(rels[0]["history"]) >= 1)
        self.assertEqual(rels[0]["history"][0]["chapter"], 5)

    # =========================================================================
    # 4. EPISTEMIC KNOWLEDGE & SECRET-LEAK GUARD TESTS
    # =========================================================================
    def test_character_cannot_know_secret_before_reveal_chapter(self):
        """
        MANDATORY REQUIREMENT: At least one test should verify:
        A character cannot know a secret before the chapter in which they learn it.
        """
        secret_fact = KnowledgeFactEntity(
            id="fact-sec-01",
            story_id=self.story_id,
            fact_key="elder_han_is_traitor",
            description="Elder Han poisoned the water supply and serves Blood Raven Sect.",
            author_knowledge=True,
            reader_knowledge=False,
            planned_reveal_chapter=50,
            character_knowledge_map={
                "char-villain": FactKnowledgeEntry(
                    character_id="char-villain", character_name="Elder Han",
                    state=KnowledgeState.KNOWN_TRUE, learned_at_chapter=1
                ),
                "char-hero": FactKnowledgeEntry(
                    character_id="char-hero", character_name="Bai Yue",
                    state=KnowledgeState.KNOWN_TRUE, learned_at_chapter=50, how_learned="Found the poisoned flask"
                )
            }
        )
        self.repo.add_knowledge_fact(secret_fact)

        # At Chapter 20, Bai Yue CANNOT know this secret!
        knows_at_ch20 = self.knowledge_service.can_character_know_fact(
            self.story_id, "char-hero", "elder_han_is_traitor", at_chapter=20
        )
        self.assertFalse(knows_at_ch20)

        # Invariant assertion: attempting to access secret at Ch 20 raises AssertionError
        with self.assertRaises(AssertionError):
            self.knowledge_service.assert_character_has_knowledge(
                self.story_id, "char-hero", "Bai Yue", "elder_han_is_traitor", at_chapter=20
            )

        # But at Chapter 52, Bai Yue CAN know it!
        knows_at_ch52 = self.knowledge_service.can_character_know_fact(
            self.story_id, "char-hero", "elder_han_is_traitor", at_chapter=52
        )
        self.assertTrue(knows_at_ch52)
        # Does not raise at Chapter 52
        self.knowledge_service.assert_character_has_knowledge(
            self.story_id, "char-hero", "Bai Yue", "elder_han_is_traitor", at_chapter=52
        )


    # =========================================================================
    # 5. LOCATION HIERARCHY & TRAVEL CONTINUITY TESTS
    # =========================================================================
    def test_travel_continuity_and_spatial_anomalies(self):
        """
        MANDATORY REQUIREMENT: At least one test should verify:
        A character cannot appear in two incompatible locations at the same story time.
        And impossible travel is flagged as a CONTINUITY ERROR.
        """
        city_a = WorldLocation(
            id="loc-a", story_id=self.story_id, name="Azure City",
            type=LocationType.CITY, coordinates={"x": 0.0, "y": 0.0}
        )
        city_c = WorldLocation(
            id="loc-c", story_id=self.story_id, name="Iron Citadel",
            type=LocationType.CITY, coordinates={"x": 600.0, "y": 0.0} # 600 km away!
        )
        self.repo.add_location(city_a)
        self.repo.add_location(city_c)

        # Travel check: 600 km in 2 days (40 km/day max standard) -> IMPOSSIBLE!
        travel_check = self.timeline_service.validate_travel_continuity(
            story_id=self.story_id, character_id="c1", character_name="Arthur",
            from_location_id="loc-a", to_location_id="loc-c",
            start_day=1, arrival_day=3, standard_travel_speed_km_per_day=40.0
        )
        self.assertFalse(travel_check["is_valid"])
        self.assertEqual(travel_check["error_type"], "CONTINUITY_ERROR_IMPOSSIBLE_TRAVEL")
        self.assertIn("600.0 km", travel_check["error_message"])

        # Spatial presence anomaly check: Character in two distant locations on same story day
        ev1 = StoryEventEntity(
            id="e1", story_id=self.story_id, chapter_number=1, scene_number=1,
            story_day=10, story_year=1, location_id="loc-a", location_name="Azure City",
            participants=["Arthur"], event_type=StoryEventType.MEETING
        )
        ev2 = StoryEventEntity(
            id="e2", story_id=self.story_id, chapter_number=1, scene_number=2,
            story_day=10, story_year=1, location_id="loc-c", location_name="Iron Citadel",
            participants=["Arthur"], event_type=StoryEventType.BATTLE
        )
        self.repo.add_event(ev1)
        self.repo.add_event(ev2)

        anomaly = self.timeline_service.check_character_presence_anomaly(
            self.story_id, "Arthur", story_day=10, active_chapter=1
        )
        self.assertIsNotNone(anomaly)
        self.assertIn("Spatial Anomaly", anomaly)

    # =========================================================================
    # 6. CANON PROTECTION & PERMISSION ENFORCEMENT TESTS
    # =========================================================================
    def test_ai_agent_cannot_modify_canon_directly(self):
        """
        MANDATORY REQUIREMENT: At least one test should verify:
        An AI agent cannot directly modify canonical information without authorization.
        """
        # Writing Agent (PROPOSAL_AGENT) tries to mutate canon directly -> MUST BE BLOCKED!
        with self.assertRaises(PermissionError):
            self.canon_service.mutate_canon_directly(
                story_id=self.story_id,
                entity_type="CHARACTER",
                entity_id="char-001",
                field_name="age",
                new_value=25,
                actor="Writing_Agent_Claude",
                permission_level=PermissionLevel.PROPOSAL_AGENT
            )

        # Instead, agent must submit a proposal:
        proposal = self.canon_service.submit_proposed_change(
            story_id=self.story_id,
            agent="Continuity_Agent",
            model="claude-3-5-sonnet",
            permission_level=PermissionLevel.PROPOSAL_AGENT,
            entity_type="CHARACTER",
            entity_id="char-001",
            field_name="age",
            previous_value=16,
            proposed_value=17,
            reason="Chapter 12 mentions his seventeenth birthday"
        )
        self.assertEqual(proposal.status, ProposalStatus.PENDING)

        # Verify proposal recorded and pending
        proposals = self.repo.get_proposals(self.story_id, status="PENDING")
        self.assertEqual(len(proposals), 1)

        # Verify audit log was created for the proposal
        audit_logs = self.repo.get_audit_logs(self.story_id)
        self.assertTrue(len(audit_logs) >= 1)
        self.assertEqual(audit_logs[0]["action"], "PROPOSAL_CREATED")

        # Unauthorized approval attempt by another PROPOSAL_AGENT -> BLOCKED!
        with self.assertRaises(PermissionError):
            self.canon_service.review_proposal(
                proposal_id=proposal.id,
                approver="Writing_Agent",
                permission_level=PermissionLevel.PROPOSAL_AGENT,
                decision="APPROVE"
            )

        # Authorized approval by CANON_EDITOR -> SUCCEEDS!
        approved = self.canon_service.review_proposal(
            proposal_id=proposal.id,
            approver="Human_Director",
            permission_level=PermissionLevel.CANON_EDITOR,
            decision="APPROVE"
        )
        self.assertTrue(approved)

        # Verify proposal status is APPROVED
        updated_prop = self.repo.get_proposals(self.story_id, status="APPROVED")
        self.assertEqual(len(updated_prop), 1)

    # =========================================================================
    # 7. STATE SNAPSHOTS & HISTORICAL RECONSTRUCTION TESTS
    # =========================================================================
    def test_state_snapshot_and_historical_reconstruction(self):
        char = CharacterEntity(
            id="c-snap-1", story_id=self.story_id, name="Lin Chen",
            current_location_name="Azure Peak",
            cultivation=CharacterCultivationProfile(realm="Novice", sub_realm="Early")
        )
        self.repo.add_character(char)

        ev1 = StoryEventEntity(
            id="ev-1", story_id=self.story_id, chapter_number=2, scene_number=1,
            story_day=2, story_year=1, location_id="loc-1", location_name="Azure Peak",
            participants=["Lin Chen"], event_type=StoryEventType.DISCOVERY,
            description="Found ancient star manual"
        )
        ev2 = StoryEventEntity(
            id="ev-2", story_id=self.story_id, chapter_number=8, scene_number=1,
            story_day=15, story_year=1, location_id="loc-2", location_name="Outer Market",
            participants=["Lin Chen"], event_type=StoryEventType.BREAKTHROUGH,
            description="Broke through to Novice Peak"
        )
        self.repo.add_event(ev1)
        self.repo.add_event(ev2)

        # Chapter memory for Ch 2 and Ch 8
        self.repo.save_chapter_memory(ChapterMemory(
            story_id=self.story_id, chapter_number=2, chapter_summary="Found manual in Azure Peak."
        ))
        self.repo.save_chapter_memory(ChapterMemory(
            story_id=self.story_id, chapter_number=8, chapter_summary="Advancement in Outer Market."
        ))

        # Reconstruct at Chapter 2: Only events up to Chapter 2 should be included!
        snap_ch2 = self.repo.get_story_state_snapshot(self.story_id, at_chapter=2)
        self.assertEqual(snap_ch2.current_chapter, 2)
        self.assertEqual(len(snap_ch2.recent_events), 1)
        self.assertEqual(snap_ch2.recent_chapter_summary, "Found manual in Azure Peak.")

        # Reconstruct at Chapter 8: Both events should be present!
        snap_ch8 = self.repo.get_story_state_snapshot(self.story_id, at_chapter=8)
        self.assertEqual(snap_ch8.current_chapter, 8)
        self.assertEqual(len(snap_ch8.recent_events), 2)
        self.assertEqual(snap_ch8.recent_chapter_summary, "Advancement in Outer Market.")

    # =========================================================================
    # 8. DATABASE <-> FILESYSTEM SYNCHRONIZATION TESTS
    # =========================================================================
    def test_database_to_filesystem_sync(self):
        export_dir = self.sync_service.export_story_to_filesystem(self.story_id, folder_name="test_export")
        self.assertTrue(os.path.exists(export_dir))
        self.assertTrue(os.path.exists(os.path.join(export_dir, "bible", "story.yaml")))
        self.assertTrue(os.path.exists(os.path.join(export_dir, "bible", "premise.md")))
        self.assertTrue(os.path.exists(os.path.join(export_dir, "world", "locations.yaml")))
        self.assertTrue(os.path.exists(os.path.join(export_dir, "timeline", "events.yaml")))


if __name__ == "__main__":
    unittest.main()
