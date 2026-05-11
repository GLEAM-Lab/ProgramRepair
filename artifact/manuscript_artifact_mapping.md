# Manuscript-to-Artifact Mapping

This file maps the current manuscript's reported counts, audit statistics, and synthesis tables to the released artifact files. It is the artifact-side index for checking that manuscript statements and released data use the same corpus and coding decisions.

## Search, Filtering, and Screening Flow

| Manuscript item | Artifact source | Reproduction or check |
|---|---|---|
| Search keyword families and automatic filters | `search_keywords_and_filters.md`; `remote_results/pipeline.py` | Documents query terms, filter rules, and the executable filtering logic. |
| Screening-flow counts: 2,317 -> 1,020 -> 752 -> 461 -> 474 -> 66 | `reproduce_screening_counts.py`; `screening_count_reproduction_2026-05-01.json`; `screening_transparency.md` | Run `python3 artifact/reproduce_screening_counts.py`. |
| Stage delta from benchmark filter to snowballing/manual supplements | `stage4_to_stage5_delta.csv`; `screening_transparency.md` | Documents the net `+13` records between released stage files. |
| Final 474-record screening decisions | `selection_reference_474_final_adjudicated.csv`; `screening_agreement_labels_474.csv` | Final adjudicated include/exclude labels for the 474 full-text candidates. |
| Screening agreement: 467/474 raw agreement, Cohen's kappa 0.9372 | `compute_screening_agreement.py`; `screening_agreement_labels_474.csv`; `selection_reference_474_final_adjudicated_summary.json` | Run `python3 artifact/compute_screening_agreement.py artifact/screening_agreement_labels_474.csv`. |

## Full-Text Exclusions

| Manuscript item | Artifact source | Reproduction or check |
|---|---|---|
| Full-text exclusion breakdown totaling 408 excluded records | `full_text_exclusion_breakdown.csv`; `selection_reference_474_final_adjudicated.csv`; `screening_transparency.md` | Category counts sum to the 408 excluded records in the final 474-record adjudicated sheet. |
| Conservative examples of clear exclusions | `exclusion_pattern_audit.csv`; `screening_transparency.md` | Provides high-confidence examples only; it is not the full exclusion distribution. |
| Notable adjacent or reviewer-mentioned boundary records | `notable_boundary_records.csv`; `screening_transparency.md` | Documents checked records that are not counted in the final 66-system corpus, including issue-resolution records outside the finalized auditable candidate pool. |

## Taxonomy and Scenario Coding

| Manuscript item | Artifact source | Reproduction or check |
|---|---|---|
| Multidimensional taxonomy rules | `taxonomy_coding_guide.md` | Defines display paradigm, control subtype, auxiliary evidence tags, and scenario labels. |
| Final 66-system taxonomy labels | `taxonomy_assignment_audit.csv` | Per-system display paradigm, control subtype, benchmark family, metric, and assumptions. |
| Deployment-scenario counts | `scenario_assignment_audit.csv` | Source for the deployment-scenario count table replacing the earlier qualitative fit figure. |
| 66-system external-coder taxonomy audit | `taxonomy_external_pair_66_audit.csv`; `taxonomy_external_pair_66_agreement_summary.md` | Run `python3 artifact/compute_annotation_agreement.py artifact/taxonomy_external_pair_66_audit.csv`. |
| Historical 62-system three-coder audit trail | `taxonomy_three_coder_audit.csv`; `taxonomy_three_coder_agreement_summary.md` | Retained as an audit trail; manuscript-facing final-corpus statistics use the 66-system files above. |
| Sensitivity and boundary-case discussion | `taxonomy_sensitivity_audit.md` | Documents remaining hybrid edge cases such as PATCH and TSAPR. |

## Benchmark Protocol Profiles

| Manuscript item | Artifact source | Reproduction or check |
|---|---|---|
| Per-system benchmark, metric, assumptions, and comparability tier | `benchmark_protocol_comparability_by_system.csv` | 66-row audit table used for benchmark protocol profiles. |
| Protocol-aligned comparison windows | `benchmark_protocol_comparability_windows.csv`; `benchmark_protocol_comparability.md` | Produced by `analyze_benchmark_comparability.py`. |
| Benchmark-family coverage groups | `benchmark_protocol_coverage_groups.csv`; `benchmark_family_breakdown.md` | Assigns all 66 systems to same-family or singleton benchmark groups. |
| pass@k reporting distribution | `benchmark_passk_distribution_by_year.csv`; `benchmark_passk_distribution_by_k.csv` | Source for year-level and metric-family pass@k distribution tables. |
| SWE-bench Verified context rows | `benchmark_swebench_verified_context.csv` | Records Verified pass@1 rows available in surveyed-paper contexts. |
| Evaluation-reliability risk coding | `evaluation_reliability_risk_coding.csv` | Source for perfect-FL, train/test split, narrowed-scope, metric-heterogeneity, comparability-tier, and acceptance-gate counts. |

## Open Challenges and Version Status

| Manuscript item | Artifact source | Reproduction or check |
|---|---|---|
| Evidence profile behind open challenges | `challenge_evidence_profile.csv` | Links each challenge/sub-challenge to corpus counts and representative systems. |
| arXiv-to-archival status and retained arXiv rationale | `version_status_audit.md` | Records publication-status updates and retained arXiv-only decisions. |

## Scope Notes

- The manuscript-facing corpus contains 66 retained systems and 474 full-text candidate records before final screening.
- The 29-record exclusion-pattern audit is only a conservative example set; the full exclusion distribution is `full_text_exclusion_breakdown.csv`.
- Boundary records in `notable_boundary_records.csv` are documented for transparency and are not included in the 474-record screening-agreement denominator or the final 66-system corpus.
- The manuscript-facing taxonomy reliability numbers use the final 66-system external-coder audit, not the older 62-system audit trail.
- Benchmark tables preserve published scores and protocol assumptions; they do not rerun systems or normalize candidate budgets across papers.
