# Benchmark Protocol Summary

This summary aggregates the 66-system audit table used in the revised manuscript (`revised_submission/11.threats.tex`) to make benchmark fragmentation easier to inspect.

## Metric families

Among the 66 retained systems:

- 21 report `pass@1`
- 28 report `pass@k` for `k > 1`
- 5 report `full match`
- 2 report `F1`
- 1 reports `top@k`
- 1 reports `accuracy`
- 1 reports `avg@5`
- 1 reports `merged PRs`
- 1 reports `CodeBLEU`
- 1 reports `accept@1`
- 2 report `EM`
- 1 reports `success rate`
- 1 reports `repair accuracy`

This explains why cross-paper ranking is difficult even within the same benchmark family.

## Explicit assumptions in the 66-system audit table

- 12 systems explicitly assume `Perfect Fault Localization`
- 3 systems explicitly narrow the task to `single-function` repair
- 1 system explicitly narrows the task to `single-hunk` repair
- 1 system explicitly reports a function-level vulnerability-patch setting
- 2 systems explicitly require human feedback or tutor guidance
- 8 systems explicitly frame evaluation around a train/test split

Taken together, at least 16 systems use a narrowed setup that is weaker than fully end-to-end repair, even before considering differences in sampling budget, benchmark version, or oracle strength.

## Selected recurring benchmark families in the 66-system table

- `Defects4J` family (`v1.2` plus `v1.2/2.0`): 12 systems
- `HumanEval-Java`: 8 systems
- `SWE-bench Lite`: 8 systems
- `SWE-bench Verified`: 1 directly benchmarked system
- `Vulnerability repair datasets`: 9 systems across eight metric families
- `API misuse repair`: 1 system
- `Crash bug repair`: 1 system

The remaining systems are spread across many smaller or domain-specific datasets, which is one reason vulnerability-repair and educational-repair results remain hard to compare globally. The more detailed family-by-family counts are summarized in `benchmark_family_breakdown.md`.
