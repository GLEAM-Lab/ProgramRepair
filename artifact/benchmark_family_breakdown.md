# Benchmark Family Breakdown

This file aggregates the final 66-system audit table into benchmark-family-level summaries so that the benchmark-protocol claims in the current manuscript can be checked directly. Counts are derived from `artifact/taxonomy_assignment_audit.csv`.

For rankability, use `artifact/benchmark_protocol_comparability_by_system.csv` and `artifact/benchmark_protocol_comparability_windows.csv`. For full-corpus coverage without invalid ranking, use `artifact/benchmark_protocol_coverage_groups.csv`. This file reports family-level concentration and fragmentation; the comparability files identify which rows can actually be compared under a common protocol, while the coverage groups show how all 66 systems participate in the benchmark audit.

## Defects4J

- Systems: 12

- Paradigm mix: Fine-Tuning=4, Prompting=3, Procedural=3, Agentic=2

- Metric mix: pass@5=1, pass@10=2, pass@1000=1, pass@1=2, pass@k (5h)=1, pass@200=1, pass@500=1, pass@25=1, pass@5000=1, pass@32=1

- Explicit `Perfect Fault Localization` assumptions: 6

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 10

- Comparability interpretation: not rankable as a single group. The family mixes benchmark versions/subsets, denominators, pass@k budgets from 1 to 5000, Perfect-FL assumptions, single-function/single-hunk settings, and repository-level execution.


## HumanEval-Java

- Systems: 6

- Paradigm mix: Fine-Tuning=4, Prompting=1, Procedural=1

- Metric mix: pass@10=3, pass@100=1, accuracy=1, pass@40=1

- Explicit `Perfect Fault Localization` assumptions: 2

- Narrowed settings (`Perfect Fault Localization`, `code-region localization`, `single-function`, or `single-hunk`): 3

- Comparability interpretation: contains one useful pass@10 PEFT-oriented window. Rows using pass@100, pass@40, or accuracy remain protocol snapshots.


## EvalRepair-Java

- Systems: 2

- Paradigm mix: Fine-Tuning=2

- Metric mix: pass@10=2

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `code-region localization`, `single-function`, or `single-hunk`): 0

- Comparability interpretation: kept separate from HumanEval-Java because EvalRepair-Java augments HumanEval-Java with additional tests and uses a different oracle protocol. The two rows share pass@10, CodeLlama 13B, and no fault-location prompt, supporting a narrow model-controlled comparison while training data and adaptation objectives still differ.


## SWE-bench Lite

- Systems: 8

- Paradigm mix: Procedural=2, Agentic=6

- Metric mix: pass@1=8

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 0

- Comparability interpretation: the cleanest whole-system comparison window in the corpus because all eight rows report SWE-bench Lite pass@1. It is still a stack comparison, not an isolated paradigm comparison, because base model, search depth, cost budget, and validation policy vary.


## SWE-bench Verified

- Systems: 1

- Paradigm mix: Fine-Tuning=1

- Metric mix: pass@1=1

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 0

- Comparability interpretation: singleton row in the current corpus; keep as a protocol snapshot.


## SWE-bench Other

- Systems: 2

- Paradigm mix: Agentic=2

- Metric mix: pass@1=2

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 0

- Comparability interpretation: not directly comparable with SWE-bench Lite or Verified because the rows use different variants or additional environment/trajectory conditions.


## Vulnerability repair datasets

- Systems: 9

- Paradigm mix: Fine-Tuning=2, Prompting=3, Procedural=3, Agentic=1

- Metric mix: EM=2, pass@1=2, full match=1, F1=1, pass@5=1, CodeBLEU similarity=1, success rate=1

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, `single-hunk`, or `function-level`): 1

- Comparability interpretation: not rankable as a group because datasets and metrics are disjoint.


## API misuse repair

- Systems: 1

- Paradigm mix: Prompting=1

- Metric mix: EM=1

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, `single-hunk`, or `function-level`): 0

- Comparability interpretation: singleton row; keep as a protocol snapshot.


## Crash bug repair

- Systems: 1

- Paradigm mix: Procedural=1

- Metric mix: repair accuracy=1

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, `single-hunk`, or `function-level`): 0

- Comparability interpretation: singleton row; keep as a protocol snapshot.


## Other

- Systems: 24

- Paradigm mix: Fine-Tuning=8, Prompting=9, Procedural=5, Agentic=2

- Metric mix: pass@1000=1, pass@1=6, pass@5=5, F1=1, pass@10=2, full match=4, pass@30=1, pass@300=1, avg@5=1, merged PRs=1, accept@1=1

- Explicit `Perfect Fault Localization` assumptions: 2

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 2

- Comparability interpretation: not rankable as a group because the rows use smaller or domain-specific datasets, and apparent metric matches occur across different benchmarks.
