# NovelForge AI — API Interface Specification

## 1. REST API Overview (FastAPI)

All story management, chapter generation pipelines, state inspections, and author revisions are exposed through FastAPI endpoints.

Base URL: `http://localhost:8000/api/v1`

---

## 2. Endpoints Reference

### 2.1 Story Management
* `POST /stories` — Initialize a new story series (creates Story Bible and default Event Ledger).
* `GET /stories/{story_id}` — Get story overview, active saga, and progress metrics.
* `GET /stories/{story_id}/bible` — Get authoritative story bible and hard rules.
* `PUT /stories/{story_id}/bible` — Propose/commit updates to foundational rules.

### 2.2 Story State & Inspection
* `GET /stories/{story_id}/state` — Get current projected story state at latest canon chapter.
* `GET /stories/{story_id}/state?at_chapter={chapter_num}` — Non-destructive time-travel inspection of state at chapter $N$.
* `GET /stories/{story_id}/characters/{char_id}` — Get character dossier, current power, and knowledge state.
* `GET /stories/{story_id}/promises` — List active, approaching, and overdue narrative promises.
* `GET /stories/{story_id}/foreshadowing` — List active foreshadowing seeds and planned payoffs.

### 2.3 Generation Pipeline & Agent Execution
* `POST /stories/{story_id}/pipeline/chapter` — Trigger the full 27-step chapter generation pipeline:
  ```json
  {
    "target_chapter_number": 341,
    "user_directive": "Escalate conflict with the Blood Raven Sect; reveal second clue about ancient relic.",
    "autonomous_mode": false
  }
  ```
* `POST /stories/{story_id}/pipeline/scene` — Regenerate an individual scene beat within a chapter.
* `POST /stories/{story_id}/pipeline/critique` — Run the parallel async QA critic swarm on a drafted chapter.
* `POST /stories/{story_id}/pipeline/revise` — Execute targeted revision on specific QA defects.

### 2.4 Canon Approval & Rollback
* `POST /stories/{story_id}/chapters/{chapter_id}/approve` — Promote chapter from `PROVISIONAL` to `CANON`, committing events to ledger and Git.
* `POST /stories/{story_id}/chapters/{chapter_id}/reject` — Reject draft and trigger director re-planning.
* `POST /stories/{story_id}/rollback` — Revert story state back to chapter $N$, preserving divergent branches.
