# Screening Transparency Note

This note documents the screening-flow evidence used by the current manuscript and the released artifacts that reproduce the reported counts.

Source files:

- `remote_results/stage4.jsonl`
- `remote_results/stage5.jsonl`
- `remote_results/stage6.jsonl`

## Current manuscript screening-flow counts

The current manuscript reports the following screening flow:

- Search query hits: 2,317
- Repair-related filter: 1,020
- LLM-related filter: 752
- Benchmark-related filter: 461
- Snowballing: 474
- Retained works: 66

These counts are reproduced by `artifact/reproduce_screening_counts.py`, with the machine-readable output saved in `artifact/screening_count_reproduction_2026-05-01.json`. This yields a final retention rate of `66 / 474 = 13.9%`.

## Legacy released stage-file counts

The released stage files provide the base flow before the current archival-status supplements. They are retained as an audit trail and are not the current manuscript totals:

- `stage4.jsonl`: 449 candidate records after the automatic benchmark-oriented filter.
- `stage5.jsonl`: 462 candidate records before final full-text screening.
- `stage6.jsonl`: 62 retained representative studies before the current archival-status supplements.

The current archival-status supplements add 12 full-text candidates and 4 retained core systems under the same eligibility criteria, producing the current 461, 474, and 66 manuscript counts above. The current totals are therefore the counts reproduced by `artifact/reproduce_screening_counts.py`, not the legacy `stage6.jsonl` count alone.

## Released stage delta: `stage4 -> stage5`

Comparing the released `stage4.jsonl` and `stage5.jsonl` files yields a net change of `+13` records:

- 14 records are present in `stage5.jsonl` but not in `stage4.jsonl`.
- 1 record is present in `stage4.jsonl` but not in `stage5.jsonl`.

The machine-readable delta is provided in `stage4_to_stage5_delta.csv`.

## Citation-chasing supplements visible in the released logs

Two records in the released `stage5.jsonl` and `stage6.jsonl` files are marked as citation-chasing supplements:

- `Unlocking LLM Repair Capabilities in Low-Resource Programming Languages Through Cross-Language Translation and Multi-Agent Refinement`
- `DistiLRR: Transferring Code Repair for Low-Resource Programming Languages`

These two entries show why the corpus should be interpreted as a criteria-bounded evidence corpus rather than an exhaustive census: citation chasing can identify relevant systems that are not returned by the automatic keyword filters alone.

## Independent dual-coder screening audit

The current manuscript reports a 474-record independent dual-coder screening audit based on `selection_reference_474_final_adjudicated.csv`, `screening_agreement_labels_474.csv`, and `selection_reference_474_final_adjudicated_summary.json`. This audit provides a fully auditable agreement check over the complete candidate pool using the released inclusion/exclusion protocol, and the adjudicated decisions form the final 66-system corpus used by the manuscript.

- the two audit coders agreed on `467/474` raw include/exclude decisions before adjudication (Cohen's kappa `0.9372`);
- the seven raw two-coder disagreements were adjudicated against the full texts and final eligibility criteria;
- after adjudication, the final decision sheet contains `66` included and `408` excluded records.

The include/exclude screening-decision statistics can be recomputed with:

```bash
python3 artifact/compute_screening_agreement.py artifact/screening_agreement_labels_474.csv
```

## Full-text exclusion breakdown

The final adjudicated selection sheet exposes the current per-record include/exclude labels. The file `full_text_exclusion_breakdown.csv` summarizes the 408 full-text exclusions:

| Exclusion reason | Records |
|---|---:|
| Not software repair | 141 |
| LLM not central at inference time | 82 |
| Benchmark, evaluation, or empirical study only | 65 |
| No patch-generation or repair pipeline | 58 |
| Insufficient full-text detail | 43 |
| Survey or review | 8 |
| Detection/localization only | 7 |
| Duplicate or superseded version | 3 |
| Other boundary exclusion after adjudication | 1 |

These categories sum to `408` and are aligned with the final `66 / 474` retained-corpus decision.

## Conservative exclusion-pattern examples

To make the final drop easier to inspect manually, `exclusion_pattern_audit.csv` also lists 29 high-confidence excluded records drawn from the released `stage5 - stage6` set:

- 6 survey/review papers
- 4 detection/localization-only papers
- 4 benchmark/evaluation-only papers
- 15 clearly non-code or non-software papers that matched search cues such as "repair" or "patch" in a different domain

This 29-record pattern audit is intentionally conservative: it is not the full exclusion distribution. The full exclusion breakdown is provided in `full_text_exclusion_breakdown.csv`, and the exhaustive current screening decision file is provided separately as `selection_reference_474_final_adjudicated.csv`.

## Notable boundary records

The file `notable_boundary_records.csv` documents a small set of adjacent records that were checked during revision but are not part of the final 66-system corpus. These rows are transparency notes, not additional screening records: they are not included in the 474-record denominator for the screening-agreement audit, and they do not change the reported 66 retained systems or 408 full-text exclusions. Boundary records are checked for whether they would introduce a new taxonomy dimension or protocol-aligned comparison window; the currently logged records do not change the codebook or benchmark-comparability windows. If a boundary record later enters the in-scope archival venue set, it should be handled through a future corpus update that reruns the same screening and coding protocol rather than by changing the current frozen audit denominator.

## Audit scope

The released stage files and supplemental files verify the stage counts, net deltas, final retained corpus, independent include/exclude agreement under the released protocol, the full 408-record exclusion breakdown, conservative exclusion examples, and the documented boundary notes. The manuscript uses these directly auditable files for the reported screening-flow and agreement statistics.
