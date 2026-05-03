# Screening Transparency Note

This note documents the screening-flow evidence that can be recovered from the released stage files and the published-update artifacts used by the current manuscript.

Source files:

- `remote_results/stage4.jsonl`
- `remote_results/stage5.jsonl`
- `remote_results/stage6.jsonl`

## Current manuscript screening-flow counts

The current manuscript reports one integrated screening flow:

- Search query hits: 2,317
- Repair-related filter: 1,020
- LLM-related filter: 752
- Benchmark-related filter: 461
- Snowballing: 474
- Representative works: 66

The integrated counts are reproduced by `artifact/reproduce_screening_counts.py`, with the machine-readable output saved in `artifact/screening_count_reproduction_2026-05-01.json`. This yields a final retention rate of `66 / 474 = 13.9%`.

## Frozen stage-file counts

The frozen released stage files provide the pre-update base flow:

- `stage4.jsonl`: 449 candidate records after the automatic benchmark-oriented filter.
- `stage5.jsonl`: 462 candidate records before final full-text screening.
- `stage6.jsonl`: 62 retained representative studies before the published-update additions.

The published-update artifacts add 12 full-text candidates and 4 retained core systems under the same eligibility criteria, producing the current 461, 474, and 66 manuscript counts above.

## Released stage delta: `stage4 -> stage5`

Comparing the released `stage4.jsonl` and `stage5.jsonl` files yields a net change of `+13` records:

- 14 records are present in `stage5.jsonl` but not in `stage4.jsonl`.
- 1 record is present in `stage4.jsonl` but not in `stage5.jsonl`.

The machine-readable delta is provided in `stage4_to_stage5_delta.csv`.

## Explicit manual supplements visible in the released logs

Two records in the released `stage5.jsonl` and `stage6.jsonl` files are explicitly marked as manual supplements with `source=manual_supplement` and `reason=representative_system_missed`:

- `Unlocking LLM Repair Capabilities in Low-Resource Programming Languages Through Cross-Language Translation and Multi-Agent Refinement`
- `DistiLRR: Transferring Code Repair for Low-Resource Programming Languages`

These two entries are the clearest recoverable evidence that the automatic retrieval stage missed representative systems and that the corpus should be interpreted as representative rather than exhaustive.

## Screening-agreement audit

The current manuscript reports a 474-record screening-agreement audit based on `selection_reference_474_final_adjudicated.csv` and summarized in `selection_reference_474_final_adjudicated_summary.json`:

- two external coders agreed on all include/exclude decisions (`474/474`; Cohen's kappa `1.0000`);
- the same two coders agreed on `391/408` exclusion-reason labels for excluded records (Cohen's kappa `0.8321`);
- a separate raw third screening pass agreed with the final reference labels on `467/474` records before adjudication (Cohen's kappa `0.9372`);
- the seven raw disagreements were adjudicated against the full texts and did not change the final 66-system corpus.

## Why a large full-text exclusion is plausible

The final adjudicated selection sheet exposes the current per-record include/exclude labels. To make the final drop easier to audit, `exclusion_pattern_audit.csv` also lists 29 high-confidence excluded records drawn from the pre-update `stage5 - stage6` set:

- 6 survey/review papers
- 4 detection/localization-only papers
- 4 benchmark/evaluation-only papers
- 15 clearly non-code or non-software papers that matched search cues such as "repair" or "patch" in a different domain

This 29-record pattern audit is intentionally conservative: it is not an exhaustive relabeling of all full-text exclusions, because the exhaustive current screening decision file is provided separately as `selection_reference_474_final_adjudicated.csv`.

## What the current public logs do not recover

The currently released stage files and supplemental files are sufficient to verify stage counts, net deltas, the final retained corpus, current include/exclude agreement, current exclusion-reason agreement, and a subset of obvious exclusions. They do not recover the following earlier query-refinement details:

- the exact size of the original random audit sample used during query refinement
- the exact number of false negatives found during that original audit

The manuscript therefore relies on the screening-flow evidence that can be audited directly from the released stage files and the supplemental files in this directory.
