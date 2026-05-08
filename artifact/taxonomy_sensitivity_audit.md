# Taxonomy Sensitivity Audit

This file records the current human coding audit for the taxonomy coding rules.

Purpose:

- test whether the released coding guide yields stable primary-paradigm and core-subtype assignments for the 62-system audit subset
- make the remaining hybrid edge cases explicit

This audit is a taxonomy robustness check. It is separate from the 474-record screening-agreement audit documented in `screening_transparency.md`.

## Procedure

1. Give two external coders the same 62-system audit subset and the same `taxonomy_coding_guide.md`.
2. Ask each coder to assign the primary paradigm, core subtype, retrieval tag, analysis tag, and primary deployment scenario.
3. Compute agreement before adjudication with `compute_annotation_agreement.py`.
4. Adjudicate the remaining boundary cases against the full texts before merging the labels into the current 66-system coding sheet.

## Result

- Primary-paradigm agreement: `61 / 62 = 98.4%`
- Cohen's kappa on the four-way primary-paradigm label: `0.978`
- Core-subtype agreement: `60 / 62 = 96.8%`
- Cohen's kappa on the core-subtype label: `0.965`
- Retrieval-tag agreement: `62 / 62 = 100.0%`
- Analysis-tag agreement: `62 / 62 = 100.0%`
- Primary-scenario agreement between the two external recodings: `62 / 62 = 100.0%`
- Rows with at least one disagreement: `2`

## Borderline cases

| System | Disagreed fields | Coder 1 label | Coder 2 label | Why this case is borderline |
|---|---|---|---|---|
| `PATCH` | primary paradigm and core subtype | `Agentic` / `Self-Controlled System` | `Procedural` / `Scripted Tool Loop` | The paper studies patch-assessment and overfitting workflows; the boundary is whether its model-guided decision process should be treated as runtime self-control or as a scripted assessment loop. |
| `TSAPR` | core subtype | `Self-Controlled System` | `LLM-as-Judges` | The tree-search framework combines search control with an LLM judge, making the finer core-subtype label less obvious even though both coders agree on the top-level Agentic paradigm. |

## Scenario-label note

The primary-scenario number above reports agreement between the two external recodings. A separate three-coder check that also includes the pre-existing scenario projection is documented in `taxonomy_three_coder_agreement_summary.md`; it yields lower scenario agreement because 10 older scenario projections needed boundary adjudication against benchmark scope and full-text evidence. The manuscript therefore treats scenario labels as descriptive deployment-scope projections, not as taxonomy-defining labels.

## Interpretation

The main consequence of this audit is that the taxonomy is stable at the top level, while hybrid and assessment-oriented systems are exactly where disagreements concentrate. This supports the current manuscript's decision to:

- keep one primary paradigm for corpus-level aggregation
- record retrieval, analysis, and deployment scenario separately
- document the explicit hybrid edge cases rather than pretending the boundaries are perfectly crisp

## Follow-up path

The source annotation file is `human_taxonomy_annotation_external_pair.csv`, and the agreement numbers above are reproduced by `compute_annotation_agreement.py`.
