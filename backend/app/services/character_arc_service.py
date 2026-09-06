"""
NovelForge AI — Character Arc & Goal Engine
Phase 4: 17 Character Arc Archetypes, Transformation Milestones & Goal Lifecycle
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any
import uuid
import datetime

from novelforge.database.plot_repository import PlotRepository
from novelforge.schemas.plot_models import (
    CharacterArc, CharacterArcMilestone, ArcType, Goal, GoalType, GoalStatus
)


class CharacterArcService:
    def __init__(self, plot_repo: PlotRepository):
        self.plot_repo = plot_repo

    def create_character_arc(
        self,
        character_id: str,
        story_id: str,
        arc_type: ArcType,
        initial_state: str,
        internal_problem: str,
        want: str,
        need: str,
        pressure: str,
        transformation: str,
        final_state: str,
        beliefs: Optional[List[str]] = None,
        fears: Optional[List[str]] = None,
        desires: Optional[List[str]] = None,
        values: Optional[List[str]] = None,
        relationships_trajectory: Optional[Dict[str, str]] = None,
        flaws: Optional[List[str]] = None,
        current_worldview: str = "",
    ) -> CharacterArc:
        arc = CharacterArc(
            id=str(uuid.uuid4()),
            character_id=character_id,
            story_id=story_id,
            arc_type=arc_type,
            initial_state=initial_state,
            internal_problem=internal_problem,
            want=want,
            need=need,
            pressure=pressure,
            transformation=transformation,
            final_state=final_state,
            beliefs=beliefs or [],
            fears=fears or [],
            desires=desires or [],
            values=values or [],
            relationships_trajectory=relationships_trajectory or {},
            flaws=flaws or [],
            current_worldview=current_worldview or initial_state,
            milestones=[],
        )
        return self.plot_repo.save_character_arc(arc)

    def add_arc_milestone(
        self,
        arc_id: str,
        chapter_number: int,
        title: str,
        description: str,
        character_id: str,
        emotional_state_before: str = "",
        emotional_state_after: str = "",
        belief_shift: str = "",
        status: str = "PLANNED"
    ) -> CharacterArcMilestone:
        ms = CharacterArcMilestone(
            id=str(uuid.uuid4()),
            arc_id=arc_id,
            chapter_number=chapter_number,
            title=title,
            description=description,
            character_id=character_id,
            emotional_state_before=emotional_state_before,
            emotional_state_after=emotional_state_after,
            belief_shift=belief_shift,
            status=status,
        )
        with self.plot_repo.conn:
            self.plot_repo.conn.execute("""
                INSERT OR REPLACE INTO character_arc_milestones (
                    id, arc_id, chapter_number, title, description, character_id,
                    emotional_state_before, emotional_state_after, belief_shift, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                ms.id, ms.arc_id, ms.chapter_number, ms.title, ms.description, ms.character_id,
                ms.emotional_state_before, ms.emotional_state_after, ms.belief_shift, ms.status
            ))
        return ms

    def get_character_arc(self, character_id: str, story_id: str) -> Optional[CharacterArc]:
        return self.plot_repo.get_character_arc(character_id, story_id)

    # =========================================================================
    # GOALS
    # =========================================================================

    def create_goal(
        self,
        character_id: str,
        story_id: str,
        description: str,
        goal_type: GoalType = GoalType.PERSONAL,
        priority: int = 3,
        motivation: str = "",
        deadline_chapter: Optional[int] = None,
        obstacles: Optional[List[str]] = None,
        resources: Optional[List[str]] = None,
        consequences: Optional[List[str]] = None,
    ) -> Goal:
        goal = Goal(
            id=str(uuid.uuid4()),
            character_id=character_id,
            story_id=story_id,
            description=description,
            goal_type=goal_type,
            priority=priority,
            motivation=motivation,
            deadline_chapter=deadline_chapter,
            obstacles=obstacles or [],
            resources=resources or [],
            progress=0.0,
            status=GoalStatus.ACTIVE,
            consequences=consequences or [],
        )
        return self.plot_repo.save_goal(goal)

    def update_goal_progress(
        self,
        goal_id: str,
        progress: float,
        status: Optional[GoalStatus] = None
    ) -> Goal:
        cur = self.plot_repo.conn.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Goal {goal_id} not found")
        goal = self.plot_repo._row_to_goal(row)
        goal.progress = min(1.0, max(0.0, progress))
        if status is not None:
            goal.status = status
        elif goal.progress >= 1.0:
            goal.status = GoalStatus.COMPLETED
        return self.plot_repo.save_goal(goal)

    def get_goals_for_character(self, character_id: str) -> List[Goal]:
        return self.plot_repo.get_goals_for_character(character_id)
