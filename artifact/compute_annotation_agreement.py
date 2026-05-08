#!/usr/bin/env python3
"""Compute agreement statistics from the human taxonomy annotation sheet."""

from __future__ import annotations

import csv
import math
import sys
from collections import Counter
from pathlib import Path


TRACKED_FIELDS = [
    ("display_paradigm", "kappa"),
    ("control_subtype", "kappa"),
    ("retrieval_tag", "kappa"),
    ("analysis_tag", "kappa"),
    ("deployment_scenario", "raw"),
]

THREE_CODER_FIELDS = [
    "display_paradigm",
    "control_subtype",
    "deployment_scenario",
]


def normalize(value: str) -> str:
    return value.strip()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def paired_values(rows: list[dict[str, str]], field: str) -> list[tuple[str, str, str]]:
    pairs = []
    for row in rows:
        left = normalize(row.get(f"coder_1_{field}", ""))
        right = normalize(row.get(f"coder_2_{field}", ""))
        if left and right:
            pairs.append((row["system"], left, right))
    return pairs


def raw_agreement(pairs: list[tuple[str, str, str]]) -> tuple[int, int, float]:
    matches = sum(1 for _, left, right in pairs if left == right)
    total = len(pairs)
    rate = matches / total if total else math.nan
    return matches, total, rate


def cohens_kappa(pairs: list[tuple[str, str, str]]) -> float:
    if not pairs:
        return math.nan
    total = len(pairs)
    observed = sum(1 for _, left, right in pairs if left == right) / total
    left_counts = Counter(left for _, left, _ in pairs)
    right_counts = Counter(right for _, _, right in pairs)
    categories = set(left_counts) | set(right_counts)
    expected = sum((left_counts[c] / total) * (right_counts[c] / total) for c in categories)
    if math.isclose(1.0, expected):
        return 1.0 if math.isclose(observed, 1.0) else math.nan
    return (observed - expected) / (1 - expected)


def fleiss_kappa(label_sets: list[list[str]]) -> tuple[float, float]:
    """Return Fleiss' kappa and mean observed agreement."""
    complete = [labels for labels in label_sets if all(labels)]
    if not complete:
        return math.nan, math.nan

    n_raters = len(complete[0])
    if n_raters < 2:
        return math.nan, math.nan

    categories = sorted({label for labels in complete for label in labels})
    total_subjects = len(complete)
    category_totals = Counter()
    observed_per_subject: list[float] = []

    for labels in complete:
        counts = Counter(labels)
        category_totals.update(counts)
        observed = sum(count * (count - 1) for count in counts.values()) / (n_raters * (n_raters - 1))
        observed_per_subject.append(observed)

    p_bar = sum(observed_per_subject) / total_subjects
    p_expected = sum((category_totals[category] / (total_subjects * n_raters)) ** 2 for category in categories)
    if math.isclose(1.0, p_expected):
        return (1.0 if math.isclose(1.0, p_bar) else math.nan), p_bar
    return (p_bar - p_expected) / (1 - p_expected), p_bar


def disagreement_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    flagged = []
    for row in rows:
        disagreements = []
        for field, _ in TRACKED_FIELDS:
            left = normalize(row.get(f"coder_1_{field}", ""))
            right = normalize(row.get(f"coder_2_{field}", ""))
            if left and right and left != right:
                disagreements.append(field)
        if disagreements:
            flagged.append(
                {
                    "system": row["system"],
                    "fields": ", ".join(disagreements),
                    "coder_1_display_paradigm": row.get("coder_1_display_paradigm", ""),
                    "coder_2_display_paradigm": row.get("coder_2_display_paradigm", ""),
                    "coder_1_control_subtype": row.get("coder_1_control_subtype", ""),
                    "coder_2_control_subtype": row.get("coder_2_control_subtype", ""),
                    "coder_1_deployment_scenario": row.get("coder_1_deployment_scenario", ""),
                    "coder_2_deployment_scenario": row.get("coder_2_deployment_scenario", ""),
                }
            )
    return flagged


def print_summary(rows: list[dict[str, str]]) -> None:
    print("Agreement summary")
    print("=================")
    for field, mode in TRACKED_FIELDS:
        pairs = paired_values(rows, field)
        matches, total, rate = raw_agreement(pairs)
        if total == 0:
            print(f"- {field}: no paired labels yet")
            continue
        if mode == "kappa":
            kappa = cohens_kappa(pairs)
            print(f"- {field}: {matches}/{total} agreement ({rate:.1%}), Cohen's kappa = {kappa:.3f}")
        else:
            print(f"- {field}: {matches}/{total} agreement ({rate:.1%})")

    flagged = disagreement_rows(rows)
    print()
    print(f"Rows with at least one disagreement: {len(flagged)}")
    if not flagged:
        return

    print()
    print("Disagreement details")
    print("====================")
    for row in flagged:
        print(
            f"- {row['system']}: {row['fields']} | "
            f"paradigm [{row['coder_1_display_paradigm']}] vs [{row['coder_2_display_paradigm']}] | "
            f"control [{row['coder_1_control_subtype']}] vs [{row['coder_2_control_subtype']}] | "
            f"scenario [{row['coder_1_deployment_scenario']}] vs [{row['coder_2_deployment_scenario']}]"
        )


def three_coder_rows_available(rows: list[dict[str, str]]) -> bool:
    if not rows:
        return False
    fields = rows[0].keys()
    return all(
        f"{prefix}_{field}" in fields
        for field in THREE_CODER_FIELDS
        for prefix in ("original", "coder_2", "coder_3")
    )


def three_coder_pair(rows: list[dict[str, str]], field: str, left_prefix: str, right_prefix: str) -> list[tuple[str, str, str]]:
    pairs = []
    for row in rows:
        left = normalize(row.get(f"{left_prefix}_{field}", ""))
        right = normalize(row.get(f"{right_prefix}_{field}", ""))
        if left and right:
            pairs.append((row["system"], left, right))
    return pairs


def print_three_coder_summary(rows: list[dict[str, str]]) -> None:
    pair_names = [
        ("existing vs external coder 1", "original", "coder_2"),
        ("existing vs external coder 2", "original", "coder_3"),
        ("external coder 1 vs external coder 2", "coder_2", "coder_3"),
    ]

    print("Three-coder taxonomy agreement summary")
    print("======================================")
    print()
    print("Pairwise agreement")
    print("------------------")
    for field in THREE_CODER_FIELDS:
        for label, left_prefix, right_prefix in pair_names:
            pairs = three_coder_pair(rows, field, left_prefix, right_prefix)
            matches, total, rate = raw_agreement(pairs)
            kappa = cohens_kappa(pairs)
            print(f"- {field}, {label}: {matches}/{total} agreement ({rate:.1%}), Cohen's kappa = {kappa:.3f}")
        print()

    print("Fleiss kappa")
    print("------------")
    for field in THREE_CODER_FIELDS:
        label_sets = [
            [
                normalize(row.get(f"original_{field}", "")),
                normalize(row.get(f"coder_2_{field}", "")),
                normalize(row.get(f"coder_3_{field}", "")),
            ]
            for row in rows
        ]
        kappa, observed = fleiss_kappa(label_sets)
        total = sum(1 for labels in label_sets if all(labels))
        print(f"- {field}: {total} subjects, Fleiss' kappa = {kappa:.3f}, mean observed agreement = {observed:.1%}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 artifact/compute_annotation_agreement.py <annotation_csv>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    rows = load_rows(path)
    if three_coder_rows_available(rows):
        print_three_coder_summary(rows)
    else:
        print_summary(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
