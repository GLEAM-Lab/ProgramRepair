# Taxonomy Sensitivity Audit

This file records the current human coding audit for the taxonomy coding rules.

Purpose:

- test whether the released coding guide yields stable display-paradigm and control-subtype assignments for the final 66-system corpus
- make the remaining hybrid edge cases explicit

This audit is a taxonomy robustness check. It is separate from the 474-record screening-agreement audit documented in `screening_transparency.md`.

## Procedure

1. Give two independent coders the same final 66-system corpus and the same `taxonomy_coding_guide.md`.
2. Ask each coder to assign the display paradigm, control subtype, retrieval tag, analysis tag, and deployment scenario.
3. Compute agreement before adjudication with `compute_annotation_agreement.py`.
4. Adjudicate the remaining boundary cases against the full texts before merging the labels into the current 66-system coding sheet.

The current manuscript-facing pairwise statistics use `taxonomy_external_pair_66_audit.csv`, which integrates the 62-system independent-pair recoding sheet and the four later-system independent recodings into one normalized 66-system audit table.

## Result

- Display-paradigm agreement: `65 / 66 = 98.5%`
- Cohen's kappa on the four-way display-paradigm label: `0.980`
- Control-subtype agreement: `64 / 66 = 97.0%`
- Cohen's kappa on the control-subtype label: `0.967`
- Retrieval-tag agreement: `66 / 66 = 100.0%`
- Analysis-tag agreement: `66 / 66 = 100.0%`
- Deployment-scenario agreement between the two independent recodings: `66 / 66 = 100.0%`
- Rows with at least one disagreement: `2`

## Borderline cases

| System | Disagreed fields | Coder 1 label | Coder 2 label | Why this case is borderline |
|---|---|---|---|---|
| `PATCH` | display paradigm and control subtype | `Agentic` / `Self-Controlled System` | `Procedural` / `Scripted Tool Loop` | The paper studies patch-assessment and overfitting workflows; the boundary is whether its model-guided decision process should be treated as runtime self-control or as a scripted assessment loop. |
| `TSAPR` | control subtype | `Self-Controlled System` | `LLM-as-Judges` | The tree-search framework combines search control with an LLM judge, making the finer control-subtype label less obvious even though both coders agree on the Agentic display paradigm. |

## Scenario-label note

The deployment-scenario number above reports agreement between the two independent recodings. A separate three-coder check that also includes the existing scenario sheet is documented in `taxonomy_three_coder_agreement_summary.md`; it yields lower scenario agreement because 10 older scenario labels needed adjudication against benchmark scope and full-text evidence. The manuscript therefore treats scenario labels as descriptive deployment-scope labels, not as display-paradigm labels.

## Interpretation

The main consequence of this audit is that the taxonomy is stable at the display-paradigm level, while hybrid and assessment-oriented systems are exactly where disagreements concentrate. This supports the current manuscript's decision to:

- keep one display paradigm for corpus-level aggregation
- record retrieval, analysis, and deployment scenario separately
- document the explicit hybrid edge cases rather than pretending the boundaries are perfectly crisp

## Follow-up path

The source annotation file is `taxonomy_external_pair_66_audit.csv`, and the agreement numbers above are reproduced by `compute_annotation_agreement.py`.
