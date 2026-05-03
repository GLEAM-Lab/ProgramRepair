# Benchmark Family Breakdown

This file aggregates the final 66-system audit table into benchmark-family-level summaries so that the benchmark-protocol claims in the current manuscript can be checked directly. Counts are derived from `artifact/taxonomy_assignment_audit.csv`.

## Defects4J

- Systems: 12

- Paradigm mix: Fine-Tuning=4, Prompting=3, Procedural=3, Agentic=2

- Metric mix: pass@5=1, pass@10=2, pass@1000=1, pass@1=2, top@k (5h)=1, pass@200=1, pass@500=1, pass@25=1, pass@5000=1, pass@16=1

- Explicit `Perfect Fault Localization` assumptions: 6

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 10


## HumanEval-Java

- Systems: 8

- Paradigm mix: Fine-Tuning=6, Prompting=1, Procedural=1

- Metric mix: pass@10=5, pass@100=1, accuracy=1, pass@40=1

- Explicit `Perfect Fault Localization` assumptions: 4

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 4


## SWE-bench Lite

- Systems: 8

- Paradigm mix: Procedural=2, Agentic=6

- Metric mix: pass@1=8

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 0


## SWE-bench Verified

- Systems: 1

- Paradigm mix: Fine-Tuning=1

- Metric mix: pass@1=1

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 0


## SWE-bench Other

- Systems: 2

- Paradigm mix: Agentic=2

- Metric mix: pass@1=2

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 0


## Vulnerability repair datasets

- Systems: 9

- Paradigm mix: Fine-Tuning=2, Prompting=3, Procedural=3, Agentic=1

- Metric mix: full match=1, pass@10=1, F1=1, pass@5=1, pass@1=2, CodeBLEU=1, EM=1, success rate=1

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, `single-hunk`, or `function-level`): 1


## API misuse repair

- Systems: 1

- Paradigm mix: Prompting=1

- Metric mix: EM=1

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, `single-hunk`, or `function-level`): 0


## Crash bug repair

- Systems: 1

- Paradigm mix: Procedural=1

- Metric mix: repair accuracy=1

- Explicit `Perfect Fault Localization` assumptions: 0

- Narrowed settings (`Perfect Fault Localization`, `single-function`, `single-hunk`, or `function-level`): 0


## Other

- Systems: 24

- Paradigm mix: Fine-Tuning=8, Prompting=9, Procedural=5, Agentic=2

- Metric mix: pass@1000=1, pass@1=6, pass@5=5, F1=1, pass@10=2, full match=4, pass@30=1, pass@300=1, avg@5=1, merged PRs=1, accept@1=1

- Explicit `Perfect Fault Localization` assumptions: 2

- Narrowed settings (`Perfect Fault Localization`, `single-function`, or `single-hunk`): 2
