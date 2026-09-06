"""
NovelForge AI — Story Architecture & Plot REST API (FastAPI Router)
Phase 4 Endpoints: Mainline Plot, Threads, Character Arcs, Mysteries, Promises, Blueprints & Health
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional

try:
    from fastapi import APIRouter, HTTPException, Query
    from pydantic import BaseModel, Field
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    class APIRouter:
        def __init__(self, *args, **kwargs):
            self.routes = []
        def get(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def post(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def put(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def delete(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            self.status_code = status_code
            self.detail = detail
    class BaseModel:
        pass
    def Field(*args, **kwargs):
        return None

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
    PlotThreadType, ThreadStatus, ArcType, GoalType, HookType, PlanConfidence
)

router = APIRouter(prefix="/api/v1/plot", tags=["Story Architecture & Plot Engine"])

# Shared service singletons
default_plot_repo = PlotRepository("novelforge/database/novelforge.sqlite3")
thread_svc = PlotThreadService(default_plot_repo)
arc_svc = CharacterArcService(default_plot_repo)
mystery_promise_svc = MysteryPromiseService(default_plot_repo)
twist_svc = ForeshadowingTwistService(default_plot_repo)
planning_svc = ArcChapterPlanningService(default_plot_repo)
dependency_svc = DependencyImpactService(default_plot_repo)
health_svc = StoryHealthService(default_plot_repo, mystery_promise_svc)
context_builder = NarrativeContextBuilder(default_plot_repo, thread_svc, mystery_promise_svc)


# =============================================================================
# 1. MAIN PLOT
# =============================================================================

@router.get("/stories/{story_id}/main")
def get_main_plot(story_id: str):
    plot = thread_svc.get_main_plot(story_id)
    if not plot:
        raise HTTPException(status_code=404, detail="Main plot not found")
    return plot.to_dict()


# =============================================================================
# 2. PLOT THREADS & SUBPLOTS
# =============================================================================

@router.get("/stories/{story_id}/threads")
def get_threads(story_id: str, status: Optional[str] = None):
    threads = default_plot_repo.get_threads_for_story(story_id, status=status)
    return [t.to_dict() for t in threads]

@router.put("/threads/{thread_id}/status")
def update_thread_status(thread_id: str, new_status: str, resolution_chapter: Optional[int] = None):
    try:
        st = ThreadStatus(new_status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid thread status: {new_status}")
    try:
        thread = thread_svc.update_thread_status(thread_id, st, resolution_chapter)
        return {"status": "success", "thread": thread.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =============================================================================
# 3. CHARACTER ARCS & GOALS
# =============================================================================

@router.get("/characters/{character_id}/arc")
def get_character_arc(character_id: str, story_id: str):
    arc = arc_svc.get_character_arc(character_id, story_id)
    if not arc:
        raise HTTPException(status_code=404, detail="Character arc not found")
    return arc.to_dict()

@router.get("/characters/{character_id}/goals")
def get_character_goals(character_id: str):
    goals = arc_svc.get_goals_for_character(character_id)
    return [g.to_dict() for g in goals]


# =============================================================================
# 4. MYSTERIES, CLUES & SECRETS
# =============================================================================

@router.get("/stories/{story_id}/mysteries")
def get_mysteries(story_id: str, role: str = "READER"):
    mysteries = default_plot_repo.get_mysteries_for_story(story_id)
    return [mystery_promise_svc.get_mystery_view(m.id, viewer_role=role) for m in mysteries]

@router.get("/mysteries/{mystery_id}/validate")
def validate_mystery_fair_play(mystery_id: str):
    try:
        return mystery_promise_svc.validate_fair_play_mystery(mystery_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# =============================================================================
# 5. PROMISES & NARRATIVE DEBT
# =============================================================================

@router.get("/stories/{story_id}/promises")
def get_promises(story_id: str, status: Optional[str] = None):
    promises = default_plot_repo.get_promises_for_story(story_id, status=status)
    return [p.to_dict() for p in promises]

@router.get("/stories/{story_id}/debts")
def get_narrative_debts(story_id: str, current_chapter: int = 1):
    debts = mystery_promise_svc.detect_promise_debts(story_id, current_chapter)
    return [d.to_dict() for d in debts]


# =============================================================================
# 6. STORY HEALTH & PACING
# =============================================================================

@router.get("/stories/{story_id}/health")
def get_story_health(story_id: str, current_chapter: int = 1):
    report = health_svc.calculate_story_health(story_id, current_chapter)
    return report.to_dict()


# =============================================================================
# 7. PLANNING HORIZONS & BLUEPRINTS
# =============================================================================

@router.get("/stories/{story_id}/horizons")
def get_planning_horizons(story_id: str, current_chapter: int = 1):
    return planning_svc.get_planning_horizons(story_id, current_chapter)

@router.get("/chapters/{chapter_number}/plan")
def get_chapter_plan(chapter_number: int, arc_id: Optional[str] = None):
    cp = planning_svc.get_chapter_plan(chapter_number, arc_id=arc_id)
    if not cp:
        raise HTTPException(status_code=404, detail=f"Chapter plan for Chapter {chapter_number} not found")
    return cp.to_dict()


# =============================================================================
# 8. CHANGE IMPACT ANALYSIS
# =============================================================================

@router.post("/stories/{story_id}/impact-analysis")
def analyze_change_impact(
    story_id: str,
    modified_entity_type: str,
    modified_entity_id: str,
    modified_chapter: int
):
    report = dependency_svc.analyze_change_impact(
        story_id=story_id,
        modified_entity_type=modified_entity_type,
        modified_entity_id=modified_entity_id,
        modified_chapter=modified_chapter,
    )
    return report.to_dict()
