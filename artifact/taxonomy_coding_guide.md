# Taxonomy Coding Guide

This guide records the operational rules used to assign one primary paradigm to each retained study while preserving hybrid features as auxiliary tags.

## Primary-paradigm decision rules

Apply the following questions in order:

1. Does the paper's main reported repair gain come from adapting the backbone model on repair data?
   If yes, assign `Fine-Tuning`.
2. Otherwise, does the runtime issue at most one LLM generation per defect?
   If yes, assign `Prompting`.
3. Otherwise, is branching and iteration fixed by handwritten script rather than chosen by the LLM at runtime?
   If yes, assign `Procedural`.
4. Otherwise, if at least one LLM chooses actions, search branches, or stopping decisions at runtime, assign `Agentic`.

Top-level counts in the retained 66-system corpus:

- `Fine-Tuning`: 21
- `Prompting`: 17
- `Procedural`: 15
- `Agentic`: 13

## Hybrid-handling rules

- A paper is not assigned to `Fine-Tuning` merely because it uses an already fine-tuned model inside a larger scripted or agentic workflow. Fine-tuning is the primary paradigm only when the paper's main empirical contribution is the adaptation itself.
- Retrieval and analysis are treated as auxiliary tags, not as mutually exclusive top-level paradigms.
- A paper may therefore have one primary paradigm plus auxiliary tags such as `RAG`, `AAG`, repository-level, vulnerability-repair, or educational-repair.
- Deployment scenarios are recorded separately from the primary paradigm. The paper uses five recurring scenario labels: `Localized benchmark repair`, `Repository-level issue resolution`, `Vulnerability repair`, `Educational tutoring`, and `Industrial / practitioner workflow`.

## Sub-paradigm rules

### Fine-Tuning

- `Full FT`: updates the full backbone on repair data.
- `PEFT`: updates a limited adapter subset.
- `Knowledge Distillation`: transfers repair behavior from a teacher model or rule system.
- `RLFT`: optimizes repair with reinforcement-learning-style reward signals.
- `Context-enriched FT`: injects traces, static-analysis artifacts, or retrieved repair context into training.

### Prompting

- `Zero-shot`: no demonstration examples in the repair prompt.
- `Few-shot`: prompt includes exemplar bug-fix pairs.
- `Context-enriched prompting`: a single-turn prompt whose main control structure is still one-shot prompting.
- Use the auxiliary tag `RAG` when the context enrichment comes primarily from retrieved project or API context.
- Use the auxiliary tag `AAG` when the context enrichment comes primarily from analysis artifacts such as failing-test evidence, slices, traces, or diagnostics.

### Procedural

- `Test-in-the-Loop`: repeated regeneration is driven primarily by test execution feedback.
- `Human-in-the-Loop`: developer feedback is explicitly interleaved with model calls.
- `Context-enriched scripted loop`: the scripted loop repeatedly inserts external evidence between model calls.
- Use the auxiliary tag `RAG` when that inserted evidence is primarily retrieved repository or documentation context.
- Use the auxiliary tag `AAG` when the scripted loop repeatedly consumes analysis artifacts.

Clarification: failing tests can appear in two roles. Raw pass/fail feedback that drives repeated regeneration is coded as `Test-in-the-Loop`, whereas richer artifacts such as traces, slices, predicate facts, or sanitizer logs are coded as `AAG`-tagged context-enriched scripted loops.

### Agentic

- `Tool-Augmented Agents`: an LLM chooses tools or actions inside a fixed outer skeleton.
- `LLM-as-Judges`: an LLM critic gates which candidate patches or search branches survive.
- `Self-Controlled System`: one or more LLMs also plan the high-level workflow, spawn sub-tasks, or decide termination.

## Intended use

This guide is designed to make corpus-level coding reproducible. It should be read together with the released stage files, `taxonomy_assignment_audit.csv`, `scenario_assignment_audit.csv`, and the paper's detailed system table rather than as a claim that all hybrids are reducible to a single ingredient.
