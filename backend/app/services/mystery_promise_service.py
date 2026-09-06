"""
NovelForge AI — Mystery, Promise & Epistemic Secrecy Service
Phase 4: Fair-Play Mystery Validation, Epistemic Access Control, and Promise Debt Engine
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any, Tuple
import uuid
import datetime
import json

from novelforge.database.plot_repository import PlotRepository
from novelforge.schemas.plot_models import (
    Mystery, MysteryClue, MysteryStatus, Secret, StoryPromise, PromiseStatus,
    NarrativeDebt, DebtSeverity
)


class MysteryPromiseService:
    def __init__(self, plot_repo: PlotRepository):
        self.plot_repo = plot_repo

    # =========================================================================
    # 1. MYSTERIES & CLUES (EPISTEMIC ACCESS CONTROL)
    # =========================================================================

    def create_mystery(
        self,
        story_id: str,
        title: str,
        question: str,
        hidden_truth: str,
        visible_clues: Optional[List[str]] = None,
        false_leads: Optional[List[str]] = None,
        true_leads: Optional[List[str]] = None,
        suspects: Optional[List[str]] = None,
        theories: Optional[List[str]] = None,
        reveal_plan: str = "",
        reveal_conditions: Optional[List[str]] = None,
        importance: str = "CORE",
        intended_reader_suspicion: str = "",
    ) -> Mystery:
        mystery = Mystery(
            id=str(uuid.uuid4()),
            story_id=story_id,
            title=title,
            question=question,
            hidden_truth=hidden_truth,
            visible_clues=visible_clues or [],
            false_leads=false_leads or [],
            true_leads=true_leads or [],
            suspects=suspects or [],
            theories=theories or [],
            reveal_plan=reveal_plan,
            reveal_conditions=reveal_conditions or [],
            resolution="",
            status=MysteryStatus.UNSOLVED,
            importance=importance,
            intended_reader_suspicion=intended_reader_suspicion,
            epistemic_knowledge={
                "AUTHOR": "KNOWN_TRUE",
                "SYSTEM": "KNOWN_TRUE",
                "READER": "UNKNOWN",
                "PROTAGONIST": "UNKNOWN"
            },
        )
        return self.plot_repo.save_mystery(mystery)

    def add_clue(
        self,
        mystery_id: str,
        clue_text: str,
        chapter_introduced: int,
        location_id: str = "",
        discoverer_id: str = "",
        visibility: str = "PUBLIC",
        interpretation: str = "",
        true_meaning: str = "",
        false_interpretations: Optional[List[str]] = None,
        importance: str = "MAJOR",
        payoff_chapter: Optional[int] = None,
    ) -> MysteryClue:
        mystery = self.plot_repo.get_mystery(mystery_id)
        if not mystery:
            raise ValueError(f"Mystery {mystery_id} not found")

        clue = MysteryClue(
            id=str(uuid.uuid4()),
            mystery_id=mystery_id,
            clue_text=clue_text,
            chapter_introduced=chapter_introduced,
            location_id=location_id,
            discoverer_id=discoverer_id,
            visibility=visibility,
            interpretation=interpretation,
            true_meaning=true_meaning,
            false_interpretations=false_interpretations or [],
            importance=importance,
            payoff_chapter=payoff_chapter,
            status="DISCOVERED",
        )
        saved = self.plot_repo.save_clue(clue)

        # Append to mystery visible clues
        if clue_text not in mystery.visible_clues:
            mystery.visible_clues.append(clue_text)
            self.plot_repo.save_mystery(mystery)

        return saved

    def get_mystery_view(
        self,
        mystery_id: str,
        viewer_role: str = "READER"
    ) -> Dict[str, Any]:
        """
        Retrieves mystery information adhering to epistemic permissions:
        - AUTHOR / SYSTEM: Can see raw hidden_truth.
        - READER / WRITING_AGENT / PROTAGONIST: hidden_truth is masked!
        """
        mystery = self.plot_repo.get_mystery(mystery_id)
        if not mystery:
            raise ValueError(f"Mystery {mystery_id} not found")

        clues = self.plot_repo.get_clues_for_mystery(mystery_id)
        mask = viewer_role not in ("AUTHOR", "SYSTEM")
        d = mystery.to_dict(mask_hidden_truth=mask)
        d["clues"] = [c.to_dict() for c in clues]
        return d

    def validate_fair_play_mystery(self, mystery_id: str) -> Dict[str, Any]:
        """
        MANDATORY REQUIREMENT: Checks if the story provided sufficient clues for
        the reader to solve the mystery and flags fair-play issues.
        """
        mystery = self.plot_repo.get_mystery(mystery_id)
        if not mystery:
            raise ValueError(f"Mystery {mystery_id} not found")

        clues = self.plot_repo.get_clues_for_mystery(mystery_id)
        flags = []

        if len(clues) == 0:
            flags.append("MISSING_CLUE: Zero discovered clues registered for this mystery.")
        elif len(clues) >= 8 and len(mystery.false_leads) == 0:
            flags.append("MYSTERY_TOO_EASY: Abundant clues with no red herrings or competing theories.")
        elif len(clues) == 1 and mystery.status == MysteryStatus.SOLVED:
            flags.append("UNSUPPORTED_REVEAL: Mystery marked solved with only 1 clue provided in text.")

        if len(mystery.false_leads) > len(clues) * 3:
            flags.append("MYSTERY_TOO_OBSCURE: False leads drastically outnumber genuine clues, risking reader frustration.")

        fair_play_score = max(0.0, 100.0 - (len(flags) * 25.0))
        status_val = mystery.status.value if hasattr(mystery.status, "value") else str(mystery.status)
        return {
            "mystery_id": mystery_id,
            "title": mystery.title,
            "status": status_val,
            "total_clues": len(clues),
            "false_leads_count": len(mystery.false_leads),
            "flags": flags,
            "is_fair_play": len(flags) == 0,
            "fair_play_score": fair_play_score,
        }

    # =========================================================================
    # 2. SECRETS
    # =========================================================================

    def create_secret(
        self,
        story_id: str,
        secret_text: str,
        owner_id: str,
        truth: str,
        who_knows: Optional[List[str]] = None,
        who_suspects: Optional[List[str]] = None,
        discovery_conditions: str = "",
        reveal_importance: str = "HIGH",
    ) -> Secret:
        secret = Secret(
            id=str(uuid.uuid4()),
            story_id=story_id,
            secret_text=secret_text,
            owner_id=owner_id,
            truth=truth,
            who_knows=who_knows or [owner_id],
            who_suspects=who_suspects or [],
            discovery_conditions=discovery_conditions,
            reveal_importance=reveal_importance,
            reveal_target="",
            is_revealed=False,
        )
        with self.plot_repo.conn:
            self.plot_repo.conn.execute("""
                INSERT OR REPLACE INTO secrets (
                    id, story_id, secret_text, owner_id, truth, who_knows_data,
                    who_suspects_data, discovery_conditions, reveal_importance,
                    reveal_target, is_revealed, reveal_chapter
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                secret.id, secret.story_id, secret.secret_text, secret.owner_id,
                secret.truth, json.dumps(secret.who_knows), json.dumps(secret.who_suspects),
                secret.discovery_conditions, secret.reveal_importance, secret.reveal_target,
                0, None
            ))
        return secret

    # =========================================================================
    # 3. NARRATIVE PROMISES & PROMISE DEBT
    # =========================================================================

    def create_promise(
        self,
        story_id: str,
        description: str,
        promise_type: str,
        introduced_chapter: int,
        importance: str = "HIGH",
        expected_payoff_window: int = 30,
        payoff_requirements: Optional[List[str]] = None,
        related_thread_id: Optional[str] = None,
        related_mystery_id: Optional[str] = None,
    ) -> StoryPromise:
        promise = StoryPromise(
            id=str(uuid.uuid4()),
            story_id=story_id,
            description=description,
            promise_type=promise_type,
            introduced_chapter=introduced_chapter,
            importance=importance,
            expected_payoff_window=expected_payoff_window,
            payoff_requirements=payoff_requirements or [],
            related_thread_id=related_thread_id,
            related_mystery_id=related_mystery_id,
            status=PromiseStatus.OPEN,
        )
        return self.plot_repo.save_promise(promise)

    def advance_promise(
        self,
        promise_id: str,
        new_status: PromiseStatus,
        payoff_chapter: Optional[int] = None
    ) -> StoryPromise:
        cur = self.plot_repo.conn.execute("SELECT * FROM story_promises WHERE id = ?", (promise_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Promise {promise_id} not found")
        prom = StoryPromise(
            id=row["id"],
            story_id=row["story_id"],
            description=row["description"],
            promise_type=row["promise_type"],
            introduced_chapter=row["introduced_chapter"],
            importance=row["importance"],
            expected_payoff_window=row["expected_payoff_window"],
            payoff_requirements=json.loads(row["payoff_requirements_data"] or "[]"),
            related_thread_id=row["related_thread_id"],
            related_mystery_id=row["related_mystery_id"],
            status=new_status,
            payoff_chapter=payoff_chapter or row["payoff_chapter"],
            created_at=row["created_at"],
        )
        return self.plot_repo.save_promise(prom)

    def detect_promise_debts(self, story_id: str, current_chapter: int) -> List[NarrativeDebt]:
        """
        Scans story promises. If current_chapter exceeds introduced_chapter + expected_payoff_window,
        flags promise as OVERDUE and generates high/critical NarrativeDebt records.
        """
        promises = self.plot_repo.get_promises_for_story(story_id)
        debts: List[NarrativeDebt] = []

        for p in promises:
            if p.status in (PromiseStatus.OPEN, PromiseStatus.ACTIVE, PromiseStatus.DEVELOPING, PromiseStatus.OVERDUE):
                age = current_chapter - p.introduced_chapter
                if age > p.expected_payoff_window:
                    # Update status to OVERDUE
                    if p.status != PromiseStatus.OVERDUE:
                        self.advance_promise(p.id, PromiseStatus.OVERDUE)

                    severity = DebtSeverity.CRITICAL if (age > p.expected_payoff_window * 2) else DebtSeverity.HIGH
                    debt = NarrativeDebt(
                        id=str(uuid.uuid4()),
                        story_id=story_id,
                        debt_type="OVERDUE_PROMISE",
                        severity=severity,
                        title=f"Overdue Promise: {p.description[:50]}...",
                        description=f"Narrative promise made in Chapter {p.introduced_chapter} has remained unresolved for {age} chapters (window was {p.expected_payoff_window}).",
                        introduced_chapter=p.introduced_chapter,
                        age_chapters=age,
                        importance=p.importance,
                        affected_entities=[p.id],
                        suggested_remedy=f"Develop or resolve promise in upcoming chapters (Chapters {current_chapter}–{current_chapter + 5})."
                    )
                    self.plot_repo.save_debt(debt)
                    debts.append(debt)
        return debts
