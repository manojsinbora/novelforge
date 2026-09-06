"""
NovelForge AI — Context Allocator & Token Budgeter
Prevents 'Lost in the Middle' attention collapse and enforces Epistemic Boundaries.
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional
from novelforge.schemas.story_schemas import Character, KnowledgeFact, Promise, PromiseStatus


class ContextBudgeter:
    def __init__(self, total_budget_tokens: int = 8000):
        self.total_budget = total_budget_tokens
        # Token quotas:
        self.quota_objective = int(total_budget_tokens * 0.15)
        self.quota_characters = int(total_budget_tokens * 0.25)
        self.quota_environment = int(total_budget_tokens * 0.10)
        self.quota_power = int(total_budget_tokens * 0.15)
        self.quota_promises = int(total_budget_tokens * 0.10)
        self.quota_rolling_scene = int(total_budget_tokens * 0.25)

    def estimate_tokens(self, text: str) -> int:
        """Rough token heuristic (approx 4 chars per token)."""
        return max(1, len(text) // 4)

    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        max_chars = max_tokens * 4
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "... [TRUNCATED TO FIT CONTEXT BUDGET]"

    def assemble_scene_prompt(
        self,
        scene_objective: str,
        present_characters: List[Character],
        knowledge_facts: List[KnowledgeFact],
        environment_desc: str,
        power_rules_desc: str,
        active_promises: List[Promise],
        recent_prose_context: str
    ) -> Dict[str, Any]:
        """
        Assembles a strictly budgeted prompt payload with epistemic safety boundaries.
        """
        # 1. Epistemic Guard Header (Critical: What characters do NOT know)
        epistemic_warnings = []
        present_char_ids = {c.id for c in present_characters}
        
        for fact in knowledge_facts:
            # If fact is not known by any present character, reinforce the boundary
            unaware_chars = [c.name for c in present_characters if not fact.is_known_by(c.id)]
            if unaware_chars:
                epistemic_warnings.append(
                    f"- Secret '{fact.fact_key}': {fact.description}. "
                    f"Characters {', '.join(unaware_chars)} DO NOT KNOW THIS. They must NOT mention or act on it."
                )

        epistemic_header = ""
        if epistemic_warnings:
            epistemic_header = (
                "=== CRITICAL EPISTEMIC INTEGRITY (KNOWLEDGE BOUNDARIES) ===\n" +
                "\n".join(epistemic_warnings) + "\n============================================================\n\n"
            )

        # 2. Budgeted Components
        budgeted_objective = self.truncate_to_tokens(
            f"SCENE OBJECTIVE & BEAT:\n{scene_objective}", self.quota_objective
        )

        char_text_blocks = []
        for c in present_characters:
            char_text_blocks.append(
                f"CHARACTER: {c.name} (Age {c.age}, {c.gender})\n"
                f"- Driving Want: {c.driving_want}\n"
                f"- Core Fear: {c.core_fear}\n"
                f"- Voice: {c.voice_profile.sentence_cadence}, Formality: {c.voice_profile.formality_level}\n"
                f"- Cultivation: {c.cultivation.realm} ({c.cultivation.sub_realm})\n"
                f"- Equipped Items: {', '.join(c.equipped_items) if c.equipped_items else 'None'}"
            )
        budgeted_chars = self.truncate_to_tokens(
            "ACTIVE PRESENT CHARACTERS:\n" + "\n\n".join(char_text_blocks),
            self.quota_characters
        )

        budgeted_env = self.truncate_to_tokens(
            f"ENVIRONMENT & LOCATION:\n{environment_desc}", self.quota_environment
        )

        budgeted_power = self.truncate_to_tokens(
            f"CULTIVATION & POWER BOUNDARIES:\n{power_rules_desc}", self.quota_power
        )

        promise_blocks = [
            f"- Promise: {p.title} (Status: {p.status.value}, Expected by Ch {p.expected_payoff_max})"
            for p in active_promises
        ]
        budgeted_promises = self.truncate_to_tokens(
            "RELEVANT ACTIVE NARRATIVE PROMISES:\n" + "\n".join(promise_blocks),
            self.quota_promises
        )

        budgeted_prose = self.truncate_to_tokens(
            f"IMMEDIATE PRECEDING SCENE CONTEXT:\n{recent_prose_context}",
            self.quota_rolling_scene
        )

        # 3. Final Prompt Assembly
        full_system_prompt = (
            "You are the Scene Writing Agent for NovelForge AI.\n"
            "Your task is to write high-immersion serialized prose for this scene.\n"
            "NEGATIVE CONSTRAINTS: Avoid cliches ('testament to', 'shiver down the spine', 'unbeknownst to them').\n\n"
            + epistemic_header
            + budgeted_objective + "\n\n"
            + budgeted_chars + "\n\n"
            + budgeted_env + "\n\n"
            + budgeted_power + "\n\n"
            + budgeted_promises + "\n\n"
            + budgeted_prose
        )

        total_estimated_tokens = self.estimate_tokens(full_system_prompt)

        return {
            "prompt_text": full_system_prompt,
            "estimated_tokens": total_estimated_tokens,
            "under_budget": total_estimated_tokens <= (self.total_budget * 1.1),
            "epistemic_guards_count": len(epistemic_warnings)
        }
