"""
NovelForge AI — Backend Application Gateway
Provides REST API endpoints for story management, state queries, and pipeline orchestration.
"""
from __future__ import annotations
from typing import Dict, Any, Optional
from novelforge.database.event_store import EventStore
from novelforge.backend.app.services.state_engine import NarrativeStateEngine
from novelforge.models.router import ModelRouter
from novelforge.tools.cultivation_evaluator import CultivationCombatEvaluator

# Initialize core services
default_event_store = EventStore(":memory:")
state_engine = NarrativeStateEngine(default_event_store)
model_router = ModelRouter(mode="mock")

def get_health_status() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "service": "NovelForge AI Narrative Engine",
        "version": "2.0.0",
        "features": [
            "Event Sourcing Ledger",
            "Epistemic Knowledge Matrix",
            "Dynamic Token Budgeting",
            "Hybrid Cultivation Evaluator",
            "Multi-Tier Model Router"
        ]
    }

def query_story_state(story_id: str, chapter_number: int, location: str = "Azure Dragon Sect") -> Dict[str, Any]:
    return state_engine.get_narrative_state(story_id, chapter_number, location)

# FastAPI Integration (when installed)
try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel

    app = FastAPI(
        title="NovelForge AI Engine API",
        description="Persistent Narrative State Engine for Long-Form Web Novels",
        version="2.0.0"
    )

    @app.get("/health")
    def health_check():
        return get_health_status()

    @app.get("/api/v1/stories/{story_id}/state")
    def get_state(story_id: str, chapter: int = 1, location: str = "Azure Dragon Sect"):
        return query_story_state(story_id, chapter, location)

except ImportError:
    # Running in lightweight standard-library environment
    app = None
