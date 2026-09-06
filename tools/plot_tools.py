"""
NovelForge AI — Story Architecture Agent Tools
Phase 4: Standardized Tool Suite for AI Planning & Writing Agents
Separates READ tools, PROPOSE tools, and CANON mutation tools.
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional

from novelforge.database.plot_repository import PlotRepository
from novelforge.backend.app.services.plot_thread_service import PlotThreadService
from novelforge.backend.app.services.character_arc_service import CharacterArcService
from novelforge.backend.app.services.mystery_promise_service import MysteryPromiseService
from novelforge.backend.app.services.foreshadowing_twist_service import ForeshadowingTwistService
from novelforge.backend.app.services.arc_chapter_planning_service import ArcChapterPlanningService
from novelforge.backend.app.services.dependency_impact_service import DependencyImpactService
from novelforge.backend.app.services.story_health_service import StoryHealthService
from novelforge.backend.app.services.narrative_context_builder import NarrativeContextBuilder
from novelforge.schemas.plot_models import PlotThreadType, ThreadStatus, ArcType, GoalType, HookType, PlanConfidence


class StoryArchitectureToolSuite:
    def __init__(self, plot_repo: Optional[PlotRepository] = None):
        self.plot_repo = plot_repo or PlotRepository()
        self.thread_svc = PlotThreadService(self.plot_repo)
        self.arc_svc = CharacterArcService(self.plot_repo)
        self.mystery_promise_svc = MysteryPromiseService(self.plot_repo)
        self.twist_svc = ForeshadowingTwistService(self.plot_repo)
        self.planning_svc = ArcChapterPlanningService(self.plot_repo)
        self.dependency_svc = DependencyImpactService(self.plot_repo)
        self.health_svc = StoryHealthService(self.plot_repo, self.mystery_promise_svc)
        self.context_builder = NarrativeContextBuilder(
            self.plot_repo, self.thread_svc, self.mystery_promise_svc
        )

    # =========================================================================
    # 1. READ TOOLS
    # =========================================================================

    def get_story_plan(self, story_id: str) -> Dict[str, Any]:
        plot = self.thread_svc.get_main_plot(story_id)
        return plot.to_dict() if plot else {"error": f"No main plot for story {story_id}"}

    def get_active_plot_threads(self, story_id: str) -> List[Dict[str, Any]]:
        threads = self.thread_svc.get_active_threads(story_id)
        return [t.to_dict() for t in threads]

    def get_open_promises(self, story_id: str) -> List[Dict[str, Any]]:
        promises = self.plot_repo.get_promises_for_story(story_id, status="OPEN")
        return [p.to_dict() for p in promises]

    def get_active_mysteries(self, story_id: str, viewer_role: str = "READER") -> List[Dict[str, Any]]:
        mysteries = self.plot_repo.get_mysteries_for_story(story_id)
        return [self.mystery_promise_svc.get_mystery_view(m.id, viewer_role=viewer_role) for m in mysteries]

    def get_story_health(self, story_id: str, current_chapter: int) -> Dict[str, Any]:
        report = self.health_svc.calculate_story_health(story_id, current_chapter)
        return report.to_dict()

    def get_planning_horizons(self, story_id: str, current_chapter: int) -> Dict[str, Any]:
        return self.planning_svc.get_planning_horizons(story_id, current_chapter)

    # =========================================================================
    # 2. PROPOSE TOOLS (AGENTS GENERATE PROPOSALS WITHOUT CANON BREAK)
    # =========================================================================

    def propose_arc_plan(
        self,
        saga_id: str,
        story_id: str,
        arc_name: str,
        sequence_order: int,
        start_chapter: int,
        end_chapter: int,
        arc_objective: str,
        central_conflict: str,
        confidence: str = "HIGH_CONFIDENCE"
    ) -> Dict[str, Any]:
        conf = PlanConfidence.HIGH_CONFIDENCE
        try:
            conf = PlanConfidence(confidence)
        except ValueError:
            pass
        plan = self.planning_svc.create_arc_plan(
            saga_id=saga_id,
            story_id=story_id,
            arc_name=arc_name,
            sequence_order=sequence_order,
            start_chapter=start_chapter,
            end_chapter=end_chapter,
            arc_objective=arc_objective,
            central_conflict=central_conflict,
            confidence=conf,
        )
        return {"status": "PROPOSED", "plan": plan.to_dict()}

    def propose_chapter_plan(
        self,
        arc_id: str,
        chapter_number: int,
        title: str,
        chapter_objective: str,
        main_conflict: str,
        ending_hook: str = "",
        hook_type: str = "MYSTERY"
    ) -> Dict[str, Any]:
        htype = HookType.MYSTERY
        try:
            htype = HookType(hook_type)
        except ValueError:
            pass
        plan = self.planning_svc.create_chapter_plan(
            arc_id=arc_id,
            chapter_number=chapter_number,
            title=title,
            chapter_objective=chapter_objective,
            main_conflict=main_conflict,
            ending_hook=ending_hook,
            hook_type=htype,
        )
        return {"status": "PROPOSED", "plan": plan.to_dict()}

    def propose_twist(
        self,
        story_id: str,
        title: str,
        setup: str,
        hidden_truth: str,
        reveal_text: str,
        actual_truth: str,
        reveal_chapter: int
    ) -> Dict[str, Any]:
        twist = self.twist_svc.create_twist(
            story_id=story_id,
            title=title,
            setup=setup,
            hidden_truth=hidden_truth,
            reveal_text=reveal_text,
            expected_reader_belief="",
            actual_truth=actual_truth,
            reveal_chapter=reveal_chapter,
        )
        return {"status": "PROPOSED", "twist": twist.to_dict()}

    # =========================================================================
    # 3. IMPACT ANALYSIS & REWRITE SUPPORT
    # =========================================================================

    def analyze_change_impact(
        self,
        story_id: str,
        modified_entity_type: str,
        modified_entity_id: str,
        modified_chapter: int
    ) -> Dict[str, Any]:
        report = self.dependency_svc.analyze_change_impact(
            story_id=story_id,
            modified_entity_type=modified_entity_type,
            modified_entity_id=modified_entity_id,
            modified_chapter=modified_chapter
        )
        return report.to_dict()
