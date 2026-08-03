#!/usr/bin/env python3
"""Quantify how many same-benchmark result pairs survive protocol auditing."""

from __future__ import annotations

import csv
import itertools
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "benchmark_protocol_comparability_by_system.csv"
PAIRWISE_OUT = ROOT / "protocol_comparability_pairwise.csv"
SUMMARY_OUT = ROOT / "protocol_comparability_attrition.csv"
REPORT_OUT = ROOT / "protocol_comparability_evidence.md"


def read_rows() -> list[dict[str, str]]:
    with INPUT.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 66:
        raise RuntimeError(f"Expected 66 systems, found {len(rows)}")
    return rows


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = read_rows()
    all_pairs = list(itertools.combinations(rows, 2))
    same_benchmark = [pair for pair in all_pairs if pair[0]["benchmark"] == pair[1]["benchmark"]]

    pairwise_rows: list[dict[str, object]] = []
    for left, right in same_benchmark:
        same_window = (
            left["comparison_windows"] != "None"
            and left["comparison_windows"] == right["comparison_windows"]
        )
        tier = left["comparability_tier"] if same_window else "D_same_benchmark_not_aligned"
        pairwise_rows.append(
            {
                "system_a": left["system"],
                "system_b": right["system"],
                "benchmark": left["benchmark"],
                "same_exact_metric": "yes" if left["metric"] == right["metric"] else "no",
                "same_metric_family": (
                    "yes" if left["metric_family"] == right["metric_family"] else "no"
                ),
                "same_assumption_bucket": (
                    "yes" if left["assumption_bucket"] == right["assumption_bucket"] else "no"
                ),
                "same_normalized_base_model": (
                    "yes" if left["normalized_base_model"] == right["normalized_base_model"] else "no"
                ),
                "protocol_aligned_window": "yes" if same_window else "no",
                "comparison_window": left["comparison_windows"] if same_window else "None",
                "comparability_tier": tier,
            }
        )

    write_rows(PAIRWISE_OUT, pairwise_rows)

    aligned = [row for row in pairwise_rows if row["protocol_aligned_window"] == "yes"]
    aligned_same_model = [
        row for row in aligned if row["same_normalized_base_model"] == "yes"
    ]
    tier_counts = Counter(row["comparability_tier"] for row in aligned)
    benchmark_counts = Counter(row["benchmark"] for row in pairwise_rows)
    benchmark_aligned = Counter(row["benchmark"] for row in aligned)
    model_controlled = [
        row
        for row in pairwise_rows
        if row["comparability_tier"] == "A_model_controlled_comparison"
    ]
    expected_model_controlled_pair = {
        "system_a": "MORepair",
        "system_b": "Luo et al.",
        "benchmark": "EvalRepair-Java",
    }
    observed_model_controlled_pairs = [
        {key: row[key] for key in expected_model_controlled_pair}
        for row in model_controlled
    ]
    expected_attrition = (2145, 100, 32, 4, 1)
    observed_attrition = (
        len(all_pairs),
        len(pairwise_rows),
        len(aligned),
        len(aligned_same_model),
        len(model_controlled),
    )
    if observed_attrition != expected_attrition:
        raise RuntimeError(
            f"Protocol-comparability attrition changed: expected {expected_attrition}, "
            f"found {observed_attrition}"
        )
    if observed_model_controlled_pairs != [expected_model_controlled_pair]:
        raise RuntimeError(
            "Model-controlled pair changed: expected MORepair vs Luo et al. "
            f"on EvalRepair-Java, found {observed_model_controlled_pairs}"
        )

    summary_rows: list[dict[str, object]] = [
        {
            "scope": "all_system_pairs",
            "measure": "all possible pairs among 66 systems",
            "count": len(all_pairs),
            "denominator": len(all_pairs),
            "percent": "100.0%",
        },
        {
            "scope": "same_benchmark_pairs",
            "measure": "pairs sharing the exact recorded benchmark label",
            "count": len(pairwise_rows),
            "denominator": len(all_pairs),
            "percent": f"{100 * len(pairwise_rows) / len(all_pairs):.1f}%",
        },
        {
            "scope": "same_benchmark_pairs",
            "measure": "pairs retained in a protocol-aligned comparison window",
            "count": len(aligned),
            "denominator": len(pairwise_rows),
            "percent": f"{100 * len(aligned) / len(pairwise_rows):.1f}%",
        },
        {
            "scope": "same_benchmark_pairs",
            "measure": "same-benchmark pairs outside predefined windows",
            "count": len(pairwise_rows) - len(aligned),
            "denominator": len(pairwise_rows),
            "percent": f"{100 * (len(pairwise_rows) - len(aligned)) / len(pairwise_rows):.1f}%",
        },
        {
            "scope": "sequential_attrition",
            "measure": "protocol-aligned pairs also sharing a normalized base model",
            "count": len(aligned_same_model),
            "denominator": len(aligned),
            "percent": f"{100 * len(aligned_same_model) / len(aligned):.1f}%",
        },
        {
            "scope": "sequential_attrition",
            "measure": "same-model aligned pairs meeting the model-controlled definition",
            "count": tier_counts["A_model_controlled_comparison"],
            "denominator": len(aligned_same_model),
            "percent": f"{100 * tier_counts['A_model_controlled_comparison'] / len(aligned_same_model):.1f}%",
        },
    ]

    diagnostics = [
        ("same exact metric", "same_exact_metric"),
        ("same metric family", "same_metric_family"),
        ("same assumption bucket", "same_assumption_bucket"),
        ("same normalized base model", "same_normalized_base_model"),
    ]
    for label, field in diagnostics:
        count = sum(row[field] == "yes" for row in pairwise_rows)
        summary_rows.append(
            {
                "scope": "same_benchmark_pairs_diagnostic",
                "measure": label,
                "count": count,
                "denominator": len(pairwise_rows),
                "percent": f"{100 * count / len(pairwise_rows):.1f}%",
            }
        )

    for tier in (
        "A_model_controlled_comparison",
        "B_protocol_aligned_stack_snapshot",
        "C_limited_within_benchmark_comparison",
    ):
        count = tier_counts[tier]
        summary_rows.append(
            {
                "scope": "aligned_pair_strength",
                "measure": tier,
                "count": count,
                "denominator": len(pairwise_rows),
                "percent": f"{100 * count / len(pairwise_rows):.1f}%",
            }
        )

    for benchmark, count in sorted(benchmark_counts.items(), key=lambda item: (-item[1], item[0])):
        retained = benchmark_aligned[benchmark]
        summary_rows.append(
            {
                "scope": "benchmark_breakdown",
                "measure": f"{benchmark}: aligned pairs",
                "count": retained,
                "denominator": count,
                "percent": f"{100 * retained / count:.1f}%",
            }
        )

    write_rows(SUMMARY_OUT, summary_rows)

    report = f"""# Protocol-Comparability Attrition Evidence

This analysis treats each unordered pair of reported system results as a potential comparison. It asks how often sharing the same recorded benchmark label is sufficient for a defensible comparison after metric, assumption, model, and protocol auditing.

## Main result

- The 66-system corpus contains {len(all_pairs)} possible result pairs.
- Only {len(pairwise_rows)} pairs share an exact recorded benchmark label.
- Of those {len(pairwise_rows)} superficially comparable pairs, only {len(aligned)} ({100 * len(aligned) / len(pairwise_rows):.1f}%) fall inside a defined protocol-aligned comparison window; {len(pairwise_rows) - len(aligned)} ({100 * (len(pairwise_rows) - len(aligned)) / len(pairwise_rows):.1f}%) fall outside the predefined windows.
- Of the {len(aligned)} protocol-aligned pairs, {len(aligned_same_model)} also share a normalized base model, and only {tier_counts['A_model_controlled_comparison']} meets the model-controlled definition.
- In this audit, a model-controlled pair must share the normalized benchmark variant, exact metric and candidate budget, normalized base model, and comparable fault-localization and oracle assumptions. Training data, adaptation objective, and workflow details remain possible confounders.
- The sole model-controlled pair is MORepair versus Luo et al. on EvalRepair-Java; both are classified as Fine-Tuning. No model-controlled cross-paradigm pair exists.
- Strength matters: {tier_counts['B_protocol_aligned_stack_snapshot']}/{len(pairwise_rows)} are protocol-aligned whole-stack snapshots, and {tier_counts['C_limited_within_benchmark_comparison']}/{len(pairwise_rows)} are limited within-benchmark comparisons.

## Why benchmark names are insufficient

Among the {len(pairwise_rows)} same-benchmark pairs:

- {sum(row['same_exact_metric'] == 'yes' for row in pairwise_rows)}/{len(pairwise_rows)} share the exact metric.
- {sum(row['same_metric_family'] == 'yes' for row in pairwise_rows)}/{len(pairwise_rows)} share only the broader metric family.
- {sum(row['same_assumption_bucket'] == 'yes' for row in pairwise_rows)}/{len(pairwise_rows)} share the same evaluation-assumption bucket.
- {sum(row['same_normalized_base_model'] == 'yes' for row in pairwise_rows)}/{len(pairwise_rows)} share the normalized base model.

These diagnostics are not a sequential filter. They show which protocol dimensions create the apparent comparability problem.

## Benchmark-specific evidence

- Defects4J v1.2/2.0 contributes {benchmark_counts['Defects4J v1.2/2.0']} same-label pairs but {benchmark_aligned['Defects4J v1.2/2.0']} aligned pairs. Reported rows mix pass@1, pass@5, pass@10, pass@25, pass@32, pass@500, pass@1000, pass@5000, and time-budgeted pass@k, together with perfect fault localization, single-function, single-hunk, and non-narrowed settings.
- HumanEval-Java contributes {benchmark_counts['HumanEval-Java']} same-label pairs, of which {benchmark_aligned['HumanEval-Java']} form the limited pass@10 adapter-tuning window.
- SWE-bench Lite contributes {benchmark_counts['SWE-bench Lite']} pass@1 pairs, all retained as protocol-aligned whole-stack snapshots. They remain unsuitable for isolating paradigm effects because base models, search, retrieval, cost, and validation policies differ.
- EvalRepair-Java contributes the sole model-controlled pair in the current corpus.

## Contribution implication

The contribution is not the generic observation that evaluation is difficult. The evidence shows that a benchmark-frequency view permits 100 apparent same-benchmark pairings, whereas result-level protocol coding supports only 32 bounded pairings, and only one meets the model-controlled definition. This is the measurable analytical consequence of the survey's protocol-comparability layer.
"""
    REPORT_OUT.write_text(report, encoding="utf-8")

    print(f"Wrote {PAIRWISE_OUT.name} ({len(pairwise_rows)} rows)")
    print(f"Wrote {SUMMARY_OUT.name} ({len(summary_rows)} rows)")
    print(f"Wrote {REPORT_OUT.name}")


if __name__ == "__main__":
    main()
