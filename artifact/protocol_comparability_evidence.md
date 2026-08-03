# Protocol-Comparability Attrition Evidence

This analysis treats each unordered pair of reported system results as a potential comparison. It asks how often sharing the same recorded benchmark label is sufficient for a defensible comparison after metric, assumption, model, and protocol auditing.

## Main result

- The 66-system corpus contains 2145 possible result pairs.
- Only 100 pairs share an exact recorded benchmark label.
- Of those 100 superficially comparable pairs, only 32 (32.0%) fall inside a defined protocol-aligned comparison window; 68 (68.0%) fall outside the predefined windows.
- Of the 32 protocol-aligned pairs, 4 also share a normalized base model, and only 1 meets the model-controlled definition.
- In this audit, a model-controlled pair must share the normalized benchmark variant, exact metric and candidate budget, normalized base model, and comparable fault-localization and oracle assumptions. Training data, adaptation objective, and workflow details remain possible confounders.
- The sole model-controlled pair is MORepair versus Luo et al. on EvalRepair-Java; both are classified as Fine-Tuning. No model-controlled cross-paradigm pair exists.
- Strength matters: 28/100 are protocol-aligned whole-stack snapshots, and 3/100 are limited within-benchmark comparisons.

## Why benchmark names are insufficient

Among the 100 same-benchmark pairs:

- 34/100 share the exact metric.
- 51/100 share only the broader metric family.
- 47/100 share the same evaluation-assumption bucket.
- 12/100 share the normalized base model.

These diagnostics are not a sequential filter. They show which protocol dimensions create the apparent comparability problem.

## Benchmark-specific evidence

- Defects4J v1.2/2.0 contributes 55 same-label pairs but 0 aligned pairs. Reported rows mix pass@1, pass@5, pass@10, pass@25, pass@32, pass@500, pass@1000, pass@5000, and time-budgeted pass@k, together with perfect fault localization, single-function, single-hunk, and non-narrowed settings.
- HumanEval-Java contributes 15 same-label pairs, of which 3 form the limited pass@10 adapter-tuning window.
- SWE-bench Lite contributes 28 pass@1 pairs, all retained as protocol-aligned whole-stack snapshots. They remain unsuitable for isolating paradigm effects because base models, search, retrieval, cost, and validation policies differ.
- EvalRepair-Java contributes the sole model-controlled pair in the current corpus.

## Contribution implication

The contribution is not the generic observation that evaluation is difficult. The evidence shows that a benchmark-frequency view permits 100 apparent same-benchmark pairings, whereas result-level protocol coding supports only 32 bounded pairings, and only one meets the model-controlled definition. This is the measurable analytical consequence of the survey's protocol-comparability layer.
