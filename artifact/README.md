# Survey Artifact Files

This directory supplements the survey repository with auditable files referenced by the current manuscript.

Included files:

- `search_keywords_and_filters.md`: readable map from the paper's search description to the executable keyword lists and screening functions in `remote_results/pipeline.py`.
- `screening_transparency.md`: exact counts for the released screening stages, the stage-to-stage delta, the explicit manual supplements, and a scope note on what is and is not recoverable from the current public logs.
- `reproduce_screening_counts.py`: script that reproduces the current integrated screening-flow counts from the released stage files and current update decisions.
- `screening_count_reproduction_2026-05-01.json`: machine-readable output from `reproduce_screening_counts.py`.
- `screening_annotation_template_474.csv`: blank two-coder annotation sheet for re-screening the 474 full-text candidates in the current manuscript screening flow.
- `screening_reference_labels_474.csv`: current final include/exclude reference labels for the same 474 candidates, derived from the retained studies, the published-update decisions, and the conservative exclusion audit.
- `selection_reference_474_final_adjudicated.csv`: final adjudicated 474-record selection sheet used for the screening-agreement audit reported in the manuscript.
- `selection_reference_474_final_adjudicated_summary.json`: machine-readable agreement summary for the final 474-record screening audit, including include/exclude agreement, exclusion-reason agreement, and the raw third screening pass.
- `screening_annotation_template_462.csv` and `screening_reference_labels_462.csv`: frozen pre-update annotation sheets kept for traceability to the originally released stage-5 records.
- `screening_annotation_instructions_zh.md`: Chinese instructions for external annotators who will re-screen the full-text candidate records.
- `stage4_to_stage5_delta.csv`: machine-readable list of the 14 additions and 1 removal between the released `stage4.jsonl` and `stage5.jsonl` files.
- `taxonomy_coding_guide.md`: operational rules for assigning one primary paradigm plus auxiliary tags, including hybrid-handling guidance and top-level corpus counts.
- `taxonomy_assignment_audit.csv`: machine-readable export of the final 66-system audit table used in the paper, including primary paradigm, sub-paradigm, benchmark family, metric, and explicit assumptions.
- `scenario_assignment_audit.csv`: per-paper deployment-scenario assignments used to replace the earlier qualitative scenario-fit figure with evidence-backed counts.
- `extraction_form_fields.md`: field-by-field description of the shared extraction form used for the current per-paper audit.
- `extraction_form_template.csv`: blank extraction template that mirrors the fields populated in the released audit tables.
- `taxonomy_sensitivity_audit.md`: robustness check showing how stable the primary-paradigm labels remain under a stricter control-first re-coding pass.
- `human_taxonomy_annotation_instructions.md`: handoff instructions for collecting human double-coding evidence for the current manuscript audit.
- `human_taxonomy_annotation_instructions_zh.md`: Chinese handoff note for distributing the same annotation package to external coders.
- `human_taxonomy_annotation_template.csv`: blank annotation template aligned with the current taxonomy and scenario fields.
- `compute_annotation_agreement.py`: lightweight script for computing agreement statistics and enumerating disagreement rows once two coders have filled the template.
- `human_taxonomy_annotation_external_pair.csv`: normalized paired annotation sheet for the two external taxonomy coders, compatible with `compute_annotation_agreement.py`.
- `taxonomy_three_coder_audit.csv`: normalized three-coder taxonomy audit combining the released coding sheet with the two external recoding sheets.
- `taxonomy_three_coder_agreement_summary.md`: pairwise Cohen's kappa and three-coder Fleiss kappa summary for the 62-system pre-update core recoding audit; the current 66-system taxonomy assignment is recorded in `taxonomy_assignment_audit.csv`.
- `exclusion_pattern_audit.csv`: a curated high-confidence audit sample of excluded records that explains why a subset of the full-text exclusions is unsurprising.
- `benchmark_protocol_summary.md`: corpus-level summary of metrics, assumptions, and benchmark concentration derived from the 66-system audit table used in the paper.
- `benchmark_family_breakdown.md`: benchmark-family-level counts derived from the final 66-system audit table, used to support the current corpus-context and benchmark-protocol synthesis.
- `version_status_audit.md`: arXiv-to-venue status audit showing which retained studies now have verified archival publications and which remain arXiv-only in the current bibliography.

Scope note:

- These files document the released stage logs and the current coding rules.
- They do not reconstruct the original random-sample false-negative log from query refinement, because that intermediate record is not present in the currently released stage files.
- Current screening agreement is reported from the released 474-record adjudicated selection files listed above. The taxonomy sensitivity audit is a separate robustness check for taxonomy coding stability.
