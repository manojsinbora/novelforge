# NovelForge AI — Database Specification & Schema Design

## 1. Database Architecture Overview

NovelForge AI uses a hybrid relational and event-sourced persistence model:
* **Primary Database:** PostgreSQL 15+ (with `pgvector` extension for semantic embedding retrieval).
* **Local Development Fallback:** SQLite 3 (with JSON extensions and fallback vector cosine similarity in Python).
* **ORM:** SQLAlchemy 2.0 (asyncio-compatible) with Alembic for migrations.

---

## 2. Core Tables and Relationships

### 2.1 Event Sourcing Ledger (`story_events`)
The single source of truth for narrative progression. All mutations flow through this table.

```sql
CREATE TABLE story_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    story_id UUID NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    saga_id UUID REFERENCES sagas(id),
    arc_id UUID REFERENCES arcs(id),
    chapter_id UUID REFERENCES chapters(id),
    scene_id UUID,
    sequence_num BIGINT NOT NULL,
    event_type VARCHAR(64) NOT NULL, -- e.g., CHARACTER_PROMOTED, ITEM_TRANSFERRED, SECRET_REVEALED
    entity_type VARCHAR(64) NOT NULL, -- e.g., CHARACTER, ITEM, FACTION, PLOT_THREAD
    entity_id UUID NOT NULL,
    payload JSONB NOT NULL, -- structured delta of the change
    author_type VARCHAR(16) NOT NULL DEFAULT 'AI', -- 'AI' or 'HUMAN'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_story_events_seq ON story_events(story_id, chapter_id, sequence_num);
CREATE INDEX idx_story_events_entity ON story_events(entity_type, entity_id);
```

### 2.2 Story Hierarchy Tables

```sql
CREATE TABLE stories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    premise TEXT NOT NULL,
    genres JSONB NOT NULL DEFAULT '[]', -- e.g. ["xianxia", "regression", "mystery"]
    target_chapter_count INT DEFAULT 2000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE sagas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    story_id UUID NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    index_num INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    major_conflicts JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE arcs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    saga_id UUID NOT NULL REFERENCES sagas(id) ON DELETE CASCADE,
    index_num INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    target_chapters INT DEFAULT 30,
    status VARCHAR(32) DEFAULT 'PLANNED', -- PLANNED, ACTIVE, COMPLETED
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    arc_id UUID NOT NULL REFERENCES arcs(id) ON DELETE CASCADE,
    chapter_number INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    blueprint JSONB, -- hook, objectives, scene outlines, ending hook
    word_count INT DEFAULT 0,
    status VARCHAR(32) DEFAULT 'DRAFT', -- DRAFT, PROVISIONAL, CANON, REJECTED
    qa_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE scenes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    scene_number INT NOT NULL,
    pov_character_id UUID,
    location_id UUID,
    objective TEXT,
    conflict TEXT,
    content TEXT,
    word_count INT DEFAULT 0,
    local_state_delta JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 2.3 Narrative State & Epistemic Tracking

```sql
CREATE TABLE character_knowledge_states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    story_id UUID NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    fact_key VARCHAR(128) NOT NULL, -- e.g., "emperor_is_alive"
    description TEXT NOT NULL,
    author_knowledge BOOLEAN NOT NULL DEFAULT TRUE,
    reader_knowledge BOOLEAN NOT NULL DEFAULT FALSE,
    character_id UUID NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
    character_knowledge BOOLEAN NOT NULL DEFAULT FALSE,
    planned_reveal_chapter INT,
    actual_revealed_chapter INT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_char_fact ON character_knowledge_states(character_id, fact_key);
```

### 2.4 Promises, Foreshadowing & Plot Threads

```sql
CREATE TABLE narrative_promises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    story_id UUID NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    promise_title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    introduced_chapter INT NOT NULL,
    target_payoff_min INT NOT NULL,
    target_payoff_max INT NOT NULL,
    status VARCHAR(32) DEFAULT 'UNRESOLVED', -- UNRESOLVED, OVERDUE, APPROACHING_PAYOFF, RESOLVED
    resolution_chapter INT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE foreshadowing_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    story_id UUID NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    seed_chapter INT NOT NULL,
    clues JSONB DEFAULT '[]', -- [{chapter: 73, text: "slight trembling in jade pendant"}]
    intended_false_meaning TEXT NOT NULL,
    true_meaning TEXT NOT NULL,
    planned_payoff_chapter INT NOT NULL,
    importance_level VARCHAR(32) DEFAULT 'MEDIUM', -- LOW, MEDIUM, HIGH, MAJOR
    status VARCHAR(32) DEFAULT 'SEEDED' -- SEEDED, DEVELOPING, PAID_OFF, ABANDONED
);
```

### 2.5 Vector Embeddings Table (`story_memory_embeddings`)

```sql
CREATE TABLE story_memory_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    story_id UUID NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    memory_tier VARCHAR(32) NOT NULL, -- SHORT_TERM, MEDIUM_TERM, LONG_TERM, ARCHIVAL
    reference_id UUID, -- chapter_id or event_id
    content TEXT NOT NULL,
    embedding vector(1536), -- compatible with OpenAI/Gemini standard embeddings
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```
