# Survey Artifact Files

This directory supplements the survey repository with auditable files referenced by the current manuscript.

Included files:

- `manuscript_artifact_mapping.md`: artifact-side index that maps manuscript counts, audit statistics, benchmark tables, and challenge evidence to their source files and reproduction scripts.
- `search_keywords_and_filters.md`: readable map from the paper's search description to the executable keyword lists and screening functions in the repo-root script `remote_results/pipeline.py`.
- `screening_transparency.md`: exact counts for the released screening stages, the stage-to-stage delta, the citation-chasing supplements, and the screening-agreement evidence used in the current manuscript.
- `reproduce_screening_counts.py`: script that reproduces the current screening-flow counts from the released stage files and current corpus decisions.
- `screening_count_reproduction_2026-05-01.json`: machine-readable output from `reproduce_screening_counts.py`.
- `screening_annotation_instructions.md`: English instructions for independently screening the 474 candidate records under the released inclusion/exclusion protocol.
- `screening_annotation_template_474.csv`: blank two-coder annotation sheet for screening the 474 full-text candidates in the current manuscript screening flow.
- `screening_reference_labels_474.csv`: current final include/exclude reference labels for the same 474 candidates, derived from the retained studies, archival-status decisions, and the conservative exclusion audit.
- `selection_reference_474_final_adjudicated.csv`: final adjudicated 474-record selection sheet used for the screening-agreement audit reported in the manuscript.
- `selection_reference_474_final_adjudicated_summary.json`: machine-readable agreement summary for the final 474-record screening audit, including raw two-coder agreement and a post-adjudication consistency check with the final reference corpus.
- `screening_agreement_labels_474.csv`: per-record audit-coder decisions and adjudication notes used to inspect the screening audit.
- `compute_screening_agreement.py`: lightweight script for recomputing raw two-coder include/exclude agreement and the post-adjudication consistency check from `screening_agreement_labels_474.csv`.
- `full_text_exclusion_breakdown.csv`: final 408-record full-text exclusion breakdown used in the manuscript, with operational definitions and representative examples for each exclusion category.
- `notable_boundary_records.csv`: checked boundary records that are relevant to adjacent issue-resolution terminology but are not part of the final 66-system corpus, including whether each record would change the taxonomy dimensions or protocol-comparison windows.
- `stage4_to_stage5_delta.csv`: machine-readable list of the 14 additions and 1 removal between the released `remote_results/stage4.jsonl` and `remote_results/stage5.jsonl` files.
- `taxonomy_coding_guide.md`: operational rules for coding parameter adaptation, runtime control, control subtype, auxiliary evidence tags, and scenario labels, including hybrid-handling guidance and corpus-level display groups.
- `taxonomy_assignment_audit.csv`: machine-readable export of the final 66-system audit table used in the paper, including display paradigm, control subtype, benchmark family, metric, and explicit assumptions.
- `scenario_assignment_audit.csv`: per-paper deployment-scenario assignments used to replace the earlier qualitative scenario-fit figure with evidence-backed counts.
- `extraction_form_fields.md`: field-by-field description of the shared extraction form used for the current per-paper audit.
- `extraction_form_template.csv`: blank extraction template that mirrors the fields populated in the released audit tables.
- `taxonomy_sensitivity_audit.md`: robustness check showing how stable the display-paradigm labels remain under a stricter control-first re-coding pass.
- `human_taxonomy_annotation_instructions.md`: handoff instructions for collecting human double-coding evidence for the current manuscript audit.
- `human_taxonomy_annotation_template.csv`: blank annotation template aligned with the current taxonomy and scenario fields.
- `compute_annotation_agreement.py`: lightweight script for computing agreement statistics and enumerating disagreement rows once two coders have filled the template.
- `human_taxonomy_annotation_independent_pair.csv`: normalized paired annotation sheet for the two independent taxonomy coders, compatible with `compute_annotation_agreement.py`.
- `taxonomy_three_coder_audit.csv`: normalized three-coder taxonomy audit combining the released coding sheet with the two independent recoding sheets.
- `taxonomy_three_coder_agreement_summary.md`: historical pairwise Cohen's kappa and three-coder Fleiss kappa summary for the 62-system core recoding audit; the manuscript-facing final-corpus audit is superseded by `taxonomy_independent_pair_66_agreement_summary.md`.
- `taxonomy_independent_pair_66_audit.csv`: normalized two-independent-coder audit sheet over the final 66-system corpus.
- `taxonomy_independent_pair_66_agreement_summary.md`: manuscript-facing 66-system taxonomy reliability summary, reporting independent-coder agreement on display paradigm, control subtype, auxiliary tags, and deployment scenario.
- `exclusion_pattern_audit.csv`: a curated high-confidence audit sample of excluded records that explains why a subset of the full-text exclusions is unsurprising.
- `benchmark_protocol_summary.md`: corpus-level summary of metrics, assumptions, and benchmark concentration derived from the 66-system audit table used in the paper.
- `benchmark_family_breakdown.md`: benchmark-family-level counts derived from the final 66-system audit table, used to support the current corpus-context and benchmark-protocol synthesis.
- `analyze_benchmark_comparability.py`: script that identifies protocol-aligned benchmark comparison windows from `taxonomy_assignment_audit.csv`.
- `benchmark_protocol_comparability_by_system.csv`: 66-row per-system comparability audit showing the benchmark, metric, result, assumption bucket, comparison-window assignment, and reason why a row is or is not rankable.
- `benchmark_protocol_comparability_windows.csv`: compact summary of the protocol-aligned comparison windows used to support the revised RQ3 analysis.
- `benchmark_protocol_coverage_groups.csv`: full-corpus same-benchmark/family grouping table that assigns all 66 retained systems to a protocol coverage group even when direct score ranking is not valid.
- `benchmark_passk_distribution_by_year.csv`: year-level counts behind the manuscript's pass@k reporting-distribution table.
- `benchmark_passk_distribution_by_k.csv`: metric-family counts and system lists used to audit pass@1, pass@5, pass@10, and other reporting choices.
- `benchmark_swebench_verified_context.csv`: SWE-bench Verified pass@1 rows available in surveyed-paper contexts; rows cited to SWE-RL are explicitly marked as comparison baselines rather than the original systems' own reports.
- `benchmark_protocol_comparability.md`: human-readable benchmark-comparability analysis, including the protocol-aligned windows, full-corpus coverage groups, and manuscript consistency checks.
- `requirements.txt`: minimal Python dependency list for full-text PDF extraction.
- `extract_pdf_text_cache.py`: utility that extracts local full-text PDFs into the ignored cache directory `artifact/pdf_text_cache/` for evidence-audit scripts.
- `audit_evaluation_reliability.py`: script that links the 66 retained systems to local full-text PDFs, extracts candidate evidence snippets, and regenerates the leakage/validation rows in `evaluation_reliability_risk_coding.csv`.
- `evaluation_reliability_candidate_snippets.csv`: keyword-based candidate snippets for contamination/leakage and validation evidence, used as an inspection aid rather than as final labels.
- `evaluation_reliability_by_system.csv`: final per-system evidence table for explicit contamination/leakage reporting and validation beyond ordinary public tests.
- `evaluation_reliability_risk_coding.csv`: corpus-level coding behind the manuscript's evaluation-reliability risk table, including perfect fault localization, train/test split, explicit contamination/leakage discussion, active leakage mitigation/control, narrowed scope, metric heterogeneity, comparability tier, acceptance-gate counts, and extra-validation counts.
- `challenge_evidence_profile.csv`: sub-challenge evidence profile used in Section 10, linking each open challenge to corpus counts, source files, and representative systems.
- `version_status_audit.md`: arXiv-to-venue status audit showing which retained studies now have verified archival publications and which remain arXiv-only in the current bibliography.

Scope note:

- These files document the released stage logs, current screening decisions, agreement summaries, and coding rules used by the manuscript.
- Current screening agreement is reported from the released 474-record adjudicated selection files listed above.
- Screening-decision agreement is reproducible from `screening_agreement_labels_474.csv` by running `python3 artifact/compute_screening_agreement.py artifact/screening_agreement_labels_474.csv`.
- Manuscript-facing taxonomy agreement is reported from `taxonomy_independent_pair_66_audit.csv` and summarized in `taxonomy_independent_pair_66_agreement_summary.md`; for deterministic auxiliary-tag and scenario fields, the manuscript reports complete raw agreement (66/66) rather than emphasizing perfect kappa values. The older 62-system three-coder file is retained as an audit trail.
- The taxonomy sensitivity audit is a separate robustness check for taxonomy coding stability.
- Evaluation-reliability leakage and extra-validation counts are reproducible from the local retained-paper PDFs. If `artifact/pdf_text_cache/manifest.csv` is absent, first install the extraction dependency with `python3 -m pip install -r artifact/requirements.txt`, run `python3 artifact/extract_pdf_text_cache.py`, and then run `python3 artifact/audit_evaluation_reliability.py`.
