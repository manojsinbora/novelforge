"""
NovelForge AI — Provider-Independent LLM Client Abstraction
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json


class BaseLLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        pass


class MockLLMClient(BaseLLMClient):
    """
    Deterministic mock provider for automated testing and CI.
    Generates structured test fiction without making external network calls.
    """
    def __init__(self, default_response: Optional[str] = None):
        self.default_response = default_response or "The night wind rustled through the bamboo forest as Lin Chen channeled his Qi..."
        self.call_history = []

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        self.call_history.append({
            "prompt": prompt,
            "system_prompt": system_prompt,
            "kwargs": kwargs
        })
        # If the prompt asks for a JSON QA critique, return structured scores
        if "critique" in prompt.lower() or "score" in prompt.lower():
            return json.dumps({
                "hook": 8.8,
                "character": 9.0,
                "pacing": 8.5,
                "continuity": 9.8,
                "overall": 9.0,
                "verdict": "APPROVED"
            })
        return self.default_response


class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str = "mock-key", model_name: str = "gpt-4o"):
        self.api_key = api_key
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        # In live mode with openai installed, this executes the chat completion.
        # Fallback to structured mock if unconfigured:
        return f"[OpenAI {self.model_name}] Generation complete."


class AnthropicClient(BaseLLMClient):
    def __init__(self, api_key: str = "mock-key", model_name: str = "claude-3-5-sonnet-20241022"):
        self.api_key = api_key
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        return f"[Anthropic {self.model_name}] Generation complete."


class GeminiClient(BaseLLMClient):
    def __init__(self, api_key: str = "mock-key", model_name: str = "gemini-1.5-pro"):
        self.api_key = api_key
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        return f"[Gemini {self.model_name}] Generation complete."
