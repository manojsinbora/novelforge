"""
NovelForge AI — Foreshadowing, Twist & Reversal Engine
Phase 4: Clue Planting, Fair-Play Twist Evaluation & Narrative Reversals
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any
import uuid
import datetime

from novelforge.database.plot_repository import PlotRepository
from novelforge.schemas.plot_models import (
    ForeshadowingSeed, ForeshadowingType, ForeshadowingQuality, PlotTwist,
    Reversal, ReversalType
)


class ForeshadowingTwistService:
    def __init__(self, plot_repo: PlotRepository):
        self.plot_repo = plot_repo

    # =========================================================================
    # 1. FORESHADOWING
    # =========================================================================

    def plant_seed(
        self,
        story_id: str,
        seed_text: str,
        foreshadowing_type: ForeshadowingType,
        target_event: str,
        target_reveal: str,
        chapter_introduced: int,
        clue_strength: float = 0.5,
        visibility: str = "BACKGROUND",
        intended_interpretation: str = "",
        actual_meaning: str = "",
        payoff_window_end: int = 50,
    ) -> ForeshadowingSeed:
        # Determine initial quality based on clue strength and visibility
        quality = ForeshadowingQuality.PERFECTLY_TIMED
        if clue_strength > 0.85:
            quality = ForeshadowingQuality.TOO_OBVIOUS
        elif clue_strength < 0.15:
            quality = ForeshadowingQuality.TOO_SUBTLE

        seed = ForeshadowingSeed(
            id=str(uuid.uuid4()),
            story_id=story_id,
            seed_text=seed_text,
            foreshadowing_type=foreshadowing_type,
            target_event=target_event,
            target_reveal=target_reveal,
            chapter_introduced=chapter_introduced,
            clue_strength=clue_strength,
            visibility=visibility,
            intended_interpretation=intended_interpretation,
            actual_meaning=actual_meaning,
            payoff_window_end=payoff_window_end,
            status="PLANTED",
            quality=quality,
        )
        return self.plot_repo.save_foreshadowing_seed(seed)

    def evaluate_foreshadowing_quality(self, seed_id: str) -> Dict[str, Any]:
        seeds = [s for s in self.plot_repo.get_foreshadowing_for_story("") if s.id == seed_id]
        if not seeds:
            cur = self.plot_repo.conn.execute("SELECT * FROM foreshadowing_seeds WHERE id = ?", (seed_id,))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Foreshadowing seed {seed_id} not found")
            seed = ForeshadowingSeed(
                id=row["id"], story_id=row["story_id"], seed_text=row["seed_text"],
                foreshadowing_type=row["foreshadowing_type"], target_event=row["target_event"],
                target_reveal=row["target_reveal"], chapter_introduced=row["chapter_introduced"],
                clue_strength=row["clue_strength"], visibility=row["visibility"],
                intended_interpretation=row["intended_interpretation"], actual_meaning=row["actual_meaning"],
                payoff_window_end=row["payoff_window_end"], status=row["status"], quality=row["quality"]
            )
        else:
            seed = seeds[0]

        issues = []
        if seed.clue_strength > 0.8:
            issues.append("TOO_OBVIOUS: Readers will likely guess the reveal prematurely.")
        elif seed.clue_strength < 0.2:
            issues.append("TOO_SUBTLE: Clue may pass completely unnoticed, failing fair-play criteria.")

        quality_val = seed.quality.value if hasattr(seed.quality, "value") else str(seed.quality)
        return {
            "seed_id": seed_id,
            "quality": quality_val,
            "clue_strength": seed.clue_strength,
            "visibility": seed.visibility,
            "issues": issues,
            "is_effective": len(issues) == 0,
        }

    def link_payoff(self, seed_id: str, payoff_chapter: int) -> ForeshadowingSeed:
        cur = self.plot_repo.conn.execute("SELECT * FROM foreshadowing_seeds WHERE id = ?", (seed_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Foreshadowing seed {seed_id} not found")
        seed = ForeshadowingSeed(
            id=row["id"], story_id=row["story_id"], seed_text=row["seed_text"],
            foreshadowing_type=row["foreshadowing_type"], target_event=row["target_event"],
            target_reveal=row["target_reveal"], chapter_introduced=row["chapter_introduced"],
            clue_strength=row["clue_strength"], visibility=row["visibility"],
            intended_interpretation=row["intended_interpretation"], actual_meaning=row["actual_meaning"],
            payoff_window_end=row["payoff_window_end"], status="PAID_OFF", quality=row["quality"]
        )
        return self.plot_repo.save_foreshadowing_seed(seed)

    # =========================================================================
    # 2. PLOT TWISTS & REVERSALS
    # =========================================================================

    def create_twist(
        self,
        story_id: str,
        title: str,
        setup: str,
        hidden_truth: str,
        reveal_text: str,
        expected_reader_belief: str,
        actual_truth: str,
        affected_characters: Optional[List[str]] = None,
        consequences: Optional[List[str]] = None,
        foreshadowing_ids: Optional[List[str]] = None,
        reveal_chapter: int = 1,
        importance: str = "MAJOR",
    ) -> PlotTwist:
        twist = PlotTwist(
            id=str(uuid.uuid4()),
            story_id=story_id,
            title=title,
            setup=setup,
            hidden_truth=hidden_truth,
            reveal_text=reveal_text,
            expected_reader_belief=expected_reader_belief,
            actual_truth=actual_truth,
            affected_characters=affected_characters or [],
            consequences=consequences or [],
            foreshadowing_ids=foreshadowing_ids or [],
            reveal_chapter=reveal_chapter,
            importance=importance,
            surprise_rating=8.5,
            fairness_rating=9.0 if (foreshadowing_ids and len(foreshadowing_ids) >= 2) else 6.0,
        )
        return self.plot_repo.save_twist(twist)

    def create_reversal(
        self,
        story_id: str,
        title: str,
        reversal_type: ReversalType,
        trigger_chapter: int,
        affected_characters: Optional[List[str]] = None,
        setup_events: Optional[List[str]] = None,
        outcome_description: str = "",
        consequences: Optional[List[str]] = None,
    ) -> Reversal:
        reversal = Reversal(
            id=str(uuid.uuid4()),
            story_id=story_id,
            title=title,
            reversal_type=reversal_type,
            trigger_chapter=trigger_chapter,
            affected_characters=affected_characters or [],
            setup_events=setup_events or [],
            outcome_description=outcome_description,
            consequences=consequences or [],
        )
        with self.plot_repo.conn:
            self.plot_repo.conn.execute("""
                INSERT OR REPLACE INTO reversals (
                    id, story_id, title, reversal_type, trigger_chapter,
                    affected_characters_data, setup_events_data, outcome_description, consequences_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                reversal.id, reversal.story_id, reversal.title,
                reversal.reversal_type.value if hasattr(reversal.reversal_type, "value") else str(reversal.reversal_type),
                reversal.trigger_chapter, json.dumps(reversal.affected_characters),
                json.dumps(reversal.setup_events), reversal.outcome_description,
                json.dumps(reversal.consequences)
            ))
        return reversal
