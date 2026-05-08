# Screening Annotation Instructions

This file describes the independent screening protocol for the 474 candidate records used in the current manuscript.

## Goal

For each candidate record, decide whether it should be included in the final survey corpus under the released inclusion and exclusion criteria.

Use `screening_annotation_template_474.csv` as the blank annotation sheet. The adjudicated reference labels are released in `selection_reference_474_final_adjudicated.csv`, and the agreement summary is released in `selection_reference_474_final_adjudicated_summary.json`.

## Include A Record If

- The study proposes, implements, or evaluates an LLM-based software repair system.
- The LLM is a central component of the repair pipeline at inference time, such as patch generation, code editing, patch ranking, patch validation, or multi-step repair orchestration.
- The study reports empirical evaluation on a reproducible repair dataset, benchmark, issue set, vulnerability set, or clearly described defect corpus.
- The record is the most complete archival or retained arXiv version available under the manuscript's venue and version-status rules.

## Exclude A Record If

- It is a survey, position paper, vision paper, benchmark-only paper, or empirical study without a concrete repair system.
- It focuses only on vulnerability detection, fault localization, bug prediction, test generation, code generation, code review, or program comprehension without generating or validating repairs.
- It uses LLMs only for data synthesis, labeling, explanation, or commentary rather than as a central repair component.
- It is outside software repair, such as image patching, hardware patching, medical image analysis, or unrelated patch terminology.
- It is a duplicate, superseded preprint, or shorter version of an included archival paper.

## Label Fields

- `include`: the record satisfies the inclusion criteria.
- `exclude`: the record does not satisfy the inclusion criteria.

For excluded records, use the closest exclusion reason from the released protocol and add a short note when the boundary is non-obvious.

## Adjudication

Disagreements are resolved against the paper title, abstract, venue record, DOI/arXiv metadata, and full text when available. The final adjudicated sheet preserves the 66-system corpus used by the manuscript.
