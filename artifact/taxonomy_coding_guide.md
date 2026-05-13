# Taxonomy Coding Guide

This guide records the operational rules used to code each retained study along multiple dimensions: parameter adaptation, runtime control, control subtype, auxiliary evidence tags, and deployment scenario. The manuscript derives a compact display paradigm from parameter adaptation and runtime control for corpus-level aggregation while preserving hybrid features as auxiliary evidence tags.

## Display-paradigm derivation rules

Apply the following questions in order:

1. Does the paper's main reported repair gain come from adapting the backbone model on repair data?
   If yes, assign `Fine-Tuning`.
2. Otherwise, does the runtime issue at most one LLM generation per defect?
   If yes, assign `Prompting`.
3. Otherwise, is branching and iteration fixed by handwritten script rather than chosen by the LLM at runtime?
   If yes, assign `Procedural`.
4. Otherwise, if at least one LLM chooses actions, search branches, or stopping decisions at runtime, assign `Agentic`.

Display-group counts in the retained 66-system corpus:

- `Fine-Tuning`: 21
- `Prompting`: 17
- `Procedural`: 15
- `Agentic`: 13

## Hybrid-handling rules

- A paper is not assigned to the `Fine-Tuning` display group merely because it uses an already fine-tuned model inside a larger scripted or agentic workflow. Fine-tuning is used as the display group only when the paper's main empirical contribution is the adaptation itself.
- Retrieval, analysis, tests, human feedback, and domain knowledge are treated as auxiliary evidence tags, not as mutually exclusive top-level paradigms or sub-paradigms.
- A paper may therefore have one display paradigm, one control subtype, and auxiliary tags such as `RAG`, `AAG`, `test feedback`, `human feedback`, or `domain knowledge`.
- Deployment scenarios are recorded separately from the display paradigm. The paper uses five recurring scenario labels: `Localized benchmark repair`, `Repository-level issue resolution`, `Vulnerability repair`, `Educational tutoring`, and `Industrial / practitioner workflow`.

## Control-subtype rules

### Fine-Tuning

- `Full FT`: updates the full backbone on repair data.
- `PEFT`: updates a limited adapter subset.
- `Knowledge Distillation`: transfers repair behavior from a teacher model or rule system.
- `RLFT`: optimizes repair with reinforcement-learning-style reward signals.
If a fine-tuned system injects traces, static-analysis artifacts, retrieved repair context, templates, or domain hints into training, keep the control subtype above and record the evidence source as an auxiliary tag.

### Prompting

- `Zero-shot`: no demonstration examples in the repair prompt.
- `Few-shot`: prompt includes exemplar bug-fix pairs.
Keep the control subtype as `Zero-shot` or `Few-shot` even when the prompt includes additional evidence. Use the auxiliary tag `RAG` when the added evidence comes primarily from retrieved project, API, documentation, or historical-fix context. Use the auxiliary tag `AAG` when the added evidence comes primarily from analysis artifacts such as failing-test evidence, slices, traces, diagnostics, or mined program facts.

### Procedural

- `Test-in-the-Loop`: repeated regeneration is driven primarily by test execution feedback.
- `Human-in-the-Loop`: developer feedback is explicitly interleaved with model calls.
- `Scripted Tool Loop`: deterministic retrieval, analysis, validation, or other tool stages are inserted between model calls, while the next control step remains hard-coded by the system designer.
Use the auxiliary tag `RAG` when inserted evidence is primarily retrieved repository, documentation, API, or historical-fix context. Use the auxiliary tag `AAG` when the scripted loop consumes analysis artifacts.

Clarification: failing tests can appear in two roles. Raw pass/fail feedback that drives repeated regeneration is coded as `Test-in-the-Loop`, whereas richer artifacts such as traces, slices, predicate facts, or sanitizer logs are coded as `Scripted Tool Loop` with an `AAG` tag.

### Agentic

- `Tool-Augmented Agents`: an LLM chooses tools or actions inside a fixed outer skeleton.
- `LLM-as-Judges`: an LLM critic gates which candidate patches or search branches survive.
- `Self-Controlled System`: one or more LLMs also plan the high-level workflow, spawn sub-tasks, or decide termination.

## Intended use

This guide is designed to make corpus-level coding reproducible. It should be read together with the released stage files, `taxonomy_assignment_audit.csv`, `scenario_assignment_audit.csv`, and the paper's detailed system table rather than as a claim that all hybrids are reducible to a single ingredient.
