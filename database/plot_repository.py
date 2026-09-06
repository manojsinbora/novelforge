"""
NovelForge AI — Story Architecture & Plot Repository
Phase 4: High-Performance SQLite Persistence for Long-Term Narrative Planning
"""
from __future__ import annotations
import sqlite3
import json
import uuid
import datetime
import os
from typing import List, Dict, Optional, Any

from novelforge.schemas.plot_models import (
    StoryMilestone, MainPlot, PlotThread, PlotThreadType, ThreadStatus, SubplotPlan,
    CharacterArcMilestone, CharacterArc, ArcType, Goal, GoalType, GoalStatus,
    ConflictParty, Conflict, ConflictType, MysteryClue, Mystery, MysteryStatus,
    Secret, StoryPromise, PromiseStatus, ForeshadowingSeed, ForeshadowingType,
    ForeshadowingQuality, PlotTwist, Reversal, ReversalType, BeatPlan, ScenePlan,
    ChapterPlan, ArcPlan, NarrativeDependency, NarrativeDebt, DebtSeverity,
    HookType, PlanConfidence
)


class PlotRepository:
    def __init__(self, db_path: str = "novelforge/database/novelforge.sqlite3", conn: Optional[sqlite3.Connection] = None):
        self.db_path = db_path
        if conn is not None:
            self.conn = conn
        else:
            if db_path != ":memory:":
                os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS main_plots (
                    id TEXT PRIMARY KEY,
                    story_id TEXT UNIQUE NOT NULL,
                    premise TEXT NOT NULL,
                    central_conflict TEXT DEFAULT '',
                    protagonist_goal TEXT DEFAULT '',
                    ultimate_antagonistic_force TEXT DEFAULT '',
                    central_stakes TEXT DEFAULT '',
                    thematic_question TEXT DEFAULT '',
                    desired_ending TEXT DEFAULT '',
                    turning_points_data TEXT DEFAULT '[]',
                    current_state TEXT DEFAULT 'ACTIVE',
                    unresolved_threads_data TEXT DEFAULT '[]',
                    updated_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS plot_threads (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    thread_type TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    importance REAL DEFAULT 5.0,
                    priority INTEGER DEFAULT 3,
                    status TEXT DEFAULT 'OPEN',
                    origin TEXT DEFAULT 'PROLOGUE',
                    related_characters_data TEXT DEFAULT '[]',
                    related_factions_data TEXT DEFAULT '[]',
                    related_locations_data TEXT DEFAULT '[]',
                    related_mysteries_data TEXT DEFAULT '[]',
                    related_promises_data TEXT DEFAULT '[]',
                    started_chapter INTEGER DEFAULT 1,
                    target_resolution_chapter INTEGER DEFAULT 50,
                    actual_resolution_chapter INTEGER,
                    notes TEXT DEFAULT '',
                    created_at TEXT,
                    updated_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS subplots (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    parent_thread_id TEXT NOT NULL,
                    setup TEXT DEFAULT '',
                    development TEXT DEFAULT '',
                    escalation TEXT DEFAULT '',
                    midpoint TEXT DEFAULT '',
                    crisis TEXT DEFAULT '',
                    climax TEXT DEFAULT '',
                    resolution TEXT DEFAULT '',
                    active_stage TEXT DEFAULT 'setup'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS character_arcs (
                    id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    story_id TEXT NOT NULL,
                    arc_type TEXT NOT NULL,
                    initial_state TEXT DEFAULT '',
                    internal_problem TEXT DEFAULT '',
                    want TEXT DEFAULT '',
                    need TEXT DEFAULT '',
                    pressure TEXT DEFAULT '',
                    transformation TEXT DEFAULT '',
                    final_state TEXT DEFAULT '',
                    beliefs_data TEXT DEFAULT '[]',
                    fears_data TEXT DEFAULT '[]',
                    desires_data TEXT DEFAULT '[]',
                    values_data TEXT DEFAULT '[]',
                    relationships_data TEXT DEFAULT '{}',
                    flaws_data TEXT DEFAULT '[]',
                    current_worldview TEXT DEFAULT '',
                    updated_at TEXT,
                    UNIQUE(character_id, story_id)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS character_arc_milestones (
                    id TEXT PRIMARY KEY,
                    arc_id TEXT NOT NULL,
                    chapter_number INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    character_id TEXT NOT NULL,
                    emotional_state_before TEXT DEFAULT '',
                    emotional_state_after TEXT DEFAULT '',
                    belief_shift TEXT DEFAULT '',
                    status TEXT DEFAULT 'PLANNED'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    id TEXT PRIMARY KEY,
                    character_id TEXT NOT NULL,
                    story_id TEXT NOT NULL,
                    description TEXT NOT NULL,
                    goal_type TEXT DEFAULT 'PERSONAL',
                    priority INTEGER DEFAULT 3,
                    motivation TEXT DEFAULT '',
                    deadline_chapter INTEGER,
                    obstacles_data TEXT DEFAULT '[]',
                    resources_data TEXT DEFAULT '[]',
                    progress REAL DEFAULT 0.0,
                    status TEXT DEFAULT 'ACTIVE',
                    consequences_data TEXT DEFAULT '[]'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS conflicts (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    conflict_type TEXT NOT NULL,
                    parties_data TEXT DEFAULT '[]',
                    objective TEXT DEFAULT '',
                    opposing_goals_data TEXT DEFAULT '{}',
                    stakes_data TEXT DEFAULT '{}',
                    resources_data TEXT DEFAULT '{}',
                    escalation_level INTEGER DEFAULT 1,
                    consequences_data TEXT DEFAULT '[]',
                    resolution_conditions_data TEXT DEFAULT '[]',
                    status TEXT DEFAULT 'ACTIVE'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS mysteries (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    question TEXT NOT NULL,
                    hidden_truth TEXT NOT NULL,
                    visible_clues_data TEXT DEFAULT '[]',
                    false_leads_data TEXT DEFAULT '[]',
                    true_leads_data TEXT DEFAULT '[]',
                    suspects_data TEXT DEFAULT '[]',
                    theories_data TEXT DEFAULT '[]',
                    reveal_plan TEXT DEFAULT '',
                    reveal_conditions_data TEXT DEFAULT '[]',
                    resolution TEXT DEFAULT '',
                    status TEXT DEFAULT 'UNSOLVED',
                    importance TEXT DEFAULT 'CORE',
                    intended_reader_suspicion TEXT DEFAULT '',
                    epistemic_knowledge_data TEXT DEFAULT '{}',
                    created_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS mystery_clues (
                    id TEXT PRIMARY KEY,
                    mystery_id TEXT NOT NULL,
                    clue_text TEXT NOT NULL,
                    chapter_introduced INTEGER NOT NULL,
                    location_id TEXT DEFAULT '',
                    discoverer_id TEXT DEFAULT '',
                    visibility TEXT DEFAULT 'PUBLIC',
                    interpretation TEXT DEFAULT '',
                    true_meaning TEXT DEFAULT '',
                    false_interpretations_data TEXT DEFAULT '[]',
                    importance TEXT DEFAULT 'MAJOR',
                    payoff_chapter INTEGER,
                    status TEXT DEFAULT 'DISCOVERED'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS secrets (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    secret_text TEXT NOT NULL,
                    owner_id TEXT NOT NULL,
                    truth TEXT NOT NULL,
                    who_knows_data TEXT DEFAULT '[]',
                    who_suspects_data TEXT DEFAULT '[]',
                    discovery_conditions TEXT DEFAULT '',
                    reveal_importance TEXT DEFAULT 'HIGH',
                    reveal_target TEXT DEFAULT '',
                    is_revealed INTEGER DEFAULT 0,
                    reveal_chapter INTEGER
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS story_promises (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    description TEXT NOT NULL,
                    promise_type TEXT NOT NULL,
                    introduced_chapter INTEGER NOT NULL,
                    importance TEXT DEFAULT 'HIGH',
                    expected_payoff_window INTEGER DEFAULT 30,
                    payoff_requirements_data TEXT DEFAULT '[]',
                    related_thread_id TEXT,
                    related_mystery_id TEXT,
                    status TEXT DEFAULT 'OPEN',
                    payoff_chapter INTEGER,
                    created_at TEXT
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS foreshadowing_seeds (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    seed_text TEXT NOT NULL,
                    foreshadowing_type TEXT NOT NULL,
                    target_event TEXT NOT NULL,
                    target_reveal TEXT DEFAULT '',
                    chapter_introduced INTEGER NOT NULL,
                    clue_strength REAL DEFAULT 0.5,
                    visibility TEXT DEFAULT 'BACKGROUND',
                    intended_interpretation TEXT DEFAULT '',
                    actual_meaning TEXT DEFAULT '',
                    payoff_window_end INTEGER DEFAULT 50,
                    status TEXT DEFAULT 'PLANTED',
                    quality TEXT DEFAULT 'PERFECTLY_TIMED'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS plot_twists (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    setup TEXT DEFAULT '',
                    hidden_truth TEXT NOT NULL,
                    reveal_text TEXT NOT NULL,
                    expected_reader_belief TEXT DEFAULT '',
                    actual_truth TEXT NOT NULL,
                    affected_characters_data TEXT DEFAULT '[]',
                    consequences_data TEXT DEFAULT '[]',
                    foreshadowing_ids_data TEXT DEFAULT '[]',
                    reveal_chapter INTEGER DEFAULT 1,
                    importance TEXT DEFAULT 'MAJOR',
                    surprise_rating REAL DEFAULT 8.5,
                    fairness_rating REAL DEFAULT 9.0
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS reversals (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    reversal_type TEXT NOT NULL,
                    trigger_chapter INTEGER NOT NULL,
                    affected_characters_data TEXT DEFAULT '[]',
                    setup_events_data TEXT DEFAULT '[]',
                    outcome_description TEXT DEFAULT '',
                    consequences_data TEXT DEFAULT '[]'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS arc_plans (
                    id TEXT PRIMARY KEY,
                    saga_id TEXT NOT NULL,
                    story_id TEXT NOT NULL,
                    arc_name TEXT NOT NULL,
                    sequence_order INTEGER DEFAULT 1,
                    start_chapter INTEGER DEFAULT 1,
                    end_chapter INTEGER DEFAULT 20,
                    arc_objective TEXT DEFAULT '',
                    central_conflict TEXT DEFAULT '',
                    primary_characters_data TEXT DEFAULT '[]',
                    secondary_characters_data TEXT DEFAULT '[]',
                    setting TEXT DEFAULT '',
                    opening_state TEXT DEFAULT '',
                    escalation_milestones_data TEXT DEFAULT '[]',
                    midpoint_reversal TEXT DEFAULT '',
                    major_reversal TEXT DEFAULT '',
                    climax TEXT DEFAULT '',
                    resolution TEXT DEFAULT '',
                    character_changes_data TEXT DEFAULT '{}',
                    power_changes_data TEXT DEFAULT '{}',
                    world_changes_data TEXT DEFAULT '[]',
                    open_threads_data TEXT DEFAULT '[]',
                    resolved_threads_data TEXT DEFAULT '[]',
                    future_hooks_data TEXT DEFAULT '[]',
                    arc_purpose_data TEXT DEFAULT '[]',
                    confidence TEXT DEFAULT 'HIGH_CONFIDENCE'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS chapter_plans (
                    id TEXT PRIMARY KEY,
                    arc_id TEXT NOT NULL,
                    chapter_number INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    chapter_objective TEXT DEFAULT '',
                    main_conflict TEXT DEFAULT '',
                    character_objectives_data TEXT DEFAULT '{}',
                    scenes_data TEXT DEFAULT '[]',
                    important_reveals_data TEXT DEFAULT '[]',
                    power_events_data TEXT DEFAULT '[]',
                    emotional_beats_data TEXT DEFAULT '[]',
                    mystery_clues_data TEXT DEFAULT '[]',
                    foreshadowing_seeds_data TEXT DEFAULT '[]',
                    promise_advancement_data TEXT DEFAULT '[]',
                    ending_hook TEXT DEFAULT '',
                    hook_type TEXT DEFAULT 'MYSTERY',
                    pacing_metrics_data TEXT DEFAULT '{}',
                    confidence TEXT DEFAULT 'HIGH_CONFIDENCE',
                    UNIQUE(arc_id, chapter_number)
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS scene_plans (
                    id TEXT PRIMARY KEY,
                    chapter_id TEXT NOT NULL,
                    sequence_order INTEGER DEFAULT 1,
                    title TEXT NOT NULL,
                    purpose TEXT DEFAULT '',
                    location_id TEXT DEFAULT '',
                    characters_present_data TEXT DEFAULT '[]',
                    primary_conflict TEXT DEFAULT '',
                    scene_goal TEXT DEFAULT '',
                    obstacle TEXT DEFAULT '',
                    information_revealed_data TEXT DEFAULT '[]',
                    emotional_change TEXT DEFAULT '',
                    power_change TEXT DEFAULT '',
                    relationship_change TEXT DEFAULT '',
                    world_change TEXT DEFAULT '',
                    mystery_change TEXT DEFAULT '',
                    promise_change TEXT DEFAULT '',
                    entry_state_data TEXT DEFAULT '{}',
                    exit_state_data TEXT DEFAULT '{}',
                    beats_data TEXT DEFAULT '[]'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS narrative_dependencies (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    target_type TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    dependency_type TEXT DEFAULT 'REQUIRES',
                    description TEXT DEFAULT ''
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS narrative_debts (
                    id TEXT PRIMARY KEY,
                    story_id TEXT NOT NULL,
                    debt_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    introduced_chapter INTEGER DEFAULT 1,
                    age_chapters INTEGER DEFAULT 0,
                    importance TEXT DEFAULT 'HIGH',
                    affected_entities_data TEXT DEFAULT '[]',
                    suggested_remedy TEXT DEFAULT ''
                );
            """)

    # =========================================================================
    # 1. MAIN PLOT
    # =========================================================================

    def save_main_plot(self, plot: MainPlot) -> MainPlot:
        with self.conn:
            tpoints_json = json.dumps([t.to_dict() if hasattr(t, "to_dict") else t for t in plot.turning_points])
            state_val = plot.current_state.value if hasattr(plot.current_state, "value") else str(plot.current_state)
            self.conn.execute("""
                INSERT OR REPLACE INTO main_plots (
                    id, story_id, premise, central_conflict, protagonist_goal,
                    ultimate_antagonistic_force, central_stakes, thematic_question,
                    desired_ending, turning_points_data, current_state, unresolved_threads_data, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plot.id, plot.story_id, plot.premise, plot.central_conflict, plot.protagonist_goal,
                plot.ultimate_antagonistic_force, plot.central_stakes, plot.thematic_question,
                plot.desired_ending, tpoints_json, state_val, json.dumps(plot.unresolved_threads),
                datetime.datetime.utcnow().isoformat()
            ))
        return plot

    def get_main_plot(self, story_id: str) -> Optional[MainPlot]:
        cur = self.conn.execute("SELECT * FROM main_plots WHERE story_id = ?", (story_id,))
        row = cur.fetchone()
        if not row:
            return None
        tpoints = [StoryMilestone.from_dict(t) for t in json.loads(row["turning_points_data"] or "[]")]
        return MainPlot(
            id=row["id"],
            story_id=row["story_id"],
            premise=row["premise"],
            central_conflict=row["central_conflict"],
            protagonist_goal=row["protagonist_goal"],
            ultimate_antagonistic_force=row["ultimate_antagonistic_force"],
            central_stakes=row["central_stakes"],
            thematic_question=row["thematic_question"],
            desired_ending=row["desired_ending"],
            turning_points=tpoints,
            current_state=row["current_state"],
            unresolved_threads=json.loads(row["unresolved_threads_data"] or "[]"),
            updated_at=row["updated_at"],
        )

    # =========================================================================
    # 2. PLOT THREADS & SUBPLOTS
    # =========================================================================

    def save_plot_thread(self, thread: PlotThread) -> PlotThread:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO plot_threads (
                    id, story_id, name, thread_type, description, importance, priority,
                    status, origin, related_characters_data, related_factions_data,
                    related_locations_data, related_mysteries_data, related_promises_data,
                    started_chapter, target_resolution_chapter, actual_resolution_chapter,
                    notes, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                thread.id, thread.story_id, thread.name,
                thread.thread_type.value if hasattr(thread.thread_type, "value") else str(thread.thread_type),
                thread.description, thread.importance, thread.priority,
                thread.status.value if hasattr(thread.status, "value") else str(thread.status),
                thread.origin, json.dumps(thread.related_characters),
                json.dumps(thread.related_factions), json.dumps(thread.related_locations),
                json.dumps(thread.related_mysteries), json.dumps(thread.related_promises),
                thread.started_chapter, thread.target_resolution_chapter,
                thread.actual_resolution_chapter, thread.notes,
                thread.created_at, datetime.datetime.utcnow().isoformat()
            ))
        return thread

    def get_plot_thread(self, thread_id: str) -> Optional[PlotThread]:
        cur = self.conn.execute("SELECT * FROM plot_threads WHERE id = ?", (thread_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_plot_thread(row)

    def get_threads_for_story(
        self,
        story_id: str,
        status: Optional[str] = None
    ) -> List[PlotThread]:
        if status:
            cur = self.conn.execute("SELECT * FROM plot_threads WHERE story_id = ? AND status = ? ORDER BY priority ASC, importance DESC", (story_id, status))
        else:
            cur = self.conn.execute("SELECT * FROM plot_threads WHERE story_id = ? ORDER BY priority ASC, importance DESC", (story_id,))
        return [self._row_to_plot_thread(r) for r in cur.fetchall()]

    def _row_to_plot_thread(self, row: sqlite3.Row) -> PlotThread:
        return PlotThread(
            id=row["id"],
            story_id=row["story_id"],
            name=row["name"],
            thread_type=row["thread_type"],
            description=row["description"],
            importance=row["importance"],
            priority=row["priority"],
            status=row["status"],
            origin=row["origin"],
            related_characters=json.loads(row["related_characters_data"] or "[]"),
            related_factions=json.loads(row["related_factions_data"] or "[]"),
            related_locations=json.loads(row["related_locations_data"] or "[]"),
            related_mysteries=json.loads(row["related_mysteries_data"] or "[]"),
            related_promises=json.loads(row["related_promises_data"] or "[]"),
            started_chapter=row["started_chapter"],
            target_resolution_chapter=row["target_resolution_chapter"],
            actual_resolution_chapter=row["actual_resolution_chapter"],
            notes=row["notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def save_subplot(self, subplot: SubplotPlan) -> SubplotPlan:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO subplots (
                    id, story_id, name, parent_thread_id, setup, development,
                    escalation, midpoint, crisis, climax, resolution, active_stage
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                subplot.id, subplot.story_id, subplot.name, subplot.parent_thread_id,
                subplot.setup, subplot.development, subplot.escalation, subplot.midpoint,
                subplot.crisis, subplot.climax, subplot.resolution, subplot.active_stage
            ))
        return subplot

    def get_subplots_for_story(self, story_id: str) -> List[SubplotPlan]:
        cur = self.conn.execute("SELECT * FROM subplots WHERE story_id = ?", (story_id,))
        return [SubplotPlan(**dict(r)) for r in cur.fetchall()]

    # =========================================================================
    # 3. CHARACTER ARCS & GOALS
    # =========================================================================

    def save_character_arc(self, arc: CharacterArc) -> CharacterArc:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO character_arcs (
                    id, character_id, story_id, arc_type, initial_state, internal_problem,
                    want, need, pressure, transformation, final_state, beliefs_data,
                    fears_data, desires_data, values_data, relationships_data,
                    flaws_data, current_worldview, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                arc.id, arc.character_id, arc.story_id,
                arc.arc_type.value if hasattr(arc.arc_type, "value") else str(arc.arc_type),
                arc.initial_state, arc.internal_problem, arc.want, arc.need, arc.pressure,
                arc.transformation, arc.final_state, json.dumps(arc.beliefs),
                json.dumps(arc.fears), json.dumps(arc.desires), json.dumps(arc.values),
                json.dumps(arc.relationships_trajectory), json.dumps(arc.flaws),
                arc.current_worldview, datetime.datetime.utcnow().isoformat()
            ))

            # Save associated milestones
            for m in arc.milestones:
                self.conn.execute("""
                    INSERT OR REPLACE INTO character_arc_milestones (
                        id, arc_id, chapter_number, title, description, character_id,
                        emotional_state_before, emotional_state_after, belief_shift, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    m.id, arc.id, m.chapter_number, m.title, m.description, m.character_id,
                    m.emotional_state_before, m.emotional_state_after, m.belief_shift, m.status
                ))
        return arc

    def get_character_arc(self, character_id: str, story_id: str) -> Optional[CharacterArc]:
        cur = self.conn.execute("SELECT * FROM character_arcs WHERE character_id = ? AND story_id = ?", (character_id, story_id))
        row = cur.fetchone()
        if not row:
            return None
        m_cur = self.conn.execute("SELECT * FROM character_arc_milestones WHERE arc_id = ? ORDER BY chapter_number ASC", (row["id"],))
        milestones = [CharacterArcMilestone(**dict(m)) for m in m_cur.fetchall()]
        return CharacterArc(
            id=row["id"],
            character_id=row["character_id"],
            story_id=row["story_id"],
            arc_type=row["arc_type"],
            initial_state=row["initial_state"],
            internal_problem=row["internal_problem"],
            want=row["want"],
            need=row["need"],
            pressure=row["pressure"],
            transformation=row["transformation"],
            final_state=row["final_state"],
            beliefs=json.loads(row["beliefs_data"] or "[]"),
            fears=json.loads(row["fears_data"] or "[]"),
            desires=json.loads(row["desires_data"] or "[]"),
            values=json.loads(row["values_data"] or "[]"),
            relationships_trajectory=json.loads(row["relationships_data"] or "{}"),
            flaws=json.loads(row["flaws_data"] or "[]"),
            current_worldview=row["current_worldview"],
            milestones=milestones,
            updated_at=row["updated_at"],
        )

    def save_goal(self, goal: Goal) -> Goal:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO goals (
                    id, character_id, story_id, description, goal_type, priority,
                    motivation, deadline_chapter, obstacles_data, resources_data,
                    progress, status, consequences_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                goal.id, goal.character_id, goal.story_id, goal.description,
                goal.goal_type.value if hasattr(goal.goal_type, "value") else str(goal.goal_type),
                goal.priority, goal.motivation, goal.deadline_chapter,
                json.dumps(goal.obstacles), json.dumps(goal.resources),
                goal.progress,
                goal.status.value if hasattr(goal.status, "value") else str(goal.status),
                json.dumps(goal.consequences)
            ))
        return goal

    def get_goals_for_character(self, character_id: str) -> List[Goal]:
        cur = self.conn.execute("SELECT * FROM goals WHERE character_id = ? ORDER BY priority ASC", (character_id,))
        return [self._row_to_goal(r) for r in cur.fetchall()]

    def _row_to_goal(self, row: sqlite3.Row) -> Goal:
        return Goal(
            id=row["id"],
            character_id=row["character_id"],
            story_id=row["story_id"],
            description=row["description"],
            goal_type=row["goal_type"],
            priority=row["priority"],
            motivation=row["motivation"],
            deadline_chapter=row["deadline_chapter"],
            obstacles=json.loads(row["obstacles_data"] or "[]"),
            resources=json.loads(row["resources_data"] or "[]"),
            progress=row["progress"],
            status=row["status"],
            consequences=json.loads(row["consequences_data"] or "[]"),
        )

    # =========================================================================
    # 4. CONFLICTS
    # =========================================================================

    def save_conflict(self, conflict: Conflict) -> Conflict:
        with self.conn:
            parties_json = json.dumps([p.to_dict() if hasattr(p, "to_dict") else p for p in conflict.parties])
            self.conn.execute("""
                INSERT OR REPLACE INTO conflicts (
                    id, story_id, title, conflict_type, parties_data, objective,
                    opposing_goals_data, stakes_data, resources_data, escalation_level,
                    consequences_data, resolution_conditions_data, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                conflict.id, conflict.story_id, conflict.title,
                conflict.conflict_type.value if hasattr(conflict.conflict_type, "value") else str(conflict.conflict_type),
                parties_json, conflict.objective, json.dumps(conflict.opposing_goals),
                json.dumps(conflict.stakes), json.dumps(conflict.resources),
                conflict.escalation_level, json.dumps(conflict.consequences),
                json.dumps(conflict.resolution_conditions), conflict.status
            ))
        return conflict

    def get_conflicts_for_story(self, story_id: str) -> List[Conflict]:
        cur = self.conn.execute("SELECT * FROM conflicts WHERE story_id = ? ORDER BY escalation_level DESC", (story_id,))
        conflicts = []
        for r in cur.fetchall():
            parties = [ConflictParty(**p) for p in json.loads(r["parties_data"] or "[]")]
            conflicts.append(Conflict(
                id=r["id"],
                story_id=r["story_id"],
                title=r["title"],
                conflict_type=r["conflict_type"],
                parties=parties,
                objective=r["objective"],
                opposing_goals=json.loads(r["opposing_goals_data"] or "{}"),
                stakes=json.loads(r["stakes_data"] or "{}"),
                resources=json.loads(r["resources_data"] or "{}"),
                escalation_level=r["escalation_level"],
                consequences=json.loads(r["consequences_data"] or "[]"),
                resolution_conditions=json.loads(r["resolution_conditions_data"] or "[]"),
                status=r["status"],
            ))
        return conflicts

    # =========================================================================
    # 5. MYSTERIES & CLUES
    # =========================================================================

    def save_mystery(self, mystery: Mystery) -> Mystery:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO mysteries (
                    id, story_id, title, question, hidden_truth, visible_clues_data,
                    false_leads_data, true_leads_data, suspects_data, theories_data,
                    reveal_plan, reveal_conditions_data, resolution, status,
                    importance, intended_reader_suspicion, epistemic_knowledge_data, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mystery.id, mystery.story_id, mystery.title, mystery.question,
                mystery.hidden_truth, json.dumps(mystery.visible_clues),
                json.dumps(mystery.false_leads), json.dumps(mystery.true_leads),
                json.dumps(mystery.suspects), json.dumps(mystery.theories),
                mystery.reveal_plan, json.dumps(mystery.reveal_conditions),
                mystery.resolution,
                mystery.status.value if hasattr(mystery.status, "value") else str(mystery.status),
                mystery.importance, mystery.intended_reader_suspicion,
                json.dumps(mystery.epistemic_knowledge), mystery.created_at
            ))
        return mystery

    def get_mystery(self, mystery_id: str) -> Optional[Mystery]:
        cur = self.conn.execute("SELECT * FROM mysteries WHERE id = ?", (mystery_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_mystery(row)

    def get_mysteries_for_story(self, story_id: str) -> List[Mystery]:
        cur = self.conn.execute("SELECT * FROM mysteries WHERE story_id = ? ORDER BY importance ASC", (story_id,))
        return [self._row_to_mystery(r) for r in cur.fetchall()]

    def _row_to_mystery(self, row: sqlite3.Row) -> Mystery:
        return Mystery(
            id=row["id"],
            story_id=row["story_id"],
            title=row["title"],
            question=row["question"],
            hidden_truth=row["hidden_truth"],
            visible_clues=json.loads(row["visible_clues_data"] or "[]"),
            false_leads=json.loads(row["false_leads_data"] or "[]"),
            true_leads=json.loads(row["true_leads_data"] or "[]"),
            suspects=json.loads(row["suspects_data"] or "[]"),
            theories=json.loads(row["theories_data"] or "[]"),
            reveal_plan=row["reveal_plan"],
            reveal_conditions=json.loads(row["reveal_conditions_data"] or "[]"),
            resolution=row["resolution"],
            status=row["status"],
            importance=row["importance"],
            intended_reader_suspicion=row["intended_reader_suspicion"],
            epistemic_knowledge=json.loads(row["epistemic_knowledge_data"] or "{}"),
            created_at=row["created_at"],
        )

    def save_clue(self, clue: MysteryClue) -> MysteryClue:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO mystery_clues (
                    id, mystery_id, clue_text, chapter_introduced, location_id,
                    discoverer_id, visibility, interpretation, true_meaning,
                    false_interpretations_data, importance, payoff_chapter, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                clue.id, clue.mystery_id, clue.clue_text, clue.chapter_introduced,
                clue.location_id, clue.discoverer_id, clue.visibility, clue.interpretation,
                clue.true_meaning, json.dumps(clue.false_interpretations), clue.importance,
                clue.payoff_chapter, clue.status
            ))
        return clue

    def get_clues_for_mystery(self, mystery_id: str) -> List[MysteryClue]:
        cur = self.conn.execute("SELECT * FROM mystery_clues WHERE mystery_id = ? ORDER BY chapter_introduced ASC", (mystery_id,))
        clues = []
        for r in cur.fetchall():
            clues.append(MysteryClue(
                id=r["id"],
                mystery_id=r["mystery_id"],
                clue_text=r["clue_text"],
                chapter_introduced=r["chapter_introduced"],
                location_id=r["location_id"],
                discoverer_id=r["discoverer_id"],
                visibility=r["visibility"],
                interpretation=r["interpretation"],
                true_meaning=r["true_meaning"],
                false_interpretations=json.loads(r["false_interpretations_data"] or "[]"),
                importance=r["importance"],
                payoff_chapter=r["payoff_chapter"],
                status=r["status"],
            ))
        return clues

    # =========================================================================
    # 6. PROMISES & PROMISE DEBT
    # =========================================================================

    def save_promise(self, promise: StoryPromise) -> StoryPromise:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO story_promises (
                    id, story_id, description, promise_type, introduced_chapter,
                    importance, expected_payoff_window, payoff_requirements_data,
                    related_thread_id, related_mystery_id, status, payoff_chapter, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                promise.id, promise.story_id, promise.description, promise.promise_type,
                promise.introduced_chapter, promise.importance, promise.expected_payoff_window,
                json.dumps(promise.payoff_requirements), promise.related_thread_id,
                promise.related_mystery_id,
                promise.status.value if hasattr(promise.status, "value") else str(promise.status),
                promise.payoff_chapter, promise.created_at
            ))
        return promise

    def get_promises_for_story(
        self,
        story_id: str,
        status: Optional[str] = None
    ) -> List[StoryPromise]:
        if status:
            cur = self.conn.execute("SELECT * FROM story_promises WHERE story_id = ? AND status = ? ORDER BY introduced_chapter ASC", (story_id, status))
        else:
            cur = self.conn.execute("SELECT * FROM story_promises WHERE story_id = ? ORDER BY introduced_chapter ASC", (story_id,))
        promises = []
        for r in cur.fetchall():
            promises.append(StoryPromise(
                id=r["id"],
                story_id=r["story_id"],
                description=r["description"],
                promise_type=r["promise_type"],
                introduced_chapter=r["introduced_chapter"],
                importance=r["importance"],
                expected_payoff_window=r["expected_payoff_window"],
                payoff_requirements=json.loads(r["payoff_requirements_data"] or "[]"),
                related_thread_id=r["related_thread_id"],
                related_mystery_id=r["related_mystery_id"],
                status=r["status"],
                payoff_chapter=r["payoff_chapter"],
                created_at=r["created_at"],
            ))
        return promises

    # =========================================================================
    # 7. FORESHADOWING, TWISTS & REVERSALS
    # =========================================================================

    def save_foreshadowing_seed(self, seed: ForeshadowingSeed) -> ForeshadowingSeed:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO foreshadowing_seeds (
                    id, story_id, seed_text, foreshadowing_type, target_event,
                    target_reveal, chapter_introduced, clue_strength, visibility,
                    intended_interpretation, actual_meaning, payoff_window_end,
                    status, quality
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                seed.id, seed.story_id, seed.seed_text,
                seed.foreshadowing_type.value if hasattr(seed.foreshadowing_type, "value") else str(seed.foreshadowing_type),
                seed.target_event, seed.target_reveal, seed.chapter_introduced,
                seed.clue_strength, seed.visibility, seed.intended_interpretation,
                seed.actual_meaning, seed.payoff_window_end, seed.status,
                seed.quality.value if hasattr(seed.quality, "value") else str(seed.quality)
            ))
        return seed

    def get_foreshadowing_for_story(self, story_id: str) -> List[ForeshadowingSeed]:
        cur = self.conn.execute("SELECT * FROM foreshadowing_seeds WHERE story_id = ? ORDER BY chapter_introduced ASC", (story_id,))
        seeds = []
        for r in cur.fetchall():
            seeds.append(ForeshadowingSeed(
                id=r["id"],
                story_id=r["story_id"],
                seed_text=r["seed_text"],
                foreshadowing_type=r["foreshadowing_type"],
                target_event=r["target_event"],
                target_reveal=r["target_reveal"],
                chapter_introduced=r["chapter_introduced"],
                clue_strength=r["clue_strength"],
                visibility=r["visibility"],
                intended_interpretation=r["intended_interpretation"],
                actual_meaning=r["actual_meaning"],
                payoff_window_end=r["payoff_window_end"],
                status=r["status"],
                quality=r["quality"],
            ))
        return seeds

    def save_twist(self, twist: PlotTwist) -> PlotTwist:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO plot_twists (
                    id, story_id, title, setup, hidden_truth, reveal_text,
                    expected_reader_belief, actual_truth, affected_characters_data,
                    consequences_data, foreshadowing_ids_data, reveal_chapter,
                    importance, surprise_rating, fairness_rating
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                twist.id, twist.story_id, twist.title, twist.setup, twist.hidden_truth,
                twist.reveal_text, twist.expected_reader_belief, twist.actual_truth,
                json.dumps(twist.affected_characters), json.dumps(twist.consequences),
                json.dumps(twist.foreshadowing_ids), twist.reveal_chapter,
                twist.importance, twist.surprise_rating, twist.fairness_rating
            ))
        return twist

    def get_twists_for_story(self, story_id: str) -> List[PlotTwist]:
        cur = self.conn.execute("SELECT * FROM plot_twists WHERE story_id = ? ORDER BY reveal_chapter ASC", (story_id,))
        twists = []
        for r in cur.fetchall():
            twists.append(PlotTwist(
                id=r["id"],
                story_id=r["story_id"],
                title=r["title"],
                setup=r["setup"],
                hidden_truth=r["hidden_truth"],
                reveal_text=r["reveal_text"],
                expected_reader_belief=r["expected_reader_belief"],
                actual_truth=r["actual_truth"],
                affected_characters=json.loads(r["affected_characters_data"] or "[]"),
                consequences=json.loads(r["consequences_data"] or "[]"),
                foreshadowing_ids=json.loads(r["foreshadowing_ids_data"] or "[]"),
                reveal_chapter=r["reveal_chapter"],
                importance=r["importance"],
                surprise_rating=r["surprise_rating"],
                fairness_rating=r["fairness_rating"],
            ))
        return twists

    # =========================================================================
    # 8. ARC & CHAPTER PLANS
    # =========================================================================

    def save_arc_plan(self, plan: ArcPlan) -> ArcPlan:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO arc_plans (
                    id, saga_id, story_id, arc_name, sequence_order, start_chapter, end_chapter,
                    arc_objective, central_conflict, primary_characters_data, secondary_characters_data,
                    setting, opening_state, escalation_milestones_data, midpoint_reversal, major_reversal,
                    climax, resolution, character_changes_data, power_changes_data, world_changes_data,
                    open_threads_data, resolved_threads_data, future_hooks_data, arc_purpose_data, confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan.id, plan.saga_id, plan.story_id, plan.arc_name, plan.sequence_order,
                plan.start_chapter, plan.end_chapter, plan.arc_objective, plan.central_conflict,
                json.dumps(plan.primary_characters), json.dumps(plan.secondary_characters),
                plan.setting, plan.opening_state, json.dumps(plan.escalation_milestones),
                plan.midpoint_reversal, plan.major_reversal, plan.climax, plan.resolution,
                json.dumps(plan.character_changes), json.dumps(plan.power_changes),
                json.dumps(plan.world_changes), json.dumps(plan.open_threads),
                json.dumps(plan.resolved_threads), json.dumps(plan.future_hooks),
                json.dumps(plan.arc_purpose),
                plan.confidence.value if hasattr(plan.confidence, "value") else str(plan.confidence)
            ))
        return plan

    def get_arc_plan(self, arc_id: str) -> Optional[ArcPlan]:
        cur = self.conn.execute("SELECT * FROM arc_plans WHERE id = ?", (arc_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_arc_plan(row)

    def get_arc_plans_for_story(self, story_id: str) -> List[ArcPlan]:
        cur = self.conn.execute("SELECT * FROM arc_plans WHERE story_id = ? ORDER BY sequence_order ASC", (story_id,))
        return [self._row_to_arc_plan(r) for r in cur.fetchall()]

    def _row_to_arc_plan(self, row: sqlite3.Row) -> ArcPlan:
        return ArcPlan(
            id=row["id"],
            saga_id=row["saga_id"],
            story_id=row["story_id"],
            arc_name=row["arc_name"],
            sequence_order=row["sequence_order"],
            start_chapter=row["start_chapter"],
            end_chapter=row["end_chapter"],
            arc_objective=row["arc_objective"],
            central_conflict=row["central_conflict"],
            primary_characters=json.loads(row["primary_characters_data"] or "[]"),
            secondary_characters=json.loads(row["secondary_characters_data"] or "[]"),
            setting=row["setting"],
            opening_state=row["opening_state"],
            escalation_milestones=json.loads(row["escalation_milestones_data"] or "[]"),
            midpoint_reversal=row["midpoint_reversal"],
            major_reversal=row["major_reversal"],
            climax=row["climax"],
            resolution=row["resolution"],
            character_changes=json.loads(row["character_changes_data"] or "{}"),
            power_changes=json.loads(row["power_changes_data"] or "{}"),
            world_changes=json.loads(row["world_changes_data"] or "[]"),
            open_threads=json.loads(row["open_threads_data"] or "[]"),
            resolved_threads=json.loads(row["resolved_threads_data"] or "[]"),
            future_hooks=json.loads(row["future_hooks_data"] or "[]"),
            arc_purpose=json.loads(row["arc_purpose_data"] or "[]"),
            confidence=row["confidence"],
        )

    def save_chapter_plan(self, plan: ChapterPlan) -> ChapterPlan:
        with self.conn:
            scenes_json = json.dumps([s.to_dict() if hasattr(s, "to_dict") else s for s in plan.scenes])
            self.conn.execute("""
                INSERT OR REPLACE INTO chapter_plans (
                    id, arc_id, chapter_number, title, chapter_objective, main_conflict,
                    character_objectives_data, scenes_data, important_reveals_data,
                    power_events_data, emotional_beats_data, mystery_clues_data,
                    foreshadowing_seeds_data, promise_advancement_data, ending_hook,
                    hook_type, pacing_metrics_data, confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                plan.id, plan.arc_id, plan.chapter_number, plan.title,
                plan.chapter_objective, plan.main_conflict,
                json.dumps(plan.character_objectives), scenes_json,
                json.dumps(plan.important_reveals), json.dumps(plan.power_events),
                json.dumps(plan.emotional_beats), json.dumps(plan.mystery_clues),
                json.dumps(plan.foreshadowing_seeds), json.dumps(plan.promise_advancement),
                plan.ending_hook,
                plan.hook_type.value if hasattr(plan.hook_type, "value") else str(plan.hook_type),
                json.dumps(plan.pacing_metrics),
                plan.confidence.value if hasattr(plan.confidence, "value") else str(plan.confidence)
            ))
        return plan

    def get_chapter_plan(self, chapter_number: int, arc_id: Optional[str] = None) -> Optional[ChapterPlan]:
        if arc_id:
            cur = self.conn.execute("SELECT * FROM chapter_plans WHERE chapter_number = ? AND arc_id = ?", (chapter_number, arc_id))
        else:
            cur = self.conn.execute("SELECT * FROM chapter_plans WHERE chapter_number = ? LIMIT 1", (chapter_number,))
        row = cur.fetchone()
        if not row:
            return None
        raw_scenes = json.loads(row["scenes_data"] or "[]")
        scenes = [ScenePlan.from_dict(s) for s in raw_scenes]
        return ChapterPlan(
            id=row["id"],
            arc_id=row["arc_id"],
            chapter_number=row["chapter_number"],
            title=row["title"],
            chapter_objective=row["chapter_objective"],
            main_conflict=row["main_conflict"],
            character_objectives=json.loads(row["character_objectives_data"] or "{}"),
            scenes=scenes,
            important_reveals=json.loads(row["important_reveals_data"] or "[]"),
            power_events=json.loads(row["power_events_data"] or "[]"),
            emotional_beats=json.loads(row["emotional_beats_data"] or "[]"),
            mystery_clues=json.loads(row["mystery_clues_data"] or "[]"),
            foreshadowing_seeds=json.loads(row["foreshadowing_seeds_data"] or "[]"),
            promise_advancement=json.loads(row["promise_advancement_data"] or "[]"),
            ending_hook=row["ending_hook"],
            hook_type=row["hook_type"],
            pacing_metrics=json.loads(row["pacing_metrics_data"] or "{}"),
            confidence=row["confidence"],
        )

    # =========================================================================
    # 9. DEPENDENCIES & DEBTS
    # =========================================================================

    def save_dependency(self, dep: NarrativeDependency) -> NarrativeDependency:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO narrative_dependencies (
                    id, story_id, source_type, source_id, target_type, target_id,
                    dependency_type, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dep.id, dep.story_id, dep.source_type, dep.source_id,
                dep.target_type, dep.target_id, dep.dependency_type, dep.description
            ))
        return dep

    def get_dependencies_for_target(self, target_type: str, target_id: str) -> List[NarrativeDependency]:
        cur = self.conn.execute("SELECT * FROM narrative_dependencies WHERE target_type = ? AND target_id = ?", (target_type, target_id))
        return [NarrativeDependency(**dict(r)) for r in cur.fetchall()]

    def get_downstream_dependencies(self, source_type: str, source_id: str) -> List[NarrativeDependency]:
        cur = self.conn.execute("SELECT * FROM narrative_dependencies WHERE source_type = ? AND source_id = ?", (source_type, source_id))
        return [NarrativeDependency(**dict(r)) for r in cur.fetchall()]

    def save_debt(self, debt: NarrativeDebt) -> NarrativeDebt:
        with self.conn:
            self.conn.execute("""
                INSERT OR REPLACE INTO narrative_debts (
                    id, story_id, debt_type, severity, title, description,
                    introduced_chapter, age_chapters, importance,
                    affected_entities_data, suggested_remedy
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                debt.id, debt.story_id, debt.debt_type,
                debt.severity.value if hasattr(debt.severity, "value") else str(debt.severity),
                debt.title, debt.description, debt.introduced_chapter,
                debt.age_chapters, debt.importance,
                json.dumps(debt.affected_entities), debt.suggested_remedy
            ))
        return debt

    def get_debts_for_story(self, story_id: str) -> List[NarrativeDebt]:
        cur = self.conn.execute("SELECT * FROM narrative_debts WHERE story_id = ? ORDER BY age_chapters DESC", (story_id,))
        debts = []
        for r in cur.fetchall():
            debts.append(NarrativeDebt(
                id=r["id"],
                story_id=r["story_id"],
                debt_type=r["debt_type"],
                severity=r["severity"],
                title=r["title"],
                description=r["description"],
                introduced_chapter=r["introduced_chapter"],
                age_chapters=r["age_chapters"],
                importance=r["importance"],
                affected_entities=json.loads(r["affected_entities_data"] or "[]"),
                suggested_remedy=r["suggested_remedy"],
            ))
        return debts
