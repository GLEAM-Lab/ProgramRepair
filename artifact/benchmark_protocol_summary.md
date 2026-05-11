# Benchmark Protocol Summary

This summary aggregates the 66-system audit table used in the current manuscript to make benchmark fragmentation easier to inspect.

## Metric families

Among the 66 retained systems:

- 21 report `pass@1`
- 28 report `pass@k` for `k > 1`
- 4 report `full match`
- 2 report `F1`
- 1 reports `accuracy`
- 1 reports `avg@5`
- 1 reports `merged PRs`
- 1 reports `CodeBLEU similarity`
- 1 reports `accept@1`
- 3 report `EM`
- 1 reports `success rate`
- 1 reports `repair accuracy`

This explains why cross-paper ranking is difficult even within the same benchmark family.

## Protocol-aligned comparison windows

We therefore identify comparison windows conservatively. The full per-system audit is in
`benchmark_protocol_comparability_by_system.csv`, and the compact window summary is in
`benchmark_protocol_comparability_windows.csv`.

The final 66-system audit supports three useful windows:

- `EvalRepair-Java`, `pass@10`, `CodeLlama 13B`, no fault-location prompt: 2 systems. This is the cleanest model-controlled fine-tuning comparison window in the current audit, while training data, objective, and federated versus multi-objective setup remain different.
- `SWE-bench Lite`, `pass@1`: 8 systems. This is comparable as whole system+model stacks, but not as isolated algorithm effects because base models, search budgets, cost, and validation depth differ.
- `HumanEval-Java`, `pass@10`, PEFT-oriented systems: 3 systems. This supports a limited same-benchmark/metric comparison, but it does not control base model, training objective, or localization assumption.

All remaining rows should be treated as protocol snapshots rather than global leaderboard entries.

## Same-benchmark/family coverage groups

The bounded windows are intentionally small. To avoid under-analyzing the rest of the corpus, we also assign every retained system to a same-benchmark or same-family protocol group in `benchmark_protocol_coverage_groups.csv`. This second layer covers all 66 systems while preserving why their scores should not be ranked directly.

- Defects4J localized/Perfect-FL group: 6 systems
- Defects4J single-function group: 3 systems
- Defects4J tool/search group without explicit Perfect-FL control: 2 systems
- Defects4J single-hunk singleton: 1 system
- HumanEval-Java pass@10 group: 3 systems
- HumanEval-Java non-pass@10 group: 3 systems
- EvalRepair-Java augmented benchmark group: 2 systems
- SWE-bench Lite pass@1 group: 8 systems
- Other SWE-bench variants: 3 systems
- Vulnerability/API/crash repair group: 11 systems
- Other task-specific or singleton benchmarks, including QuixBugs, BugsInPy, RepoBugs, DS-1000, TutorCode, Flink, and Google accept@1: 24 systems

This makes benchmark comparability a positive analysis result: a few windows support bounded comparison, while the full-corpus grouping reveals where the field lacks shared protocols.

## Evaluation-readiness signals used in Section 10

The open-challenge sub-challenge table in the manuscript uses the following aggregate signals from the released audit files:

- 38/66 systems use proprietary/API models, 27/66 use open or academic models, and 1/66 does not specify the base model.
- 19/21 fine-tuning systems use open or academic models, while 37/45 prompting, procedural, and agentic systems use proprietary/API models.
- 10/66 systems explicitly assume `Perfect Fault Localization`, 7/66 use train/test split style evaluation, and 6/66 narrow repair to single-function, single-hunk, code-region, or function-level settings.
- 36/66 systems explicitly discuss benchmark, pretraining, train/test, temporal, or corpus contamination/leakage risk.
- 28/66 systems report an active mitigation or diagnostic control, such as decontamination, temporal or train/test split design, benchmark construction to avoid overlap, dataset exclusion, or leakage analysis tied to evaluation.
- 39/66 systems use hidden, held-out, or additional tests, manual/expert review, LLM/human review, static/runtime validation, sanitizer/exploit reproduction, or a comparable independent validation signal beyond ordinary public benchmark tests.
- 21/66 systems report `pass@1`, 28/66 report larger pass@k candidate-budget metrics, and 17/66 use single-candidate or non-pass@k task-specific metrics.
- 13/66 systems fall into model-controlled, protocol-aligned, or limited within-benchmark comparison tiers, while 53/66 are snapshot-only rows.
- 13/66 systems target repository-level issue resolution, including 8 agentic systems.
- 28/66 systems are procedural or agentic, meaning the repair process is explicitly organized as a multi-step scripted or model-controlled loop.
- Within these loop-oriented systems, the taxonomy records 8 scripted tool loops, 7 tool-augmented agent systems, 4 test-in-the-loop workflows, and 3 self-controlled systems.
- The manuscript taxonomy table records explicit retrieval-enriched prompting/procedural rows for 7 systems, explicit analysis-enriched prompting/procedural rows for 10 systems, 4 test-feedback loops, and 3 human-feedback loops.
- 10/66 systems use test feedback, human feedback, or LLM-as-judge review as the recorded control subtype; the complementary 56/66 do not expose such an acceptance gate as their main repair-control mechanism.
- Security/API/crash repair covers 11 systems, and repository-level issue resolution covers 13 systems.

The row-level source table for these Section 10 challenge and sub-challenge signals is `challenge_evidence_profile.csv`.

For the model-dependency count, the grouping is derived from the recorded `base_model` field: GPT, Claude, Gemini, and Codex variants are counted as proprietary/API models; CodeLlama, DeepSeek, Llama, StarCoder, CodeT5, CodeGen, Qwen, Incoder, and CodeBERT variants are counted as open or academic models; `/` is counted as not specified. The mixed `GPT-4 + CodeT5P` row is counted as proprietary/API because the reported repair loop uses GPT-4.

## Explicit assumptions in the 66-system audit table

- 10 systems explicitly assume `Perfect Fault Localization`
- 3 systems explicitly narrow the task to `single-function` repair
- 1 system explicitly narrows the task to `single-hunk` repair
- 1 system explicitly reports `code-region` localization
- 1 system explicitly reports a function-level vulnerability-patch setting
- 10 systems use test feedback, human feedback, or LLM-as-judge review as the recorded control subtype
- 7 systems explicitly frame evaluation around a train/test split
- 36 systems explicitly report contamination/leakage discussion or control
- 39 systems use extra validation signals beyond ordinary public benchmark tests

The first five assumption rows indicate that at least 16 systems use a narrowed setup that is weaker than fully end-to-end repair, even before considering differences in sampling budget, benchmark version, or oracle strength. The leakage-reporting and extra-validation rows are tracked separately because they improve protocol transparency but remain too heterogeneous to normalize into a single comparable repair score.

## Selected recurring benchmark families in the 66-system table

- `Defects4J` family (`v1.2` plus `v1.2/2.0`): 12 systems
- `HumanEval-Java`: 6 systems
- `EvalRepair-Java`: 2 systems
- `SWE-bench Lite`: 8 systems
- `SWE-bench Verified`: 1 directly benchmarked system
- `Vulnerability repair datasets`: 9 systems across seven metric families
- `API misuse repair`: 1 system
- `Crash bug repair`: 1 system

The remaining systems are spread across many smaller or domain-specific datasets, which is one reason vulnerability-repair and educational-repair results remain hard to compare globally. The more detailed family-by-family counts are summarized in `benchmark_family_breakdown.md`.

## Manuscript consistency check

The current manuscript is synchronized with the final 66-system audit. The SWE-bench protocol table uses `MAGIS` for the SWE-bench Lite `pass@1` row and keeps `TSAPR` only in the Defects4J table, matching `taxonomy_assignment_audit.csv`.

The remaining alignment checks are also reflected in the manuscript tables: `KNOD` uses `Not specified` as the base model, `TSAPR` is not marked as a Perfect-FL row, and the fragmented security/API/crash table follows the final audit's metric labels, including `pass@1`/`pass@5` rows when they match the paper's candidate-budget definition.
