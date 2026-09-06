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
        "version": "3.0.0",
        "features": [
            "Event Sourcing Ledger",
            "Epistemic Knowledge Matrix",
            "Dynamic Token Budgeting",
            "Hybrid Cultivation Evaluator",
            "Multi-Tier Model Router",
            "Phase 2: Narrative State Engine & Story Bible System",
            "Phase 3: Power, Mutation, Cultivation, Progression & Equipment Engine"
        ]
    }

# FastAPI Integration (when installed)
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from novelforge.backend.app.api.v1.narrative_router import router as narrative_router
    from novelforge.backend.app.api.v1.power_router import router as power_router

    app = FastAPI(
        title="NovelForge AI Engine API",
        description="Persistent Narrative State, Story Bible & Power Progression Engine for Long-Form Web Novels",
        version="3.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health_check():
        return get_health_status()

    # Mount Phase 2 narrative router
    app.include_router(narrative_router)
    # Mount Phase 3 power & progression router
    app.include_router(power_router)

except ImportError:
    app = None
