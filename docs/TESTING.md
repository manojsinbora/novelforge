# NovelForge AI — Testing & Verification Strategy

## 1. Testing Philosophy

Because NovelForge AI generates serialized fiction across thousands of chapters, standard software testing is coupled with **narrative state invariant testing**:
1. **Deterministic Rule Tests:** 100% test coverage for combat power calculations, inventory constraints, and state transition logic.
2. **Event Sourcing Replay Tests:** Verifying that replaying an event stream from Chapter 1 to Chapter 500 produces the exact same projected state every time.
3. **Epistemic Invariant Tests:** Ensuring no character can ever possess or act on unrevealed knowledge.
4. **Context Budgeting Tests:** Verifying that prompt assembly strictly stays within the token budget.
5. **Mock LLM Pipeline Tests:** Fast, zero-cost CI testing using mock LLM responses with deterministic validation.

---

## 2. Test Execution Commands

```bash
# Run all unit tests
pytest novelforge/tests/

# Run event sourcing replay tests
pytest novelforge/tests/test_event_sourcing.py

# Run context allocator token budget tests
pytest novelforge/tests/test_context_budgeter.py

# Run mock pipeline integration tests
pytest novelforge/tests/test_pipeline_integration.py
```

---

## 3. Mandatory State Invariant Assertions

* `assert not character.has_item(item_id)` when the item was transferred in a prior event.
* `assert character_a.cannot_defeat(character_b)` when character B is two major cultivation realms above A without divine treasure intervention.
* `assert not character.knows(secret_id)` when `character_knowledge_states.character_knowledge == False`.
* `assert prompt.token_count <= max_budget` across all scene prompt assembly calls.
