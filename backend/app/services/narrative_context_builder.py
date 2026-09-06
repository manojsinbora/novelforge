"""
NovelForge AI — Narrative Context Builder
Phase 4: Relevance-Filtered, Token-Budgeted Story Architecture Prompt Builder
Prevents context window bloat by assembling only relevant narrative elements.
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any

from novelforge.database.plot_repository import PlotRepository
from novelforge.backend.app.services.plot_thread_service import PlotThreadService
from novelforge.backend.app.services.mystery_promise_service import MysteryPromiseService


class NarrativeContextBuilder:
    def __init__(
        self,
        plot_repo: PlotRepository,
        plot_thread_svc: PlotThreadService,
        mystery_promise_svc: MysteryPromiseService
    ):
        self.plot_repo = plot_repo
        self.plot_thread_svc = plot_thread_svc
        self.mystery_promise_svc = mystery_promise_svc

    def build_scene_context(
        self,
        story_id: str,
        chapter_number: int,
        scene_num: int,
        character_ids: List[str],
        token_budget: int = 1200
    ) -> Dict[str, Any]:
        """
        Builds a compact prompt block containing only what is strictly relevant
        to the immediate scene: active threads involving these characters,
        active goals, and upcoming promises.
        """
        active_threads = self.plot_thread_svc.get_active_threads(story_id)
        relevant_threads = [
            t for t in active_threads
            if any(cid in t.related_characters for cid in character_ids)
        ]

        # Gather relevant character goals
        goals = []
        for cid in character_ids:
            g_list = self.plot_repo.get_goals_for_character(cid)
            active_g = [g for g in g_list if g.status.value == "ACTIVE"]
            if active_g:
                goals.extend(active_g[:2])

        # Gather chapter plan if available
        cp = self.plot_repo.get_chapter_plan(chapter_number)

        lines = [
            "### RELEVANT SCENE NARRATIVE CONTEXT",
            f"**Chapter**: {chapter_number} | **Scene**: {scene_num}",
        ]
        if cp:
            lines.append(f"**Chapter Objective**: {cp.chapter_objective}")
            lines.append(f"**Main Conflict**: {cp.main_conflict}")

        if relevant_threads:
            lines.append("**Active Plot Threads**:")
            for t in relevant_threads[:3]:
                lines.append(f"- [{t.thread_type.value}] {t.name} (Priority {t.priority}): {t.description}")

        if goals:
            lines.append("**Active Character Goals**:")
            for g in goals[:4]:
                lines.append(f"- Character {g.character_id}: {g.description} (Progress: {g.progress*100:.0f}%)")

        prompt_text = "\n".join(lines)
        return {
            "prompt_text": prompt_text,
            "relevant_threads_count": len(relevant_threads),
            "relevant_goals_count": len(goals),
            "token_estimate": len(prompt_text) // 4,
        }

    def build_chapter_context(
        self,
        story_id: str,
        chapter_number: int,
        token_budget: int = 2000
    ) -> Dict[str, Any]:
        """
        Builds comprehensive planning context for chapter drafting.
        """
        cp = self.plot_repo.get_chapter_plan(chapter_number)
        active_threads = self.plot_thread_svc.get_active_threads(story_id)
        open_promises = self.plot_repo.get_promises_for_story(story_id, status="OPEN")

        lines = [
            f"### AUTHORITATIVE CHAPTER {chapter_number} BLUEPRINT",
        ]
        if cp:
            lines.append(f"**Title**: {cp.title}")
            lines.append(f"**Objective**: {cp.chapter_objective}")
            lines.append(f"**Conflict**: {cp.main_conflict}")
            if cp.important_reveals:
                lines.append(f"**Required Reveals**: {', '.join(cp.important_reveals)}")
            if cp.ending_hook:
                lines.append(f"**Ending Hook ({cp.hook_type.value})**: {cp.ending_hook}")

        if open_promises:
            lines.append("**Open Promises to Advance/Consider**:")
            for p in open_promises[:4]:
                lines.append(f"- {p.description} (Introduced Ch {p.introduced_chapter})")

        prompt_text = "\n".join(lines)
        return {
            "prompt_text": prompt_text,
            "chapter_number": chapter_number,
            "token_estimate": len(prompt_text) // 4,
        }

    def build_mystery_context(
        self,
        mystery_ids: List[str],
        viewer_role: str = "READER"
    ) -> Dict[str, Any]:
        """
        Builds mystery context strictly masking hidden truths for non-author roles.
        """
        blocks = []
        for mid in mystery_ids:
            view = self.mystery_promise_svc.get_mystery_view(mid, viewer_role=viewer_role)
            blocks.append(f"**Mystery**: {view['title']}\nQuestion: {view['question']}\nTruth: {view['hidden_truth']}\nVisible Clues: {', '.join(view['visible_clues'])}")
        return {
            "prompt_text": "\n\n".join(blocks),
            "mysteries_count": len(mystery_ids),
        }
