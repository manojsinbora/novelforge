# NovelForge AI — 13-Phase Vertical Slice Roadmap

This roadmap implements NovelForge AI incrementally. Each phase delivers a testable, working vertical slice without placeholder stubs.

---

### Phase 1: Project Foundation & Core State Engine (Completed)
* **Deliverables:**
  * Project structure, dependency setup, and packaging.
  * SQLAlchemy / SQLite database layer with Event Sourcing Ledger (`story_events`, `event_snapshots`).
  * Provider-independent LLM abstraction with Mock & Live providers.
  * Dynamic Context Budgeter & Token Allocator module.
  * FastAPI server skeleton with initial endpoints.
* **Exit Criteria:** All unit tests pass; state can be mutated, replayed, and projected deterministically.

### Phase 2: Narrative State Engine & Story Bible System (Completed)
* **Deliverables:**
  * Story Entity Hierarchy (Series -> Saga -> Arc -> Chapter -> Scene).
  * Configurable Story Bible (Premise, Themes, Tone dials, Narrative & World Rules).
  * Canon Protection System (CANON, PROVISIONAL, DRAFT, DEPRECATED with approval workflow).
  * Character Engine & First-Class Relationships with historical tracking.
  * Epistemic Knowledge Matrix (Author vs Reader vs Character knowledge; secret-leak guard).
  * Hierarchical World Engine (Locations & Factions) and Spatial Travel Continuity Validator.
  * Story Events & Timeline (separating Real World Date, Story Day/Year, and Chapter Number).
  * Chapter Memory & Historical State Reconstruction at Chapter N.
  * Dual-mode persistence (SQLite zero-dependency + PostgreSQL compatible).
  * Agent Access Layer facade (`StoryContextService`).
  * Full REST API & Interactive Web Dashboard (`dashboard.html`).
  * Seed Story: *"Echoes of the Fallen Heaven"* (Cultivation + Regression + Mystery).
* **Exit Criteria:** 100% test pass rate across 16 unit tests; invariant assertions verified; filesystem export verified.

### Phase 3: Hierarchical Planning (Saga -> Arc -> Chapter) (Next Phase)

* Arc Planner & Chapter Blueprinting agent prompts.
* Scene beat planner (3–5 scenes per chapter).
* Tension curve and hook placement validation.

### Phase 4: Scene-by-Scene Generation & Assembly
* Iterative scene generation loop with local micro-state tracking.
* Character Voice profiling & Anti-AI Cliché Filter.
* Chapter stitching and transition smoothing.

### Phase 5: Hybrid Cultivation & Combat Engine
* Cultivation realm, sub-realm, and technique data structures.
* Deterministic Python Combat Power Evaluator ("Can A defeat B?").
* Breakthrough and tribulation event handlers.

### Phase 6: Equipment, Inventory & World Mechanics
* Inventory tracking and item transfer event handlers.
* Location hierarchy and spatial travel validation.

### Phase 7: Plot, Promise & Foreshadowing System
* Long-term promise lifecycle manager and overdue alert engine.
* Foreshadowing clue disperser and payoff tracking.

### Phase 8: Parallel QA Critic Suite & Revision Loop
* Fast-path regex/rule checks + Deep-path async parallel critics.
* Configurable scoring thresholds ($<7.5$ rewrite, $8.5+$ approve).
* Surgical Editor/Revision agent.

### Phase 9: Memory Archival & Vector Retrieval
* Short-term, Medium-term, Long-term, and Archival memory tiers.
* Vector embeddings (pgvector) with temporal and semantic hybrid search.

### Phase 10: Reference Story Intelligence & Genre DNA
* Structural trope and pacing curve extractor (non-plagiarizing inspiration).
* Composable Genre DNA profiles (Cultivation + Regression + Mystery).

### Phase 11: Intelligent Model Router & Cost Control
* Task-to-model routing matrix with automated fallbacks and token budgeting.
* Generation cost estimator and latency tracking.

### Phase 12: Autonomous Multi-Chapter Batch Mode
* Resumable background DAG execution for generating batches (e.g., 5–10 chapters).
* Automatic pause-on-contradiction for human author intervention.

### Phase 13: Analytics & Web Novel Reader Engagement
* Chapter length, tension curve, and pacing analytics dashboard.
* Simulated reader retention scoring and chapter drop-off indicators.
