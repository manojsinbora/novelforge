# Narrative Context Builder & Story Health Engine Design

## 1. Context Bloat Mitigation
Injecting the entire story bible into an LLM prompt exhausts token budgets and induces model confusion. The  assembles token-budgeted prompt blocks:
- Filters plot threads strictly relevant to characters present in the scene.
- Extracts active goals and immediate promise deadlines.
- Epistemically masks canonical secrets from writing agents.

## 2. Quantitative Story Health Index
The  generates a composite health score (0–100):
- Deducts points for overdue promise debts.
- Flags stagnant subplots (>40 chapters without development).
- Audits pacing balance across Action, Mystery, Dialogue, and Progression.
