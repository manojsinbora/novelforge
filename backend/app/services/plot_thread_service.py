"""
NovelForge AI — Plot Thread & Subplot Service
Phase 4: Mainline Story Engine & 19-Type Plot Thread Lifecycle
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any
import uuid
import datetime

from novelforge.database.plot_repository import PlotRepository
from novelforge.schemas.plot_models import (
    MainPlot, StoryMilestone, PlotThread, PlotThreadType, ThreadStatus,
    SubplotPlan, StoryState
)


class PlotThreadService:
    def __init__(self, plot_repo: PlotRepository):
        self.plot_repo = plot_repo

    # =========================================================================
    # 1. MAIN PLOT MANAGEMENT
    # =========================================================================

    def initialize_main_plot(
        self,
        story_id: str,
        premise: str,
        central_conflict: str,
        protagonist_goal: str,
        ultimate_antagonistic_force: str,
        central_stakes: str,
        thematic_question: str,
        desired_ending: str,
        turning_points: Optional[List[StoryMilestone]] = None,
    ) -> MainPlot:
        plot = MainPlot(
            id=str(uuid.uuid4()),
            story_id=story_id,
            premise=premise,
            central_conflict=central_conflict,
            protagonist_goal=protagonist_goal,
            ultimate_antagonistic_force=ultimate_antagonistic_force,
            central_stakes=central_stakes,
            thematic_question=thematic_question,
            desired_ending=desired_ending,
            turning_points=turning_points or [],
            current_state=StoryState.ACTIVE,
        )
        return self.plot_repo.save_main_plot(plot)

    def get_main_plot(self, story_id: str) -> Optional[MainPlot]:
        return self.plot_repo.get_main_plot(story_id)

    def add_turning_point(
        self,
        story_id: str,
        title: str,
        description: str,
        target_saga: int,
        target_arc: int,
        approximate_chapter: int,
        consequences: Optional[List[str]] = None,
    ) -> StoryMilestone:
        plot = self.get_main_plot(story_id)
        if not plot:
            raise ValueError(f"Main plot for story {story_id} not found")
        ms = StoryMilestone(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            target_saga=target_saga,
            target_arc=target_arc,
            approximate_chapter=approximate_chapter,
            status="PLANNED",
            consequences=consequences or [],
        )
        plot.turning_points.append(ms)
        self.plot_repo.save_main_plot(plot)
        return ms

    # =========================================================================
    # 2. PLOT THREADS
    # =========================================================================

    def create_thread(
        self,
        story_id: str,
        name: str,
        thread_type: PlotThreadType,
        description: str,
        importance: float = 5.0,
        priority: int = 3,
        origin: str = "PROLOGUE",
        related_characters: Optional[List[str]] = None,
        related_factions: Optional[List[str]] = None,
        related_locations: Optional[List[str]] = None,
        related_mysteries: Optional[List[str]] = None,
        related_promises: Optional[List[str]] = None,
        started_chapter: int = 1,
        target_resolution_chapter: int = 50,
        notes: str = "",
    ) -> PlotThread:
        thread = PlotThread(
            id=str(uuid.uuid4()),
            story_id=story_id,
            name=name,
            thread_type=thread_type,
            description=description,
            importance=importance,
            priority=priority,
            status=ThreadStatus.OPEN,
            origin=origin,
            related_characters=related_characters or [],
            related_factions=related_factions or [],
            related_locations=related_locations or [],
            related_mysteries=related_mysteries or [],
            related_promises=related_promises or [],
            started_chapter=started_chapter,
            target_resolution_chapter=target_resolution_chapter,
            notes=notes,
        )
        return self.plot_repo.save_plot_thread(thread)

    def update_thread_status(
        self,
        thread_id: str,
        new_status: ThreadStatus,
        actual_resolution_chapter: Optional[int] = None
    ) -> PlotThread:
        thread = self.plot_repo.get_plot_thread(thread_id)
        if not thread:
            raise ValueError(f"Plot thread {thread_id} not found")
        thread.status = new_status
        if actual_resolution_chapter is not None:
            thread.actual_resolution_chapter = actual_resolution_chapter
        return self.plot_repo.save_plot_thread(thread)

    def get_active_threads(self, story_id: str) -> List[PlotThread]:
        all_threads = self.plot_repo.get_threads_for_story(story_id)
        active_statuses = {
            ThreadStatus.OPEN, ThreadStatus.ACTIVE, ThreadStatus.DEVELOPING,
            ThreadStatus.ESCALATING, ThreadStatus.READY_FOR_PAYOFF
        }
        return [t for t in all_threads if t.status in active_statuses]

    def get_threads_for_character(self, story_id: str, character_id: str) -> List[PlotThread]:
        all_threads = self.plot_repo.get_threads_for_story(story_id)
        return [t for t in all_threads if character_id in t.related_characters]

    # =========================================================================
    # 3. SUBPLOTS
    # =========================================================================

    def create_subplot(
        self,
        story_id: str,
        name: str,
        parent_thread_id: str,
        setup: str = "",
        development: str = "",
        escalation: str = "",
        midpoint: str = "",
        crisis: str = "",
        climax: str = "",
        resolution: str = "",
    ) -> SubplotPlan:
        sub = SubplotPlan(
            id=str(uuid.uuid4()),
            story_id=story_id,
            name=name,
            parent_thread_id=parent_thread_id,
            setup=setup,
            development=development,
            escalation=escalation,
            midpoint=midpoint,
            crisis=crisis,
            climax=climax,
            resolution=resolution,
            active_stage="setup",
        )
        return self.plot_repo.save_subplot(sub)

    def advance_subplot_stage(self, subplot_id: str, new_stage: str) -> SubplotPlan:
        cur = self.plot_repo.conn.execute("SELECT * FROM subplots WHERE id = ?", (subplot_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Subplot {subplot_id} not found")
        sub = SubplotPlan(**dict(row))
        sub.active_stage = new_stage
        return self.plot_repo.save_subplot(sub)
