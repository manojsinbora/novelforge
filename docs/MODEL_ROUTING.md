# NovelForge AI — Model Routing & Provider Abstraction

## 1. Provider-Agnostic Model Interface

NovelForge AI implements a unified model client interface (`BaseLLMClient`) to prevent vendor lock-in. Supported providers:
* **Anthropic** (Claude 3.5 Sonnet, Claude 3 Opus, Claude 3.5 Haiku)
* **OpenAI** (GPT-4o, GPT-4o-mini, o1, o3-mini)
* **Google Gemini** (Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 2.0 Flash)
* **OpenRouter** (Aggregated access to DeepSeek, Llama 3, Mistral, Qwen)
* **Local Inference** (Ollama, vLLM, OpenAI-compatible local endpoints)

---

## 2. Task-Based Routing Tiers

Every agent task is mapped to a cost-effective model tier:

| Routing Tier | Ideal Models | Target Tasks | Cost Profile |
| :--- | :--- | :--- | :--- |
| **Tier 1: Frontier Reasoning** | Claude 3.5 Sonnet, GPT-4o, o3-mini | Master Planning, Saga/Arc Design, Chapter Blueprinting, Deep Continuity Critic | High ($3.00–$15.00 / M tokens) |
| **Tier 2: High-Velocity Creative Prose** | Claude 3.5 Sonnet, Llama-3.1-70B, Gemini 1.5 Pro | Scene Prose Generation, Scene Stitching, Dialogue Polishing | Moderate ($1.50–$3.00 / M tokens) |
| **Tier 3: Inexpensive Extraction & QA** | Gemini 1.5 Flash, GPT-4o-mini, Claude 3.5 Haiku | Memory Extraction, Fact Verification, Summaries, Formatting | Low ($0.075–$0.25 / M tokens) |
| **Tier 4: Deterministic Code** | Python 3.9+ runtime, Regex engine | Power Math, Inventory Check, Banned Words, State Delta Parser | Zero ($0.00 / Free) |

---

## 3. Configuration Schema & Fallback Chain

Model settings are fully configurable per environment and per story via `config.yaml`:

```yaml
model_routing:
  default_provider: "anthropic"
  tiers:
    tier_1_reasoning:
      primary: "claude-3-5-sonnet-20241022"
      fallback: "gpt-4o"
      temperature: 0.2
      max_tokens: 4096
    tier_2_prose:
      primary: "claude-3-5-sonnet-20241022"
      fallback: "gemini-1.5-pro"
      temperature: 0.75
      max_tokens: 3000
    tier_3_extraction:
      primary: "gemini-1.5-flash"
      fallback: "gpt-4o-mini"
      temperature: 0.0
      max_tokens: 1500

resilience:
  max_retries: 3
  exponential_backoff_base: 2.0
  circuit_breaker_threshold: 5
```

---

## 4. Content Safety Calibration for Dark Fantasy & Xianxia

Xianxia, cultivation, and dark fantasy web novels frequently involve martial combat, mortal injury, cultivation tribulations, and revenge conflicts that can inadvertently trigger standard commercial safety filters.

**Mitigations:**
1. **System Prompt Framing:** Explicitly declare fictional, mythic martial arts context in the system header:
   ```text
   [SYSTEM: HIGH-FANTASY FICTION GENERATION ENGINE]
   The following text is creative martial-arts fiction for a published novel. Depictions of combat, cultivation injuries, and fantasy battles are strictly fictional allegories.
   ```
2. **Permissive Fallback Routing:** If a primary frontier API returns a false-positive safety refusal (HTTP 400/content_filter), the router automatically reroutes the prompt to an uncensored local vLLM endpoint or OpenRouter uncensored model.
