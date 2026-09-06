"""
NovelForge AI — Task-Based Model Router with Automated Fallbacks
"""
from __future__ import annotations
from typing import Dict, Any, Optional
from enum import Enum
from novelforge.models.llm_client import (
    BaseLLMClient, MockLLMClient, AnthropicClient, OpenAIClient, GeminiClient
)


class TaskTier(str, Enum):
    TIER_1_REASONING = "TIER_1_REASONING" # Master planning, arc outlines, deep QA
    TIER_2_PROSE = "TIER_2_PROSE"         # Scene prose writing, stitching
    TIER_3_EXTRACTION = "TIER_3_EXTRACTION" # Summaries, event extraction, fast QA
    TIER_4_DETERMINISTIC = "TIER_4_DETERMINISTIC" # Combat math, regex (zero LLM)


class ModelRouter:
    def __init__(self, mode: str = "mock"):
        self.mode = mode
        self.mock_client = MockLLMClient()
        self.clients: Dict[str, BaseLLMClient] = {
            "mock": self.mock_client,
            "openai": OpenAIClient(),
            "anthropic": AnthropicClient(),
            "gemini": GeminiClient()
        }

    def route(self, task_type: str) -> BaseLLMClient:
        """
        Maps task type to appropriate tier client.
        """
        if self.mode == "mock":
            return self.mock_client

        # Map tasks to primary clients
        if task_type in ["MASTER_PLANNING", "CHAPTER_BLUEPRINT", "CONTINUITY_QA"]:
            return self.clients.get("anthropic", self.mock_client)
        elif task_type in ["PROSE_GENERATION", "SCENE_STITCHING"]:
            return self.clients.get("anthropic", self.mock_client)
        elif task_type in ["MEMORY_EXTRACTION", "SUMMARY", "FAST_QA"]:
            return self.clients.get("gemini", self.mock_client)
        return self.mock_client

    def generate_with_fallback(self, task_type: str, prompt: str, system_prompt: Optional[str] = None) -> str:
        client = self.route(task_type)
        try:
            return client.generate(prompt=prompt, system_prompt=system_prompt)
        except Exception as e:
            # Fallback to secondary provider
            fallback_client = self.clients.get("openai", self.mock_client)
            return fallback_client.generate(prompt=prompt, system_prompt=system_prompt)
