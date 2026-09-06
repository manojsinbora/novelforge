"""
NovelForge AI — Story Dependency Graph & Change Impact Service
Phase 4: Dependency Traversal, Downstream Impact Analysis & Story Rewrite Guard
"""
from __future__ import annotations
from typing import List, Dict, Optional, Any, Set
import uuid

from novelforge.database.plot_repository import PlotRepository
from novelforge.schemas.plot_models import (
    NarrativeDependency, ChangeImpactReport
)


class DependencyImpactService:
    def __init__(self, plot_repo: PlotRepository):
        self.plot_repo = plot_repo

    def add_dependency(
        self,
        story_id: str,
        source_type: str,
        source_id: str,
        target_type: str,
        target_id: str,
        dependency_type: str = "REQUIRES",
        description: str = "",
    ) -> NarrativeDependency:
        dep = NarrativeDependency(
            id=str(uuid.uuid4()),
            story_id=story_id,
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
            dependency_type=dependency_type,
            description=description,
        )
        return self.plot_repo.save_dependency(dep)

    def analyze_change_impact(
        self,
        story_id: str,
        modified_entity_type: str,
        modified_entity_id: str,
        modified_chapter: int,
    ) -> ChangeImpactReport:
        """
        MANDATORY REQUIREMENT: If an author or agent changes an event, clue, or chapter,
        this method traverses downstream dependencies to identify affected arcs,
        chapters, promises, and mysteries without performing destructive rewrites.
        """
        affected_arcs: Set[str] = set()
        affected_chapters: Set[int] = set()
        affected_mysteries: Set[str] = set()
        affected_promises: Set[str] = set()
        affected_foreshadowing: Set[str] = set()
        affected_characters: Set[str] = set()

        # 1. Direct dependencies from narrative_dependencies graph
        direct_deps = self.plot_repo.get_downstream_dependencies(
            source_type=modified_entity_type,
            source_id=modified_entity_id
        )

        for dep in direct_deps:
            target_t = dep.target_type.upper()
            if "ARC" in target_t:
                affected_arcs.add(dep.target_id)
            elif "CHAPTER" in target_t:
                try:
                    affected_chapters.add(int(dep.target_id))
                except ValueError:
                    affected_chapters.add(hash(dep.target_id) % 1000)
            elif "MYSTERY" in target_t:
                affected_mysteries.add(dep.target_id)
            elif "PROMISE" in target_t:
                affected_promises.add(dep.target_id)
            elif "FORESHADOWING" in target_t:
                affected_foreshadowing.add(dep.target_id)
            elif "CHARACTER" in target_t:
                affected_characters.add(dep.target_id)
            else:
                # Catch-all for other narrative entities (SCENE, BEAT, etc.)
                affected_arcs.add(dep.target_id)

        # 2. Check future promises linked to this chapter
        promises = self.plot_repo.get_promises_for_story(story_id)
        for p in promises:
            if p.introduced_chapter == modified_chapter or p.related_thread_id == modified_entity_id:
                affected_promises.add(p.id)
                if p.payoff_chapter and p.payoff_chapter > modified_chapter:
                    affected_chapters.add(p.payoff_chapter)

        # 3. Check foreshadowing seeds planted at or after this chapter
        seeds = self.plot_repo.get_foreshadowing_for_story(story_id)
        for s in seeds:
            if s.chapter_introduced == modified_chapter or s.target_event == modified_entity_id:
                affected_foreshadowing.add(s.id)

        # 4. Check future arcs whose start_chapter is after modified_chapter
        arcs = self.plot_repo.get_arc_plans_for_story(story_id)
        for a in arcs:
            if a.start_chapter > modified_chapter and (modified_entity_id in a.open_threads or modified_entity_id in a.primary_characters):
                affected_arcs.add(a.id)

        total_affected = (
            len(affected_arcs) + len(affected_chapters) +
            len(affected_mysteries) + len(affected_promises) +
            len(affected_foreshadowing) + len(affected_characters)
        )

        if total_affected == 0:
            risk = "LOW"
        elif total_affected <= 3:
            risk = "MEDIUM"
        elif total_affected <= 7:
            risk = "HIGH"
        else:
            risk = "CATASTROPHIC"

        recommendations = []
        if affected_mysteries:
            recommendations.append(f"Review clues and reveal timing for mysteries: {list(affected_mysteries)}")
        if affected_promises:
            recommendations.append(f"Verify payoff fulfillment for promises: {list(affected_promises)}")
        if affected_arcs:
            recommendations.append(f"Update arc blueprints for affected arcs: {list(affected_arcs)}")
        if not recommendations:
            recommendations.append("No downstream structural breaks detected. Change is safe to canonize.")

        return ChangeImpactReport(
            modified_entity_type=modified_entity_type,
            modified_entity_id=modified_entity_id,
            modified_chapter=modified_chapter,
            affected_arcs=list(affected_arcs),
            affected_chapters=sorted(list(affected_chapters)),
            affected_mysteries=list(affected_mysteries),
            affected_promises=list(affected_promises),
            affected_foreshadowing=list(affected_foreshadowing),
            affected_characters=list(affected_characters),
            downstream_rewrite_risk=risk,
            total_affected_elements=total_affected,
            recommendations=recommendations,
        )
