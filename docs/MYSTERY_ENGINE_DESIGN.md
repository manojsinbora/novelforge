# Fair-Play Mystery & Epistemic Secrecy Engine Design

## 1. System Overview
Web novels frequently rely on overarching enigmas (e.g. historical cataclysms, hidden bloodlines, sect traitors). Standard LLM generation often either leaks spoilers prematurely or invents unearned, arbitrary revelations. The **Mystery & Secrecy Engine** guarantees fair-play mystery construction while enforcing strict epistemic access control.

## 2. Epistemic Access Control
The engine enforces role-based information visibility:
- **Author & System**: Raw access to  and resolution criteria.
- **Reader, Drafting Agent & Characters**:  is masked to . Drafting prompts receive only observed clues, false leads, and surface theories.

## 3. Fair-Play Mystery Validation
The  protocol audits:
- **Clue Sufficiency**: Verifies that genuine clues exist in canon before allowing mystery resolution.
- **Red Herring Balance**: Flags mysteries where false leads outnumber verifiable clues by more than 3:1.
- **Fair Play Score**: A quantitative 0–100 score indicating reader solvability.
