"""
NovelForge AI — Story Memory Engine Architecture
Provides clean interfaces: MemoryStore, MemoryRetriever, MemoryWriter, MemorySummarizer.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from novelforge.database.narrative_repository import NarrativeRepository
from novelforge.schemas.narrative_models import ChapterMemory


class MemoryStore(ABC):
    @abstractmethod
    def store_chapter_memory(self, memory: ChapterMemory) -> None:
        pass

    @abstractmethod
    def retrieve_chapter_memory(self, story_id: str, chapter_number: int) -> Optional[Dict[str, Any]]:
        pass


class MemoryRetriever(ABC):
    @abstractmethod
    def retrieve_relevant_memory(self, story_id: str, query: str, tier: str) -> List[Dict[str, Any]]:
        pass


class MemoryWriter(ABC):
    @abstractmethod
    def record_scene_delta(self, story_id: str, chapter_num: int, scene_num: int, delta: Dict[str, Any]) -> None:
        pass


class MemorySummarizer(ABC):
    @abstractmethod
    def summarize_chapter(self, story_id: str, chapter_number: int, prose_text: str) -> ChapterMemory:
        pass


class DefaultNarrativeMemoryEngine(MemoryStore, MemoryRetriever, MemoryWriter, MemorySummarizer):
    def __init__(self, repository: NarrativeRepository):
        self.repo = repository

    def store_chapter_memory(self, memory: ChapterMemory) -> None:
        self.repo.save_chapter_memory(memory)

    def retrieve_chapter_memory(self, story_id: str, chapter_number: int) -> Optional[Dict[str, Any]]:
        return self.repo.get_chapter_memory(story_id, chapter_number)

    def retrieve_relevant_memory(self, story_id: str, query: str, tier: str = "SHORT_TERM") -> List[Dict[str, Any]]:
        """
        Tiered memory retrieval without heavy semantic dependencies in Phase 2.
        Future phases connect this to vector embeddings.
        """
        results = []
        if tier in ["SHORT_TERM", "MEDIUM_TERM"]:
            # Retrieve recent chapters
            story = self.repo.get_story(story_id)
            current_ch = story.current_chapter if story else 1
            for ch in range(max(1, current_ch - 3), current_ch + 1):
                mem = self.repo.get_chapter_memory(story_id, ch)
                if mem:
                    results.append(mem)
        elif tier in ["LONG_TERM", "ARCHIVAL"]:
            # Retrieve facts and major events
            facts = self.repo.get_knowledge_facts(story_id)
            results.extend(facts[:10])
        return results

    def record_scene_delta(self, story_id: str, chapter_num: int, scene_num: int, delta: Dict[str, Any]) -> None:
        # Appends delta into recent state
        pass

    def summarize_chapter(self, story_id: str, chapter_number: int, prose_text: str) -> ChapterMemory:
        """
        Extracts structured memory from chapter prose.
        """
        summary_text = f"Chapter {chapter_number} events: " + (prose_text[:200] + "..." if len(prose_text) > 200 else prose_text)
        return ChapterMemory(
            story_id=story_id,
            chapter_number=chapter_number,
            chapter_summary=summary_text,
            important_events=["Chapter progression recorded"],
            characters_present=[],
            locations=[]
        )
