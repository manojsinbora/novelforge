"""
NovelForge AI — Narrative State Engine REST API (FastAPI Router)
Phase 2 Endpoints: Stories, Hierarchy, Characters, Knowledge, World, Timeline, State Snapshots
"""
from __future__ import annotations
from typing import Dict, Any, List, Optional

try:
    from fastapi import APIRouter, HTTPException, Query
    from pydantic import BaseModel, Field
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    class APIRouter:
        def __init__(self, *args, **kwargs):
            self.routes = []
        def get(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def post(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def put(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
        def delete(self, *args, **kwargs):
            def decorator(f): return f
            return decorator
    class HTTPException(Exception):
        def __init__(self, status_code: int, detail: str):
            self.status_code = status_code
            self.detail = detail
    class BaseModel:
        pass
    def Field(*args, **kwargs):
        return None

from novelforge.database.narrative_repository import NarrativeRepository
from novelforge.backend.app.services.story_context_service import StoryContextService
from novelforge.backend.app.services.canon_service import CanonService
from novelforge.backend.app.services.knowledge_service import KnowledgeService
from novelforge.backend.app.services.timeline_service import TimelineService
from novelforge.backend.app.services.sync_service import StorySyncService
from novelforge.schemas.narrative_models import (
    StoryModel, StoryBible, Saga, Arc, Chapter, CharacterEntity,
    CharacterRelationship, KnowledgeFactEntity, WorldLocation, FactionEntity,
    StoryEventEntity, ProposedChange, PermissionLevel, ProposalStatus, KnowledgeState
)

router = APIRouter(prefix="/api/v1", tags=["Narrative State Engine"])

# Shared repository singleton
default_repo = NarrativeRepository("sqlite:///novelforge/database/novelforge.sqlite3")
context_service = StoryContextService(default_repo)
canon_service = CanonService(default_repo)
knowledge_service = KnowledgeService(default_repo)
timeline_service = TimelineService(default_repo)
sync_service = StorySyncService(default_repo)


# =============================================================================
# 1. STORIES & STORY BIBLE
# =============================================================================

@router.post("/stories")
def create_story(story: StoryModel):
    return default_repo.create_story(story)

@router.get("/stories/{story_id}")
def get_story(story_id: str):
    story = default_repo.get_story(story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.get("/stories/{story_id}/bible")
def get_story_bible(story_id: str):
    bible = default_repo.get_story_bible(story_id)
    if not bible:
        raise HTTPException(status_code=404, detail="Story Bible not found")
    return bible

@router.put("/stories/{story_id}/bible")
def update_story_bible(story_id: str, bible_data: Dict[str, Any]):
    # Note: Bible updates should be structured
    bible = StoryBible(story_id=story_id)
    # populated from bible_data
    default_repo.set_story_bible(bible)
    return {"status": "success", "message": "Story Bible updated"}


# =============================================================================
# 2. STORY HIERARCHY
# =============================================================================

@router.get("/stories/{story_id}/sagas")
def list_sagas(story_id: str):
    return default_repo.get_sagas(story_id)

@router.post("/stories/{story_id}/sagas")
def add_saga(story_id: str, saga: Saga):
    saga.story_id = story_id
    default_repo.add_saga(saga)
    return {"status": "created", "id": saga.id}

@router.get("/stories/{story_id}/arcs")
def list_arcs(story_id: str):
    return default_repo.get_arcs(story_id)

@router.post("/stories/{story_id}/arcs")
def add_arc(story_id: str, arc: Arc):
    arc.story_id = story_id
    default_repo.add_arc(arc)
    return {"status": "created", "id": arc.id}

@router.get("/stories/{story_id}/chapters")
def list_chapters(story_id: str):
    return default_repo.get_chapters(story_id)

@router.post("/stories/{story_id}/chapters")
def add_chapter(story_id: str, chapter: Chapter):
    chapter.story_id = story_id
    default_repo.add_chapter(chapter)
    return {"status": "created", "id": chapter.id}

@router.get("/stories/{story_id}/chapters/{chapter_number}")
def get_chapter(story_id: str, chapter_number: int):
    ch = default_repo.get_chapter(story_id, chapter_number)
    if not ch:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return ch


# =============================================================================
# 3. CHARACTERS & RELATIONSHIPS
# =============================================================================

@router.get("/stories/{story_id}/characters")
def list_characters(story_id: str):
    return default_repo.get_characters(story_id)

@router.post("/stories/{story_id}/characters")
def add_character(story_id: str, char: CharacterEntity):
    char.story_id = story_id
    default_repo.add_character(char)
    return {"status": "created", "id": char.id}

@router.get("/stories/{story_id}/characters/{char_id}")
def get_character(story_id: str, char_id: str):
    char = default_repo.get_character(story_id, char_id)
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return char

@router.get("/stories/{story_id}/relationships")
def list_relationships(story_id: str, character_id: Optional[str] = None):
    return default_repo.get_relationships(story_id, character_id)

@router.post("/stories/{story_id}/relationships")
def set_relationship(story_id: str, rel: CharacterRelationship):
    rel.story_id = story_id
    default_repo.set_relationship(rel)
    return {"status": "saved", "id": rel.id}


# =============================================================================
# 4. KNOWLEDGE & WORLD
# =============================================================================

@router.get("/stories/{story_id}/knowledge")
def list_knowledge_facts(story_id: str):
    return default_repo.get_knowledge_facts(story_id)

@router.post("/stories/{story_id}/knowledge")
def add_knowledge_fact(story_id: str, fact: KnowledgeFactEntity):
    fact.story_id = story_id
    default_repo.add_knowledge_fact(fact)
    return {"status": "created", "id": fact.id}

@router.get("/stories/{story_id}/locations")
def list_locations(story_id: str):
    return default_repo.get_locations(story_id)

@router.post("/stories/{story_id}/locations")
def add_location(story_id: str, loc: WorldLocation):
    loc.story_id = story_id
    default_repo.add_location(loc)
    return {"status": "created", "id": loc.id}

@router.get("/stories/{story_id}/factions")
def list_factions(story_id: str):
    return default_repo.get_factions(story_id)

@router.post("/stories/{story_id}/factions")
def add_faction(story_id: str, fac: FactionEntity):
    fac.story_id = story_id
    default_repo.add_faction(fac)
    return {"status": "created", "id": fac.id}


# =============================================================================
# 5. TIMELINE, STATE SNAPSHOTS & AUDIT LOGS
# =============================================================================

@router.get("/stories/{story_id}/timeline")
def get_timeline(story_id: str, up_to_chapter: Optional[int] = None):
    return default_repo.get_events(story_id, up_to_chapter=up_to_chapter)

@router.post("/stories/{story_id}/timeline")
def add_timeline_event(story_id: str, ev: StoryEventEntity):
    ev.story_id = story_id
    default_repo.add_event(ev)
    return {"status": "created", "id": ev.id}

@router.get("/stories/{story_id}/state")
def get_story_state(story_id: str, at_chapter: Optional[int] = Query(None, description="Reconstruct historical state at chapter N")):
    return default_repo.get_story_state_snapshot(story_id, at_chapter=at_chapter).to_dict()

@router.get("/stories/{story_id}/audit-logs")
def get_audit_logs(story_id: str):
    return default_repo.get_audit_logs(story_id)

@router.get("/stories/{story_id}/proposals")
def get_proposals(story_id: str, status: Optional[str] = None):
    return default_repo.get_proposals(story_id, status=status)

@router.post("/stories/{story_id}/proposals/{proposal_id}/review")
def review_proposal(
    story_id: str,
    proposal_id: str,
    decision: str = Query("APPROVE", enum=["APPROVE", "REJECT"]),
    approver: str = "Author/Director"
):
    success = canon_service.review_proposal(
        proposal_id=proposal_id,
        approver=approver,
        permission_level=PermissionLevel.CANON_EDITOR,
        decision=decision
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to process proposal")
    return {"status": "success", "decision": decision}

@router.post("/stories/{story_id}/sync/export")
def export_story_filesystem(story_id: str, folder_name: Optional[str] = None):
    export_dir = sync_service.export_story_to_filesystem(story_id, folder_name=folder_name)
    return {"status": "success", "exported_directory": export_dir}
