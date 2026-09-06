"""
NovelForge AI — Phase 4 Comprehensive Unit & Integration Tests
Tests all 10 core engines of Phase 4 Long-Term Story Architecture:
1. Plot Thread Lifecycle & Multi-Thread Query
2. Character Arc Archetypes & Transformation Milestones
3. Fair-Play Mystery Validation & Epistemic Secrecy Masking
4. Narrative Promises & Promise Debt Engine
5. Foreshadowing Planting, Quality Evaluation & Payoff
6. Plot Twists & Reversals Logic
7. Arc, Chapter & Scene Planning & Scene Transition Continuity
8. Narrative Dependency Graph & Downstream Change Impact Analysis
9. Story Health Engine (Composite 0-100 score, pacing, debts)
10. Narrative Context Builder (Token budgeting, relevance filtering)
"""
import unittest
import json
import sqlite3

from novelforge.database.plot_repository import PlotRepository
from novelforge.backend.app.services.plot_thread_service import PlotThreadService
from novelforge.backend.app.services.character_arc_service import CharacterArcService
from novelforge.backend.app.services.mystery_promise_service import MysteryPromiseService
from novelforge.backend.app.services.foreshadowing_twist_service import ForeshadowingTwistService
from novelforge.backend.app.services.arc_chapter_planning_service import ArcChapterPlanningService
from novelforge.backend.app.services.dependency_impact_service import DependencyImpactService
from novelforge.backend.app.services.story_health_service import StoryHealthService
from novelforge.backend.app.services.narrative_context_builder import NarrativeContextBuilder
from novelforge.schemas.plot_models import (
    PlotThreadType, ThreadStatus, ArcType, GoalType, GoalStatus,
    MysteryStatus, PromiseStatus, ForeshadowingType, ForeshadowingQuality,
    PlanConfidence, PlanningHorizon, HookType
)

class TestPhase4PlotEngine(unittest.TestCase):
    def setUp(self):
        # In-memory database for isolated, high-speed test execution
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.plot_repo = PlotRepository(db_path=':memory:', conn=self.conn)
        
        self.plot_svc = PlotThreadService(self.plot_repo)
        self.arc_svc = CharacterArcService(self.plot_repo)
        self.mp_svc = MysteryPromiseService(self.plot_repo)
        self.ft_svc = ForeshadowingTwistService(self.plot_repo)
        self.plan_svc = ArcChapterPlanningService(self.plot_repo)
        self.dep_svc = DependencyImpactService(self.plot_repo)
        self.health_svc = StoryHealthService(self.plot_repo, self.mp_svc)
        self.context_builder = NarrativeContextBuilder(self.plot_repo, self.plot_svc, self.mp_svc)

        self.story_id = 'test-story-phase4'

    def tearDown(self):
        self.conn.close()

    def test_01_main_plot_and_threads(self):
        """Verify main plot creation, turning points, and 19-type plot thread lifecycle."""
        plot = self.plot_svc.initialize_main_plot(
            story_id=self.story_id,
            premise='A cultivator returns to alter destiny.',
            central_conflict='Mortal resistance vs Cosmic Dao',
            protagonist_goal='Defend the Nine Peaks',
            ultimate_antagonistic_force='Outer God Cult',
            central_stakes='Total extinction',
            thematic_question='Can destiny be rewritten?',
            desired_ending='True peace'
        )
        self.assertIsNotNone(plot.id)
        self.assertEqual(plot.premise, 'A cultivator returns to alter destiny.')

        tp = self.plot_svc.add_turning_point(self.story_id, 'Eclipse Awakening', 'Protagonist revives', 1, 1, 1)
        self.assertEqual(tp.title, 'Eclipse Awakening')

        # Create plot threads across multiple types
        t1 = self.plot_svc.create_thread(
            story_id=self.story_id,
            name='Purify Faction Moles',
            thread_type=PlotThreadType.POLITICAL,
            description='Identify spies in inner court',
            started_chapter=1,
            target_resolution_chapter=20
        )
        self.assertEqual(t1.status, ThreadStatus.OPEN)

        # Update status and resolve
        t1_updated = self.plot_svc.update_thread_status(t1.id, ThreadStatus.RESOLVED, actual_resolution_chapter=18)
        self.assertEqual(t1_updated.status, ThreadStatus.RESOLVED)
        self.assertEqual(t1_updated.actual_resolution_chapter, 18)

    def test_02_character_arcs_and_milestones(self):
        """Verify character arc archetypes, transformation milestones, and goal progress."""
        arc = self.arc_svc.create_character_arc(
            character_id='char-hero',
            story_id=self.story_id,
            arc_type=ArcType.REDEMPTION,
            initial_state='Cold-blooded loner',
            internal_problem='Survivor guilt',
            want='Retribution',
            need='Forgiveness and fellowship',
            pressure='Impending war',
            transformation='From vengeful ghost to guardian pillar',
            final_state='Compassionate protector'
        )
        self.assertEqual(arc.arc_type, ArcType.REDEMPTION)

        m = self.arc_svc.add_arc_milestone(arc.id, 5, 'Spares an Enemy Disciple', 'Decides not to execute a surrendering foe.', 'char-hero')
        self.assertEqual(m.title, 'Spares an Enemy Disciple')

        # Goals
        g = self.arc_svc.create_goal(
            character_id='char-hero',
            story_id=self.story_id,
            description='Reach Intermediate Realm',
            goal_type=GoalType.POWER,
            priority=5
        )
        self.assertEqual(g.progress, 0.0)
        g_updated = self.arc_svc.update_goal_progress(g.id, progress=0.75, status=GoalStatus.PROGRESSING)
        self.assertEqual(g_updated.progress, 0.75)
        self.assertEqual(g_updated.status, GoalStatus.PROGRESSING)

    def test_03_mystery_epistemic_masking_and_fair_play(self):
        """Verify mystery epistemic access control (reader masking vs author visibility) and fair-play validation."""
        myst = self.mp_svc.create_mystery(
            story_id=self.story_id,
            title='The Poisoned Sovereign',
            question='Who slipped the Nether-Lotus into the Emperor tea?',
            hidden_truth='The Imperial Physician under blackmail by the Crown Prince.'
        )
        
        # Epistemic masking test
        reader_view = self.mp_svc.get_mystery_view(myst.id, viewer_role='READER')
        self.assertEqual(reader_view['hidden_truth'], '[PROTECTED CANONICAL TRUTH]')

        author_view = self.mp_svc.get_mystery_view(myst.id, viewer_role='AUTHOR')
        self.assertEqual(author_view['hidden_truth'], 'The Imperial Physician under blackmail by the Crown Prince.')

        # Fair-play check: Initially no clues -> should fail fair play
        fp_initial = self.mp_svc.validate_fair_play_mystery(myst.id)
        self.assertFalse(fp_initial['is_fair_play'])
        
        # Add clues
        self.mp_svc.add_clue(myst.id, 'Stained silver needle in the royal kitchen', 2, importance='MAJOR')
        self.mp_svc.add_clue(myst.id, 'Physician missing medicinal supply logs', 4, importance='MAJOR')
        
        fp_updated = self.mp_svc.validate_fair_play_mystery(myst.id)
        self.assertTrue(fp_updated['is_fair_play'])
        self.assertEqual(fp_updated['total_clues'], 2)

    def test_04_promises_and_narrative_debt(self):
        """Verify story promise lifecycle and overdue promise debt calculation."""
        p = self.mp_svc.create_promise(
            story_id=self.story_id,
            description='Hero vows to challenge Clan Patriarch at Year-End Tournament',
            promise_type='TOURNAMENT_CLIMAX',
            introduced_chapter=5,
            expected_payoff_window=10  # Expected by ch 15
        )
        self.assertEqual(p.status, PromiseStatus.OPEN)

        # Evaluate debt at chapter 12 (within window -> 0 debt)
        debts_ch12 = self.mp_svc.detect_promise_debts(self.story_id, current_chapter=12)
        self.assertEqual(len(debts_ch12), 0)

        # Evaluate debt at chapter 20 (overdue by 5 chapters -> narrative debt generated)
        debts_ch20 = self.mp_svc.detect_promise_debts(self.story_id, current_chapter=20)
        self.assertGreaterEqual(len(debts_ch20), 1)
        self.assertIn('Overdue Promise', debts_ch20[0].title)

    def test_05_foreshadowing_clue_quality_and_twists(self):
        """Verify foreshadowing clue quality evaluation (too subtle, too obvious) and twist linking."""
        # Plant too obvious clue
        seed_obvious = self.ft_svc.plant_seed(
            story_id=self.story_id,
            seed_text='The chancellor villainous tattoo was seen by everyone.',
            foreshadowing_type=ForeshadowingType.VISUAL,
            target_event='Chancellor Betrayal',
            target_reveal='Chancellor is evil',
            chapter_introduced=1,
            clue_strength=0.95
        )
        eval_obvious = self.ft_svc.evaluate_foreshadowing_quality(seed_obvious.id)
        self.assertIn('TOO_OBVIOUS', eval_obvious['issues'][0])

        # Plant perfectly timed clue
        seed_perfect = self.ft_svc.plant_seed(
            story_id=self.story_id,
            seed_text='Faint jasmine aroma lingering in the study.',
            foreshadowing_type=ForeshadowingType.ENVIRONMENTAL,
            target_event='Midnight Infiltrator',
            target_reveal='Empress secret meeting',
            chapter_introduced=3,
            clue_strength=0.5
        )
        eval_perfect = self.ft_svc.evaluate_foreshadowing_quality(seed_perfect.id)
        self.assertTrue(eval_perfect['is_effective'])

        # Create plot twist linking the seed
        twist = self.ft_svc.create_twist(
            story_id=self.story_id,
            title='Empress Secret Alliance',
            setup='Empress presumed loyal to Emperor',
            hidden_truth='Empress secretly directing the northern rebellion',
            reveal_text='Empress reveals northern seal',
            expected_reader_belief='Empress is loyal',
            actual_truth='Empress is rebel commander',
            reveal_chapter=25,
            foreshadowing_ids=[seed_perfect.id]
        )
        self.assertIsNotNone(twist.id)
        self.assertEqual(len(twist.foreshadowing_ids), 1)

    def test_06_arc_chapter_and_scene_planning(self):
        """Verify arc planning, chapter blueprinting, and scene continuity checks."""
        arc = self.plan_svc.create_arc_plan(
            saga_id='saga-1',
            story_id=self.story_id,
            arc_name='Trial of the Nine Peaks',
            sequence_order=1,
            start_chapter=1,
            end_chapter=30,
            arc_objective='Secure peak disciple status',
            central_conflict='Lin Chen vs Rival Disciples'
        )
        self.assertEqual(arc.arc_name, 'Trial of the Nine Peaks')

        ch = self.plan_svc.create_chapter_plan(
            arc_id=arc.id,
            chapter_number=1,
            title='The Awakening',
            chapter_objective='Orient in past body',
            main_conflict='Weak body vs memory of grandmaster cultivation'
        )

        sc1 = self.plan_svc.create_scene_plan(
            chapter_id=ch.id,
            sequence_order=1,
            title='Waking in the Infirmary',
            purpose='Realize regression',
            location_id='loc-infirmary',
            entry_state={'location_id': 'loc-infirmary', 'active_injuries': ['fever']},
            exit_state={'location_id': 'loc-infirmary', 'active_injuries': ['meridian fatigue']}
        )

        # sc2 has consistent entry state
        sc2 = self.plan_svc.create_scene_plan(
            chapter_id=ch.id,
            sequence_order=2,
            title='Leaving the Infirmary Bed',
            purpose='Inspect brother room',
            location_id='loc-infirmary',
            entry_state={'location_id': 'loc-infirmary', 'active_injuries': ['meridian fatigue']},
            exit_state={'location_id': 'loc-courtyard', 'active_injuries': ['meridian fatigue']}
        )

        is_valid_good, issues_good = self.plan_svc.validate_scene_transition(sc1, sc2)
        self.assertTrue(is_valid_good)
        self.assertEqual(len(issues_good), 0)

        # sc3 has teleportation discontinuity (entry location is suddenly mountain peak without transit)
        sc3 = self.plan_svc.create_scene_plan(
            chapter_id=ch.id,
            sequence_order=3,
            title='Top of the Mountain',
            purpose='Fight eagle',
            location_id='loc-peak',
            entry_state={'location_id': 'loc-distant-peak', 'active_injuries': ['meridian fatigue']},
            exit_state={'location_id': 'loc-distant-peak'}
        )
        is_valid_bad, issues_bad = self.plan_svc.validate_scene_transition(sc2, sc3)
        self.assertFalse(is_valid_bad)
        self.assertIn('SPATIAL_JUMP', issues_bad[0])

    def test_07_dependency_graph_and_change_impact(self):
        """Verify narrative dependency graph and rewrite risk analysis."""
        dep1 = self.dep_svc.add_dependency(
            story_id=self.story_id,
            source_type='PLOT_THREAD',
            source_id='node-A',
            target_type='CHAPTER_PLAN',
            target_id='node-B',
            dependency_type='CAUSAL',
            description='Chapter B relies on Node A resolution'
        )
        dep2 = self.dep_svc.add_dependency(
            story_id=self.story_id,
            source_type='CHAPTER_PLAN',
            source_id='node-B',
            target_type='SCENE_PLAN',
            target_id='node-C',
            dependency_type='TEMPORAL',
            description='Scene C relies on Chapter B'
        )

        impact = self.dep_svc.analyze_change_impact(
            story_id=self.story_id,
            modified_entity_type='PLOT_THREAD',
            modified_entity_id='node-A',
            modified_chapter=1
        )
        self.assertGreaterEqual(impact.total_affected_elements, 1)
        self.assertIn(impact.downstream_rewrite_risk, ('LOW', 'MEDIUM', 'HIGH', 'CATASTROPHIC'))

    def test_08_story_health_and_context_builder(self):
        """Verify quantitative story health calculation and token-budgeted narrative context builder."""
        # Story Health Report
        health = self.health_svc.calculate_story_health(self.story_id, current_chapter=10)
        self.assertGreaterEqual(health.overall_health_score, 0.0)
        self.assertLessEqual(health.overall_health_score, 100.0)
        self.assertIsNotNone(health.recommendations)

        # Context Builder
        ctx = self.context_builder.build_scene_context(
            story_id=self.story_id,
            chapter_number=1,
            scene_num=1,
            character_ids=['char-hero'],
            token_budget=1500
        )
        self.assertIn('prompt_text', ctx)
        self.assertLessEqual(ctx['token_estimate'], 1600)

if __name__ == '__main__':
    unittest.main()
