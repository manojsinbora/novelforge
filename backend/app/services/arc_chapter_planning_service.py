"""
NovelForge AI — Arc & Chapter Planning Service
Phase 4: Hierarchical Planning Horizons (Series -> Saga -> Arc -> Chapter -> Scene -> Beat)
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any, Tuple
import uuid
import datetime
import json

from novelforge.database.plot_repository import PlotRepository
from novelforge.schemas.plot_models import (
    ArcPlan, ChapterPlan, ScenePlan, BeatPlan, HookType, PlanConfidence, PlanningHorizon
)


class ArcChapterPlanningService:
    def __init__(self, plot_repo: PlotRepository):
        self.plot_repo = plot_repo

    # =========================================================================
    # 1. ARC BLUEPRINTING
    # =========================================================================

    def create_arc_plan(
        self,
        saga_id: str,
        story_id: str,
        arc_name: str,
        sequence_order: int,
        start_chapter: int,
        end_chapter: int,
        arc_objective: str,
        central_conflict: str,
        primary_characters: Optional[List[str]] = None,
        secondary_characters: Optional[List[str]] = None,
        setting: str = "",
        opening_state: str = "",
        escalation_milestones: Optional[List[str]] = None,
        midpoint_reversal: str = "",
        major_reversal: str = "",
        climax: str = "",
        resolution: str = "",
        character_changes: Optional[Dict[str, str]] = None,
        power_changes: Optional[Dict[str, str]] = None,
        world_changes: Optional[List[str]] = None,
        open_threads: Optional[List[str]] = None,
        resolved_threads: Optional[List[str]] = None,
        future_hooks: Optional[List[str]] = None,
        arc_purpose: Optional[List[str]] = None,
        confidence: PlanConfidence = PlanConfidence.HIGH_CONFIDENCE
    ) -> ArcPlan:
        plan = ArcPlan(
            id=str(uuid.uuid4()),
            saga_id=saga_id,
            story_id=story_id,
            arc_name=arc_name,
            sequence_order=sequence_order,
            start_chapter=start_chapter,
            end_chapter=end_chapter,
            arc_objective=arc_objective,
            central_conflict=central_conflict,
            primary_characters=primary_characters or [],
            secondary_characters=secondary_characters or [],
            setting=setting,
            opening_state=opening_state,
            escalation_milestones=escalation_milestones or [],
            midpoint_reversal=midpoint_reversal,
            major_reversal=major_reversal,
            climax=climax,
            resolution=resolution,
            character_changes=character_changes or {},
            power_changes=power_changes or {},
            world_changes=world_changes or [],
            open_threads=open_threads or [],
            resolved_threads=resolved_threads or [],
            future_hooks=future_hooks or [],
            arc_purpose=arc_purpose or ["character_development", "power_progression"],
            confidence=confidence,
        )
        return self.plot_repo.save_arc_plan(plan)

    def get_arc_plan(self, arc_id: str) -> Optional[ArcPlan]:
        return self.plot_repo.get_arc_plan(arc_id)

    def get_arc_plans_for_story(self, story_id: str) -> List[ArcPlan]:
        return self.plot_repo.get_arc_plans_for_story(story_id)

    # =========================================================================
    # 2. CHAPTER BLUEPRINTING
    # =========================================================================

    def create_chapter_plan(
        self,
        arc_id: str,
        chapter_number: int,
        title: str,
        chapter_objective: str,
        main_conflict: str,
        character_objectives: Optional[Dict[str, str]] = None,
        scenes: Optional[List[ScenePlan]] = None,
        important_reveals: Optional[List[str]] = None,
        power_events: Optional[List[str]] = None,
        emotional_beats: Optional[List[str]] = None,
        mystery_clues: Optional[List[str]] = None,
        foreshadowing_seeds: Optional[List[str]] = None,
        promise_advancement: Optional[List[str]] = None,
        ending_hook: str = "",
        hook_type: HookType = HookType.MYSTERY,
        pacing_metrics: Optional[Dict[str, float]] = None,
        confidence: PlanConfidence = PlanConfidence.HIGH_CONFIDENCE
    ) -> ChapterPlan:
        plan = ChapterPlan(
            id=str(uuid.uuid4()),
            arc_id=arc_id,
            chapter_number=chapter_number,
            title=title,
            chapter_objective=chapter_objective,
            main_conflict=main_conflict,
            character_objectives=character_objectives or {},
            scenes=scenes or [],
            important_reveals=important_reveals or [],
            power_events=power_events or [],
            emotional_beats=emotional_beats or [],
            mystery_clues=mystery_clues or [],
            foreshadowing_seeds=foreshadowing_seeds or [],
            promise_advancement=promise_advancement or [],
            ending_hook=ending_hook,
            hook_type=hook_type,
            pacing_metrics=pacing_metrics or {"action": 0.4, "dialogue": 0.3, "mystery": 0.3},
            confidence=confidence,
        )
        return self.plot_repo.save_chapter_plan(plan)

    def get_chapter_plan(self, chapter_number: int, arc_id: Optional[str] = None) -> Optional[ChapterPlan]:
        return self.plot_repo.get_chapter_plan(chapter_number=chapter_number, arc_id=arc_id)

    # =========================================================================
    # 3. SCENE BLUEPRINTING & TRANSITION VALIDATION
    # =========================================================================

    def create_scene_plan(
        self,
        chapter_id: str,
        sequence_order: int,
        title: str,
        purpose: str,
        location_id: str = "",
        characters_present: Optional[List[str]] = None,
        primary_conflict: str = "",
        scene_goal: str = "",
        obstacle: str = "",
        information_revealed: Optional[List[str]] = None,
        emotional_change: str = "",
        power_change: str = "",
        relationship_change: str = "",
        world_change: str = "",
        mystery_change: str = "",
        promise_change: str = "",
        entry_state: Optional[Dict[str, Any]] = None,
        exit_state: Optional[Dict[str, Any]] = None,
        beats: Optional[List[BeatPlan]] = None,
    ) -> ScenePlan:
        scene = ScenePlan(
            id=str(uuid.uuid4()),
            chapter_id=chapter_id,
            sequence_order=sequence_order,
            title=title,
            purpose=purpose,
            location_id=location_id,
            characters_present=characters_present or [],
            primary_conflict=primary_conflict,
            scene_goal=scene_goal,
            obstacle=obstacle,
            information_revealed=information_revealed or [],
            emotional_change=emotional_change,
            power_change=power_change,
            relationship_change=relationship_change,
            world_change=world_change,
            mystery_change=mystery_change,
            promise_change=promise_change,
            entry_state=entry_state or {},
            exit_state=exit_state or {},
            beats=beats or [],
        )
        with self.plot_repo.conn:
            beats_json = json.dumps([b.to_dict() if hasattr(b, "to_dict") else b for b in scene.beats])
            self.plot_repo.conn.execute("""
                INSERT OR REPLACE INTO scene_plans (
                    id, chapter_id, sequence_order, title, purpose, location_id,
                    characters_present_data, primary_conflict, scene_goal, obstacle,
                    information_revealed_data, emotional_change, power_change,
                    relationship_change, world_change, mystery_change, promise_change,
                    entry_state_data, exit_state_data, beats_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                scene.id, scene.chapter_id, scene.sequence_order, scene.title, scene.purpose,
                scene.location_id, json.dumps(scene.characters_present), scene.primary_conflict,
                scene.scene_goal, scene.obstacle, json.dumps(scene.information_revealed),
                scene.emotional_change, scene.power_change, scene.relationship_change,
                scene.world_change, scene.mystery_change, scene.promise_change,
                json.dumps(scene.entry_state), json.dumps(scene.exit_state), beats_json
            ))
        return scene

    def validate_scene_transition(
        self,
        scene_a: ScenePlan,
        scene_b: ScenePlan
    ) -> Tuple[bool, List[str]]:
        """
        Validates continuity between consecutive scenes:
        Compares exit_state of Scene A with entry_state of Scene B.
        """
        anomalies = []
        exit_a = scene_a.exit_state or {}
        entry_b = scene_b.entry_state or {}

        # 1. Location Continuity
        loc_a = exit_a.get("location_id") or scene_a.location_id
        loc_b = entry_b.get("location_id") or scene_b.location_id
        if loc_a and loc_b and loc_a != loc_b:
            # Requires explicit travel note in entry_state
            if not entry_b.get("travel_elapsed") and not entry_b.get("transition_explained"):
                anomalies.append(f"UNEXPLAINED_SPATIAL_JUMP: Scene {scene_a.sequence_order} ends at '{loc_a}', but Scene {scene_b.sequence_order} begins at '{loc_b}' without travel transition.")

        # 2. Condition / Injury Continuity
        injuries_a = exit_a.get("active_injuries", [])
        injuries_b = entry_b.get("active_injuries", [])
        for inj in injuries_a:
            if inj not in injuries_b and not entry_b.get("healed"):
                anomalies.append(f"MIRACULOUS_HEALING: Character injury '{inj}' vanished between Scene {scene_a.sequence_order} and Scene {scene_b.sequence_order} without healing event.")

        # 3. Character Presence Continuity
        chars_a = set(scene_a.characters_present)
        chars_b = set(scene_b.characters_present)
        disappeared = exit_a.get("characters_departed", [])
        for ch in chars_a - chars_b:
            if ch not in disappeared and not entry_b.get("characters_arrived"):
                # Warning only
                pass

        is_valid = len(anomalies) == 0
        return is_valid, anomalies

    # =========================================================================
    # 4. PLANNING HORIZONS
    # =========================================================================

    def get_planning_horizons(
        self,
        story_id: str,
        current_chapter: int
    ) -> Dict[str, Any]:
        """
        Returns structured content mapped across the 5 canonical horizons:
        - Horizon 1 (Current): Chapters current to current+4 (Scene/Beat resolution)
        - Horizon 2 (Near): Chapters current+5 to current+29 (Chapter blueprints)
        - Horizon 3 (Medium): Chapters current+30 to current+149 (Arc plans)
        - Horizon 4 (Long): Chapters current+150 to current+499 (Saga milestones)
        - Horizon 5 (Distant): Chapters current+500+ (Strategic story milestones)
        """
        arcs = self.get_arc_plans_for_story(story_id)
        main_plot = self.plot_repo.get_main_plot(story_id)

        h1_chapters = []
        for ch in range(current_chapter, current_chapter + 5):
            cp = self.get_chapter_plan(ch)
            if cp:
                h1_chapters.append(cp.to_dict())

        h2_chapters = []
        for ch in range(current_chapter + 5, current_chapter + 30):
            cp = self.get_chapter_plan(ch)
            if cp:
                h2_chapters.append(cp.to_dict())

        h3_arcs = [a.to_dict() for a in arcs if a.start_chapter >= current_chapter + 30 and a.end_chapter < current_chapter + 150]

        h4_sagas = []
        if main_plot:
            h4_sagas = [
                m.to_dict() for m in main_plot.turning_points
                if current_chapter + 150 <= m.approximate_chapter < current_chapter + 500
            ]
            h5_distant = [
                m.to_dict() for m in main_plot.turning_points
                if m.approximate_chapter >= current_chapter + 500
            ]
        else:
            h5_distant = []

        return {
            "current_chapter": current_chapter,
            "horizon_1_current": {"range": f"Chapters {current_chapter}–{current_chapter+4}", "items": h1_chapters, "resolution": "HIGH (Scene & Beat level)"},
            "horizon_2_near": {"range": f"Chapters {current_chapter+5}–{current_chapter+29}", "items": h2_chapters, "resolution": "MEDIUM-HIGH (Chapter Blueprint level)"},
            "horizon_3_medium": {"range": f"Chapters {current_chapter+30}–{current_chapter+149}", "items": h3_arcs, "resolution": "MEDIUM (Arc level)"},
            "horizon_4_long": {"range": f"Chapters {current_chapter+150}–{current_chapter+499}", "items": h4_sagas, "resolution": "LOW-MEDIUM (Saga level)"},
            "horizon_5_distant": {"range": f"Chapters {current_chapter+500}+", "items": h5_distant, "resolution": "LOW (Strategic Milestones)"},
        }
