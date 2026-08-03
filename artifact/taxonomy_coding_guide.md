# Taxonomy Coding Guide

This guide records the operational rules used to code each retained study. The primary display paradigm captures where repair capability and control logic principally reside. Separate fields preserve parameter adaptation, generation pattern, secondary control mechanisms, auxiliary evidence, and deployment scenario so that hybrid systems are not reduced to one ingredient.

## Display-paradigm derivation rules

Apply the following questions in order:

1. Does task-specific parameter adaptation carry the principal repair capability, and does the headline repair result depend on the adapted parameters? If yes, assign `Fine-Tuning`. Merely using an adapted checkpoint inside a larger workflow is insufficient.
2. Otherwise, do the prompt and supplied context carry the principal repair mechanism, without a designer-specified multi-stage trajectory or LLM-directed controller carrying the main result? If yes, assign `Prompting`.
3. Otherwise, does a designer-specified workflow carry the principal runtime control, including stage order, available tools, retry policy, and stopping budget? If yes, assign `Procedural`.
4. Otherwise, if LLM-directed action or tool selection, branching, regeneration, or termination is the principal runtime controller, assign `Agentic`.

For hybrids, determine the principal locus from the authors' stated contribution, workflow, headline comparisons, and ablation evidence when available. Multiple independent samples generated solely to estimate pass@k are evaluation replications, not workflow steps.

Display-group counts in the retained 66-system corpus:

- `Fine-Tuning`: 21
- `Prompting`: 17
- `Procedural`: 15
- `Agentic`: 13

## Orthogonal coding fields

- Parameter adaptation records whether and how model parameters are adapted.
- Generation pattern records zero-shot, few-shot, reasoning-prompt, or repeated-generation behavior without determining the primary paradigm by itself.
- Secondary control records coexisting scripted or learned control mechanisms.
- Auxiliary-evidence tags are non-exclusive: `retrieval`, `program-analysis evidence`, `test feedback`, `human feedback`, and `domain knowledge`.
- In the independent-pair audit, coder fields preserve pre-adjudication labels; `final_retrieval_tag` and `final_analysis_tag` record full-text adjudication without overwriting those raw labels.
- Deployment scenario is recorded separately. The recurring labels are `Localized benchmark repair`, `Repository-level issue resolution`, `Vulnerability repair`, `Educational tutoring`, and `Industrial / practitioner workflow`.

## Control-subtype rules

### Fine-Tuning

- `Full Tuning`: updates the full model on repair data.
- `Adapter Tuning`: updates adapters or another parameter-efficient subset.
- `Knowledge Distillation`: transfers repair behavior from a teacher model or rule system.
- `RL Tuning`: optimizes repair with reinforcement-learning-style reward signals.

If a fine-tuned system also uses traces, static-analysis artifacts, retrieval, templates, or domain hints, retain the Fine-Tuning subtype and record those evidence sources separately.

### Prompting

- `Zero-shot`: no demonstration bug-fix pair is supplied.
- `Few-shot`: exemplar bug-fix pairs are supplied.
- `Zero-/few-shot`: the study reports or compares both settings.

Reasoning prompts, including chain-of-thought-style prompts, are prompting attributes rather than separate control subtypes. Additional retrieval or program-analysis evidence is recorded with auxiliary-evidence tags.

### Procedural

- `Test-Feedback Loop`: a designer-specified loop uses test results to condition regeneration.
- `Human-in-the-Loop`: developer feedback is explicitly interleaved with model calls.
- `Scripted Tool Loop`: deterministic retrieval, analysis, validation, or other tool stages are inserted between model calls while the next control step remains designer-specified.

A bounded analysis, scoring, review, or validation module does not by itself make the system Agentic. Raw test feedback that drives regeneration is a Test-Feedback Loop; richer traces, slices, predicate facts, or sanitizer logs are also recorded as program-analysis evidence.

### Agentic

- `Tool-Augmented Agent`: LLM-directed tool or action selection carries runtime progression.
- `LLM-Gated Review`: learned judgment gates acceptance, branching, regeneration, or stopping. An offline score used only for evaluation is not agentic control.
- `Self-Controlled System`: one or more LLMs plan the higher-level workflow, spawn subtasks, or decide termination.

The three systems assigned to LLM-Gated Review were individually re-audited under the narrowed gate. Their evidence and outcomes are recorded in the `classification_reaudit` column of `taxonomy_assignment_audit.csv`.

## Intended use

Read this guide together with `taxonomy_assignment_audit.csv`, `taxonomy_independent_pair_66_audit.csv`, `scenario_assignment_audit.csv`, and the manuscript's detailed system table. The primary label supports corpus-level aggregation; the orthogonal fields preserve mechanisms that coexist in hybrid systems.
