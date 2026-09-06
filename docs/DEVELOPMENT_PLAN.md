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

### Phase 3: Power, Mutation, Cultivation, Progression & Equipment Engine (Completed)
* **Deliverables:**
  * Multi-system tier ladder (Cultivation, Awakening, Magic, Mutation, Martial Arts, Soul, Tech, Hybrid).
  * 7-Tier configurable progression system (`Novice` to `Transcendent`) with `Early`, `Mid`, `Late`, `Peak` sub-realms.
  * 12-Dimensional Power Vector (Physical, Energy, Speed, Durability, Perception, Mental, Technique, Combat Skill, Control, Adaptability, Regeneration, Special Ability).
  * Validated breakthrough engine with bottleneck checks, catalyst requirements, and ceiling limits.
  * 10-category Mutation Engine with 6 stability states and epistemic visibility filters.
  * 17 ability types and 5 mastery ranks with chapter cooldown enforcement.
  * Equipment & Relic engine with 7 rarities, durability loss/destruction, and immutable provenance history.
  * Multi-dimensional Combat Assessment Engine with probabilistic outcomes, decisive factors, and reversal conditions.
  * Power QA Guard and live continuity validator reporting Power QA Score.
  * Interactive UI tabs in `dashboard.html` for systems, dossiers, combat simulation, equipment, and QA.
  * Full seed data for *"Echoes of the Fallen Heaven"* and 12 automated unit tests.
* **Exit Criteria:** 100% test pass rate across all 28 automated unit tests; temporal isolation verified; breakthrough invariants verified.

### Phase 4: Plot, Story Architecture, Arc Planning, Mysteries, Promises & Foreshadowing Engine (Completed)
* **Deliverables:**
  * Complete Long-Term Story Architecture Schemas (`novelforge/schemas/plot_models.py`): MainPlot, StoryMilestone, PlotThread (19 types), CharacterArc (17 archetypes), CharacterArcMilestone, Goal, Conflict, Mystery, MysteryClue, Secret, StoryPromise, ForeshadowingSeed (14 types), PlotTwist, Reversal (9 types), BeatPlan, ScenePlan, ChapterPlan, ArcPlan, NarrativeDependency, NarrativeDebt, StoryHealthReport, ChangeImpactReport.
  * Relational Database Engine (`novelforge/database/plot_repository.py`): 19 tables in SQLite with full CRUD, temporal querying, and directed dependency traversal.
  * Service Suite (`novelforge/backend/app/services/`):
    * `plot_thread_service.py`: Mainline story engine & plot thread manager across 11 lifecycle states.
    * `character_arc_service.py`: Transformation arc engine, goal tracking, and character conflict matrix.
    * `mystery_promise_service.py`: Fair-play mystery validation, role-based epistemic masking, and overdue promise debt calculation.
    * `foreshadowing_twist_service.py`: Clue planting, subtlety quality scoring, and plot twist linking.
    * `arc_chapter_planning_service.py`: Hierarchical multi-horizon planner (5 Horizons), scene entry/exit state transition validator.
    * `dependency_impact_service.py`: Downstream change impact analysis and rewrite risk assessment.
    * `story_health_service.py`: Quantitative story health index (0–100), stagnant subplot detector.
    * `narrative_context_builder.py`: Relevance-filtered, token-budgeted prompt context builder.
  * Story Architecture Tool Suite (`novelforge/tools/plot_tools.py`) & REST Router (`novelforge/backend/app/api/v1/plot_router.py`).
  * Interactive UI Tabs in `novelforge/frontend/dashboard.html` for Plot Threads, Mysteries & Secrets, Promises & Debt, Foreshadowing, Character Arcs, and Story Health.
  * Full seed data for *"Echoes of the Fallen Heaven"* (`novelforge/scripts/seed_phase_4_plot.py`) and filesystem exports in `novelforge/stories/echoes_of_the_fallen_heaven/plot/`.
  * Comprehensive automated test suite (`novelforge/tests/test_phase_4_plot_engine.py`): 8 tests covering all 10 core engines. Total test suite passes 36/36 tests with 100% success rate.
* **Exit Criteria:** Zero-dependency Python 3.9 execution; epistemic masking enforced; fair-play checks verified; promise debts flagged; downstream change impact verified; 100% test pass rate.

### Phase 5: Multi-Agent Writing & Critique Pipeline (Next Phase)

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
